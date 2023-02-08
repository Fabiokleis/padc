from client import Client, Scope
from enum import Enum
from typing import List, Dict, Any
from .error_handler import catch_exception

class AccountControlCode(Enum):
    """ Possible Account Control States 
    ref <https://learn.microsoft.com/en-us/troubleshoot/windows-server/identity/useraccountcontrol-manipulate-account-properties>
    """

    NormalAccount = 512
    DisableAccount = 514

    def __repr__(self) -> str:
        return f'AccountControl: {self.name}'


class MsAD(Client):
    """ Active Directory client """

    @catch_exception
    def __init__(self, uri: str, base_dn: str, bind_dn: str, auth_pass: str, debug=False) -> None:
        Client.__init__(self, uri, 0, debug)
        self.uri = uri
        self.base_dn = base_dn
        self.auth_pass = auth_pass
        self.bind_dn = bind_dn

    @catch_exception
    def connect(self) -> None:
        """ Should connect to ad server """
        self.bind(self.bind_dn, self.auth_pass)

    @catch_exception 
    def get_entries(self, s_filter: str, attr: List[str], scope: Scope=Scope.SubTree) -> List[Dict[Any, Any]]:
        """ Get attributes entries by permforming ldap search over a specified base and scope """
        raw_entry = self.search(self.base_dn, s_filter, attr, scope)
        assert raw_entry is not None

        entry = list()

        assert_dict = lambda x: type(x) is dict and x

        for _,val in raw_entry:
            value = assert_dict(val)
            if value:
                entry.append(value)        

        return entry

    @catch_exception
    def modify_account_control(self, s_filter: str, state: AccountControlCode) -> None:
        """ Modify user account control, useful to disable account """

        user_entry = self.get_entries(s_filter, ['distinguishedName', 'userAccountControl'])[0]
        target_dn = user_entry['distinguishedName'][0].decode()
        old_acc = { 'userAccountControl': user_entry['userAccountControl']}
        new_acc = {'userAccountControl': [f'{state.value}'.encode()]}
        
        entry = (old_acc, new_acc)
        
        self.modify(target_dn, entry)
        

    def __str__(self) -> str:
        return f'uri: {self.uri}\nbind_dn: {self.bind_dn}\nauth_pass: {self.auth_pass}\n{self.state}'

