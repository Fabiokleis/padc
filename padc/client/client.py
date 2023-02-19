import sys, ldap
from typing import List, Dict, Tuple, Optional, Any
from enum import Enum

from ldap.modlist import modifyModlist, addModlist
from ldap.dn import str2dn
from ldif import LDIFRecordList
from .state import State
from .error_handler import catch_exception, LdapSuccessResult

class Scope(Enum):
    """Search Scope interface."""
    Base = ldap.SCOPE_BASE
    SubTree = ldap.SCOPE_SUBTREE

    def __repr__(self) -> str:
        return f'Scope: {self.name}'

class Client:
    """Base class to manipulate LDAP connections!"""
   
    @catch_exception
    def __init__(self, uri: str, log_level: int = 0, debug: bool = False) -> None:
        """Initialize a new LDAP object."""

        self.debug = debug
        self.connection = ldap.initialize(uri, log_level, sys.stderr)
        self.connection.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        self.connection.set_option(ldap.OPT_REFERRALS, 0)

        if self.debug:
            self.connection.set_option(ldap.OPT_DEBUG_LEVEL, 255)

        self.state = State.Connected

    @catch_exception
    def _start_tls(self, ca_path: Optional[str] = None) -> LdapSuccessResult:
        """Start tls connection by passing a ca-certificate path."""

        assert self.state == State.Connected, "Cannot start tls without initialized connection"

        if ca_path:
            self.connection.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
            self.connection.set_option(ldap.OPT_X_TLS_CACERTFILE, ca_path)

        self.connection.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
        self.connection.start_tls_s()
        return LdapSuccessResult("_start_tls: Started tls ldap server connection")

    @catch_exception
    def _search(self, base: str, s_filter: str,  attr: Optional[List[str]], scope: Scope = Scope.SubTree) -> LdapSuccessResult:
        """Perform LDAP search on target DN, if attributes are None all objects will return."""

        assert self.state == State.Signed, "Cannot perform search without a signed connection"
        entry = self.connection.search_s(base, scope.value, s_filter, attr, 0)
        return LdapSuccessResult(entry)
   
    @catch_exception
    def _modify_add(self, target_dn: str, entry: Dict[str, Any]) -> LdapSuccessResult:
        """Modify entry by modlist add operation on it at target_dn."""
        assert self.state == State.Signed, "Cannot perform modify without a signed connection"
        modlist = [ (ldap.MOD_ADD, k, v) for k,v in entry.items() ]
        self.connection.modify_s(target_dn, modlist)
        return LdapSuccessResult(f"_modify_add: {target_dn}")

    @catch_exception
    def _modify_delete(self, target_dn: str, entry: Dict[str, Any]) -> LdapSuccessResult:
        """Modify entry by modlist delete operation on it at target_dn."""
        assert self.state == State.Signed, "Cannot perform modify without a signed connection"
        modlist = [ (ldap.MOD_DELETE, k, v) for k,v in entry.items() ]
        self.connection.modify_s(target_dn, modlist)
        return LdapSuccessResult(f"_modify_delete: {target_dn}")

    @catch_exception
    def _modify_replace(self, target_dn: str, entry: Tuple[Dict[str, Any], Dict[str, Any]]) -> LdapSuccessResult:
        """Modify entries by modlist replace (delete and add) operation on it based on argument entry."""

        assert self.state == State.Signed, "Cannot perform modify without a signed connection"
        old,new = entry
        modlist = modifyModlist(old, new)
        
        self.connection.modify_s(target_dn, modlist)
        return LdapSuccessResult(f"_modify_replace: {target_dn}")

    @catch_exception
    def _add(self, target_dn: str, entry: Dict[str, Any]) -> LdapSuccessResult:
        """Create a new entry at target DN."""
        
        assert self.state == State.Signed, "Cannot perform add without a signed connection"

        modlist = addModlist(entry)
        self.connection.add_s(target_dn, modlist)
        return LdapSuccessResult(f"_add: {target_dn}")

    @catch_exception
    def _delete(self, target_dn: str) -> LdapSuccessResult:
        """Delete entry based on target DN."""
        assert self.state == State.Signed, "Cannot perform delete without signed connection"

        self.connection.delete_s(target_dn)
        return LdapSuccessResult(f"_delete: {target_dn}")

    @catch_exception
    def _parse_dn(self, target_dn: str) -> LdapSuccessResult:
        """Parse target DN to sepated elements."""
        return LdapSuccessResult(str2dn(target_dn, ldap.DN_FORMAT_LDAPV3))

    @catch_exception
    def _parse_ldif(self, ldif_path: str) -> LdapSuccessResult:
        """Parse a ldif file, return all records inside payload."""
        parser = LDIFRecordList(open(ldif_path, "r"))
        parser.parse()
        return LdapSuccessResult(parser.all_records)

    @catch_exception
    def _bind(self, new_bind: str, new_pass: str) -> LdapSuccessResult:
        """Bind to connected server."""

        assert self.state == State.Connected, "Cannot perform bind without connection"

        self.connection.simple_bind_s(new_bind, new_pass)
        self.state = State.Signed

        return LdapSuccessResult(f"_bind: {new_bind}")

    @catch_exception
    def _close(self) -> LdapSuccessResult:
        """Close connection with LDAP server, turn connection object invalid."""

        assert self.state == State.Signed, "Cannot close connection without a connection"
        self.connection.unbind_s()
        self.state = State.Disconnected

        return LdapSuccessResult("_close: Unbinded connection in ldap server")

