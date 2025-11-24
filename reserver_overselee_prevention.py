from itertools import product
import json
from time import sleep
import unittest
from fastapi import FastAPI
from httpx import Response
from pydantic import BaseModel
from uuid import uuid4
from threading import Lock

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, thread

from fastapi.testclient import TestClient

# If inventory is enough → reserve and decrement available stock.
# If inventory is NOT enough → return "status": "unavailable".
# 2. Releases inventory> If checkout fails or expires:
# Basic in-memory persistence >No DB is required — just use Python dictionaries or similar.
# Handle concurrency >Two reservations at same time must not cause overselling.
# You may use:locks,atomic operations,transactions (if in a real DB, but here we simulate)




app = FastAPI()

class Unit_Test_Reservation(unittest.TestCase):
    def setUp(self):
        """Reset inventory before each test"""
        global inventory, reservations
        inventory.clear()
        inventory.update({
            "shirt-001": 15,
            "hat-002": 40,
        })
        reservations.clear()
        self.client = TestClient(app)
    
    def test_reserveSuccess(self):
        response = self.client.post("/reserve",json={"product_id": "shirt-001",
            "qty": 5
        })
        
        self.assertEqual(response.status_code, 200)
        print("Status Code= " + str(response.status_code))
        data =response.json()
        print('Status= ' + data["status"])
        print('Remaining Stock= ' + str(data["remaining_stock"]) )
        self.assertEqual(data["status"], "reserved")
        self.assertIn("reservation_id", data)
        self.assertEqual(data["remaining_stock"], 10)
        

    def test_reserveInsufficientStock(self):
        response = self.client.post("/reserve",json={"product_id": "shirt-001",
            "qty": 20
        })
        # self.assertEqual(response.status_code, 200)
        data =response.json()
        # print(data)
        print('Status= ' + data["status"])
        print('Restored Qty= ' + str(data["requested"]) )
        print('Available Stock= ' + str(data["available"]) )
        self.assertEqual(data["status"], "unavailable")
        self.assertEqual(data["requested"], 20) 
        self.assertEqual(data["available"], 15)




    def test_lock(self):
        global inventory
        inventory["shirt-001"] = 20
        print('current inventory = ' + str(inventory["shirt-001"]))
        # 20 reserver of 2 Qty
        # 10 should pass through 
        # Final quantity should be 0
        def make_reservaton():
            response = self.client.post("/reserve",json={"product_id": "shirt-001",
            "qty": 2
            }).json()

            return response
        
        threads = []
        results = []

        def worker():
            result = make_reservaton()
            results.append(result)

        for x in range(20):
            thread = threading.Thread(target= worker)
            threads.append(thread)
        
        for thread in threads:
            thread.start()
            time.sleep(0.01)

        for thread in threads:
            thread.join()

        successful = [r for r in results if r is not None and r.get("status") == "reserved"]
        total_reserved_qty = len(successful) * 2

        print(f"\n=== Thread Safety Test ===")
        print(f"Total requests: 20")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {20 - len(successful)}")
        print(f"Total quantity reserved: {total_reserved_qty}")
        print(f"Final inventory: {inventory['shirt-001']}")
        
        # Critical assertions
        self.assertLessEqual(total_reserved_qty, 20, 
                            "CRITICAL: Must not oversell!")
        self.assertEqual(inventory["shirt-001"], 20 - total_reserved_qty,
                        "Inventory should be correctly decremented")
        self.assertEqual(len(successful), 10,
                        "Exactly 10 reservations should succeed (10 * 2 = 20)")


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


if __name__ == '__main__':
    unittest.main()