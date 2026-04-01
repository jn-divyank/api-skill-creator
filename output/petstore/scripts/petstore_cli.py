#!/usr/bin/env python3
"""
petstore CLI tool for Claude Code skill integration.
Provides access to the swagger-petstore API.
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
BASE_URL = _env.get("PETSTORE_URL", "https://petstore.swagger.io/v2")
AUTH_TOKEN = _env.get("PETSTORE_TOKEN", "")

_ssl_ctx = ssl.create_default_context()
if _env.get("PETSTORE_VERIFY_SSL", "true").lower() == "false":
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = ssl.CERT_NONE


def get_auth_header() -> dict:
    """Build authorization header."""
    if AUTH_TOKEN:
        return {"api_key": AUTH_TOKEN}
    return {}


def make_request(path: str, method: str = "GET", data: bytes = None, params: dict = None) -> tuple:
    """Make HTTP request to the petstore API."""
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
    """Verify connectivity to the petstore API."""
    if not BASE_URL:
        print(f"Error: PETSTORE_URL not set", file=sys.stderr)
        sys.exit(1)
    status, body = make_request("/")
    if status == 0:
        print(f"Cannot connect to {BASE_URL}", file=sys.stderr)
        print(f"Error: {body}", file=sys.stderr)
        sys.exit(1)
    print(f"Connected to {BASE_URL} (HTTP {status})")


def cmd_pet_upload(args):
    """uploads an image"""
    path = "/pet/{petId}/uploadImage".replace("{petId}", str(args.petId))
    data = None
    if hasattr(args, "data") and args.data:
        data = args.data.encode("utf-8")
    status, body = make_request(path, "POST", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_pet_add(args):
    """Add a new pet to the store"""
    path = "/pet"
    data = None
    if hasattr(args, "data") and args.data:
        data = args.data.encode("utf-8")
    status, body = make_request(path, "POST", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_pet_update(args):
    """Update an existing pet"""
    path = "/pet"
    data = None
    if hasattr(args, "data") and args.data:
        data = args.data.encode("utf-8")
    status, body = make_request(path, "PUT", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_pet_list(args):
    """Finds Pets by status"""
    path = "/pet/findByStatus"
    params = {}
    if args.status is not None:
        params["status"] = args.status
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


def cmd_pet_list_2(args):
    """Finds Pets by tags"""
    path = "/pet/findByTags"
    params = {}
    if args.tags is not None:
        params["tags"] = args.tags
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


def cmd_pet_get(args):
    """Find pet by ID"""
    path = "/pet/{petId}".replace("{petId}", str(args.petId))
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


def cmd_pet_update_2(args):
    """Updates a pet in the store with form data"""
    path = "/pet/{petId}".replace("{petId}", str(args.petId))
    data = None
    if hasattr(args, "data") and args.data:
        data = args.data.encode("utf-8")
    status, body = make_request(path, "POST", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_pet_delete(args):
    """Deletes a pet"""
    path = "/pet/{petId}".replace("{petId}", str(args.petId))
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


def cmd_store_get(args):
    """Returns pet inventories by status"""
    path = "/store/inventory"
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


def cmd_store_placeorder(args):
    """Place an order for a pet"""
    path = "/store/order"
    data = None
    if hasattr(args, "data") and args.data:
        data = args.data.encode("utf-8")
    status, body = make_request(path, "POST", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_store_get_2(args):
    """Find purchase order by ID"""
    path = "/store/order/{orderId}".replace("{orderId}", str(args.orderId))
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


def cmd_store_delete(args):
    """Delete purchase order by ID"""
    path = "/store/order/{orderId}".replace("{orderId}", str(args.orderId))
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


def cmd_user_create(args):
    """Creates list of users with given input array"""
    path = "/user/createWithList"
    data = None
    if hasattr(args, "data") and args.data:
        data = args.data.encode("utf-8")
    status, body = make_request(path, "POST", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_user_get(args):
    """Get user by user name"""
    path = "/user/{username}".replace("{username}", str(args.username))
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


def cmd_user_update(args):
    """Updated user"""
    path = "/user/{username}".replace("{username}", str(args.username))
    data = None
    if hasattr(args, "data") and args.data:
        data = args.data.encode("utf-8")
    status, body = make_request(path, "PUT", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_user_delete(args):
    """Delete user"""
    path = "/user/{username}".replace("{username}", str(args.username))
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


def cmd_user_loginuser(args):
    """Logs user into the system"""
    path = "/user/login"
    params = {}
    if args.username is not None:
        params["username"] = args.username
    if args.password is not None:
        params["password"] = args.password
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


def cmd_user_logoutuser(args):
    """Logs out current logged in user session"""
    path = "/user/logout"
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


def cmd_user_create_2(args):
    """Creates list of users with given input array"""
    path = "/user/createWithArray"
    data = None
    if hasattr(args, "data") and args.data:
        data = args.data.encode("utf-8")
    status, body = make_request(path, "POST", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def cmd_user_create_3(args):
    """Create user"""
    path = "/user"
    data = None
    if hasattr(args, "data") and args.data:
        data = args.data.encode("utf-8")
    status, body = make_request(path, "POST", data=data, params=None)
    if status == 0 or status >= 400:
        print(f"Error (HTTP {status}): {body}", file=sys.stderr)
        sys.exit(1)
    try:
        result = json.loads(body)
        print(json.dumps(result, indent=2))
    except (json.JSONDecodeError, ValueError):
        print(body)


def main():
    parser = argparse.ArgumentParser(description="petstore CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- check ---
    subparsers.add_parser("check", help="Test API connectivity")

    # --- pet ---
    parser_pet = subparsers.add_parser("pet", help="Pet operations")
    sub_pet = parser_pet.add_subparsers(dest="pet_action", help="pet actions")

    p_pet_upload = sub_pet.add_parser("upload", help="uploads an image")
    p_pet_upload.add_argument("petId", help="petId")
    p_pet_upload.add_argument("--data", default=None, help="JSON request body")
    p_pet_upload.set_defaults(func=cmd_pet_upload)

    p_pet_add = sub_pet.add_parser("add", help="Add a new pet to the store")
    p_pet_add.add_argument("--data", default=None, help="JSON request body")
    p_pet_add.set_defaults(func=cmd_pet_add)

    p_pet_update = sub_pet.add_parser("update", help="Update an existing pet")
    p_pet_update.add_argument("--data", default=None, help="JSON request body")
    p_pet_update.set_defaults(func=cmd_pet_update)

    p_pet_list = sub_pet.add_parser("list", help="Finds Pets by status")
    p_pet_list.add_argument("--status", dest="status", default=None, help="Status values that need to be considered for filter")
    p_pet_list.set_defaults(func=cmd_pet_list)

    p_pet_list_2 = sub_pet.add_parser("list-2", help="Finds Pets by tags")
    p_pet_list_2.add_argument("--tags", dest="tags", default=None, help="Tags to filter by")
    p_pet_list_2.set_defaults(func=cmd_pet_list_2)

    p_pet_get = sub_pet.add_parser("get", help="Find pet by ID")
    p_pet_get.add_argument("petId", help="petId")
    p_pet_get.set_defaults(func=cmd_pet_get)

    p_pet_update_2 = sub_pet.add_parser("update-2", help="Updates a pet in the store with form data")
    p_pet_update_2.add_argument("petId", help="petId")
    p_pet_update_2.add_argument("--data", default=None, help="JSON request body")
    p_pet_update_2.set_defaults(func=cmd_pet_update_2)

    p_pet_delete = sub_pet.add_parser("delete", help="Deletes a pet")
    p_pet_delete.add_argument("petId", help="petId")
    p_pet_delete.set_defaults(func=cmd_pet_delete)

    # --- store ---
    parser_store = subparsers.add_parser("store", help="Store operations")
    sub_store = parser_store.add_subparsers(dest="store_action", help="store actions")

    p_store_get = sub_store.add_parser("get", help="Returns pet inventories by status")
    p_store_get.set_defaults(func=cmd_store_get)

    p_store_placeorder = sub_store.add_parser("placeorder", help="Place an order for a pet")
    p_store_placeorder.add_argument("--data", default=None, help="JSON request body")
    p_store_placeorder.set_defaults(func=cmd_store_placeorder)

    p_store_get_2 = sub_store.add_parser("get-2", help="Find purchase order by ID")
    p_store_get_2.add_argument("orderId", help="orderId")
    p_store_get_2.set_defaults(func=cmd_store_get_2)

    p_store_delete = sub_store.add_parser("delete", help="Delete purchase order by ID")
    p_store_delete.add_argument("orderId", help="orderId")
    p_store_delete.set_defaults(func=cmd_store_delete)

    # --- user ---
    parser_user = subparsers.add_parser("user", help="User operations")
    sub_user = parser_user.add_subparsers(dest="user_action", help="user actions")

    p_user_create = sub_user.add_parser("create", help="Creates list of users with given input array")
    p_user_create.add_argument("--data", default=None, help="JSON request body")
    p_user_create.set_defaults(func=cmd_user_create)

    p_user_get = sub_user.add_parser("get", help="Get user by user name")
    p_user_get.add_argument("username", help="username")
    p_user_get.set_defaults(func=cmd_user_get)

    p_user_update = sub_user.add_parser("update", help="Updated user")
    p_user_update.add_argument("username", help="username")
    p_user_update.add_argument("--data", default=None, help="JSON request body")
    p_user_update.set_defaults(func=cmd_user_update)

    p_user_delete = sub_user.add_parser("delete", help="Delete user")
    p_user_delete.add_argument("username", help="username")
    p_user_delete.set_defaults(func=cmd_user_delete)

    p_user_loginuser = sub_user.add_parser("loginuser", help="Logs user into the system")
    p_user_loginuser.add_argument("--username", dest="username", default=None, help="The user name for login")
    p_user_loginuser.add_argument("--password", dest="password", default=None, help="The password for login in clear text")
    p_user_loginuser.set_defaults(func=cmd_user_loginuser)

    p_user_logoutuser = sub_user.add_parser("logoutuser", help="Logs out current logged in user session")
    p_user_logoutuser.set_defaults(func=cmd_user_logoutuser)

    p_user_create_2 = sub_user.add_parser("create-2", help="Creates list of users with given input array")
    p_user_create_2.add_argument("--data", default=None, help="JSON request body")
    p_user_create_2.set_defaults(func=cmd_user_create_2)

    p_user_create_3 = sub_user.add_parser("create-3", help="Create user")
    p_user_create_3.add_argument("--data", default=None, help="JSON request body")
    p_user_create_3.set_defaults(func=cmd_user_create_3)

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
