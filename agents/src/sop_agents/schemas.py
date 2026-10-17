from decimal import Decimal
from pydantic import BaseModel
from typing import Optional
from datetime import date


class LineItem(BaseModel):
    description: str
    quantity: int
    unit_price: Decimal
    amount: Decimal

class Invoice(BaseModel):
    invoice_number: Optional[str]
    vendor_name: Optional[str]
    buyer_name: Optional[str]
    invoice_date: Optional[date]
    currency: str
    line_items: list[LineItem]
    subtotal: Decimal
    tax_rate_percent: Decimal
    tax: Decimal
    total: Decimal

