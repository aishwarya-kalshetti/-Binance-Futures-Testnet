from .validators import (
    validate_symbol, 
    validate_side, 
    validate_order_type, 
    validate_quantity, 
    validate_price
)
from .client import BinanceTestnetClient
from .exceptions import OrderExecutionError
from .utils import format_order_response
from .logging_config import logger

def place_order(
    symbol: str,
    side: str, 
    order_type: str, 
    quantity: float, 
    price: float = None, 
    stopPrice: float = None
) -> dict:
    """
    Main business logic layer for preparing constraints, enforcing validation,
    and delegating the order execution to the client.
    """
    # 1. Validation
    logger.info(f"Validating inputs for: {side} {quantity} {symbol} @ {order_type} (Price={price})")
    try:
        sym = validate_symbol(symbol)
        sd = validate_side(side)
        oty = validate_order_type(order_type)
        qty = validate_quantity(quantity)
        prc = validate_price(oty, price)

        # 2. Build Order Kwargs
        order_args = {
            "symbol": sym,
            "side": sd,
            "type": oty,
            "quantity": qty
        }

        # Handle specific order type requirements
        if oty == "LIMIT":
            order_args["price"] = prc
            order_args["timeInForce"] = "GTC" # Required for limits

        if oty in ["STOP", "STOP_MARKET"]:
            if not stopPrice:
                raise ValueError("stopPrice is required for STOP or STOP_MARKET orders")
            order_args["stopPrice"] = stopPrice
            if oty == "STOP":
                order_args["price"] = prc

        logger.info(f"Validation successful. Kwargs built: {order_args}")

        # 3. Execution using our Client Wrapper
        client = BinanceTestnetClient()
        
        # Optional: ping to verify connection before placing real order
        client.ping_futures()
        
        # Place the order
        raw_response = client.place_futures_order(**order_args)
        
        # 4. Success handling
        formatted_response = format_order_response(raw_response)
        return formatted_response
        
    except Exception as e:
        logger.error(f"Order placement lifecycle failed: {str(e)}")
        raise OrderExecutionError(str(e))
