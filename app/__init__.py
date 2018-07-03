from flask import Flask

from .config import config


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
    return app
