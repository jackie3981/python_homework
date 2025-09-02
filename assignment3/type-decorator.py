# Task 2

def type_converter(type_of_output):
    def decorator(func):
        def wrapper(*args, **kwargs):
            x = func(*args, **kwargs)
            return type_of_output(x)
        return wrapper
    return decorator

# Returns an int, converted into a str
@type_converter(str)
def return_int():
    return 5

# Returns a str, converted into an int (will fail)
@type_converter(int)
def return_string():
    return "not a number"

if __name__ == "__main__":
    y = return_int()
    print(type(y).__name__)

    try:
        y = return_string()
        print("shouldn't get here!")
    except ValueError:
        print("can't convert that string to an integer!")
