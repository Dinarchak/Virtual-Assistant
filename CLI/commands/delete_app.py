from sqlalchemy import create_engine
from db import Repository
from settings import config
import click


def delete_app(name: str) -> None:
    """Удаляет программу из списка отслеживаемых

    Args:
        names (str): имя программы
    """
    engine = create_engine(config['db_url'])
    repo = Repository(engine)
    if repo.delete_app(name):
        click.echo(f'Процесса с именем {name} нет в списке отслеживаемых')
