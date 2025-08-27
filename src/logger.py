"""
Logging utilities
File: src/logger.py
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

def get_logger(name="app"):
    """
    Create and configure logger with both file and console output
    
    Args:
        name (str): Logger name
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Get logger
    logger = logging.getLogger(name)
    
    # If logger already has handlers, return it (avoid duplicate handlers)
    if logger.handlers:
        return logger
    
    # Set log level
    logger.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler with rotation
    log_filename = f"logs/naukri_automation_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = RotatingFileHandler(
        log_filename,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger