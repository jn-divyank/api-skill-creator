#!/usr/bin/env python3
"""
twilio CLI tool for Claude Code skill integration.
Provides access to the twilio-api API.
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
BASE_URL = _env.get("TWILIO_URL", "https://api.twilio.com")
AUTH_TOKEN = _env.get("TWILIO_TOKEN", "")

_ssl_ctx = ssl.create_default_context()
if _env.get("TWILIO_VERIFY_SSL", "true").lower() == "false":
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = ssl.CERT_NONE


def get_auth_header() -> dict:
    """Build authorization header."""
    if AUTH_TOKEN:
        # AUTH_TOKEN should be "user:password"
        encoded = base64.b64encode(AUTH_TOKEN.encode()).decode()
        return {"Authorization": f"Basic {encoded}"}
    return {}


def make_request(path: str, method: str = "GET", data: bytes = None, params: dict = None) -> tuple:
    """Make HTTP request to the twilio API."""
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
    """Verify connectivity to the twilio API."""
    if not BASE_URL:
        print(f"Error: TWILIO_URL not set", file=sys.stderr)
        sys.exit(1)
    status, body = make_request("/")
    if status == 0:
        print(f"Cannot connect to {BASE_URL}", file=sys.stderr)
        print(f"Error: {body}", file=sys.stderr)
        sys.exit(1)
    print(f"Connected to {BASE_URL} (HTTP {status})")


def cmd__2010_04_01_list(args):
    """Retrieves a collection of Accounts belonging to the account used to make the request"""
    path = "/2010-04-01/Accounts.json"
    params = {}
    if args.FriendlyName is not None:
        params["FriendlyName"] = args.FriendlyName
    if args.Status is not None:
        params["Status"] = args.Status
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_fetchaccount(args):
    """Fetch the account specified by the provided Account Sid"""
    path = "/2010-04-01/Accounts/{Sid}.json".replace("{Sid}", str(args.Sid))
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


def cmd__2010_04_01_list_2(args):
    """"""
    path = "/2010-04-01/Accounts/{AccountSid}/Keys.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_list_3(args):
    """Retrieves a collection of calls made to and from your account"""
    path = "/2010-04-01/Accounts/{AccountSid}/Calls.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.To is not None:
        params["To"] = args.To
    if args.From is not None:
        params["From"] = args.From
    if args.ParentCallSid is not None:
        params["ParentCallSid"] = args.ParentCallSid
    if args.Status is not None:
        params["Status"] = args.Status
    if args.StartTime is not None:
        params["StartTime"] = args.StartTime
    if args.StartTime is not None:
        params["StartTime<"] = args.StartTime
    if args.StartTime is not None:
        params["StartTime>"] = args.StartTime
    if args.EndTime is not None:
        params["EndTime"] = args.EndTime
    if args.EndTime is not None:
        params["EndTime<"] = args.EndTime
    if args.EndTime is not None:
        params["EndTime>"] = args.EndTime
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_list_4(args):
    """Retrieve a list of queues belonging to the account used to make the request"""
    path = "/2010-04-01/Accounts/{AccountSid}/Queues.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_fetchbalance(args):
    """Fetch the balance for an Account based on Account Sid. Balance changes may not be reflected immediately. Child accounts do not contain balance information"""
    path = "/2010-04-01/Accounts/{AccountSid}/Balance.json".replace("{AccountSid}", str(args.AccountSid))
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


def cmd__2010_04_01_list_5(args):
    """Retrieve a list of messages belonging to the account used to make the request"""
    path = "/2010-04-01/Accounts/{AccountSid}/Messages.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.To is not None:
        params["To"] = args.To
    if args.From is not None:
        params["From"] = args.From
    if args.DateSent is not None:
        params["DateSent"] = args.DateSent
    if args.DateSent is not None:
        params["DateSent<"] = args.DateSent
    if args.DateSent is not None:
        params["DateSent>"] = args.DateSent
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_list_6(args):
    """"""
    path = "/2010-04-01/Accounts/{AccountSid}/Addresses.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.CustomerName is not None:
        params["CustomerName"] = args.CustomerName
    if args.FriendlyName is not None:
        params["FriendlyName"] = args.FriendlyName
    if args.IsoCountry is not None:
        params["IsoCountry"] = args.IsoCountry
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_fetchkey(args):
    """"""
    path = "/2010-04-01/Accounts/{AccountSid}/Keys/{Sid}.json".replace("{AccountSid}", str(args.AccountSid))
    path = "{already_substituted}".replace("{Sid}", str(args.Sid))
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


def cmd__2010_04_01_list_7(args):
    """Retrieve a list of recordings belonging to the account used to make the request"""
    path = "/2010-04-01/Accounts/{AccountSid}/Recordings.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.DateCreated is not None:
        params["DateCreated"] = args.DateCreated
    if args.DateCreated is not None:
        params["DateCreated<"] = args.DateCreated
    if args.DateCreated is not None:
        params["DateCreated>"] = args.DateCreated
    if args.CallSid is not None:
        params["CallSid"] = args.CallSid
    if args.ConferenceSid is not None:
        params["ConferenceSid"] = args.ConferenceSid
    if args.IncludeSoftDeleted is not None:
        params["IncludeSoftDeleted"] = args.IncludeSoftDeleted
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_fetchcall(args):
    """Fetch the call specified by the provided Call SID"""
    path = "/2010-04-01/Accounts/{AccountSid}/Calls/{Sid}.json".replace("{AccountSid}", str(args.AccountSid))
    path = "{already_substituted}".replace("{Sid}", str(args.Sid))
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


def cmd__2010_04_01_list_8(args):
    """Retrieve a list of conferences belonging to the account used to make the request"""
    path = "/2010-04-01/Accounts/{AccountSid}/Conferences.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.DateCreated is not None:
        params["DateCreated"] = args.DateCreated
    if args.DateCreated is not None:
        params["DateCreated<"] = args.DateCreated
    if args.DateCreated is not None:
        params["DateCreated>"] = args.DateCreated
    if args.DateUpdated is not None:
        params["DateUpdated"] = args.DateUpdated
    if args.DateUpdated is not None:
        params["DateUpdated<"] = args.DateUpdated
    if args.DateUpdated is not None:
        params["DateUpdated>"] = args.DateUpdated
    if args.FriendlyName is not None:
        params["FriendlyName"] = args.FriendlyName
    if args.Status is not None:
        params["Status"] = args.Status
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_list_9(args):
    """Retrieve a list of connect-apps belonging to the account used to make the request"""
    path = "/2010-04-01/Accounts/{AccountSid}/ConnectApps.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_list_10(args):
    """Retrieve a list of domains belonging to the account used to make the request"""
    path = "/2010-04-01/Accounts/{AccountSid}/SIP/Domains.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_list_11(args):
    """"""
    path = "/2010-04-01/Accounts/{AccountSid}/SigningKeys.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_list_12(args):
    """Retrieve a list of applications representing an application within the requesting account"""
    path = "/2010-04-01/Accounts/{AccountSid}/Applications.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.FriendlyName is not None:
        params["FriendlyName"] = args.FriendlyName
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_fetchqueue(args):
    """Fetch an instance of a queue identified by the QueueSid"""
    path = "/2010-04-01/Accounts/{AccountSid}/Queues/{Sid}.json".replace("{AccountSid}", str(args.AccountSid))
    path = "{already_substituted}".replace("{Sid}", str(args.Sid))
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


def cmd__2010_04_01_list_13(args):
    """Retrieve a list of notifications belonging to the account used to make the request"""
    path = "/2010-04-01/Accounts/{AccountSid}/Notifications.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.Log is not None:
        params["Log"] = args.Log
    if args.MessageDate is not None:
        params["MessageDate"] = args.MessageDate
    if args.MessageDate is not None:
        params["MessageDate<"] = args.MessageDate
    if args.MessageDate is not None:
        params["MessageDate>"] = args.MessageDate
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_list_14(args):
    """Retrieve a list of usage-records belonging to the account used to make the request"""
    path = "/2010-04-01/Accounts/{AccountSid}/Usage/Records.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.Category is not None:
        params["Category"] = args.Category
    if args.StartDate is not None:
        params["StartDate"] = args.StartDate
    if args.EndDate is not None:
        params["EndDate"] = args.EndDate
    if args.IncludeSubaccounts is not None:
        params["IncludeSubaccounts"] = args.IncludeSubaccounts
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_fetchmessage(args):
    """Fetch a message belonging to the account used to make the request"""
    path = "/2010-04-01/Accounts/{AccountSid}/Messages/{Sid}.json".replace("{AccountSid}", str(args.AccountSid))
    path = "{already_substituted}".replace("{Sid}", str(args.Sid))
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


def cmd__2010_04_01_list_15(args):
    """Retrieve a list of short-codes belonging to the account used to make the request"""
    path = "/2010-04-01/Accounts/{AccountSid}/SMS/ShortCodes.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.FriendlyName is not None:
        params["FriendlyName"] = args.FriendlyName
    if args.ShortCode is not None:
        params["ShortCode"] = args.ShortCode
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_list_16(args):
    """Retrieve a list of transcriptions belonging to the account used to make the request"""
    path = "/2010-04-01/Accounts/{AccountSid}/Transcriptions.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_list_17(args):
    """Retrieve a list of usage-triggers belonging to the account used to make the request"""
    path = "/2010-04-01/Accounts/{AccountSid}/Usage/Triggers.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.Recurring is not None:
        params["Recurring"] = args.Recurring
    if args.TriggerBy is not None:
        params["TriggerBy"] = args.TriggerBy
    if args.UsageCategory is not None:
        params["UsageCategory"] = args.UsageCategory
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_fetchaddress(args):
    """"""
    path = "/2010-04-01/Accounts/{AccountSid}/Addresses/{Sid}.json".replace("{AccountSid}", str(args.AccountSid))
    path = "{already_substituted}".replace("{Sid}", str(args.Sid))
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


def cmd__2010_04_01_fetchrecording(args):
    """Fetch an instance of a recording"""
    path = "/2010-04-01/Accounts/{AccountSid}/Recordings/{Sid}.json".replace("{AccountSid}", str(args.AccountSid))
    path = "{already_substituted}".replace("{Sid}", str(args.Sid))
    params = {}
    if args.IncludeSoftDeleted is not None:
        params["IncludeSoftDeleted"] = args.IncludeSoftDeleted
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


def cmd__2010_04_01_fetchconference(args):
    """Fetch an instance of a conference"""
    path = "/2010-04-01/Accounts/{AccountSid}/Conferences/{Sid}.json".replace("{AccountSid}", str(args.AccountSid))
    path = "{already_substituted}".replace("{Sid}", str(args.Sid))
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


def cmd__2010_04_01_fetchconnectapp(args):
    """Fetch an instance of a connect-app"""
    path = "/2010-04-01/Accounts/{AccountSid}/ConnectApps/{Sid}.json".replace("{AccountSid}", str(args.AccountSid))
    path = "{already_substituted}".replace("{Sid}", str(args.Sid))
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


def cmd__2010_04_01_list_18(args):
    """Retrieve a list of outgoing-caller-ids belonging to the account used to make the request"""
    path = "/2010-04-01/Accounts/{AccountSid}/OutgoingCallerIds.json".replace("{AccountSid}", str(args.AccountSid))
    params = {}
    if args.PhoneNumber is not None:
        params["PhoneNumber"] = args.PhoneNumber
    if args.FriendlyName is not None:
        params["FriendlyName"] = args.FriendlyName
    if args.PageSize is not None:
        params["PageSize"] = args.PageSize
    if args.Page is not None:
        params["Page"] = args.Page
    if args.PageToken is not None:
        params["PageToken"] = args.PageToken
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


def cmd__2010_04_01_fetchsipdomain(args):
    """Fetch an instance of a Domain"""
    path = "/2010-04-01/Accounts/{AccountSid}/SIP/Domains/{Sid}.json".replace("{AccountSid}", str(args.AccountSid))
    path = "{already_substituted}".replace("{Sid}", str(args.Sid))
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


def cmd__2010_04_01_fetchsigningkey(args):
    """"""
    path = "/2010-04-01/Accounts/{AccountSid}/SigningKeys/{Sid}.json".replace("{AccountSid}", str(args.AccountSid))
    path = "{already_substituted}".replace("{Sid}", str(args.Sid))
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
    parser = argparse.ArgumentParser(description="twilio CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- check ---
    subparsers.add_parser("check", help="Test API connectivity")

    # --- 2010-04-01 ---
    parser__2010_04_01 = subparsers.add_parser("2010-04-01", help="2010-04-01 operations")
    sub__2010_04_01 = parser__2010_04_01.add_subparsers(dest="_2010_04_01_action", help="2010-04-01 actions")

    p__2010_04_01_list = sub__2010_04_01.add_parser("list", help="Retrieves a collection of Accounts belonging to the account used to make the request")
    p__2010_04_01_list.add_argument("--FriendlyName", dest="FriendlyName", default=None, help="Only return the Account resources with friendly names that exactly match this name.")
    p__2010_04_01_list.add_argument("--Status", dest="Status", default=None, help="Only return Account resources with the given status. Can be `closed`, `suspended` or `active`.")
    p__2010_04_01_list.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list.set_defaults(func=cmd__2010_04_01_list)

    p__2010_04_01_fetchaccount = sub__2010_04_01.add_parser("fetchaccount", help="Fetch the account specified by the provided Account Sid")
    p__2010_04_01_fetchaccount.add_argument("Sid", help="Sid")
    p__2010_04_01_fetchaccount.set_defaults(func=cmd__2010_04_01_fetchaccount)

    p__2010_04_01_list_2 = sub__2010_04_01.add_parser("list-2", help="")
    p__2010_04_01_list_2.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_2.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_2.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_2.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_2.set_defaults(func=cmd__2010_04_01_list_2)

    p__2010_04_01_list_3 = sub__2010_04_01.add_parser("list-3", help="Retrieves a collection of calls made to and from your account")
    p__2010_04_01_list_3.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_3.add_argument("--To", dest="To", default=None, help="Only show calls made to this phone number, SIP address, Client identifier or SIM SID.")
    p__2010_04_01_list_3.add_argument("--From", dest="From", default=None, help="Only include calls from this phone number, SIP address, Client identifier or SIM SID.")
    p__2010_04_01_list_3.add_argument("--ParentCallSid", dest="ParentCallSid", default=None, help="Only include calls spawned by calls with this SID.")
    p__2010_04_01_list_3.add_argument("--Status", dest="Status", default=None, help="The status of the calls to include. Can be: `queued`, `ringing`, `in-progress`, `canceled`, `completed`, `failed`, `busy`, or `no-answer`.")
    p__2010_04_01_list_3.add_argument("--StartTime", dest="StartTime", default=None, help="Only include calls that started on this date. Specify a date as `YYYY-MM-DD` in GMT, for example: `2009-07-06`, to read only calls that started on this date. You can also specify an inequality, such as `StartTime<=YYYY-MM-DD`, to read calls that started on or before midnight of this date, and `StartTime>=YYYY-MM-DD` to read calls that started on or after midnight of this date.")
    p__2010_04_01_list_3.add_argument("--StartTime<", dest="StartTime", default=None, help="Only include calls that started on this date. Specify a date as `YYYY-MM-DD` in GMT, for example: `2009-07-06`, to read only calls that started on this date. You can also specify an inequality, such as `StartTime<=YYYY-MM-DD`, to read calls that started on or before midnight of this date, and `StartTime>=YYYY-MM-DD` to read calls that started on or after midnight of this date.")
    p__2010_04_01_list_3.add_argument("--StartTime>", dest="StartTime", default=None, help="Only include calls that started on this date. Specify a date as `YYYY-MM-DD` in GMT, for example: `2009-07-06`, to read only calls that started on this date. You can also specify an inequality, such as `StartTime<=YYYY-MM-DD`, to read calls that started on or before midnight of this date, and `StartTime>=YYYY-MM-DD` to read calls that started on or after midnight of this date.")
    p__2010_04_01_list_3.add_argument("--EndTime", dest="EndTime", default=None, help="Only include calls that ended on this date. Specify a date as `YYYY-MM-DD` in GMT, for example: `2009-07-06`, to read only calls that ended on this date. You can also specify an inequality, such as `EndTime<=YYYY-MM-DD`, to read calls that ended on or before midnight of this date, and `EndTime>=YYYY-MM-DD` to read calls that ended on or after midnight of this date.")
    p__2010_04_01_list_3.add_argument("--EndTime<", dest="EndTime", default=None, help="Only include calls that ended on this date. Specify a date as `YYYY-MM-DD` in GMT, for example: `2009-07-06`, to read only calls that ended on this date. You can also specify an inequality, such as `EndTime<=YYYY-MM-DD`, to read calls that ended on or before midnight of this date, and `EndTime>=YYYY-MM-DD` to read calls that ended on or after midnight of this date.")
    p__2010_04_01_list_3.add_argument("--EndTime>", dest="EndTime", default=None, help="Only include calls that ended on this date. Specify a date as `YYYY-MM-DD` in GMT, for example: `2009-07-06`, to read only calls that ended on this date. You can also specify an inequality, such as `EndTime<=YYYY-MM-DD`, to read calls that ended on or before midnight of this date, and `EndTime>=YYYY-MM-DD` to read calls that ended on or after midnight of this date.")
    p__2010_04_01_list_3.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_3.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_3.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_3.set_defaults(func=cmd__2010_04_01_list_3)

    p__2010_04_01_list_4 = sub__2010_04_01.add_parser("list-4", help="Retrieve a list of queues belonging to the account used to make the request")
    p__2010_04_01_list_4.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_4.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_4.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_4.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_4.set_defaults(func=cmd__2010_04_01_list_4)

    p__2010_04_01_fetchbalance = sub__2010_04_01.add_parser("fetchbalance", help="Fetch the balance for an Account based on Account Sid. Balance changes may not be reflected immediately. Child accounts do not contain balance information")
    p__2010_04_01_fetchbalance.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_fetchbalance.set_defaults(func=cmd__2010_04_01_fetchbalance)

    p__2010_04_01_list_5 = sub__2010_04_01.add_parser("list-5", help="Retrieve a list of messages belonging to the account used to make the request")
    p__2010_04_01_list_5.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_5.add_argument("--To", dest="To", default=None, help="Read messages sent to only this phone number.")
    p__2010_04_01_list_5.add_argument("--From", dest="From", default=None, help="Read messages sent from only this phone number or alphanumeric sender ID.")
    p__2010_04_01_list_5.add_argument("--DateSent", dest="DateSent", default=None, help="The date of the messages to show. Specify a date as `YYYY-MM-DD` in GMT to read only messages sent on this date. For example: `2009-07-06`. You can also specify an inequality, such as `DateSent<=YYYY-MM-DD`, to read messages sent on or before midnight on a date, and `DateSent>=YYYY-MM-DD` to read messages sent on or after midnight on a date.")
    p__2010_04_01_list_5.add_argument("--DateSent<", dest="DateSent", default=None, help="The date of the messages to show. Specify a date as `YYYY-MM-DD` in GMT to read only messages sent on this date. For example: `2009-07-06`. You can also specify an inequality, such as `DateSent<=YYYY-MM-DD`, to read messages sent on or before midnight on a date, and `DateSent>=YYYY-MM-DD` to read messages sent on or after midnight on a date.")
    p__2010_04_01_list_5.add_argument("--DateSent>", dest="DateSent", default=None, help="The date of the messages to show. Specify a date as `YYYY-MM-DD` in GMT to read only messages sent on this date. For example: `2009-07-06`. You can also specify an inequality, such as `DateSent<=YYYY-MM-DD`, to read messages sent on or before midnight on a date, and `DateSent>=YYYY-MM-DD` to read messages sent on or after midnight on a date.")
    p__2010_04_01_list_5.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_5.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_5.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_5.set_defaults(func=cmd__2010_04_01_list_5)

    p__2010_04_01_list_6 = sub__2010_04_01.add_parser("list-6", help="")
    p__2010_04_01_list_6.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_6.add_argument("--CustomerName", dest="CustomerName", default=None, help="The `customer_name` of the Address resources to read.")
    p__2010_04_01_list_6.add_argument("--FriendlyName", dest="FriendlyName", default=None, help="The string that identifies the Address resources to read.")
    p__2010_04_01_list_6.add_argument("--IsoCountry", dest="IsoCountry", default=None, help="The ISO country code of the Address resources to read.")
    p__2010_04_01_list_6.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_6.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_6.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_6.set_defaults(func=cmd__2010_04_01_list_6)

    p__2010_04_01_fetchkey = sub__2010_04_01.add_parser("fetchkey", help="")
    p__2010_04_01_fetchkey.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_fetchkey.add_argument("Sid", help="Sid")
    p__2010_04_01_fetchkey.set_defaults(func=cmd__2010_04_01_fetchkey)

    p__2010_04_01_list_7 = sub__2010_04_01.add_parser("list-7", help="Retrieve a list of recordings belonging to the account used to make the request")
    p__2010_04_01_list_7.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_7.add_argument("--DateCreated", dest="DateCreated", default=None, help="Only include recordings that were created on this date. Specify a date as `YYYY-MM-DD` in GMT, for example: `2009-07-06`, to read recordings that were created on this date. You can also specify an inequality, such as `DateCreated<=YYYY-MM-DD`, to read recordings that were created on or before midnight of this date, and `DateCreated>=YYYY-MM-DD` to read recordings that were created on or after midnight of this date.")
    p__2010_04_01_list_7.add_argument("--DateCreated<", dest="DateCreated", default=None, help="Only include recordings that were created on this date. Specify a date as `YYYY-MM-DD` in GMT, for example: `2009-07-06`, to read recordings that were created on this date. You can also specify an inequality, such as `DateCreated<=YYYY-MM-DD`, to read recordings that were created on or before midnight of this date, and `DateCreated>=YYYY-MM-DD` to read recordings that were created on or after midnight of this date.")
    p__2010_04_01_list_7.add_argument("--DateCreated>", dest="DateCreated", default=None, help="Only include recordings that were created on this date. Specify a date as `YYYY-MM-DD` in GMT, for example: `2009-07-06`, to read recordings that were created on this date. You can also specify an inequality, such as `DateCreated<=YYYY-MM-DD`, to read recordings that were created on or before midnight of this date, and `DateCreated>=YYYY-MM-DD` to read recordings that were created on or after midnight of this date.")
    p__2010_04_01_list_7.add_argument("--CallSid", dest="CallSid", default=None, help="The [Call](https://www.twilio.com/docs/voice/api/call-resource) SID of the resources to read.")
    p__2010_04_01_list_7.add_argument("--ConferenceSid", dest="ConferenceSid", default=None, help="The Conference SID that identifies the conference associated with the recording to read.")
    p__2010_04_01_list_7.add_argument("--IncludeSoftDeleted", dest="IncludeSoftDeleted", default=None, help="A boolean parameter indicating whether to retrieve soft deleted recordings or not. Recordings metadata are kept after deletion for a retention period of 40 days.")
    p__2010_04_01_list_7.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_7.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_7.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_7.set_defaults(func=cmd__2010_04_01_list_7)

    p__2010_04_01_fetchcall = sub__2010_04_01.add_parser("fetchcall", help="Fetch the call specified by the provided Call SID")
    p__2010_04_01_fetchcall.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_fetchcall.add_argument("Sid", help="Sid")
    p__2010_04_01_fetchcall.set_defaults(func=cmd__2010_04_01_fetchcall)

    p__2010_04_01_list_8 = sub__2010_04_01.add_parser("list-8", help="Retrieve a list of conferences belonging to the account used to make the request")
    p__2010_04_01_list_8.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_8.add_argument("--DateCreated", dest="DateCreated", default=None, help="The `date_created` value, specified as `YYYY-MM-DD`, of the resources to read. To read conferences that started on or before midnight on a date, use `<=YYYY-MM-DD`, and to specify  conferences that started on or after midnight on a date, use `>=YYYY-MM-DD`.")
    p__2010_04_01_list_8.add_argument("--DateCreated<", dest="DateCreated", default=None, help="The `date_created` value, specified as `YYYY-MM-DD`, of the resources to read. To read conferences that started on or before midnight on a date, use `<=YYYY-MM-DD`, and to specify  conferences that started on or after midnight on a date, use `>=YYYY-MM-DD`.")
    p__2010_04_01_list_8.add_argument("--DateCreated>", dest="DateCreated", default=None, help="The `date_created` value, specified as `YYYY-MM-DD`, of the resources to read. To read conferences that started on or before midnight on a date, use `<=YYYY-MM-DD`, and to specify  conferences that started on or after midnight on a date, use `>=YYYY-MM-DD`.")
    p__2010_04_01_list_8.add_argument("--DateUpdated", dest="DateUpdated", default=None, help="The `date_updated` value, specified as `YYYY-MM-DD`, of the resources to read. To read conferences that were last updated on or before midnight on a date, use `<=YYYY-MM-DD`, and to specify conferences that were last updated on or after midnight on a given date, use  `>=YYYY-MM-DD`.")
    p__2010_04_01_list_8.add_argument("--DateUpdated<", dest="DateUpdated", default=None, help="The `date_updated` value, specified as `YYYY-MM-DD`, of the resources to read. To read conferences that were last updated on or before midnight on a date, use `<=YYYY-MM-DD`, and to specify conferences that were last updated on or after midnight on a given date, use  `>=YYYY-MM-DD`.")
    p__2010_04_01_list_8.add_argument("--DateUpdated>", dest="DateUpdated", default=None, help="The `date_updated` value, specified as `YYYY-MM-DD`, of the resources to read. To read conferences that were last updated on or before midnight on a date, use `<=YYYY-MM-DD`, and to specify conferences that were last updated on or after midnight on a given date, use  `>=YYYY-MM-DD`.")
    p__2010_04_01_list_8.add_argument("--FriendlyName", dest="FriendlyName", default=None, help="The string that identifies the Conference resources to read.")
    p__2010_04_01_list_8.add_argument("--Status", dest="Status", default=None, help="The status of the resources to read. Can be: `init`, `in-progress`, or `completed`.")
    p__2010_04_01_list_8.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_8.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_8.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_8.set_defaults(func=cmd__2010_04_01_list_8)

    p__2010_04_01_list_9 = sub__2010_04_01.add_parser("list-9", help="Retrieve a list of connect-apps belonging to the account used to make the request")
    p__2010_04_01_list_9.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_9.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_9.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_9.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_9.set_defaults(func=cmd__2010_04_01_list_9)

    p__2010_04_01_list_10 = sub__2010_04_01.add_parser("list-10", help="Retrieve a list of domains belonging to the account used to make the request")
    p__2010_04_01_list_10.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_10.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_10.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_10.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_10.set_defaults(func=cmd__2010_04_01_list_10)

    p__2010_04_01_list_11 = sub__2010_04_01.add_parser("list-11", help="")
    p__2010_04_01_list_11.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_11.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_11.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_11.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_11.set_defaults(func=cmd__2010_04_01_list_11)

    p__2010_04_01_list_12 = sub__2010_04_01.add_parser("list-12", help="Retrieve a list of applications representing an application within the requesting account")
    p__2010_04_01_list_12.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_12.add_argument("--FriendlyName", dest="FriendlyName", default=None, help="The string that identifies the Application resources to read.")
    p__2010_04_01_list_12.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_12.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_12.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_12.set_defaults(func=cmd__2010_04_01_list_12)

    p__2010_04_01_fetchqueue = sub__2010_04_01.add_parser("fetchqueue", help="Fetch an instance of a queue identified by the QueueSid")
    p__2010_04_01_fetchqueue.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_fetchqueue.add_argument("Sid", help="Sid")
    p__2010_04_01_fetchqueue.set_defaults(func=cmd__2010_04_01_fetchqueue)

    p__2010_04_01_list_13 = sub__2010_04_01.add_parser("list-13", help="Retrieve a list of notifications belonging to the account used to make the request")
    p__2010_04_01_list_13.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_13.add_argument("--Log", dest="Log", default=None, help="Only read notifications of the specified log level. Can be:  `0` to read only ERROR notifications or `1` to read only WARNING notifications. By default, all notifications are read.")
    p__2010_04_01_list_13.add_argument("--MessageDate", dest="MessageDate", default=None, help="Only show notifications for the specified date, formatted as `YYYY-MM-DD`. You can also specify an inequality, such as `<=YYYY-MM-DD` for messages logged at or before midnight on a date, or `>=YYYY-MM-DD` for messages logged at or after midnight on a date.")
    p__2010_04_01_list_13.add_argument("--MessageDate<", dest="MessageDate", default=None, help="Only show notifications for the specified date, formatted as `YYYY-MM-DD`. You can also specify an inequality, such as `<=YYYY-MM-DD` for messages logged at or before midnight on a date, or `>=YYYY-MM-DD` for messages logged at or after midnight on a date.")
    p__2010_04_01_list_13.add_argument("--MessageDate>", dest="MessageDate", default=None, help="Only show notifications for the specified date, formatted as `YYYY-MM-DD`. You can also specify an inequality, such as `<=YYYY-MM-DD` for messages logged at or before midnight on a date, or `>=YYYY-MM-DD` for messages logged at or after midnight on a date.")
    p__2010_04_01_list_13.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_13.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_13.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_13.set_defaults(func=cmd__2010_04_01_list_13)

    p__2010_04_01_list_14 = sub__2010_04_01.add_parser("list-14", help="Retrieve a list of usage-records belonging to the account used to make the request")
    p__2010_04_01_list_14.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_14.add_argument("--Category", dest="Category", default=None, help="The [usage category](https://www.twilio.com/docs/usage/api/usage-record#usage-categories) of the UsageRecord resources to read. Only UsageRecord resources in the specified category are retrieved.")
    p__2010_04_01_list_14.add_argument("--StartDate", dest="StartDate", default=None, help="Only include usage that has occurred on or after this date. Specify the date in GMT and format as `YYYY-MM-DD`. You can also specify offsets from the current date, such as: `-30days`, which will set the start date to be 30 days before the current date.")
    p__2010_04_01_list_14.add_argument("--EndDate", dest="EndDate", default=None, help="Only include usage that occurred on or before this date. Specify the date in GMT and format as `YYYY-MM-DD`.  You can also specify offsets from the current date, such as: `+30days`, which will set the end date to 30 days from the current date.")
    p__2010_04_01_list_14.add_argument("--IncludeSubaccounts", dest="IncludeSubaccounts", default=None, help="Whether to include usage from the master account and all its subaccounts. Can be: `true` (the default) to include usage from the master account and all subaccounts or `false` to retrieve usage from only the specified account.")
    p__2010_04_01_list_14.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_14.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_14.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_14.set_defaults(func=cmd__2010_04_01_list_14)

    p__2010_04_01_fetchmessage = sub__2010_04_01.add_parser("fetchmessage", help="Fetch a message belonging to the account used to make the request")
    p__2010_04_01_fetchmessage.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_fetchmessage.add_argument("Sid", help="Sid")
    p__2010_04_01_fetchmessage.set_defaults(func=cmd__2010_04_01_fetchmessage)

    p__2010_04_01_list_15 = sub__2010_04_01.add_parser("list-15", help="Retrieve a list of short-codes belonging to the account used to make the request")
    p__2010_04_01_list_15.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_15.add_argument("--FriendlyName", dest="FriendlyName", default=None, help="The string that identifies the ShortCode resources to read.")
    p__2010_04_01_list_15.add_argument("--ShortCode", dest="ShortCode", default=None, help="Only show the ShortCode resources that match this pattern. You can specify partial numbers and use '*' as a wildcard for any digit.")
    p__2010_04_01_list_15.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_15.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_15.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_15.set_defaults(func=cmd__2010_04_01_list_15)

    p__2010_04_01_list_16 = sub__2010_04_01.add_parser("list-16", help="Retrieve a list of transcriptions belonging to the account used to make the request")
    p__2010_04_01_list_16.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_16.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_16.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_16.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_16.set_defaults(func=cmd__2010_04_01_list_16)

    p__2010_04_01_list_17 = sub__2010_04_01.add_parser("list-17", help="Retrieve a list of usage-triggers belonging to the account used to make the request")
    p__2010_04_01_list_17.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_17.add_argument("--Recurring", dest="Recurring", default=None, help="The frequency of recurring UsageTriggers to read. Can be: `daily`, `monthly`, or `yearly` to read recurring UsageTriggers. An empty value or a value of `alltime` reads non-recurring UsageTriggers.")
    p__2010_04_01_list_17.add_argument("--TriggerBy", dest="TriggerBy", default=None, help="The trigger field of the UsageTriggers to read.  Can be: `count`, `usage`, or `price` as described in the [UsageRecords documentation](https://www.twilio.com/docs/usage/api/usage-record#usage-count-price).")
    p__2010_04_01_list_17.add_argument("--UsageCategory", dest="UsageCategory", default=None, help="The usage category of the UsageTriggers to read. Must be a supported [usage categories](https://www.twilio.com/docs/usage/api/usage-record#usage-categories).")
    p__2010_04_01_list_17.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_17.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_17.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_17.set_defaults(func=cmd__2010_04_01_list_17)

    p__2010_04_01_fetchaddress = sub__2010_04_01.add_parser("fetchaddress", help="")
    p__2010_04_01_fetchaddress.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_fetchaddress.add_argument("Sid", help="Sid")
    p__2010_04_01_fetchaddress.set_defaults(func=cmd__2010_04_01_fetchaddress)

    p__2010_04_01_fetchrecording = sub__2010_04_01.add_parser("fetchrecording", help="Fetch an instance of a recording")
    p__2010_04_01_fetchrecording.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_fetchrecording.add_argument("Sid", help="Sid")
    p__2010_04_01_fetchrecording.add_argument("--IncludeSoftDeleted", dest="IncludeSoftDeleted", default=None, help="A boolean parameter indicating whether to retrieve soft deleted recordings or not. Recordings metadata are kept after deletion for a retention period of 40 days.")
    p__2010_04_01_fetchrecording.set_defaults(func=cmd__2010_04_01_fetchrecording)

    p__2010_04_01_fetchconference = sub__2010_04_01.add_parser("fetchconference", help="Fetch an instance of a conference")
    p__2010_04_01_fetchconference.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_fetchconference.add_argument("Sid", help="Sid")
    p__2010_04_01_fetchconference.set_defaults(func=cmd__2010_04_01_fetchconference)

    p__2010_04_01_fetchconnectapp = sub__2010_04_01.add_parser("fetchconnectapp", help="Fetch an instance of a connect-app")
    p__2010_04_01_fetchconnectapp.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_fetchconnectapp.add_argument("Sid", help="Sid")
    p__2010_04_01_fetchconnectapp.set_defaults(func=cmd__2010_04_01_fetchconnectapp)

    p__2010_04_01_list_18 = sub__2010_04_01.add_parser("list-18", help="Retrieve a list of outgoing-caller-ids belonging to the account used to make the request")
    p__2010_04_01_list_18.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_list_18.add_argument("--PhoneNumber", dest="PhoneNumber", default=None, help="The phone number of the OutgoingCallerId resources to read.")
    p__2010_04_01_list_18.add_argument("--FriendlyName", dest="FriendlyName", default=None, help="The string that identifies the OutgoingCallerId resources to read.")
    p__2010_04_01_list_18.add_argument("--PageSize", dest="PageSize", default=None, help="How many resources to return in each list page. The default is 50, and the maximum is 1000.")
    p__2010_04_01_list_18.add_argument("--Page", dest="Page", default=None, help="The page index. This value is simply for client state.")
    p__2010_04_01_list_18.add_argument("--PageToken", dest="PageToken", default=None, help="The page token. This is provided by the API.")
    p__2010_04_01_list_18.set_defaults(func=cmd__2010_04_01_list_18)

    p__2010_04_01_fetchsipdomain = sub__2010_04_01.add_parser("fetchsipdomain", help="Fetch an instance of a Domain")
    p__2010_04_01_fetchsipdomain.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_fetchsipdomain.add_argument("Sid", help="Sid")
    p__2010_04_01_fetchsipdomain.set_defaults(func=cmd__2010_04_01_fetchsipdomain)

    p__2010_04_01_fetchsigningkey = sub__2010_04_01.add_parser("fetchsigningkey", help="")
    p__2010_04_01_fetchsigningkey.add_argument("AccountSid", help="AccountSid")
    p__2010_04_01_fetchsigningkey.add_argument("Sid", help="Sid")
    p__2010_04_01_fetchsigningkey.set_defaults(func=cmd__2010_04_01_fetchsigningkey)

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
