import logging
import os
import sys

def exception_hook(exc_type, exc_value, exc_traceback):
   logging.error(
       "Uncaught exception",
       exc_info=(exc_type, exc_value, exc_traceback)
   )
   sys.exit()

def get_logger (
    logger_name: str,
    log_level: str = "INFO",
):     
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    # sys.excepthook = exception_hook
    
    return logger

def assign_filehandler_to_logger (
    logger: logging.Logger,
    file_location: tuple = ('result', 'actions.log')
):       
    file_handler = logging.FileHandler(
        os.path.join(
            *file_location
        )
    )
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return file_handler