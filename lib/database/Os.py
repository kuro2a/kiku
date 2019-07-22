#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, TIMESTAMP

from lib.database.DatabaseCore import Base
from datetime import datetime


class Os(Base):
    __tablename__ = 'ma_os'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    os_type = Column(String(15), nullable=False)
    os_version = Column(String(50), nullable=False)
    created_time = Column(TIMESTAMP, default=datetime.now, nullable=False)
    modified_time = Column(TIMESTAMP, default=datetime.now, nullable=False)

    def __repr__(self):
        return "<Os(os_type='%s', os_version='%s', created_time='%s', modified_time='%s')>" % (
            self.os_type,
            self.os_version,
            self.created_time,
            self.modified_time
        )
