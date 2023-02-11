from msad import MsAD 
from msad import AccountControlCode as Acc
from dotenv import dotenv_values

# load .env variables
# local Active Directory settings
config = dotenv_values(".env")

def create_user(uri, base_dn, bind_dn, auth_pass, ca_path):
    ldap = MsAD(uri, base_dn, bind_dn, auth_pass, False)
    print(ldap.start_tls(ca_path).unwrap())
    print(ldap.connect())
    print(ldap.create_user("unitters3332 pythonic", "uniTtest@213", Acc.NormalAccount))
    print(ldap.close().unwrap())


if __name__ == "__main__":
    uri = config["URI"]
    base_dn = config["BASE_DN"]
    bind_dn = config["BIND_DN"]
    auth_pass = config["AUTH_PASS"]
    ca_path = None #config["CA_PATH"]

    create_user(uri, base_dn, bind_dn, auth_pass, ca_path)
