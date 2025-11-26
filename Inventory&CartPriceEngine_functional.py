from ast import Continue
from dataclasses import dataclass
from typing import Dict, List, Any
import numpy as np
import unittest

# products = [
#         {"id": "shirt", "price": 20, "inventory": 5},
#         {"id": "hat", "price": 10, "inventory": 2},
#         {"id": "bag", "price": 50, "inventory": 1},
#     ]

#     operations = [
#         "add shirt",
#         "add shirt",
#         "add hat",
#         "add bag",
#         "remove shirt",
#         "discount 10",
#         "add shirt",
#         "discount 20",
#         "restock hat 3",
#         "add hat",
#     ]
class unit_test_price_engine(unittest.TestCase):
    def test_price_engine(self):
        expected_total = 79.2  #(2*20 + 2*10 + 1*50)*0.9*0.8 = 
        actual_total = result['total']
        self.assertEqual(expected_total,actual_total)


@dataclass
class Product:
    id: str
    price: float
    inventory: int


def build_product_map(products: List[Dict[str, Any]]) -> Dict[str, Product]:
    """
    Convert raw product dictionaries into a map of product_id -> Product.
    """
    # TODO: Implement this
    # Hint: loop through products, create Product objects, store by id
    #  products = [
    #     {"id": "shirt", "price": 20, "inventory": 5},
    #     {"id": "hat", "price": 10, "inventory": 2},
    #     {"id": "bag", "price": 50, "inventory": 1},
    # ]

    # product map is a mapped object, which has product_id as key  and the product dictionnary as value
    product_map = {} # define dictionary
    for p in products:
        product = Product(id=p["id"], price=p["price"], inventory=p["inventory"])
        product_map[product.id] = product

    # pass
    return product_map

def parse_operation(op: str) -> List[str]:
    """
    Parse an operation string into tokens.
    Example:
        "add shirt"      -> ["add", "shirt"]
        "restock hat 3"  -> ["restock", "hat", "3"]
        "discount 10"    -> ["discount", "10"]
    """
    # TODO: Implement this
    # op.split()
    # print(result)

    # takes each element from the Operations and splits them so actual operation, product, quantity etc is seperarted 
    # result is retruned to the calling function, in this case process_operations()
    return op.split()


def process_operations(
    product_map: Dict[str, Product],
    operations: List[str]
) -> Dict[str, Any]:
    """
    Process all operations and return final state.

    Returns a dict of the form:
    {
        "cart": {"shirt": 2, "hat": 2, ...},
        "inventory": {"shirt": 3, "hat": 3, ...},
        "total": 83.52
    }
    """
    # State you probably want to track:
    # - cart: product_id -> quantity
    # - discounts: cumulative multiplier (start at 1.0)
    # - product_map: already holds inventory and price

    # goal is to create the cart with product_ids, corresponding quantity, inbventory status and total amount after dsicount etc

    cart: Dict[str, int] = {}
    discount_multiplier: float = 1.0
    
    cartops = {}
    for raw_op in operations:
        tokens = parse_operation(raw_op)
        if not tokens:
            continue
        action = tokens[0]
        print(action)   
        
        if action == "add":
            print('Adding')
            # TODO: handle "add <product_id>"
            # 1. Check product exists
            # 2. Check inventory > 0
            # 3. Update cart and inventory

            # product = Product(id=p["id"], price=p["price"], inventory=p["inventory"])
            # product_map[product.id] = product 
            #  "cart": {"shirt": 2, "hat": 2, ...},
            # "inventory": {"shirt": 3, "hat": 3, ...},
            # "total": 83.52
            # "add shirt"      -> ["add", "shirt"]
            # "restock hat 3"  -> ["restock", "hat", "3"]
            # "discount 10"    -> ["discount", "10"]

            product_id = tokens[1]
            print(product_id)
            if len(tokens) < 2:
                continue
            if product_map[product_id].inventory > 0 :
                
                product_map[product_id].inventory -= 1
                cart[product_id] = cart.get(product_id,0) +1 
                
                # cartops['ops'] = action

            

        elif action == "remove":
            print('Removing')
            # TODO: handle "remove <product_id>"
            # 1. Check item in cart and qty > 0
            # 2. Update cart and inventory
            product_id = tokens[1]
            if len(tokens) < 2:
                continue
            product_map[product_id].inventory += 1
            cart[product_id] = cart.get(product_id) - 1
                


        elif action == "discount":
            
            if len(tokens) < 2:
                continue
            discount_multiplier *= (1 - int(tokens[1])/100)
            # TODO: handle "discount <percentage>"
            # 1. Parse percentage
            # 2. Update discount_multiplier *= (1 - percentage/100)
            

        elif action == "restock":
            print('Restocking')
            product_id = tokens[1]
            if len(tokens) < 3:
                Continue
            product_map[product_id].inventory += int(tokens[2])    
            # TODO: handle "restock <product_id> <amount>"
            # 1. Parse amount
            # 2. Increase product inventory
            

        else:
            # Optional: ignore or raise exception
            # raise ValueError(f"Unknown operation: {raw_op}")
            pass
    
    # After processing all operations, compute final total
    total_before_discount = compute_cart_total(cart, product_map)
    total_after_discount = round(total_before_discount * discount_multiplier, 2)

    inventory_snapshot = {pid: p.inventory for pid, p in product_map.items()}

    compute_cart_total(cart, product_map)
    return {
        "cart": cart,
        "inventory": inventory_snapshot,
        "total": total_after_discount,
        "cartops": cartops
    }


def compute_cart_total(cart: Dict[str, int], product_map: Dict[str, Product]) -> float:
    """
    Compute the total price of items in the cart before discounts.
    """
    print(cart)
    print(product_map)
    total = 0 
    for prodid,qty in  cart.items():
       total += qty * product_map[prodid].price   
    return total     
    
    # TODO: Implement this
    # Hint: sum over (quantity * product.price)
    
    


if __name__ == "__main__":
    # Example usage / test harness

    products = [
        {"id": "shirt", "price": 20, "inventory": 5},
        {"id": "hat", "price": 10, "inventory": 2},
        {"id": "bag", "price": 50, "inventory": 1},
    ]

    operations = [
        "add shirt",
        "add shirt",
        "add hat",
        "add bag",
        "remove shirt",
        "discount 10",
        "add shirt",
        "discount 20",
        "restock hat 3",
        "add hat",
    ]
    
    product_map = build_product_map(products)

    # compute_cart_total()

    # print(product_map)
    result = process_operations(product_map, operations)

    print(result)
    
    unittest.main(exit= False)


    
    # X = build_product_map(products)
    # print(X)
    # print(parse_operation(operations))  

