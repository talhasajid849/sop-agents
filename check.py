import json

with open("invoices.json") as f:
    invoices = json.load(f)

for inv in invoices:
    problems = []
    total = sum(item["price"] for item in inv["items"])
    for key, value in inv.items():
        if(value == ""):
            problems.append(f"{key} is empty.")
    if total != inv["amount"]:
        problems.append(f"WRONG, items = {total}, amount = {inv["amount"]}")

    if problems:
        print(f"Invoice {inv["id"]}: REJECT -> {problems}")
    else:
        print(f"Invoice {inv["id"]}: OK")