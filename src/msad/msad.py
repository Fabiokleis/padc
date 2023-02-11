from client import Client, Scope
from typing import List, Dict, Optional, Any
from enum import Enum

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

    def __init__(self, uri: str, base_dn: str, bind_dn: str, auth_pass: str, debug=False) -> None:
        Client.__init__(self, uri, 0, debug)
        self.uri = uri
        self.base_dn = base_dn
        self.auth_pass = auth_pass
        self.bind_dn = bind_dn

    def connect(self) -> str:
        """ Should connect to ad server, return true if bind works or raise a ldap error """
        return self.bind(self.bind_dn, self.auth_pass).unwrap()

    def create_user(self, user_name: str, user_password: str, acc: Optional[AccountControlCode], exp: int=0, lockout: int=0) -> str:
        """ Should create a new user under Active Directory return true if create works or raise a ldap error """
        name,sn = user_name.split()
        parsed_dn = self.parse_dn(self.base_dn).unwrap()
        principal_name = f"{name}@{parsed_dn[0][0][1]}.{parsed_dn[1][0][1]}"

        target_dn = f"CN={user_name},CN=Users,{self.base_dn}"
        entry = {}
        entry['objectclass'] = [b'top', b'person', b'organizationalPerson', b'user']
        entry['cn'] = user_name.encode('utf-8')
        entry['sn'] = sn.encode('utf-8')
        entry['unicodePwd'] = f'"{user_password}"'.encode('utf-16-le')
        entry['sAMAccountName'] = name.encode('utf-8')
        entry['givenName'] = name.encode('utf-8')
        entry['userPrincipalName'] = principal_name.encode('utf-8')
        entry['displayName'] = user_name.encode('utf-8')
    
        if acc is not None and type(acc) == AccountControlCode:
            entry['userAccountControl'] = f'{acc.value}'.encode('utf-8')
        else:
            entry['userAccountControl'] = f'{AccountControlCode.NormalAccount.value}'.encode('utf-8')

        entry['lockoutTime'] = f'{lockout}'.encode('utf-8')
        entry['accountExpires'] = f'{exp}'.encode('utf-8')

        return self.add(target_dn, entry).unwrap()

    def get_entries(self, s_filter: str, attr: List[str], scope: Scope=Scope.SubTree) -> List[Dict[Any, Any]]:
        """ Get attributes entries by permforming ldap search over a specified base and scope """
        raw_entry = self.search(self.base_dn, s_filter, attr, scope).unwrap()
        assert raw_entry is not None

        entry = list()

        assert_dict = lambda x: type(x) is dict and x

        for _,val in raw_entry:
            value = assert_dict(val)
            if value:
                entry.append(value)        

        return entry

    def modify_account_control(self, s_filter: str, state: AccountControlCode) -> str:
        """ Modify user account control, useful to disable account, return true if could modify Acc or raise  ldap error """

        user_entry = self.get_entries(s_filter, ['distinguishedName', 'userAccountControl'])[0]
        target_dn = user_entry['distinguishedName'][0].decode()
        old_acc = {'userAccountControl': user_entry['userAccountControl']}
        new_acc = {'userAccountControl': [f'{state.value}'.encode()]}
        
        entry = (old_acc, new_acc)
        
        return self.modify(target_dn, entry).unwrap()
        
    def __str__(self) -> str:
        return f'uri: {self.uri}\nbind_dn: {self.bind_dn}\nauth_pass: {self.auth_pass}\n{self.state}'

