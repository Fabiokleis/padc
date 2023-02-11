# p_ad

lab using python-ldap lib to create connection with Active Directory

## Setup
```console
python -m venv env && source env/bin/activate && pip install -r requirements.txt
```

## Running
```console
chmod +x init.sh && ./init.sh
```

## Testing
Create .env file inside src/
### .env
```
URI='ldap://192.168.0.213'
BIND_DN='administrator@rts.local'
AUTH_PASS='Mypasswd@123'
CA_PATH='' 
BASE_DN='DC=RTS,DC=LOCAL'
```

```console
cd src && python -m unittest test.py
```
