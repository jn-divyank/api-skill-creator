#!/usr/bin/env python3
"""
generate_skill.py — Generate a complete Claude Code skill from a parsed API spec.

Reads JSON from stdin (output of fetch_docs.py), produces:
  <output>/SKILL.md          — Claude Code skill definition
  <output>/scripts/<name>_cli.py  — Python CLI with nested subcommand groups
  <output>/api_spec.json     — Persisted spec for incremental updates

Usage:
    python3 fetch_docs.py <URL> | python3 generate_skill.py --name petstore
    python3 fetch_docs.py <URL> | python3 generate_skill.py --name petstore --output ~/.claude/skills/petstore

Default output: ./output/<name>  (created automatically in the current directory)

Optional flags:
    --multi-env      Add multi-environment support (dev/stg/pro)
    --shell-source   Add shell profile sourcing for env vars
    --force          Overwrite existing output directory
"""

import json
import os
import re
import stat
import sys
import textwrap
from collections import defaultdict


# ---------------------------------------------------------------------------
# CLI argument parsing
# ---------------------------------------------------------------------------
def parse_args():
    import argparse
    p = argparse.ArgumentParser(description="Generate Claude Code skill from API spec JSON")
    p.add_argument("--name", required=True, help="Service name (lowercase, hyphens). Used for directory and file naming.")
    p.add_argument("--output", default=None, help="Output directory (default: ./output/<name>)")
    p.add_argument("--multi-env", action="store_true", dest="multi_env", help="Add multi-environment support (dev/stg/pro)")
    p.add_argument("--shell-source", action="store_true", dest="shell_source", help="Add shell profile sourcing (~/.zshrc) for env var loading")
    p.add_argument("--force", action="store_true", help="Overwrite existing output directory")
    return p.parse_args()


# ---------------------------------------------------------------------------
# Name utilities
# ---------------------------------------------------------------------------
def _validate_name(name):
    """Ensure name is a valid skill directory name."""
    if not re.match(r'^[a-z0-9][a-z0-9\-]{0,62}[a-z0-9]?$', name):
        print(f"Error: name '{name}' must be 1-64 chars, lowercase + hyphens only", file=sys.stderr)
        sys.exit(1)
    return name


def _env_prefix(name):
    """Convert service name to environment variable prefix: petstore → PETSTORE."""
    return name.upper().replace("-", "_")


def _python_ident(s):
    """Convert a string to a valid Python identifier."""
    s = re.sub(r'[^a-zA-Z0-9_]', '_', s)
    s = re.sub(r'_+', '_', s).strip('_')
    if s and s[0].isdigit():
        s = '_' + s
    return s or 'unnamed'


# ---------------------------------------------------------------------------
# Group endpoints into resource → actions
# ---------------------------------------------------------------------------
def group_endpoints(endpoints):
    """
    Group endpoints into resource→action structure for nested subcommand groups.

    Returns dict: { resource_name: [ {action, method, path, summary, params, body_fields} ] }
    """
    groups = defaultdict(list)

    for ep in endpoints:
        # Determine resource name from tags or path
        resource = _infer_resource(ep)
        action = _infer_action(ep)

        groups[resource].append({
            "action": action,
            "method": ep["method"],
            "path": ep["path"],
            "summary": ep.get("summary", ""),
            "parameters": ep.get("parameters", []),
            "body_fields": ep.get("body_fields", []),
            "operation_id": ep.get("operation_id", ""),
        })

    # If total endpoints ≤5 and ≤2 groups, flatten to single level
    total = sum(len(v) for v in groups.values())
    if total <= 5 and len(groups) <= 2:
        flat = {}
        for resource, actions in groups.items():
            for act in actions:
                flat_name = f"{resource}-{act['action']}" if len(groups) > 1 else act["action"]
                flat[flat_name] = [act]
        return flat

    # Deduplicate action names within a group
    for resource, actions in groups.items():
        seen = {}
        for act in actions:
            base = act["action"]
            if base in seen:
                seen[base] += 1
                act["action"] = f"{base}-{seen[base]}"
            else:
                seen[base] = 1

    return dict(groups)


def _infer_resource(ep):
    """Infer the resource group name for an endpoint."""
    # Prefer tags
    tags = ep.get("tags", [])
    if tags:
        return _slugify(tags[0])

    # Fall back to first meaningful path segment
    parts = [p for p in ep["path"].strip("/").split("/") if p and not p.startswith("{")]
    if parts:
        # Skip version prefixes like v1, v2, api
        for part in parts:
            if not re.match(r'^(v\d+|api|rest)$', part, re.IGNORECASE):
                return _slugify(part)
        return _slugify(parts[-1])

    return "general"


def _infer_action(ep):
    """Infer action name from method + path."""
    method = ep["method"].upper()
    path = ep["path"]

    # If operationId exists, derive from it
    op_id = ep.get("operation_id", "")
    if op_id:
        # Handle slash-separated operationIds like "rate-limit/get" or "repos/list-branches"
        # Use only the last segment after the slash
        if "/" in op_id:
            op_id = op_id.split("/")[-1]

        # e.g., getUserById → get, listUsers → list, createUser → create
        for prefix in ("get", "list", "find", "search", "create", "add", "update", "delete", "remove", "upload"):
            if op_id.lower().startswith(prefix):
                return prefix if prefix not in ("find", "search") else "list"
        return _slugify(op_id)

    # Infer from method + path pattern
    has_id = bool(re.search(r'\{[^}]+\}', path.split("/")[-1] if "/" in path else ""))
    ends_with_param = has_id

    if method == "GET":
        return "get" if ends_with_param else "list"
    elif method == "POST":
        return "create"
    elif method in ("PUT", "PATCH"):
        return "update"
    elif method == "DELETE":
        return "delete"
    else:
        return method.lower()


def _slugify(s):
    """Convert to lowercase-hyphen format."""
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9\-]', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s or "unnamed"


# ---------------------------------------------------------------------------
# Python CLI generator
# ---------------------------------------------------------------------------
def generate_cli_script(spec, name, groups, multi_env=False, shell_source=False):
    """Generate the full Python CLI script content."""
    prefix = _env_prefix(name)
    lines = []

    # -- Header
    lines.append('#!/usr/bin/env python3')
    lines.append(f'"""')
    lines.append(f'{name} CLI tool for Claude Code skill integration.')
    lines.append(f'Provides access to the {spec.get("service_name", name)} API.')
    lines.append(f'"""')
    lines.append('')

    # -- Imports
    lines.append('import argparse')
    lines.append('import base64')
    lines.append('import json')
    lines.append('import os')
    if shell_source:
        lines.append('import subprocess')
    lines.append('import ssl')
    lines.append('import sys')
    lines.append('import urllib.error')
    lines.append('import urllib.parse')
    lines.append('import urllib.request')
    lines.append('')

    # -- dotenv loading (always on) + optional shell profile sourcing
    lines.append('')
    lines.append('def _load_environment() -> dict:')
    lines.append('    """Load env vars: os.environ → ~/.skills.env → optional shell profile."""')
    lines.append('    env = os.environ.copy()')
    lines.append('    dotenv_path = os.path.expanduser("~/.skills.env")')
    lines.append('    if os.path.exists(dotenv_path):')
    lines.append('        try:')
    lines.append('            with open(dotenv_path) as f:')
    lines.append('                for line in f:')
    lines.append('                    line = line.strip()')
    lines.append('                    if not line or line.startswith("#") or "=" not in line:')
    lines.append('                        continue')
    lines.append('                    # strip optional leading "export "')
    lines.append('                    if line.startswith("export "):')
    lines.append('                        line = line[7:]')
    lines.append('                    k, v = line.split("=", 1)')
    lines.append('                    k = k.strip()')
    lines.append("                    v = v.strip().strip('\"\\'')")
    lines.append('                    if k and k not in env:')
    lines.append('                        env[k] = v')
    lines.append('        except Exception:')
    lines.append('            pass')
    if shell_source:
        lines.append('    # also source shell profile as fallback')
        lines.append(f'    required = ["{prefix}_URL", "{prefix}_TOKEN"]')
        lines.append('    if not all(k in env for k in required):')
        lines.append('        for profile in [os.path.expanduser("~/.zshrc"), os.path.expanduser("~/.bashrc")]:')
        lines.append('            if os.path.exists(profile):')
        lines.append('                shell = "zsh" if profile.endswith(".zshrc") else "bash"')
        lines.append('                try:')
        lines.append('                    result = subprocess.run(')
        lines.append(f'                        f"source {{profile}} && env",')
        lines.append('                        shell=True, executable=f"/bin/{shell}",')
        lines.append('                        capture_output=True, text=True, timeout=5')
        lines.append('                    )')
        lines.append('                    if result.returncode == 0:')
        lines.append('                        for line in result.stdout.split("\\n"):')
        lines.append('                            if "=" in line:')
        lines.append('                                k, v = line.split("=", 1)')
        lines.append('                                if k not in env:')
        lines.append('                                    env[k] = v')
        lines.append('                    break')
        lines.append('                except Exception:')
        lines.append('                    pass')
    lines.append('    return env')
    lines.append('')
    lines.append('')
    lines.append('_env = _load_environment()')

    # -- Module globals
    lines.append('')
    lines.append('# --- Configuration ---')
    if multi_env:
        lines.append(f'ACTIVE_ENV = _env.get("RPSP_ENV", "dev")')
        lines.append('')
        lines.append('')
        lines.append('def _get_env_var(base_name):')
        lines.append('    """Get environment variable with per-env fallback: SERVICE_DEV_URL → SERVICE_URL."""')
        lines.append(f'    env_key = f"{prefix}_{{ACTIVE_ENV.upper()}}_{{base_name}}"')
        lines.append(f'    val = _env.get(env_key)')
        lines.append('    if val:')
        lines.append('        return val')
        lines.append(f'    return _env.get(f"{prefix}_{{base_name}}", "")')
        lines.append('')
        lines.append('')
        lines.append(f'BASE_URL = _get_env_var("URL") or "{spec.get("base_url", "")}"')
        lines.append(f'AUTH_TOKEN = _get_env_var("TOKEN")')
    else:
        lines.append(f'BASE_URL = _env.get("{prefix}_URL", "{spec.get("base_url", "")}")')
        lines.append(f'AUTH_TOKEN = _env.get("{prefix}_TOKEN", "")')

    # -- SSL context
    lines.append('')
    lines.append('_ssl_ctx = ssl.create_default_context()')
    lines.append(f'if _env.get("{prefix}_VERIFY_SSL", "true").lower() == "false":')
    lines.append('    _ssl_ctx.check_hostname = False')
    lines.append('    _ssl_ctx.verify_mode = ssl.CERT_NONE')
    lines.append('')

    # -- Auth header
    lines.append('')
    auth_type = spec.get("auth_type", "bearer")
    lines.append('def get_auth_header() -> dict:')
    lines.append('    """Build authorization header."""')
    if auth_type == "bearer":
        lines.append('    if AUTH_TOKEN:')
        lines.append('        return {"Authorization": f"Bearer {AUTH_TOKEN}"}')
    elif auth_type == "basic":
        lines.append('    if AUTH_TOKEN:')
        lines.append('        # AUTH_TOKEN should be "user:password"')
        lines.append('        encoded = base64.b64encode(AUTH_TOKEN.encode()).decode()')
        lines.append('        return {"Authorization": f"Basic {encoded}"}')
    elif auth_type in ("api_key", "api_key_query"):
        auth_header_fmt = spec.get("auth_header_format", "X-API-Key: {token}")
        header_name = auth_header_fmt.split(":")[0].strip() if ":" in auth_header_fmt else "X-API-Key"
        lines.append('    if AUTH_TOKEN:')
        lines.append(f'        return {{"{header_name}": AUTH_TOKEN}}')
    else:
        lines.append('    if AUTH_TOKEN:')
        lines.append('        return {"Authorization": f"Bearer {AUTH_TOKEN}"}')
    lines.append('    return {}')
    lines.append('')

    # -- make_request
    lines.append('')
    lines.append('def make_request(path: str, method: str = "GET", data: bytes = None, params: dict = None) -> tuple:')
    lines.append(f'    """Make HTTP request to the {name} API."""')
    lines.append('    base = BASE_URL.rstrip("/")')
    lines.append('    url = f"{base}/{path.lstrip(\'/\')}"')
    lines.append('    if params:')
    lines.append('        url = f"{url}?{urllib.parse.urlencode(params)}"')
    lines.append('')
    lines.append('    headers = get_auth_header()')
    lines.append('    headers["Content-Type"] = "application/json"')
    lines.append('    headers["Accept"] = "application/json"')
    lines.append('')
    lines.append('    req = urllib.request.Request(url, data=data, headers=headers, method=method)')
    lines.append('    try:')
    lines.append('        with urllib.request.urlopen(req, timeout=30, context=_ssl_ctx) as resp:')
    lines.append('            return resp.status, resp.read().decode("utf-8")')
    lines.append('    except urllib.error.HTTPError as e:')
    lines.append('        return e.code, e.read().decode("utf-8", errors="replace")')
    lines.append('    except urllib.error.URLError as e:')
    lines.append('        return 0, f"Connection error: {e.reason}"')
    lines.append('    except Exception as e:')
    lines.append('        return 0, f"Error: {e}"')
    lines.append('')

    # -- check command
    lines.append('')
    lines.append('def cmd_check(args):')
    lines.append(f'    """Verify connectivity to the {name} API."""')
    lines.append('    if not BASE_URL:')
    lines.append(f'        print(f"Error: {prefix}_URL not set", file=sys.stderr)')
    lines.append('        sys.exit(1)')
    lines.append('    status, body = make_request("/")')
    lines.append('    if status == 0:')
    lines.append('        print(f"Cannot connect to {BASE_URL}", file=sys.stderr)')
    lines.append(f'        print(f"Error: {{body}}", file=sys.stderr)')
    lines.append('        sys.exit(1)')
    lines.append('    print(f"Connected to {BASE_URL} (HTTP {status})")')
    lines.append('')

    # -- Generate command functions for each resource/action
    for resource, actions in sorted(groups.items()):
        for act in actions:
            func_name = f"cmd_{_python_ident(resource)}_{_python_ident(act['action'])}"
            lines.append('')
            lines.append(f'def {func_name}(args):')
            summary = act.get("summary", f'{act["method"]} {act["path"]}')
            lines.append(f'    """{summary}"""')

            # Build the path with parameter substitution
            path = act["path"]
            path_params = re.findall(r'\{(\w+)\}', path)

            # Substitute path params from args
            for pp in path_params:
                arg_name = _python_ident(pp)
                lines.append(f'    path = "{path}".replace("{{{pp}}}", str(args.{arg_name}))')
                path = f'{{already_substituted}}'  # prevent double substitution in template

            if path_params:
                pass  # path already built via .replace() calls above
            else:
                lines.append(f'    path = "{path}"')

            # Build query params
            query_params = [p for p in act.get("parameters", []) if p.get("in") == "query" and p.get("name", "").strip()]
            if query_params:
                lines.append('    params = {}')
                for qp in query_params:
                    arg_name = _python_ident(qp["name"])
                    lines.append(f'    if args.{arg_name} is not None:')
                    lines.append(f'        params["{qp["name"]}"] = args.{arg_name}')

            # Build request body
            body_fields = act.get("body_fields", [])
            method = act["method"]

            if method in ("POST", "PUT", "PATCH") and body_fields:
                lines.append('    body = {}')
                for bf in body_fields:
                    arg_name = _python_ident(bf["name"])
                    lines.append(f'    if args.{arg_name} is not None:')
                    lines.append(f'        body["{bf["name"]}"] = args.{arg_name}')
                lines.append('    data = json.dumps(body).encode("utf-8") if body else None')
            elif method in ("POST", "PUT", "PATCH"):
                # Accept raw JSON from --data flag
                lines.append('    data = None')
                lines.append('    if hasattr(args, "data") and args.data:')
                lines.append('        data = args.data.encode("utf-8")')
            else:
                lines.append('    data = None')

            # Make request
            param_arg = "params" if query_params else "None"
            lines.append(f'    status, body = make_request(path, "{method}", data=data, params={param_arg})')

            # Handle response
            lines.append('    if status == 0 or status >= 400:')
            lines.append(f'        print(f"Error (HTTP {{status}}): {{body}}", file=sys.stderr)')
            lines.append('        sys.exit(1)')
            lines.append('    try:')
            lines.append('        result = json.loads(body)')
            lines.append('        print(json.dumps(result, indent=2))')
            lines.append('    except (json.JSONDecodeError, ValueError):')
            lines.append('        print(body)')
            lines.append('')

    # -- Argparse setup with nested subcommand groups
    lines.append('')
    lines.append('def main():')
    if multi_env:
        lines.append('    global ACTIVE_ENV, BASE_URL, AUTH_TOKEN')
    lines.append(f'    parser = argparse.ArgumentParser(description="{name} CLI")')

    if multi_env:
        lines.append('    parser.add_argument("--env", choices=["dev", "stg", "pro"], default=None,')
        lines.append('                        help="Environment to use (overrides RPSP_ENV)")')

    lines.append('    subparsers = parser.add_subparsers(dest="command", help="Available commands")')
    lines.append('')

    # check command
    lines.append('    # --- check ---')
    lines.append('    subparsers.add_parser("check", help="Test API connectivity")')
    lines.append('')

    # For each resource group, create a sub-parser with its own sub-parsers
    for resource, actions in sorted(groups.items()):
        resource_var = _python_ident(resource)
        lines.append(f'    # --- {resource} ---')
        lines.append(f'    parser_{resource_var} = subparsers.add_parser("{resource}", help="{resource.title()} operations")')
        lines.append(f'    sub_{resource_var} = parser_{resource_var}.add_subparsers(dest="{resource_var}_action", help="{resource} actions")')
        lines.append('')

        for act in actions:
            action_name = act["action"]
            action_var = _python_ident(action_name)
            func_name = f"cmd_{resource_var}_{action_var}"
            summary = act.get("summary", f'{act["method"]} {act["path"]}')
            # Sanitize text for embedding in double-quoted Python string literals
            def _safe_str(s):
                return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").replace("\r", "")
            summary_escaped = _safe_str(summary)
            lines.append(f'    p_{resource_var}_{action_var} = sub_{resource_var}.add_parser("{action_name}", help="{summary_escaped}")')

            # Add path parameters as positional args
            path_params = re.findall(r'\{(\w+)\}', act["path"])
            for pp in path_params:
                arg_name = _python_ident(pp)
                lines.append(f'    p_{resource_var}_{action_var}.add_argument("{arg_name}", help="{pp}")')

            # Add query parameters as optional args
            query_params = [p for p in act.get("parameters", []) if p.get("in") == "query" and p.get("name", "").strip()]
            for qp in query_params:
                arg_name = _python_ident(qp["name"])
                flag = f'--{qp["name"].replace("_", "-")}'
                desc = _safe_str(qp.get("description", ""))
                lines.append(f'    p_{resource_var}_{action_var}.add_argument("{flag}", dest="{arg_name}", default=None, help="{desc}")')

            # Add body fields as optional args for POST/PUT/PATCH
            body_fields = act.get("body_fields", [])
            method = act["method"]
            if method in ("POST", "PUT", "PATCH"):
                if body_fields:
                    for bf in body_fields:
                        arg_name = _python_ident(bf["name"])
                        flag = f'--{bf["name"].replace("_", "-")}'
                        lines.append(f'    p_{resource_var}_{action_var}.add_argument("{flag}", dest="{arg_name}", default=None, help="{bf["name"]}")')
                else:
                    lines.append(f'    p_{resource_var}_{action_var}.add_argument("--data", default=None, help="JSON request body")')

            lines.append(f'    p_{resource_var}_{action_var}.set_defaults(func={func_name})')
            lines.append('')

    # -- Parse and dispatch
    lines.append('    args = parser.parse_args()')

    if multi_env:
        lines.append('')
        lines.append('    if args.env:')
        lines.append('        ACTIVE_ENV = args.env')
        lines.append('        BASE_URL = _get_env_var("URL") or BASE_URL')
        lines.append('        AUTH_TOKEN = _get_env_var("TOKEN") or AUTH_TOKEN')

    lines.append('')
    lines.append('    if args.command == "check":')
    lines.append('        cmd_check(args)')
    lines.append('    elif hasattr(args, "func"):')
    lines.append('        args.func(args)')
    lines.append('    else:')
    lines.append('        parser.print_help()')
    lines.append('        sys.exit(1)')
    lines.append('')
    lines.append('')
    lines.append('if __name__ == "__main__":')
    lines.append('    main()')
    lines.append('')

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# SKILL.md generator
# ---------------------------------------------------------------------------
def generate_skill_md(spec, name, groups, multi_env=False, shell_source=False):
    """Generate SKILL.md content."""
    prefix = _env_prefix(name)
    script_path = f'${{CLAUDE_SKILL_DIR}}/scripts/{name}_cli.py'

    lines = []

    # -- Frontmatter
    lines.append('---')
    lines.append(f'name: {name}')
    svc = spec.get("service_name", name)
    desc = (
        f'Interact with {svc} API. Use for querying, creating, and managing {svc} resources. '
        f'Use when asked about {svc} operations.'
    )
    if len(desc) > 1024:
        desc = desc[:1021] + "..."
    lines.append(f'description: {desc}')
    lines.append(f'argument-hint: [command] [args]')
    lines.append(f'allowed-tools: Bash(python3:*)')
    lines.append('---')
    lines.append('')

    # -- Title
    lines.append(f'# {svc.replace("-", " ").title()} Integration')
    lines.append('')

    # -- Configuration
    lines.append('## Configuration')
    lines.append('')
    lines.append('Set these environment variables in `~/.zshrc`:')
    lines.append('')
    if multi_env:
        lines.append('**Shared (used by all skills):**')
        lines.append('- `RPSP_ENV` — Active environment: `dev`, `stg`, or `pro`. Default: `dev`')
        lines.append('')
        lines.append(f'**Per-environment {svc} config:**')
        lines.append(f'- `{prefix}_DEV_URL` / `{prefix}_STG_URL` / `{prefix}_PRO_URL` — API base URL')
        lines.append(f'- `{prefix}_DEV_TOKEN` / `{prefix}_STG_TOKEN` / `{prefix}_PRO_TOKEN` — Auth token')
    else:
        lines.append(f'- `{prefix}_URL` — API base URL (default: `{spec.get("base_url", "")}`)')
        lines.append(f'- `{prefix}_TOKEN` — Authentication token')
    lines.append('')

    if shell_source:
        lines.append('**IMPORTANT**: Always run the Python script directly — it loads environment')
        lines.append('variables from `~/.zshrc` automatically. Do NOT use `echo` or `export` commands')
        lines.append('to check/set variables first.')
        lines.append('')

    # -- Available Commands
    lines.append('## Available Commands')
    lines.append('')

    lines.append('### Check Connection')
    lines.append('```bash')
    lines.append(f'python3 {script_path} check')
    if multi_env:
        lines.append(f'python3 {script_path} --env stg check')
    lines.append('```')
    lines.append('')

    for resource, actions in sorted(groups.items()):
        lines.append(f'### {resource.title()}')
        lines.append('```bash')
        for act in actions:
            cmd_parts = [f'python3 {script_path}']
            if multi_env:
                pass  # don't add --env in every example
            cmd_parts.append(resource)
            cmd_parts.append(act["action"])

            # Add example args
            path_params = re.findall(r'\{(\w+)\}', act["path"])
            for pp in path_params:
                cmd_parts.append(pp.upper())

            query_params = [p for p in act.get("parameters", []) if p.get("in") == "query"]
            for qp in query_params[:2]:  # show max 2 query params in example
                cmd_parts.append(f'--{qp["name"].replace("_", "-")} VALUE')

            lines.append(f'# {act.get("summary", act["method"] + " " + act["path"])}')
            lines.append(' '.join(cmd_parts))
        lines.append('```')
        lines.append('')

    # -- Usage Instructions
    lines.append('## Usage Instructions')
    lines.append('')
    if shell_source:
        lines.append(f'**CRITICAL: Do NOT run `echo ${prefix}_URL` or check/export env vars before using')
        lines.append('this skill. The Python script loads all variables from `~/.zshrc` internally.**')
        lines.append('')
    lines.append('Map user requests to commands:')
    lines.append('')

    idx = 1
    lines.append(f'{idx}. **"Is {svc} reachable?"** / **"Test connection"** → `check`')
    idx += 1

    for resource, actions in sorted(groups.items()):
        for act in actions:
            action_desc = act.get("summary", f'{act["action"]} {resource}')
            path_params = re.findall(r'\{(\w+)\}', act["path"])
            param_str = ' '.join(pp.upper() for pp in path_params)
            query_params = [p for p in act.get("parameters", []) if p.get("in") == "query"]
            flag_str = ' '.join(f'--{qp["name"].replace("_", "-")} VALUE' for qp in query_params[:1])
            cmd = f'{resource} {act["action"]}'
            if param_str:
                cmd += f' {param_str}'
            if flag_str:
                cmd += f' {flag_str}'
            lines.append(f'{idx}. **"{action_desc}"** → `{cmd}`')
            idx += 1

    lines.append('')

    # -- Examples
    lines.append('## Examples')
    lines.append('')

    # Generate a few representative examples
    example_count = 0
    lines.append(f'User: "Is {svc} connected?"')
    lines.append('```bash')
    lines.append(f'python3 {script_path} check')
    lines.append('```')
    lines.append('')
    example_count += 1

    for resource, actions in sorted(groups.items()):
        if example_count >= 5:
            break
        for act in actions[:1]:  # one example per resource
            if example_count >= 5:
                break
            cmd_parts = [f'python3 {script_path}', resource, act["action"]]
            path_params = re.findall(r'\{(\w+)\}', act["path"])
            for pp in path_params:
                cmd_parts.append(f'EXAMPLE_{pp.upper()}')
            summary = act.get("summary", f'{act["action"]} {resource}')
            lines.append(f'User: "{summary}"')
            lines.append('```bash')
            lines.append(' '.join(cmd_parts))
            lines.append('```')
            lines.append('')
            example_count += 1

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    args = parse_args()
    name = _validate_name(args.name)
    output = os.path.expanduser(args.output) if args.output else os.path.join("output", name)

    # Read spec from stdin
    try:
        spec = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error: Invalid JSON on stdin: {e}", file=sys.stderr)
        sys.exit(1)

    # Create output directory
    if os.path.exists(output) and not args.force:
        print(f"Error: Output directory '{output}' already exists. Use --force to overwrite.", file=sys.stderr)
        sys.exit(1)

    scripts_dir = os.path.join(output, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    # Group endpoints
    groups = group_endpoints(spec.get("endpoints", []))

    if not groups:
        print("Warning: No endpoint groups generated. Check your spec.", file=sys.stderr)

    # Save api_spec.json
    spec_path = os.path.join(output, "api_spec.json")
    with open(spec_path, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
        f.write("\n")
    print(f"Saved API spec: {spec_path}", file=sys.stderr)

    # Generate CLI script
    cli_content = generate_cli_script(
        spec, name, groups,
        multi_env=args.multi_env, shell_source=args.shell_source,
    )
    cli_path = os.path.join(scripts_dir, f"{name}_cli.py")
    with open(cli_path, "w", encoding="utf-8") as f:
        f.write(cli_content)
    os.chmod(cli_path, os.stat(cli_path).st_mode | stat.S_IEXEC)
    print(f"Generated CLI: {cli_path}", file=sys.stderr)

    # Generate SKILL.md
    skill_content = generate_skill_md(
        spec, name, groups,
        multi_env=args.multi_env, shell_source=args.shell_source,
    )
    skill_path = os.path.join(output, "SKILL.md")
    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(skill_content)
    print(f"Generated SKILL.md: {skill_path}", file=sys.stderr)

    # Summary
    total_endpoints = sum(len(v) for v in groups.values())
    print(f"\nSkill '{name}' generated successfully!", file=sys.stderr)
    print(f"  Resources: {len(groups)} ({', '.join(sorted(groups.keys()))})", file=sys.stderr)
    print(f"  Endpoints: {total_endpoints}", file=sys.stderr)
    print(f"  Output: {output}", file=sys.stderr)

    prefix = _env_prefix(name)
    if args.multi_env:
        print(f"\nSet environment variables in ~/.zshrc:", file=sys.stderr)
        print(f"  export {prefix}_DEV_URL=<url>", file=sys.stderr)
        print(f"  export {prefix}_DEV_TOKEN=<token>", file=sys.stderr)
    else:
        print(f"\nSet environment variables in ~/.zshrc:", file=sys.stderr)
        print(f"  export {prefix}_URL=<url>", file=sys.stderr)
        print(f"  export {prefix}_TOKEN=<token>", file=sys.stderr)


if __name__ == "__main__":
    main()
