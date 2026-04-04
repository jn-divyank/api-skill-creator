# api-skill-creator

A code generation tool that transforms API documentation into fully functional [Claude Code](https://claude.ai/code) skills — automatically.

Point it at any OpenAPI, Swagger, or Postman spec (or a URL), and it generates a ready-to-use Python CLI tool plus a `SKILL.md` definition file. No manual coding required.

---

## What it does

1. **Fetches** API documentation from a URL or local file
2. **Parses** the spec (OpenAPI 3.x, Swagger 2.0, Postman v2, HTML, DeepWiki)
3. **Generates** a Python CLI with nested subcommands and a `SKILL.md` definition
4. **Installs** the skill into `~/.claude/skills/<name>/`

The generated CLI follows a consistent pattern:

```
python3 <name>_cli.py <resource> <action> [args]
```

Resources come from API tags or URL paths; actions are inferred from HTTP methods (`list`, `get`, `create`, `update`, `delete`). Every generated skill includes a `check` command for connectivity testing and automatic auth header handling.

---

## Requirements

- Python 3.8+
- PyYAML (optional — only needed for YAML spec parsing; installed automatically by `install.sh`)

No other dependencies.

---

## Installation

```bash
bash install.sh
```

This copies the skill to `~/.claude/skills/skill-creator/` and installs PyYAML if needed.

---

## Usage

### One-step (simplest)

```bash
python3 ~/.claude/skills/skill-creator/scripts/create_skill.py https://api.example.com/openapi.json
```

Fetches, generates, and installs in a single command. The skill name is inferred from the spec or URL.

### Step by step

**Step 1 — Fetch and parse the API spec:**

```bash
python3 ~/.claude/skills/skill-creator/scripts/fetch_docs.py https://api.example.com/openapi.json
```

Outputs a normalized JSON representation of the API to stdout. Review it before generating.

**Step 2 — Generate the skill:**

```bash
python3 ~/.claude/skills/skill-creator/scripts/fetch_docs.py <URL> | \
  python3 ~/.claude/skills/skill-creator/scripts/generate_skill.py \
    --name myapi \
    --output ~/.claude/skills/myapi
```

**Step 3 — Verify:**

```bash
python3 ~/.claude/skills/myapi/scripts/myapi_cli.py --help
python3 ~/.claude/skills/myapi/scripts/myapi_cli.py check
```

**Step 4 — Configure credentials:**

```bash
# ~/.skills.env
MYAPI_TOKEN=your_token_here
MYAPI_BASE_URL=https://api.example.com
```

Source this file or add it to your shell profile.

### Updating an existing skill

When an API changes, re-fetch and regenerate:

```bash
python3 ~/.claude/skills/skill-creator/scripts/fetch_docs.py <URL> | \
  python3 ~/.claude/skills/skill-creator/scripts/generate_skill.py \
    --name myapi \
    --output ~/.claude/skills/myapi \
    --force
```

The tool compares the new spec against the saved `api_spec.json` and shows a diff summary before overwriting.

---

## Options

| Flag | Description |
|------|-------------|
| `--name <name>` | Skill name (used for directory and CLI script name) |
| `--output <dir>` | Installation directory (default: `~/.claude/skills/<name>`) |
| `--force` | Overwrite existing output |
| `--multi-env` | Add dev/staging/production environment support |
| `--shell-source` | Source shell profile for environment variables |

---

## Output structure

```
~/.claude/skills/<name>/
  SKILL.md              # Claude Code skill definition
  api_spec.json         # Saved spec for future updates
  scripts/
    <name>_cli.py       # Generated Python CLI
```

---

## Supported input formats

| Format | Notes |
|--------|-------|
| OpenAPI 3.x | JSON or YAML |
| Swagger 2.0 | JSON or YAML |
| Postman v2 | JSON collection |
| DeepWiki | HTML extraction |
| Generic HTML | Schema extraction |
| Local files | JSON or YAML |

The fetcher handles SSL fallback, 429 rate-limit retries (2s backoff), and automatic redirects.

---

## Examples

Pre-generated example skills are in the `output/` directory:

- `output/github/` — GitHub REST API v3
- `output/stripe/` — Stripe API
- `output/slack/` — Slack Web API
- `output/spotify/` — Spotify Web API
- `output/notion/` — Notion API
- `output/twilio/` — Twilio API
- `output/petstore/` — OpenAPI Petstore (test)

Each contains a `SKILL.md`, a generated `*_cli.py`, and the saved `api_spec.json`.

---

## Running tests

```bash
python3 -m pytest tests/
```

Tests cover spec parsing (`test_fetch_docs.py`) and code generation (`test_generate_skill.py`).

---

## License

MIT
