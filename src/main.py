from msad import MsAD 
from msad import AccountControlCode as Acc
from dotenv import dotenv_values

# load .env variables
# local Active Directory settings
config = dotenv_values(".env")

def create_user(uri, base_dn, bind_dn, auth_pass, ca_path):
    """ test create user in ms ad server """
    ldap = MsAD(uri, base_dn, bind_dn, auth_pass, False)
    print(ldap.start_tls(ca_path).unwrap())
    print(ldap.connect())
    print(ldap.create_user("unittester pythonic", "uniTtest@213", Acc.NormalAccount))
    print(ldap.close().unwrap())

def disable_account(uri, base_dn, bind_dn, auth_pass, ca_path):
    """ test disable user account in ms ad server """
    ldap = MsAD(uri, base_dn, bind_dn, auth_pass, False)
    print(ldap.start_tls(ca_path).unwrap())
    print(ldap.connect())
    print(ldap.modify_account_control("(&(objectClass=User)(sAMAccountName=unittester))", Acc.DisableAccount))
    print(ldap.close().unwrap())

def enable_account(uri, base_dn, bind_dn, auth_pass, ca_path):
    """ test enable user account in ms ad server """
    ldap = MsAD(uri, base_dn, bind_dn, auth_pass, False)
    print(ldap.start_tls(ca_path).unwrap())
    print(ldap.connect())
    print(ldap.modify_account_control("(&(objectClass=User)(sAMAccountName=unittester))", Acc.NormalAccount))
    print(ldap.close().unwrap())

def delete_account(uri, base_dn, bind_dn, auth_pass, ca_path):
    """ teste delete user account in ms ad server """
    ldap = MsAD(uri, base_dn, bind_dn, auth_pass, False)
    print(ldap.start_tls(ca_path).unwrap())
    print(ldap.connect())
    print(ldap.delete_user("unittester pythonic"))
    print(ldap.close().unwrap())


if __name__ == "__main__":
    uri = config["URI"]
    base_dn = config["BASE_DN"]
    bind_dn = config["BIND_DN"]
    auth_pass = config["AUTH_PASS"]
    ca_path = None #config["CA_PATH"]

    #create_user(uri, base_dn, bind_dn, auth_pass, ca_path)
    #disable_account(uri, base_dn, bind_dn, auth_pass, ca_path)
    #enable_account(uri, base_dn,bind_dn,auth_pass, ca_path)
    #delete_account(uri, base_dn, bind_dn, auth_pass, ca_path)
