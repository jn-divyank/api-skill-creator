---
name: stripe
description: Interact with stripe-api API. Use for querying, creating, and managing stripe-api resources. Use when asked about stripe-api operations.
argument-hint: [command] [args]
allowed-tools: Bash(python3:*)
---

# Stripe Api Integration

## Configuration

Set these environment variables in `~/.zshrc`:

- `STRIPE_URL` — API base URL (default: `https://api.stripe.com/`)
- `STRIPE_TOKEN` — Authentication token

## Available Commands

### Check Connection
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py check
```

### Account
```bash
# Retrieve account
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py account get --expand VALUE
```

### Accounts
```bash
# List all connected accounts
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py accounts get --created VALUE --ending-before VALUE
```

### Apps
```bash
# List secrets
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py apps get --ending-before VALUE --expand VALUE
```

### Balance
```bash
# Retrieve balance
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py balance get --expand VALUE
```

### Charges
```bash
# List all charges
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py charges get --created VALUE --customer VALUE
```

### Coupons
```bash
# List all coupons
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py coupons get --created VALUE --ending-before VALUE
```

### Credit-Notes
```bash
# List all credit notes
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py credit-notes get --created VALUE --customer VALUE
```

### Customers
```bash
# List all customers
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py customers get --created VALUE --email VALUE
```

### Disputes
```bash
# List all disputes
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py disputes get --charge VALUE --created VALUE
```

### Events
```bash
# List all events
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py events get --created VALUE --delivery-success VALUE
# Retrieve an event
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py events get-2 ID --expand VALUE
```

### File-Links
```bash
# List all file links
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py file-links get --created VALUE --ending-before VALUE
```

### Files
```bash
# List all files
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py files get --created VALUE --ending-before VALUE
# Retrieve a file
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py files get-2 FILE --expand VALUE
```

### Invoiceitems
```bash
# List all invoice items
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py invoiceitems get --created VALUE --customer VALUE
```

### Invoices
```bash
# List all invoices
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py invoices get --collection-method VALUE --created VALUE
```

### Payouts
```bash
# List all payouts
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py payouts get --arrival-date VALUE --created VALUE
```

### Plans
```bash
# List all plans
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py plans get --active VALUE --created VALUE
# Retrieve a plan
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py plans get-2 PLAN --expand VALUE
```

### Prices
```bash
# List all prices
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py prices get --active VALUE --created VALUE
```

### Products
```bash
# List all products
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py products get --active VALUE --created VALUE
```

### Quotes
```bash
# List all quotes
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py quotes get --customer VALUE --customer-account VALUE
```

### Refunds
```bash
# List all refunds
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py refunds get --charge VALUE --created VALUE
```

### Reviews
```bash
# List all open reviews
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py reviews get --created VALUE --ending-before VALUE
```

### Tax
```bash
# Retrieve settings
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py tax get --expand VALUE
```

### Tax-Codes
```bash
# List all tax codes
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py tax-codes get --ending-before VALUE --expand VALUE
```

### Tax-Ids
```bash
# List all tax IDs
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py tax-ids get --ending-before VALUE --expand VALUE
```

### Tax-Rates
```bash
# List all tax rates
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py tax-rates get --active VALUE --created VALUE
```

### Topups
```bash
# List all top-ups
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py topups get --amount VALUE --created VALUE
```

### Transfers
```bash
# List all transfers
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py transfers get --created VALUE --destination VALUE
```

## Usage Instructions

Map user requests to commands:

1. **"Is stripe-api reachable?"** / **"Test connection"** → `check`
2. **"Retrieve account"** → `account get --expand VALUE`
3. **"List all connected accounts"** → `accounts get --created VALUE`
4. **"List secrets"** → `apps get --ending-before VALUE`
5. **"Retrieve balance"** → `balance get --expand VALUE`
6. **"List all charges"** → `charges get --created VALUE`
7. **"List all coupons"** → `coupons get --created VALUE`
8. **"List all credit notes"** → `credit-notes get --created VALUE`
9. **"List all customers"** → `customers get --created VALUE`
10. **"List all disputes"** → `disputes get --charge VALUE`
11. **"List all events"** → `events get --created VALUE`
12. **"Retrieve an event"** → `events get-2 ID --expand VALUE`
13. **"List all file links"** → `file-links get --created VALUE`
14. **"List all files"** → `files get --created VALUE`
15. **"Retrieve a file"** → `files get-2 FILE --expand VALUE`
16. **"List all invoice items"** → `invoiceitems get --created VALUE`
17. **"List all invoices"** → `invoices get --collection-method VALUE`
18. **"List all payouts"** → `payouts get --arrival-date VALUE`
19. **"List all plans"** → `plans get --active VALUE`
20. **"Retrieve a plan"** → `plans get-2 PLAN --expand VALUE`
21. **"List all prices"** → `prices get --active VALUE`
22. **"List all products"** → `products get --active VALUE`
23. **"List all quotes"** → `quotes get --customer VALUE`
24. **"List all refunds"** → `refunds get --charge VALUE`
25. **"List all open reviews"** → `reviews get --created VALUE`
26. **"Retrieve settings"** → `tax get --expand VALUE`
27. **"List all tax codes"** → `tax-codes get --ending-before VALUE`
28. **"List all tax IDs"** → `tax-ids get --ending-before VALUE`
29. **"List all tax rates"** → `tax-rates get --active VALUE`
30. **"List all top-ups"** → `topups get --amount VALUE`
31. **"List all transfers"** → `transfers get --created VALUE`

## Examples

User: "Is stripe-api connected?"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py check
```

User: "Retrieve account"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py account get
```

User: "List all connected accounts"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py accounts get
```

User: "List secrets"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py apps get
```

User: "Retrieve balance"
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/stripe_cli.py balance get
```
