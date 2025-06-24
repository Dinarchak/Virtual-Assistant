from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from settings import config
from db.models import Process, ProcessType
from db.repository import Repository
import click

# todo: через pydantic отслеживать, чтобу type_name не был None
# todo: вместо имени типа сразу передавать его id
def add_app(name: str, type_name: int) -> None:
    """Добавить новое приложение в список отслеживаемого

    Args:
        name (str): имя приложения
        type_name (int): тип приложения
    """
    engine = create_engine(config['db_url'])
    repo = Repository(engine)
    if type is None:
        click.echo('Нераспознанные тип программы')
        return
    repo.add_app(name, type_name)