from cli.users_utils import *
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

def match_code(code: int) -> AccountControlCode:
        """ Match the possible code, return Normal Account variant if code doens't matchs any of them """
        match code:
            case 512:
                return AccountControlCode.NormalAccount
            case 514:
                return AccountControlCode.DisableAccount
            case _:
                return AccountControlCode.NormalAccount


class MsAD(Client):
    """ Active Directory client """

    def __init__(self, uri: str, base_dn: str, bind_dn: str, auth_pass: str, debug=False) -> None:
        Client.__init__(self, uri, 0, debug)
        self.uri = uri
        self.base_dn = base_dn
        self.auth_pass = auth_pass
        self.bind_dn = bind_dn

    def connect(self) -> str:
        """ Should connect to ad server """
        return self._bind(self.bind_dn, self.auth_pass).unwrap()

    def start_tls(self, ca_path: Optional[str]) -> str:
        """ Should start tls over created connection in Active Directory """
        return self._start_tls(ca_path).unwrap()

    def close(self) -> str:
        """ Should unbind a created connection in Active Directory """
        return self._close().unwrap()

    def create_user(self, user_name: str, user_password: str, acc: Optional[AccountControlCode], exp: int=0, lockout: int=0) -> str:
        """ Should create a new user in Active Directory """
        name,sn = user_name.split()
        parsed_dn = self._parse_dn(self.base_dn).unwrap()
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

        return self._add(target_dn, entry).unwrap()

    def delete_user(self, user_name: str) -> str:
        """ Should delete user by his username"""
        target_dn = f"CN={user_name},CN=Users,{self.base_dn}"
        return self._delete(target_dn).unwrap()

    def get_entries(self, s_filter: str, attr: List[str], scope: Scope=Scope.SubTree) -> List[Dict[Any, Any]]:
        """ Get attributes entries by permforming ldap search over a specified filter,base and scope """
        raw_entry = self._search(self.base_dn, s_filter, attr, scope).unwrap()

        entry = list()

        assert_dict = lambda x: type(x) is dict and x

        for _,val in raw_entry:
            value = assert_dict(val)
            if value:
                entry.append(value)        

        assert len(entry) >= 1, f"{s_filter} not found any entry"
        return entry

    def modify_account_control(self, s_filter: str, state: AccountControlCode) -> str:
        """ Should modify user account control """

        user_entry = self.get_entries(s_filter, ['distinguishedName', 'userAccountControl'])[0]
        target_dn = user_entry['distinguishedName'][0].decode()
        old_acc = {'userAccountControl': user_entry['userAccountControl']}
        new_acc = {'userAccountControl': [f'{state.value}'.encode()]}
        
        entry = (old_acc, new_acc)
        
        return self._modify_replace(target_dn, entry).unwrap()
    
    def create_user_from_ldif(self, ldif_path: str) -> str:
        """ Should create a new user from ldif file, if exists unicodePwd this function will encoded it """
        all_records = self._parse_ldif(ldif_path).unwrap()
        unicode_pwd = all_records[0][1].get('unicodePwd')
        if unicode_pwd:
            enc = f'"{unicode_pwd[0].decode()}"'.encode('utf-16-le')
            all_records[0][1].update({'unicodePwd': [enc]})
        return self._add(all_records[0][0], all_records[0][1]).unwrap()

    def add_account_to_group(self, s_filter, group_dn) -> str:
        """ Should add user account to AD group """
        user_entry = self.get_entries(s_filter, ['distinguishedName'])[0]
        user_dn = user_entry['distinguishedName'][0]
        entry = {'member': [user_dn]}

        return self._modify_add(group_dn, entry).unwrap()

    def remove_account_from_group(self, s_filter: str, group_dn: str) -> str:
        """ Should remove user account from a group of ms ad """
        user_entry = self.get_entries(s_filter, ['distinguishedName'])[0]
        user_dn = user_entry['distinguishedName'][0]
        entry = {'member': [user_dn]}
        return self._modify_delete(group_dn, entry).unwrap()

    def __str__(self) -> str:
        return f'uri: {self.uri}\nbind_dn: {self.bind_dn}\nauth_pass: {self.auth_pass}\n{self.state}'

