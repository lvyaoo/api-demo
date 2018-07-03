from __future__ import annotations
from datetime import datetime
from os import getenv
from time import time
from typing import Iterable, Optional, Type, TypeVar, Union
from uuid import uuid4

from flask import current_app
from peewee import *
from werkzeug.security import check_password_hash, generate_password_hash

from .api_utils import APIError
from utils.aes_util import aes_crypto


db = MySQLDatabase(
    getenv('MYSQL_DB'),
    user=getenv('MYSQL_USER'),
    password=getenv('MYSQL_PASSWORD'),
    host=getenv('MYSQL_HOST') or '127.0.0.1',
    port=int(getenv('MYSQL_PORT') or 3306),
    charset='utf8mb4'
)
T = TypeVar('T', bound='_BaseModel')


class _ObjectField(Field):
    """python对象字段"""
    field_type = 'TEXT'

    def db_value(self, value):
        return None if value is None else repr(value)

    def python_value(self, value):
        return None if value is None else eval(value)


class _BaseModel(Model):
    """表基类"""
    id = AutoField()  # 主键
    uuid = UUIDField(unique=True, default=uuid4)  # UUID
    create_time = DateTimeField(default=datetime.now)  # 创建时间
    update_time = DateTimeField(default=datetime.now)  # 更新时间

    class Meta:
        database = db
        only_save_dirty = True

    @classmethod
    def _excluded_field_names(cls) -> set:
        """转换为dict时排除在外的字段名"""
        return set()

    @classmethod
    def _extra_attr_names(cls) -> set:
        """转换为dict时额外增加的属性名"""
        return set()

    @classmethod
    def get_by_id(cls: Type[T], _id: Union[int, str], code: int=0, message: str=None) -> Optional[T]:
        """根据主键获取

        Args:
            _id: 主键
            code: APIError错误码
            message: APIError错误描述
        """
        try:
            return cls.select().where(cls.id == _id).get()
        except cls.DoesNotExist:
            if code:
                raise APIError(code, message)

    @classmethod
    def get_by_uuid(cls: Type[T], _uuid: str, code: int=0, message: str=None) -> Optional[T]:
        """根据UUID获取

        Args:
            _uuid: UUID
            code: APIError错误码
            message: APIError错误描述
        """
        try:
            return cls.select().where(cls.uuid == _uuid).get()
        except cls.DoesNotExist:
            if code:
                raise APIError(code, message)

    def to_dict(self, *, only: Iterable[str]=None, exclude: Iterable[str]=None, recurse: bool=False,
                max_depth: int=None) -> dict:
        """转换为dict

        Args:
            only: 仅包含在内的字段名列表
            exclude: 排除在外的字段名列表
            recurse: 是否对外键进行递归转换
            max_depth: 递归深度，默认无限制
        """
        only = set(only or [])
        exclude = set(exclude or []) | self._excluded_field_names()
        if max_depth is None:
            max_depth = -1
        if max_depth == 0:
            recurse = False
        data = {}

        # fields
        for field_name, field in self._meta.fields.items():
            if field_name in exclude or (only and field_name not in only):
                continue
            field_data = self.__data__.get(field_name)
            if recurse and isinstance(field, ForeignKeyField):
                if field_data:
                    rel_obj = getattr(self, field_name)
                    field_data = rel_obj.to_dict(recurse=True, max_depth=max_depth - 1)
                else:
                    field_data = None
            data[field_name] = field_data

        # extra
        for attr_name in self._extra_attr_names():
            if attr_name in exclude or (only and attr_name not in only):
                continue
            attr = getattr(self, attr_name)
            data[attr_name] = attr() if callable(attr) else attr
        return data

    def save_ut(self) -> int:
        """记录更新时间并持久化到数据库"""
        self.update_time = datetime.now()
        return self.save()

    def save_if_changed(self, update_ut: bool=True) -> Optional[int]:
        """若有数值变动则持久化到数据库

        Args:
            update_ut: 是否记录更新时间
        """
        db_obj = self.get_by_id(self.id)
        for f in self._dirty:
            if self.__data__.get(f) != db_obj.__data__.get(f):
                if update_ut:
                    return self.save_ut()
                else:
                    return self.save()


class Admin(_BaseModel):
    """管理员"""
    TOKEN_EXPIRES = 7  # 身份令牌的过期时间（天）
    MIN_PW_LEN = 6  # 最小密码长度
    MAX_PW_LEN = 16  # 最大密码长度

    username = CharField(max_length=32, unique=True)  # 用户名
    password = CharField()  # 密码
    last_login_time = DateTimeField(null=True)  # 最近登录时间
    last_login_ip = CharField(null=True)  # 最近登录IP
    auth = BitField(default=0)  # 权限

    class Meta:
        table_name = 'admin'

    @classmethod
    def _excluded_field_names(cls):
        return {'password'}

    @classmethod
    def new(cls, username: str, password: str) -> Admin:
        """创建管理员"""
        return cls.create(
            username=username.strip(),
            password=generate_password_hash(password)
        )

    @classmethod
    def get_by_username(cls, username: str) -> Optional[Admin]:
        """根据用户名获取"""
        try:
            return cls.select().where(cls.username == username).get()
        except cls.DoesNotExist:
            pass

    @classmethod
    def get_by_token(cls, token: str) -> Optional[Admin]:
        """根据身份令牌获取"""
        try:
            text = aes_crypto.decrypt(token)
            _uuid, expires = text.split(':')
            expires = int(expires)
        except Exception as e:
            current_app.logger.error(e)
        else:
            if expires > time():
                return cls.get_by_uuid(_uuid)

    def gen_token(self) -> str:
        """生成身份令牌"""
        text = '{0}:{1}'.format(self.uuid, int(time()) + 86400 * self.TOKEN_EXPIRES)
        return aes_crypto.encrypt(text)

    def check_password(self, password: str) -> bool:
        """核对密码"""
        return check_password_hash(self.password, password)

    def set_password(self, password: str) -> int:
        """设置密码"""
        self.password = generate_password_hash(password)
        return self.save_ut()

    def login(self, ip: str) -> int:
        """登录"""
        self.last_login_time = datetime.now()
        self.last_login_ip = ip
        return self.save()


models = [Admin]
