from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Process
from settings import config
import click

def delete_app(names):
    engine = create_engine(config['db_url'])
    with Session(engine) as session:
        for procs_name in names:
            procs = session.scalars(select(Process).where(Process.name == procs_name)).first()
            if procs is None:
                click.echo(f'Процесса с именем {procs_name} нет в списке отслеживаемых')
                return
            session.delete(procs)
        session.commit()