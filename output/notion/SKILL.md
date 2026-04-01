---
name: notion
description: Interact with notion-api API. Use for querying, creating, and managing notion-api resources. Use when asked about notion-api operations.
argument-hint: [command] [args]
allowed-tools: Bash(python3:*)
---

# Notion Api Integration

## Configuration

Set these environment variables in `~/.zshrc`:

- `NOTION_URL` — API base URL (default: `https://api.notion.com`)
- `NOTION_TOKEN` — Authentication token

## Available Commands

### Check Connection
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py check
```

### Blocks
```bash
# Delete a block
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py blocks delete ID
# Retrieve a block
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py blocks retrieveablock ID
# Update a block
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py blocks update ID
# Retrieve block children
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py blocks retrieveblockchildren ID --page-size VALUE
# Append block children
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py blocks appendblockchildren ID
```

### Comments
```bash
# Retrieve comments
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py comments retrievecomments --block-id VALUE --page-size VALUE
```

### Databases
```bash
# Retrieve a database
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py databases retrieveadatabase ID
# Update a database
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py databases update ID
# Query a database
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py databases queryadatabase ID
```

### Pages
```bash
# Retrieve a Page
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py pages retrieveapage ID
# Update Page properties 
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py pages update ID
# Retrieve a Page Property Item
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py pages retrieveapagepropertyitem PAGE_ID PROPERTY_ID
```

### Users
```bash
# Retrieve a user
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py users retrieveauser ID
```

## Usage Instructions

Map user requests to commands:

1. **"Is notion-api reachable?"** / **"Test connection"** → `check`
2. **"Delete a block"** → `blocks delete ID`
3. **"Retrieve a block"** → `blocks retrieveablock ID`
4. **"Update a block"** → `blocks update ID`
5. **"Retrieve block children"** → `blocks retrieveblockchildren ID --page-size VALUE`
6. **"Append block children"** → `blocks appendblockchildren ID`
7. **"Retrieve comments"** → `comments retrievecomments --block-id VALUE`
8. **"Retrieve a database"** → `databases retrieveadatabase ID`
9. **"Update a database"** → `databases update ID`
10. **"Query a database"** → `databases queryadatabase ID`
11. **"Retrieve a Page"** → `pages retrieveapage ID`
12. **"Update Page properties "** → `pages update ID`
13. **"Retrieve a Page Property Item"** → `pages retrieveapagepropertyitem PAGE_ID PROPERTY_ID`
14. **"Retrieve a user"** → `users retrieveauser ID`

## Examples

User: "Is notion-api connected?"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py check
```

User: "Delete a block"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py blocks delete EXAMPLE_ID
```

User: "Retrieve comments"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py comments retrievecomments
```

User: "Retrieve a database"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py databases retrieveadatabase EXAMPLE_ID
```

User: "Retrieve a Page"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/notion_cli.py pages retrieveapage EXAMPLE_ID
```
