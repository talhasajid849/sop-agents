import random
from datetime import date, timedelta
from decimal import Decimal

from sop_agents.schemas import Invoice, LineItem
from benchmark.faults import (
    REQUIRED_FIELDS,
    find_violations,
    inject_line_item_error,
    inject_missing_fields,
    inject_off_by_one,
    inject_total_mismatch,
    money,
)

import json
from pathlib import Path

VENDORS = ["Ravi Paper Mills", "Indus Office Supplies", "Margalla Tech Services", "Chenab Textiles"]
BUYERS = ["Vehari Agro Traders", "Lahore Software House", "Multan Medical Store"]
PRODUCTS = [
    ("A4 paper ream", 850),
    ("USB-C cable", 450),
    ("Office chair", 18000),
    ("Network switch", 14500),
    ("Printer toner", 6200),
]


def make_clean_invoice(rng: random.Random, number: int) -> Invoice:
    """Build one correct invoice form the random choices."""
    items = []
    for description , price in rng.sample(PRODUCTS, 3):
        quantity = rng.randint(1, 20)
        unit_price = money(price)
        items.append(
            LineItem(
                description=description,
                quantity=quantity,
                unit_price=unit_price,
                amount=money(quantity * unit_price)
            )
        )
    subtotal = sum(line.amount for line in items)
    rate = Decimal(rng.choice([0, 5, 10, 17]))
    tax = money(rate * subtotal / 100)
    return Invoice(
        invoice_number=f"INV-{number:03d}",
        vendor_name=rng.choice(VENDORS),
        buyer_name=rng.choice(BUYERS),
        invoice_date=date(2026, 1, 1) + timedelta(days=rng.randint(0, 270)),
        currency="PKR",
        line_items=items,
        subtotal=Decimal(subtotal),
        tax_rate_percent=rate,
        tax=tax,
        total=subtotal + tax,
    )


def built_dataset(n_clean: int, n_each: int, seed: int) -> list[tuple[Invoice, str]]:
    """Make the exam: clean invoice plus n_each invoice for every kind of the mistake."""
    rng = random.Random(seed)
    plan = ["none"] * n_clean
    for fault in ["off_by_one", "missing_field", "total_mismatch", "line_item"]:
        plan += [fault] * n_each
    rng.shuffle(plan)

    dataset = []
    for number, fault in enumerate(plan, start=1):
        inv = make_clean_invoice(rng, number)
        if fault == "off_by_one":
            inv = inject_off_by_one(inv)
        elif fault == "missing_field":
            inv = inject_missing_fields(inv, rng.choice(REQUIRED_FIELDS))
        elif fault == "total_mismatch":
            inv = inject_total_mismatch(inv, rng.choice([10, 20, 30, 40, 50]))
        elif fault == "line_item":
            inv = inject_line_item_error(inv, rng.randrange(3), rng.choice(["100.00", "250.00", "500.00"]))
        # safety check: only "none" invoices may be free of broken rules
        assert (find_violations(inv) == []) == (fault == "none"), (number, fault)
        dataset.append((inv, fault))
    return dataset


def show(value) -> str:
    """Blank fields are printed as empty text."""
    return "" if value is None else str(value)


def render_document(inv: Invoice) -> str:
    """Turn an invoice into the plain text that an AI agent will read."""
    lines = [
        "INVOICE",
        f"Invoice No: {show(inv.invoice_number)}",
        f"Date: {show(inv.invoice_date)}",
        f"From: {show(inv.vendor_name)}",
        f"Bill To: {show(inv.buyer_name)}",
        f"Currency: {inv.currency}",
        "",
    ]
    for number, line in enumerate(inv.line_items, start=1):
        lines.append(
            f"{number}. {line.description} | qty {line.quantity} | "
            f"price {line.unit_price:,.2f} | amount {line.amount:,.2f}"
        )
    lines += [
        "",
        f"Subtotal: {inv.subtotal:,.2f}",
        f"Tax ({inv.tax_rate_percent}%): {inv.tax:,.2f}",
        f"TOTAL ({inv.currency}): {inv.total:,.2f}",
    ]
    return "\n".join(lines)


def write_tasks(dataset: list[tuple[Invoice, str]], path: str) -> None:
    """Save the exam: one line of JSON per invoice, with the correct answer."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for number, (inv, fault) in enumerate(dataset, start=1):
            record = {
                "task_id": f"v1-{number:03d}",
                "document": render_document(inv),
                "truth": inv.model_dump(mode="json"),
                "fault": fault,
                "correct_verdict": "accept" if fault == "none" else "reject",
            }
            f.write(json.dumps(record) + "\n")



if __name__ == "__main__":
    dataset = built_dataset(n_clean=12, n_each=7, seed=42)
    print("total invoices:", len(dataset))
    for fault in ["none", "off_by_one", "missing_field", "total_mismatch", "line_item"]:
        print(fault, sum(1 for _, f in dataset if f == fault))
    print("first five:", [f for _, f in dataset[:5]])

    inv, fault = dataset[3]
    print("--- invoice 4, planted mistake:", fault)
    print(render_document(inv))

    write_tasks(dataset, "benchmark/datasets/v1/tasks.jsonl")
    print("saved benchmark/datasets/v1/tasks.jsonl")