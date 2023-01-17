#!/bin/env python
import click
import dataset
import os
import dsnparse
from dotenv import load_dotenv
import datetime

load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'), verbose=True)

DATABASE_URL = os.getenv('DATABASE_URL')
parsed_url = dsnparse.parse(DATABASE_URL)
db = dataset.connect(DATABASE_URL)

script_table = db['__ctrl_scripts_applied']


@click.group()
def cli():
    click.secho(f'using {parsed_url.scheme}://{parsed_url.hostloc}', fg='red')


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
def add(filename):
    filename = click.format_filename(filename)
    click.secho(f'adding {filename}', fg='green')
    now = datetime.datetime.now()
    script_table.insert_ignore(dict(script_name=filename, applied_at=now), ['script_name'])

@cli.command()
@click.argument('path', type=click.Path())
@click.pass_context
def add_dir(ctx, path):
    for root, dir, files in os.walk(path):
        for file in files:
            filename = os.path.join(root,file)
            ctx.invoke(add, filename=filename)

if __name__ == "__main__":
    cli()

