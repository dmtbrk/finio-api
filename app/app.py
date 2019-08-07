from aiohttp import web

from .db import setup_db, teardown_db
from .routes import setup_routes


async def create_app(config: dict) -> web.Application:
    app = web.Application()
    app['config'] = config

    setup_routes(app)

    app.on_startup.append(setup_db)
    app.on_cleanup.append(teardown_db)

    return app
