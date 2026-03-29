from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
import time
from .config import Config
from .exceptions import APIConnectionError
from .logging_config import logger

class BinanceTestnetClient:
    """Wrapper around python-binance client tailored for Futures Testnet."""
    
    def __init__(self):
        Config.validate()
        try:
            self.client = Client(
                api_key=Config.API_KEY,
                api_secret=Config.API_SECRET,
                testnet=True # Directs requests to the testnet endpoints
            )
            
            # Synchronize time offset to prevent "Timestamp ahead" errors
            try:
                server_time = self.client.futures_time()['serverTime']
                local_time = int(time.time() * 1000)
                self.client.timestamp_offset = server_time - local_time
                logger.info(f"Time offset synced: {self.client.timestamp_offset}ms to prevent API rejections.")
            except Exception as e:
                logger.warning(f"Failed to sync time offset: {e}")
                
            logger.info("Initialized python-binance Testnet Client.")
        except Exception as e:
            logger.error(f"Initialization error: {str(e)}")
            raise APIConnectionError(f"Failed to initialize Binance Client: {str(e)}")
            
    def ping_futures(self):
        """Pings the futures API to ensure connectivity."""
        try:
            self.client.futures_ping()
            logger.info("Successfully pinged Binance Futures Testnet API.")
            return True
        except BinanceAPIException as e:
            logger.error(f"Binance API Ping failed: {e.message}")
            raise APIConnectionError(f"Binance API Error: {e.message}")
        except Exception as e:
            logger.error(f"Ping failed: {e}")
            raise APIConnectionError(f"Failed to connect to Futures API: {str(e)}")

    def place_futures_order(self, **kwargs):
        """Wrapper for futures_create_order to capture and log API interactions."""
        try:
            logger.info(f"Sending order request payload: {kwargs}")
            response = self.client.futures_create_order(**kwargs)
            logger.info(f"Order successful! Response: {response}")
            return response
        except BinanceAPIException as e:
            logger.error(f"Binance API Exception [{e.status_code}]: {e.message}")
            raise APIConnectionError(f"Binance API Error: {e.message}")
        except BinanceRequestException as e:
            logger.error(f"Binance Request Exception: {e.message}")
            raise APIConnectionError(f"Binance Request Error: {e.message}")
        except Exception as e:
            logger.error(f"Unexpected error when placing order: {str(e)}")
            raise APIConnectionError(f"Unexpected Error: {str(e)}")
