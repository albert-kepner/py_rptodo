from typing import Optional
import typer
from pathlib import Path
from typing_extensions import Annotated

from rptodo import ERRORS,  __app_name__, __version__, config, database, rptodo

app = typer.Typer()

@app.command()
def init(db_path: Annotated[
    str,
    typer.Option(
        "--db-path",
        "-db",
        prompt = "The to-do database location?"
    ),
] = str(database.DEFAULT_DB_FILE_PATH)) -> None:
    """Initializes the to-do database"""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database file failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    else:
        typer.secho(f"The to-do database is {db_path}", fg=typer.colors.GREEN)


def get_todoer() -> rptodo.Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "rptodo init"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    if db_path.exists():
        return rptodo.Todoer(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "rptodo init"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

@app.command()
def add(description: Annotated[
    list[str],
    typer.Argument(
        ...,
        help = "The to-do item description"
    )
], priority: Annotated[
    int,
    typer.Option(
        "--priority",
        "-p",
        min=1,
        max=3,
        help="The to-do item priority value"
    ),
] = 2) -> None:
    """Add a new to-do to the database"""
    todoer = get_todoer()
    todo, error = todoer.add(description, priority)
    if error:
        typer.secho(
            f'Adding to-do failed with "{ERRORS[error]}"', fg = typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f""" to-do: "{todo['Description']}" was added"""
            f""" with priority : {priority}""",
            fg=typer.colors.GREEN
        )



def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(version: Annotated[
    Optional[bool],
    typer.Option(
        "--version",
        "-v",
        help="Shows the application's version, and exits",
        callback=_version_callback,
        is_eager = True
    )
] = None) -> None:
    """The main entry point for the to-do application"""
    return