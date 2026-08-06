# rad-repo scripts

All scripts are Python-standard-library tools. Mechanical gates can block; heuristic
reports remain evidence for human or agent judgment.

## Executable contract

### `repo_contract.py`

Discovers root and scoped `AGENTS.md` files, excludes dependency/build trees and
out-of-repository symlinks, parses labeled validation commands, and merges optional
global or path-scoped commands from `.rad-repo.json`.

```bash
python repo_contract.py <project-dir> --changed-path src/app.py --json
```

### `pre_ship.py`

Inspects staged Git blobs rather than untrusted working-tree copies. It blocks
protected paths, secret patterns, unexpected generated output, oversized files,
unreviewed contract changes, failed validation commands, and missing validation
declarations unless `validation.allow_empty` is explicitly true.

```bash
python pre_ship.py <project-dir> --run-validation --json
```

Exit `1` means shipping is blocked. Review contract changes before adding
`--allow-contract-change`; unstaged contract edits cannot be bypassed, and the flag
is never a general bypass.

## Context validators

### `repo-scan.py`

Reports deterministic shelf drift, size budgets, instruction files, and malformed
active initiatives. It exits `0`; consumers use JSON severity and findings.

### `doc-freshness.py`

Reports commit-distance trust bands. Managed docs may add frontmatter `tracks:` paths;
the report then identifies missing paths and code changes since the document's last
commit. This is stronger evidence than age alone but is not proof that prose is
semantically current.

### `vocab-lint.py`

Uses `.rad-repo.json` vocabulary profiles. `advisory` is the default and exits
`0`; `strict` emits error findings and exits `1`; `off` disables synonym checks.

### `doc-contradiction.py`

Checks PRD non-goals against plan commitments and locked decision constraints against
plan objectives. Matching is lexical/containment-based and must be reviewed before
editing authoritative docs.

### `doc-redundancy.py`

Checks managed shelf docs and active initiatives for substantial cross-document
duplication while filtering common template headings. Medium findings exit `1`.

### `audit-user-content.py`

Audits user-owned portions of all in-repository `AGENTS.md` files for dead paths and
orphan terminology. It never edits content and exits `0` with advisory findings.

## Configuration

Copy `../templates/repo.json` to `.rad-repo.json`. JSON is validated;
invalid modes, scopes, lists, command objects, or shipping values fail closed in the
contract and pre-ship tools.

## Tests

```bash
python tests/run_all.py
```

Each executable behavior has a focused regression file. Fixtures cover malformed
Markdown, nested instructions and monorepos, Unicode and Windows-style paths,
out-of-root symlinks, Git and no-history repositories, staged blobs, and configured
exceptions.
