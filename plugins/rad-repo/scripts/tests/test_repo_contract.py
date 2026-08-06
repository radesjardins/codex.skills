#!/usr/bin/env python3
"""Regression tests for repository contract discovery."""

import json
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from repo_contract import (
    all_instruction_files,
    applicable_instruction_files,
    load_contract,
    repository_profile,
    validation_commands,
    validation_plan,
)


with tempfile.TemporaryDirectory() as temporary:
    root = Path(temporary)
    (root / "src" / "web").mkdir(parents=True)
    (root / "AGENTS.md").write_text(
        """# Root
## Stack & commands
- Build: `python -m compileall src` · Test: `python -m unittest`
- Run: `python app.py`
""",
        encoding="utf-8",
    )
    (root / "src" / "AGENTS.md").write_text(
        """# Source overlay
## Stack & commands
- Lint: `python lint.py`
| Check | `python table_check.py` |
""",
        encoding="utf-8",
    )
    (root / ".rad-repo.json").write_text(
        json.dumps({
            "validation": {
                "commands": ["python root_check.py"],
                "scopes": {"src/web": ["python web_check.py"]},
            }
        }),
        encoding="utf-8",
    )

    assert [path.relative_to(root).as_posix() for path in applicable_instruction_files(
        root, "src/web/page.py"
    )] == ["AGENTS.md", "src/AGENTS.md"]
    assert [path.relative_to(root).as_posix() for path in all_instruction_files(root)] == [
        "AGENTS.md", "src/AGENTS.md",
    ]

    contract = load_contract(root)
    commands = validation_commands(contract, ["src/web/page.py"])
    assert commands == [
        "python -m compileall src",
        "python -m unittest",
        "python lint.py",
        "python table_check.py",
        "python root_check.py",
        "python web_check.py",
    ], commands
    assert "python app.py" not in commands
    assert validation_commands(contract, [r"src\web\page.py"]) == commands
    assert repository_profile(contract) == "core"
    plan = validation_plan(contract, ["src/web/page.py"])
    assert plan["commands"][0] == {
        "command": "python -m compileall src",
        "source": "AGENTS.md",
    }, plan

    (root / ".rad-repo.json").write_text(json.dumps({"profile": "wide"}), encoding="utf-8")
    try:
        repository_profile(load_contract(root))
    except ValueError as error:
        assert "core" in str(error) and "full" in str(error), error
    else:
        raise AssertionError("invalid profile must fail")
    (root / ".rad-repo.json").write_text(
        json.dumps({
            "validation": {
                "commands": ["python root_check.py"],
                "scopes": {"src/web": ["python web_check.py"]},
            }
        }),
        encoding="utf-8",
    )

    (root / "docs").mkdir()
    (root / "docs" / "AGENTS.md").write_text(
        "# Docs\n\n- Build: `<command>` · Test: `none`\n",
        encoding="utf-8",
    )
    commands = validation_commands(load_contract(root), ["docs/readme.md"])
    assert commands == [
        "python -m compileall src",
        "python -m unittest",
        "python root_check.py",
    ], commands

    outside = Path(temporary).parent / f"{Path(temporary).name}-outside"
    outside.mkdir()
    try:
        (outside / "AGENTS.md").write_text("# Outside\n", encoding="utf-8")
        link = root / "linked"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError:
            pass
        else:
            assert link / "AGENTS.md" not in all_instruction_files(root)
    finally:
        (outside / "AGENTS.md").unlink(missing_ok=True)
        outside.rmdir()

print("repo-contract regression tests passed")
