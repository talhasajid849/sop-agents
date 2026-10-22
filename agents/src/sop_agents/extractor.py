import json

from pydantic import ValidationError

from sop_agents.llm.base import LLMClient, LLMResponse
from sop_agents.llm.fake import FakeLLM
from sop_agents.llm.parsing import parse_invoice
from sop_agents.schemas import Invoice

INSTRUCTIONS = """You are an invoice extractor. Read the invoice below and return ONLY one JSON object.
Copy every value exactly as printed. Do not fix mistakes. Do not add comments.
If a field is blank on the invoice, use null.

Fields:
invoice_number, vendor_name, buyer_name: text or null
invoice_date: YYYY-MM-DD or null
currency: 3-letter code
line_items: list of objects with description, quantity (whole number), unit_price, amount
subtotal, tax_rate_percent, tax, total
All money values are strings with 2 decimals, like "850.00"."""

def build_prompt(document: str) -> str:
    return INSTRUCTIONS + "\n\nINVOICE:\n" + document

def extract(client: LLMClient, document: str) -> tuple[Invoice | None, LLMResponse]:
    """Ask the AI to read one invoice. Returns the Invoice (or None if the answer was bad) and the raw response."""
    response = client.complete(build_prompt(document))
    try:
        invoice = parse_invoice(response.text)
    except ValidationError:
        invoice = None
    return invoice, response

if __name__ == "__main__":
    with open("benchmark/datasets/v1/tasks.jsonl", encoding="utf-8") as f:
        task = json.loads(f.readline())

    client = FakeLLM(json.dumps(task["truth"]))
    invoice, response = extract(client, task["document"])
    print("task:", task["task_id"])
    print("got an invoice:", invoice is not None)
    print("same as truth:", invoice == Invoice.model_validate(task["truth"]))
    print("input words:", response.input_tokens)

    bad_client = FakeLLM("sorry, I cannot read this")
    invoice, response = extract(bad_client, task["document"])
    print("bad answer gives:", invoice)