import ldap

# ref: https://stackoverflow.com/questions/11420464/catch-exceptions-inside-a-class
def catch_exception(f):
    """ function decorator exception handler """
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (ldap.LDAPError) as e:
            raise e
    return func

