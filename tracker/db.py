import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


# There is definitely probably a better way to do this, but given I'm doing this
# as a band-aid measure to avoid doing auth work + separate project creation, it'll
# have to do.
# Luckily, since I know I'm only doing this for 2 simple tables, I can skimp on
# both the constraints and the expandability.
# Could also probably come up with a better name.
# Maybe better in another location?
# TODO: Account for capitalization somewhere.
def get_id_or_create(table, col, val):
    ''' Insert the kv_pair into the table if it is not already present.
    Either way, return the ID of the element. '''
    
    db = get_db()
    
    # Check existense
    # '?' is not supported for things that aren't value params...but still need to be sanitized.
    # So basically, this =is not safe=
    # TODO: Make it safe
    id = db.execute(
        f"SELECT id FROM {table} WHERE {col} = ?",
        (val,)
    ).fetchone()

    # If it doesn't exist, make it, then grab the id
    # TODO: Make this safe, too
    if id is None:
        id = db.execute(
            f'INSERT INTO {table} ({col}) VALUES (?)',
            (val,)
        ).lastrowid
        # id = db.lastrowid
        db.commit()
    else:
        id = id[0] # Val is returned as a tuple

    # Return the ID
    return id
