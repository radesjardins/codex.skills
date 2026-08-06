# Claude to Codex Plugin Port

This plugin helps an author convert a Claude Code plugin or skill set into a Codex marketplace package.

It is for migration work on source you own or have permission to change. It does not make an application or ordinary repository compatible with Codex.

## What it does

The plugin has one skill:

| Skill | Use it for | Main result |
| --- | --- | --- |
| [claude-to-codex-plugin-port:port-claude-plugin](skills/port-claude-plugin/SKILL.md) | Moving a Claude Code plugin, one skill, or a mixed Claude and Codex package | A Codex package with a valid manifest, focused skill triggers, mapped hook behavior, and recorded validation |

The skill tells Codex to:

1. Read the source manifest, skills, scripts, references, templates, and marketplace files.
2. Create the Codex plugin structure and marketplace entry.
3. Remove unsupported hook wiring from the Codex copy.
4. Replace useful hook behavior with an explicit skill, script, or validation step.
5. Remove Claude runtime paths, cache scripts, generated files, and stale command wording when they do not belong in the Codex package.
6. narrow skill descriptions that would trigger on unrelated work.
7. validate the result and report any intentional Claude references that remain.

The source Claude package stays in place unless the user gives a separate request to remove it.

## Local scanner

The bundled scanner finds common migration leftovers:

~~~powershell
python .\scripts\audit_claude_port.py <plugin-root>
python .\scripts\audit_claude_port.py <plugin-root> --json
~~~

It checks for a missing or invalid Codex manifest, a missing skills folder, hook directories and common hook script names, Claude runtime variables, generated Python files, broad trigger phrases, and selected Claude-specific terms.

The scanner matches file names and text patterns. It can flag an intentional reference in documentation. A clean scan does not prove feature parity or correct runtime behavior.

## Where it fits

Most plugin ports need a file inventory, text searches, manifest changes, and manual testing. This plugin uses those same steps.

Its specific addition is the mapping rule for hook behavior. The port must say what happened to each useful hook action. The local scanner then checks for common residue that is easy to miss in a manual copy.

## Limits

- Codex and Claude Code do not have identical plugin features. Some behavior needs a new workflow or must be dropped.
- The scanner knows a fixed set of patterns. It does not understand every custom hook or script.
- Validation checks package shape. It does not prove that every migrated skill gives the same answer as its source.
- Publishing, committing, pushing, installing, and removing the old marketplace entry happen only when the request includes them.
- The workflow keeps unsupported cross-agent shims out by default. A user can request shared templates as separate work.

## Install

~~~powershell
codex plugin add claude-to-codex-plugin-port@radesjardins-codex-skills
~~~

Example request:

> Port the Claude plugin at R:\path\to\source into the Codex marketplace at R:\path\to\marketplace. Keep the source unchanged.

## License

MIT. See [LICENSE](LICENSE).
