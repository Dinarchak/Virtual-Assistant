from sqlalchemy import create_engine, select
from db import Repository
from db.models import Process
from settings import config
from typing import List


def get_apps() -> List[Process]:
    engine = create_engine(config['db_url'])
    repo = Repository(engine)
    return repo.get_apps()
