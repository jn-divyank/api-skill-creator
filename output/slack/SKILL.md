---
name: slack
description: Interact with slack-web-api API. Use for querying, creating, and managing slack-web-api resources. Use when asked about slack-web-api operations.
argument-hint: [command] [args]
allowed-tools: Bash(python3:*)
---

# Slack Web Api Integration

## Configuration

Set these environment variables in `~/.zshrc`:

- `SLACK_URL` — API base URL (default: `https://slack.com/api`)
- `SLACK_TOKEN` — Authentication token

## Available Commands

### Check Connection
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py check
```

### Api
```bash
# Checks API calling code.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py api api-test --error VALUE --foo VALUE
```

### Apps
```bash
# Uninstalls your app from a workspace.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py apps apps-uninstall --token VALUE --client-id VALUE
```

### Auth
```bash
# Checks authentication & identity.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py auth auth-test
# Revokes a token.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py auth auth-revoke --token VALUE --test VALUE
```

### Bots
```bash
# Gets information about a bot user.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py bots bots-info --token VALUE --bot VALUE
```

### Calls
```bash
# Returns information about a Call.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py calls calls-info --id VALUE
```

### Dialog
```bash
# Open a dialog with a user
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py dialog dialog-open --dialog VALUE --trigger-id VALUE
```

### Dnd
```bash
# Retrieves a user's current Do Not Disturb status.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py dnd dnd-info --token VALUE --user VALUE
# Retrieves the Do Not Disturb status for up to 50 users on a team.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py dnd dnd-teaminfo --token VALUE --users VALUE
```

### Emoji
```bash
# Lists custom emoji for a team.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py emoji emoji-list --token VALUE
```

### Files
```bash
# Gets information about a file.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py files files-info --token VALUE --file VALUE
# List for a team, in a channel, or from a user with applied filters.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py files files-list --token VALUE --user VALUE
```

### Oauth
```bash
# Exchanges a temporary OAuth verifier code for a workspace token.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py oauth oauth-token --client-id VALUE --client-secret VALUE
# Exchanges a temporary OAuth verifier code for an access token.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py oauth oauth-access --client-id VALUE --client-secret VALUE
```

### Oauth-V2
```bash
# Exchanges a temporary OAuth verifier code for an access token.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py oauth-v2 oauth-v2-access --client-id VALUE --client-secret VALUE
```

### Pins
```bash
# Lists items pinned to a channel.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py pins pins-list --token VALUE --channel VALUE
```

### Reactions
```bash
# Gets reactions for an item.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py reactions reactions-get --token VALUE --channel VALUE
# Lists reactions made by a user.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py reactions reactions-list --token VALUE --user VALUE
```

### Reminders
```bash
# Gets information about a reminder.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py reminders reminders-info --token VALUE --reminder VALUE
# Lists all reminders created by or for a given user.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py reminders reminders-list --token VALUE
```

### Rtm
```bash
# Starts a Real Time Messaging session.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py rtm rtm-connect --token VALUE --batch-presence-aware VALUE
```

### Stars
```bash
# Lists stars for a user.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py stars stars-list --token VALUE --count VALUE
```

### Team
```bash
# Gets information about the current team.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py team team-info --token VALUE --team VALUE
```

### Users
```bash
# Gets information about a user.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py users users-info --token VALUE --include-locale VALUE
# Lists all users in a Slack team.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py users users-list --token VALUE --limit VALUE
# Get a user's identity.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py users users-identity --token VALUE
```

### Views
```bash
# Open a view for a user.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py views views-open --trigger-id VALUE --view VALUE
# Push a view onto the stack of a root view.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py views views-push --trigger-id VALUE --view VALUE
# Update an existing view.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py views views-update --view-id VALUE --external-id VALUE
# Publish a static view for a User.
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py views views-publish --user-id VALUE --view VALUE
```

## Usage Instructions

Map user requests to commands:

1. **"Is slack-web-api reachable?"** / **"Test connection"** → `check`
2. **"Checks API calling code."** → `api api-test --error VALUE`
3. **"Uninstalls your app from a workspace."** → `apps apps-uninstall --token VALUE`
4. **"Checks authentication & identity."** → `auth auth-test`
5. **"Revokes a token."** → `auth auth-revoke --token VALUE`
6. **"Gets information about a bot user."** → `bots bots-info --token VALUE`
7. **"Returns information about a Call."** → `calls calls-info --id VALUE`
8. **"Open a dialog with a user"** → `dialog dialog-open --dialog VALUE`
9. **"Retrieves a user's current Do Not Disturb status."** → `dnd dnd-info --token VALUE`
10. **"Retrieves the Do Not Disturb status for up to 50 users on a team."** → `dnd dnd-teaminfo --token VALUE`
11. **"Lists custom emoji for a team."** → `emoji emoji-list --token VALUE`
12. **"Gets information about a file."** → `files files-info --token VALUE`
13. **"List for a team, in a channel, or from a user with applied filters."** → `files files-list --token VALUE`
14. **"Exchanges a temporary OAuth verifier code for a workspace token."** → `oauth oauth-token --client-id VALUE`
15. **"Exchanges a temporary OAuth verifier code for an access token."** → `oauth oauth-access --client-id VALUE`
16. **"Exchanges a temporary OAuth verifier code for an access token."** → `oauth-v2 oauth-v2-access --client-id VALUE`
17. **"Lists items pinned to a channel."** → `pins pins-list --token VALUE`
18. **"Gets reactions for an item."** → `reactions reactions-get --token VALUE`
19. **"Lists reactions made by a user."** → `reactions reactions-list --token VALUE`
20. **"Gets information about a reminder."** → `reminders reminders-info --token VALUE`
21. **"Lists all reminders created by or for a given user."** → `reminders reminders-list --token VALUE`
22. **"Starts a Real Time Messaging session."** → `rtm rtm-connect --token VALUE`
23. **"Lists stars for a user."** → `stars stars-list --token VALUE`
24. **"Gets information about the current team."** → `team team-info --token VALUE`
25. **"Gets information about a user."** → `users users-info --token VALUE`
26. **"Lists all users in a Slack team."** → `users users-list --token VALUE`
27. **"Get a user's identity."** → `users users-identity --token VALUE`
28. **"Open a view for a user."** → `views views-open --trigger-id VALUE`
29. **"Push a view onto the stack of a root view."** → `views views-push --trigger-id VALUE`
30. **"Update an existing view."** → `views views-update --view-id VALUE`
31. **"Publish a static view for a User."** → `views views-publish --user-id VALUE`

## Examples

User: "Is slack-web-api connected?"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py check
```

User: "Checks API calling code."
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py api api-test
```

User: "Uninstalls your app from a workspace."
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py apps apps-uninstall
```

User: "Checks authentication & identity."
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py auth auth-test
```

User: "Gets information about a bot user."
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/slack_cli.py bots bots-info
```
