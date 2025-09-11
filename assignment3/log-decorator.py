# Task 1
import logging
from functools import wraps

# Logger setup
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

# Decorator
def logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        result = func(*args, **kwargs)

        pos_args = list(args) if args else "none"
        kw_args = dict(kwargs) if kwargs else "none"

        # Write on log's file
        logger.log(
            logging.INFO,
            f"function: {func.__name__} "
            f"positional parameters: {pos_args} "
            f"keyword parameters: {kw_args} "
            f"return: {result}"
        )

        return result
    return wrapper

# Function 1: no parameters, no return
@logger_decorator
def say_hello():
    print("Hello, World!")

# Function 2: just *args
@logger_decorator
def return_true(*args):
    return True

# Function 3: just **kwargs
@logger_decorator
def return_decorator(**kwargs):
    return logger_decorator

if __name__ == "__main__":
    say_hello()
    return_true(1, 2, 3)
    return_decorator(debug=True, verbose=False)
