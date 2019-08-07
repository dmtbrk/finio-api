import hashlib

from aiohttp import web

from .models import User


async def login(request: web.Request) -> web.Response:
    if request.method == 'POST':
        data = await request.json()
        username = data.get('username')
        password = data.get('password')
        if username and password:
            async with request.app['db'].acquire() as connection:
                user = await User.get_by_username(connection, username)
                if user.password_hash == hashlib.sha256(password.encode('utf-8')).hexdigest():
                    return web.json_response({'token': 'fuck yeah'})
                else:
                    raise web.HTTPUnauthorized
        else:
            raise web.HTTPBadRequest
