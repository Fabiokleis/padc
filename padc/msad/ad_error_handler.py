from typing import Any
import logging

from ..client.error_handler import LdapErrorResult
from ..logger import logger


def match_level(message: Any, level: int = 10) -> None:
    """Match level of loggin and send message!"""
    match level:
        case 10:
            logger.debug(message)
        case 20:
            logger.info(message)
        case 30:
            logger.warning(message)
        case 40:
            logger.error(message)
        case 50:
            logger.critical(message)
        case _:
            logger.debug(f"counld not match any level for this message: {message}")

class ADSuccessResult:
    """Active Directory Success Result."""

    def __init__(self, payload: Any):
        self.payload = payload

    def unwrap(self, level: int = logging.INFO) -> Any:
        """Get payload, send log maintaing the flexibility to change the loggin level of success."""
        if isinstance(self.payload, str):
            match_level(self.payload, level)
        return self.payload

class ADErrorResult(Exception):
    """Active Directory Error Result."""
    
    def __init__(self, message, fn: str):
        self.message = f'{fn}: {message}'

    def unwrap(self, level: int = logging.ERROR) -> str:
        """Get message, send log maintaing the flexibility to change the loggin level of the exception."""
        match_level(self.message, level)
        return self.message
   
# ref: https://stackoverflow.com/questions/11420464/catch-exceptions-inside-a-class
def catch_exception(f):
    """Function decorator exception handler."""
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (LdapErrorResult, AssertionError) as e:
            return ADErrorResult(e, f.__name__)
    return func
