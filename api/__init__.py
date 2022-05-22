import logging
import os
from concurrent.futures import ThreadPoolExecutor
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

    app.static('/', app.ctx.config.STATIC)
    from api.router.v1 import checkin
    app.blueprint(checkin.bp)

    Extend(app)
    return app
