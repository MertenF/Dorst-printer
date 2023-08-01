import sqlite3
import logging
from dataclasses import asdict

import click
import flask.app
from flask import current_app, g

from dorstorder.order import Order

DBFILE = 'dorst.db'


def get_db() -> sqlite3.Connection:
    if 'db' not in g:
        g.db = sqlite3.connect(
            # current_app.config['DATABASE'],
            DBFILE,
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None) -> None:
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command() -> None:
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app: flask.app.Flask) -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def insert_order(self, order: Order) -> None:
    params = asdict(order)
    params['customer_firstname'] = params['customer']['first']
    params['customer_lastname'] = params['customer']['last']
    params['customer_email'] = params['customer']['email']

    with self.conn:
        self.conn.execute(
            """INSERT INTO orders VALUES (
                :table_name,
                :payment_status,
                :order_num,
                :payment_method,
                :customer,
                :prepare_location,
                :total_price_cents,
                :total_items_amount,
                :order_datetime
            );""",
            params
        )


def main():
    insert_order()


if __name__ == '__main__':
    main()
