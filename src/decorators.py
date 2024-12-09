from src.logger_setup import standard_logger_set_up

def try_function(func_to_try):
    def inner():    
        try:
            return func_to_try()
        except Exception as exception:
            logger = standard_logger_set_up("Error handler")
            logger.exception(exception)
            raise exception
    
    return inner