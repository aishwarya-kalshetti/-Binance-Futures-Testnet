from .exceptions import ValidationError

def validate_symbol(symbol: str) -> str:
    """Validate trading symbol format."""
    symbol = symbol.upper().strip()
    if not symbol:
        raise ValidationError("Symbol cannot be empty.")
    # In Futures, contracts usually end with USDT or USD. 
    # Just a basic validation for this bot to avoid obvious errors.
    return symbol

def validate_side(side: str) -> str:
    """Validate order side (BUY or SELL)."""
    side = side.upper().strip()
    if side not in ["BUY", "SELL"]:
        raise ValidationError(f"Invalid side '{side}'. Must be 'BUY' or 'SELL'.")
    return side

def validate_order_type(order_type: str) -> str:
    """Validate order type. Supports MARKET and LIMIT, expanding to STOP for advanced orders."""
    order_type = order_type.upper().strip()
    if order_type not in ["MARKET", "LIMIT", "STOP", "STOP_MARKET"]:
        raise ValidationError(f"Invalid order type '{order_type}'. Supported: 'MARKET', 'LIMIT', 'STOP'.")
    return order_type

def validate_quantity(quantity: float) -> float:
    """Validate that quantity is strictly positive."""
    if quantity <= 0:
        raise ValidationError(f"Quantity must be greater than 0. Got: {quantity}")
    return quantity

def validate_price(order_type: str, price: float = None) -> float:
    """Validate that price is provided correctly for LIMIT orders."""
    if order_type == "LIMIT":
        if price is None or price <= 0:
            raise ValidationError("Price is required and must be greater than 0 for LIMIT orders.")
    return price
