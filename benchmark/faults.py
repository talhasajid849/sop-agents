from decimal import ROUND_HALF_UP, Decimal
from sop_agents.schemas import Invoice, LineItem
from datetime import date

REQUIRED_FIELDS = ["invoice_number", "vendor_name", "buyer_name", "invoice_date"]


def money(x):
    """Round to 2 decimals, the way invoices are written."""
    return Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def find_violations(inv: Invoice) -> list[str]:
    """Check the 5 SOP rules. Return the broken rule. Enpty list = valid invoice"""
    broken = []

    # R1: required fields must not be blank
    for field in REQUIRED_FIELDS:
        if getattr(inv, field) in (None, ""):
            broken.append(f"R1: {field} is blank")

    # R1: each line: amount == quantity * unit_price
    for i, line in enumerate(inv.line_items):
        if line.amount != money(line.quantity * line.unit_price):
            broken.append(f"R2: line {i + 1} amount is wrong")

    # R3: subtotal == sum of line amount
    if inv.subtotal != money(sum(line.amount for line in inv.line_items)):
        broken.append("R3: subtotal is wrong")

    # R4: tax = taxrate * subtotal 
    if inv.tax != money(inv.subtotal * inv.tax_rate_percent / 100):
        broken.append("R4: tax is wrong")

    #R5: total = subtotal + tax
    if inv.total != inv.subtotal + inv.tax:
        broken.append("R5: total is wrong")

    return broken

def inject_off_by_one(inv: Invoice) -> Invoice:
    """Plan the one mistake and make the totoal wring by 1.0"""
    return inv.model_copy(update={"total": inv.total + Decimal("1.0")})

def inject_missing_fields(inv: Invoice, fields: str) -> Invoice:
    """Plant one mistake: leave one required fields blank."""
    return inv.model_copy(update={fields: None})


def inject_total_mismatch(inv: Invoice, percent: int) -> Invoice:
    """Plant one mistake: make the total wrong by the percent"""
    wrong = money(inv.total * (100 + percent) / 100)
    return inv.model_copy(update={"total": wrong})


def inject_line_item_error(inv: Invoice, index: int, extra: str) -> Invoice:
    """Plant one mistake: one line amount is wrong, but the total still add up."""
    items = list(inv.line_items)
    items[index] = items[index].model_copy(update={"amount": items[index].amount + Decimal(extra)})
    subtotal = sum(line.amount for line in items)
    tax = money(subtotal * inv.tax_rate_percent / 100)
    return inv.model_copy(update={
        "line_items": items,
        "subtotal": subtotal,
        "tax": tax,
        "total": subtotal + tax,
    })

if __name__ == "__main__":
    good = Invoice(
        invoice_number="INV-001",
        vendor_name="Ravi Paper Mills",
        buyer_name="Vehari Agro Traders",
        invoice_date=date(2026, 10, 16),
        currency="PKR",
        line_items=[
            LineItem(description="A4 paper", quantity=10, unit_price=Decimal("850.00"), amount=Decimal("8500.00")),
            LineItem(description="USB-C cable", quantity=2, unit_price=Decimal("450.00"), amount=Decimal("900.00")),
        ],
        subtotal=Decimal("9400.00"),
        tax_rate_percent=Decimal("17"),
        tax=Decimal("1598.00"),
        total=Decimal("10998.00"),
    )
    print("good invoice:", find_violations(good))

    bad = inject_off_by_one(good)
    print("bad total:   ", bad.total)
    print("bad invoice: ", find_violations(bad))

    missing = inject_missing_fields(good, "invoice_date")
    print("missing date:", find_violations(missing))

    big = inject_total_mismatch(good, 30)
    print("big mitchmatch:", big.total, find_violations(big))

    line_bad = inject_line_item_error(good, 0, "500.00")
    print("line error: ", find_violations(line_bad))