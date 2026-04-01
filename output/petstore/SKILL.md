---
name: petstore
description: Interact with swagger-petstore API. Use for querying, creating, and managing swagger-petstore resources. Use when asked about swagger-petstore operations.
argument-hint: [command] [args]
allowed-tools: Bash(python3:*)
---

# Swagger Petstore Integration

## Configuration

Set these environment variables in `~/.zshrc`:

- `PETSTORE_URL` — API base URL (default: `https://petstore.swagger.io/v2`)
- `PETSTORE_TOKEN` — Authentication token

## Available Commands

### Check Connection
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py check
```

### Pet
```bash
# uploads an image
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py pet upload PETID
# Add a new pet to the store
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py pet add
# Update an existing pet
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py pet update
# Finds Pets by status
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py pet list --status VALUE
# Finds Pets by tags
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py pet list-2 --tags VALUE
# Find pet by ID
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py pet get PETID
# Updates a pet in the store with form data
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py pet update-2 PETID
# Deletes a pet
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py pet delete PETID
```

### Store
```bash
# Returns pet inventories by status
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py store get
# Place an order for a pet
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py store placeorder
# Find purchase order by ID
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py store get-2 ORDERID
# Delete purchase order by ID
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py store delete ORDERID
```

### User
```bash
# Creates list of users with given input array
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py user create
# Get user by user name
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py user get USERNAME
# Updated user
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py user update USERNAME
# Delete user
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py user delete USERNAME
# Logs user into the system
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py user loginuser --username VALUE --password VALUE
# Logs out current logged in user session
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py user logoutuser
# Creates list of users with given input array
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py user create-2
# Create user
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py user create-3
```

## Usage Instructions

Map user requests to commands:

1. **"Is swagger-petstore reachable?"** / **"Test connection"** → `check`
2. **"uploads an image"** → `pet upload PETID`
3. **"Add a new pet to the store"** → `pet add`
4. **"Update an existing pet"** → `pet update`
5. **"Finds Pets by status"** → `pet list --status VALUE`
6. **"Finds Pets by tags"** → `pet list-2 --tags VALUE`
7. **"Find pet by ID"** → `pet get PETID`
8. **"Updates a pet in the store with form data"** → `pet update-2 PETID`
9. **"Deletes a pet"** → `pet delete PETID`
10. **"Returns pet inventories by status"** → `store get`
11. **"Place an order for a pet"** → `store placeorder`
12. **"Find purchase order by ID"** → `store get-2 ORDERID`
13. **"Delete purchase order by ID"** → `store delete ORDERID`
14. **"Creates list of users with given input array"** → `user create`
15. **"Get user by user name"** → `user get USERNAME`
16. **"Updated user"** → `user update USERNAME`
17. **"Delete user"** → `user delete USERNAME`
18. **"Logs user into the system"** → `user loginuser --username VALUE`
19. **"Logs out current logged in user session"** → `user logoutuser`
20. **"Creates list of users with given input array"** → `user create-2`
21. **"Create user"** → `user create-3`

## Examples

User: "Is swagger-petstore connected?"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py check
```

User: "uploads an image"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py pet upload EXAMPLE_PETID
```

User: "Returns pet inventories by status"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py store get
```

User: "Creates list of users with given input array"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore_cli.py user create
```
