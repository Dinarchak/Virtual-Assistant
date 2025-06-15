from sqlalchemy import create_engine
from settings import config
from datetime import timedelta, datetime
from db.charts import Chart


def get_stats(start_time=None, end_time=None, delta='1d', chart_type=0):

    delta_resolution = {
        'h': 1,
        'd': 24,
        'w': 168
    }

    charts = {
        2: Chart.week_stat,
        3: Chart.daily_stat
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
