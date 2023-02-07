import inspect
from client import Client

# ref: https://stackoverflow.com/questions/11420464/catch-exceptions-inside-a-class
def catch_exception(f):
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            raise e
    return func


class MsAD(Client):
    """ Active Directory client """

    @catch_exception
    def __init__(self, uri: str, bind_dn: str, auth_pass: str, debug=False) -> None:
        Client.__init__(self, uri, 0, debug)
        self.uri = uri
        self.auth_pass = auth_pass
        self.bind_dn = bind_dn

    @catch_exception
    def connect(self) -> None:
        """ Should connect to ad server """
        self.bind(self.bind_dn, self.auth_pass)

    def __str__(self) -> str:
        return f'uri: {self.uri}\nbind_dn: {self.bind_dn}\nauth_pass: {self.auth_pass}\n{self.state}'
