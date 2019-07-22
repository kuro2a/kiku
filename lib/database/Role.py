#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, TIMESTAMP

from lib.database.DatabaseCore import Base
from datetime import datetime


class Role(Base):
    __tablename__ = 'ma_role'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    role_type = Column(String(15), nullable=False)
    created_time = Column(TIMESTAMP, default=datetime.now, nullable=False)
    modified_time = Column(TIMESTAMP, default=datetime.now, nullable=False)

    def __repr__(self):
        return "<Os(role_type='%s', created_time='%s', modified_time='%s')>" % (
            self.role_type,
            self.created_time,
            self.modified_time
        )
