# RAD Coolify validators

These four scripts provide file-based checks for the `coolify-review` skill. Each can also run as a standalone command.

| Script | Checks |
| --- | --- |
| `lint-dockerfile.py` | Image tags, users, ports, health checks, secret-shaped build values, stages, and copy scope |
| `lint-compose.py` | Health checks, restart policy, secret-shaped values, privileges, volumes, and port conflicts |
| `check-coolify-env.py` | Environment files, ignore rules, secret-shaped values, examples, and Nixpacks version pins |
| `audit-cicd.py` | Deploy requests, exposed tokens, image tags, test gates, and status checks |

Run a script against one file or a project root:

```powershell
python scripts\lint-dockerfile.py <path> --json
python scripts\lint-compose.py <path> --json
python scripts\check-coolify-env.py <path> --json
python scripts\audit-cicd.py <path> --json
```

Exit code `0` means no covered issue was found. Exit code `1` means the script found issues. Exit code `2` means the script could not complete its check.

The scripts do not build containers, start services, call the Coolify API, or prove that a deployment will work. Their results are evidence for review.
