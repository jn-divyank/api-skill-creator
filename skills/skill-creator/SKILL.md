---
name: skill-creator
description: >-
  Auto-generate Claude Code skills from API documentation. Takes an API doc URL
  (OpenAPI, Swagger, Postman, DeepWiki, HTML) and generates a complete skill with
  SKILL.md + Python CLI script. Use when asked to create a new skill, generate an
  API integration, or update an existing skill from API docs.
argument-hint: <API_DOC_URL> [options]
allowed-tools: Bash(python3:*)
disable-model-invocation: true
---

# Skill Creator — Auto-generate Claude Code Skills from API Docs

Generate complete, runnable Claude Code skills from API documentation URLs.
Produces a SKILL.md + Python CLI with nested subcommand groups (like kubectl/aws-cli).

## Scripts

- `${CLAUDE_SKILL_DIR}/scripts/fetch_docs.py` — Fetch and parse API docs into structured JSON
- `${CLAUDE_SKILL_DIR}/scripts/generate_skill.py` — Generate SKILL.md + Python CLI from JSON spec

## Workflow A — Create New Skill

### Step 1: Fetch and parse the API spec

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/fetch_docs.py <URL_OR_FILE>
```

Supported formats: OpenAPI 3.x, Swagger 2.0, Postman v2, DeepWiki, HTML.
Outputs structured JSON with service_name, base_url, auth_type, endpoints[].

### Step 2: Review the JSON

Examine the output. Key things to verify:
- `service_name` — will become the skill directory name
- `base_url` — correct API host
- `auth_type` — bearer, basic, api_key
- `endpoints` — check groupings (tags), remove unwanted endpoints
- Optionally modify the JSON (add/remove endpoints, adjust tags, rename resources)

### Step 3: Generate the skill

```bash
# Minimal (clean, simple output) — files created in ./output/<SERVICE>/
python3 ${CLAUDE_SKILL_DIR}/scripts/fetch_docs.py <URL> | python3 ${CLAUDE_SKILL_DIR}/scripts/generate_skill.py --name <SERVICE>

# With explicit install destination
python3 ${CLAUDE_SKILL_DIR}/scripts/fetch_docs.py <URL> | python3 ${CLAUDE_SKILL_DIR}/scripts/generate_skill.py --name <SERVICE> --output ~/.claude/skills/<SERVICE>

# Full setup with multi-env and shell sourcing
python3 ${CLAUDE_SKILL_DIR}/scripts/fetch_docs.py <URL> | python3 ${CLAUDE_SKILL_DIR}/scripts/generate_skill.py --name <SERVICE> --output ~/.claude/skills/<SERVICE> --multi-env --shell-source
```

**generate_skill.py flags:**
- `--name <name>` — (required) Service name, lowercase+hyphens, becomes directory name
- `--output <dir>` — Output directory (default: `./output/<name>`)
- `--multi-env` — Add multi-environment support (dev/stg/pro with RPSP_ENV)
- `--shell-source` — Source ~/.zshrc automatically for env var loading
- `--force` — Overwrite existing output directory

### Step 4: Verify

```bash
python3 ~/.claude/skills/<SERVICE>/scripts/<SERVICE>_cli.py --help
python3 ~/.claude/skills/<SERVICE>/scripts/<SERVICE>_cli.py <resource> --help
```

Confirm: nested subcommand groups work, `check` command exists, all resources listed.

### Step 5: Inform the user

Tell the user which environment variables to set in `~/.zshrc`:
```
export SERVICE_URL=https://api.example.com
export SERVICE_TOKEN=your-api-token
```

## Workflow B — Update Existing Skill

When the API changes (new endpoints, removed endpoints, parameter changes):

### Step 1: Fetch the new spec

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/fetch_docs.py <NEW_URL> > /tmp/new_spec.json
```

### Step 2: Compare with existing spec

Read `~/.claude/skills/<name>/api_spec.json` (saved from original generation).
Compare with `/tmp/new_spec.json`:
- New endpoints (in new but not old)
- Removed endpoints (in old but not new)
- Changed endpoints (same path but different params/body)

### Step 3: Show the user a summary

Example: "3 new endpoints found, 1 removed, 2 parameters changed."
Ask if they want to proceed with regeneration.

### Step 4: Regenerate

```bash
cat /tmp/new_spec.json | python3 ${CLAUDE_SKILL_DIR}/scripts/generate_skill.py --name <SERVICE> --output ~/.claude/skills/<SERVICE> --force
```

### Step 5: Verify

```bash
python3 ~/.claude/skills/<SERVICE>/scripts/<SERVICE>_cli.py --help
```

## Output Structure

Generated skills follow this structure:
```
~/.claude/skills/<name>/
  SKILL.md              # Skill definition with frontmatter
  api_spec.json         # Persisted spec for incremental updates
  scripts/
    <name>_cli.py       # Python CLI with nested subcommand groups
```

The CLI uses nested subcommand groups: `cli.py <resource> <action> [args]`
- Resources derived from OpenAPI tags or URL path segments
- Actions: list, get, create, update, delete (inferred from HTTP methods)
- Always includes a top-level `check` command for connectivity testing

## Usage Instructions

Map user requests to workflows:

1. **"Create a skill for <API>"** / **"Generate a CLI for <service>"** → Workflow A
2. **"Update the <service> skill"** / **"API changed, regenerate"** → Workflow B
3. **"Parse this API spec"** → Just run fetch_docs.py, show JSON output
4. **"Add multi-env support to <service>"** → Re-run generate_skill.py with --multi-env --force

## Examples

User: "Create a skill for the PagerDuty API from their OpenAPI spec"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/fetch_docs.py https://api.pagerduty.com/openapi.json | python3 ${CLAUDE_SKILL_DIR}/scripts/generate_skill.py --name pagerduty --output ~/.claude/skills/pagerduty
```

User: "Generate a Petstore skill with full environment support"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/fetch_docs.py https://petstore.swagger.io/v2/swagger.json | python3 ${CLAUDE_SKILL_DIR}/scripts/generate_skill.py --name petstore --output ~/.claude/skills/petstore --multi-env --shell-source
```

User: "What endpoints does this API have?"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/fetch_docs.py https://api.example.com/openapi.json
```

User: "Regenerate the Splunk skill from the new API docs"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/fetch_docs.py https://docs.splunk.com/openapi.json > /tmp/new_splunk.json
# Compare with existing: cat ~/.claude/skills/splunk/api_spec.json
cat /tmp/new_splunk.json | python3 ${CLAUDE_SKILL_DIR}/scripts/generate_skill.py --name splunk --output ~/.claude/skills/splunk --multi-env --shell-source --force
```
