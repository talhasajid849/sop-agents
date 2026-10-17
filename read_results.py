import json

with open("claude_results.json") as f:
    results = json.load(f)


expected = {1: True, 2: False, 3: False, 4: False}
correct = 0
for r in results:
    text = r["answer"].replace("```json", "").replace("```", "").strip()
    data = json.loads(text)
    if data["is_valid"] == expected[r["invoice_id"]]:
        correct += 1
        print(r["invoice_id"], "correct")
    else:
        print(r["invoice_id"], "WRONG")

print(f"Score: {correct} / {len(results)}")