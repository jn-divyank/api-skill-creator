#!/usr/bin/env python3
"""Tests for generate_skill.py — Claude Code skill generator."""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "skills", "skill-creator", "scripts", "generate_skill.py")

# Sample spec matching the output format of fetch_docs.py
SAMPLE_SPEC = {
    "service_name": "test-api",
    "base_url": "https://api.example.com/v1",
    "auth_type": "bearer",
    "auth_header_format": "Bearer {token}",
    "env_vars_needed": ["TEST_API_URL", "TEST_API_TOKEN"],
    "endpoints": [
        {
            "method": "GET", "path": "/users",
            "summary": "List all users", "tags": ["users"],
            "parameters": [{"name": "limit", "in": "query", "required": False, "description": "Max results"}],
            "body_fields": [], "operation_id": "listUsers"
        },
        {
            "method": "GET", "path": "/users/{id}",
            "summary": "Get user by ID", "tags": ["users"],
            "parameters": [{"name": "id", "in": "path", "required": True, "description": "User ID"}],
            "body_fields": [], "operation_id": "getUserById"
        },
        {
            "method": "POST", "path": "/users",
            "summary": "Create a user", "tags": ["users"],
            "parameters": [],
            "body_fields": [
                {"name": "name", "required": True, "type": "string"},
                {"name": "email", "required": False, "type": "string"}
            ],
            "operation_id": "createUser"
        },
        {
            "method": "DELETE", "path": "/users/{id}",
            "summary": "Delete a user", "tags": ["users"],
            "parameters": [{"name": "id", "in": "path", "required": True, "description": "User ID"}],
            "body_fields": [], "operation_id": "deleteUser"
        },
        {
            "method": "GET", "path": "/items",
            "summary": "List items", "tags": ["items"],
            "parameters": [], "body_fields": [], "operation_id": "listItems"
        },
        {
            "method": "GET", "path": "/items/{itemId}",
            "summary": "Get item", "tags": ["items"],
            "parameters": [{"name": "itemId", "in": "path", "required": True, "description": ""}],
            "body_fields": [], "operation_id": "getItem"
        },
    ],
    "source_format": "swagger2"
}


class TestGenerateSkill(unittest.TestCase):
    """Test the skill generator output."""

    def setUp(self):
        self.outdir = tempfile.mkdtemp(prefix="skill_test_")

    def tearDown(self):
        shutil.rmtree(self.outdir, ignore_errors=True)

    def _generate(self, name="test-api", extra_args=None):
        """Run generate_skill.py with SAMPLE_SPEC and return (returncode, stderr)."""
        cmd = [sys.executable, SCRIPT, "--name", name, "--output", self.outdir, "--force"]
        if extra_args:
            cmd.extend(extra_args)
        result = subprocess.run(
            cmd,
            input=json.dumps(SAMPLE_SPEC),
            capture_output=True, text=True, timeout=10
        )
        return result.returncode, result.stderr

    def test_basic_generation(self):
        """Test that basic generation produces all expected files."""
        rc, stderr = self._generate()
        self.assertEqual(rc, 0, f"Generation failed: {stderr}")

        self.assertTrue(os.path.exists(os.path.join(self.outdir, "SKILL.md")))
        self.assertTrue(os.path.exists(os.path.join(self.outdir, "scripts", "test-api_cli.py")))
        self.assertTrue(os.path.exists(os.path.join(self.outdir, "api_spec.json")))

    def test_skill_md_frontmatter(self):
        """Test SKILL.md has valid YAML frontmatter."""
        self._generate()
        skill_path = os.path.join(self.outdir, "SKILL.md")
        with open(skill_path) as f:
            content = f.read()

        # Must start with ---
        self.assertTrue(content.startswith("---"))

        # Extract frontmatter
        parts = content.split("---", 2)
        self.assertGreaterEqual(len(parts), 3)
        frontmatter = parts[1]

        # Required fields
        self.assertIn("name: test-api", frontmatter)
        self.assertIn("allowed-tools:", frontmatter)
        self.assertIn("description:", frontmatter)
        self.assertIn("argument-hint:", frontmatter)

    def test_skill_md_sections(self):
        """Test SKILL.md has required sections."""
        self._generate()
        skill_path = os.path.join(self.outdir, "SKILL.md")
        with open(skill_path) as f:
            content = f.read()

        self.assertIn("## Configuration", content)
        self.assertIn("## Available Commands", content)
        self.assertIn("### Check Connection", content)
        self.assertIn("## Usage Instructions", content)
        self.assertIn("## Examples", content)
        self.assertIn("${CLAUDE_SKILL_DIR}", content)

    def test_cli_help_runs(self):
        """Test generated CLI --help runs without errors."""
        self._generate()
        cli_path = os.path.join(self.outdir, "scripts", "test-api_cli.py")

        result = subprocess.run(
            [sys.executable, cli_path, "--help"],
            capture_output=True, text=True, timeout=10
        )
        self.assertEqual(result.returncode, 0, f"CLI --help failed: {result.stderr}")
        self.assertIn("check", result.stdout)

    def test_cli_nested_groups(self):
        """Test CLI has nested subcommand groups."""
        self._generate()
        cli_path = os.path.join(self.outdir, "scripts", "test-api_cli.py")

        # Top-level should show resource groups
        result = subprocess.run(
            [sys.executable, cli_path, "--help"],
            capture_output=True, text=True, timeout=10
        )
        self.assertIn("users", result.stdout)
        self.assertIn("items", result.stdout)
        self.assertIn("check", result.stdout)

        # Resource group should show actions
        result = subprocess.run(
            [sys.executable, cli_path, "users", "--help"],
            capture_output=True, text=True, timeout=10
        )
        self.assertIn("list", result.stdout)
        self.assertIn("get", result.stdout)
        self.assertIn("create", result.stdout)
        self.assertIn("delete", result.stdout)

    def test_cli_check_subcommand(self):
        """Test that 'check' subcommand exists."""
        self._generate()
        cli_path = os.path.join(self.outdir, "scripts", "test-api_cli.py")

        result = subprocess.run(
            [sys.executable, cli_path, "--help"],
            capture_output=True, text=True, timeout=10
        )
        self.assertIn("check", result.stdout)

    def test_cli_core_patterns(self):
        """Test generated Python has core patterns."""
        self._generate()
        cli_path = os.path.join(self.outdir, "scripts", "test-api_cli.py")
        with open(cli_path) as f:
            code = f.read()

        # Core patterns that must always be present
        self.assertIn("def get_auth_header()", code)
        self.assertIn("def make_request(", code)
        self.assertIn("def cmd_check(", code)
        self.assertIn("argparse.ArgumentParser", code)
        self.assertIn("add_subparsers", code)
        self.assertIn("import urllib.request", code)
        self.assertIn("import json", code)
        self.assertIn("ssl.create_default_context()", code)
        self.assertIn("sys.stderr", code)

    def test_api_spec_saved(self):
        """Test that api_spec.json is saved correctly."""
        self._generate()
        spec_path = os.path.join(self.outdir, "api_spec.json")

        with open(spec_path) as f:
            saved = json.load(f)

        self.assertEqual(saved["service_name"], "test-api")
        self.assertEqual(saved["base_url"], "https://api.example.com/v1")
        self.assertEqual(len(saved["endpoints"]), 6)

    def test_multi_env_flag(self):
        """Test --multi-env generates environment switching code."""
        self._generate(extra_args=["--multi-env"])
        cli_path = os.path.join(self.outdir, "scripts", "test-api_cli.py")
        with open(cli_path) as f:
            code = f.read()

        self.assertIn("RPSP_ENV", code)
        self.assertIn("ACTIVE_ENV", code)
        self.assertIn("_get_env_var", code)
        self.assertIn('--env', code)
        self.assertIn('"dev"', code)
        self.assertIn('"stg"', code)
        self.assertIn('"pro"', code)

        # SKILL.md should mention multi-env
        skill_path = os.path.join(self.outdir, "SKILL.md")
        with open(skill_path) as f:
            skill = f.read()
        self.assertIn("RPSP_ENV", skill)

    def test_shell_source_flag(self):
        """Test --shell-source generates shell env loading."""
        self._generate(extra_args=["--shell-source"])
        cli_path = os.path.join(self.outdir, "scripts", "test-api_cli.py")
        with open(cli_path) as f:
            code = f.read()

        self.assertIn("_load_shell_environment", code)
        self.assertIn(".zshrc", code)
        self.assertIn(".bashrc", code)

    def test_all_flags(self):
        """Test with all flags enabled."""
        self._generate(extra_args=["--multi-env", "--shell-source"])
        cli_path = os.path.join(self.outdir, "scripts", "test-api_cli.py")

        # Should still run --help cleanly
        result = subprocess.run(
            [sys.executable, cli_path, "--help"],
            capture_output=True, text=True, timeout=10
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("--env", result.stdout)

    def test_force_flag(self):
        """Test that --force overwrites existing output."""
        # Generate twice to the same dir
        self._generate()
        rc, _ = self._generate()
        self.assertEqual(rc, 0)

    def test_no_force_fails_on_existing(self):
        """Test that generation fails without --force when dir exists."""
        self._generate()
        # Try again without --force
        cmd = [sys.executable, SCRIPT, "--name", "test-api", "--output", self.outdir]
        result = subprocess.run(
            cmd,
            input=json.dumps(SAMPLE_SPEC),
            capture_output=True, text=True, timeout=10
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("already exists", result.stderr)

    def test_invalid_name_rejected(self):
        """Test that invalid service names are rejected."""
        cmd = [sys.executable, SCRIPT, "--name", "INVALID NAME!", "--output", self.outdir, "--force"]
        result = subprocess.run(
            cmd,
            input=json.dumps(SAMPLE_SPEC),
            capture_output=True, text=True, timeout=10
        )
        self.assertNotEqual(result.returncode, 0)

    def test_bearer_auth(self):
        """Test bearer auth generation."""
        self._generate()
        cli_path = os.path.join(self.outdir, "scripts", "test-api_cli.py")
        with open(cli_path) as f:
            code = f.read()
        self.assertIn("Bearer", code)

    def test_api_key_auth(self):
        """Test API key auth generation."""
        spec = SAMPLE_SPEC.copy()
        spec["auth_type"] = "api_key"
        spec["auth_header_format"] = "X-API-Key: {token}"

        cmd = [sys.executable, SCRIPT, "--name", "test-api", "--output", self.outdir, "--force"]
        result = subprocess.run(
            cmd,
            input=json.dumps(spec),
            capture_output=True, text=True, timeout=10
        )
        self.assertEqual(result.returncode, 0)

        cli_path = os.path.join(self.outdir, "scripts", "test-api_cli.py")
        with open(cli_path) as f:
            code = f.read()
        self.assertIn("X-API-Key", code)


if __name__ == "__main__":
    unittest.main()
