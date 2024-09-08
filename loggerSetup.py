import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')
    
    handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Ensure the logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Setup loggers
db_logger = setup_logger('db_logger', 'logs/database.log')
user_logger = setup_logger('user_logger', 'logs/user.log')
