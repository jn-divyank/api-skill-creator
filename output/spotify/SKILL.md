---
name: spotify
description: Interact with spotify-web-api-with-fixes-and-improvements-from-sonallux API. Use for querying, creating, and managing spotify-web-api-with-fixes-and-improvements-from-sonallux resources. Use when asked about spotify-web-api-with-fixes-and-improvements-from-sonallux operations.
argument-hint: [command] [args]
allowed-tools: Bash(python3:*)
---

# Spotify Web Api With Fixes And Improvements From Sonallux Integration

## Configuration

Set these environment variables in `~/.zshrc`:

- `SPOTIFY_URL` — API base URL (default: `https://api.spotify.com/v1`)
- `SPOTIFY_TOKEN` — Authentication token

## Available Commands

### Check Connection
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py check
```

### Albums
```bash
# Get Several Albums

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py albums get -- VALUE -- VALUE
# Get User's Saved Albums

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py albums get-2 -- VALUE -- VALUE
# Get Album

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py albums get-3 ID -- VALUE -- VALUE
```

### Artists
```bash
# Get Several Artists

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py artists get --ids VALUE
# Get Artist

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py artists get-2 ID -- VALUE
```

### Audiobooks
```bash
# Get Several Audiobooks

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py audiobooks get -- VALUE -- VALUE
# Get User's Saved Audiobooks

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py audiobooks get-2 -- VALUE -- VALUE
# Get an Audiobook

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py audiobooks get-3 ID -- VALUE -- VALUE
```

### Chapters
```bash
# Get Several Chapters

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py chapters get -- VALUE -- VALUE
# Get a Chapter

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py chapters get-2 ID -- VALUE -- VALUE
```

### Episodes
```bash
# Get Several Episodes

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py episodes get --ids VALUE -- VALUE
# Get User's Saved Episodes

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py episodes get-2 -- VALUE -- VALUE
# Get Episode

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py episodes get-3 ID -- VALUE
```

### Markets
```bash
# Get Available Markets

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py markets get
```

### Player
```bash
# Get Playback State

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py player get -- VALUE -- VALUE
# Get the User's Queue

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py player get-2
```

### Playlists
```bash
# Get Current User's Playlists

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py playlists get -- VALUE --offset VALUE
```

### Search
```bash
# Search for Item

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py search list --q VALUE --type VALUE
```

### Shows
```bash
# Get Several Shows

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py shows get -- VALUE -- VALUE
# Get User's Saved Shows

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py shows get-2 -- VALUE -- VALUE
# Get Show

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py shows get-3 ID -- VALUE -- VALUE
```

### Tracks
```bash
# Get Several Tracks

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py tracks get -- VALUE -- VALUE
# Get User's Saved Tracks

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py tracks get-2 -- VALUE -- VALUE
# Get Track

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py tracks get-3 ID -- VALUE
# Get Tracks' Audio Features

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py tracks get-4 --ids VALUE
# Get Recommendations

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py tracks get-5 --limit VALUE -- VALUE
```

### Users
```bash
# Get Current User's Profile

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py users get
# Get Followed Artists

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py users get-2 --type VALUE --after VALUE
# Get User's Top Tracks

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py users get-3 --time-range VALUE -- VALUE
# Get User's Top Artists

python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py users get-4 --time-range VALUE -- VALUE
```

## Usage Instructions

Map user requests to commands:

1. **"Is spotify-web-api-with-fixes-and-improvements-from-sonallux reachable?"** / **"Test connection"** → `check`
2. **"Get Several Albums
"** → `albums get -- VALUE`
3. **"Get User's Saved Albums
"** → `albums get-2 -- VALUE`
4. **"Get Album
"** → `albums get-3 ID -- VALUE`
5. **"Get Several Artists
"** → `artists get --ids VALUE`
6. **"Get Artist
"** → `artists get-2 ID -- VALUE`
7. **"Get Several Audiobooks
"** → `audiobooks get -- VALUE`
8. **"Get User's Saved Audiobooks
"** → `audiobooks get-2 -- VALUE`
9. **"Get an Audiobook
"** → `audiobooks get-3 ID -- VALUE`
10. **"Get Several Chapters
"** → `chapters get -- VALUE`
11. **"Get a Chapter
"** → `chapters get-2 ID -- VALUE`
12. **"Get Several Episodes
"** → `episodes get --ids VALUE`
13. **"Get User's Saved Episodes
"** → `episodes get-2 -- VALUE`
14. **"Get Episode
"** → `episodes get-3 ID -- VALUE`
15. **"Get Available Markets
"** → `markets get`
16. **"Get Playback State
"** → `player get -- VALUE`
17. **"Get the User's Queue
"** → `player get-2`
18. **"Get Current User's Playlists
"** → `playlists get -- VALUE`
19. **"Search for Item
"** → `search list --q VALUE`
20. **"Get Several Shows
"** → `shows get -- VALUE`
21. **"Get User's Saved Shows
"** → `shows get-2 -- VALUE`
22. **"Get Show
"** → `shows get-3 ID -- VALUE`
23. **"Get Several Tracks
"** → `tracks get -- VALUE`
24. **"Get User's Saved Tracks
"** → `tracks get-2 -- VALUE`
25. **"Get Track
"** → `tracks get-3 ID -- VALUE`
26. **"Get Tracks' Audio Features
"** → `tracks get-4 --ids VALUE`
27. **"Get Recommendations
"** → `tracks get-5 --limit VALUE`
28. **"Get Current User's Profile
"** → `users get`
29. **"Get Followed Artists
"** → `users get-2 --type VALUE`
30. **"Get User's Top Tracks
"** → `users get-3 --time-range VALUE`
31. **"Get User's Top Artists
"** → `users get-4 --time-range VALUE`

## Examples

User: "Is spotify-web-api-with-fixes-and-improvements-from-sonallux connected?"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py check
```

User: "Get Several Albums
"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py albums get
```

User: "Get Several Artists
"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py artists get
```

User: "Get Several Audiobooks
"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py audiobooks get
```

User: "Get Several Chapters
"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/spotify_cli.py chapters get
```
