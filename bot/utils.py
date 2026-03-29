def format_order_response(response: dict) -> dict:
    """
    Format the raw binance response dict into a cleaner structure 
    containing only necessary summary detail.
    """
    return {
        "orderId": response.get("orderId"),
        "status": response.get("status"),
        "executedQty": response.get("executedQty", "0"),
        "avgPrice": response.get("avgPrice", "0"),
        "clientOrderId": response.get("clientOrderId")
    }
