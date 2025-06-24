from aiohttp import web
from settings import config

app = web.Application()

if __name__ == '__main__':
    web.run_app(port=config['port'])