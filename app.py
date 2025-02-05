import click
from start_tracking import start_tracking as start_tracking_foo
from add_app import add_app as add_app_foo
from delete_app import delete_app as delete_app_foo
from show_apps import show_apps as show_apps_foo

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
    apps = show_apps_foo()
    click.echo('Список отслеживаемых програм:')
    for k, v in enumerate(apps):
        print(f'{k}. {v.name}')
    

@cli.command()
def start_tracking():
    click.echo('Отслживаю работу процессов...')
    start_tracking_foo()

@cli.command()
def show_statistic():
    click.echo('Показать статистику')

if __name__ == '__main__':
    cli()