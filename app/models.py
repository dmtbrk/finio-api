from __future__ import annotations
import hashlib

from asyncpgsa.connection import SAConnection

from . import db


class User:
    def __init__(self, id, username, password_hash, email=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email

    @classmethod
    async def create(cls, connection: SAConnection, username: str, password: str, email: str = None) -> User:
        password_hash = hashlib.sha256(password.encode(encoding='utf-8')).hexdigest()
        result = await connection.fetchrow(db.users.insert()
                                           .values(username=username,
                                                   password_hash=password_hash,
                                                   email=email)
                                           .returning(db.users.c.id,
                                                      db.users.c.username,
                                                      db.users.c.password_hash,
                                                      db.users.c.email))

        return cls(id=result.get('id'),
                   username=result.get('username'),
                   password_hash=result.get('password_hash'),
                   email=result.get('email'))

    @classmethod
    async def get_by_username(cls, connection: SAConnection, username: str = None) -> User:
        result = await connection.fetchrow(db.users.select().where(db.users.c.username == username))

        return cls(id=result.get('id'),
                   username=result.get('username'),
                   password_hash=result.get('password_hash'),
                   email=result.get('email'))
