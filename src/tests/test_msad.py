import unittest
from msad import MsAD
from msad import AccountControlCode as Acc
from msad.ad_error_handler import ADSuccessResult
from cli.users_utils import load_env_variables_from_file, ensure_loaded_variables


class MsADTest(unittest.TestCase):
    """Active Directory unittest class."""

    def setUp(self):
        """Load needed env variables."""
        self.config = ensure_loaded_variables(load_env_variables_from_file(".env"))
        self.uri = self.config["URI"]
        self.base_dn = self.config["BASE_DN"]
        self.bind_dn = self.config["BIND_DN"]
        self.auth_pass = self.config["AUTH_PASS"]
        self.ca_path = self.config["CA_PATH"] 

        self.ldap = MsAD(self.uri, self.base_dn, self.bind_dn, self.auth_pass, False)
        self.new_user = "unittester pythonic"
        self.new_passwd = "unittestPassword@123"
        self.filter = '(&(objectClass=User)(sAMAccountName=unittester))'

    def test_connect_to_ad_server(self):
        """Should connect to ad server!"""
        tls = self.ldap.start_tls(self.ca_path)
        self.assertTrue(isinstance(tls, ADSuccessResult))
        print(tls.unwrap())

        conn = self.ldap.connect()
        self.assertTrue(isinstance(conn, ADSuccessResult))
        print(conn.unwrap())

        close = self.ldap.close()
        self.assertTrue(isinstance(close, ADSuccessResult))
        print(close.unwrap())
 
    def test_create_account(self):
        """Should create a new user in ad server!"""
        self.ldap.start_tls(self.ca_path)
        self.ldap.connect()

        user = self.ldap.create_user(self.new_user, self.new_passwd, Acc.NormalAccount)
        self.assertTrue(isinstance(user, ADSuccessResult))
        print(user.unwrap())

        self.ldap.close()

    def test_disable_account(self):
        """Should disable a user account by modify userAccountCode!"""
        self.ldap.start_tls(self.ca_path)
        self.ldap.connect()

        mod = self.ldap.modify_account_control(self.filter, Acc.DisableAccount)
        self.assertTrue(isinstance(mod, ADSuccessResult))
        print(mod.unwrap())

        self.ldap.close()

    def test_enable_account(self):
        """Should enable a user account by modify userAccountCode!"""
        self.ldap.start_tls(self.ca_path)
        self.ldap.connect()

        mod = self.ldap.modify_account_control(self.filter, Acc.NormalAccount)
        self.assertTrue(isinstance(mod, ADSuccessResult))
        print(mod.unwrap())        

        self.ldap.close()

  
    def test_delete_account(self):
        """Should delete a user account!"""
        self.ldap.start_tls(self.ca_path)
        self.ldap.connect()

        user = self.ldap.delete_user(self.new_user)
        self.assertTrue(isinstance(user, ADSuccessResult))
        print(user.unwrap())

        self.ldap.close()




if __name__ == '__main__':
    unittest.main()
