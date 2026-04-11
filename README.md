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

```
usage: create_skill.py [-h] [--name NAME] [--output OUTPUT] [--multi-env]
                       [--shell-source] [--force]
                       url

Fetch API docs and generate a Claude Code skill in one step.

positional arguments:
  url              API documentation URL (OpenAPI, Swagger, Postman, HTML)

options:
  -h, --help       show this help message and exit
  --name NAME      Skill name (inferred from spec if omitted)
  --output OUTPUT  Output directory (default: ~/.claude/skills/<name>)
  --multi-env
  --shell-source
  --force
```

Fetches, generates, and installs in a single command. The skill name is inferred from the spec or URL.

### Step by step

**Step 1 — Fetch and parse the API spec:**

```bash
python3 ~/.claude/skills/skill-creator/scripts/fetch_docs.py https://petstore.swagger.io/v2/swagger.json
```

Outputs a normalized JSON representation of the API to stdout. Review it before generating.

**Step 2 — Generate the skill:**

```bash
python3 ~/.claude/skills/skill-creator/scripts/fetch_docs.py <URL> | \
  python3 ~/.claude/skills/skill-creator/scripts/generate_skill.py \
    --name petstore \
    --output ~/.claude/skills/petstore
```

```
Saved API spec: ~/.claude/skills/petstore/api_spec.json
Generated CLI:  ~/.claude/skills/petstore/scripts/petstore_cli.py
Generated SKILL.md: ~/.claude/skills/petstore/SKILL.md

Skill 'petstore' generated successfully!
  Resources: 3 (pet, store, user)
  Endpoints: 20
  Output: ~/.claude/skills/petstore

Set environment variables in ~/.zshrc:
  export PETSTORE_URL=<url>
  export PETSTORE_TOKEN=<token>
```

**Step 3 — Verify the generated CLI:**

```bash
python3 ~/.claude/skills/petstore/scripts/petstore_cli.py --help
```

```
usage: petstore_cli.py [-h] {check,pet,store,user} ...

petstore CLI

positional arguments:
  {check,pet,store,user}
                        Available commands
    check               Test API connectivity
    pet                 Pet operations
    store               Store operations
    user                User operations

options:
  -h, --help            show this help message and exit
```

Drill into a resource:

```bash
python3 ~/.claude/skills/petstore/scripts/petstore_cli.py pet --help
```

```
usage: petstore_cli.py pet [-h]
                           {upload,add,update,list,list-2,get,update-2,delete}
                           ...

positional arguments:
  {upload,add,update,list,list-2,get,update-2,delete}
                        pet actions
    upload              uploads an image
    add                 Add a new pet to the store
    update              Update an existing pet
    list                Finds Pets by status
    list-2              Finds Pets by tags
    get                 Find pet by ID
    update-2            Updates a pet in the store with form data
    delete              Deletes a pet

options:
  -h, --help            show this help message and exit
```

And a specific action:

```bash
python3 ~/.claude/skills/petstore/scripts/petstore_cli.py pet get --help
```

```
usage: petstore_cli.py pet get [-h] petId

positional arguments:
  petId       petId

options:
  -h, --help  show this help message and exit
```

**Step 4 — Configure credentials:**

```bash
# ~/.skills.env
PETSTORE_TOKEN=your_token_here
PETSTORE_URL=https://petstore.swagger.io/v2
```

Source this file or add it to your shell profile.

### Multi-environment support

Use `--multi-env` to generate a CLI with `dev`, `stg`, and `pro` environment switching:

```bash
python3 ~/.claude/skills/skill-creator/scripts/fetch_docs.py <URL> | \
  python3 ~/.claude/skills/skill-creator/scripts/generate_skill.py \
    --name petstore --multi-env
```

```
usage: petstore_cli.py [-h] [--env {dev,stg,pro}] {check,pet,store,user} ...

petstore CLI

positional arguments:
  {check,pet,store,user}
                        Available commands
    check               Test API connectivity
    pet                 Pet operations
    store               Store operations
    user                User operations

options:
  -h, --help            show this help message and exit
  --env {dev,stg,pro}   Environment to use (overrides RPSP_ENV)
```

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

After generation, the skill directory looks like this:

```
~/.claude/skills/petstore/
  SKILL.md              # Claude Code skill definition
  api_spec.json         # Saved spec for future updates
  scripts/
    petstore_cli.py     # Generated Python CLI
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

## Example skills

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
