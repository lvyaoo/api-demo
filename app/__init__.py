from celery import Celery
from flask import Flask

from .config import config
from .models import db, models


def create_app(env: str=None) -> Flask:
    """创建flask应用对象

    Args:
        env: 运行环境：development/testing/production
    """
    if not env:
        env = 'default'
    app = Flask(__name__)
    app.config.from_object(config[env])
    config[env].init_app(app)
    db.init(**app.config['DATABASE'])
    db.create_tables(models)
    return app


def create_celery(app: Flask) -> Celery:
    """创建celery应用对象"""
    celery = Celery(app.import_name)
    celery.conf.update(app.config)

    class AppContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = AppContextTask
    return celery
