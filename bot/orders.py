from typing import Optional

from .client import BinanceClient
from .validators import validate_order
from .logging_config import setup_logging

logger = setup_logging()


def place_order(client: BinanceClient, symbol: str, side: str, order_type: str,
                quantity: float, price: Optional[float] = None) -> dict:
    validate_order(symbol, side, order_type, quantity, price)

    logger.info(
        "Placing %s %s order | symbol=%s qty=%s price=%s",
        side.upper(), order_type.upper(), symbol.upper(), quantity, price
    )

    response = client.place_order(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
        stop_price=price,
    )

    logger.info(
        "Order placed | orderId=%s status=%s executedQty=%s avgPrice=%s",
        response.get("orderId"),
        response.get("status"),
        response.get("executedQty"),
        response.get("avgPrice"),
    )
    return response
