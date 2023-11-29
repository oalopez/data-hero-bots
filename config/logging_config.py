# config/logging_config.py
import logging
from colorlog import ColoredFormatter

def setup_logging():
    # Create a root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Create a formatter that will color our log records
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s%(reset)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    
    # Create a console handler using the formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Remove existing handlers if any and add our custom handler
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    logger.addHandler(console_handler)

    # TODO: Add more handlers, such as a FileHandler to log to files
    # handler = logging.FileHandler('myapp.log')
    # handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    # logging.getLogger('').addHandler(handler)