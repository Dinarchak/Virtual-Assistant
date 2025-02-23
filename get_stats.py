import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from models import LifePeriod, Process
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from settings import config
from sqlalchemy import func

from  datetime import timedelta, datetime

def get_stats(start_time=None, end_time=None, delta='1d', chart_type=0):

    delta_resolution = {
        'h': 1,
        'd': 24,
        'w': 168
    }

    charts = {
        0: hourly_bar,
        1: hourly_scale
    }

    if start_time is None:
        a = datetime.now()
        start_time = datetime(a.year, a.month, a.day, 0, 0, 0, 0)
    else:
        start_time = datetime.strptime(start_time, config['datetime_str_format'])
    
    if end_time is None:
        delta = timedelta(hours=(int(delta[:-1]) * delta_resolution[delta[-1]]))
        end_time = start_time + delta
    else:
        end_time = datetime.strptime(end_time, config['datetime_str_format'])

    engine = create_engine(config['db_url'])

    charts[chart_type](engine, start_time, end_time)

def hourly_bar(engine, start_time, end_time):

    with Session(engine) as session:
        query = (session.query(Process.name, func.sum(LifePeriod.delta))
                  .where(LifePeriod.start >= start_time, LifePeriod.end <= end_time)
                  .join(Process)
                  .group_by(LifePeriod.process_id).all())

    processes = []
    data = []
    
    for i in query:
        processes.append(i[0])
        data.append(i[1] // 60)

    fig, ax = plt.subplots()

    ax.yaxis.set_major_locator(MultipleLocator(base=30))
    ax.yaxis.set_minor_locator(MultipleLocator(base=5))

    ax.yaxis.set_major_formatter(lambda x, pos: (start_time + timedelta(minutes=x)).strftime('%H:%M'))
    ax.bar(processes, data, align='center')
    plt.show()

def hourly_scale(engine, start_time, end_time):

    with Session(engine) as session:
        query = (session.query(Process.name, LifePeriod.start, LifePeriod.end)
                 .where(LifePeriod.start >= start_time, LifePeriod.end <= end_time)
                 .join(Process))

        ranges = {}
    
        for i in query:
            if i[0] not in ranges:
                ranges[i[0]] = [((i[1] - start_time).total_seconds() // 60, (i[2] - i[1]).total_seconds() // 60)]
            else:
                ranges[i[0]].append(((i[1] - start_time).total_seconds() // 60, (i[2] - i[1]).total_seconds() // 60))


        fig, ax = plt.subplots()

        for i, k in enumerate(ranges.keys()):
            ax.broken_barh(ranges[k], (i + .8, .4))

        ax.set_yticks([1 + i for i in range(len(ranges.keys()))], list(ranges.keys()))

        ax.set_xlim(0, (end_time - start_time).total_seconds() // 60)
        ax.xaxis.set_major_locator(MultipleLocator(base=60))
        ax.xaxis.set_minor_locator(MultipleLocator(base=15))
        ax.xaxis.set_major_formatter(lambda x, pos: (start_time + timedelta(minutes=x)).strftime('%H:%M'))
        plt.xticks(rotation=45)

        plt.show()
