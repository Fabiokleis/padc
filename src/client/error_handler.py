import sys,ldap
from typing import Any, NoReturn


class LdapSuccessResult:
    """ Ldap Success Result """

    def __init__(self, payload: Any):
        self.payload = payload

    def unwrap(self) -> Any:
        return self.payload

class LdapErrorResult(Exception):
    """ Ldap Error Result """
    
    def __init__(self, message):
        self.message = message

    def unwrap(self) -> NoReturn:
        raise self


# ref: https://stackoverflow.com/questions/11420464/catch-exceptions-inside-a-class
def catch_exception(f):
    """ function decorator exception handler """
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ldap.LDAPError as e:
            if args[0].debug:
                raise e
            
            return LdapErrorResult(e)
    return func

