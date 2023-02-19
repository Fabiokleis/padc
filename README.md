# padc

cli using [python-ldap](https://github.com/python-ldap/python-ldap) lib to create connections with Active Directory
this project use [poetry](https://python-poetry.org)

## Setup for development
create virtual environment
```console
python -m venv .venv
```
activate environment
```console
poetry shell 
```
install `padc`
```console
poetry install
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

`padc` has logging_settings.ini inside `padc/config`
```ini
[loggers]
keys = root

[handlers]
keys = FileHandler,StreamHandler

[formatters]
keys = simpleFormatter

[logger_root]
level = DEBUG
handlers = FileHandler,StreamHandler

[handler_FileHandler]
class     = FileHandler
formatter = simpleFormatter
args      = ('padc.log', 'a')

[handler_StreamHandler]
class     = StreamHandler
formatter = simpleFormatter
args      = (sys.stdout,)

[formatter_simpleFormatter]
format = %(asctime)s:%(levelname)s: %(message)s
```

## Install padc from pypi
```console
pip install padc
```
You can modify where log file will be created by editing logging_settings.ini
the default file is created at current directory with name 'padc.log'

## Running
cli written in [Typer](https://github.com/tiangolo/typer) to manipulate operations in AD

```console
padc --help
```
`users` is the main subcommand, every subcommand has a helper option
```console
pacd users --help
```

`padc` has in users subcommand some basic operations
if one of the supported operations run with `--debug` option
when errors occurs the traceback and exception will be raised.

exp:
```console
padc users create -f .env "Pingu pythonico" "Pingupassword@123" -c 514 --debug
```
```console
padc users create-ldif -f .env --ldif example.ldif
```
```console
padc users add-to-group --file .env "Pingu" "CN=testgroup,CN=Users,DC=RTS,DC=LOCAL" --debug
```
```console
padc users remove-from-group --file .env "Pingu" "CN=testgroup,CN=Users,DC=RTS,DC=LOCAL"
```
```console
padc users delete --file .env "Pingu pythonico"
```
```console
padc users enable -f .env "Pingu" --debug
```
```console
padc users disable "Pingu" --debug
```

## Testing
Simple Unittest to create/delete/modify user account in AD
```console
python -m unittest -v tests.test_msad
```

## Building
```console
poetry build
```
