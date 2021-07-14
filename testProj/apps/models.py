# coding: utf-8

import datetime
from enum import IntEnum, unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql.types import TINYINT, TEXT, LONGTEXT, DATETIME

from libs.uuid import make_uuid

db = SQLAlchemy()


class Xxx(db.Model):

    __tablename__ = 't_xxx'
    __table_args__ = {'comment': 'xxx表'}

    @unique
    class XxxTypeEnum(IntEnum):
        """ xxx类型枚举类 """

        TYPE_ONE = 1    # 类型1
        TYPE_TWO = 2    # 类型2
        TYPE_THREE = 3  # 类型3

    # 主键自增id，要求使用bigint且业务无关
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, comment='表id')
    # xxx_id使用uuid，固定32位长度，唯一键
    xxx_id = db.Column(db.CHAR(length=32), nullable=False, default=make_uuid, unique=True, comment='xxxid')
    # 类型字段建议使用tinyint，针对choices扩展出枚举类，方便管理
    xxx_type = db.Column(TINYINT, nullable=False, default=XxxTypeEnum.TYPE_ONE.value, comment='xxx类型: 1类型1, 2类型2 3类型3')
    # varchar类型统一定义成 not null default ''
    xxx_name = db.Column(db.VARCHAR(length=50), nullable=False, default='', comment='xxx名称')
    # varchar 区分大小写，指定collation，不要使用VARBINARY
    xxx_name_bin = db.Column(db.VARCHAR(length=50, collation='utf8mb4_bin'), nullable=False, default='', comment='xxx名称（区分大小写）')
    # 价格使用
    xxx_price = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False, default=0, comment='xxx价格')
    # 每个表必加的三个字段
    # 是否已删除，使用ORM布尔类型，对应mysql的tinyint
    is_deleted = db.Column(TINYINT, nullable=False, default=0, comment='是否已删除：0未删除 1已删除')
    # 模型创建时自动更新
    create_time = db.Column(DATETIME(fsp=6), nullable=False, default=datetime.datetime.now, comment='创建时间')
    # 模型修改时自动更新
    update_time = db.Column(DATETIME(fsp=6), nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')

    xxx_detail = db.relationship('XxxDetail', backref='xxx')
    yyy = db.relationship('Yyy', backref='xxx')

    """生成的表结构
    CREATE TABLE `t_xxx` (
      `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '表id',
      `xxx_id` char(32) NOT NULL COMMENT 'xxxid',
      `xxx_type` tinyint(4) NOT NULL COMMENT 'xxx类型: 1类型1, 2类型2 3类型3',
      `xxx_name` varchar(50) NOT NULL COMMENT 'xxx名称',
      `xxx_name_bin` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT 'xxx名称（区分大小写）',
      `xxx_price` decimal(10,2) NOT NULL COMMENT 'xxx价格',
      `is_deleted` tinyint(4) NOT NULL COMMENT '是否已删除：0未删除 1已删除',
      `create_time` datetime(6) NOT NULL COMMENT '创建时间',
      `update_time` datetime(6) NOT NULL COMMENT '更新时间',
      PRIMARY KEY (`id`),
      UNIQUE KEY `xxx_id` (`xxx_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='xxx表'
    """


class XxxDetail(db.Model):
    """xxx子表（详情表）

    有些情况，需要将大字段从源表中垂直拆分出来，形成一个子表，以减少查询I/O
    """

    __tablename__ = 't_xxx_detail'
    __table_args__ = {'comment': 'xxx详情表'}

    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, comment='表id')
    # 一对一外键
    xxx_id = db.Column(db.CHAR(length=32), db.ForeignKey('t_xxx.xxx_id'), unique=True, comment='xxxid')
    # 大字段类型，统一设置nullable=True
    content = db.Column(TEXT, nullable=True, comment='内容')
    long_content = db.Column(LONGTEXT, nullable=True, comment='长内容')
    name_list = db.Column(db.JSON, nullable=True, comment='名称列表')

    """生成的表结构
    CREATE TABLE `t_xxx_detail` (
      `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '表id',
      `xxx_id` char(32) DEFAULT NULL COMMENT 'xxxid',
      `content` text COMMENT '内容',
      `long_content` longtext COMMENT '长内容',
      `name_list` json DEFAULT NULL COMMENT '名称列表',
      PRIMARY KEY (`id`),
      UNIQUE KEY `xxx_id` (`xxx_id`),
      CONSTRAINT `t_xxx_detail_ibfk_1` FOREIGN KEY (`xxx_id`) REFERENCES `t_xxx` (`xxx_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='xxx详情表'
    """


class Yyy(db.Model):

    __tablename__ = 't_yyy'
    __table_args__ = {'comment': 'yyy表'}

    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, comment='表id')
    yyy_id = db.Column(db.CHAR(length=32), nullable=False, default=make_uuid, unique=True, comment='yyyid')
    xxx_id = db.Column(db.CHAR(length=32), db.ForeignKey('t_xxx.xxx_id'), comment='xxxid')
    is_deleted = db.Column(TINYINT, nullable=False, default=0, comment='是否已删除：0未删除 1已删除')
    create_time = db.Column(DATETIME(fsp=6), nullable=False, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(DATETIME(fsp=6), nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')

    """生成的表结构
    CREATE TABLE `t_yyy` (
      `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '表id',
      `yyy_id` char(32) NOT NULL COMMENT 'yyyid',
      `xxx_id` char(32) DEFAULT NULL COMMENT 'xxxid',
      `is_deleted` tinyint(4) NOT NULL COMMENT '是否已删除：0未删除 1已删除',
      `create_time` datetime(6) NOT NULL COMMENT '创建时间',
      `update_time` datetime(6) NOT NULL COMMENT '更新时间',
      PRIMARY KEY (`id`),
      UNIQUE KEY `yyy_id` (`yyy_id`),
      KEY `xxx_id` (`xxx_id`),
      CONSTRAINT `t_yyy_ibfk_1` FOREIGN KEY (`xxx_id`) REFERENCES `t_xxx` (`xxx_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='yyy表
    """