# RAD Coolify

RAD Coolify is an Agent Plugins 1.0.0 package that gives Codex procedures and local checks for self-hosted Coolify v4 deployments. It covers deployment setup, databases, security, CI/CD, troubleshooting, monitoring, infrastructure, live operations, and deployment review.

It is for developers who manage self-hosted Coolify installations and want guidance near their repository work. It does not replace Coolify documentation, server monitoring, backups, or a staging environment.

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

## Install

Add the public marketplace and install the plugin:

```powershell
codex plugin marketplace add radesjardins/codex.skills
codex plugin add rad-coolify@radesjardins-codex-skills
```

If you use a fork or private marketplace, replace `radesjardins-codex-skills` with that marketplace's name.

## MCP server

The plugin starts [`@radoriginllc/coolify-mcp`](https://www.npmjs.com/package/@radoriginllc/coolify-mcp) as a local stdio MCP process through `npx`. That package calls the Coolify REST API. It includes read and write tools for applications, deployments, environment variables, databases, services, and other resources.

This MCP setup is client-specific. Agent Plugins 1.0.0 has no portable secret field, so another compatible client may need its own secure credential mapping or MCP configuration. Portable package conformance alone does not make live operations available.

This is separate from [Coolify's built-in `/mcp` endpoint](https://coolify.io/docs/integrations/mcp). Coolify currently documents its built-in endpoint as read-only. RAD Coolify does not configure that endpoint.

### 1. Check requirements

You need:

- Node.js 18 or newer, with `npx`
- A running self-hosted Coolify v4 instance
- Coolify API access
- Python 3.8 or newer only when using the four local validators

The first MCP start may download the npm package. It therefore needs npm registry access.

### 2. Enable the Coolify API

In Coolify:

1. Open `Settings > Advanced`.
2. Turn on `API Access`.
3. If you use an API IP allowlist, include the machine that runs Codex.

See [Coolify API authorization](https://coolify.io/docs/api-reference/authorization).

### 3. Create a token

In Coolify:

1. Select the team that owns the resources you want to manage.
2. Open `Security > API Tokens`.
3. Create a token with an expiration date and the smallest permissions needed.
4. Copy the full token when Coolify shows it. Coolify displays it only once.

Permission guide:

| Permission | Use |
| --- | --- |
| `read` | Status, inventory, and ordinary read-only queries |
| `read:sensitive` | Logs, secrets, private keys, environment values, and other sensitive responses |
| `deploy` | Trigger and manage deployments |
| `write` | Create, update, start, stop, restart, or delete supported resources |
| `root` | Full API control. Avoid this unless a specific administrative task requires it |

Coolify tokens are scoped to the active team. Create separate tokens for separate teams.

### 4. Set the URL and token

The plugin reads two environment variables:

| Variable | Value |
| --- | --- |
| `COOLIFY_URL` | Your Coolify instance base URL, such as `https://coolify.example.com` |
| `COOLIFY_API_TOKEN` | The full token copied from `Security > API Tokens` |

`COOLIFY_URL` is the dashboard base URL. Do not add `/api/v1` or `/mcp`.

Do not put the token in this repository, a project `.env` file, `.mcp.json`, a prompt, or an issue report. The bundled `.mcp.json` contains variable references only.

#### Windows PowerShell, persistent for your user account

```powershell
[Environment]::SetEnvironmentVariable(
  "COOLIFY_URL",
  "https://coolify.example.com",
  "User"
)

[Environment]::SetEnvironmentVariable(
  "COOLIFY_API_TOKEN",
  "paste-the-full-token-here",
  "User"
)
```

Close all Codex windows and reopen Codex after you set or change either variable.

#### macOS or Linux, current terminal session

```bash
export COOLIFY_URL="https://coolify.example.com"
export COOLIFY_API_TOKEN="paste-the-full-token-here"
codex
```

For persistent setup, use your operating system's secret-aware login environment or your shell's startup configuration. A Codex process only sees variables that exist when it starts.

### 5. Verify with a read-only request

Start a new Codex thread and ask:

```text
Check my Coolify health and version. Do not change anything.
```

If the MCP connection fails, check:

- API Access is enabled.
- The URL is the instance base URL.
- The full token was copied.
- The token belongs to the correct team.
- The token has `read` permission.
- Your API IP allowlist permits the Codex machine.
- Codex was restarted after the variables changed.
- Node.js and `npx` are available.

## Safety

The MCP server can change live resources when the token has `deploy` or `write` permission. Codex should state the planned action and exact target before a write. Start with a `read` token if you only need status and inventory.

The `coolify-status` and `coolify-review` skills are read-only. Other skills can propose or perform changes when the user asks and the required tools are available.

## Limits

- Coolify v4 changes often. Version-specific facts can become stale.
- The plugin does not cover Coolify Cloud or Kubernetes.
- A file review cannot prove that a deployment will succeed.
- The validators can produce false positives and can miss problems.
- The plugin does not monitor a deployment after shipping unless the user asks for a bounded status check.
- The npm MCP package is a separate project from Coolify's built-in MCP server.

## Example requests

- "Review this project for Coolify deployment risks."
- "Help me choose a Coolify build pack for this app."
- "Why does this Coolify deployment return a 502?"
- "Show the current status of my Coolify instance."

## License

MIT. See [LICENSE](LICENSE).
