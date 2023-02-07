from msad import MsAD

# local Active Directory settings
uri = "ldap://192.168.0.213"
bind_dn = "administrator@rts.local"
auth_pass = "Mypasswd@123"
ca_path = None #"/etc/ca-certificates/trust-source/anchors/ca-test.pem"

def run():
    ldap = MsAD(uri, bind_dn, auth_pass)
    ldap.start_tls(ca_path)
    ldap.connect()
    print(ldap)

if __name__ == "__main__":
    run()
