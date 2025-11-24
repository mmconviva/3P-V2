from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from math import floor

import unittest

app = FastAPI()

# You are working on Shopify’s Cart & Discounts team.
# Merchants complain that their discount rules don’t always apply correctly at checkout — especially when multiple discount types overlap (coupon codes, automatic discounts, quantity breaks, etc.)
# Your task is to implement a simplified discount engine that:

# Accepts a cart with multiple items
# Applies one or more discount rules
# Returns the final price, savings, and applied rules

# Create discount schemes
# Add Cart Items
# Apply discounts
# Validate with test cases


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

#  Create Items
items = [
    CartItem(product_id = "shirt-001", qty= 2, unit_price= 25.99),
    CartItem(product_id= "hat-002", qty= 1, unit_price= 15.50),
    CartItem(product_id= "shoes-003", qty= 1, unit_price= 79.99)
    ]
#  Create Discount Schemes
discounts = [Discount(type="percentage", value= 20.0,product_id="shirt-001"),
            Discount(type="fixed_amount", value= 10.0,product_id="hat-002"),
            Discount(type="buy_x_get_y", x = 4,y=1)]
# Create Request to calculate discount with specific Items and discount schemes
Request = PriceRequest(items=items,discounts = discounts)

# TestCase 
#  shirt-001 : 51.98 >41.584 > 41.59
#  hat-002 : 15.50 >5.50 > 5.5
#  shoes-003 : 79.99 > 79.99
#  Initial Subtotal = 51.98 + 15.50 + 79.99 = 147.47
# TOTAL > 127.074

class unitTest_pricecalculator(unittest.TestCase):
    def test_pricecalculator(self):
        expected_price = 127.074
        self.assertEqual(calculate_price(Request)["final_price"],expected_price)


# @app.post("/price")
# def calculate_price(req: PriceRequest):
#     # Calculate subtotal
#     subtotal = sum(item.qty * item.unit_price for item in req.items)
#     print('Initial Subtotal= ' + str(subtotal))
#     discount_total = 0
#     applied = []

#     # Apply discounts
#     for d in req.discounts:
#         if d.type == "percentage":
#             discount_total += subtotal * (d.value / 100)
#             print('PercentageDiscount: ' + str(discount_total))
#             applied.append("percentage")

#         elif d.type == "fixed_amount":
#             discount_total += d.value
#             print('Fixed: ' + str(discount_total))
#             applied.append("fixed_amount")

#         elif d.type == "buy_x_get_y":
#             for item in req.items:
#                 if item.product_id == d.product_id:
#                     free_units = floor(item.qty / (d.x + d.y)) * d.y
#                     discount_total += free_units * item.unit_price
#                     applied.append("buy_x_get_y")

#     final_price = subtotal - discount_total
#     if final_price < 0:
#         final_price = 0
#     print(round(final_price, 2))
#     print(applied)
#     return {
#         "subtotal": round(subtotal, 2),
#         "discount_total": round(discount_total, 2),
#         "final_price": round(final_price, 2),
#         "applied_discounts": applied,
#     }




    
    

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

if __name__ == '__main__':
    unittest.main(exit=False)