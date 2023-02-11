import sys, ldap
from typing import List, Dict, Tuple, Optional, Any
from enum import Enum

from ldap.modlist import modifyModlist, addModlist
from ldap.dn import str2dn
from .state import State
from error_handler import catch_exception, LdapSuccessResult

class Scope(Enum):
    """ Search Scope interface """
    Base = ldap.SCOPE_BASE
    SubTree = ldap.SCOPE_SUBTREE

    def __repr__(self) -> str:
        return f'Scope: {self.name}'

class Client:
    """ Base class to manipulate LDAP connections """
   
    @catch_exception
    def __init__(self, uri: str, log_level=0, debug=False) -> None:
        """ Initialize a new LDAP object """

        self.debug = debug
        self.connection = ldap.initialize(uri, log_level, sys.stderr)
        self.connection.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        self.connection.set_option(ldap.OPT_REFERRALS, 0)

        if self.debug:
            self.connection.set_option(ldap.OPT_DEBUG_LEVEL, 255)

        self.state = State.Connected

    @catch_exception
    def start_tls(self, ca_path=None) -> LdapSuccessResult:
        """ Start tls connection by passing a ca-certificate path """

        assert self.state == State.Connected, "Cannot start tls without initialized connection"

        if ca_path:
            self.connection.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
            self.connection.set_option(ldap.OPT_X_TLS_CACERTFILE, ca_path)

        self.connection.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
        self.connection.start_tls_s()
        return LdapSuccessResult("Started tls ldap server connection")

    @catch_exception
    def search(self, base: str, s_filter: str,  attr: Optional[List[str]], scope: Scope=Scope.SubTree) -> LdapSuccessResult:
        """ Perform LDAP search on target DN, if attributes are None all objects will return """

        assert self.state == State.Signed, "Cannot perform search without a signed connection"
        entry = self.connection.search_s(base, scope.value, s_filter, attr, 0)
        return LdapSuccessResult(entry)
    
    @catch_exception
    def modify(self, target_dn: str, entry: Tuple[Dict[str, Any], Dict[str, Any]]) -> LdapSuccessResult:
        """ Modify entries by modlist operation on it based on argument entry """

        assert self.state == State.Signed, "Cannot perform modify without a signed connection"
        old,new = entry
        modlist = modifyModlist(old, new)
        
        self.connection.modify_s(target_dn, modlist)
        return LdapSuccessResult(f"Modified {target_dn}")

    @catch_exception
    def add(self, target_dn: str, entry: Dict[str, Any]) -> LdapSuccessResult:
        """ Create a new entry at target DN """
        
        assert self.state == State.Signed, "Cannot perform add without a signed connection"

        modlist = addModlist(entry)
        self.connection.add_s(target_dn, modlist)
        return LdapSuccessResult(f"Added new entry at {target_dn}")

    @catch_exception
    def delete(self, target_dn: str) -> LdapSuccessResult:
        """ Delete entry based on target DN """
        assert self.state == State.Signed, "Cannot perform delete without signed connection"

        self.connection.delete_s(target_dn)
        return LdapSuccessResult(f"Deleted {target_dn} entry")


    @catch_exception
    def parse_dn(self, target_dn: str) -> LdapSuccessResult:
        """ Parse target DN to sepated elements """
        return LdapSuccessResult(str2dn(target_dn, ldap.DN_FORMAT_LDAPV3))

    @catch_exception
    def bind(self, new_bind: str, new_pass: str) -> LdapSuccessResult:
        """ Bind to connected server """

        assert self.state == State.Connected, "Cannot perform bind without connection"

        self.connection.simple_bind_s(new_bind, new_pass)
        self.state = State.Signed

        return LdapSuccessResult(f"Binded in ldap server using {new_bind} and {new_pass}")

    @catch_exception
    def close(self) -> LdapSuccessResult:
        """ Close connection with LDAP server, turn connection object invalid """

        assert self.state != State.Disconnected, "Cannot close connection without a connection"
        self.connection.unbind_s()
        self.state = State.Disconnected

        return LdapSuccessResult("Unbinded connection in ldap server")

