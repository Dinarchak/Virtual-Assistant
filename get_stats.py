import matplotlib.pyplot as plt
from models import LifePeriod, Process
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from settings import config
from sqlalchemy import func

from  datetime import date, timedelta

def get_stats():
    day = timedelta(days=1)
    engine = create_engine(config['db_url'])
    start_time = date.today()

    processes = []
    data = []

    with Session(engine) as session:
        query = (session.query(Process.name, func.sum(LifePeriod.delta))
                  .where(LifePeriod.start >= start_time, LifePeriod.end <= start_time + day)
                  .join(Process)
                  .group_by(LifePeriod.process_id).all())
        for i in query:
            processes.append(i[0])
            data.append(i[1] // 60)

        fix, ax = plt.subplots()


        ax.bar(processes, data, align='center', )
        plt.show()

get_stats()