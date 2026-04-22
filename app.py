import os
from flask import Flask, render_template, request

from bot.client import BinanceClient
from bot.orders import place_order as execute_order
from bot.logging_config import setup_logging

app = Flask(__name__)
logger = setup_logging()

API_KEY    = os.getenv("BINANCE_API_KEY", "")
API_SECRET = os.getenv("BINANCE_API_SECRET", "")
LOG_FILE   = "trading_bot.log"


def read_logs(n=40):
    try:
        with open(LOG_FILE) as f:
            return f.readlines()[-n:]
    except FileNotFoundError:
        return []


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html",
        response=None,
        logs=read_logs(),
        api_key=API_KEY,
        api_secret=API_SECRET,
        account_balance=None,
    )


@app.route("/place_order", methods=["POST"])
def place():
    f = request.form
    api_key    = f.get("api_key", "").strip()
    api_secret = f.get("api_secret", "").strip()
    symbol     = f.get("symbol", "").strip()
    side       = f.get("side", "").strip()
    order_type = f.get("order_type", "").strip()
    quantity   = f.get("quantity", "").strip()
    price      = f.get("price", "").strip() or None

    response = None
    try:
        qty = float(quantity)
        prc = float(price) if price else None
        client = BinanceClient(api_key, api_secret)
        response = execute_order(client, symbol, side, order_type, qty, prc)
    except Exception as e:
        response = {"error": str(e)}

    return render_template("index.html",
        response=response,
        logs=read_logs(),
        api_key=api_key,
        api_secret=api_secret,
        account_balance=None,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
