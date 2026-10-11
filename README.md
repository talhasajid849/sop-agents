# sop-agents
A small agent team that processes invoices.
Research question: do structured (SOP) agent teams stop checking their own work?

## Agents
- **Extractor**: reads the invoice and pull out the data
- **Checker**: check the data is correct
- **Approver**: approves and reject the invoices

## What each agents Sends
- Extractor → Checker: {vendor, amount, date, items}
- Checker → Approver: {is_valid, problems}

## What the Checker checks
- The total amount equals the sum of the items
- All fields are filled in
- The amount is a valid number
