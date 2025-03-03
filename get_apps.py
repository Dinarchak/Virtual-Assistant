from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Process
from settings import config
from typing import List


def get_apps() -> List[Process]:
    engine = create_engine(config['db_url'])
    with Session(engine) as session:
        return list(session.scalars(select(Process)))
