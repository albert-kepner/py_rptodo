import configparser
from pathlib import Path

from rptodo import DB_WRITE_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path(__file__).parent.joinpath(".default_todo.json")

def get_datbase_path(config_file: Path) -> Path:
    """returns the current path to the to-do database"""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)

    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    """Creates the to-do database"""
    try:
        db_path.write_text("[]") # Initializes an empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR