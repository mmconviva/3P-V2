from dataclasses import dataclass
from typing import Dict, List, Any


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
    pass


def parse_operation(op: str) -> List[str]:
    """
    Parse an operation string into tokens.
    Example:
        "add shirt"      -> ["add", "shirt"]
        "restock hat 3"  -> ["restock", "hat", "3"]
        "discount 10"    -> ["discount", "10"]
    """
    # TODO: Implement this
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

    cart: Dict[str, int] = {}
    discount_multiplier: float = 1.0

    for raw_op in operations:
        tokens = parse_operation(raw_op)
        if not tokens:
            continue

        action = tokens[0]

        if action == "add":
            # TODO: handle "add <product_id>"
            # 1. Check product exists
            # 2. Check inventory > 0
            # 3. Update cart and inventory
            pass

        elif action == "remove":
            # TODO: handle "remove <product_id>"
            # 1. Check item in cart and qty > 0
            # 2. Update cart and inventory
            pass

        elif action == "discount":
            # TODO: handle "discount <percentage>"
            # 1. Parse percentage
            # 2. Update discount_multiplier *= (1 - percentage/100)
            pass

        elif action == "restock":
            # TODO: handle "restock <product_id> <amount>"
            # 1. Parse amount
            # 2. Increase product inventory
            pass

        else:
            # Optional: ignore or raise exception
            # raise ValueError(f"Unknown operation: {raw_op}")
            pass

    # After processing all operations, compute final total
    total_before_discount = compute_cart_total(cart, product_map)
    total_after_discount = round(total_before_discount * discount_multiplier, 2)

    inventory_snapshot = {pid: p.inventory for pid, p in product_map.items()}

    return {
        "cart": cart,
        "inventory": inventory_snapshot,
        "total": total_after_discount,
    }


def compute_cart_total(cart: Dict[str, int], product_map: Dict[str, Product]) -> float:
    """
    Compute the total price of items in the cart before discounts.
    """
    # TODO: Implement this
    # Hint: sum over (quantity * product.price)
    pass


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
    result = process_operations(product_map, operations)
    print(result)
