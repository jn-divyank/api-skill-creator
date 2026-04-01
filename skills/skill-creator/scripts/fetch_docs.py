#!/usr/bin/env python3
"""
fetch_docs.py — Fetch and parse API documentation into a structured JSON spec.

Supports: OpenAPI 3.x (JSON/YAML), Swagger 2.0 (JSON/YAML), Postman v2,
          DeepWiki pages, generic HTML, local files.

Usage:
    python3 fetch_docs.py <URL_or_FILE>
    python3 fetch_docs.py https://petstore.swagger.io/v2/swagger.json
    python3 fetch_docs.py ./my-api-spec.json
"""

import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

# ---------------------------------------------------------------------------
# YAML support — optional dependency
# ---------------------------------------------------------------------------
try:
    import yaml

    def _parse_yaml(text):
        return yaml.safe_load(text)
except ImportError:
    yaml = None

    def _parse_yaml(text):
        """Minimal YAML-ish parser for simple OpenAPI specs (no anchors/aliases)."""
        # Try JSON first — many .yaml URLs actually serve JSON
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            pass
        print(
            "Warning: pyyaml not installed. YAML parsing is limited. "
            "Install with: pip install pyyaml",
            file=sys.stderr,
        )
        return _basic_yaml_parse(text)


def _basic_yaml_parse(text):
    """Best-effort YAML→dict for flat/simple OpenAPI specs."""
    result = {}
    current_key = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m = re.match(r'^(\w[\w\-]*):\s*(.*)', stripped)
        if m:
            current_key = m.group(1)
            val = m.group(2).strip()
            if val:
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                elif val.startswith("'") and val.endswith("'"):
                    val = val[1:-1]
                result[current_key] = val
            else:
                result[current_key] = {}
    return result


# ---------------------------------------------------------------------------
# HTTP fetching
# ---------------------------------------------------------------------------
_SSL_CTX = ssl.create_default_context()
_SSL_CTX_NOVERIFY = ssl.create_default_context()
_SSL_CTX_NOVERIFY.check_hostname = False
_SSL_CTX_NOVERIFY.verify_mode = ssl.CERT_NONE


def fetch_url(url, timeout=30):
    """Fetch URL content. Follows redirects, retries once on 429, falls back to no-verify SSL."""
    headers = {
        "User-Agent": "skill-creator/1.0",
        "Accept": "application/json, text/yaml, text/html, */*",
    }
    req = urllib.request.Request(url, headers=headers)

    for attempt in range(2):
        ctx = _SSL_CTX if attempt == 0 else _SSL_CTX_NOVERIFY
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                content_type = resp.headers.get("Content-Type", "")
                data = resp.read().decode("utf-8", errors="replace")
                return data, content_type, resp.geturl()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 0:
                import time
                time.sleep(2)
                continue
            raise
        except ssl.SSLError:
            if attempt == 0:
                print("Warning: SSL verification failed, retrying without verification", file=sys.stderr)
                continue
            raise
        except urllib.error.URLError as e:
            if "CERTIFICATE_VERIFY_FAILED" in str(e) and attempt == 0:
                print("Warning: SSL verification failed, retrying without verification", file=sys.stderr)
                continue
            raise
    raise RuntimeError("Failed to fetch URL after retries")


def read_local_file(path):
    """Read a local file and return (content, guessed_content_type)."""
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    ext = os.path.splitext(path)[1].lower()
    ct_map = {
        ".json": "application/json",
        ".yaml": "text/yaml",
        ".yml": "text/yaml",
        ".html": "text/html",
        ".htm": "text/html",
    }
    return data, ct_map.get(ext, "text/plain"), path


# ---------------------------------------------------------------------------
# Format detection
# ---------------------------------------------------------------------------
def detect_format(data, content_type, url):
    """Return one of: openapi3, swagger2, postman, deepwiki, yaml, html, unknown."""
    # DeepWiki detection by hostname
    parsed = urllib.parse.urlparse(url) if url.startswith("http") else None
    if parsed and "deepwiki.com" in (parsed.hostname or ""):
        return "deepwiki"

    # Try JSON parse
    try:
        obj = json.loads(data)
        if isinstance(obj, dict):
            if obj.get("openapi", "").startswith("3."):
                return "openapi3"
            if obj.get("swagger", "").startswith("2."):
                return "swagger2"
            if obj.get("info", {}).get("schema", "").startswith("https://schema.getpostman.com"):
                return "postman"
            # Postman v2 alternative detection
            if "item" in obj and "info" in obj:
                info = obj["info"]
                if "_postman_id" in info or "schema" in info:
                    return "postman"
            # Generic JSON that looks like OpenAPI
            if "paths" in obj and ("info" in obj or "servers" in obj):
                return "openapi3"
        return "unknown"
    except (json.JSONDecodeError, ValueError):
        pass

    # Check for YAML-like content
    if any(k in content_type.lower() for k in ("yaml", "yml")) or url.endswith((".yaml", ".yml")):
        return "yaml"

    # Try YAML parse
    if _is_likely_yaml(data):
        return "yaml"

    # HTML
    if "<html" in data.lower()[:500] or "text/html" in content_type.lower():
        return "html"

    return "unknown"


def _is_likely_yaml(data):
    """Heuristic: looks like YAML if it has key: value lines and no < html tags."""
    lines = data.strip().splitlines()[:20]
    yaml_like = sum(1 for l in lines if re.match(r'^\w[\w\-]*:', l))
    html_like = sum(1 for l in lines if "<" in l)
    return yaml_like >= 3 and html_like == 0


# ---------------------------------------------------------------------------
# OpenAPI 3.x parser
# ---------------------------------------------------------------------------
def parse_openapi3(data):
    """Parse OpenAPI 3.x spec (JSON string or dict) into our intermediate format."""
    spec = json.loads(data) if isinstance(data, str) else data

    info = spec.get("info", {})
    service_name = _slugify(info.get("title", "api"))

    # Base URL
    servers = spec.get("servers", [])
    base_url = servers[0].get("url", "") if servers else ""

    # Auth
    auth_type, auth_header = _extract_auth_openapi3(spec)

    # Endpoints
    endpoints = []
    for path, methods in spec.get("paths", {}).items():
        for method, op in methods.items():
            if method.lower() in ("get", "post", "put", "patch", "delete", "head", "options"):
                if isinstance(op, dict):
                    tags = op.get("tags", [])
                    params = _extract_params(op)
                    body_fields = _extract_request_body(op)
                    endpoints.append({
                        "method": method.upper(),
                        "path": path,
                        "summary": op.get("summary", op.get("description", "")),
                        "tags": tags,
                        "parameters": params,
                        "body_fields": body_fields,
                        "operation_id": op.get("operationId", ""),
                    })

    endpoints = _rank_and_limit(endpoints)

    env_prefix = service_name.upper().replace("-", "_")
    env_vars = [f"{env_prefix}_URL", f"{env_prefix}_TOKEN"]

    return {
        "service_name": service_name,
        "base_url": base_url,
        "auth_type": auth_type,
        "auth_header_format": auth_header,
        "env_vars_needed": env_vars,
        "endpoints": endpoints,
        "source_format": "openapi3",
    }


def _extract_auth_openapi3(spec):
    """Extract authentication scheme from OpenAPI 3.x securitySchemes."""
    components = spec.get("components", {})
    schemes = components.get("securitySchemes", {})

    for name, scheme in schemes.items():
        scheme_type = scheme.get("type", "")
        if scheme_type == "http":
            sub = scheme.get("scheme", "bearer").lower()
            if sub == "bearer":
                return "bearer", "Bearer {token}"
            elif sub == "basic":
                return "basic", "Basic {base64(user:pass)}"
        elif scheme_type == "apiKey":
            loc = scheme.get("in", "header")
            key_name = scheme.get("name", "X-API-Key")
            if loc == "header":
                return "api_key", f"{key_name}: {{token}}"
            else:
                return "api_key_query", f"?{key_name}={{token}}"
        elif scheme_type == "oauth2":
            return "bearer", "Bearer {token}"

    return "bearer", "Bearer {token}"


def _extract_params(operation):
    """Extract path/query parameters from an operation."""
    params = []
    for p in operation.get("parameters", []):
        params.append({
            "name": p.get("name", ""),
            "in": p.get("in", "query"),
            "required": p.get("required", False),
            "description": p.get("description", ""),
        })
    return params


def _extract_request_body(operation):
    """Extract request body field names from OpenAPI 3.x operation."""
    body = operation.get("requestBody", {})
    if not body:
        return []
    content = body.get("content", {})
    for ct, media in content.items():
        schema = media.get("schema", {})
        # Resolve top-level $ref to a descriptive placeholder
        if "$ref" in schema and not schema.get("properties"):
            ref_name = schema["$ref"].split("/")[-1]
            return [{"name": "body", "required": True, "type": ref_name}]
        props = schema.get("properties", {})
        if props:
            return [
                {"name": k, "required": k in schema.get("required", []), "type": v.get("type", "")}
                for k, v in props.items()
            ]
        # Array type
        if schema.get("type") == "array":
            return [{"name": "items", "required": True, "type": "array"}]
    return []


# ---------------------------------------------------------------------------
# Swagger 2.0 parser
# ---------------------------------------------------------------------------
def parse_swagger2(data):
    """Parse Swagger 2.0 spec into our intermediate format."""
    spec = json.loads(data) if isinstance(data, str) else data

    info = spec.get("info", {})
    service_name = _slugify(info.get("title", "api"))

    # Base URL
    host = spec.get("host", "")
    base_path = spec.get("basePath", "")
    schemes = spec.get("schemes", ["https"])
    scheme = schemes[0] if schemes else "https"
    base_url = f"{scheme}://{host}{base_path}" if host else ""

    # Auth
    auth_type, auth_header = _extract_auth_swagger2(spec)

    # Endpoints
    endpoints = []
    for path, methods in spec.get("paths", {}).items():
        for method, op in methods.items():
            if method.lower() in ("get", "post", "put", "patch", "delete", "head", "options"):
                if isinstance(op, dict):
                    tags = op.get("tags", [])
                    params = []
                    body_fields = []
                    for p in op.get("parameters", []):
                        if p.get("in") == "body":
                            schema = p.get("schema", {})
                            props = schema.get("properties", {})
                            body_fields = [
                                {"name": k, "required": k in schema.get("required", []), "type": v.get("type", "")}
                                for k, v in props.items()
                            ]
                        else:
                            params.append({
                                "name": p.get("name", ""),
                                "in": p.get("in", "query"),
                                "required": p.get("required", False),
                                "description": p.get("description", ""),
                            })
                    endpoints.append({
                        "method": method.upper(),
                        "path": path,
                        "summary": op.get("summary", op.get("description", "")),
                        "tags": tags,
                        "parameters": params,
                        "body_fields": body_fields,
                        "operation_id": op.get("operationId", ""),
                    })

    endpoints = _rank_and_limit(endpoints)

    env_prefix = service_name.upper().replace("-", "_")
    env_vars = [f"{env_prefix}_URL", f"{env_prefix}_TOKEN"]

    return {
        "service_name": service_name,
        "base_url": base_url,
        "auth_type": auth_type,
        "auth_header_format": auth_header,
        "env_vars_needed": env_vars,
        "endpoints": endpoints,
        "source_format": "swagger2",
    }


def _extract_auth_swagger2(spec):
    """Extract authentication from Swagger 2.0 securityDefinitions."""
    defs = spec.get("securityDefinitions", {})
    for name, defn in defs.items():
        dtype = defn.get("type", "")
        if dtype == "apiKey":
            loc = defn.get("in", "header")
            key_name = defn.get("name", "api_key")
            if loc == "header":
                return "api_key", f"{key_name}: {{token}}"
            else:
                return "api_key_query", f"?{key_name}={{token}}"
        elif dtype == "oauth2":
            return "bearer", "Bearer {token}"
        elif dtype == "basic":
            return "basic", "Basic {base64(user:pass)}"

    return "bearer", "Bearer {token}"


# ---------------------------------------------------------------------------
# YAML spec parser (OpenAPI in YAML format)
# ---------------------------------------------------------------------------
def parse_yaml_spec(data):
    """Parse a YAML OpenAPI/Swagger spec."""
    if yaml is None:
        print(
            "Error: pyyaml is required to parse YAML specs.\n"
            "Install it with: pip3 install pyyaml\n"
            "Then re-run this command.",
            file=sys.stderr,
        )
        sys.exit(1)

    obj = _parse_yaml(data)
    if not isinstance(obj, dict):
        print("Error: YAML did not parse to a dictionary", file=sys.stderr)
        sys.exit(1)

    if obj.get("openapi", "").startswith("3."):
        return parse_openapi3(obj)
    elif obj.get("swagger", "").startswith("2."):
        return parse_swagger2(obj)
    else:
        # Try as OpenAPI 3 anyway if it has paths
        if "paths" in obj:
            return parse_openapi3(obj)
        print("Error: YAML file does not appear to be an OpenAPI or Swagger spec", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Postman Collection v2 parser
# ---------------------------------------------------------------------------
def parse_postman(data):
    """Parse Postman Collection v2.x into our intermediate format."""
    spec = json.loads(data) if isinstance(data, str) else data

    info = spec.get("info", {})
    service_name = _slugify(info.get("name", "api"))

    # Flatten Postman items (may be nested in folders)
    items = _flatten_postman_items(spec.get("item", []))

    endpoints = []
    base_urls = set()

    for item in items:
        req = item.get("request", {})
        if not req:
            continue

        method = req.get("method", "GET").upper()
        url_obj = req.get("url", {})
        if isinstance(url_obj, str):
            url_str = url_obj
            path = urllib.parse.urlparse(url_str).path
        else:
            raw = url_obj.get("raw", "")
            host = ".".join(url_obj.get("host", []))
            path_parts = url_obj.get("path", [])
            path = "/" + "/".join(path_parts) if path_parts else ""
            if host:
                base_urls.add(f"https://{host}")

        # Determine tags from folder structure
        tags = []
        folder = item.get("_folder", "")
        if folder:
            tags.append(folder.lower())

        # Parameters
        params = []
        if isinstance(url_obj, dict):
            for q in url_obj.get("query", []):
                params.append({
                    "name": q.get("key", ""),
                    "in": "query",
                    "required": False,
                    "description": q.get("description", ""),
                })
            for v in url_obj.get("variable", []):
                params.append({
                    "name": v.get("key", ""),
                    "in": "path",
                    "required": True,
                    "description": v.get("description", ""),
                })

        # Body fields
        body_fields = []
        body = req.get("body", {})
        if body and body.get("mode") == "raw":
            try:
                raw_json = json.loads(body.get("raw", "{}"))
                if isinstance(raw_json, dict):
                    body_fields = [
                        {"name": k, "required": True, "type": type(v).__name__}
                        for k, v in raw_json.items()
                    ]
            except (json.JSONDecodeError, ValueError):
                pass

        # Convert Postman path variables from :var to {var}
        path = re.sub(r':(\w+)', r'{\1}', path)

        endpoints.append({
            "method": method,
            "path": path,
            "summary": item.get("name", ""),
            "tags": tags,
            "parameters": params,
            "body_fields": body_fields,
            "operation_id": "",
        })

    endpoints = _rank_and_limit(endpoints)
    base_url = base_urls.pop() if base_urls else ""

    # Auth detection from collection-level auth
    auth_type, auth_header = "bearer", "Bearer {token}"
    coll_auth = spec.get("auth", {})
    if coll_auth:
        atype = coll_auth.get("type", "")
        if atype == "apikey":
            auth_type, auth_header = "api_key", "X-API-Key: {token}"
        elif atype == "basic":
            auth_type, auth_header = "basic", "Basic {base64(user:pass)}"

    env_prefix = service_name.upper().replace("-", "_")
    env_vars = [f"{env_prefix}_URL", f"{env_prefix}_TOKEN"]

    return {
        "service_name": service_name,
        "base_url": base_url,
        "auth_type": auth_type,
        "auth_header_format": auth_header,
        "env_vars_needed": env_vars,
        "endpoints": endpoints,
        "source_format": "postman",
    }


def _flatten_postman_items(items, folder=""):
    """Recursively flatten nested Postman collection items."""
    flat = []
    for item in items:
        if "item" in item:
            # This is a folder
            folder_name = item.get("name", folder)
            flat.extend(_flatten_postman_items(item["item"], folder_name))
        else:
            item["_folder"] = folder
            flat.append(item)
    return flat


# ---------------------------------------------------------------------------
# DeepWiki parser
# ---------------------------------------------------------------------------
class _DeepWikiHTMLParser(HTMLParser):
    """Extract structured content from DeepWiki pages."""

    def __init__(self):
        super().__init__()
        self.sections = []
        self._current_section = None
        self._current_tag = None
        self._in_code = False
        self._code_buf = []
        self._text_buf = []

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3", "h4"):
            self._flush_text()
            self._current_tag = tag
            self._text_buf = []
        elif tag == "code":
            self._in_code = True
            self._code_buf = []
        elif tag == "pre":
            self._in_code = True
            self._code_buf = []

    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3", "h4"):
            title = "".join(self._text_buf).strip()
            self._current_section = {"title": title, "level": tag, "content": "", "code_blocks": []}
            self.sections.append(self._current_section)
            self._text_buf = []
            self._current_tag = None
        elif tag in ("code", "pre") and self._in_code:
            code = "".join(self._code_buf).strip()
            if code and self._current_section:
                self._current_section["code_blocks"].append(code)
            self._in_code = False
            self._code_buf = []

    def handle_data(self, data):
        if self._in_code:
            self._code_buf.append(data)
        elif self._current_tag:
            self._text_buf.append(data)
        elif self._current_section:
            self._current_section["content"] += data

    def _flush_text(self):
        if self._current_section and self._text_buf:
            self._current_section["content"] += "".join(self._text_buf)
            self._text_buf = []


def parse_deepwiki(data, url):
    """Parse DeepWiki HTML into our intermediate format."""
    parser = _DeepWikiHTMLParser()
    parser.feed(data)

    # Extract service name from URL: deepwiki.com/org/repo
    parsed = urllib.parse.urlparse(url)
    path_parts = [p for p in parsed.path.strip("/").split("/") if p]
    if len(path_parts) >= 2:
        service_name = _slugify(path_parts[1])
    elif path_parts:
        service_name = _slugify(path_parts[0])
    else:
        service_name = "api"

    # Extract API endpoints from code blocks and content
    endpoints = []
    base_url = ""

    url_pattern = re.compile(r'(GET|POST|PUT|PATCH|DELETE|HEAD)\s+(https?://\S+|/\S+)', re.IGNORECASE)
    base_url_pattern = re.compile(r'https?://[a-zA-Z0-9\-\.]+(?:\.[a-zA-Z]{2,})(?::\d+)?(?:/api(?:/v\d+)?)?')

    for section in parser.sections:
        # Check code blocks for API endpoints
        for code in section["code_blocks"]:
            for m in url_pattern.finditer(code):
                method = m.group(1).upper()
                path = m.group(2)
                # Try to extract base URL
                if path.startswith("http"):
                    parsed_ep = urllib.parse.urlparse(path)
                    if not base_url:
                        base_url = f"{parsed_ep.scheme}://{parsed_ep.netloc}"
                    path = parsed_ep.path
                endpoints.append({
                    "method": method,
                    "path": path,
                    "summary": section["title"],
                    "tags": [],
                    "parameters": [],
                    "body_fields": [],
                    "operation_id": "",
                })

        # Check content text for endpoints
        for m in url_pattern.finditer(section.get("content", "")):
            method = m.group(1).upper()
            path = m.group(2)
            if path.startswith("http"):
                parsed_ep = urllib.parse.urlparse(path)
                if not base_url:
                    base_url = f"{parsed_ep.scheme}://{parsed_ep.netloc}"
                path = parsed_ep.path
            endpoints.append({
                "method": method,
                "path": path,
                "summary": section["title"],
                "tags": [],
                "parameters": [],
                "body_fields": [],
                "operation_id": "",
            })

        # Try to find base URL in content
        if not base_url:
            bm = base_url_pattern.search(section.get("content", ""))
            if bm:
                base_url = bm.group(0)

    # Clean up path artifacts (trailing backticks, quotes, escape sequences, \n\r)
    for ep in endpoints:
        path = ep["path"]
        # Remove literal escape sequences like \n, \r, \t, \" at the end
        path = re.sub(r'\\[nrtfvb"\'\\]', '', path)
        # Strip remaining trailing non-path characters
        path = re.sub(r'[^a-zA-Z0-9/_{}.\-*]+$', '', path)
        ep["path"] = path.strip()

    # Filter out code-hosting / non-API base URLs
    _non_api_hosts = re.compile(
        r'(github\.com|gitlab\.com|bitbucket\.org|npmjs\.com|pypi\.org'
        r'|stackoverflow\.com|docs\.python\.org)',
        re.IGNORECASE,
    )
    if base_url and _non_api_hosts.search(base_url):
        base_url = ""

    # Deduplicate endpoints by method+path
    seen = set()
    unique = []
    for ep in endpoints:
        key = f"{ep['method']}:{ep['path']}"
        if key not in seen:
            seen.add(key)
            unique.append(ep)
    endpoints = _rank_and_limit(unique)

    # Infer tags from path segments
    for ep in endpoints:
        if not ep["tags"]:
            parts = [p for p in ep["path"].strip("/").split("/") if p and not p.startswith("{")]
            if parts:
                ep["tags"] = [parts[0]]

    env_prefix = service_name.upper().replace("-", "_")
    env_vars = [f"{env_prefix}_URL", f"{env_prefix}_TOKEN"]

    return {
        "service_name": service_name,
        "base_url": base_url,
        "auth_type": "bearer",
        "auth_header_format": "Bearer {token}",
        "env_vars_needed": env_vars,
        "endpoints": endpoints,
        "source_format": "deepwiki",
    }


# ---------------------------------------------------------------------------
# Generic HTML parser
# ---------------------------------------------------------------------------
class _GenericHTMLParser(HTMLParser):
    """Best-effort extraction of API info from generic HTML docs."""

    def __init__(self):
        super().__init__()
        self.headings = []
        self.code_blocks = []
        self._current_tag = None
        self._text_buf = []
        self._in_code = False
        self._code_buf = []

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3"):
            self._current_tag = tag
            self._text_buf = []
        elif tag in ("code", "pre"):
            self._in_code = True
            self._code_buf = []

    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3"):
            text = "".join(self._text_buf).strip()
            if text:
                self.headings.append({"level": tag, "text": text})
            self._current_tag = None
        elif tag in ("code", "pre") and self._in_code:
            code = "".join(self._code_buf).strip()
            if code:
                self.code_blocks.append(code)
            self._in_code = False

    def handle_data(self, data):
        if self._in_code:
            self._code_buf.append(data)
        elif self._current_tag:
            self._text_buf.append(data)


def parse_html(data, url):
    """Best-effort extraction of API endpoints from generic HTML documentation."""
    parser = _GenericHTMLParser()
    parser.feed(data)

    endpoints = []
    base_url = ""

    url_pattern = re.compile(r'(GET|POST|PUT|PATCH|DELETE)\s+(https?://\S+|/[\w/\{\}\-\.]+)', re.IGNORECASE)
    base_url_pattern = re.compile(r'https?://[a-zA-Z0-9\-\.]+(?:\.[a-zA-Z]{2,})(?::\d+)?(?:/api(?:/v\d+)?)?')

    all_text = data  # search the entire HTML for patterns
    for m in url_pattern.finditer(all_text):
        method = m.group(1).upper()
        path = m.group(2)
        if path.startswith("http"):
            parsed_ep = urllib.parse.urlparse(path)
            if not base_url:
                base_url = f"{parsed_ep.scheme}://{parsed_ep.netloc}"
            path = parsed_ep.path
        endpoints.append({
            "method": method,
            "path": path,
            "summary": "",
            "tags": [],
            "parameters": [],
            "body_fields": [],
            "operation_id": "",
        })

    # Also check code blocks
    for code in parser.code_blocks:
        for m in url_pattern.finditer(code):
            method = m.group(1).upper()
            path = m.group(2)
            if path.startswith("http"):
                parsed_ep = urllib.parse.urlparse(path)
                if not base_url:
                    base_url = f"{parsed_ep.scheme}://{parsed_ep.netloc}"
                path = parsed_ep.path
            endpoints.append({
                "method": method,
                "path": path,
                "summary": "",
                "tags": [],
                "parameters": [],
                "body_fields": [],
                "operation_id": "",
            })

    # Build base_url: prefer URLs that look like API hosts, not CDNs/analytics
    _cdn_pattern = re.compile(
        r'(googletagmanager|googleapis|google-analytics|cloudflare|cdnjs'
        r'|jquery|bootstrapcdn|fontawesome|w3\.org|schema\.org'
        r'|facebook\.net|twitter\.com|linkedin\.com)',
        re.IGNORECASE,
    )
    if not base_url:
        for m in re.finditer(base_url_pattern, all_text):
            candidate = m.group(0)
            if not _cdn_pattern.search(candidate):
                base_url = candidate
                break

    # Deduplicate
    seen = set()
    unique = []
    for ep in endpoints:
        key = f"{ep['method']}:{ep['path']}"
        if key not in seen:
            seen.add(key)
            unique.append(ep)
    endpoints = _rank_and_limit(unique)

    # Infer tags from paths
    for ep in endpoints:
        if not ep["tags"]:
            parts = [p for p in ep["path"].strip("/").split("/") if p and not p.startswith("{")]
            if parts:
                ep["tags"] = [parts[0]]

    # Infer service name: prefer <title> tag, then full hostname (not just first segment)
    title_m = re.search(r'<title[^>]*>([^<]+)</title>', data, re.IGNORECASE)
    parsed = urllib.parse.urlparse(url) if url.startswith("http") else None
    if title_m:
        service_name = _slugify(title_m.group(1).strip())
    elif parsed and parsed.hostname:
        # Use full hostname minus TLD: api.artic.edu → api-artic
        parts = parsed.hostname.split(".")
        host_slug = "-".join(parts[:-1]) if len(parts) > 2 else parts[0]
        service_name = _slugify(host_slug)
    elif parser.headings:
        service_name = _slugify(parser.headings[0]["text"])
    else:
        service_name = "api"

    env_prefix = service_name.upper().replace("-", "_")
    env_vars = [f"{env_prefix}_URL", f"{env_prefix}_TOKEN"]

    return {
        "service_name": service_name,
        "base_url": base_url,
        "auth_type": "bearer",
        "auth_header_format": "Bearer {token}",
        "env_vars_needed": env_vars,
        "endpoints": endpoints,
        "source_format": "html",
    }


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------
def _slugify(name):
    """Convert a name to a valid skill directory name (lowercase, hyphens only)."""
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9\-]', '-', s)
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    return s[:64] if s else "api"


# Method priority for ranking: lower = more useful to users
_METHOD_PRIORITY = {"GET": 0, "POST": 1, "PUT": 2, "PATCH": 3, "DELETE": 4, "HEAD": 5, "OPTIONS": 6}

# Path patterns that indicate admin/internal endpoints
_ADMIN_PATTERNS = re.compile(
    r'(/admin/|/internal/|/debug/|/healthz|/metrics|/swagger|/openapi|'
    r'/__\w+|/\.well-known)',
    re.IGNORECASE,
)


def _rank_and_limit(endpoints, limit=30):
    """Rank endpoints by usefulness, limit to top N if >100 total."""
    if len(endpoints) <= limit:
        return endpoints

    # Filter out admin/internal endpoints
    filtered = [ep for ep in endpoints if not _ADMIN_PATTERNS.search(ep["path"])]
    if not filtered:
        filtered = endpoints

    # Sort by: method priority, then path length (shorter = more common)
    filtered.sort(key=lambda ep: (
        _METHOD_PRIORITY.get(ep["method"], 99),
        len(ep["path"]),
    ))

    return filtered[:limit]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_docs.py <URL_or_FILE>", file=sys.stderr)
        print("  Supports: OpenAPI 3.x, Swagger 2.0, Postman v2, DeepWiki, HTML", file=sys.stderr)
        sys.exit(1)

    source = sys.argv[1]

    # Is it a local file?
    if os.path.exists(source):
        data, content_type, final_url = read_local_file(source)
    elif source.startswith(("http://", "https://")):
        try:
            data, content_type, final_url = fetch_url(source)
        except Exception as e:
            print(f"Error fetching URL: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Error: '{source}' is not a valid URL or file path", file=sys.stderr)
        sys.exit(1)

    fmt = detect_format(data, content_type, final_url)

    if fmt == "openapi3":
        result = parse_openapi3(data)
    elif fmt == "swagger2":
        result = parse_swagger2(data)
    elif fmt == "yaml":
        result = parse_yaml_spec(data)
    elif fmt == "postman":
        result = parse_postman(data)
    elif fmt == "deepwiki":
        result = parse_deepwiki(data, final_url)
    elif fmt == "html":
        result = parse_html(data, final_url)
    else:
        # Last resort: try as YAML, then HTML
        try:
            result = parse_yaml_spec(data)
        except (SystemExit, Exception):
            result = parse_html(data, final_url)

    if not result["endpoints"]:
        print("Warning: No API endpoints found. The output may need manual editing.", file=sys.stderr)

    json.dump(result, sys.stdout, indent=2)
    print()  # trailing newline


if __name__ == "__main__":
    main()
