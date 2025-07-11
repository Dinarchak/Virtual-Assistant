from sqlalchemy import create_engine, select
from db.repository import Repository
from settings import config
from typing import List
import click

# todo: через pydantic отслеживать, чтобу type_name не был None
# todo: вместо имени типа сразу передавать его id
def add_app(name: str, types: List[str]) -> None:
    """Добавить новое приложение в список отслеживаемого

    Args:
        name (str): имя приложения
        types (List[str]): категории приложения
    """
    engine = create_engine(config['db_url'])
    repo = Repository(engine)
    repo.add_app(name, types)