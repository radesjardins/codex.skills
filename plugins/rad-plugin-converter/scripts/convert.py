from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from audit import (
    AUTHOR_FIELDS,
    MCP_SCHEMA,
    PLUGIN_FIELDS,
    PLUGIN_NAME_RE,
    PLUGIN_SCHEMA,
    audit_path,
)
from frontmatter import audit_frontmatter, repair_skill_name
from models import ConversionResult, Finding


CLAUDE_ROOT = "${CLAUDE_PLUGIN_ROOT}"
PORTABLE_ROOT = "${PLUGIN_ROOT}"


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _atomic_write_text(path: Path, text: str) -> bool:
    try:
        current = path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        current = None
    if current == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise
    return True


def _atomic_write_json(path: Path, value: object) -> bool:
    return _atomic_write_text(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def _read_json(path: Path, root: Path) -> tuple[dict[str, Any] | None, Finding | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except OSError as exc:
        return None, Finding("error", "conversion-read", _relative(path, root), str(exc))
    except json.JSONDecodeError as exc:
        return None, Finding(
            "error",
            "conversion-json",
            _relative(path, root),
            f"Invalid JSON: {exc.msg}.",
            exc.lineno,
        )
    if not isinstance(data, dict):
        return None, Finding(
            "error",
            "conversion-json-type",
            _relative(path, root),
            "Source manifest must contain a JSON object.",
        )
    return data, None


def _source_manifest(root: Path) -> tuple[dict[str, Any] | None, Path | None, Finding | None]:
    candidates = (
        root / "plugin.json",
        root / ".codex-plugin" / "plugin.json",
        root / ".claude-plugin" / "plugin.json",
    )
    for path in candidates:
        if path.is_file():
            data, finding = _read_json(path, root)
            return data, path, finding
    return None, None, Finding(
        "error",
        "conversion-source-manifest",
        ".",
        "No plugin manifest was found.",
    )


def _portable_manifest(source: dict[str, Any], source_path: Path, root: Path) -> tuple[dict[str, Any] | None, list[Finding]]:
    findings: list[Finding] = []
    name = source.get("name")
    if not isinstance(name, str) or not (1 <= len(name) <= 64) or not PLUGIN_NAME_RE.fullmatch(name):
        return None, [
            Finding(
                "error",
                "conversion-plugin-name",
                _relative(source_path, root),
                "Source plugin name cannot be used as an Agent Plugins 1.0.0 name.",
            )
        ]

    result: dict[str, Any] = {"$schema": PLUGIN_SCHEMA, "name": name}
    for field in ("version", "description", "homepage", "repository", "license"):
        value = source.get(field)
        if isinstance(value, str):
            result[field] = value
        elif field in source:
            findings.append(
                Finding(
                    "warning",
                    "conversion-field-omitted",
                    _relative(source_path, root),
                    f"Non-string field '{field}' was omitted from the portable manifest.",
                )
            )

    author = source.get("author")
    if isinstance(author, dict):
        portable_author = {
            key: value
            for key, value in author.items()
            if key in AUTHOR_FIELDS and isinstance(value, str)
        }
        if portable_author:
            result["author"] = portable_author
        if portable_author != author:
            findings.append(
                Finding(
                    "warning",
                    "conversion-author-field-omitted",
                    _relative(source_path, root),
                    "Unsupported or non-string author fields were omitted from the portable manifest.",
                )
            )
    elif "author" in source:
        findings.append(
            Finding(
                "warning",
                "conversion-field-omitted",
                _relative(source_path, root),
                "Non-object author field was omitted from the portable manifest.",
            )
        )

    keywords = source.get("keywords")
    if isinstance(keywords, list) and all(isinstance(value, str) for value in keywords):
        result["keywords"] = keywords
    elif "keywords" in source:
        findings.append(
            Finding(
                "warning",
                "conversion-field-omitted",
                _relative(source_path, root),
                "Invalid keywords were omitted from the portable manifest.",
            )
        )

    extensions = source.get("extensions")
    if isinstance(extensions, dict) and all(isinstance(value, dict) for value in extensions.values()):
        result["extensions"] = extensions
    elif "extensions" in source:
        findings.append(
            Finding(
                "warning",
                "conversion-field-omitted",
                _relative(source_path, root),
                "Invalid extensions were omitted from the portable manifest.",
            )
        )

    for field in sorted(set(source) - PLUGIN_FIELDS):
        if source_path.name == "plugin.json" and source_path.parent == root:
            findings.append(
                Finding(
                    "warning",
                    "conversion-client-field-omitted",
                    "plugin.json",
                    f"Client field '{field}' was omitted from the portable manifest.",
                )
            )
    return result, findings


def _portable_value(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace(CLAUDE_ROOT, PORTABLE_ROOT)
    if isinstance(value, list):
        return [_portable_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _portable_value(item) for key, item in value.items()}
    return value


def _convert_mcp(root: Path) -> tuple[dict[str, Any] | None, list[Finding]]:
    source_path = root / ".mcp.json"
    if not source_path.is_file() or (root / "mcp.json").exists():
        return None, []
    source, read_finding = _read_json(source_path, root)
    if read_finding is not None:
        return None, [read_finding]
    assert source is not None
    servers = source.get("mcpServers")
    if not isinstance(servers, dict):
        return None, [
            Finding("error", "conversion-mcp-servers", ".mcp.json", "mcpServers must be an object.")
        ]

    converted: dict[str, Any] = {}
    findings: list[Finding] = []
    for name, raw_server in servers.items():
        if not isinstance(name, str) or not isinstance(raw_server, dict):
            findings.append(
                Finding("error", "conversion-mcp-server", ".mcp.json", "Every MCP server must be a named object.")
            )
            continue
        server = _portable_value(raw_server)
        transport = server.get("type")
        if transport is None and "command" in server:
            server = {"type": "stdio", **server}
        elif transport is None and "url" in server:
            findings.append(
                Finding(
                    "error",
                    "conversion-mcp-transport",
                    ".mcp.json",
                    f"MCP server '{name}' needs an explicit streamable-http or sse transport.",
                )
            )
            continue
        converted[name] = server
    if findings:
        return None, findings
    return {"$schema": MCP_SCHEMA, "mcpServers": converted}, []


def _repair_skills(root: Path) -> list[str]:
    changed: list[str] = []
    skills = root / "skills"
    if not skills.is_dir():
        return changed
    for skill_dir in sorted((item for item in skills.iterdir() if item.is_dir()), key=lambda path: path.name.lower()):
        skill_path = skill_dir / "SKILL.md"
        if not skill_path.is_file():
            continue
        codes = {item.code for item in audit_frontmatter(skill_dir, root)}
        if "skill-name-mismatch" in codes and repair_skill_name(skill_dir):
            changed.append(_relative(skill_path, root))
    return changed


def convert_in_place(path: Path) -> ConversionResult:
    root = path.resolve(strict=False)
    if not root.is_dir():
        return ConversionResult(
            root=root,
            findings=[Finding("error", "conversion-root-kind", str(root), "Conversion target must be a directory.")],
        )

    if (root / "SKILL.md").is_file() and not any(
        (root / relative).is_file()
        for relative in ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json")
    ):
        changed = ["SKILL.md"] if repair_skill_name(root) else []
        report = audit_path(root)
        return ConversionResult(root=root, changed_files=changed, findings=report.findings)

    source, source_path, source_finding = _source_manifest(root)
    if source_finding is not None or source is None or source_path is None:
        return ConversionResult(root=root, findings=[source_finding] if source_finding else [])

    portable, conversion_findings = _portable_manifest(source, source_path, root)
    if portable is None:
        return ConversionResult(root=root, findings=conversion_findings)

    changed: list[str] = []
    try:
        if _atomic_write_json(root / "plugin.json", portable):
            changed.append("plugin.json")
        changed.extend(_repair_skills(root))
        mcp_data, mcp_findings = _convert_mcp(root)
        conversion_findings.extend(mcp_findings)
        if mcp_data is not None and _atomic_write_json(root / "mcp.json", mcp_data):
            changed.append("mcp.json")
    except OSError as exc:
        conversion_findings.append(Finding("error", "conversion-write", ".", str(exc)))

    final_report = audit_path(root)
    findings = conversion_findings + final_report.findings
    findings.sort(key=lambda item: (item.path.lower(), item.line or 0, item.severity, item.code))
    return ConversionResult(root=root, changed_files=list(dict.fromkeys(changed)), findings=findings)


def _copy_source(source: Path, target: Path) -> list[str]:
    ignore = shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "*.pyo")
    if target.exists():
        shutil.copytree(source, target, dirs_exist_ok=True, symlinks=True, ignore=ignore)
    else:
        shutil.copytree(source, target, symlinks=True, ignore=ignore)
    return sorted(
        item.relative_to(target).as_posix()
        for item in target.rglob("*")
        if item.is_file() or item.is_symlink()
    )


def convert_to_target(source_path: Path, target_path: Path) -> ConversionResult:
    source = source_path.resolve(strict=False)
    target = target_path.resolve(strict=False)
    if not source.is_dir():
        return ConversionResult(
            root=target,
            findings=[Finding("error", "conversion-source-kind", str(source), "Source must be a directory.")],
        )
    if target == source or target.is_relative_to(source):
        return ConversionResult(
            root=target,
            findings=[Finding("error", "conversion-target-location", str(target), "Target cannot be the source or inside it.")],
        )
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        return ConversionResult(
            root=target,
            findings=[
                Finding("error", "conversion-target-not-empty", str(target), "Target must be absent or an empty directory.")
            ],
        )

    source_report = audit_path(source)
    blocking = [item for item in source_report.findings if item.code == "package-path-escape"]
    if blocking:
        return ConversionResult(root=target, findings=blocking)
    try:
        copied = _copy_source(source, target)
    except OSError as exc:
        return ConversionResult(
            root=target,
            findings=[Finding("error", "conversion-copy", str(target), str(exc))],
        )

    converted = convert_in_place(target)
    converted.changed_files = list(dict.fromkeys(copied + converted.changed_files))
    return converted


def _marketplace_paths(root: Path) -> tuple[list[Path], Finding | None]:
    manifest_path = root / "marketplace.json"
    data, read_finding = _read_json(manifest_path, root)
    if read_finding is not None or data is None:
        return [], read_finding
    entries = data.get("plugins")
    if not isinstance(entries, list):
        return [], Finding("error", "conversion-marketplace-plugins", "marketplace.json", "plugins must be an array.")

    paths: list[Path] = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("source"), dict):
            return [], Finding("error", "conversion-marketplace-entry", "marketplace.json", "Plugin entry has no source object.")
        source = entry["source"]
        if source.get("source") != "local" or not isinstance(source.get("path"), str):
            return [], Finding("error", "conversion-marketplace-source", "marketplace.json", "Only local plugin sources can be converted.")
        candidate = (root / source["path"]).resolve(strict=False)
        if not candidate.is_relative_to(root.resolve(strict=True)):
            return [], Finding("error", "conversion-marketplace-path", "marketplace.json", "Plugin path escapes the marketplace root.")
        paths.append(candidate)
    return paths, None


def convert_marketplace(path: Path, apply: bool) -> list[ConversionResult]:
    root = path.resolve(strict=False)
    plugin_paths, finding = _marketplace_paths(root)
    if finding is not None:
        return [ConversionResult(root=root, findings=[finding])]
    if apply:
        return [convert_in_place(plugin_path) for plugin_path in plugin_paths]
    return [
        ConversionResult(root=plugin_path, findings=audit_path(plugin_path).findings)
        for plugin_path in plugin_paths
    ]
