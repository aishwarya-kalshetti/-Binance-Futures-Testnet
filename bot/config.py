import os
from dotenv import load_dotenv
from .exceptions import ConfigurationError

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration holder for the Trading Bot."""
    API_KEY = os.getenv("BINANCE_API_KEY")
    API_SECRET = os.getenv("BINANCE_API_SECRET")
    BASE_URL = "https://testnet.binancefuture.com"
    
    @classmethod
    def validate(cls):
        """Validate that all required configurations are present."""
        if not cls.API_KEY or not cls.API_SECRET:
            raise ConfigurationError(
                "Missing BINANCE_API_KEY or BINANCE_API_SECRET in environment variables. "
                "Please ensure your .env file is configured correctly."
            )
