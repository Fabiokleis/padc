from msad import MsAD 
from msad import AccountControlCode as Acc
from msad.msad import AccountControlCode

# local Active Directory settings
uri = 'ldap://192.168.0.213'
bind_dn = 'administrator@rts.local'
auth_pass = 'Mypasswd@123'
ca_path = None #'/etc/ca-certificates/trust-source/anchors/ca-test.pem'
base_dn = 'DC=RTS,DC=LOCAL'
s_filter = '(&(objectClass=User)(sAMAccountName=tester))'
attr = ['userAccountControl', 'givenName', 'cn', 'dn', 'pwdLastSet']

def create_user() -> None:
    """ Should create user at Active Directory """
    ldap = MsAD(uri, base_dn, bind_dn, auth_pass)
    ldap.start_tls(ca_path)
    ldap.connect()

    new_user = "testerpy pythontester"
    new_passwd = "Python@135"
    ldap.create_user(new_user, new_passwd, Acc.NormalAccount)

    ldap.close()

def main():
    ldap = MsAD(uri, base_dn, bind_dn, auth_pass)
    ldap.start_tls(ca_path)
    ldap.connect()
    ldap.modify_account_control(s_filter, Acc.DisableAccount)
    ldap.close()

if __name__ == "__main__":
    create_user()
