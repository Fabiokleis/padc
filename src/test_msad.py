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
        self.new_user = "unittester pythonic"
        self.new_passwd = "unittestPassword@123"
        self.filter = '(&(objectClass=User)(sAMAccountName=unittester))'

    def test_connect_to_ad_server(self):
        """ Should connect to ad server """
        tls = self.ldap.start_tls(self.ca_path)
        self.assertTrue(isinstance(tls, LdapSuccessResult))
        print(tls.unwrap())

        conn = self.ldap.connect()
        print(conn)
        self.assertTrue(isinstance(conn, str))

        close = self.ldap.close()
        self.assertTrue(isinstance(close, LdapSuccessResult))
        print(close.unwrap())
 
    def test_create_account(self):
        """ Should create a new user in ad server """
        self.assertTrue(isinstance(self.ldap.start_tls(self.ca_path), LdapSuccessResult))
        self.assertTrue(self.ldap.connect(), str)

        user = self.ldap.create_user(self.new_user, self.new_passwd, Acc.NormalAccount)
        self.assertTrue(isinstance(user, str))
        print(user)

        self.assertTrue(isinstance(self.ldap.close(), LdapSuccessResult))

    def test_disable_account(self):
        """ Should disable a user account by modify userAccountCode """
        self.assertTrue(isinstance(self.ldap.start_tls(self.ca_path), LdapSuccessResult))
        self.assertTrue(self.ldap.connect(), str)

        mod = self.ldap.modify_account_control(self.filter, Acc.DisableAccount)
        self.assertTrue(isinstance(mod, str))
        print(mod)

        self.assertTrue(isinstance(self.ldap.close(), LdapSuccessResult))

    def test_enable_account(self):
        """ Should enable a user account by modify userAccountCode """
        self.assertTrue(isinstance(self.ldap.start_tls(self.ca_path), LdapSuccessResult))
        self.assertTrue(self.ldap.connect(), str)

        mod = self.ldap.modify_account_control(self.filter, Acc.NormalAccount)
        self.assertTrue(isinstance(mod, str))
        print(mod)        

        self.assertTrue(isinstance(self.ldap.close(), LdapSuccessResult))
  
    def test_delete_account(self):
        """ Should delete a user account """
        self.assertTrue(isinstance(self.ldap.start_tls(self.ca_path), LdapSuccessResult))
        self.assertTrue(self.ldap.connect(), str)

        user = self.ldap.delete_user(self.new_user)
        self.assertTrue(isinstance(user, str))
        print(user)

        self.assertTrue(isinstance(self.ldap.close(), LdapSuccessResult))


if __name__ == '__main__':
    unittest.main()
