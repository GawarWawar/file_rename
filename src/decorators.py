from src.set_up import get_config
from src.logger_setup import get_logger, assign_filehandler_to_logger

def try_function(func_to_try):
    def inner():    
        try:
            return func_to_try()
        except Exception as exception:
            logger = get_logger(
                "Error handler",
                # TODO: set up this as config variable
                log_level="INFO"
            )
            file_handler = assign_filehandler_to_logger(logger=logger)
            
            logger.exception(exception)
            logger.removeHandler(file_handler)
            raise exception
    
    return inner