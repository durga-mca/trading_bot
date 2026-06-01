import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from bot.logging_config import get_logger

logger = get_logger(__name__)

BASE_URL = "https://testnet.binancefuture.com"


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str, paper_trading: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.paper_trading = paper_trading
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key
        })

    def _sign(self, params: dict) -> str:
        query_string = urlencode(params)
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def get_latest_price(self, symbol: str) -> float:
        try:
            url = "https://fapi.binance.com/fapi/v1/ticker/price"
            response = requests.get(url, params={"symbol": symbol}, timeout=10)
            data = response.json()
            return float(data["price"])
        except Exception:
            return 50000.0

    def place_order(self, symbol: str, side: str, order_type: str,
                    quantity: float, price: float = None) -> dict:
        if self.paper_trading:
            return self._paper_order(symbol, side, order_type, quantity, price)
        return self._real_order(symbol, side, order_type, quantity, price)

    def _paper_order(self, symbol: str, side: str, order_type: str,
                     quantity: float, price: float = None) -> dict:
        import random
        market_price = self.get_latest_price(symbol)
        order_id = random.randint(100000000, 999999999)
        exec_price = price if (order_type == "LIMIT" and price) else market_price

        result = {
            "orderId": order_id,
            "symbol": symbol.upper(),
            "status": "FILLED" if order_type == "MARKET" else "NEW",
            "side": side.upper(),
            "type": order_type.upper(),
            "origQty": str(quantity),
            "executedQty": str(quantity) if order_type == "MARKET" else "0",
            "avgPrice": str(round(exec_price, 2)),
            "price": str(price) if price else "0",
            "timeInForce": "GTC" if order_type == "LIMIT" else "GTE_GTC",
            "paper_trading": True
        }
        logger.info("PAPER ORDER placed: %s", result)
        return result

    def _real_order(self, symbol: str, side: str, order_type: str,
                    quantity: float, price: float = None) -> dict:
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
            "timestamp": int(time.time() * 1000),
            "recvWindow": 5000
        }
        if order_type.upper() == "LIMIT" and price:
            params["price"] = price
            params["timeInForce"] = "GTC"

        params["signature"] = self._sign(params)
        url = BASE_URL + "/fapi/v1/order"
        logger.info("POST %s | params: %s", url,
                    {k: v for k, v in params.items() if k != "signature"})
        try:
            response = self.session.post(url, params=params, timeout=10)
            data = response.json()
            if "code" in data and data["code"] != 200:
                logger.error("API error: %s", data)
                raise BinanceAPIError(data.get("msg", "Unknown error"), data.get("code", -1))
            logger.info("Response: %s", data)
            return data
        except requests.exceptions.ConnectionError as e:
            logger.error("Network failure: %s", e)
            raise NetworkError(f"Could not reach Binance Testnet: {e}") from e
        except requests.exceptions.Timeout as e:
            logger.error("Request timed out: %s", e)
            raise NetworkError("Request timed out.") from e


class BinanceAPIError(Exception):
    def __init__(self, message: str, code: int = -1):
        super().__init__(message)
        self.code = code


class NetworkError(Exception):
    pass