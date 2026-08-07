from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


IGNORED_DIRECTORY_NAMES = {"__pycache__"}
IGNORED_FILE_NAMES = {".DS_Store"}
IGNORED_FILE_SUFFIXES = {".pyc", ".pyo"}


@dataclass(frozen=True, slots=True)
class SharedPackageResult:
    name: str
    different_files: tuple[str, ...]

    @property
    def in_sync(self) -> bool:
        return not self.different_files

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "in_sync": self.in_sync,
            "different_files": list(self.different_files),
        }


@dataclass(frozen=True, slots=True)
class SyncReport:
    left: Path
    right: Path
    shared: tuple[SharedPackageResult, ...]
    left_only: tuple[str, ...]
    right_only: tuple[str, ...]

    @property
    def in_sync(self) -> bool:
        return all(package.in_sync for package in self.shared)

    def to_dict(self) -> dict[str, Any]:
        return {
            "left": str(self.left),
            "right": str(self.right),
            "in_sync": self.in_sync,
            "shared": [package.to_dict() for package in self.shared],
            "left_only": list(self.left_only),
            "right_only": list(self.right_only),
        }


def _plugin_names(marketplace_root: Path) -> set[str]:
    plugins = marketplace_root / "plugins"
    if not plugins.is_dir():
        raise FileNotFoundError(f"Marketplace plugins directory not found: {plugins}")
    return {
        path.name
        for path in plugins.iterdir()
        if path.is_dir()
        and ((path / "plugin.json").is_file() or (path / ".codex-plugin" / "plugin.json").is_file())
    }


def _content_hash(path: Path) -> str:
    content = path.read_bytes()
    try:
        normalized = content.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    except UnicodeDecodeError:
        normalized = content
    return hashlib.sha256(normalized).hexdigest()


def _file_hashes(package_root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in package_root.rglob("*"):
        relative = path.relative_to(package_root)
        if any(part in IGNORED_DIRECTORY_NAMES for part in relative.parts):
            continue
        if not path.is_file() or path.name in IGNORED_FILE_NAMES or path.suffix in IGNORED_FILE_SUFFIXES:
            continue
        hashes[relative.as_posix()] = _content_hash(path)
    return hashes


def compare_marketplaces(left: Path, right: Path) -> SyncReport:
    left = left.resolve()
    right = right.resolve()
    left_names = _plugin_names(left)
    right_names = _plugin_names(right)
    shared_names = sorted(left_names & right_names)
    shared: list[SharedPackageResult] = []
    for name in shared_names:
        left_files = _file_hashes(left / "plugins" / name)
        right_files = _file_hashes(right / "plugins" / name)
        different = tuple(
            path
            for path in sorted(left_files.keys() | right_files.keys())
            if left_files.get(path) != right_files.get(path)
        )
        shared.append(SharedPackageResult(name=name, different_files=different))
    return SyncReport(
        left=left,
        right=right,
        shared=tuple(shared),
        left_only=tuple(sorted(left_names - right_names)),
        right_only=tuple(sorted(right_names - left_names)),
    )
