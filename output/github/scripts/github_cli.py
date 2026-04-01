#!/usr/bin/env python3
"""
github CLI tool for Claude Code skill integration.
Provides access to the github-v3-rest-api API.
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
BASE_URL = _env.get("GITHUB_URL", "https://api.github.com")
AUTH_TOKEN = _env.get("GITHUB_TOKEN", "")

_ssl_ctx = ssl.create_default_context()
if _env.get("GITHUB_VERIFY_SSL", "true").lower() == "false":
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = ssl.CERT_NONE


def get_auth_header() -> dict:
    """Build authorization header."""
    if AUTH_TOKEN:
        return {"Authorization": f"Bearer {AUTH_TOKEN}"}
    return {}


def make_request(path: str, method: str = "GET", data: bytes = None, params: dict = None) -> tuple:
    """Make HTTP request to the github API."""
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
    """Verify connectivity to the github API."""
    if not BASE_URL:
        print(f"Error: GITHUB_URL not set", file=sys.stderr)
        sys.exit(1)
    status, body = make_request("/")
    if status == 0:
        print(f"Cannot connect to {BASE_URL}", file=sys.stderr)
        print(f"Error: {body}", file=sys.stderr)
        sys.exit(1)
    print(f"Connected to {BASE_URL} (HTTP {status})")


def cmd_activity_get(args):
    """Get feeds"""
    path = "/feeds"
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


def cmd_activity_list(args):
    """List public events"""
    path = "/events"
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


def cmd_activity_list_2(args):
    """List repositories starred by the authenticated user"""
    path = "/user/starred"
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


def cmd_activity_list_3(args):
    """List notifications for the authenticated user"""
    path = "/notifications"
    params = {}
    if args.per_page is not None:
        params["per_page"] = args.per_page
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


def cmd_apps_get(args):
    """Get the authenticated app"""
    path = "/app"
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


def cmd_emojis_get(args):
    """Get emojis"""
    path = "/emojis"
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


def cmd_gists_list(args):
    """List gists for the authenticated user"""
    path = "/gists"
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


def cmd_gists_list_2(args):
    """List public gists"""
    path = "/gists/public"
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


def cmd_gists_list_3(args):
    """List starred gists"""
    path = "/gists/starred"
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


def cmd_issues_list(args):
    """List issues assigned to the authenticated user"""
    path = "/issues"
    params = {}
    if args.filter is not None:
        params["filter"] = args.filter
    if args.state is not None:
        params["state"] = args.state
    if args.sort is not None:
        params["sort"] = args.sort
    if args.collab is not None:
        params["collab"] = args.collab
    if args.orgs is not None:
        params["orgs"] = args.orgs
    if args.owned is not None:
        params["owned"] = args.owned
    if args.pulls is not None:
        params["pulls"] = args.pulls
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


def cmd_issues_list_2(args):
    """List user account issues assigned to the authenticated user"""
    path = "/user/issues"
    params = {}
    if args.filter is not None:
        params["filter"] = args.filter
    if args.state is not None:
        params["state"] = args.state
    if args.sort is not None:
        params["sort"] = args.sort
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


def cmd_licenses_get(args):
    """Get all commonly used licenses"""
    path = "/licenses"
    params = {}
    if args.featured is not None:
        params["featured"] = args.featured
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


def cmd_meta_root(args):
    """GitHub API Root"""
    path = "/"
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


def cmd_meta_get(args):
    """Get the Zen of GitHub"""
    path = "/zen"
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


def cmd_meta_get_2(args):
    """Get GitHub meta information"""
    path = "/meta"
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


def cmd_meta_get_3(args):
    """Get Octocat"""
    path = "/octocat"
    params = {}
    if args.s is not None:
        params["s"] = args.s
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


def cmd_meta_get_4(args):
    """Get all API versions"""
    path = "/versions"
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


def cmd_orgs_list(args):
    """List organizations for the authenticated user"""
    path = "/user/orgs"
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


def cmd_orgs_get(args):
    """Get an organization"""
    path = "/orgs/{org}".replace("{org}", str(args.org))
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


def cmd_rate_limit_get(args):
    """Get rate limit status for the authenticated user"""
    path = "/rate_limit"
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


def cmd_repos_list(args):
    """List repositories for the authenticated user"""
    path = "/user/repos"
    params = {}
    if args.visibility is not None:
        params["visibility"] = args.visibility
    if args.affiliation is not None:
        params["affiliation"] = args.affiliation
    if args.type is not None:
        params["type"] = args.type
    if args.sort is not None:
        params["sort"] = args.sort
    if args.direction is not None:
        params["direction"] = args.direction
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


def cmd_repos_list_2(args):
    """List public repositories"""
    path = "/repositories"
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


def cmd_search_code(args):
    """Search code"""
    path = "/search/code"
    params = {}
    if args.q is not None:
        params["q"] = args.q
    if args.sort is not None:
        params["sort"] = args.sort
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


def cmd_search_users(args):
    """Search users"""
    path = "/search/users"
    params = {}
    if args.q is not None:
        params["q"] = args.q
    if args.sort is not None:
        params["sort"] = args.sort
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


def cmd_teams_list(args):
    """List teams for the authenticated user"""
    path = "/user/teams"
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


def cmd_users_get(args):
    """Get the authenticated user"""
    path = "/user"
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


def cmd_users_list(args):
    """List users"""
    path = "/users"
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


def cmd_users_list_2(args):
    """List public SSH keys for the authenticated user"""
    path = "/user/keys"
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


def cmd_users_list_3(args):
    """List users blocked by the authenticated user"""
    path = "/user/blocks"
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


def cmd_users_list_4(args):
    """List email addresses for the authenticated user"""
    path = "/user/emails"
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
    parser = argparse.ArgumentParser(description="github CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- check ---
    subparsers.add_parser("check", help="Test API connectivity")

    # --- activity ---
    parser_activity = subparsers.add_parser("activity", help="Activity operations")
    sub_activity = parser_activity.add_subparsers(dest="activity_action", help="activity actions")

    p_activity_get = sub_activity.add_parser("get", help="Get feeds")
    p_activity_get.set_defaults(func=cmd_activity_get)

    p_activity_list = sub_activity.add_parser("list", help="List public events")
    p_activity_list.set_defaults(func=cmd_activity_list)

    p_activity_list_2 = sub_activity.add_parser("list-2", help="List repositories starred by the authenticated user")
    p_activity_list_2.set_defaults(func=cmd_activity_list_2)

    p_activity_list_3 = sub_activity.add_parser("list-3", help="List notifications for the authenticated user")
    p_activity_list_3.add_argument("--per-page", dest="per_page", default=None, help="The number of results per page (max 50).")
    p_activity_list_3.set_defaults(func=cmd_activity_list_3)

    # --- apps ---
    parser_apps = subparsers.add_parser("apps", help="Apps operations")
    sub_apps = parser_apps.add_subparsers(dest="apps_action", help="apps actions")

    p_apps_get = sub_apps.add_parser("get", help="Get the authenticated app")
    p_apps_get.set_defaults(func=cmd_apps_get)

    # --- emojis ---
    parser_emojis = subparsers.add_parser("emojis", help="Emojis operations")
    sub_emojis = parser_emojis.add_subparsers(dest="emojis_action", help="emojis actions")

    p_emojis_get = sub_emojis.add_parser("get", help="Get emojis")
    p_emojis_get.set_defaults(func=cmd_emojis_get)

    # --- gists ---
    parser_gists = subparsers.add_parser("gists", help="Gists operations")
    sub_gists = parser_gists.add_subparsers(dest="gists_action", help="gists actions")

    p_gists_list = sub_gists.add_parser("list", help="List gists for the authenticated user")
    p_gists_list.set_defaults(func=cmd_gists_list)

    p_gists_list_2 = sub_gists.add_parser("list-2", help="List public gists")
    p_gists_list_2.set_defaults(func=cmd_gists_list_2)

    p_gists_list_3 = sub_gists.add_parser("list-3", help="List starred gists")
    p_gists_list_3.set_defaults(func=cmd_gists_list_3)

    # --- issues ---
    parser_issues = subparsers.add_parser("issues", help="Issues operations")
    sub_issues = parser_issues.add_subparsers(dest="issues_action", help="issues actions")

    p_issues_list = sub_issues.add_parser("list", help="List issues assigned to the authenticated user")
    p_issues_list.add_argument("--filter", dest="filter", default=None, help="Indicates which sorts of issues to return. `assigned` means issues assigned to you. `created` means issues created by you. `mentioned` means issues mentioning you. `subscribed` means issues you're subscribed to updates for. `all` or `repos` means all issues you can see, regardless of participation or creation.")
    p_issues_list.add_argument("--state", dest="state", default=None, help="Indicates the state of the issues to return.")
    p_issues_list.add_argument("--sort", dest="sort", default=None, help="What to sort results by.")
    p_issues_list.add_argument("--collab", dest="collab", default=None, help="")
    p_issues_list.add_argument("--orgs", dest="orgs", default=None, help="")
    p_issues_list.add_argument("--owned", dest="owned", default=None, help="")
    p_issues_list.add_argument("--pulls", dest="pulls", default=None, help="")
    p_issues_list.set_defaults(func=cmd_issues_list)

    p_issues_list_2 = sub_issues.add_parser("list-2", help="List user account issues assigned to the authenticated user")
    p_issues_list_2.add_argument("--filter", dest="filter", default=None, help="Indicates which sorts of issues to return. `assigned` means issues assigned to you. `created` means issues created by you. `mentioned` means issues mentioning you. `subscribed` means issues you're subscribed to updates for. `all` or `repos` means all issues you can see, regardless of participation or creation.")
    p_issues_list_2.add_argument("--state", dest="state", default=None, help="Indicates the state of the issues to return.")
    p_issues_list_2.add_argument("--sort", dest="sort", default=None, help="What to sort results by.")
    p_issues_list_2.set_defaults(func=cmd_issues_list_2)

    # --- licenses ---
    parser_licenses = subparsers.add_parser("licenses", help="Licenses operations")
    sub_licenses = parser_licenses.add_subparsers(dest="licenses_action", help="licenses actions")

    p_licenses_get = sub_licenses.add_parser("get", help="Get all commonly used licenses")
    p_licenses_get.add_argument("--featured", dest="featured", default=None, help="")
    p_licenses_get.set_defaults(func=cmd_licenses_get)

    # --- meta ---
    parser_meta = subparsers.add_parser("meta", help="Meta operations")
    sub_meta = parser_meta.add_subparsers(dest="meta_action", help="meta actions")

    p_meta_root = sub_meta.add_parser("root", help="GitHub API Root")
    p_meta_root.set_defaults(func=cmd_meta_root)

    p_meta_get = sub_meta.add_parser("get", help="Get the Zen of GitHub")
    p_meta_get.set_defaults(func=cmd_meta_get)

    p_meta_get_2 = sub_meta.add_parser("get-2", help="Get GitHub meta information")
    p_meta_get_2.set_defaults(func=cmd_meta_get_2)

    p_meta_get_3 = sub_meta.add_parser("get-3", help="Get Octocat")
    p_meta_get_3.add_argument("--s", dest="s", default=None, help="The words to show in Octocat's speech bubble")
    p_meta_get_3.set_defaults(func=cmd_meta_get_3)

    p_meta_get_4 = sub_meta.add_parser("get-4", help="Get all API versions")
    p_meta_get_4.set_defaults(func=cmd_meta_get_4)

    # --- orgs ---
    parser_orgs = subparsers.add_parser("orgs", help="Orgs operations")
    sub_orgs = parser_orgs.add_subparsers(dest="orgs_action", help="orgs actions")

    p_orgs_list = sub_orgs.add_parser("list", help="List organizations for the authenticated user")
    p_orgs_list.set_defaults(func=cmd_orgs_list)

    p_orgs_get = sub_orgs.add_parser("get", help="Get an organization")
    p_orgs_get.add_argument("org", help="org")
    p_orgs_get.set_defaults(func=cmd_orgs_get)

    # --- rate-limit ---
    parser_rate_limit = subparsers.add_parser("rate-limit", help="Rate-Limit operations")
    sub_rate_limit = parser_rate_limit.add_subparsers(dest="rate_limit_action", help="rate-limit actions")

    p_rate_limit_get = sub_rate_limit.add_parser("get", help="Get rate limit status for the authenticated user")
    p_rate_limit_get.set_defaults(func=cmd_rate_limit_get)

    # --- repos ---
    parser_repos = subparsers.add_parser("repos", help="Repos operations")
    sub_repos = parser_repos.add_subparsers(dest="repos_action", help="repos actions")

    p_repos_list = sub_repos.add_parser("list", help="List repositories for the authenticated user")
    p_repos_list.add_argument("--visibility", dest="visibility", default=None, help="Limit results to repositories with the specified visibility.")
    p_repos_list.add_argument("--affiliation", dest="affiliation", default=None, help="Comma-separated list of values. Can include:    * `owner`: Repositories that are owned by the authenticated user.    * `collaborator`: Repositories that the user has been added to as a collaborator.    * `organization_member`: Repositories that the user has access to through being a member of an organization. This includes every repository on every team that the user is on.")
    p_repos_list.add_argument("--type", dest="type", default=None, help="Limit results to repositories of the specified type. Will cause a `422` error if used in the same request as **visibility** or **affiliation**.")
    p_repos_list.add_argument("--sort", dest="sort", default=None, help="The property to sort the results by.")
    p_repos_list.add_argument("--direction", dest="direction", default=None, help="The order to sort by. Default: `asc` when using `full_name`, otherwise `desc`.")
    p_repos_list.set_defaults(func=cmd_repos_list)

    p_repos_list_2 = sub_repos.add_parser("list-2", help="List public repositories")
    p_repos_list_2.set_defaults(func=cmd_repos_list_2)

    # --- search ---
    parser_search = subparsers.add_parser("search", help="Search operations")
    sub_search = parser_search.add_subparsers(dest="search_action", help="search actions")

    p_search_code = sub_search.add_parser("code", help="Search code")
    p_search_code.add_argument("--q", dest="q", default=None, help="The query contains one or more search keywords and qualifiers. Qualifiers allow you to limit your search to specific areas of GitHub. The REST API supports the same qualifiers as the web interface for GitHub. To learn more about the format of the query, see [Constructing a search query](https://docs.github.com/rest/reference/search#constructing-a-search-query). See \"[Searching code](https://docs.github.com/search-github/searching-on-github/searching-code)\" for a detailed list of qualifiers.")
    p_search_code.add_argument("--sort", dest="sort", default=None, help="Sorts the results of your query. Can only be `indexed`, which indicates how recently a file has been indexed by the GitHub search infrastructure. Default: [best match](https://docs.github.com/rest/reference/search#ranking-search-results)")
    p_search_code.set_defaults(func=cmd_search_code)

    p_search_users = sub_search.add_parser("users", help="Search users")
    p_search_users.add_argument("--q", dest="q", default=None, help="The query contains one or more search keywords and qualifiers. Qualifiers allow you to limit your search to specific areas of GitHub. The REST API supports the same qualifiers as the web interface for GitHub. To learn more about the format of the query, see [Constructing a search query](https://docs.github.com/rest/reference/search#constructing-a-search-query). See \"[Searching users](https://docs.github.com/search-github/searching-on-github/searching-users)\" for a detailed list of qualifiers.")
    p_search_users.add_argument("--sort", dest="sort", default=None, help="Sorts the results of your query by number of `followers` or `repositories`, or when the person `joined` GitHub. Default: [best match](https://docs.github.com/rest/reference/search#ranking-search-results)")
    p_search_users.set_defaults(func=cmd_search_users)

    # --- teams ---
    parser_teams = subparsers.add_parser("teams", help="Teams operations")
    sub_teams = parser_teams.add_subparsers(dest="teams_action", help="teams actions")

    p_teams_list = sub_teams.add_parser("list", help="List teams for the authenticated user")
    p_teams_list.set_defaults(func=cmd_teams_list)

    # --- users ---
    parser_users = subparsers.add_parser("users", help="Users operations")
    sub_users = parser_users.add_subparsers(dest="users_action", help="users actions")

    p_users_get = sub_users.add_parser("get", help="Get the authenticated user")
    p_users_get.set_defaults(func=cmd_users_get)

    p_users_list = sub_users.add_parser("list", help="List users")
    p_users_list.set_defaults(func=cmd_users_list)

    p_users_list_2 = sub_users.add_parser("list-2", help="List public SSH keys for the authenticated user")
    p_users_list_2.set_defaults(func=cmd_users_list_2)

    p_users_list_3 = sub_users.add_parser("list-3", help="List users blocked by the authenticated user")
    p_users_list_3.set_defaults(func=cmd_users_list_3)

    p_users_list_4 = sub_users.add_parser("list-4", help="List email addresses for the authenticated user")
    p_users_list_4.set_defaults(func=cmd_users_list_4)

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
