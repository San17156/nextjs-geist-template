"""
Logging utilities
"""

import logging
import os
from datetime import datetime

def setup_logger(name: str = 'smart-recruitment-system') -> logging.Logger:
    """Set up application logger"""
    
    # Create logs directory if it doesn't exist
    log_dir = 'src/data/logs'
    os.makedirs(log_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create file handler
    log_file = os.path.join(log_dir, f'smart-recruitment-{datetime.now().strftime("%Y-%m-%d")}.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Initialize logger
logger = setup_logger()
