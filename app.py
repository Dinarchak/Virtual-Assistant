from commands.start_tracking import start_tracking as start_tracking_foo
from commands.get_stats import get_stats as get_stats_foo
from commands.get_apps import get_apps as get_apps_foo
from commands.add_app import add_app as add_app_foo
from commands.delete_app import delete_app as delete_app_foo
from datetime import datetime, timedelta
from settings import config
import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('-t', '--type', help='Категория программы', required=True)
@click.option('-n', '--name', help='Имя программы', required=True)
def add_app(type, name):
    add_app_foo(name, type)
    click.echo(f"Программа '{name}' добавлена в список отслеживаемых")

@cli.command()
@click.argument('name', nargs=-1, required=True)
def delete_app(name):
    delete_app_foo(name)

@cli.command()
def show_apps():
    apps = get_apps_foo()
    click.echo('Список отслеживаемых програм:')
    for k, v in enumerate(apps):
        click.echo(f'{k}. {v.name}')

@cli.command()
def start_tracking():
    click.echo('Отслживаю работу процессов...')
    start_tracking_foo()

@cli.command()
@click.option('--start-time', help='Начало отсчета', default=None)
@click.option('--end-time', help='конец отсчета', default=None)
@click.option('--delta', help='Промежуток отсчета', default='1d')
@click.option('--chart-type', help='Тип диаграммы', type=click.INT, default=0)
def show_statistic(start_time, end_time, delta, chart_type):
    get_stats_foo(start_time, end_time, delta, chart_type)

@cli.command()
def week_statistic():
    start = datetime.now()
    start -= timedelta(hours=start.hour, minutes=start.minute, seconds=start.second)
    start -= timedelta(days=start.weekday())
    get_stats_foo(start_time=datetime.strftime(start, config['datetime_str_format']), delta='7d', chart_type=2)

@cli.command()
def day_statistic():
    start = datetime.now()
    start -= timedelta(hours=start.hour, minutes=start.minute, seconds=start.second)
    get_stats_foo(start_time=datetime.strftime(start, config['datetime_str_format']), delta='1d', chart_type=3)


if __name__ == '__main__':
    cli()
