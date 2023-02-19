import typer
from .users import users

# Create cli and Registry subcommands
app = typer.Typer(help="Python active directory user management cli!", pretty_exceptions_show_locals=False)
app.add_typer(users, name="users")

def run():
    app()
