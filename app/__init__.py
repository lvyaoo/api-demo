from flask import Flask

from .config import config
from .models import db, models
from .socketio import DefaultNamespace, socketio


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
    socketio.init_app(app)
    socketio.on_namespace(DefaultNamespace(app.config['DEFAULT_NS']))
    return app
