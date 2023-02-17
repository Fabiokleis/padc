import typer
from .users_utils import *
from msad import match_code, AccountControlCode as Acc
from pathlib import Path

users = typer.Typer(help="Users subcommand")

@users.command("create-ldif")
def cli_create_from_ldif(
        from_file: Optional[Path] = typer.Option(
            None, 
            "--file",
            "-f",
            help="A .env file or load from host envvars by ignoring this argument",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
        from_ldif: Optional[Path] = typer.Option(
            ..., 
            "--ldif",
            "-l",
            help="A ldif file to create a new user",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
        debug: bool = typer.Option(False, help="Enable debug mode")
        ):
    """Create a new user account from ldif in Microsoft Active Directory Server."""
    config = {}
    if from_file:
        config = load_env_variables_from_file(str(from_file))
    else:
        config = load_env_variables()

    config = ensure_loaded_variables(config)

    create_user_from_ldif(str(from_ldif), config, debug)

@users.command("create")
def cli_create_user(
        from_file: Optional[Path] = typer.Option(
            None, 
            "--file",
            "-f",
            help="A .env file or load from host envvars by ignoring this argument",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
        name: str = typer.Argument(..., help="A CN attribute value, don't pass a single name"), 
        password: str = typer.Argument(..., help="A user account password, unicodePwd will be create"),
        account_control_code: int = typer.Option(
            512,
            "--acc",
            "-c",
            help="User Account Control Code, 512 is NormalAccount and 514 is DisableAccount",
            show_default=True
            ),
        debug: bool = typer.Option(False, help="Enable debug mode")
        ):

    """Create a new user account in Microsoft Active Directory Server."""
    print(f"A new {name} will be created with {password}")
    config = {}
    if from_file:
        config = load_env_variables_from_file(str(from_file))
    else:
        config = load_env_variables()

    config = ensure_loaded_variables(config)

    create_user(name, password, config, match_code(account_control_code), debug)

@users.command("delete")
def cli_delete_user(
        from_file: Optional[Path] = typer.Option(
            None, 
            "--file",
            "-f",
            help="A .env file or load from host envvars by ignoring this argument",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
        name: str = typer.Argument(..., help="A CN attribute value, don't pass a single name"),
        debug: bool = typer.Option(False, help="Enable debug mode")
        ):

    """Delete a user account in Microsoft Active Directory Server."""
    print(f"A new {name} will be delete")
    config = {}
    if from_file:
        config = load_env_variables_from_file(str(from_file))
    else:
        config = load_env_variables()

    config = ensure_loaded_variables(config)

    delete_account(name, config, debug)

@users.command("disable")
def cli_disable_user(
        from_file: Optional[Path] = typer.Option(
            None, 
            "--file",
            "-f",
            help="A .env file or load from host envvars by ignoring this argument",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
        name: str = typer.Argument(..., help="A sAMAccountName attribute value, don't pass CN "), 
        debug: bool = typer.Option(False, help="Enable debug mode")
        ):

    """Disable a user account in Microsoft Active Directory Server."""
    print(f"This {name} account will be disable")
    config = {}
    if from_file:
        config = load_env_variables_from_file(str(from_file))
    else:
        config = load_env_variables()

    config = ensure_loaded_variables(config)

    modify_acc(name, Acc.DisableAccount, config, debug)

@users.command("enable")
def cli_enable_user(
        from_file: Optional[Path] = typer.Option(
            None, 
            "--file",
            "-f",
            help="A .env file or load from host envvars by ignoring this argument",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
        name: str = typer.Argument(..., help="A sAMAccountName attribute value, don't pass CN "), 
        debug: bool = typer.Option(False, help="Enable debug mode")
        ):

    """Enable a user account in Microsoft Active Directory Server."""
    print(f"This {name} account will be enable")
    config = {}
    if from_file:
        config = load_env_variables_from_file(str(from_file))
    else:
        config = load_env_variables()

    config = ensure_loaded_variables(config)

    modify_acc(name, Acc.NormalAccount, config, debug) 

@users.command("add-to-group")
def cli_add_to_group(
        from_file: Optional[Path] = typer.Option(
            None, 
            "--file",
            "-f",
            help="A .env file or load from host envvars by ignoring this argument",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
        name: str = typer.Argument(..., help="A sAMAccountName attribute value, don't pass CN "), 
        groupdn: str = typer.Argument(..., help="A group DN attribute value"),
        debug: bool = typer.Option(False, help="Enable debug mode")
        ):

    """Add a user account to group in Microsoft Active Directory Server."""
    print(f"This {name} account will be a member of {groupdn} group")
    config = {}
    if from_file:
        config = load_env_variables_from_file(str(from_file))
    else:
        config = load_env_variables()

    config = ensure_loaded_variables(config)

    add_account_to_group(name, groupdn, config, debug) 

@users.command("remove-from-group")
def cli_remove_from_group(
        from_file: Optional[Path] = typer.Option(
            None, 
            "--file",
            "-f",
            help="A .env file or load from host envvars by ignoring this argument",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
        name: str = typer.Argument(..., help="A sAMAccountName attribute value, don't pass CN "), 
        groupdn: str = typer.Argument(..., help="A group DN attribute value"),
        debug: bool = typer.Option(False, help="Enable debug mode")
        ):

    """Remove user account from group in Microsoft Active Directory Server."""
    print(f"This {name} account will be remove from {groupdn} group")
    config = {}
    if from_file:
        config = load_env_variables_from_file(str(from_file))
    else:
        config = load_env_variables()

    config = ensure_loaded_variables(config)

    remove_account_from_group(name, groupdn, config, debug) 
