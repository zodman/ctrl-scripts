#!/bin/env python
import click
import dataset
import os
import dsnparse
from dotenv import load_dotenv
import datetime

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"), verbose=True)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    click.secho("DATABASE_URL env missing")
    exit(1)

parsed_url = dsnparse.parse(DATABASE_URL)
db = dataset.connect(DATABASE_URL)
table_name = "__ctrl_scripts_applied"
script_table = db[table_name]


@click.group()
def cli():
    click.secho(f":: 🎛️   Ctrl-S - control scripts applied ::")
    try:
        click.secho(
            f"Using {parsed_url.scheme}://{parsed_url.hostloc}/{parsed_url.paths[0]}?table={table_name}",
            fg="red",
        )
    except Exception as e:
        pass


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
def add(filename):
    filename = click.format_filename(filename)
    click.secho(f"adding {filename}", fg="green")
    now = datetime.datetime.now()
    script_table.insert_ignore(
        dict(script_name=filename, applied_at=now), ["script_name"]
    )


@cli.command()
@click.argument("path", type=click.Path())
@click.pass_context
def add_dir(ctx, path):
    for root, _, files in os.walk(path):
        for file in files:
            filename = os.path.join(root, file)
            ctx.invoke(add, filename=filename)


@cli.command()
@click.argument("path", type=click.Path())
def status(path):
    for root, _, files in os.walk(path):
        for file in files:
            filename = os.path.join(root, file)
            exists = script_table.find_one(script_name=filename)
            applied = exists is not None
            click.secho(f"{'*' if applied else  ' '} {file}", bold=applied)


if __name__ == "__main__":
    cli()
