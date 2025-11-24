from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from math import floor

app = FastAPI()

class CartItem(BaseModel):
    product_id: str
    qty: int
    unit_price: float

class Discount(BaseModel):
    type: str                     # "percentage", "fixed_amount", "buy_x_get_y"
    value: Optional[float] = None
    product_id: Optional[str] = None
    x: Optional[int] = None
    y: Optional[int] = None

class PriceRequest(BaseModel):
    items: List[CartItem]
    discounts: List[Discount]


@app.post("/price")
def calculate_price(req: PriceRequest):
    # Calculate subtotal
    subtotal = sum(item.qty * item.unit_price for item in req.items)
    discount_total = 0
    applied = []

    # Apply discounts
    for d in req.discounts:
        if d.type == "percentage":
            discount_total += subtotal * (d.value / 100)
            applied.append("percentage")

        elif d.type == "fixed_amount":
            discount_total += d.value
            applied.append("fixed_amount")

        elif d.type == "buy_x_get_y":
            for item in req.items:
                if item.product_id == d.product_id:
                    free_units = floor(item.qty / (d.x + d.y)) * d.y
                    discount_total += free_units * item.unit_price
                    applied.append("buy_x_get_y")

    final_price = subtotal - discount_total
    if final_price < 0:
        final_price = 0

    return {
        "subtotal": round(subtotal, 2),
        "discount_total": round(discount_total, 2),
        "final_price": round(final_price, 2),
        "applied_discounts": applied,
    }
