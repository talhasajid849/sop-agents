import json
from dotenv import load_dotenv
from google import genai
from google.genai import errors
import time

load_dotenv()
client = genai.Client()

with open("invoices.json") as f:
    invoices = json.load(f)

RULES = """You are an Invoice Checker. Rule:
1. The amount must equal the sum of the item Prices.
2. No field may be empty.
3. The Amount must be a number.
Reply only woth JOSN: {"is_valid": true/false,
"problems": [...]}"""

for inv in invoices:
  for attemp in range(3):
    try:
        reponse = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=RULES + "\n\nInvoices:\n" + json.dumps(inv),
        )
        print(f"Invoice {inv["id"]}: {reponse.text}")
        break
    except errors.ServerError:
        print(f"Invoice {inv['id']}: server busy, 10 sec baad dobara...")
        time.sleep(10)