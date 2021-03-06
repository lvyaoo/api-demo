import logging
from logging.handlers import RotatingFileHandler
from os import getenv

from flask import Flask

from .hooks import before_app_request, teardown_app_request
from .misc import CustomJSONEncoder
from .blueprints.admin_api import bp_admin_api
from .blueprints.admin_ext import bp_admin_ext


class _Config:
    """配置"""
    SERVER_NAME = getenv('SERVER_NAME')

    # blueprint
    BP_SUB_DOMAIN = {}
    BP_URL_PREFIX = {
        'admin_api': '/api',
        'admin_ext': '/ext'
    }

    @classmethod
    def init_app(cls, app: Flask) -> None:
        """初始化flask应用对象"""
        app.before_request(before_app_request)
        app.teardown_request(teardown_app_request)
        app.json_encoder = CustomJSONEncoder
        sub, url = cls.BP_SUB_DOMAIN, cls.BP_URL_PREFIX
        app.register_blueprint(bp_admin_api, subdomain=sub.get('admin'), url_prefix=url.get('admin_api'))
        app.register_blueprint(bp_admin_ext, subdomain=sub.get('admin'), url_prefix=url.get('admin_ext'))

        # 日志
        formatter = logging.Formatter('[%(asctime)s] %(pathname)s:%(lineno)d [%(levelname)s] %(message)s')
        debug_log = RotatingFileHandler('debug.log', maxBytes=1024 * 1024 * 100, backupCount=10, encoding='utf-8')
        debug_log.setLevel(logging.DEBUG)
        debug_log.setFormatter(formatter)
        error_log = RotatingFileHandler('error.log', maxBytes=1024 * 1024 * 100, backupCount=10, encoding='utf-8')
        error_log.setLevel(logging.ERROR)
        error_log.setFormatter(formatter)
        app.logger.setLevel(logging.DEBUG)
        app.logger.addHandler(debug_log)
        app.logger.addHandler(error_log)


class _DevelopmentConfig(_Config):
    """开发环境配置"""
    BP_URL_PREFIX = {
        'admin_api': '/api.admin',
        'admin_ext': '/ext.admin'
    }


class _TestingConfig(_Config):
    """测试环境配置"""
    BP_SUB_DOMAIN = {
        'admin': 'demo-admin'
    }


class _ProductionConfig(_Config):
    """生产环境配置"""
    BP_SUB_DOMAIN = {
        'admin': 'admin'
    }


config = {
    'development': _DevelopmentConfig,
    'testing': _TestingConfig,
    'production': _ProductionConfig,

    'default': _DevelopmentConfig
}
