from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from models import Finding


ALLOWED_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
SKILL_NAME_RE = re.compile(r"^(?!.*--)[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:[ \t]*(.*))?$")
INTEGER_RE = re.compile(r"^[+-]?[0-9]+$")
FLOAT_RE = re.compile(r"^[+-]?(?:[0-9]+\.[0-9]*|[0-9]*\.[0-9]+)$")


class FrontmatterError(ValueError):
    pass


@dataclass(slots=True)
class FrontmatterDocument:
    path: Path
    values: dict[str, Any]
    key_lines: dict[str, int]
    end_line: int


def _parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if not value:
        return ""
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise FrontmatterError(f"Invalid double-quoted scalar: {exc.msg}") from exc
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    lower = value.lower()
    if lower in {"true", "false"}:
        return lower == "true"
    if lower in {"null", "~"}:
        return None
    if INTEGER_RE.fullmatch(value):
        return int(value)
    if FLOAT_RE.fullmatch(value):
        return float(value)
    if value.startswith("[") or value.startswith("{"):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _block_value(lines: list[str], start: int, style: str) -> tuple[str, int]:
    collected: list[str] = []
    index = start
    while index < len(lines):
        line = lines[index]
        if line and not line[0].isspace():
            break
        collected.append(line)
        index += 1

    nonempty = [len(line) - len(line.lstrip()) for line in collected if line.strip()]
    indent = min(nonempty) if nonempty else 0
    content = [line[indent:] if line.strip() else "" for line in collected]
    if style.startswith(">"):
        value = " ".join(part.strip() for part in content).strip()
    else:
        value = "\n".join(content).strip("\n")
    return value, index


def _metadata_value(lines: list[str], start: int) -> tuple[dict[str, Any], int]:
    metadata: dict[str, Any] = {}
    index = start
    while index < len(lines):
        line = lines[index]
        if line and not line[0].isspace():
            break
        if not line.strip():
            index += 1
            continue
        stripped = line.lstrip()
        if len(line) - len(stripped) < 2:
            raise FrontmatterError("Metadata entries must be indented by at least two spaces")
        match = KEY_RE.fullmatch(stripped)
        if not match:
            raise FrontmatterError(f"Invalid metadata entry on line {index + 2}")
        key, raw_value = match.group(1), match.group(2) or ""
        if key in metadata:
            raise FrontmatterError(f"Duplicate metadata key: {key}")
        metadata[key] = _parse_scalar(raw_value)
        index += 1
    return metadata, index


def parse_frontmatter(path: Path) -> FrontmatterDocument:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("SKILL.md must start with YAML frontmatter")

    try:
        end_index = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration as exc:
        raise FrontmatterError("YAML frontmatter has no closing delimiter") from exc

    frontmatter_lines = lines[1:end_index]
    values: dict[str, Any] = {}
    key_lines: dict[str, int] = {}
    index = 0
    while index < len(frontmatter_lines):
        line = frontmatter_lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        if line[0].isspace():
            raise FrontmatterError(f"Unexpected indentation on line {index + 2}")
        match = KEY_RE.fullmatch(line)
        if not match:
            raise FrontmatterError(f"Invalid frontmatter entry on line {index + 2}")
        key, raw_value = match.group(1), (match.group(2) or "").strip()
        if key in values:
            raise FrontmatterError(f"Duplicate frontmatter field: {key}")
        key_lines[key] = index + 2
        if key == "metadata" and not raw_value:
            value, next_index = _metadata_value(frontmatter_lines, index + 1)
        elif raw_value in {">", ">-", ">+", "|", "|-", "|+"}:
            value, next_index = _block_value(frontmatter_lines, index + 1, raw_value)
        else:
            value = _parse_scalar(raw_value)
            next_index = index + 1
        values[key] = value
        index = next_index

    return FrontmatterDocument(
        path=path,
        values=values,
        key_lines=key_lines,
        end_line=end_index + 1,
    )


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _type_finding(
    findings: list[Finding],
    path: str,
    document: FrontmatterDocument,
    field: str,
    expected: str,
) -> None:
    findings.append(
        Finding(
            "error",
            f"skill-{field}-type",
            path,
            f"Frontmatter field '{field}' must be {expected}.",
            document.key_lines.get(field),
        )
    )


def audit_frontmatter(skill_dir: Path, plugin_root: Path) -> list[Finding]:
    skill_path = skill_dir / "SKILL.md"
    rel = _relative(skill_path, plugin_root)
    if not skill_path.is_file():
        return [Finding("error", "missing-skill-md", rel, "Skill directory has no regular SKILL.md file.")]

    try:
        document = parse_frontmatter(skill_path)
    except (OSError, UnicodeError, FrontmatterError) as exc:
        return [Finding("error", "skill-frontmatter", rel, str(exc))]

    findings: list[Finding] = []
    unknown = sorted(set(document.values) - ALLOWED_FIELDS)
    for field in unknown:
        findings.append(
            Finding(
                "error",
                "skill-unknown-field",
                rel,
                f"Unsupported Agent Skills frontmatter field: {field}.",
                document.key_lines.get(field),
            )
        )

    name = document.values.get("name")
    if not isinstance(name, str):
        _type_finding(findings, rel, document, "name", "a string")
    elif not (1 <= len(name) <= 64) or not SKILL_NAME_RE.fullmatch(name):
        findings.append(
            Finding("error", "skill-name", rel, "Skill name does not meet Agent Skills naming rules.", document.key_lines.get("name"))
        )
    elif name != skill_dir.name:
        findings.append(
            Finding(
                "error",
                "skill-name-mismatch",
                rel,
                f"Skill name '{name}' does not match directory '{skill_dir.name}'.",
                document.key_lines.get("name"),
            )
        )

    description = document.values.get("description")
    if not isinstance(description, str):
        _type_finding(findings, rel, document, "description", "a string")
    elif not (1 <= len(description.strip()) <= 1024):
        findings.append(
            Finding(
                "error",
                "skill-description-length",
                rel,
                "Skill description must contain 1 to 1024 characters.",
                document.key_lines.get("description"),
            )
        )

    for field in ("license", "allowed-tools"):
        value = document.values.get(field)
        if field in document.values and not isinstance(value, str):
            _type_finding(findings, rel, document, field, "a string")

    compatibility = document.values.get("compatibility")
    if "compatibility" in document.values:
        if not isinstance(compatibility, str):
            _type_finding(findings, rel, document, "compatibility", "a string")
        elif not (1 <= len(compatibility.strip()) <= 500):
            findings.append(
                Finding(
                    "error",
                    "skill-compatibility-length",
                    rel,
                    "Compatibility must contain 1 to 500 characters.",
                    document.key_lines.get("compatibility"),
                )
            )

    metadata = document.values.get("metadata")
    if "metadata" in document.values:
        if not isinstance(metadata, dict):
            _type_finding(findings, rel, document, "metadata", "a string-to-string map")
        else:
            for key, value in metadata.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    findings.append(
                        Finding(
                            "error",
                            "skill-metadata-value",
                            rel,
                            "Every metadata key and value must be a string.",
                            document.key_lines.get("metadata"),
                        )
                    )
                    break
    return findings


def _atomic_write(path: Path, text: str) -> None:
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def repair_skill_name(skill_dir: Path) -> bool:
    if not SKILL_NAME_RE.fullmatch(skill_dir.name) or len(skill_dir.name) > 64:
        return False
    skill_path = skill_dir / "SKILL.md"
    document = parse_frontmatter(skill_path)
    current = document.values.get("name")
    if current == skill_dir.name or "name" not in document.key_lines:
        return False

    text = skill_path.read_text(encoding="utf-8-sig")
    lines = text.splitlines(keepends=True)
    index = document.key_lines["name"] - 1
    ending = "\r\n" if lines[index].endswith("\r\n") else "\n" if lines[index].endswith("\n") else ""
    lines[index] = f"name: {skill_dir.name}{ending}"
    _atomic_write(skill_path, "".join(lines))
    return True
