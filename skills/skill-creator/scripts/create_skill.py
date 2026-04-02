#!/usr/bin/env python3
"""
create_skill.py — One-step wrapper: fetch API docs → generate skill → install.

Usage:
    python3 create_skill.py <API_DOC_URL> [--name <name>] [--multi-env] [--shell-source]

The URL can be an OpenAPI 3.x, Swagger 2.0, Postman v2, or HTML docs page.
Installs directly to ~/.claude/skills/<name>/ when --output is not specified.
"""

import argparse
import json
import os
import subprocess
import sys

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
FETCH_DOCS   = os.path.join(SCRIPTS_DIR, "fetch_docs.py")
GEN_SKILL    = os.path.join(SCRIPTS_DIR, "generate_skill.py")


def main():
    p = argparse.ArgumentParser(
        description="Fetch API docs and generate a Claude Code skill in one step."
    )
    p.add_argument("url", help="API documentation URL (OpenAPI, Swagger, Postman, HTML)")
    p.add_argument("--name", default=None, help="Skill name (inferred from spec if omitted)")
    p.add_argument("--output", default=None, help="Output directory (default: ~/.claude/skills/<name>)")
    p.add_argument("--multi-env", action="store_true", dest="multi_env")
    p.add_argument("--shell-source", action="store_true", dest="shell_source")
    p.add_argument("--force", action="store_true")
    args = p.parse_args()

    # --- Step 1: fetch ---
    print(f"Fetching API docs from: {args.url}", flush=True)
    fetch_result = subprocess.run(
        [sys.executable, FETCH_DOCS, args.url],
        capture_output=True, text=True
    )
    if fetch_result.returncode != 0:
        print(fetch_result.stderr.strip(), file=sys.stderr)
        sys.exit(1)

    # Print any warnings from fetch step
    for line in fetch_result.stderr.strip().splitlines():
        print(line)

    spec_json = fetch_result.stdout

    # --- Infer name from spec if not provided ---
    if not args.name:
        try:
            spec = json.loads(spec_json)
            raw = spec.get("service_name", "api-skill")
            import re
            name = re.sub(r'[^a-z0-9]+', '-', raw.lower()).strip('-')[:40]
        except Exception:
            name = "api-skill"
        args.name = name
        print(f"Inferred skill name: {args.name}")

    # --- Default output to ~/.claude/skills/<name> ---
    if not args.output:
        args.output = os.path.expanduser(f"~/.claude/skills/{args.name}")

    # --- Step 2: generate ---
    print(f"Generating skill '{args.name}' → {args.output}", flush=True)
    gen_cmd = [sys.executable, GEN_SKILL, "--name", args.name, "--output", args.output]
    if args.multi_env:
        gen_cmd.append("--multi-env")
    if args.shell_source:
        gen_cmd.append("--shell-source")
    if args.force:
        gen_cmd.append("--force")

    gen_result = subprocess.run(gen_cmd, input=spec_json, capture_output=True, text=True)
    if gen_result.returncode != 0:
        print(gen_result.stderr.strip(), file=sys.stderr)
        sys.exit(1)

    print(gen_result.stdout.strip())
    if gen_result.stderr.strip():
        print(gen_result.stderr.strip())

    # --- Make CLI executable ---
    scripts_dir = os.path.join(args.output, "scripts")
    if os.path.isdir(scripts_dir):
        for f in os.listdir(scripts_dir):
            if f.endswith(".py"):
                os.chmod(os.path.join(scripts_dir, f), 0o755)

    # --- Done ---
    cli = os.path.join(args.output, "scripts", f"{args.name}_cli.py")
    print()
    print(f"Done! Test it:")
    print(f"  python3 {cli} --help")
    print(f"  python3 {cli} check")


if __name__ == "__main__":
    main()
