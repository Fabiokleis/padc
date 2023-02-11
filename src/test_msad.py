import unittest
from msad import MsAD
from msad import AccountControlCode as Acc
from dotenv import dotenv_values
from error_handler import LdapSuccessResult

# load .env variables
# local Active Directory settings

config = dotenv_values(".env")

class MsADTest(unittest.TestCase):
    """ Active Directory unittest class """

    def setUp(self):
        self.uri = config["URI"]
        self.base_dn = config["BASE_DN"]
        self.bind_dn = config["BIND_DN"]
        self.auth_pass = config["AUTH_PASS"]
        self.ca_path = None #config["CA_PATH"] 
        self.ldap = MsAD(self.uri, self.base_dn, self.bind_dn, self.auth_pass)

    def test_connect_to_ad_server(self):
        """ Should connect to ad server """
        self.assertTrue(isinstance(self.ldap.start_tls(self.ca_path), LdapSuccessResult))
        self.assertTrue(self.ldap.connect(), str)
        self.assertTrue(isinstance(self.ldap.close(), LdapSuccessResult))
 
    def test_create_user(self):
        """ Should create a new user in ad server """
        self.assertTrue(isinstance(self.ldap.start_tls(self.ca_path), LdapSuccessResult))
        self.assertTrue(self.ldap.connect(), str)
        self.assertTrue(self.ldap.create_user("unitters pythonic", "uniTtest@213", Acc.NormalAccount), str)
        self.assertTrue(isinstance(self.ldap.close(), LdapSuccessResult))

    def test_disable_account(self):
        """ Should disable a user account by modify userAccountCode """
        self.assertTrue(isinstance(self.ldap.start_tls(self.ca_path), LdapSuccessResult))
        self.assertTrue(self.ldap.connect(), str)
        s_filter='(&(objectClass=User)(sAMAccountName=unitters))'
        self.assertTrue(self.ldap.modify_account_control(s_filter, Acc.DisableAccount), str)
        self.assertTrue(isinstance(self.ldap.close(), LdapSuccessResult))

if __name__ == '__main__':
    unittest.main()
