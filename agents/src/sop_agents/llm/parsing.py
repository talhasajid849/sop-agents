from pydantic import ValidationError
from sop_agents.schemas import Invoice


def strip_fence(text: str) -> str:
    """Remove a ```json ... ``` wrapper if the model added one. """
    text.strip()
    if text.startswith("```"):
        text = text.removeprefix("```json").removeprefix("```")
        text = text.removesuffix("```")
    return text.strip()


def parse_invoice(text: str) -> Invoice:
    """Turn the model text into a checked Invoice obj. """
    return Invoice.model_validate_json(strip_fence(text))



if __name__ == "__main__":
    raw = (
        '{"invoice_number": "INV-001", "vendor_name": "Ravi", "buyer_name": "V",'
        ' "invoice_date": "2026-10-16", "currency": "PKR",'
        ' "line_items": [{"description": "A4", "quantity": 2, "unit_price": "100.00", "amount": "200.00"}],'
        ' "subtotal": "200.00", "tax_rate_percent": "0", "tax": "0.00", "total": "200.00"}'
    )
    print("plain:  ", parse_invoice(raw).invoice_number)
    print("fenced: ", parse_invoice("```json\n" + raw + "\n```").invoice_number)
    try:
        parse_invoice("I think the invoice is fine")
    except ValidationError as e:
        print("bad answer caught:", e.error_count(), "problem")