import click
from start_tracking import start_tracking

@click.group()
def cli():
    pass

@cli.command()
def add_procs():
    click.echo('Добавить новый файл в список отслеживаемых')

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