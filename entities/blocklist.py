import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from entities import db

class TokenBlockList(db.Model):
    __tablename__ = 'tokens_blocklist'

    jti = Column(String, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.now)

    @classmethod
    def is_blocked(cls, jti) -> 'TokenBlockList':
        return cls.query.filter_by(jti=jti).first() is not None

    def save(self) -> None:
        db.session.add(self)
