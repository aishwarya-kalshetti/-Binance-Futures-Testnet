import logging
import os
from pathlib import Path

def setup_logger():
    """Sets up and returns a configured logger logging to file."""
    # Ensure logs directory exists at the project root
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger("TradingBot")
    
    # Avoid adding handlers multiple times in interactive environments
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.INFO)
    
    # Formatter: timestamp | level | module | message
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(module)-10s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # File Handler
    file_handler = logging.FileHandler(log_dir / "trading_bot.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# Expose a global logger instance
logger = setup_logger()
