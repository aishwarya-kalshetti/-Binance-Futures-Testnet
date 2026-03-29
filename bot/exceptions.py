class TradingBotException(Exception):
    """Base exception for the Trading Bot."""
    pass

class ConfigurationError(TradingBotException):
    """Raised when there is a missing or invalid configuration (e.g., missing API keys)."""
    pass

class APIConnectionError(TradingBotException):
    """Raised when the bot fails to connect or communicate with the Binance API."""
    pass

class ValidationError(TradingBotException):
    """Raised when user input fails validation constraints."""
    pass

class OrderExecutionError(TradingBotException):
    """Raised when the order placement fails."""
    pass
