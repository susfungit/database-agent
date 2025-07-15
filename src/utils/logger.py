import logging
import os
from typing import Dict, Any

def setup_logger(name: str, config: Dict[str, Any] = None) -> logging.Logger:
    """Setup logger with configuration."""
    logger = logging.getLogger(name)
    
    if config is None:
        config = {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": "logs/database_agent.log"
        }
    
    # Set log level
    logger.setLevel(getattr(logging, config.get("level", "INFO").upper()))
    
    # Create formatter
    formatter = logging.Formatter(config.get("format"))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    log_file = config.get("file", "logs/database_agent.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger 