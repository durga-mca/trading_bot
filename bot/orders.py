from bot.client import BinanceClient, BinanceAPIError, NetworkError
from bot.validators import validate_order_params, ValidationError
from bot.logging_config import get_logger

logger = get_logger(__name__)


def place_order(client: BinanceClient, symbol: str, side: str,
                order_type: str, quantity: float, price: float = None) -> dict:
    try:
        validate_order_params(symbol, side, order_type, quantity, price)
    except ValidationError as e:
        logger.error("Order blocked due to validation errors:\n%s", e)
        raise

    try:
        result = client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        logger.info("Order placed successfully: %s", result)
        return result
    except BinanceAPIError as e:
        logger.error("API error placing order (code %s): %s", e.code, e)
        raise
    except NetworkError as e:
        logger.error("Network error placing order: %s", e)
        raise