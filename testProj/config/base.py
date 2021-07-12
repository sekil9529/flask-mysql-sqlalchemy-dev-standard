# coding: utf-8

import os

__all__ = ('BaseConfig', 'BASE_DIR')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BaseConfig(object):
    """配置基类"""
    DEBUG = False

