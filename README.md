# p_ad

lab using [python-ldap](https://github.com/python-ldap/python-ldap) lib to create connection with Active Directory

## Setup
```console
python -m venv env && source env/bin/activate && pip install -e .
```
Create .env file inside root directory to establish a ldap connection
### .env
```
URI='ldap://192.168.0.213'
BIND_DN='administrator@rts.local'
AUTH_PASS='Mypasswd@123'
CA_PATH='' 
BASE_DN='DC=RTS,DC=LOCAL'
```

## Running
p_ad has a cli written in [Typer](https://github.com/tiangolo/typer) to manipulate operations in AD
```console
./env/bin/padc --help
```
`users` is the main subcommand, every subcommand has a helper option
```console
./env/bin/pacd users --help
```

`padc` has in users subcommand some basic operations
if one of the supported operations run with `--debug` option
when errors occurs the traceback and exception will be raised.

exp:
```console
./env/bin/padc users create -f .env "Pingu pythonico" "Pingupassword@123" -c 514 --debug
```
```console
./env/bin/padc users create-ldif -f .env --ldif example.ldif
```
```console
./env/bin/padc users add-to-group --file .env "Pingu" "CN=testgroup,CN=Users,DC=RTS,DC=LOCAL" --debug
```
```console
./env/bin/padc users remove-from-group --file .env "Pingu" "CN=testgroup,CN=Users,DC=RTS,DC=LOCAL"
```
```console
./env/bin/padc users delete --file .env "Pingu pythonico"
```
```console
./env/bin/padc users enable -f .env "Pingu" --debug
```
```console
./env/bin/padc users disable "Pingu" --debug
```

## Testing
Simple Unittest to create/delete/modify user account in AD
```console
python -m unittest -v tests.test_msad
```

## Building
Ensure that you have build package installed first
```console
pip install --upgrade build
```

```console
python -m build
```
