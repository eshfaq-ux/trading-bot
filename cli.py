#!/usr/bin/env python3
"""CLI entry point for the Binance Futures Testnet trading bot."""

import argparse
import json
import os
import sys

from bot.client import BinanceClient
from bot.orders import place_order
from bot.logging_config import setup_logging

logger = setup_logging()


def print_order_summary(symbol, side, order_type, quantity, price):
    print("\n── Order Request ──────────────────────────")
    print(f"  Symbol     : {symbol.upper()}")
    print(f"  Side       : {side.upper()}")
    print(f"  Type       : {order_type.upper()}")
    print(f"  Quantity   : {quantity}")
    if price is not None:
        print(f"  Price      : {price}")
    print("───────────────────────────────────────────\n")


def print_order_response(resp: dict):
    print("── Order Response ─────────────────────────")
    print(f"  Order ID   : {resp.get('orderId')}")
    print(f"  Status     : {resp.get('status', 'ACCEPTED')}")
    print(f"  Executed   : {resp.get('executedQty', '0')}")
    avg = resp.get('avgPrice')
    if avg and float(avg) > 0:
        print(f"  Avg Price  : {avg}")
    print("───────────────────────────────────────────\n")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="trading_bot",
        description="Place orders on Binance Futures Testnet (USDT-M)",
    )
    p.add_argument("--symbol",     required=True,  help="Trading pair, e.g. BTCUSDT")
    p.add_argument("--side",       required=True,  choices=["BUY", "SELL"], type=str.upper)
    p.add_argument("--type",       required=True,  dest="order_type",
                   choices=["MARKET", "LIMIT", "STOP_LOSS_LIMIT"], type=str.upper)
    p.add_argument("--quantity",   required=True,  type=float)
    p.add_argument("--price",      required=False, type=float, default=None,
                   help="Required for LIMIT and STOP_MARKET orders")
    p.add_argument("--api-key",    default=os.getenv("BINANCE_API_KEY"),    help="API key (or set BINANCE_API_KEY)")
    p.add_argument("--api-secret", default=os.getenv("BINANCE_API_SECRET"), help="API secret (or set BINANCE_API_SECRET)")
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.api_key or not args.api_secret:
        parser.error("API key and secret are required. Use --api-key/--api-secret or set BINANCE_API_KEY/BINANCE_API_SECRET env vars.")

    print_order_summary(args.symbol, args.side, args.order_type, args.quantity, args.price)

    try:
        client = BinanceClient(args.api_key, args.api_secret)
        resp = place_order(client, args.symbol, args.side, args.order_type, args.quantity, args.price)
        print_order_response(resp)
        print("✅  Order placed successfully.")
    except ValueError as e:
        logger.error("Validation error: %s", e)
        print(f"❌  Validation error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logger.error("Failed to place order: %s", e)
        print(f"❌  Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
