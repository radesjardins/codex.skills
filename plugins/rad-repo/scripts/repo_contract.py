#!/usr/bin/env python3
"""Discover scoped repository instructions and executable validation commands."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

CONFIG_NAME = ".rad-repo.json"
COMMAND_LABELS = ("build", "test", "lint", "type-check", "typecheck", "validate", "check")
COMMAND_RE = re.compile(
    rf"(?:{'|'.join(re.escape(label) for label in COMMAND_LABELS)})\s*:\s*`([^`]+)`",
    re.IGNORECASE,
)
PLACEHOLDER_COMMANDS = {"<command>", "none", "n/a", "not configured", "not applicable"}
IGNORED_INSTRUCTION_DIRS = {
    ".git", ".hg", ".svn", ".next", ".venv", "build", "coverage", "dist",
    "node_modules", "target", "vendor",
}


@dataclass(frozen=True)
class RepositoryContract:
    root: Path
    config: dict


def load_config(root: Path, config_path: Path | None = None) -> dict:
    path = config_path or root / CONFIG_NAME
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid repository config {path}: {error}") from error
    if not isinstance(data, dict):
        raise ValueError(f"invalid repository config {path}: root must be an object")
    return data


def load_contract(root: Path, config_path: Path | None = None) -> RepositoryContract:
    resolved = root.resolve()
    return RepositoryContract(root=resolved, config=load_config(resolved, config_path))


def all_instruction_files(root: Path) -> list[Path]:
    root = root.resolve()
    files: list[Path] = []
    for path in root.rglob("AGENTS.md"):
        relative = path.relative_to(root)
        if any(part in IGNORED_INSTRUCTION_DIRS for part in relative.parts[:-1]):
            continue
        try:
            path.resolve().relative_to(root)
        except (OSError, ValueError):
            continue
        if path.is_file():
            files.append(path)
    return sorted(files)


def applicable_instruction_files(root: Path, target: str | Path) -> list[Path]:
    root = root.resolve()
    target_path = Path(target)
    if not target_path.is_absolute():
        target_path = root / target_path
    target_path = target_path.resolve(strict=False)
    try:
        relative = target_path.relative_to(root)
    except ValueError as error:
        raise ValueError(f"target is outside repository: {target}") from error

    parent = relative if target_path.is_dir() else relative.parent
    candidates = [root / "AGENTS.md"]
    current = root
    for part in parent.parts:
        current /= part
        candidates.append(current / "AGENTS.md")
    return [path for path in candidates if path.is_file()]


def commands_from_instruction(path: Path) -> list[str]:
    commands: list[str] = []
    for match in COMMAND_RE.finditer(path.read_text(encoding="utf-8", errors="replace")):
        command = match.group(1).strip()
        if command and command.lower() not in PLACEHOLDER_COMMANDS and command not in commands:
            commands.append(command)
    return commands


def _matches_scope(path: str, scope: str) -> bool:
    normalized_path = Path(path).as_posix().strip("/")
    normalized_scope = Path(scope).as_posix().strip("/")
    return normalized_path == normalized_scope or normalized_path.startswith(normalized_scope + "/")


def validation_commands(contract: RepositoryContract, changed_paths: list[str]) -> list[str]:
    commands: list[str] = []

    targets = changed_paths or ["."]
    for target in targets:
        for instruction in applicable_instruction_files(contract.root, target):
            for command in commands_from_instruction(instruction):
                if command not in commands:
                    commands.append(command)

    validation = contract.config.get("validation", {})
    if not isinstance(validation, dict):
        raise ValueError("validation config must be an object")
    root_commands = validation.get("commands", [])
    if not isinstance(root_commands, list) or not all(isinstance(item, str) for item in root_commands):
        raise ValueError("validation.commands must be a list of strings")
    for command in root_commands:
        if command and command not in commands:
            commands.append(command)

    scopes = validation.get("scopes", {})
    if not isinstance(scopes, dict):
        raise ValueError("validation.scopes must be an object")
    for scope, scoped_commands in scopes.items():
        if not isinstance(scoped_commands, list) or not all(isinstance(item, str) for item in scoped_commands):
            raise ValueError(f"validation.scopes.{scope} must be a list of strings")
        if any(_matches_scope(path, scope) for path in changed_paths):
            for command in scoped_commands:
                if command and command not in commands:
                    commands.append(command)
    return commands


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--config", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        contract = load_contract(Path(args.root), args.config)
        paths = args.paths or ["."]
        instruction_map = {
            path: [
                instruction.relative_to(contract.root).as_posix()
                for instruction in applicable_instruction_files(contract.root, path)
            ]
            for path in paths
        }
        report = {
            "instruction_map": instruction_map,
            "validation_commands": validation_commands(contract, paths),
        }
    except ValueError as error:
        report = {"error": str(error)}
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"ERROR: {error}")
        return 2

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for path, instructions in instruction_map.items():
            print(f"{path}: {', '.join(instructions) or '(no AGENTS.md)'}")
        for command in report["validation_commands"]:
            print(f"validate: {command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
