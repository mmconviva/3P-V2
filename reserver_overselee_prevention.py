from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
from threading import Lock

app = FastAPI()

inventory = {
    "shirt-001": 15,
    "hat-002": 40,
}

reservations = {}

inventory_lock = Lock()

class ReserveRequest(BaseModel):
    product_id: str
    qty: int

class ReleaseRequest(BaseModel):
    reservation_id: str


@app.post("/reserve")
def reserve_item(req: ReserveRequest):
    product = req.product_id
    qty = req.qty

    # concurrency protection
    with inventory_lock:
        available = inventory.get(product, 0)

        if available >= qty:
            inventory[product] = available - qty
            r_id = f"res_{uuid4().hex}"
            reservations[r_id] = {
                "product_id": product,
                "qty": qty
            }
            return {
                "reservation_id": r_id,
                "status": "reserved",
                "remaining_stock": inventory[product]
            }
        
        return {
            "status": "unavailable",
            "requested": qty,
            "available": available
        }


@app.post("/release")
def release_item(req: ReleaseRequest):
    r_id = req.reservation_id
    data = reservations.get(r_id)

    if not data:
        return { "status": "not_found" }

    product = data["product_id"]
    qty = data["qty"]

    # concurrency protection
    with inventory_lock:
        inventory[product] += qty

    del reservations[r_id]

    return {
        "status": "released",
        "product_id": product,
        "restored_qty": qty,
        "remaining_stock": inventory[product]
    }
