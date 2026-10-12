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

## Results v0 (3 invoices, corrected prompt)
| Invoice | Rule-based check.py | AI Checker (Gemini) | AI Checker (Claude) |
|---|---|---|---|
| 1 (correct) | OK | OK | OK |
| 2 (empty date) | Rejected | Rejected | Rejected |
| 3 (wrong total) | Rejected | Rejected | Rejected (showed the sum) |

Notes:
- All verdicts agree. In an earlier run (prompt had typos), Gemini worded invoice 3's reason backwards. Same verdict, wrong explanation.
- Format: Gemini wrapped only invoice 3 in ```json fences; Claude wrapped all three, despite "Reply only with JSON".
- Gemini free API sometimes returns 503 (server busy); a retry loop handles it.