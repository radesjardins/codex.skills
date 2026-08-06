#!/usr/bin/env python3
"""Ensure the standalone compatibility bundle mirrors shared plugin assets."""

from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = PLUGIN_ROOT.parents[1]
STANDALONE_ROOT = REPOSITORY_ROOT / "skills" / ".curated" / "rad-repo"
EXCLUDED = {
    Path("scripts/tests/test_standalone_mirror.py"),
}


def shared_files(root: Path) -> dict[Path, str]:
    files: dict[Path, str] = {}
    for directory in ("references", "scripts", "templates"):
        base = root / directory
        if not base.exists():
            continue
        for path in base.rglob("*"):
            relative = path.relative_to(root)
            if not path.is_file() or "__pycache__" in relative.parts or path.suffix == ".pyc":
                continue
            if relative in EXCLUDED:
                continue
            files[relative] = path.read_text(encoding="utf-8").replace("\r\n", "\n").rstrip()
    return files


if STANDALONE_ROOT.exists():
    plugin_files = shared_files(PLUGIN_ROOT)
    standalone_files = shared_files(STANDALONE_ROOT)
    assert standalone_files.keys() == plugin_files.keys(), (
        f"standalone file set differs: plugin-only={sorted(plugin_files.keys() - standalone_files.keys())}, "
        f"standalone-only={sorted(standalone_files.keys() - plugin_files.keys())}"
    )
    changed = [path for path in plugin_files if plugin_files[path] != standalone_files[path]]
    assert not changed, f"standalone shared assets are stale: {changed}"

print("standalone mirror regression test passed")
