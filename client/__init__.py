import sys,ldap
from .state import State

class Client:
    """ Base class to manipulate LDAP connections """
    
    #state = State.Created

    def __init__(self, uri: str, log_level=0, debug=False) -> None:
        """ Initialize a new LDAP object """

        self.connection = ldap.initialize(uri, log_level, sys.stderr)
        self.connection.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        self.connection.set_option(ldap.OPT_REFERRALS, 0)

        if debug:
            self.connection.set_option(ldap.OPT_DEBUG_LEVEL, 255)

        self.state = State.Connected


    def start_tls(self, ca_path=None) -> None:
        """ Start tls connection by passing a ca-certificate path """

        assert self.state == State.Connected

        if ca_path:
            self.connection.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
            self.connection.set_option(ldap.OPT_X_TLS_CACERTFILE, ca_path)

        self.connection.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
        self.connection.start_tls_s()


    def bind(self, new_bind: str, new_pass: str) -> None:
        """ Bind to connected server """

        assert self.state == State.Connected

        self.connection.simple_bind(new_bind, new_pass)
        self.state = State.Signed
