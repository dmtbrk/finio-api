import argparse
import asyncio

import uvloop
import yaml
from aiohttp import web

from app import create_app

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def load_config(path: str) -> dict:
    with open(path) as f:
        config = yaml.safe_load(f)
        return config


def run(config: dict, host: str = '0.0.0.0', port: int = 8080):
    app = create_app(config=config)
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Finio API application.')
    arg_parser.add_argument('--host', help="Host to listen.", default='0.0.0.0')
    arg_parser.add_argument('--port', help="Port to listen.", default=8080)
    arg_parser.add_argument('-c', '--config', help="Path to configuration file.")
    args = arg_parser.parse_args()

    run(config=load_config(args.config), host=args.host, port=args.port)
