# coding: utf-8

# from logging.config import dictConfig
from flask import Flask

from .models import db
from config.development import DevConfig


def init_db(app):
    db.init_app(app)
    return None


def create_app(env=None):
    """

    :param env: str: 环境
    :return: obj
    """
    # 获取配置
    config = DevConfig

    # dictConfig(config.LOGGING)

    app = Flask(__name__)

    # 配置
    app.config.from_object(config)

    # # 注册中间件
    # init_middleware(app)

    # 注册数据库
    init_db(app)

    # # 注册蓝图
    # init_blueprint(app)

    return app

