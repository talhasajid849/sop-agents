import json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

with open("invoices.json") as f:
    invoices = json.load(f)

RULES = """You are an Invoice Checker. Rules:
1. The amount must equal the sum of the item prices.
2. No field may be empty.
3. The amount must be a number.
Reply only with JSON: {"is_valid": true/false, "problems": [...]}"""

for inv in invoices:
  response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=2000,
    messages=[{"role": "user", "content": RULES + "\n\nInvoices:\n" + json.dumps(inv)}],
)
  text = next(b.text for b in response.content if b.type == "text")
  print(f"Invoice {inv['id']}: {text}")