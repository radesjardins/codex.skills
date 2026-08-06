# Conversion Map

| Source item | Portable result | Required review |
| --- | --- | --- |
| Plugin metadata | Root `plugin.json` | Keep only portable fields |
| Agent Skill | `skills/<name>/SKILL.md` | Name and frontmatter must conform |
| MCP command server | Root `mcp.json` with `stdio` | Command must be one executable token |
| MCP URL server | Root `mcp.json` | Choose `streamable-http` or `sse` |
| Hook | No portable v1 component | Keep compatibility, replace, or record limitation |
| Custom agent, command, LSP, or UI | No portable v1 component | Keep only with documented client support |
| Marketplace entry | Distribution metadata | Update after the package validates |
