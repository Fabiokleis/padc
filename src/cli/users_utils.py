import os
from msad import MsAD
from msad import AccountControlCode as Acc
from typing import Dict
from dotenv import dotenv_values
from typing import Dict, Optional

from msad.msad import AccountControlCode

# Local Active Directory Settings

def load_env_variables_from_file(file_name: str) -> Dict[str, Optional[str]]:
    return dotenv_values(file_name)

def load_env_variables() -> Dict[str, Optional[str]]:
    return {
        "URI" : os.environ.get("URI"),
        "BASE_DN": os.environ.get("BASE_DN"),
        "BIND_DN": os.environ.get("BIND_DN"),
        "AUTH_PASS": os.environ.get("AUTH_PASS"),
        "CA_PATH": os.environ.get("CA_PATH")
    }

def ensure_loaded_variables(config: Dict[str, Optional[str]]) -> Dict[str, str]:
    d = {}
    for k,v in config.items():
        if v is not None:
            d[f"{k}"] = v
        else:
            d[f"{k}"] = ""
    return d 

def create_user(name: str, passwd: str, config: Dict[str, str], acc: Acc, debug = False):
    """ Create user in ms ad server """
    ldap = MsAD(config["URI"], config["BASE_DN"], config["BIND_DN"], config["AUTH_PASS"], debug)
    print(ldap.start_tls(config["CA_PATH"]).unwrap())
    print(ldap.connect())
    print(ldap.create_user(name, passwd, acc))
    print(ldap.close().unwrap())

def create_user_from_ldif(from_ldif: str, config: Dict[str, str], debug = False):
    """ Create user in ms ad server from ldif file """
    ldap = MsAD(config["URI"], config["BASE_DN"], config["BIND_DN"], config["AUTH_PASS"], debug)
    print(ldap.start_tls(config["CA_PATH"]).unwrap())
    print(ldap.connect())
    print(ldap.create_user_from_ldif(from_ldif))
    print(ldap.close().unwrap())

def add_account_to_group(name: str, group_dn: str, config: Dict[str, str], debug = False):
    """ Add a user account to a group of Active directory server """
    ldap = MsAD(config["URI"], config["BASE_DN"], config["BIND_DN"], config["AUTH_PASS"], debug)
    print(ldap.start_tls(config["CA_PATH"]).unwrap())
    print(ldap.connect())
    s_filter = f"(&(objectClass=User)(sAMAccountName={name}))"
    print(ldap.add_account_to_group(s_filter, group_dn))
    print(ldap.close().unwrap())

def remove_account_from_group(name: str, group_dn: str, config: Dict[str, str], debug = False):
    """ Remove user account from a group of Active directory server """
    ldap = MsAD(config["URI"], config["BASE_DN"], config["BIND_DN"], config["AUTH_PASS"], debug)
    print(ldap.start_tls(config["CA_PATH"]).unwrap())
    print(ldap.connect())
    s_filter = f"(&(objectClass=User)(sAMAccountName={name}))"
    print(ldap.remove_account_from_group(s_filter, group_dn))
    print(ldap.close().unwrap())

def modify_acc(name: str, acc: AccountControlCode, config: Dict[str, str], debug = False):
    """ Enable/Disable user account in ms ad server """
    ldap = MsAD(config["URI"], config["BASE_DN"], config["BIND_DN"], config["AUTH_PASS"], debug)
    print(ldap.start_tls(config["CA_PATH"]).unwrap())
    print(ldap.connect())
    s_filter = f"(&(objectClass=User)(sAMAccountName={name}))"
    print(ldap.modify_account_control(s_filter, acc))
    print(ldap.close().unwrap())

def delete_account(name: str, config: Dict[str, str], debug = False):
    """ Delete user account in ms ad server """
    ldap = MsAD(config["URI"], config["BASE_DN"], config["BIND_DN"], config["AUTH_PASS"], debug)
    print(ldap.start_tls(config["CA_PATH"]).unwrap())
    print(ldap.connect())
    print(ldap.delete_user(name))
    print(ldap.close().unwrap())

