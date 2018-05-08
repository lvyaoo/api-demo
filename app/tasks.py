from os import getenv

from celery.signals import task_postrun, task_prerun
from flask import current_app

from . import create_app, create_celery
from .models import db


if current_app:
    celery = create_celery(current_app)
else:
    _app = create_app(getenv('FLASK_CONFIG'))
    celery = create_celery(_app)


@task_prerun.connect
def celery_prerun(*args, **kwargs) -> None:
    """celery任务执行前钩子函数"""
    db.connect(reuse_if_open=True)


@task_postrun.connect
def celery_postrun(*args, **kwargs) -> None:
    """celery任务执行后钩子函数"""
    db.close()
