# coding: utf-8

from __future__ import annotations
from typing import Union
from sqlalchemy.engine.row import Row

from . import Base
try:
    from flask_sqlalchemy.model import Model
except ImportError:
    Model = Base


def model_format(model: Union[Base, Model]) -> dict:
    """ 模型数据格式化 """
    return {c.name: getattr(model, c.name, None) for c in model.__table__.columns}


def row_format(result: Row) -> dict:
    """ 行数据格式化 """
    return dict(zip(result.keys(), result))


def list_format(result: list[Union[Row, Union[Base, Model]]]) -> list[dict]:
    """ 行数据列表格式化 """
    lst = []
    for items in result:
        if isinstance(items, Row):
            elem = row_format(items)
        elif isinstance(items, (Base, Model)):
            elem = model_format(items)
        lst.append(elem)
    return lst


def result_format(result: Union[Union[Base, Model], Row, list, None]) -> Union[dict, list[dict]]:
    """ sqlalchemy query result 格式化 """
    if not result:
        return result
    elif isinstance(result, list):
        return list_format(result)
    elif isinstance(result, Row):
        return row_format(result)
    return model_format(result)
