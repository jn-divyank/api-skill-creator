---
name: github
description: Interact with github-v3-rest-api API. Use for querying, creating, and managing github-v3-rest-api resources. Use when asked about github-v3-rest-api operations.
argument-hint: [command] [args]
allowed-tools: Bash(python3:*)
---

# Github V3 Rest Api Integration

## Configuration

Set these environment variables in `~/.zshrc`:

- `GITHUB_URL` — API base URL (default: `https://api.github.com`)
- `GITHUB_TOKEN` — Authentication token

## Available Commands

### Check Connection
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py check
```

### Activity
```bash
# Get feeds
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py activity get
# List public events
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py activity list -- VALUE -- VALUE
# List repositories starred by the authenticated user
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py activity list-2 -- VALUE -- VALUE
# List notifications for the authenticated user
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py activity list-3 -- VALUE -- VALUE
```

### Apps
```bash
# Get the authenticated app
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py apps get
```

### Emojis
```bash
# Get emojis
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py emojis get
```

### Gists
```bash
# List gists for the authenticated user
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py gists list -- VALUE -- VALUE
# List public gists
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py gists list-2 -- VALUE -- VALUE
# List starred gists
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py gists list-3 -- VALUE -- VALUE
```

### Issues
```bash
# List issues assigned to the authenticated user
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py issues list --filter VALUE --state VALUE
# List user account issues assigned to the authenticated user
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py issues list-2 --filter VALUE --state VALUE
```

### Licenses
```bash
# Get all commonly used licenses
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py licenses get --featured VALUE -- VALUE
```

### Meta
```bash
# GitHub API Root
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py meta root
# Get the Zen of GitHub
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py meta get
# Get GitHub meta information
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py meta get-2
# Get Octocat
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py meta get-3 --s VALUE
# Get all API versions
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py meta get-4
```

### Orgs
```bash
# List organizations for the authenticated user
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py orgs list -- VALUE -- VALUE
# Get an organization
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py orgs get ORG -- VALUE
```

### Rate-Limit
```bash
# Get rate limit status for the authenticated user
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py rate-limit get
```

### Repos
```bash
# List repositories for the authenticated user
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py repos list --visibility VALUE --affiliation VALUE
# List public repositories
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py repos list-2 -- VALUE
```

### Search
```bash
# Search code
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py search code --q VALUE --sort VALUE
# Search users
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py search users --q VALUE --sort VALUE
```

### Teams
```bash
# List teams for the authenticated user
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py teams list -- VALUE -- VALUE
```

### Users
```bash
# Get the authenticated user
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py users get
# List users
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py users list -- VALUE -- VALUE
# List public SSH keys for the authenticated user
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py users list-2 -- VALUE -- VALUE
# List users blocked by the authenticated user
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py users list-3 -- VALUE -- VALUE
# List email addresses for the authenticated user
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py users list-4 -- VALUE -- VALUE
```

## Usage Instructions

Map user requests to commands:

1. **"Is github-v3-rest-api reachable?"** / **"Test connection"** → `check`
2. **"Get feeds"** → `activity get`
3. **"List public events"** → `activity list -- VALUE`
4. **"List repositories starred by the authenticated user"** → `activity list-2 -- VALUE`
5. **"List notifications for the authenticated user"** → `activity list-3 -- VALUE`
6. **"Get the authenticated app"** → `apps get`
7. **"Get emojis"** → `emojis get`
8. **"List gists for the authenticated user"** → `gists list -- VALUE`
9. **"List public gists"** → `gists list-2 -- VALUE`
10. **"List starred gists"** → `gists list-3 -- VALUE`
11. **"List issues assigned to the authenticated user"** → `issues list --filter VALUE`
12. **"List user account issues assigned to the authenticated user"** → `issues list-2 --filter VALUE`
13. **"Get all commonly used licenses"** → `licenses get --featured VALUE`
14. **"GitHub API Root"** → `meta root`
15. **"Get the Zen of GitHub"** → `meta get`
16. **"Get GitHub meta information"** → `meta get-2`
17. **"Get Octocat"** → `meta get-3 --s VALUE`
18. **"Get all API versions"** → `meta get-4`
19. **"List organizations for the authenticated user"** → `orgs list -- VALUE`
20. **"Get an organization"** → `orgs get ORG -- VALUE`
21. **"Get rate limit status for the authenticated user"** → `rate-limit get`
22. **"List repositories for the authenticated user"** → `repos list --visibility VALUE`
23. **"List public repositories"** → `repos list-2 -- VALUE`
24. **"Search code"** → `search code --q VALUE`
25. **"Search users"** → `search users --q VALUE`
26. **"List teams for the authenticated user"** → `teams list -- VALUE`
27. **"Get the authenticated user"** → `users get`
28. **"List users"** → `users list -- VALUE`
29. **"List public SSH keys for the authenticated user"** → `users list-2 -- VALUE`
30. **"List users blocked by the authenticated user"** → `users list-3 -- VALUE`
31. **"List email addresses for the authenticated user"** → `users list-4 -- VALUE`

## Examples

User: "Is github-v3-rest-api connected?"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py check
```

User: "Get feeds"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py activity get
```

User: "Get the authenticated app"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py apps get
```

User: "Get emojis"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py emojis get
```

User: "List gists for the authenticated user"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/github_cli.py gists list
```
