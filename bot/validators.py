from bot.logging_config import get_logger

logger = get_logger(__name__)

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


class ValidationError(Exception):
    pass


def validate_order_params(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    errors = []

    if not symbol or not symbol.isalpha():
        errors.append(f"Invalid symbol '{symbol}'. Use format like BTCUSDT.")

    if side.upper() not in VALID_SIDES:
        errors.append(f"Invalid side '{side}'. Must be one of: {', '.join(VALID_SIDES)}.")

    if order_type.upper() not in VALID_ORDER_TYPES:
        errors.append(f"Invalid order type '{order_type}'. Must be one of: {', '.join(VALID_ORDER_TYPES)}.")

    if quantity is None:
        errors.append("Quantity is required.")
    elif quantity <= 0:
        errors.append(f"Quantity must be positive (got {quantity}).")

    if order_type.upper() == "LIMIT":
        if price is None:
            errors.append("Price is required for LIMIT orders.")
        elif price <= 0:
            errors.append(f"Price must be positive (got {price}).")

    if order_type.upper() == "STOP_MARKET":
        if price is None:
            errors.append("Stop price is required for STOP_MARKET orders.")
        elif price <= 0:
            errors.append(f"Stop price must be positive (got {price}).")

    if errors:
        for e in errors:
            logger.warning("Validation error: %s", e)
        raise ValidationError("\n".join(errors))

    logger.info(
        "Validation passed — symbol=%s side=%s type=%s qty=%s price=%s",
        symbol.upper(), side.upper(), order_type.upper(), quantity, price
    )