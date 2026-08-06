# Claude to Codex Plugin Port

Codex marketplace plugin for porting Claude Code plugins and skills into clean Codex packages.

The plugin provides one skill, `port-claude-plugin`, plus a scanner script:

```powershell
python .\scripts\audit_claude_port.py <plugin-root>
```

Use it when moving a plugin into a Codex marketplace and you need to remove unsupported hooks, Claude runtime variables, cross-agent shims, stale cache scripts, and overbroad skill triggers.
