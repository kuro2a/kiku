#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, TIMESTAMP

from lib.database.DatabaseCore import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'ma_user'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    account = Column(String(10), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    username = Column(String(30), nullable=False)
    nickname = Column(String(30))
    role_id = Column(Integer, default=0, nullable=False)
    mail = Column(String(64))
    created_time = Column(TIMESTAMP, default=datetime.now, nullable=False)
    modified_time = Column(TIMESTAMP, default=datetime.now, nullable=False)

    def __repr__(self):
        return "<User(account='%s', password='%s', username='%s', nickname='%s', role_id='%s', mail='%s', created_time='%s', modified_time='%s')>" % (
            self.account,
            self.password,
            self.username,
            self.nickname,
            self.role_id,
            self.mail,
            self.created_time,
            self.modified_time
        )
