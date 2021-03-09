import base64
import datetime
from uuid import uuid4
from typing import List
from sqlalchemy import Column, String, Date, DateTime, Enum
from werkzeug.exceptions import BadRequest, Unauthorized
from decorators.type import GUID
from plugins.sqlalchemy import db
from entities.types import RoleType



class User(db.Model):
    __tablename__ = 'users'

    uuid = Column(GUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    position = Column(String)
    role = Column(Enum(RoleType), default=RoleType.USER)
    birth = Column(Date, nullable=True)
    username = Column(String, unique=True, nullable=True)
    _password = Column('password', String, nullable=True)
    last_update = Column(DateTime, default=datetime.datetime.now)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value) -> None:
        self._password = base64.b64encode(value.encode('utf-8'))
    
    def check_password(self, password: str) -> bool:
        encoded_password = base64.b64encode(password.encode('utf-8'))
        if self._password == encoded_password:
            return True
        raise Unauthorized('Password verification failed.')

    @classmethod
    def get_by_uuid(cls, uuid: str) -> 'User':
        return cls.query.filter_by(uuid = uuid).first()
    
    @classmethod
    def get_by_username(cls, username: str) -> 'User':
        user = cls.query.filter_by(username = username).first()
        if user:
            return user
        raise BadRequest(f"User with username \'{username}\' not found.")

    @classmethod
    def list_by_role(cls, role: str) -> List['User']:
        return cls.query.filter_by(role = role).all()
