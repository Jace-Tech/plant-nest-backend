from functools import wraps
from .helpers import response

class CustomRequestError(Exception):
    """
    Request error class
    """
    def __init__(self, message, code = 400):
        super().__init__(message)
        self.message = message
        self.code = code

class CustomError(Exception):
    """
    Request error class
    """
    def __init__(self, message, category= "error"):
        super().__init__(message)
        self.message = message
        self.category = category


def catch_exception(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)

        except CustomRequestError as e:
            return response(e.message, None, False), e.code

        except Exception as e:
            return response(str(e), None, False), 500
    return wrapper