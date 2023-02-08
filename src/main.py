from msad import MsAD 
from msad import AccountControlCode as Acc

# local Active Directory settings
uri = 'ldap://192.168.0.213'
bind_dn = 'administrator@rts.local'
auth_pass = 'Mypasswd@123'
ca_path = None #'/etc/ca-certificates/trust-source/anchors/ca-test.pem'
target = ''
base_dn = 'DC=RTS,DC=LOCAL'
s_filter = '(&(objectClass=User)(sAMAccountName=tester))'
attr = ['userAccountControl', 'givenName', 'cn', 'dn', 'pwdLastSet']

def main():
    ldap = MsAD(uri, base_dn, bind_dn, auth_pass)
    ldap.start_tls(ca_path)
    ldap.connect()
    ldap.modify_account_control(s_filter, Acc.DisableAccount)
    ldap.close()

if __name__ == "__main__":
    main()
