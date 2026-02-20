import logging
import os
from datetime import datetime

def setup_logger(name=__name__, log_level=logging.INFO):
    """
    Sets up a logger with the specified name and level.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(log_level)
        
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # File Handler
        log_file = f'logs/app_{datetime.now().strftime("%Y-%m-%d")}.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger
