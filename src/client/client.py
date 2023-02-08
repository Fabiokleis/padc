import sys, ldap
from typing import List, Dict, Tuple, Optional, Any
from enum import Enum

from ldap.modlist import modifyModlist
from .state import State

class Scope(Enum):
    """ Search Scope interface """
    Base = ldap.SCOPE_BASE
    SubTree = ldap.SCOPE_SUBTREE

    def __repr__(self) -> str:
        return f'Scope: {self.name}'

class Client:
    """ Base class to manipulate LDAP connections """
    
    def __init__(self, uri: str, log_level=0, debug=False) -> None:
        """ Initialize a new LDAP object """

        self.connection = initialize(uri, log_level, sys.stderr)
        self.connection.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        self.connection.set_option(ldap.OPT_REFERRALS, 0)

        if debug:
            self.connection.set_option(ldap.OPT_DEBUG_LEVEL, 255)

        self.state = State.Connected

    def start_tls(self, ca_path=None) -> None:
        """ Start tls connection by passing a ca-certificate path """

        assert self.state == State.Connected

        if ca_path:
            self.connection.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, OPT_X_TLS_DEMAND)
            self.connection.set_option(ldap.OPT_X_TLS_CACERTFILE, ca_path)

        self.connection.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
        self.connection.start_tls_s()

    def search(self, base: str, s_filter: str,  attr: Optional[List[str]], scope: Scope=Scope.SubTree) -> List[str]|None:
        """ Perform LDAP search on target DN, if attributes are None all objects will return """

        assert self.state == State.Signed

        return self.connection.search_s(base, scope.value, s_filter, attr, 0)
    

    def modify(self, target_dn: str, entry: Tuple[Dict[str, Any], Dict[str, Any]]) -> None:
        """ Modify entries by modlist operation on it based on argument entry """

        assert self.state == State.Signed
        old,new = entry
        modlist = modifyModlist(old, new)
        
        self.connection.modify_s(target_dn, modlist)

    def bind(self, new_bind: str, new_pass: str) -> None:
        """ Bind to connected server """

        assert self.state == State.Connected

        self.connection.simple_bind(new_bind, new_pass)
        self.state = State.Signed

    def close(self) -> None:
        """ Close connection with LDAP server, turn connection object invalid """

        assert self.state != State.Disconnected
        self.connection.unbind_s()
        self.state = State.Disconnected

