import click
from start_tracking import start_tracking as start_tracking_foo
from add_app import add_app as add_app_foo

@click.group()
def cli():
    pass

@cli.command()
@click.option('-t', '--type', help='Категория программы', required=True)
@click.option('-n', '--name', help='Имя программы', required=True)
def add_app(type, name):
    add_app_foo(name, type)

@cli.command()
def delete_procs():
    click.echo('Удалить файлы из списка')

@cli.command()
def start_tracking():
    click.echo('Отслживаю работу процессов...')
    start_tracking()

@cli.command()
def show_statistic():
    click.echo('Показать статистику')

if __name__ == '__main__':
    cli()