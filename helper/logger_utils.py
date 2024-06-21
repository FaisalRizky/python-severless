import logging
import os

def setup_logger(filename):
    # Ensure the log directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    logging.basicConfig(
        filename=filename,  # Use the provided filename for the log file
        level=logging.DEBUG,  # Log level
        format='%(asctime)s %(levelname)s %(message)s',  # Log message format
        datefmt='%Y-%m-%d %H:%M:%S'  # Date format
    )
    logger = logging.getLogger()
    return logger
