#!/usr/bin/env python3
"""Tests for fetch_docs.py — API documentation parser."""

import json
import os
import subprocess
import sys
import unittest

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "skills", "skill-creator", "scripts", "fetch_docs.py")


class TestFetchDocsOpenAPI(unittest.TestCase):
    """Test parsing of OpenAPI/Swagger specs."""

    SAMPLE_SWAGGER2 = json.dumps({
        "swagger": "2.0",
        "info": {"title": "Test API", "version": "1.0"},
        "host": "api.example.com",
        "basePath": "/v1",
        "schemes": ["https"],
        "securityDefinitions": {
            "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
        },
        "paths": {
            "/users": {
                "get": {
                    "summary": "List users",
                    "tags": ["users"],
                    "operationId": "listUsers",
                    "parameters": [
                        {"name": "limit", "in": "query", "type": "integer", "description": "Max results"}
                    ],
                    "responses": {"200": {"description": "OK"}}
                },
                "post": {
                    "summary": "Create user",
                    "tags": ["users"],
                    "operationId": "createUser",
                    "parameters": [
                        {"name": "body", "in": "body", "schema": {
                            "properties": {"name": {"type": "string"}, "email": {"type": "string"}},
                            "required": ["name"]
                        }}
                    ],
                    "responses": {"201": {"description": "Created"}}
                }
            },
            "/users/{id}": {
                "get": {
                    "summary": "Get user by ID",
                    "tags": ["users"],
                    "operationId": "getUserById",
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "type": "string"}
                    ],
                    "responses": {"200": {"description": "OK"}}
                },
                "delete": {
                    "summary": "Delete user",
                    "tags": ["users"],
                    "operationId": "deleteUser",
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "type": "string"}
                    ],
                    "responses": {"204": {"description": "Deleted"}}
                }
            },
            "/items": {
                "get": {
                    "summary": "List items",
                    "tags": ["items"],
                    "operationId": "listItems",
                    "parameters": [],
                    "responses": {"200": {"description": "OK"}}
                }
            },
            "/items/{itemId}": {
                "get": {
                    "summary": "Get item",
                    "tags": ["items"],
                    "operationId": "getItem",
                    "parameters": [
                        {"name": "itemId", "in": "path", "required": True, "type": "string"}
                    ],
                    "responses": {"200": {"description": "OK"}}
                }
            }
        }
    })

    SAMPLE_OPENAPI3 = json.dumps({
        "openapi": "3.0.0",
        "info": {"title": "Widget Service", "version": "2.0"},
        "servers": [{"url": "https://widgets.example.com/api/v2"}],
        "components": {
            "securitySchemes": {
                "bearerAuth": {"type": "http", "scheme": "bearer"}
            }
        },
        "paths": {
            "/widgets": {
                "get": {
                    "summary": "List widgets",
                    "tags": ["widgets"],
                    "parameters": [
                        {"name": "page", "in": "query", "schema": {"type": "integer"}}
                    ],
                    "responses": {"200": {"description": "OK"}}
                },
                "post": {
                    "summary": "Create widget",
                    "tags": ["widgets"],
                    "requestBody": {
                        "content": {"application/json": {"schema": {
                            "properties": {"name": {"type": "string"}, "color": {"type": "string"}},
                            "required": ["name"]
                        }}}
                    },
                    "responses": {"201": {"description": "Created"}}
                }
            },
            "/widgets/{widgetId}": {
                "get": {
                    "summary": "Get widget",
                    "tags": ["widgets"],
                    "parameters": [
                        {"name": "widgetId", "in": "path", "required": True}
                    ],
                    "responses": {"200": {"description": "OK"}}
                }
            }
        }
    })

    def _run_fetch(self, input_file):
        """Run fetch_docs.py with a local file and return parsed JSON."""
        result = subprocess.run(
            [sys.executable, SCRIPT, input_file],
            capture_output=True, text=True, timeout=10
        )
        self.assertEqual(result.returncode, 0, f"fetch_docs.py failed: {result.stderr}")
        return json.loads(result.stdout)

    def test_swagger2_parse(self):
        """Test Swagger 2.0 JSON parsing."""
        tmp = "/tmp/test_swagger2.json"
        with open(tmp, "w") as f:
            f.write(self.SAMPLE_SWAGGER2)

        result = self._run_fetch(tmp)

        self.assertEqual(result["source_format"], "swagger2")
        self.assertEqual(result["service_name"], "test-api")
        self.assertEqual(result["base_url"], "https://api.example.com/v1")
        self.assertIn(result["auth_type"], ("api_key", "bearer"))
        self.assertGreaterEqual(len(result["endpoints"]), 5)

        # Check required fields on each endpoint
        for ep in result["endpoints"]:
            self.assertIn("method", ep)
            self.assertIn("path", ep)
            self.assertIn("tags", ep)
            self.assertIn("parameters", ep)

    def test_openapi3_parse(self):
        """Test OpenAPI 3.x JSON parsing."""
        tmp = "/tmp/test_openapi3.json"
        with open(tmp, "w") as f:
            f.write(self.SAMPLE_OPENAPI3)

        result = self._run_fetch(tmp)

        self.assertEqual(result["source_format"], "openapi3")
        self.assertEqual(result["service_name"], "widget-service")
        self.assertEqual(result["base_url"], "https://widgets.example.com/api/v2")
        self.assertEqual(result["auth_type"], "bearer")
        self.assertEqual(len(result["endpoints"]), 3)

    def test_required_fields(self):
        """Test that output JSON has all required fields."""
        tmp = "/tmp/test_swagger2.json"
        with open(tmp, "w") as f:
            f.write(self.SAMPLE_SWAGGER2)

        result = self._run_fetch(tmp)

        required = ["service_name", "base_url", "auth_type", "auth_header_format",
                     "env_vars_needed", "endpoints", "source_format"]
        for field in required:
            self.assertIn(field, result, f"Missing required field: {field}")

    def test_env_vars_format(self):
        """Test that env_vars_needed follow SERVICE_URL/SERVICE_TOKEN pattern."""
        tmp = "/tmp/test_swagger2.json"
        with open(tmp, "w") as f:
            f.write(self.SAMPLE_SWAGGER2)

        result = self._run_fetch(tmp)
        env_vars = result["env_vars_needed"]

        self.assertEqual(len(env_vars), 2)
        self.assertTrue(env_vars[0].endswith("_URL"))
        self.assertTrue(env_vars[1].endswith("_TOKEN"))

    def test_endpoint_ranking_limit(self):
        """Test that >100 endpoints get ranked and limited to ~30."""
        # Build a spec with 120 endpoints
        paths = {}
        for i in range(120):
            method = ["get", "post", "put", "delete"][i % 4]
            paths[f"/resource{i}"] = {
                method: {
                    "summary": f"Endpoint {i}",
                    "tags": [f"group{i % 5}"],
                    "operationId": f"op{i}",
                    "responses": {"200": {"description": "OK"}}
                }
            }
        big_spec = json.dumps({
            "swagger": "2.0",
            "info": {"title": "Big API", "version": "1.0"},
            "host": "api.example.com",
            "basePath": "/",
            "paths": paths
        })

        tmp = "/tmp/test_big_api.json"
        with open(tmp, "w") as f:
            f.write(big_spec)

        result = self._run_fetch(tmp)
        self.assertLessEqual(len(result["endpoints"]), 30)

    def test_postman_collection(self):
        """Test Postman Collection v2 parsing."""
        postman = json.dumps({
            "info": {
                "name": "My API Collection",
                "_postman_id": "abc123",
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            },
            "item": [
                {
                    "name": "Users",
                    "item": [
                        {
                            "name": "List users",
                            "request": {
                                "method": "GET",
                                "url": {
                                    "raw": "https://api.example.com/users",
                                    "host": ["api", "example", "com"],
                                    "path": ["users"],
                                    "query": [{"key": "limit", "value": "10"}]
                                }
                            }
                        },
                        {
                            "name": "Get user",
                            "request": {
                                "method": "GET",
                                "url": {
                                    "raw": "https://api.example.com/users/:userId",
                                    "host": ["api", "example", "com"],
                                    "path": ["users", ":userId"],
                                    "variable": [{"key": "userId", "description": "User ID"}]
                                }
                            }
                        }
                    ]
                }
            ]
        })

        tmp = "/tmp/test_postman.json"
        with open(tmp, "w") as f:
            f.write(postman)

        result = self._run_fetch(tmp)
        self.assertEqual(result["source_format"], "postman")
        self.assertEqual(len(result["endpoints"]), 2)
        self.assertEqual(result["service_name"], "my-api-collection")

    def test_invalid_input_exits(self):
        """Test that invalid input produces non-zero exit code."""
        result = subprocess.run(
            [sys.executable, SCRIPT, "/nonexistent/path.json"],
            capture_output=True, text=True, timeout=10
        )
        self.assertNotEqual(result.returncode, 0)

    def test_no_args_exits(self):
        """Test that no arguments produce usage message."""
        result = subprocess.run(
            [sys.executable, SCRIPT],
            capture_output=True, text=True, timeout=10
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Usage", result.stderr)


class TestFetchDocsLive(unittest.TestCase):
    """Integration tests that require network access. Skipped in CI."""

    @unittest.skipUnless(os.environ.get("RUN_LIVE_TESTS"), "Set RUN_LIVE_TESTS=1 to run")
    def test_petstore_swagger(self):
        """Fetch the real Petstore Swagger 2.0 spec."""
        result = subprocess.run(
            [sys.executable, SCRIPT, "https://petstore.swagger.io/v2/swagger.json"],
            capture_output=True, text=True, timeout=30
        )
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertEqual(data["source_format"], "swagger2")
        self.assertGreaterEqual(len(data["endpoints"]), 5)


if __name__ == "__main__":
    unittest.main()
