import hashlib
import hmac
import time
from urllib.parse import urlencode
from typing import Optional

import requests

from .logging_config import setup_logging

BASE_URL = "https://testnet.binance.vision"
logger = setup_logging()


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": api_key})

    def _sign(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000)
        query = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode(), query.encode(), hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def _request(self, method: str, path: str, params: dict) -> dict:
        url = BASE_URL + path
        signed = self._sign(params)
        logger.debug("REQUEST %s %s params=%s", method, url, {k: v for k, v in signed.items() if k != "signature"})
        try:
            if method == "GET":
                resp = self.session.request(method, url, params=signed)
            else:
                query_str = urlencode(signed)
                resp = self.session.request(method, url, data=query_str,
                    headers={"Content-Type": "application/x-www-form-urlencoded"})
            data = resp.json()
            logger.debug("RESPONSE status=%s body=%s", resp.status_code, data)
            resp.raise_for_status()
            return data
        except requests.exceptions.HTTPError as e:
            logger.error("HTTP error: %s — %s", e, resp.text)
            raise
        except requests.exceptions.RequestException as e:
            logger.error("Network error: %s", e)
            raise

    def get_account(self) -> dict:
        return self._request("GET", "/api/v3/account", {})

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float,
                    price: Optional[float] = None, stop_price: Optional[float] = None) -> dict:
        def fmt(v): return f"{v:.8f}".rstrip('0').rstrip('.')
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": fmt(quantity),
        }
        if order_type.upper() == "LIMIT":
            params["price"] = fmt(price)
            params["timeInForce"] = "GTC"
        if order_type.upper() == "STOP_LOSS_LIMIT":
            params["stopPrice"] = fmt(price)
            params["price"] = fmt(price)
            params["timeInForce"] = "GTC"
        return self._request("POST", "/api/v3/order", params)
