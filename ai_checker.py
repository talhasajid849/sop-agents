import json
from dotenv import load_dotenv
from google import genai
from google.genai import errors
import time

load_dotenv()
client = genai.Client()

with open("invoices.json") as f:
    invoices = json.load(f)

RULES = """You are an Invoice Checker. Rules:
1. The amount must equal the sum of the item prices.
2. No field may be empty.
3. The amount must be a number.
Reply only with JSON: {"is_valid": true/false, "problems": [...]}"""

results = []
for inv in invoices:
  for attemp in range(3):
    try:
        reponse = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=RULES + "\n\nInvoices:\n" + json.dumps(inv),
        )
        print(f"Invoice {inv["id"]}: {reponse.text}")
        results.append({"invoice_id": inv["id"], "model": "gemini-3.8-flash", "answer": reponse.text})
        break
    except errors.ServerError:
        print(f"Invoice {inv['id']}: server busy, 10 sec baad dobara...")
        time.sleep(10)


with open("gemini_results.json", "w") as f:
    json.dump(results, f, indent=2)