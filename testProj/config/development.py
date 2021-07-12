# coding: utf-8

import os

from .base import *
from libs.config import Config

CONFIG_INFO = Config(os.path.join(BASE_DIR, '.env')).format()
DB_CONFIG = CONFIG_INFO['db']


class DevConfig(BaseConfig):
    """开发环境配置"""

    DEBUG = True

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}" \
                              f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}" \
                              f"?charset={DB_CONFIG['charset']}"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10  # 10个连接
    SQLALCHEMY_MAX_OVERFLOW = 0  # 可以溢出的连接数
    SQLALCHEMY_POOL_RECYCLE = 60 * 60 * 2  # 2小时
    SQLALCHEMY_ENGINE_OPTIONS = {
        'isolation_level': 'READ COMMITTED'  # RC隔离级别
    }
