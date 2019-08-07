from aiohttp import web

from .handlers import login


def setup_routes(app: web.Application) -> None:
    app.add_routes([
        web.post('/login', login)
    ])
