import asyncpgsa
from aiohttp import web
from sqlalchemy import (Table, MetaData, Column, Integer, String, ForeignKey)

metadata = MetaData()

users = Table(
    'users', metadata,

    Column('id', Integer, primary_key=True),
    Column('username', String(64), nullable=False, unique=True),
    Column('email', String(120)),
    Column('password_hash', String(128), nullable=False)
)


def make_dsn(host, port, database, user, password):
    return f'postgresql://{user}:{password}@{host}:{port}/{database}'


async def setup_db(app: web.Application) -> None:
    config = app['config']
    app['db'] = await asyncpgsa.create_pool(**config['database'])


async def teardown_db(app: web.Application) -> None:
    await app['db'].close()
