---
name: petstore3
description: Interact with swagger-petstore-openapi-3-0 API. Use for querying, creating, and managing swagger-petstore-openapi-3-0 resources. Use when asked about swagger-petstore-openapi-3-0 operations.
argument-hint: [command] [args]
allowed-tools: Bash(python3:*)
---

# Swagger Petstore Openapi 3 0 Integration

## Configuration

Set these environment variables in `~/.zshrc`:

- `PETSTORE3_URL` — API base URL (default: `/api/v3`)
- `PETSTORE3_TOKEN` — Authentication token

## Available Commands

### Check Connection
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py check
```

### Pet
```bash
# Update an existing pet.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py pet update
# Add a new pet to the store.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py pet add
# Finds Pets by status.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py pet list --status VALUE
# Finds Pets by tags.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py pet list-2 --tags VALUE
# Find pet by ID.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py pet get PETID
# Updates a pet in the store with form data.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py pet update-2 PETID --name VALUE --status VALUE
# Deletes a pet.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py pet delete PETID
# Uploads an image.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py pet upload PETID --additionalMetadata VALUE
```

### Store
```bash
# Returns pet inventories by status.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py store get
# Place an order for a pet.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py store placeorder
# Find purchase order by ID.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py store get-2 ORDERID
# Delete purchase order by identifier.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py store delete ORDERID
```

### User
```bash
# Create user.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py user create
# Creates list of users with given input array.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py user create-2
# Logs user into the system.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py user loginuser --username VALUE --password VALUE
# Logs out current logged in user session.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py user logoutuser
# Get user by user name.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py user get USERNAME
# Update user resource.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py user update USERNAME
# Delete user resource.
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py user delete USERNAME
```

## Usage Instructions

Map user requests to commands:

1. **"Is swagger-petstore-openapi-3-0 reachable?"** / **"Test connection"** → `check`
2. **"Update an existing pet."** → `pet update`
3. **"Add a new pet to the store."** → `pet add`
4. **"Finds Pets by status."** → `pet list --status VALUE`
5. **"Finds Pets by tags."** → `pet list-2 --tags VALUE`
6. **"Find pet by ID."** → `pet get PETID`
7. **"Updates a pet in the store with form data."** → `pet update-2 PETID --name VALUE`
8. **"Deletes a pet."** → `pet delete PETID`
9. **"Uploads an image."** → `pet upload PETID --additionalMetadata VALUE`
10. **"Returns pet inventories by status."** → `store get`
11. **"Place an order for a pet."** → `store placeorder`
12. **"Find purchase order by ID."** → `store get-2 ORDERID`
13. **"Delete purchase order by identifier."** → `store delete ORDERID`
14. **"Create user."** → `user create`
15. **"Creates list of users with given input array."** → `user create-2`
16. **"Logs user into the system."** → `user loginuser --username VALUE`
17. **"Logs out current logged in user session."** → `user logoutuser`
18. **"Get user by user name."** → `user get USERNAME`
19. **"Update user resource."** → `user update USERNAME`
20. **"Delete user resource."** → `user delete USERNAME`

## Examples

User: "Is swagger-petstore-openapi-3-0 connected?"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py check
```

User: "Update an existing pet."
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py pet update
```

User: "Returns pet inventories by status."
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py store get
```

User: "Create user."
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/petstore3_cli.py user create
```
