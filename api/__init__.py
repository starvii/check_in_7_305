import logging
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from api.utility.config import Config
from sanic import Sanic
from sanic_ext import Extend

APP_NAME = 'check_in'


def create_app() -> Sanic:
    app = Sanic(name=APP_NAME)
    app.ctx.config = Config()
    app.ctx.logger = logging.getLogger(APP_NAME)
    app.ctx.executor = ThreadPoolExecutor(os.cpu_count() * 5)

    from api.dao.data_access import DataAccess
    app.ctx.dao = DataAccess()
    app.ctx.dao.init()

    # 很遗憾，sanic的静态文件好像不支持默认文件名，比如'/' => '/index.html'
    app.static('/', app.ctx.config.STATIC, stream_large_files=True)
    app.static('/', str(Path(app.ctx.config.STATIC).joinpath('index.html')), stream_large_files=True)

    from api.router.v1 import checkin
    app.blueprint(checkin.bp)

    Extend(app)
    return app
