#!/usr/bin/env python3
"""
stripe CLI tool for Claude Code skill integration.
Provides access to the stripe-api API.
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
BASE_URL = _env.get("STRIPE_URL", "https://api.stripe.com/")
AUTH_TOKEN = _env.get("STRIPE_TOKEN", "")

_ssl_ctx = ssl.create_default_context()
if _env.get("STRIPE_VERIFY_SSL", "true").lower() == "false":
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
    """Make HTTP request to the stripe API."""
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
    """Verify connectivity to the stripe API."""
    if not BASE_URL:
        print(f"Error: STRIPE_URL not set", file=sys.stderr)
        sys.exit(1)
    status, body = make_request("/")
    if status == 0:
        print(f"Cannot connect to {BASE_URL}", file=sys.stderr)
        print(f"Error: {body}", file=sys.stderr)
        sys.exit(1)
    print(f"Connected to {BASE_URL} (HTTP {status})")


def cmd_account_get(args):
    """Retrieve account"""
    path = "/v1/account"
    params = {}
    if args.expand is not None:
        params["expand"] = args.expand
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


def cmd_accounts_get(args):
    """List all connected accounts"""
    path = "/v1/accounts"
    params = {}
    if args.created is not None:
        params["created"] = args.created
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
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
    """List secrets"""
    path = "/v1/apps/secrets"
    params = {}
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.scope is not None:
        params["scope"] = args.scope
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
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


def cmd_balance_get(args):
    """Retrieve balance"""
    path = "/v1/balance"
    params = {}
    if args.expand is not None:
        params["expand"] = args.expand
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


def cmd_charges_get(args):
    """List all charges"""
    path = "/v1/charges"
    params = {}
    if args.created is not None:
        params["created"] = args.created
    if args.customer is not None:
        params["customer"] = args.customer
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.payment_intent is not None:
        params["payment_intent"] = args.payment_intent
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
    if args.transfer_group is not None:
        params["transfer_group"] = args.transfer_group
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


def cmd_coupons_get(args):
    """List all coupons"""
    path = "/v1/coupons"
    params = {}
    if args.created is not None:
        params["created"] = args.created
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
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


def cmd_credit_notes_get(args):
    """List all credit notes"""
    path = "/v1/credit_notes"
    params = {}
    if args.created is not None:
        params["created"] = args.created
    if args.customer is not None:
        params["customer"] = args.customer
    if args.customer_account is not None:
        params["customer_account"] = args.customer_account
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.invoice is not None:
        params["invoice"] = args.invoice
    if args.limit is not None:
        params["limit"] = args.limit
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
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


def cmd_customers_get(args):
    """List all customers"""
    path = "/v1/customers"
    params = {}
    if args.created is not None:
        params["created"] = args.created
    if args.email is not None:
        params["email"] = args.email
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
    if args.test_clock is not None:
        params["test_clock"] = args.test_clock
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


def cmd_disputes_get(args):
    """List all disputes"""
    path = "/v1/disputes"
    params = {}
    if args.charge is not None:
        params["charge"] = args.charge
    if args.created is not None:
        params["created"] = args.created
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.payment_intent is not None:
        params["payment_intent"] = args.payment_intent
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
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


def cmd_events_get(args):
    """List all events"""
    path = "/v1/events"
    params = {}
    if args.created is not None:
        params["created"] = args.created
    if args.delivery_success is not None:
        params["delivery_success"] = args.delivery_success
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
    if args.type is not None:
        params["type"] = args.type
    if args.types is not None:
        params["types"] = args.types
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


def cmd_events_get_2(args):
    """Retrieve an event"""
    path = "/v1/events/{id}".replace("{id}", str(args.id))
    params = {}
    if args.expand is not None:
        params["expand"] = args.expand
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


def cmd_file_links_get(args):
    """List all file links"""
    path = "/v1/file_links"
    params = {}
    if args.created is not None:
        params["created"] = args.created
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.expired is not None:
        params["expired"] = args.expired
    if args.file is not None:
        params["file"] = args.file
    if args.limit is not None:
        params["limit"] = args.limit
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
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


def cmd_files_get(args):
    """List all files"""
    path = "/v1/files"
    params = {}
    if args.created is not None:
        params["created"] = args.created
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.purpose is not None:
        params["purpose"] = args.purpose
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
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


def cmd_files_get_2(args):
    """Retrieve a file"""
    path = "/v1/files/{file}".replace("{file}", str(args.file))
    params = {}
    if args.expand is not None:
        params["expand"] = args.expand
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


def cmd_invoiceitems_get(args):
    """List all invoice items"""
    path = "/v1/invoiceitems"
    params = {}
    if args.created is not None:
        params["created"] = args.created
    if args.customer is not None:
        params["customer"] = args.customer
    if args.customer_account is not None:
        params["customer_account"] = args.customer_account
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.invoice is not None:
        params["invoice"] = args.invoice
    if args.limit is not None:
        params["limit"] = args.limit
    if args.pending is not None:
        params["pending"] = args.pending
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
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


def cmd_invoices_get(args):
    """List all invoices"""
    path = "/v1/invoices"
    params = {}
    if args.collection_method is not None:
        params["collection_method"] = args.collection_method
    if args.created is not None:
        params["created"] = args.created
    if args.customer is not None:
        params["customer"] = args.customer
    if args.customer_account is not None:
        params["customer_account"] = args.customer_account
    if args.due_date is not None:
        params["due_date"] = args.due_date
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
    if args.status is not None:
        params["status"] = args.status
    if args.subscription is not None:
        params["subscription"] = args.subscription
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


def cmd_payouts_get(args):
    """List all payouts"""
    path = "/v1/payouts"
    params = {}
    if args.arrival_date is not None:
        params["arrival_date"] = args.arrival_date
    if args.created is not None:
        params["created"] = args.created
    if args.destination is not None:
        params["destination"] = args.destination
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
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


def cmd_plans_get(args):
    """List all plans"""
    path = "/v1/plans"
    params = {}
    if args.active is not None:
        params["active"] = args.active
    if args.created is not None:
        params["created"] = args.created
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.product is not None:
        params["product"] = args.product
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
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


def cmd_plans_get_2(args):
    """Retrieve a plan"""
    path = "/v1/plans/{plan}".replace("{plan}", str(args.plan))
    params = {}
    if args.expand is not None:
        params["expand"] = args.expand
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


def cmd_prices_get(args):
    """List all prices"""
    path = "/v1/prices"
    params = {}
    if args.active is not None:
        params["active"] = args.active
    if args.created is not None:
        params["created"] = args.created
    if args.currency is not None:
        params["currency"] = args.currency
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.lookup_keys is not None:
        params["lookup_keys"] = args.lookup_keys
    if args.product is not None:
        params["product"] = args.product
    if args.recurring is not None:
        params["recurring"] = args.recurring
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
    if args.type is not None:
        params["type"] = args.type
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


def cmd_products_get(args):
    """List all products"""
    path = "/v1/products"
    params = {}
    if args.active is not None:
        params["active"] = args.active
    if args.created is not None:
        params["created"] = args.created
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.ids is not None:
        params["ids"] = args.ids
    if args.limit is not None:
        params["limit"] = args.limit
    if args.shippable is not None:
        params["shippable"] = args.shippable
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
    if args.url is not None:
        params["url"] = args.url
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


def cmd_quotes_get(args):
    """List all quotes"""
    path = "/v1/quotes"
    params = {}
    if args.customer is not None:
        params["customer"] = args.customer
    if args.customer_account is not None:
        params["customer_account"] = args.customer_account
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
    if args.status is not None:
        params["status"] = args.status
    if args.test_clock is not None:
        params["test_clock"] = args.test_clock
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


def cmd_refunds_get(args):
    """List all refunds"""
    path = "/v1/refunds"
    params = {}
    if args.charge is not None:
        params["charge"] = args.charge
    if args.created is not None:
        params["created"] = args.created
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.payment_intent is not None:
        params["payment_intent"] = args.payment_intent
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
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


def cmd_reviews_get(args):
    """List all open reviews"""
    path = "/v1/reviews"
    params = {}
    if args.created is not None:
        params["created"] = args.created
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
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


def cmd_tax_get(args):
    """Retrieve settings"""
    path = "/v1/tax/settings"
    params = {}
    if args.expand is not None:
        params["expand"] = args.expand
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


def cmd_tax_codes_get(args):
    """List all tax codes"""
    path = "/v1/tax_codes"
    params = {}
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
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


def cmd_tax_ids_get(args):
    """List all tax IDs"""
    path = "/v1/tax_ids"
    params = {}
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.owner is not None:
        params["owner"] = args.owner
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
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


def cmd_tax_rates_get(args):
    """List all tax rates"""
    path = "/v1/tax_rates"
    params = {}
    if args.active is not None:
        params["active"] = args.active
    if args.created is not None:
        params["created"] = args.created
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.inclusive is not None:
        params["inclusive"] = args.inclusive
    if args.limit is not None:
        params["limit"] = args.limit
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
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


def cmd_topups_get(args):
    """List all top-ups"""
    path = "/v1/topups"
    params = {}
    if args.amount is not None:
        params["amount"] = args.amount
    if args.created is not None:
        params["created"] = args.created
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
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


def cmd_transfers_get(args):
    """List all transfers"""
    path = "/v1/transfers"
    params = {}
    if args.created is not None:
        params["created"] = args.created
    if args.destination is not None:
        params["destination"] = args.destination
    if args.ending_before is not None:
        params["ending_before"] = args.ending_before
    if args.expand is not None:
        params["expand"] = args.expand
    if args.limit is not None:
        params["limit"] = args.limit
    if args.starting_after is not None:
        params["starting_after"] = args.starting_after
    if args.transfer_group is not None:
        params["transfer_group"] = args.transfer_group
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
    parser = argparse.ArgumentParser(description="stripe CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- check ---
    subparsers.add_parser("check", help="Test API connectivity")

    # --- account ---
    parser_account = subparsers.add_parser("account", help="Account operations")
    sub_account = parser_account.add_subparsers(dest="account_action", help="account actions")

    p_account_get = sub_account.add_parser("get", help="Retrieve account")
    p_account_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_account_get.set_defaults(func=cmd_account_get)

    # --- accounts ---
    parser_accounts = subparsers.add_parser("accounts", help="Accounts operations")
    sub_accounts = parser_accounts.add_subparsers(dest="accounts_action", help="accounts actions")

    p_accounts_get = sub_accounts.add_parser("get", help="List all connected accounts")
    p_accounts_get.add_argument("--created", dest="created", default=None, help="Only return connected accounts that were created during the given date interval.")
    p_accounts_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_accounts_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_accounts_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_accounts_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_accounts_get.set_defaults(func=cmd_accounts_get)

    # --- apps ---
    parser_apps = subparsers.add_parser("apps", help="Apps operations")
    sub_apps = parser_apps.add_subparsers(dest="apps_action", help="apps actions")

    p_apps_get = sub_apps.add_parser("get", help="List secrets")
    p_apps_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_apps_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_apps_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_apps_get.add_argument("--scope", dest="scope", default=None, help="Specifies the scoping of the secret. Requests originating from UI extensions can only access account-scoped secrets or secrets scoped to their own user.")
    p_apps_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_apps_get.set_defaults(func=cmd_apps_get)

    # --- balance ---
    parser_balance = subparsers.add_parser("balance", help="Balance operations")
    sub_balance = parser_balance.add_subparsers(dest="balance_action", help="balance actions")

    p_balance_get = sub_balance.add_parser("get", help="Retrieve balance")
    p_balance_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_balance_get.set_defaults(func=cmd_balance_get)

    # --- charges ---
    parser_charges = subparsers.add_parser("charges", help="Charges operations")
    sub_charges = parser_charges.add_subparsers(dest="charges_action", help="charges actions")

    p_charges_get = sub_charges.add_parser("get", help="List all charges")
    p_charges_get.add_argument("--created", dest="created", default=None, help="Only return charges that were created during the given date interval.")
    p_charges_get.add_argument("--customer", dest="customer", default=None, help="Only return charges for the customer specified by this customer ID.")
    p_charges_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_charges_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_charges_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_charges_get.add_argument("--payment-intent", dest="payment_intent", default=None, help="Only return charges that were created by the PaymentIntent specified by this PaymentIntent ID.")
    p_charges_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_charges_get.add_argument("--transfer-group", dest="transfer_group", default=None, help="Only return charges for this transfer group, limited to 100.")
    p_charges_get.set_defaults(func=cmd_charges_get)

    # --- coupons ---
    parser_coupons = subparsers.add_parser("coupons", help="Coupons operations")
    sub_coupons = parser_coupons.add_subparsers(dest="coupons_action", help="coupons actions")

    p_coupons_get = sub_coupons.add_parser("get", help="List all coupons")
    p_coupons_get.add_argument("--created", dest="created", default=None, help="A filter on the list, based on the object `created` field. The value can be a string with an integer Unix timestamp, or it can be a dictionary with a number of different query options.")
    p_coupons_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_coupons_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_coupons_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_coupons_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_coupons_get.set_defaults(func=cmd_coupons_get)

    # --- credit-notes ---
    parser_credit_notes = subparsers.add_parser("credit-notes", help="Credit-Notes operations")
    sub_credit_notes = parser_credit_notes.add_subparsers(dest="credit_notes_action", help="credit-notes actions")

    p_credit_notes_get = sub_credit_notes.add_parser("get", help="List all credit notes")
    p_credit_notes_get.add_argument("--created", dest="created", default=None, help="Only return credit notes that were created during the given date interval.")
    p_credit_notes_get.add_argument("--customer", dest="customer", default=None, help="Only return credit notes for the customer specified by this customer ID.")
    p_credit_notes_get.add_argument("--customer-account", dest="customer_account", default=None, help="Only return credit notes for the account representing the customer specified by this account ID.")
    p_credit_notes_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_credit_notes_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_credit_notes_get.add_argument("--invoice", dest="invoice", default=None, help="Only return credit notes for the invoice specified by this invoice ID.")
    p_credit_notes_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_credit_notes_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_credit_notes_get.set_defaults(func=cmd_credit_notes_get)

    # --- customers ---
    parser_customers = subparsers.add_parser("customers", help="Customers operations")
    sub_customers = parser_customers.add_subparsers(dest="customers_action", help="customers actions")

    p_customers_get = sub_customers.add_parser("get", help="List all customers")
    p_customers_get.add_argument("--created", dest="created", default=None, help="Only return customers that were created during the given date interval.")
    p_customers_get.add_argument("--email", dest="email", default=None, help="A case-sensitive filter on the list based on the customer's `email` field. The value must be a string.")
    p_customers_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_customers_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_customers_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_customers_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_customers_get.add_argument("--test-clock", dest="test_clock", default=None, help="Provides a list of customers that are associated with the specified test clock. The response will not include customers with test clocks if this parameter is not set.")
    p_customers_get.set_defaults(func=cmd_customers_get)

    # --- disputes ---
    parser_disputes = subparsers.add_parser("disputes", help="Disputes operations")
    sub_disputes = parser_disputes.add_subparsers(dest="disputes_action", help="disputes actions")

    p_disputes_get = sub_disputes.add_parser("get", help="List all disputes")
    p_disputes_get.add_argument("--charge", dest="charge", default=None, help="Only return disputes associated to the charge specified by this charge ID.")
    p_disputes_get.add_argument("--created", dest="created", default=None, help="Only return disputes that were created during the given date interval.")
    p_disputes_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_disputes_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_disputes_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_disputes_get.add_argument("--payment-intent", dest="payment_intent", default=None, help="Only return disputes associated to the PaymentIntent specified by this PaymentIntent ID.")
    p_disputes_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_disputes_get.set_defaults(func=cmd_disputes_get)

    # --- events ---
    parser_events = subparsers.add_parser("events", help="Events operations")
    sub_events = parser_events.add_subparsers(dest="events_action", help="events actions")

    p_events_get = sub_events.add_parser("get", help="List all events")
    p_events_get.add_argument("--created", dest="created", default=None, help="Only return events that were created during the given date interval.")
    p_events_get.add_argument("--delivery-success", dest="delivery_success", default=None, help="Filter events by whether all webhooks were successfully delivered. If false, events which are still pending or have failed all delivery attempts to a webhook endpoint will be returned.")
    p_events_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_events_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_events_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_events_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_events_get.add_argument("--type", dest="type", default=None, help="A string containing a specific event name, or group of events using * as a wildcard. The list will be filtered to include only events with a matching event property.")
    p_events_get.add_argument("--types", dest="types", default=None, help="An array of up to 20 strings containing specific event names. The list will be filtered to include only events with a matching event property. You may pass either `type` or `types`, but not both.")
    p_events_get.set_defaults(func=cmd_events_get)

    p_events_get_2 = sub_events.add_parser("get-2", help="Retrieve an event")
    p_events_get_2.add_argument("id", help="id")
    p_events_get_2.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_events_get_2.set_defaults(func=cmd_events_get_2)

    # --- file-links ---
    parser_file_links = subparsers.add_parser("file-links", help="File-Links operations")
    sub_file_links = parser_file_links.add_subparsers(dest="file_links_action", help="file-links actions")

    p_file_links_get = sub_file_links.add_parser("get", help="List all file links")
    p_file_links_get.add_argument("--created", dest="created", default=None, help="Only return links that were created during the given date interval.")
    p_file_links_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_file_links_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_file_links_get.add_argument("--expired", dest="expired", default=None, help="Filter links by their expiration status. By default, Stripe returns all links.")
    p_file_links_get.add_argument("--file", dest="file", default=None, help="Only return links for the given file.")
    p_file_links_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_file_links_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_file_links_get.set_defaults(func=cmd_file_links_get)

    # --- files ---
    parser_files = subparsers.add_parser("files", help="Files operations")
    sub_files = parser_files.add_subparsers(dest="files_action", help="files actions")

    p_files_get = sub_files.add_parser("get", help="List all files")
    p_files_get.add_argument("--created", dest="created", default=None, help="Only return files that were created during the given date interval.")
    p_files_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_files_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_files_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_files_get.add_argument("--purpose", dest="purpose", default=None, help="Filter queries by the file purpose. If you don't provide a purpose, the queries return unfiltered files.")
    p_files_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_files_get.set_defaults(func=cmd_files_get)

    p_files_get_2 = sub_files.add_parser("get-2", help="Retrieve a file")
    p_files_get_2.add_argument("file", help="file")
    p_files_get_2.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_files_get_2.set_defaults(func=cmd_files_get_2)

    # --- invoiceitems ---
    parser_invoiceitems = subparsers.add_parser("invoiceitems", help="Invoiceitems operations")
    sub_invoiceitems = parser_invoiceitems.add_subparsers(dest="invoiceitems_action", help="invoiceitems actions")

    p_invoiceitems_get = sub_invoiceitems.add_parser("get", help="List all invoice items")
    p_invoiceitems_get.add_argument("--created", dest="created", default=None, help="Only return invoice items that were created during the given date interval.")
    p_invoiceitems_get.add_argument("--customer", dest="customer", default=None, help="The identifier of the customer whose invoice items to return. If none is provided, returns all invoice items.")
    p_invoiceitems_get.add_argument("--customer-account", dest="customer_account", default=None, help="The identifier of the account representing the customer whose invoice items to return. If none is provided, returns all invoice items.")
    p_invoiceitems_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_invoiceitems_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_invoiceitems_get.add_argument("--invoice", dest="invoice", default=None, help="Only return invoice items belonging to this invoice. If none is provided, all invoice items will be returned. If specifying an invoice, no customer identifier is needed.")
    p_invoiceitems_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_invoiceitems_get.add_argument("--pending", dest="pending", default=None, help="Set to `true` to only show pending invoice items, which are not yet attached to any invoices. Set to `false` to only show invoice items already attached to invoices. If unspecified, no filter is applied.")
    p_invoiceitems_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_invoiceitems_get.set_defaults(func=cmd_invoiceitems_get)

    # --- invoices ---
    parser_invoices = subparsers.add_parser("invoices", help="Invoices operations")
    sub_invoices = parser_invoices.add_subparsers(dest="invoices_action", help="invoices actions")

    p_invoices_get = sub_invoices.add_parser("get", help="List all invoices")
    p_invoices_get.add_argument("--collection-method", dest="collection_method", default=None, help="The collection method of the invoice to retrieve. Either `charge_automatically` or `send_invoice`.")
    p_invoices_get.add_argument("--created", dest="created", default=None, help="Only return invoices that were created during the given date interval.")
    p_invoices_get.add_argument("--customer", dest="customer", default=None, help="Only return invoices for the customer specified by this customer ID.")
    p_invoices_get.add_argument("--customer-account", dest="customer_account", default=None, help="Only return invoices for the account representing the customer specified by this account ID.")
    p_invoices_get.add_argument("--due-date", dest="due_date", default=None, help="")
    p_invoices_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_invoices_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_invoices_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_invoices_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_invoices_get.add_argument("--status", dest="status", default=None, help="The status of the invoice, one of `draft`, `open`, `paid`, `uncollectible`, or `void`. [Learn more](https://docs.stripe.com/billing/invoices/workflow#workflow-overview)")
    p_invoices_get.add_argument("--subscription", dest="subscription", default=None, help="Only return invoices for the subscription specified by this subscription ID.")
    p_invoices_get.set_defaults(func=cmd_invoices_get)

    # --- payouts ---
    parser_payouts = subparsers.add_parser("payouts", help="Payouts operations")
    sub_payouts = parser_payouts.add_subparsers(dest="payouts_action", help="payouts actions")

    p_payouts_get = sub_payouts.add_parser("get", help="List all payouts")
    p_payouts_get.add_argument("--arrival-date", dest="arrival_date", default=None, help="Only return payouts that are expected to arrive during the given date interval.")
    p_payouts_get.add_argument("--created", dest="created", default=None, help="Only return payouts that were created during the given date interval.")
    p_payouts_get.add_argument("--destination", dest="destination", default=None, help="The ID of an external account - only return payouts sent to this external account.")
    p_payouts_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_payouts_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_payouts_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_payouts_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_payouts_get.add_argument("--status", dest="status", default=None, help="Only return payouts that have the given status: `pending`, `paid`, `failed`, or `canceled`.")
    p_payouts_get.set_defaults(func=cmd_payouts_get)

    # --- plans ---
    parser_plans = subparsers.add_parser("plans", help="Plans operations")
    sub_plans = parser_plans.add_subparsers(dest="plans_action", help="plans actions")

    p_plans_get = sub_plans.add_parser("get", help="List all plans")
    p_plans_get.add_argument("--active", dest="active", default=None, help="Only return plans that are active or inactive (e.g., pass `false` to list all inactive plans).")
    p_plans_get.add_argument("--created", dest="created", default=None, help="A filter on the list, based on the object `created` field. The value can be a string with an integer Unix timestamp, or it can be a dictionary with a number of different query options.")
    p_plans_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_plans_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_plans_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_plans_get.add_argument("--product", dest="product", default=None, help="Only return plans for the given product.")
    p_plans_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_plans_get.set_defaults(func=cmd_plans_get)

    p_plans_get_2 = sub_plans.add_parser("get-2", help="Retrieve a plan")
    p_plans_get_2.add_argument("plan", help="plan")
    p_plans_get_2.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_plans_get_2.set_defaults(func=cmd_plans_get_2)

    # --- prices ---
    parser_prices = subparsers.add_parser("prices", help="Prices operations")
    sub_prices = parser_prices.add_subparsers(dest="prices_action", help="prices actions")

    p_prices_get = sub_prices.add_parser("get", help="List all prices")
    p_prices_get.add_argument("--active", dest="active", default=None, help="Only return prices that are active or inactive (e.g., pass `false` to list all inactive prices).")
    p_prices_get.add_argument("--created", dest="created", default=None, help="A filter on the list, based on the object `created` field. The value can be a string with an integer Unix timestamp, or it can be a dictionary with a number of different query options.")
    p_prices_get.add_argument("--currency", dest="currency", default=None, help="Only return prices for the given currency.")
    p_prices_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_prices_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_prices_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_prices_get.add_argument("--lookup-keys", dest="lookup_keys", default=None, help="Only return the price with these lookup_keys, if any exist. You can specify up to 10 lookup_keys.")
    p_prices_get.add_argument("--product", dest="product", default=None, help="Only return prices for the given product.")
    p_prices_get.add_argument("--recurring", dest="recurring", default=None, help="Only return prices with these recurring fields.")
    p_prices_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_prices_get.add_argument("--type", dest="type", default=None, help="Only return prices of type `recurring` or `one_time`.")
    p_prices_get.set_defaults(func=cmd_prices_get)

    # --- products ---
    parser_products = subparsers.add_parser("products", help="Products operations")
    sub_products = parser_products.add_subparsers(dest="products_action", help="products actions")

    p_products_get = sub_products.add_parser("get", help="List all products")
    p_products_get.add_argument("--active", dest="active", default=None, help="Only return products that are active or inactive (e.g., pass `false` to list all inactive products).")
    p_products_get.add_argument("--created", dest="created", default=None, help="Only return products that were created during the given date interval.")
    p_products_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_products_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_products_get.add_argument("--ids", dest="ids", default=None, help="Only return products with the given IDs. Cannot be used with [starting_after](https://api.stripe.com#list_products-starting_after) or [ending_before](https://api.stripe.com#list_products-ending_before).")
    p_products_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_products_get.add_argument("--shippable", dest="shippable", default=None, help="Only return products that can be shipped (i.e., physical, not digital products).")
    p_products_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_products_get.add_argument("--url", dest="url", default=None, help="Only return products with the given url.")
    p_products_get.set_defaults(func=cmd_products_get)

    # --- quotes ---
    parser_quotes = subparsers.add_parser("quotes", help="Quotes operations")
    sub_quotes = parser_quotes.add_subparsers(dest="quotes_action", help="quotes actions")

    p_quotes_get = sub_quotes.add_parser("get", help="List all quotes")
    p_quotes_get.add_argument("--customer", dest="customer", default=None, help="The ID of the customer whose quotes you're retrieving.")
    p_quotes_get.add_argument("--customer-account", dest="customer_account", default=None, help="The ID of the account representing the customer whose quotes you're retrieving.")
    p_quotes_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_quotes_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_quotes_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_quotes_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_quotes_get.add_argument("--status", dest="status", default=None, help="The status of the quote.")
    p_quotes_get.add_argument("--test-clock", dest="test_clock", default=None, help="Provides a list of quotes that are associated with the specified test clock. The response will not include quotes with test clocks if this and the customer parameter is not set.")
    p_quotes_get.set_defaults(func=cmd_quotes_get)

    # --- refunds ---
    parser_refunds = subparsers.add_parser("refunds", help="Refunds operations")
    sub_refunds = parser_refunds.add_subparsers(dest="refunds_action", help="refunds actions")

    p_refunds_get = sub_refunds.add_parser("get", help="List all refunds")
    p_refunds_get.add_argument("--charge", dest="charge", default=None, help="Only return refunds for the charge specified by this charge ID.")
    p_refunds_get.add_argument("--created", dest="created", default=None, help="Only return refunds that were created during the given date interval.")
    p_refunds_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_refunds_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_refunds_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_refunds_get.add_argument("--payment-intent", dest="payment_intent", default=None, help="Only return refunds for the PaymentIntent specified by this ID.")
    p_refunds_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_refunds_get.set_defaults(func=cmd_refunds_get)

    # --- reviews ---
    parser_reviews = subparsers.add_parser("reviews", help="Reviews operations")
    sub_reviews = parser_reviews.add_subparsers(dest="reviews_action", help="reviews actions")

    p_reviews_get = sub_reviews.add_parser("get", help="List all open reviews")
    p_reviews_get.add_argument("--created", dest="created", default=None, help="Only return reviews that were created during the given date interval.")
    p_reviews_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_reviews_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_reviews_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_reviews_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_reviews_get.set_defaults(func=cmd_reviews_get)

    # --- tax ---
    parser_tax = subparsers.add_parser("tax", help="Tax operations")
    sub_tax = parser_tax.add_subparsers(dest="tax_action", help="tax actions")

    p_tax_get = sub_tax.add_parser("get", help="Retrieve settings")
    p_tax_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_tax_get.set_defaults(func=cmd_tax_get)

    # --- tax-codes ---
    parser_tax_codes = subparsers.add_parser("tax-codes", help="Tax-Codes operations")
    sub_tax_codes = parser_tax_codes.add_subparsers(dest="tax_codes_action", help="tax-codes actions")

    p_tax_codes_get = sub_tax_codes.add_parser("get", help="List all tax codes")
    p_tax_codes_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_tax_codes_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_tax_codes_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_tax_codes_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_tax_codes_get.set_defaults(func=cmd_tax_codes_get)

    # --- tax-ids ---
    parser_tax_ids = subparsers.add_parser("tax-ids", help="Tax-Ids operations")
    sub_tax_ids = parser_tax_ids.add_subparsers(dest="tax_ids_action", help="tax-ids actions")

    p_tax_ids_get = sub_tax_ids.add_parser("get", help="List all tax IDs")
    p_tax_ids_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_tax_ids_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_tax_ids_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_tax_ids_get.add_argument("--owner", dest="owner", default=None, help="The account or customer the tax ID belongs to. Defaults to `owner[type]=self`.")
    p_tax_ids_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_tax_ids_get.set_defaults(func=cmd_tax_ids_get)

    # --- tax-rates ---
    parser_tax_rates = subparsers.add_parser("tax-rates", help="Tax-Rates operations")
    sub_tax_rates = parser_tax_rates.add_subparsers(dest="tax_rates_action", help="tax-rates actions")

    p_tax_rates_get = sub_tax_rates.add_parser("get", help="List all tax rates")
    p_tax_rates_get.add_argument("--active", dest="active", default=None, help="Optional flag to filter by tax rates that are either active or inactive (archived).")
    p_tax_rates_get.add_argument("--created", dest="created", default=None, help="Optional range for filtering created date.")
    p_tax_rates_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_tax_rates_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_tax_rates_get.add_argument("--inclusive", dest="inclusive", default=None, help="Optional flag to filter by tax rates that are inclusive (or those that are not inclusive).")
    p_tax_rates_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_tax_rates_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_tax_rates_get.set_defaults(func=cmd_tax_rates_get)

    # --- topups ---
    parser_topups = subparsers.add_parser("topups", help="Topups operations")
    sub_topups = parser_topups.add_subparsers(dest="topups_action", help="topups actions")

    p_topups_get = sub_topups.add_parser("get", help="List all top-ups")
    p_topups_get.add_argument("--amount", dest="amount", default=None, help="A positive integer representing how much to transfer.")
    p_topups_get.add_argument("--created", dest="created", default=None, help="A filter on the list, based on the object `created` field. The value can be a string with an integer Unix timestamp, or it can be a dictionary with a number of different query options.")
    p_topups_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_topups_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_topups_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_topups_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_topups_get.add_argument("--status", dest="status", default=None, help="Only return top-ups that have the given status. One of `canceled`, `failed`, `pending` or `succeeded`.")
    p_topups_get.set_defaults(func=cmd_topups_get)

    # --- transfers ---
    parser_transfers = subparsers.add_parser("transfers", help="Transfers operations")
    sub_transfers = parser_transfers.add_subparsers(dest="transfers_action", help="transfers actions")

    p_transfers_get = sub_transfers.add_parser("get", help="List all transfers")
    p_transfers_get.add_argument("--created", dest="created", default=None, help="Only return transfers that were created during the given date interval.")
    p_transfers_get.add_argument("--destination", dest="destination", default=None, help="Only return transfers for the destination specified by this account ID.")
    p_transfers_get.add_argument("--ending-before", dest="ending_before", default=None, help="A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.")
    p_transfers_get.add_argument("--expand", dest="expand", default=None, help="Specifies which fields in the response should be expanded.")
    p_transfers_get.add_argument("--limit", dest="limit", default=None, help="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.")
    p_transfers_get.add_argument("--starting-after", dest="starting_after", default=None, help="A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.")
    p_transfers_get.add_argument("--transfer-group", dest="transfer_group", default=None, help="Only return transfers with the specified transfer group.")
    p_transfers_get.set_defaults(func=cmd_transfers_get)

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
