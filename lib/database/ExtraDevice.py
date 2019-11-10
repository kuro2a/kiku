#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, TIMESTAMP

from lib.database.DatabaseCore import Base
from datetime import datetime


class ExtraDevice(Base):
    __tablename__ = 'ma_extra_device'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    server_id = Column(Integer, nullable=False, index=True)
    device_name = Column(String(50))
    created_time = Column(TIMESTAMP, default=datetime.now, nullable=False)
    modified_time = Column(TIMESTAMP, default=datetime.now, nullable=False)

    def __repr__(self):
        return "<ExtraDevice(server_id='%s', device_name='%s', created_time='%s', modified_time='%s')>" % (
            self.server_id,
            self.device_name,
            self.created_time,
            self.modified_time
        )
