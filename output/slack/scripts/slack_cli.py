#!/usr/bin/env python3
"""
slack CLI tool for Claude Code skill integration.
Provides access to the slack-web-api API.
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
BASE_URL = _env.get("SLACK_URL", "https://slack.com/api")
AUTH_TOKEN = _env.get("SLACK_TOKEN", "")

_ssl_ctx = ssl.create_default_context()
if _env.get("SLACK_VERIFY_SSL", "true").lower() == "false":
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = ssl.CERT_NONE


def get_auth_header() -> dict:
    """Build authorization header."""
    if AUTH_TOKEN:
        return {"Authorization": f"Bearer {AUTH_TOKEN}"}
    return {}


def make_request(path: str, method: str = "GET", data: bytes = None, params: dict = None) -> tuple:
    """Make HTTP request to the slack API."""
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
    """Verify connectivity to the slack API."""
    if not BASE_URL:
        print(f"Error: SLACK_URL not set", file=sys.stderr)
        sys.exit(1)
    status, body = make_request("/")
    if status == 0:
        print(f"Cannot connect to {BASE_URL}", file=sys.stderr)
        print(f"Error: {body}", file=sys.stderr)
        sys.exit(1)
    print(f"Connected to {BASE_URL} (HTTP {status})")


def cmd_api_api_test(args):
    """Checks API calling code."""
    path = "/api.test"
    params = {}
    if args.error is not None:
        params["error"] = args.error
    if args.foo is not None:
        params["foo"] = args.foo
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


def cmd_apps_apps_uninstall(args):
    """Uninstalls your app from a workspace."""
    path = "/apps.uninstall"
    params = {}
    if args.token is not None:
        params["token"] = args.token
    if args.client_id is not None:
        params["client_id"] = args.client_id
    if args.client_secret is not None:
        params["client_secret"] = args.client_secret
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


def cmd_auth_auth_test(args):
    """Checks authentication & identity."""
    path = "/auth.test"
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


def cmd_auth_auth_revoke(args):
    """Revokes a token."""
    path = "/auth.revoke"
    params = {}
    if args.token is not None:
        params["token"] = args.token
    if args.test is not None:
        params["test"] = args.test
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


def cmd_bots_bots_info(args):
    """Gets information about a bot user."""
    path = "/bots.info"
    params = {}
    if args.token is not None:
        params["token"] = args.token
    if args.bot is not None:
        params["bot"] = args.bot
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


def cmd_calls_calls_info(args):
    """Returns information about a Call."""
    path = "/calls.info"
    params = {}
    if args.id is not None:
        params["id"] = args.id
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


def cmd_dialog_dialog_open(args):
    """Open a dialog with a user"""
    path = "/dialog.open"
    params = {}
    if args.dialog is not None:
        params["dialog"] = args.dialog
    if args.trigger_id is not None:
        params["trigger_id"] = args.trigger_id
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


def cmd_dnd_dnd_info(args):
    """Retrieves a user's current Do Not Disturb status."""
    path = "/dnd.info"
    params = {}
    if args.token is not None:
        params["token"] = args.token
    if args.user is not None:
        params["user"] = args.user
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


def cmd_dnd_dnd_teaminfo(args):
    """Retrieves the Do Not Disturb status for up to 50 users on a team."""
    path = "/dnd.teamInfo"
    params = {}
    if args.token is not None:
        params["token"] = args.token
    if args.users is not None:
        params["users"] = args.users
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


def cmd_emoji_emoji_list(args):
    """Lists custom emoji for a team."""
    path = "/emoji.list"
    params = {}
    if args.token is not None:
        params["token"] = args.token
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


def cmd_files_files_info(args):
    """Gets information about a file."""
    path = "/files.info"
    params = {}
    if args.token is not None:
        params["token"] = args.token
    if args.file is not None:
        params["file"] = args.file
    if args.count is not None:
        params["count"] = args.count
    if args.page is not None:
        params["page"] = args.page
    if args.limit is not None:
        params["limit"] = args.limit
    if args.cursor is not None:
        params["cursor"] = args.cursor
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


def cmd_files_files_list(args):
    """List for a team, in a channel, or from a user with applied filters."""
    path = "/files.list"
    params = {}
    if args.token is not None:
        params["token"] = args.token
    if args.user is not None:
        params["user"] = args.user
    if args.channel is not None:
        params["channel"] = args.channel
    if args.ts_from is not None:
        params["ts_from"] = args.ts_from
    if args.ts_to is not None:
        params["ts_to"] = args.ts_to
    if args.types is not None:
        params["types"] = args.types
    if args.count is not None:
        params["count"] = args.count
    if args.page is not None:
        params["page"] = args.page
    if args.show_files_hidden_by_limit is not None:
        params["show_files_hidden_by_limit"] = args.show_files_hidden_by_limit
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


def cmd_oauth_oauth_token(args):
    """Exchanges a temporary OAuth verifier code for a workspace token."""
    path = "/oauth.token"
    params = {}
    if args.client_id is not None:
        params["client_id"] = args.client_id
    if args.client_secret is not None:
        params["client_secret"] = args.client_secret
    if args.code is not None:
        params["code"] = args.code
    if args.redirect_uri is not None:
        params["redirect_uri"] = args.redirect_uri
    if args.single_channel is not None:
        params["single_channel"] = args.single_channel
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


def cmd_oauth_oauth_access(args):
    """Exchanges a temporary OAuth verifier code for an access token."""
    path = "/oauth.access"
    params = {}
    if args.client_id is not None:
        params["client_id"] = args.client_id
    if args.client_secret is not None:
        params["client_secret"] = args.client_secret
    if args.code is not None:
        params["code"] = args.code
    if args.redirect_uri is not None:
        params["redirect_uri"] = args.redirect_uri
    if args.single_channel is not None:
        params["single_channel"] = args.single_channel
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


def cmd_oauth_v2_oauth_v2_access(args):
    """Exchanges a temporary OAuth verifier code for an access token."""
    path = "/oauth.v2.access"
    params = {}
    if args.client_id is not None:
        params["client_id"] = args.client_id
    if args.client_secret is not None:
        params["client_secret"] = args.client_secret
    if args.code is not None:
        params["code"] = args.code
    if args.redirect_uri is not None:
        params["redirect_uri"] = args.redirect_uri
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


def cmd_pins_pins_list(args):
    """Lists items pinned to a channel."""
    path = "/pins.list"
    params = {}
    if args.token is not None:
        params["token"] = args.token
    if args.channel is not None:
        params["channel"] = args.channel
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


def cmd_reactions_reactions_get(args):
    """Gets reactions for an item."""
    path = "/reactions.get"
    params = {}
    if args.token is not None:
        params["token"] = args.token
    if args.channel is not None:
        params["channel"] = args.channel
    if args.file is not None:
        params["file"] = args.file
    if args.file_comment is not None:
        params["file_comment"] = args.file_comment
    if args.full is not None:
        params["full"] = args.full
    if args.timestamp is not None:
        params["timestamp"] = args.timestamp
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


def cmd_reactions_reactions_list(args):
    """Lists reactions made by a user."""
    path = "/reactions.list"
    params = {}
    if args.token is not None:
        params["token"] = args.token
    if args.user is not None:
        params["user"] = args.user
    if args.full is not None:
        params["full"] = args.full
    if args.count is not None:
        params["count"] = args.count
    if args.page is not None:
        params["page"] = args.page
    if args.cursor is not None:
        params["cursor"] = args.cursor
    if args.limit is not None:
        params["limit"] = args.limit
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


def cmd_reminders_reminders_info(args):
    """Gets information about a reminder."""
    path = "/reminders.info"
    params = {}
    if args.token is not None:
        params["token"] = args.token
    if args.reminder is not None:
        params["reminder"] = args.reminder
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


def cmd_reminders_reminders_list(args):
    """Lists all reminders created by or for a given user."""
    path = "/reminders.list"
    params = {}
    if args.token is not None:
        params["token"] = args.token
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


def cmd_rtm_rtm_connect(args):
    """Starts a Real Time Messaging session."""
    path = "/rtm.connect"
    params = {}
    if args.token is not None:
        params["token"] = args.token
    if args.batch_presence_aware is not None:
        params["batch_presence_aware"] = args.batch_presence_aware
    if args.presence_sub is not None:
        params["presence_sub"] = args.presence_sub
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


def cmd_stars_stars_list(args):
    """Lists stars for a user."""
    path = "/stars.list"
    params = {}
    if args.token is not None:
        params["token"] = args.token
    if args.count is not None:
        params["count"] = args.count
    if args.page is not None:
        params["page"] = args.page
    if args.cursor is not None:
        params["cursor"] = args.cursor
    if args.limit is not None:
        params["limit"] = args.limit
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


def cmd_team_team_info(args):
    """Gets information about the current team."""
    path = "/team.info"
    params = {}
    if args.token is not None:
        params["token"] = args.token
    if args.team is not None:
        params["team"] = args.team
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


def cmd_users_users_info(args):
    """Gets information about a user."""
    path = "/users.info"
    params = {}
    if args.token is not None:
        params["token"] = args.token
    if args.include_locale is not None:
        params["include_locale"] = args.include_locale
    if args.user is not None:
        params["user"] = args.user
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


def cmd_users_users_list(args):
    """Lists all users in a Slack team."""
    path = "/users.list"
    params = {}
    if args.token is not None:
        params["token"] = args.token
    if args.limit is not None:
        params["limit"] = args.limit
    if args.cursor is not None:
        params["cursor"] = args.cursor
    if args.include_locale is not None:
        params["include_locale"] = args.include_locale
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


def cmd_users_users_identity(args):
    """Get a user's identity."""
    path = "/users.identity"
    params = {}
    if args.token is not None:
        params["token"] = args.token
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


def cmd_views_views_open(args):
    """Open a view for a user."""
    path = "/views.open"
    params = {}
    if args.trigger_id is not None:
        params["trigger_id"] = args.trigger_id
    if args.view is not None:
        params["view"] = args.view
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


def cmd_views_views_push(args):
    """Push a view onto the stack of a root view."""
    path = "/views.push"
    params = {}
    if args.trigger_id is not None:
        params["trigger_id"] = args.trigger_id
    if args.view is not None:
        params["view"] = args.view
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


def cmd_views_views_update(args):
    """Update an existing view."""
    path = "/views.update"
    params = {}
    if args.view_id is not None:
        params["view_id"] = args.view_id
    if args.external_id is not None:
        params["external_id"] = args.external_id
    if args.view is not None:
        params["view"] = args.view
    if args.hash is not None:
        params["hash"] = args.hash
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


def cmd_views_views_publish(args):
    """Publish a static view for a User."""
    path = "/views.publish"
    params = {}
    if args.user_id is not None:
        params["user_id"] = args.user_id
    if args.view is not None:
        params["view"] = args.view
    if args.hash is not None:
        params["hash"] = args.hash
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


def main():
    parser = argparse.ArgumentParser(description="slack CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- check ---
    subparsers.add_parser("check", help="Test API connectivity")

    # --- api ---
    parser_api = subparsers.add_parser("api", help="Api operations")
    sub_api = parser_api.add_subparsers(dest="api_action", help="api actions")

    p_api_api_test = sub_api.add_parser("api-test", help="Checks API calling code.")
    p_api_api_test.add_argument("--error", dest="error", default=None, help="Error response to return")
    p_api_api_test.add_argument("--foo", dest="foo", default=None, help="example property to return")
    p_api_api_test.set_defaults(func=cmd_api_api_test)

    # --- apps ---
    parser_apps = subparsers.add_parser("apps", help="Apps operations")
    sub_apps = parser_apps.add_subparsers(dest="apps_action", help="apps actions")

    p_apps_apps_uninstall = sub_apps.add_parser("apps-uninstall", help="Uninstalls your app from a workspace.")
    p_apps_apps_uninstall.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `none`")
    p_apps_apps_uninstall.add_argument("--client-id", dest="client_id", default=None, help="Issued when you created your application.")
    p_apps_apps_uninstall.add_argument("--client-secret", dest="client_secret", default=None, help="Issued when you created your application.")
    p_apps_apps_uninstall.set_defaults(func=cmd_apps_apps_uninstall)

    # --- auth ---
    parser_auth = subparsers.add_parser("auth", help="Auth operations")
    sub_auth = parser_auth.add_subparsers(dest="auth_action", help="auth actions")

    p_auth_auth_test = sub_auth.add_parser("auth-test", help="Checks authentication & identity.")
    p_auth_auth_test.set_defaults(func=cmd_auth_auth_test)

    p_auth_auth_revoke = sub_auth.add_parser("auth-revoke", help="Revokes a token.")
    p_auth_auth_revoke.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `none`")
    p_auth_auth_revoke.add_argument("--test", dest="test", default=None, help="Setting this parameter to `1` triggers a _testing mode_ where the specified token will not actually be revoked.")
    p_auth_auth_revoke.set_defaults(func=cmd_auth_auth_revoke)

    # --- bots ---
    parser_bots = subparsers.add_parser("bots", help="Bots operations")
    sub_bots = parser_bots.add_subparsers(dest="bots_action", help="bots actions")

    p_bots_bots_info = sub_bots.add_parser("bots-info", help="Gets information about a bot user.")
    p_bots_bots_info.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `users:read`")
    p_bots_bots_info.add_argument("--bot", dest="bot", default=None, help="Bot user to get info on")
    p_bots_bots_info.set_defaults(func=cmd_bots_bots_info)

    # --- calls ---
    parser_calls = subparsers.add_parser("calls", help="Calls operations")
    sub_calls = parser_calls.add_subparsers(dest="calls_action", help="calls actions")

    p_calls_calls_info = sub_calls.add_parser("calls-info", help="Returns information about a Call.")
    p_calls_calls_info.add_argument("--id", dest="id", default=None, help="`id` of the Call returned by the [`calls.add`](/methods/calls.add) method.")
    p_calls_calls_info.set_defaults(func=cmd_calls_calls_info)

    # --- dialog ---
    parser_dialog = subparsers.add_parser("dialog", help="Dialog operations")
    sub_dialog = parser_dialog.add_subparsers(dest="dialog_action", help="dialog actions")

    p_dialog_dialog_open = sub_dialog.add_parser("dialog-open", help="Open a dialog with a user")
    p_dialog_dialog_open.add_argument("--dialog", dest="dialog", default=None, help="The dialog definition. This must be a JSON-encoded string.")
    p_dialog_dialog_open.add_argument("--trigger-id", dest="trigger_id", default=None, help="Exchange a trigger to post to the user.")
    p_dialog_dialog_open.set_defaults(func=cmd_dialog_dialog_open)

    # --- dnd ---
    parser_dnd = subparsers.add_parser("dnd", help="Dnd operations")
    sub_dnd = parser_dnd.add_subparsers(dest="dnd_action", help="dnd actions")

    p_dnd_dnd_info = sub_dnd.add_parser("dnd-info", help="Retrieves a user's current Do Not Disturb status.")
    p_dnd_dnd_info.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `dnd:read`")
    p_dnd_dnd_info.add_argument("--user", dest="user", default=None, help="User to fetch status for (defaults to current user)")
    p_dnd_dnd_info.set_defaults(func=cmd_dnd_dnd_info)

    p_dnd_dnd_teaminfo = sub_dnd.add_parser("dnd-teaminfo", help="Retrieves the Do Not Disturb status for up to 50 users on a team.")
    p_dnd_dnd_teaminfo.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `dnd:read`")
    p_dnd_dnd_teaminfo.add_argument("--users", dest="users", default=None, help="Comma-separated list of users to fetch Do Not Disturb status for")
    p_dnd_dnd_teaminfo.set_defaults(func=cmd_dnd_dnd_teaminfo)

    # --- emoji ---
    parser_emoji = subparsers.add_parser("emoji", help="Emoji operations")
    sub_emoji = parser_emoji.add_subparsers(dest="emoji_action", help="emoji actions")

    p_emoji_emoji_list = sub_emoji.add_parser("emoji-list", help="Lists custom emoji for a team.")
    p_emoji_emoji_list.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `emoji:read`")
    p_emoji_emoji_list.set_defaults(func=cmd_emoji_emoji_list)

    # --- files ---
    parser_files = subparsers.add_parser("files", help="Files operations")
    sub_files = parser_files.add_subparsers(dest="files_action", help="files actions")

    p_files_files_info = sub_files.add_parser("files-info", help="Gets information about a file.")
    p_files_files_info.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `files:read`")
    p_files_files_info.add_argument("--file", dest="file", default=None, help="Specify a file by providing its ID.")
    p_files_files_info.add_argument("--count", dest="count", default=None, help="")
    p_files_files_info.add_argument("--page", dest="page", default=None, help="")
    p_files_files_info.add_argument("--limit", dest="limit", default=None, help="The maximum number of items to return. Fewer than the requested number of items may be returned, even if the end of the list hasn't been reached.")
    p_files_files_info.add_argument("--cursor", dest="cursor", default=None, help="Parameter for pagination. File comments are paginated for a single file. Set `cursor` equal to the `next_cursor` attribute returned by the previous request's `response_metadata`. This parameter is optional, but pagination is mandatory: the default value simply fetches the first \"page\" of the collection of comments. See [pagination](/docs/pagination) for more details.")
    p_files_files_info.set_defaults(func=cmd_files_files_info)

    p_files_files_list = sub_files.add_parser("files-list", help="List for a team, in a channel, or from a user with applied filters.")
    p_files_files_list.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `files:read`")
    p_files_files_list.add_argument("--user", dest="user", default=None, help="Filter files created by a single user.")
    p_files_files_list.add_argument("--channel", dest="channel", default=None, help="Filter files appearing in a specific channel, indicated by its ID.")
    p_files_files_list.add_argument("--ts-from", dest="ts_from", default=None, help="Filter files created after this timestamp (inclusive).")
    p_files_files_list.add_argument("--ts-to", dest="ts_to", default=None, help="Filter files created before this timestamp (inclusive).")
    p_files_files_list.add_argument("--types", dest="types", default=None, help="Filter files by type ([see below](#file_types)). You can pass multiple values in the types argument, like `types=spaces,snippets`.The default value is `all`, which does not filter the list.")
    p_files_files_list.add_argument("--count", dest="count", default=None, help="")
    p_files_files_list.add_argument("--page", dest="page", default=None, help="")
    p_files_files_list.add_argument("--show-files-hidden-by-limit", dest="show_files_hidden_by_limit", default=None, help="Show truncated file info for files hidden due to being too old, and the team who owns the file being over the file limit.")
    p_files_files_list.set_defaults(func=cmd_files_files_list)

    # --- oauth ---
    parser_oauth = subparsers.add_parser("oauth", help="Oauth operations")
    sub_oauth = parser_oauth.add_subparsers(dest="oauth_action", help="oauth actions")

    p_oauth_oauth_token = sub_oauth.add_parser("oauth-token", help="Exchanges a temporary OAuth verifier code for a workspace token.")
    p_oauth_oauth_token.add_argument("--client-id", dest="client_id", default=None, help="Issued when you created your application.")
    p_oauth_oauth_token.add_argument("--client-secret", dest="client_secret", default=None, help="Issued when you created your application.")
    p_oauth_oauth_token.add_argument("--code", dest="code", default=None, help="The `code` param returned via the OAuth callback.")
    p_oauth_oauth_token.add_argument("--redirect-uri", dest="redirect_uri", default=None, help="This must match the originally submitted URI (if one was sent).")
    p_oauth_oauth_token.add_argument("--single-channel", dest="single_channel", default=None, help="Request the user to add your app only to a single channel.")
    p_oauth_oauth_token.set_defaults(func=cmd_oauth_oauth_token)

    p_oauth_oauth_access = sub_oauth.add_parser("oauth-access", help="Exchanges a temporary OAuth verifier code for an access token.")
    p_oauth_oauth_access.add_argument("--client-id", dest="client_id", default=None, help="Issued when you created your application.")
    p_oauth_oauth_access.add_argument("--client-secret", dest="client_secret", default=None, help="Issued when you created your application.")
    p_oauth_oauth_access.add_argument("--code", dest="code", default=None, help="The `code` param returned via the OAuth callback.")
    p_oauth_oauth_access.add_argument("--redirect-uri", dest="redirect_uri", default=None, help="This must match the originally submitted URI (if one was sent).")
    p_oauth_oauth_access.add_argument("--single-channel", dest="single_channel", default=None, help="Request the user to add your app only to a single channel. Only valid with a [legacy workspace app](https://api.slack.com/legacy-workspace-apps).")
    p_oauth_oauth_access.set_defaults(func=cmd_oauth_oauth_access)

    # --- oauth-v2 ---
    parser_oauth_v2 = subparsers.add_parser("oauth-v2", help="Oauth-V2 operations")
    sub_oauth_v2 = parser_oauth_v2.add_subparsers(dest="oauth_v2_action", help="oauth-v2 actions")

    p_oauth_v2_oauth_v2_access = sub_oauth_v2.add_parser("oauth-v2-access", help="Exchanges a temporary OAuth verifier code for an access token.")
    p_oauth_v2_oauth_v2_access.add_argument("--client-id", dest="client_id", default=None, help="Issued when you created your application.")
    p_oauth_v2_oauth_v2_access.add_argument("--client-secret", dest="client_secret", default=None, help="Issued when you created your application.")
    p_oauth_v2_oauth_v2_access.add_argument("--code", dest="code", default=None, help="The `code` param returned via the OAuth callback.")
    p_oauth_v2_oauth_v2_access.add_argument("--redirect-uri", dest="redirect_uri", default=None, help="This must match the originally submitted URI (if one was sent).")
    p_oauth_v2_oauth_v2_access.set_defaults(func=cmd_oauth_v2_oauth_v2_access)

    # --- pins ---
    parser_pins = subparsers.add_parser("pins", help="Pins operations")
    sub_pins = parser_pins.add_subparsers(dest="pins_action", help="pins actions")

    p_pins_pins_list = sub_pins.add_parser("pins-list", help="Lists items pinned to a channel.")
    p_pins_pins_list.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `pins:read`")
    p_pins_pins_list.add_argument("--channel", dest="channel", default=None, help="Channel to get pinned items for.")
    p_pins_pins_list.set_defaults(func=cmd_pins_pins_list)

    # --- reactions ---
    parser_reactions = subparsers.add_parser("reactions", help="Reactions operations")
    sub_reactions = parser_reactions.add_subparsers(dest="reactions_action", help="reactions actions")

    p_reactions_reactions_get = sub_reactions.add_parser("reactions-get", help="Gets reactions for an item.")
    p_reactions_reactions_get.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `reactions:read`")
    p_reactions_reactions_get.add_argument("--channel", dest="channel", default=None, help="Channel where the message to get reactions for was posted.")
    p_reactions_reactions_get.add_argument("--file", dest="file", default=None, help="File to get reactions for.")
    p_reactions_reactions_get.add_argument("--file-comment", dest="file_comment", default=None, help="File comment to get reactions for.")
    p_reactions_reactions_get.add_argument("--full", dest="full", default=None, help="If true always return the complete reaction list.")
    p_reactions_reactions_get.add_argument("--timestamp", dest="timestamp", default=None, help="Timestamp of the message to get reactions for.")
    p_reactions_reactions_get.set_defaults(func=cmd_reactions_reactions_get)

    p_reactions_reactions_list = sub_reactions.add_parser("reactions-list", help="Lists reactions made by a user.")
    p_reactions_reactions_list.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `reactions:read`")
    p_reactions_reactions_list.add_argument("--user", dest="user", default=None, help="Show reactions made by this user. Defaults to the authed user.")
    p_reactions_reactions_list.add_argument("--full", dest="full", default=None, help="If true always return the complete reaction list.")
    p_reactions_reactions_list.add_argument("--count", dest="count", default=None, help="")
    p_reactions_reactions_list.add_argument("--page", dest="page", default=None, help="")
    p_reactions_reactions_list.add_argument("--cursor", dest="cursor", default=None, help="Parameter for pagination. Set `cursor` equal to the `next_cursor` attribute returned by the previous request's `response_metadata`. This parameter is optional, but pagination is mandatory: the default value simply fetches the first \"page\" of the collection. See [pagination](/docs/pagination) for more details.")
    p_reactions_reactions_list.add_argument("--limit", dest="limit", default=None, help="The maximum number of items to return. Fewer than the requested number of items may be returned, even if the end of the list hasn't been reached.")
    p_reactions_reactions_list.set_defaults(func=cmd_reactions_reactions_list)

    # --- reminders ---
    parser_reminders = subparsers.add_parser("reminders", help="Reminders operations")
    sub_reminders = parser_reminders.add_subparsers(dest="reminders_action", help="reminders actions")

    p_reminders_reminders_info = sub_reminders.add_parser("reminders-info", help="Gets information about a reminder.")
    p_reminders_reminders_info.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `reminders:read`")
    p_reminders_reminders_info.add_argument("--reminder", dest="reminder", default=None, help="The ID of the reminder")
    p_reminders_reminders_info.set_defaults(func=cmd_reminders_reminders_info)

    p_reminders_reminders_list = sub_reminders.add_parser("reminders-list", help="Lists all reminders created by or for a given user.")
    p_reminders_reminders_list.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `reminders:read`")
    p_reminders_reminders_list.set_defaults(func=cmd_reminders_reminders_list)

    # --- rtm ---
    parser_rtm = subparsers.add_parser("rtm", help="Rtm operations")
    sub_rtm = parser_rtm.add_subparsers(dest="rtm_action", help="rtm actions")

    p_rtm_rtm_connect = sub_rtm.add_parser("rtm-connect", help="Starts a Real Time Messaging session.")
    p_rtm_rtm_connect.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `rtm:stream`")
    p_rtm_rtm_connect.add_argument("--batch-presence-aware", dest="batch_presence_aware", default=None, help="Batch presence deliveries via subscription. Enabling changes the shape of `presence_change` events. See [batch presence](/docs/presence-and-status#batching).")
    p_rtm_rtm_connect.add_argument("--presence-sub", dest="presence_sub", default=None, help="Only deliver presence events when requested by subscription. See [presence subscriptions](/docs/presence-and-status#subscriptions).")
    p_rtm_rtm_connect.set_defaults(func=cmd_rtm_rtm_connect)

    # --- stars ---
    parser_stars = subparsers.add_parser("stars", help="Stars operations")
    sub_stars = parser_stars.add_subparsers(dest="stars_action", help="stars actions")

    p_stars_stars_list = sub_stars.add_parser("stars-list", help="Lists stars for a user.")
    p_stars_stars_list.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `stars:read`")
    p_stars_stars_list.add_argument("--count", dest="count", default=None, help="")
    p_stars_stars_list.add_argument("--page", dest="page", default=None, help="")
    p_stars_stars_list.add_argument("--cursor", dest="cursor", default=None, help="Parameter for pagination. Set `cursor` equal to the `next_cursor` attribute returned by the previous request's `response_metadata`. This parameter is optional, but pagination is mandatory: the default value simply fetches the first \"page\" of the collection. See [pagination](/docs/pagination) for more details.")
    p_stars_stars_list.add_argument("--limit", dest="limit", default=None, help="The maximum number of items to return. Fewer than the requested number of items may be returned, even if the end of the list hasn't been reached.")
    p_stars_stars_list.set_defaults(func=cmd_stars_stars_list)

    # --- team ---
    parser_team = subparsers.add_parser("team", help="Team operations")
    sub_team = parser_team.add_subparsers(dest="team_action", help="team actions")

    p_team_team_info = sub_team.add_parser("team-info", help="Gets information about the current team.")
    p_team_team_info.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `team:read`")
    p_team_team_info.add_argument("--team", dest="team", default=None, help="Team to get info on, if omitted, will return information about the current team. Will only return team that the authenticated token is allowed to see through external shared channels")
    p_team_team_info.set_defaults(func=cmd_team_team_info)

    # --- users ---
    parser_users = subparsers.add_parser("users", help="Users operations")
    sub_users = parser_users.add_subparsers(dest="users_action", help="users actions")

    p_users_users_info = sub_users.add_parser("users-info", help="Gets information about a user.")
    p_users_users_info.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `users:read`")
    p_users_users_info.add_argument("--include-locale", dest="include_locale", default=None, help="Set this to `true` to receive the locale for this user. Defaults to `false`")
    p_users_users_info.add_argument("--user", dest="user", default=None, help="User to get info on")
    p_users_users_info.set_defaults(func=cmd_users_users_info)

    p_users_users_list = sub_users.add_parser("users-list", help="Lists all users in a Slack team.")
    p_users_users_list.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `users:read`")
    p_users_users_list.add_argument("--limit", dest="limit", default=None, help="The maximum number of items to return. Fewer than the requested number of items may be returned, even if the end of the users list hasn't been reached. Providing no `limit` value will result in Slack attempting to deliver you the entire result set. If the collection is too large you may experience `limit_required` or HTTP 500 errors.")
    p_users_users_list.add_argument("--cursor", dest="cursor", default=None, help="Paginate through collections of data by setting the `cursor` parameter to a `next_cursor` attribute returned by a previous request's `response_metadata`. Default value fetches the first \"page\" of the collection. See [pagination](/docs/pagination) for more detail.")
    p_users_users_list.add_argument("--include-locale", dest="include_locale", default=None, help="Set this to `true` to receive the locale for users. Defaults to `false`")
    p_users_users_list.set_defaults(func=cmd_users_users_list)

    p_users_users_identity = sub_users.add_parser("users-identity", help="Get a user's identity.")
    p_users_users_identity.add_argument("--token", dest="token", default=None, help="Authentication token. Requires scope: `identity.basic`")
    p_users_users_identity.set_defaults(func=cmd_users_users_identity)

    # --- views ---
    parser_views = subparsers.add_parser("views", help="Views operations")
    sub_views = parser_views.add_subparsers(dest="views_action", help="views actions")

    p_views_views_open = sub_views.add_parser("views-open", help="Open a view for a user.")
    p_views_views_open.add_argument("--trigger-id", dest="trigger_id", default=None, help="Exchange a trigger to post to the user.")
    p_views_views_open.add_argument("--view", dest="view", default=None, help="A [view payload](/reference/surfaces/views). This must be a JSON-encoded string.")
    p_views_views_open.set_defaults(func=cmd_views_views_open)

    p_views_views_push = sub_views.add_parser("views-push", help="Push a view onto the stack of a root view.")
    p_views_views_push.add_argument("--trigger-id", dest="trigger_id", default=None, help="Exchange a trigger to post to the user.")
    p_views_views_push.add_argument("--view", dest="view", default=None, help="A [view payload](/reference/surfaces/views). This must be a JSON-encoded string.")
    p_views_views_push.set_defaults(func=cmd_views_views_push)

    p_views_views_update = sub_views.add_parser("views-update", help="Update an existing view.")
    p_views_views_update.add_argument("--view-id", dest="view_id", default=None, help="A unique identifier of the view to be updated. Either `view_id` or `external_id` is required.")
    p_views_views_update.add_argument("--external-id", dest="external_id", default=None, help="A unique identifier of the view set by the developer. Must be unique for all views on a team. Max length of 255 characters. Either `view_id` or `external_id` is required.")
    p_views_views_update.add_argument("--view", dest="view", default=None, help="A [view object](/reference/surfaces/views). This must be a JSON-encoded string.")
    p_views_views_update.add_argument("--hash", dest="hash", default=None, help="A string that represents view state to protect against possible race conditions.")
    p_views_views_update.set_defaults(func=cmd_views_views_update)

    p_views_views_publish = sub_views.add_parser("views-publish", help="Publish a static view for a User.")
    p_views_views_publish.add_argument("--user-id", dest="user_id", default=None, help="`id` of the user you want publish a view to.")
    p_views_views_publish.add_argument("--view", dest="view", default=None, help="A [view payload](/reference/surfaces/views). This must be a JSON-encoded string.")
    p_views_views_publish.add_argument("--hash", dest="hash", default=None, help="A string that represents view state to protect against possible race conditions.")
    p_views_views_publish.set_defaults(func=cmd_views_views_publish)

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
