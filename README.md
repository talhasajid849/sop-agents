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

## Results v1 (4 invoices, corrected prompt)
| Invoice | Rule-based check.py | AI Checker (Gemini) | AI Checker (Claude) |
|---|---|---|---|
| 1 (correct) | OK | OK | OK |
| 2 (empty date) | Rejected | Rejected | Rejected |
| 3 (wrong total) | Rejected | Rejected | Rejected (showed the sum) |
| 4 (10 items, off by 1) | Rejected | Rejected (gave both numbers) | Rejected (found difference of 1) |

Notes:
- All verdicts agree on all 4 invoices.
- Invoice 3: Gemini wrote "expected 1000, got 8000" but did not say which number is the amount and which is the sum. Claude named both numbers clearly.
- Format: both models sometimes wrap the JSON in ```json fences and sometimes don't, despite "Reply only with JSON".
- Gemini free API: sometimes 503 (server busy, a retry loop handles it) and a limit of 20 calls per day.
- Every answer is saved in claude_results.json and gemini_results.json.