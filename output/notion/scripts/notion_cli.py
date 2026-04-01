#!/usr/bin/env python3
"""
notion CLI tool for Claude Code skill integration.
Provides access to the notion-api API.
"""

import argparse
import base64
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request


_env = os.environ.copy()

# --- Configuration ---
BASE_URL = _env.get("NOTION_URL", "https://api.notion.com")
AUTH_TOKEN = _env.get("NOTION_TOKEN", "")

_ssl_ctx = ssl.create_default_context()
if _env.get("NOTION_VERIFY_SSL", "true").lower() == "false":
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = ssl.CERT_NONE


def get_auth_header() -> dict:
    """Build authorization header."""
    if AUTH_TOKEN:
        return {"Authorization": f"Bearer {AUTH_TOKEN}"}
    return {}


def make_request(path: str, method: str = "GET", data: bytes = None, params: dict = None) -> tuple:
    """Make HTTP request to the notion API."""
    base = BASE_URL.rstrip("/")
    url = f"{base}/{path.lstrip('/')}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"

    headers = get_auth_header()
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30, context=_ssl_ctx) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as e:
        return 0, f"Connection error: {e.reason}"
    except Exception as e:
        return 0, f"Error: {e}"


def cmd_check(args):
    """Verify connectivity to the notion API."""
    if not BASE_URL:
        print(f"Error: NOTION_URL not set", file=sys.stderr)
        sys.exit(1)
    status, body = make_request("/")
    if status == 0:
        print(f"Cannot connect to {BASE_URL}", file=sys.stderr)
        print(f"Error: {body}", file=sys.stderr)
        sys.exit(1)
    print(f"Connected to {BASE_URL} (HTTP {status})")


def cmd_blocks_delete(args):
    """Delete a block"""
    path = "/v1/blocks/{id}".replace("{id}", str(args.id))
    data = None
    status, body = make_request(path, "DELETE", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_blocks_retrieveablock(args):
    """Retrieve a block"""
    path = "/v1/blocks/{id}".replace("{id}", str(args.id))
    data = None
    status, body = make_request(path, "GET", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_blocks_update(args):
    """Update a block"""
    path = "/v1/blocks/{id}".replace("{id}", str(args.id))
    body = {}
    if args.paragraph is not None:
        body["paragraph"] = args.paragraph
    data = json.dumps(body).encode("utf-8") if body else None
    status, body = make_request(path, "PATCH", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_blocks_retrieveblockchildren(args):
    """Retrieve block children"""
    path = "/v1/blocks/{id}/children".replace("{id}", str(args.id))
    params = {}
    if args.page_size is not None:
        params["page_size"] = args.page_size
    data = None
    status, body = make_request(path, "GET", data=data, params=params)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_blocks_appendblockchildren(args):
    """Append block children"""
    path = "/v1/blocks/{id}/children".replace("{id}", str(args.id))
    body = {}
    if args.children is not None:
        body["children"] = args.children
    data = json.dumps(body).encode("utf-8") if body else None
    status, body = make_request(path, "PATCH", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_comments_retrievecomments(args):
    """Retrieve comments"""
    path = "/v1/comments"
    params = {}
    if args.block_id is not None:
        params["block_id"] = args.block_id
    if args.page_size is not None:
        params["page_size"] = args.page_size
    data = None
    status, body = make_request(path, "GET", data=data, params=params)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_databases_retrieveadatabase(args):
    """Retrieve a database"""
    path = "/v1/databases/{id}".replace("{id}", str(args.id))
    data = None
    status, body = make_request(path, "GET", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_databases_update(args):
    """Update a database"""
    path = "/v1/databases/{id}".replace("{id}", str(args.id))
    body = {}
    if args.properties is not None:
        body["properties"] = args.properties
    if args.title is not None:
        body["title"] = args.title
    data = json.dumps(body).encode("utf-8") if body else None
    status, body = make_request(path, "PATCH", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_databases_queryadatabase(args):
    """Query a database"""
    path = "/v1/databases/{id}/query".replace("{id}", str(args.id))
    body = {}
    if args.filter is not None:
        body["filter"] = args.filter
    data = json.dumps(body).encode("utf-8") if body else None
    status, body = make_request(path, "POST", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_pages_retrieveapage(args):
    """Retrieve a Page"""
    path = "/v1/pages/{id}".replace("{id}", str(args.id))
    data = None
    status, body = make_request(path, "GET", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_pages_update(args):
    """Update Page properties """
    path = "/v1/pages/{id}".replace("{id}", str(args.id))
    body = {}
    if args.properties is not None:
        body["properties"] = args.properties
    data = json.dumps(body).encode("utf-8") if body else None
    status, body = make_request(path, "PATCH", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_pages_retrieveapagepropertyitem(args):
    """Retrieve a Page Property Item"""
    path = "/v1/pages/{page_id}/properties/{property_id}".replace("{page_id}", str(args.page_id))
    path = "{already_substituted}".replace("{property_id}", str(args.property_id))
    data = None
    status, body = make_request(path, "GET", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_users_retrieveauser(args):
    """Retrieve a user"""
    path = "/v1/users/{id}".replace("{id}", str(args.id))
    data = None
    status, body = make_request(path, "GET", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def main():
    parser = argparse.ArgumentParser(description="notion CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- check ---
    subparsers.add_parser("check", help="Test API connectivity")

    # --- blocks ---
    parser_blocks = subparsers.add_parser("blocks", help="Blocks operations")
    sub_blocks = parser_blocks.add_subparsers(dest="blocks_action", help="blocks actions")

    p_blocks_delete = sub_blocks.add_parser("delete", help="Delete a block")
    p_blocks_delete.add_argument("id", help="id")
    p_blocks_delete.set_defaults(func=cmd_blocks_delete)

    p_blocks_retrieveablock = sub_blocks.add_parser("retrieveablock", help="Retrieve a block")
    p_blocks_retrieveablock.add_argument("id", help="id")
    p_blocks_retrieveablock.set_defaults(func=cmd_blocks_retrieveablock)

    p_blocks_update = sub_blocks.add_parser("update", help="Update a block")
    p_blocks_update.add_argument("id", help="id")
    p_blocks_update.add_argument("--paragraph", dest="paragraph", default=None, help="paragraph")
    p_blocks_update.set_defaults(func=cmd_blocks_update)

    p_blocks_retrieveblockchildren = sub_blocks.add_parser("retrieveblockchildren", help="Retrieve block children")
    p_blocks_retrieveblockchildren.add_argument("id", help="id")
    p_blocks_retrieveblockchildren.add_argument("--page-size", dest="page_size", default=None, help="")
    p_blocks_retrieveblockchildren.set_defaults(func=cmd_blocks_retrieveblockchildren)

    p_blocks_appendblockchildren = sub_blocks.add_parser("appendblockchildren", help="Append block children")
    p_blocks_appendblockchildren.add_argument("id", help="id")
    p_blocks_appendblockchildren.add_argument("--children", dest="children", default=None, help="children")
    p_blocks_appendblockchildren.set_defaults(func=cmd_blocks_appendblockchildren)

    # --- comments ---
    parser_comments = subparsers.add_parser("comments", help="Comments operations")
    sub_comments = parser_comments.add_subparsers(dest="comments_action", help="comments actions")

    p_comments_retrievecomments = sub_comments.add_parser("retrievecomments", help="Retrieve comments")
    p_comments_retrievecomments.add_argument("--block-id", dest="block_id", default=None, help="")
    p_comments_retrievecomments.add_argument("--page-size", dest="page_size", default=None, help="")
    p_comments_retrievecomments.set_defaults(func=cmd_comments_retrievecomments)

    # --- databases ---
    parser_databases = subparsers.add_parser("databases", help="Databases operations")
    sub_databases = parser_databases.add_subparsers(dest="databases_action", help="databases actions")

    p_databases_retrieveadatabase = sub_databases.add_parser("retrieveadatabase", help="Retrieve a database")
    p_databases_retrieveadatabase.add_argument("id", help="id")
    p_databases_retrieveadatabase.set_defaults(func=cmd_databases_retrieveadatabase)

    p_databases_update = sub_databases.add_parser("update", help="Update a database")
    p_databases_update.add_argument("id", help="id")
    p_databases_update.add_argument("--properties", dest="properties", default=None, help="properties")
    p_databases_update.add_argument("--title", dest="title", default=None, help="title")
    p_databases_update.set_defaults(func=cmd_databases_update)

    p_databases_queryadatabase = sub_databases.add_parser("queryadatabase", help="Query a database")
    p_databases_queryadatabase.add_argument("id", help="id")
    p_databases_queryadatabase.add_argument("--filter", dest="filter", default=None, help="filter")
    p_databases_queryadatabase.set_defaults(func=cmd_databases_queryadatabase)

    # --- pages ---
    parser_pages = subparsers.add_parser("pages", help="Pages operations")
    sub_pages = parser_pages.add_subparsers(dest="pages_action", help="pages actions")

    p_pages_retrieveapage = sub_pages.add_parser("retrieveapage", help="Retrieve a Page")
    p_pages_retrieveapage.add_argument("id", help="id")
    p_pages_retrieveapage.set_defaults(func=cmd_pages_retrieveapage)

    p_pages_update = sub_pages.add_parser("update", help="Update Page properties ")
    p_pages_update.add_argument("id", help="id")
    p_pages_update.add_argument("--properties", dest="properties", default=None, help="properties")
    p_pages_update.set_defaults(func=cmd_pages_update)

    p_pages_retrieveapagepropertyitem = sub_pages.add_parser("retrieveapagepropertyitem", help="Retrieve a Page Property Item")
    p_pages_retrieveapagepropertyitem.add_argument("page_id", help="page_id")
    p_pages_retrieveapagepropertyitem.add_argument("property_id", help="property_id")
    p_pages_retrieveapagepropertyitem.set_defaults(func=cmd_pages_retrieveapagepropertyitem)

    # --- users ---
    parser_users = subparsers.add_parser("users", help="Users operations")
    sub_users = parser_users.add_subparsers(dest="users_action", help="users actions")

    p_users_retrieveauser = sub_users.add_parser("retrieveauser", help="Retrieve a user")
    p_users_retrieveauser.add_argument("id", help="id")
    p_users_retrieveauser.set_defaults(func=cmd_users_retrieveauser)

    args = parser.parse_args()

    if args.command == "check":
        cmd_check(args)
    elif hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
