from typing import Any, NoReturn

from client.error_handler import LdapErrorResult

class ADSuccessResult:
    """Active Directory Success Result."""

    def __init__(self, payload: Any):
        self.payload = payload

    def unwrap(self) -> Any:
        return self.payload

class ADErrorResult(Exception):
    """Active Directory Error Result."""
    
    def __init__(self, message):
        self.message = message

    def unwrap(self) -> NoReturn:
        raise self


# ref: https://stackoverflow.com/questions/11420464/catch-exceptions-inside-a-class
def catch_exception(f):
    """Function decorator exception handler."""
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (LdapErrorResult, AssertionError) as e:
            return ADErrorResult(e)
    return func
