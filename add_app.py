from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from settings import config
from models import Process, ProcessType
import click

def add_app(name, type_name):
    engine = create_engine(config['db_url'])
    with Session(engine) as session:
        type = session.scalars(select(ProcessType).where(ProcessType.name==type_name)).first()
        if type is None:
            click.echo('Нераспознанные тип программы')        
        else:
            procs = Process(name=name, type_id=type.id)
            session.add(procs)
            session.commit()
        