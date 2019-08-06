import asyncpg
from aiohttp import web

from .routes import setup_routes


async def create_app(config: dict) -> web.Application:
    app = web.Application()
    app['config'] = config

    setup_routes(app)

    app.on_startup.append(on_start)
    app.on_cleanup.append(on_shutdown)

    return app


async def on_start(app: web.Application) -> None:
    config = app['config']
    app['db'] = asyncpg.create_pool(config['database'])


async def on_shutdown(app: web.Application) -> None:
    await app['db'].close()
