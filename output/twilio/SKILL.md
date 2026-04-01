---
name: twilio
description: Interact with twilio-api API. Use for querying, creating, and managing twilio-api resources. Use when asked about twilio-api operations.
argument-hint: [command] [args]
allowed-tools: Bash(python3:*)
---

# Twilio Api Integration

## Configuration

Set these environment variables in `~/.zshrc`:

- `TWILIO_URL` — API base URL (default: `https://api.twilio.com`)
- `TWILIO_TOKEN` — Authentication token

## Available Commands

### Check Connection
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py check
```

### 2010-04-01
```bash
# Retrieves a collection of Accounts belonging to the account used to make the request
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list --FriendlyName VALUE --Status VALUE
# Fetch the account specified by the provided Account Sid
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 fetchaccount SID
# 
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-2 ACCOUNTSID --PageSize VALUE --Page VALUE
# Retrieves a collection of calls made to and from your account
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-3 ACCOUNTSID --To VALUE --From VALUE
# Retrieve a list of queues belonging to the account used to make the request
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-4 ACCOUNTSID --PageSize VALUE --Page VALUE
# Fetch the balance for an Account based on Account Sid. Balance changes may not be reflected immediately. Child accounts do not contain balance information
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 fetchbalance ACCOUNTSID
# Retrieve a list of messages belonging to the account used to make the request
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-5 ACCOUNTSID --To VALUE --From VALUE
# 
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-6 ACCOUNTSID --CustomerName VALUE --FriendlyName VALUE
# 
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 fetchkey ACCOUNTSID SID
# Retrieve a list of recordings belonging to the account used to make the request
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-7 ACCOUNTSID --DateCreated VALUE --DateCreated< VALUE
# Fetch the call specified by the provided Call SID
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 fetchcall ACCOUNTSID SID
# Retrieve a list of conferences belonging to the account used to make the request
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-8 ACCOUNTSID --DateCreated VALUE --DateCreated< VALUE
# Retrieve a list of connect-apps belonging to the account used to make the request
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-9 ACCOUNTSID --PageSize VALUE --Page VALUE
# Retrieve a list of domains belonging to the account used to make the request
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-10 ACCOUNTSID --PageSize VALUE --Page VALUE
# 
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-11 ACCOUNTSID --PageSize VALUE --Page VALUE
# Retrieve a list of applications representing an application within the requesting account
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-12 ACCOUNTSID --FriendlyName VALUE --PageSize VALUE
# Fetch an instance of a queue identified by the QueueSid
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 fetchqueue ACCOUNTSID SID
# Retrieve a list of notifications belonging to the account used to make the request
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-13 ACCOUNTSID --Log VALUE --MessageDate VALUE
# Retrieve a list of usage-records belonging to the account used to make the request
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-14 ACCOUNTSID --Category VALUE --StartDate VALUE
# Fetch a message belonging to the account used to make the request
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 fetchmessage ACCOUNTSID SID
# Retrieve a list of short-codes belonging to the account used to make the request
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-15 ACCOUNTSID --FriendlyName VALUE --ShortCode VALUE
# Retrieve a list of transcriptions belonging to the account used to make the request
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-16 ACCOUNTSID --PageSize VALUE --Page VALUE
# Retrieve a list of usage-triggers belonging to the account used to make the request
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-17 ACCOUNTSID --Recurring VALUE --TriggerBy VALUE
# 
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 fetchaddress ACCOUNTSID SID
# Fetch an instance of a recording
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 fetchrecording ACCOUNTSID SID --IncludeSoftDeleted VALUE
# Fetch an instance of a conference
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 fetchconference ACCOUNTSID SID
# Fetch an instance of a connect-app
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 fetchconnectapp ACCOUNTSID SID
# Retrieve a list of outgoing-caller-ids belonging to the account used to make the request
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list-18 ACCOUNTSID --PhoneNumber VALUE --FriendlyName VALUE
# Fetch an instance of a Domain
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 fetchsipdomain ACCOUNTSID SID
# 
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 fetchsigningkey ACCOUNTSID SID
```

## Usage Instructions

Map user requests to commands:

1. **"Is twilio-api reachable?"** / **"Test connection"** → `check`
2. **"Retrieves a collection of Accounts belonging to the account used to make the request"** → `2010-04-01 list --FriendlyName VALUE`
3. **"Fetch the account specified by the provided Account Sid"** → `2010-04-01 fetchaccount SID`
4. **""** → `2010-04-01 list-2 ACCOUNTSID --PageSize VALUE`
5. **"Retrieves a collection of calls made to and from your account"** → `2010-04-01 list-3 ACCOUNTSID --To VALUE`
6. **"Retrieve a list of queues belonging to the account used to make the request"** → `2010-04-01 list-4 ACCOUNTSID --PageSize VALUE`
7. **"Fetch the balance for an Account based on Account Sid. Balance changes may not be reflected immediately. Child accounts do not contain balance information"** → `2010-04-01 fetchbalance ACCOUNTSID`
8. **"Retrieve a list of messages belonging to the account used to make the request"** → `2010-04-01 list-5 ACCOUNTSID --To VALUE`
9. **""** → `2010-04-01 list-6 ACCOUNTSID --CustomerName VALUE`
10. **""** → `2010-04-01 fetchkey ACCOUNTSID SID`
11. **"Retrieve a list of recordings belonging to the account used to make the request"** → `2010-04-01 list-7 ACCOUNTSID --DateCreated VALUE`
12. **"Fetch the call specified by the provided Call SID"** → `2010-04-01 fetchcall ACCOUNTSID SID`
13. **"Retrieve a list of conferences belonging to the account used to make the request"** → `2010-04-01 list-8 ACCOUNTSID --DateCreated VALUE`
14. **"Retrieve a list of connect-apps belonging to the account used to make the request"** → `2010-04-01 list-9 ACCOUNTSID --PageSize VALUE`
15. **"Retrieve a list of domains belonging to the account used to make the request"** → `2010-04-01 list-10 ACCOUNTSID --PageSize VALUE`
16. **""** → `2010-04-01 list-11 ACCOUNTSID --PageSize VALUE`
17. **"Retrieve a list of applications representing an application within the requesting account"** → `2010-04-01 list-12 ACCOUNTSID --FriendlyName VALUE`
18. **"Fetch an instance of a queue identified by the QueueSid"** → `2010-04-01 fetchqueue ACCOUNTSID SID`
19. **"Retrieve a list of notifications belonging to the account used to make the request"** → `2010-04-01 list-13 ACCOUNTSID --Log VALUE`
20. **"Retrieve a list of usage-records belonging to the account used to make the request"** → `2010-04-01 list-14 ACCOUNTSID --Category VALUE`
21. **"Fetch a message belonging to the account used to make the request"** → `2010-04-01 fetchmessage ACCOUNTSID SID`
22. **"Retrieve a list of short-codes belonging to the account used to make the request"** → `2010-04-01 list-15 ACCOUNTSID --FriendlyName VALUE`
23. **"Retrieve a list of transcriptions belonging to the account used to make the request"** → `2010-04-01 list-16 ACCOUNTSID --PageSize VALUE`
24. **"Retrieve a list of usage-triggers belonging to the account used to make the request"** → `2010-04-01 list-17 ACCOUNTSID --Recurring VALUE`
25. **""** → `2010-04-01 fetchaddress ACCOUNTSID SID`
26. **"Fetch an instance of a recording"** → `2010-04-01 fetchrecording ACCOUNTSID SID --IncludeSoftDeleted VALUE`
27. **"Fetch an instance of a conference"** → `2010-04-01 fetchconference ACCOUNTSID SID`
28. **"Fetch an instance of a connect-app"** → `2010-04-01 fetchconnectapp ACCOUNTSID SID`
29. **"Retrieve a list of outgoing-caller-ids belonging to the account used to make the request"** → `2010-04-01 list-18 ACCOUNTSID --PhoneNumber VALUE`
30. **"Fetch an instance of a Domain"** → `2010-04-01 fetchsipdomain ACCOUNTSID SID`
31. **""** → `2010-04-01 fetchsigningkey ACCOUNTSID SID`

## Examples

User: "Is twilio-api connected?"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py check
```

User: "Retrieves a collection of Accounts belonging to the account used to make the request"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/twilio_cli.py 2010-04-01 list
```
