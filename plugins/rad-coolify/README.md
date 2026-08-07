# RAD Coolify

RAD Coolify gives Codex procedures and local checks for self-hosted Coolify v4 deployments. It covers deployment setup, databases, security, CI/CD, troubleshooting, monitoring, infrastructure, live operations, and deployment review.

It is for developers who manage small or medium self-hosted Coolify installations and want guidance near their repository work. It does not replace Coolify documentation, server monitoring, backups, or a staging environment.

## What is included

| Skill | Purpose |
| --- | --- |
| `coolify-deploy` | Choose and configure build packs, Dockerfiles, Compose, registries, and deployment settings |
| `coolify-databases` | Provision, connect, back up, and restore Coolify-managed databases |
| `coolify-security` | Review secrets, access, networks, resource limits, and host firewall concerns |
| `coolify-cicd` | Set up API, webhook, GitHub Actions, GitLab CI, and registry workflows |
| `coolify-infrastructure` | Work with multiple servers, build servers, migration, and experimental Swarm support |
| `coolify-observability` | Configure Sentinel, notifications, log drains, and external monitoring |
| `coolify-troubleshoot` | Diagnose routing, TLS, container, build, and deployment failures |
| `coolify-actions` | Use the optional MCP server for live Coolify operations |
| `coolify-status` | Produce a read-only instance status summary through MCP |
| `coolify-review` | Run four local validators, then review issues that require repository context |

Four Python scripts check Dockerfiles, Compose files, environment handling, and deployment pipelines. They use file rules and heuristics. Their findings require review.

## What is specific

Many Coolify guides explain one setup step. RAD Coolify keeps related repository checks together and separates them into focused skills. The review skill runs deterministic file checks before it judges health endpoints, service relationships, and deployment intent.

The original Claude package used an automatic post-edit hook. Codex does not run that hook. In this port, `coolify-review` is the explicit review path. After Codex changes a Dockerfile or Compose file during a Coolify task, the active skill should offer the matching local validator when that check would add value.

## Live operations

The package can launch `@radoriginllc/coolify-mcp` through `npx`. Configure these environment variables outside the repository:

```text
COOLIFY_URL=https://your-coolify-instance.example.com
COOLIFY_API_TOKEN=your-api-token
```

The MCP server can read and change live Coolify resources. Codex should state the planned action and target before a write operation. The `coolify-status` skill remains read-only.

## Requirements

- Python 3.8 or newer for the four validators
- Node.js and `npx` for optional live MCP operations
- A self-hosted Coolify v4 instance for live actions

The Python scripts use the standard library. `lint-compose.py` can use PyYAML when it is already installed, and it has a smaller built-in parser when it is absent.

## Limits

- Coolify v4 is updated often. Version-specific facts can become stale.
- The plugin does not cover Coolify Cloud or Kubernetes.
- A file review cannot prove that a deployment will succeed.
- The validators can produce false positives and can miss problems.
- The plugin does not monitor a deployment after shipping unless the user asks for a bounded status check.
- Live actions require working MCP access and user authorization for the requested change.

## Example requests

- "Review this project for Coolify deployment risks."
- "Help me choose a Coolify build pack for this app."
- "Why does this Coolify deployment return a 502?"
- "Show the current status of my Coolify instance."

## License

MIT. See [LICENSE](LICENSE).
