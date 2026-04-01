#!/usr/bin/env python3
"""
spotify CLI tool for Claude Code skill integration.
Provides access to the spotify-web-api-with-fixes-and-improvements-from-sonallux API.
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
BASE_URL = _env.get("SPOTIFY_URL", "https://api.spotify.com/v1")
AUTH_TOKEN = _env.get("SPOTIFY_TOKEN", "")

_ssl_ctx = ssl.create_default_context()
if _env.get("SPOTIFY_VERIFY_SSL", "true").lower() == "false":
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = ssl.CERT_NONE


def get_auth_header() -> dict:
    """Build authorization header."""
    if AUTH_TOKEN:
        return {"Authorization": f"Bearer {AUTH_TOKEN}"}
    return {}


def make_request(path: str, method: str = "GET", data: bytes = None, params: dict = None) -> tuple:
    """Make HTTP request to the spotify API."""
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
    """Verify connectivity to the spotify API."""
    if not BASE_URL:
        print(f"Error: SPOTIFY_URL not set", file=sys.stderr)
        sys.exit(1)
    status, body = make_request("/")
    if status == 0:
        print(f"Cannot connect to {BASE_URL}", file=sys.stderr)
        print(f"Error: {body}", file=sys.stderr)
        sys.exit(1)
    print(f"Connected to {BASE_URL} (HTTP {status})")


def cmd_albums_get(args):
    """Get Several Albums
"""
    path = "/albums"
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


def cmd_albums_get_2(args):
    """Get User's Saved Albums
"""
    path = "/me/albums"
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


def cmd_albums_get_3(args):
    """Get Album
"""
    path = "/albums/{id}".replace("{id}", str(args.id))
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


def cmd_artists_get(args):
    """Get Several Artists
"""
    path = "/artists"
    params = {}
    if args.ids is not None:
        params["ids"] = args.ids
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


def cmd_artists_get_2(args):
    """Get Artist
"""
    path = "/artists/{id}".replace("{id}", str(args.id))
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


def cmd_audiobooks_get(args):
    """Get Several Audiobooks
"""
    path = "/audiobooks"
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


def cmd_audiobooks_get_2(args):
    """Get User's Saved Audiobooks
"""
    path = "/me/audiobooks"
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


def cmd_audiobooks_get_3(args):
    """Get an Audiobook
"""
    path = "/audiobooks/{id}".replace("{id}", str(args.id))
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


def cmd_chapters_get(args):
    """Get Several Chapters
"""
    path = "/chapters"
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


def cmd_chapters_get_2(args):
    """Get a Chapter
"""
    path = "/chapters/{id}".replace("{id}", str(args.id))
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


def cmd_episodes_get(args):
    """Get Several Episodes
"""
    path = "/episodes"
    params = {}
    if args.ids is not None:
        params["ids"] = args.ids
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


def cmd_episodes_get_2(args):
    """Get User's Saved Episodes
"""
    path = "/me/episodes"
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


def cmd_episodes_get_3(args):
    """Get Episode
"""
    path = "/episodes/{id}".replace("{id}", str(args.id))
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


def cmd_markets_get(args):
    """Get Available Markets
"""
    path = "/markets"
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


def cmd_player_get(args):
    """Get Playback State
"""
    path = "/me/player"
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


def cmd_player_get_2(args):
    """Get the User's Queue
"""
    path = "/me/player/queue"
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


def cmd_playlists_get(args):
    """Get Current User's Playlists
"""
    path = "/me/playlists"
    params = {}
    if args.offset is not None:
        params["offset"] = args.offset
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


def cmd_search_list(args):
    """Search for Item
"""
    path = "/search"
    params = {}
    if args.q is not None:
        params["q"] = args.q
    if args.type is not None:
        params["type"] = args.type
    if args.limit is not None:
        params["limit"] = args.limit
    if args.offset is not None:
        params["offset"] = args.offset
    if args.include_external is not None:
        params["include_external"] = args.include_external
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


def cmd_shows_get(args):
    """Get Several Shows
"""
    path = "/shows"
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


def cmd_shows_get_2(args):
    """Get User's Saved Shows
"""
    path = "/me/shows"
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


def cmd_shows_get_3(args):
    """Get Show
"""
    path = "/shows/{id}".replace("{id}", str(args.id))
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


def cmd_tracks_get(args):
    """Get Several Tracks
"""
    path = "/tracks"
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


def cmd_tracks_get_2(args):
    """Get User's Saved Tracks
"""
    path = "/me/tracks"
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


def cmd_tracks_get_3(args):
    """Get Track
"""
    path = "/tracks/{id}".replace("{id}", str(args.id))
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


def cmd_tracks_get_4(args):
    """Get Tracks' Audio Features
"""
    path = "/audio-features"
    params = {}
    if args.ids is not None:
        params["ids"] = args.ids
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


def cmd_tracks_get_5(args):
    """Get Recommendations
"""
    path = "/recommendations"
    params = {}
    if args.limit is not None:
        params["limit"] = args.limit
    if args.seed_artists is not None:
        params["seed_artists"] = args.seed_artists
    if args.seed_genres is not None:
        params["seed_genres"] = args.seed_genres
    if args.seed_tracks is not None:
        params["seed_tracks"] = args.seed_tracks
    if args.min_acousticness is not None:
        params["min_acousticness"] = args.min_acousticness
    if args.max_acousticness is not None:
        params["max_acousticness"] = args.max_acousticness
    if args.target_acousticness is not None:
        params["target_acousticness"] = args.target_acousticness
    if args.min_danceability is not None:
        params["min_danceability"] = args.min_danceability
    if args.max_danceability is not None:
        params["max_danceability"] = args.max_danceability
    if args.target_danceability is not None:
        params["target_danceability"] = args.target_danceability
    if args.min_duration_ms is not None:
        params["min_duration_ms"] = args.min_duration_ms
    if args.max_duration_ms is not None:
        params["max_duration_ms"] = args.max_duration_ms
    if args.target_duration_ms is not None:
        params["target_duration_ms"] = args.target_duration_ms
    if args.min_energy is not None:
        params["min_energy"] = args.min_energy
    if args.max_energy is not None:
        params["max_energy"] = args.max_energy
    if args.target_energy is not None:
        params["target_energy"] = args.target_energy
    if args.min_instrumentalness is not None:
        params["min_instrumentalness"] = args.min_instrumentalness
    if args.max_instrumentalness is not None:
        params["max_instrumentalness"] = args.max_instrumentalness
    if args.target_instrumentalness is not None:
        params["target_instrumentalness"] = args.target_instrumentalness
    if args.min_key is not None:
        params["min_key"] = args.min_key
    if args.max_key is not None:
        params["max_key"] = args.max_key
    if args.target_key is not None:
        params["target_key"] = args.target_key
    if args.min_liveness is not None:
        params["min_liveness"] = args.min_liveness
    if args.max_liveness is not None:
        params["max_liveness"] = args.max_liveness
    if args.target_liveness is not None:
        params["target_liveness"] = args.target_liveness
    if args.min_loudness is not None:
        params["min_loudness"] = args.min_loudness
    if args.max_loudness is not None:
        params["max_loudness"] = args.max_loudness
    if args.target_loudness is not None:
        params["target_loudness"] = args.target_loudness
    if args.min_mode is not None:
        params["min_mode"] = args.min_mode
    if args.max_mode is not None:
        params["max_mode"] = args.max_mode
    if args.target_mode is not None:
        params["target_mode"] = args.target_mode
    if args.min_popularity is not None:
        params["min_popularity"] = args.min_popularity
    if args.max_popularity is not None:
        params["max_popularity"] = args.max_popularity
    if args.target_popularity is not None:
        params["target_popularity"] = args.target_popularity
    if args.min_speechiness is not None:
        params["min_speechiness"] = args.min_speechiness
    if args.max_speechiness is not None:
        params["max_speechiness"] = args.max_speechiness
    if args.target_speechiness is not None:
        params["target_speechiness"] = args.target_speechiness
    if args.min_tempo is not None:
        params["min_tempo"] = args.min_tempo
    if args.max_tempo is not None:
        params["max_tempo"] = args.max_tempo
    if args.target_tempo is not None:
        params["target_tempo"] = args.target_tempo
    if args.min_time_signature is not None:
        params["min_time_signature"] = args.min_time_signature
    if args.max_time_signature is not None:
        params["max_time_signature"] = args.max_time_signature
    if args.target_time_signature is not None:
        params["target_time_signature"] = args.target_time_signature
    if args.min_valence is not None:
        params["min_valence"] = args.min_valence
    if args.max_valence is not None:
        params["max_valence"] = args.max_valence
    if args.target_valence is not None:
        params["target_valence"] = args.target_valence
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


def cmd_users_get(args):
    """Get Current User's Profile
"""
    path = "/me"
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


def cmd_users_get_2(args):
    """Get Followed Artists
"""
    path = "/me/following"
    params = {}
    if args.type is not None:
        params["type"] = args.type
    if args.after is not None:
        params["after"] = args.after
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


def cmd_users_get_3(args):
    """Get User's Top Tracks
"""
    path = "/me/top/tracks"
    params = {}
    if args.time_range is not None:
        params["time_range"] = args.time_range
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


def cmd_users_get_4(args):
    """Get User's Top Artists
"""
    path = "/me/top/artists"
    params = {}
    if args.time_range is not None:
        params["time_range"] = args.time_range
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
    parser = argparse.ArgumentParser(description="spotify CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- check ---
    subparsers.add_parser("check", help="Test API connectivity")

    # --- albums ---
    parser_albums = subparsers.add_parser("albums", help="Albums operations")
    sub_albums = parser_albums.add_subparsers(dest="albums_action", help="albums actions")

    p_albums_get = sub_albums.add_parser("get", help="Get Several Albums ")
    p_albums_get.set_defaults(func=cmd_albums_get)

    p_albums_get_2 = sub_albums.add_parser("get-2", help="Get User's Saved Albums ")
    p_albums_get_2.set_defaults(func=cmd_albums_get_2)

    p_albums_get_3 = sub_albums.add_parser("get-3", help="Get Album ")
    p_albums_get_3.add_argument("id", help="id")
    p_albums_get_3.set_defaults(func=cmd_albums_get_3)

    # --- artists ---
    parser_artists = subparsers.add_parser("artists", help="Artists operations")
    sub_artists = parser_artists.add_subparsers(dest="artists_action", help="artists actions")

    p_artists_get = sub_artists.add_parser("get", help="Get Several Artists ")
    p_artists_get.add_argument("--ids", dest="ids", default=None, help="")
    p_artists_get.set_defaults(func=cmd_artists_get)

    p_artists_get_2 = sub_artists.add_parser("get-2", help="Get Artist ")
    p_artists_get_2.add_argument("id", help="id")
    p_artists_get_2.set_defaults(func=cmd_artists_get_2)

    # --- audiobooks ---
    parser_audiobooks = subparsers.add_parser("audiobooks", help="Audiobooks operations")
    sub_audiobooks = parser_audiobooks.add_subparsers(dest="audiobooks_action", help="audiobooks actions")

    p_audiobooks_get = sub_audiobooks.add_parser("get", help="Get Several Audiobooks ")
    p_audiobooks_get.set_defaults(func=cmd_audiobooks_get)

    p_audiobooks_get_2 = sub_audiobooks.add_parser("get-2", help="Get User's Saved Audiobooks ")
    p_audiobooks_get_2.set_defaults(func=cmd_audiobooks_get_2)

    p_audiobooks_get_3 = sub_audiobooks.add_parser("get-3", help="Get an Audiobook ")
    p_audiobooks_get_3.add_argument("id", help="id")
    p_audiobooks_get_3.set_defaults(func=cmd_audiobooks_get_3)

    # --- chapters ---
    parser_chapters = subparsers.add_parser("chapters", help="Chapters operations")
    sub_chapters = parser_chapters.add_subparsers(dest="chapters_action", help="chapters actions")

    p_chapters_get = sub_chapters.add_parser("get", help="Get Several Chapters ")
    p_chapters_get.set_defaults(func=cmd_chapters_get)

    p_chapters_get_2 = sub_chapters.add_parser("get-2", help="Get a Chapter ")
    p_chapters_get_2.add_argument("id", help="id")
    p_chapters_get_2.set_defaults(func=cmd_chapters_get_2)

    # --- episodes ---
    parser_episodes = subparsers.add_parser("episodes", help="Episodes operations")
    sub_episodes = parser_episodes.add_subparsers(dest="episodes_action", help="episodes actions")

    p_episodes_get = sub_episodes.add_parser("get", help="Get Several Episodes ")
    p_episodes_get.add_argument("--ids", dest="ids", default=None, help="")
    p_episodes_get.set_defaults(func=cmd_episodes_get)

    p_episodes_get_2 = sub_episodes.add_parser("get-2", help="Get User's Saved Episodes ")
    p_episodes_get_2.set_defaults(func=cmd_episodes_get_2)

    p_episodes_get_3 = sub_episodes.add_parser("get-3", help="Get Episode ")
    p_episodes_get_3.add_argument("id", help="id")
    p_episodes_get_3.set_defaults(func=cmd_episodes_get_3)

    # --- markets ---
    parser_markets = subparsers.add_parser("markets", help="Markets operations")
    sub_markets = parser_markets.add_subparsers(dest="markets_action", help="markets actions")

    p_markets_get = sub_markets.add_parser("get", help="Get Available Markets ")
    p_markets_get.set_defaults(func=cmd_markets_get)

    # --- player ---
    parser_player = subparsers.add_parser("player", help="Player operations")
    sub_player = parser_player.add_subparsers(dest="player_action", help="player actions")

    p_player_get = sub_player.add_parser("get", help="Get Playback State ")
    p_player_get.set_defaults(func=cmd_player_get)

    p_player_get_2 = sub_player.add_parser("get-2", help="Get the User's Queue ")
    p_player_get_2.set_defaults(func=cmd_player_get_2)

    # --- playlists ---
    parser_playlists = subparsers.add_parser("playlists", help="Playlists operations")
    sub_playlists = parser_playlists.add_subparsers(dest="playlists_action", help="playlists actions")

    p_playlists_get = sub_playlists.add_parser("get", help="Get Current User's Playlists ")
    p_playlists_get.add_argument("--offset", dest="offset", default=None, help="")
    p_playlists_get.set_defaults(func=cmd_playlists_get)

    # --- search ---
    parser_search = subparsers.add_parser("search", help="Search operations")
    sub_search = parser_search.add_subparsers(dest="search_action", help="search actions")

    p_search_list = sub_search.add_parser("list", help="Search for Item ")
    p_search_list.add_argument("--q", dest="q", default=None, help="")
    p_search_list.add_argument("--type", dest="type", default=None, help="")
    p_search_list.add_argument("--limit", dest="limit", default=None, help="")
    p_search_list.add_argument("--offset", dest="offset", default=None, help="")
    p_search_list.add_argument("--include-external", dest="include_external", default=None, help="")
    p_search_list.set_defaults(func=cmd_search_list)

    # --- shows ---
    parser_shows = subparsers.add_parser("shows", help="Shows operations")
    sub_shows = parser_shows.add_subparsers(dest="shows_action", help="shows actions")

    p_shows_get = sub_shows.add_parser("get", help="Get Several Shows ")
    p_shows_get.set_defaults(func=cmd_shows_get)

    p_shows_get_2 = sub_shows.add_parser("get-2", help="Get User's Saved Shows ")
    p_shows_get_2.set_defaults(func=cmd_shows_get_2)

    p_shows_get_3 = sub_shows.add_parser("get-3", help="Get Show ")
    p_shows_get_3.add_argument("id", help="id")
    p_shows_get_3.set_defaults(func=cmd_shows_get_3)

    # --- tracks ---
    parser_tracks = subparsers.add_parser("tracks", help="Tracks operations")
    sub_tracks = parser_tracks.add_subparsers(dest="tracks_action", help="tracks actions")

    p_tracks_get = sub_tracks.add_parser("get", help="Get Several Tracks ")
    p_tracks_get.set_defaults(func=cmd_tracks_get)

    p_tracks_get_2 = sub_tracks.add_parser("get-2", help="Get User's Saved Tracks ")
    p_tracks_get_2.set_defaults(func=cmd_tracks_get_2)

    p_tracks_get_3 = sub_tracks.add_parser("get-3", help="Get Track ")
    p_tracks_get_3.add_argument("id", help="id")
    p_tracks_get_3.set_defaults(func=cmd_tracks_get_3)

    p_tracks_get_4 = sub_tracks.add_parser("get-4", help="Get Tracks' Audio Features ")
    p_tracks_get_4.add_argument("--ids", dest="ids", default=None, help="")
    p_tracks_get_4.set_defaults(func=cmd_tracks_get_4)

    p_tracks_get_5 = sub_tracks.add_parser("get-5", help="Get Recommendations ")
    p_tracks_get_5.add_argument("--limit", dest="limit", default=None, help="")
    p_tracks_get_5.add_argument("--seed-artists", dest="seed_artists", default=None, help="")
    p_tracks_get_5.add_argument("--seed-genres", dest="seed_genres", default=None, help="")
    p_tracks_get_5.add_argument("--seed-tracks", dest="seed_tracks", default=None, help="")
    p_tracks_get_5.add_argument("--min-acousticness", dest="min_acousticness", default=None, help="")
    p_tracks_get_5.add_argument("--max-acousticness", dest="max_acousticness", default=None, help="")
    p_tracks_get_5.add_argument("--target-acousticness", dest="target_acousticness", default=None, help="")
    p_tracks_get_5.add_argument("--min-danceability", dest="min_danceability", default=None, help="")
    p_tracks_get_5.add_argument("--max-danceability", dest="max_danceability", default=None, help="")
    p_tracks_get_5.add_argument("--target-danceability", dest="target_danceability", default=None, help="")
    p_tracks_get_5.add_argument("--min-duration-ms", dest="min_duration_ms", default=None, help="")
    p_tracks_get_5.add_argument("--max-duration-ms", dest="max_duration_ms", default=None, help="")
    p_tracks_get_5.add_argument("--target-duration-ms", dest="target_duration_ms", default=None, help="")
    p_tracks_get_5.add_argument("--min-energy", dest="min_energy", default=None, help="")
    p_tracks_get_5.add_argument("--max-energy", dest="max_energy", default=None, help="")
    p_tracks_get_5.add_argument("--target-energy", dest="target_energy", default=None, help="")
    p_tracks_get_5.add_argument("--min-instrumentalness", dest="min_instrumentalness", default=None, help="")
    p_tracks_get_5.add_argument("--max-instrumentalness", dest="max_instrumentalness", default=None, help="")
    p_tracks_get_5.add_argument("--target-instrumentalness", dest="target_instrumentalness", default=None, help="")
    p_tracks_get_5.add_argument("--min-key", dest="min_key", default=None, help="")
    p_tracks_get_5.add_argument("--max-key", dest="max_key", default=None, help="")
    p_tracks_get_5.add_argument("--target-key", dest="target_key", default=None, help="")
    p_tracks_get_5.add_argument("--min-liveness", dest="min_liveness", default=None, help="")
    p_tracks_get_5.add_argument("--max-liveness", dest="max_liveness", default=None, help="")
    p_tracks_get_5.add_argument("--target-liveness", dest="target_liveness", default=None, help="")
    p_tracks_get_5.add_argument("--min-loudness", dest="min_loudness", default=None, help="")
    p_tracks_get_5.add_argument("--max-loudness", dest="max_loudness", default=None, help="")
    p_tracks_get_5.add_argument("--target-loudness", dest="target_loudness", default=None, help="")
    p_tracks_get_5.add_argument("--min-mode", dest="min_mode", default=None, help="")
    p_tracks_get_5.add_argument("--max-mode", dest="max_mode", default=None, help="")
    p_tracks_get_5.add_argument("--target-mode", dest="target_mode", default=None, help="")
    p_tracks_get_5.add_argument("--min-popularity", dest="min_popularity", default=None, help="")
    p_tracks_get_5.add_argument("--max-popularity", dest="max_popularity", default=None, help="")
    p_tracks_get_5.add_argument("--target-popularity", dest="target_popularity", default=None, help="")
    p_tracks_get_5.add_argument("--min-speechiness", dest="min_speechiness", default=None, help="")
    p_tracks_get_5.add_argument("--max-speechiness", dest="max_speechiness", default=None, help="")
    p_tracks_get_5.add_argument("--target-speechiness", dest="target_speechiness", default=None, help="")
    p_tracks_get_5.add_argument("--min-tempo", dest="min_tempo", default=None, help="")
    p_tracks_get_5.add_argument("--max-tempo", dest="max_tempo", default=None, help="")
    p_tracks_get_5.add_argument("--target-tempo", dest="target_tempo", default=None, help="")
    p_tracks_get_5.add_argument("--min-time-signature", dest="min_time_signature", default=None, help="")
    p_tracks_get_5.add_argument("--max-time-signature", dest="max_time_signature", default=None, help="")
    p_tracks_get_5.add_argument("--target-time-signature", dest="target_time_signature", default=None, help="")
    p_tracks_get_5.add_argument("--min-valence", dest="min_valence", default=None, help="")
    p_tracks_get_5.add_argument("--max-valence", dest="max_valence", default=None, help="")
    p_tracks_get_5.add_argument("--target-valence", dest="target_valence", default=None, help="")
    p_tracks_get_5.set_defaults(func=cmd_tracks_get_5)

    # --- users ---
    parser_users = subparsers.add_parser("users", help="Users operations")
    sub_users = parser_users.add_subparsers(dest="users_action", help="users actions")

    p_users_get = sub_users.add_parser("get", help="Get Current User's Profile ")
    p_users_get.set_defaults(func=cmd_users_get)

    p_users_get_2 = sub_users.add_parser("get-2", help="Get Followed Artists ")
    p_users_get_2.add_argument("--type", dest="type", default=None, help="")
    p_users_get_2.add_argument("--after", dest="after", default=None, help="")
    p_users_get_2.set_defaults(func=cmd_users_get_2)

    p_users_get_3 = sub_users.add_parser("get-3", help="Get User's Top Tracks ")
    p_users_get_3.add_argument("--time-range", dest="time_range", default=None, help="")
    p_users_get_3.set_defaults(func=cmd_users_get_3)

    p_users_get_4 = sub_users.add_parser("get-4", help="Get User's Top Artists ")
    p_users_get_4.add_argument("--time-range", dest="time_range", default=None, help="")
    p_users_get_4.set_defaults(func=cmd_users_get_4)

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
