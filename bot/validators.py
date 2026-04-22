from typing import Optional

VALID_SYMBOLS = None  # lazy-loaded
VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_LOSS_LIMIT"}


def validate_order(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float]):
    if not symbol or not symbol.isalnum():
        raise ValueError(f"Invalid symbol: '{symbol}'")
    if side.upper() not in VALID_SIDES:
        raise ValueError(f"Side must be one of {VALID_SIDES}, got '{side}'")
    if order_type.upper() not in VALID_ORDER_TYPES:
        raise ValueError(f"Order type must be one of {VALID_ORDER_TYPES}, got '{order_type}'")
    if quantity <= 0:
        raise ValueError(f"Quantity must be positive, got {quantity}")
    if order_type.upper() == "LIMIT":
        if price is None or price <= 0:
            raise ValueError("Price is required and must be positive for LIMIT orders")
    if order_type.upper() == "STOP_LOSS_LIMIT":
        if price is None or price <= 0:
            raise ValueError("Price and stop price are required for STOP_LOSS_LIMIT orders")
