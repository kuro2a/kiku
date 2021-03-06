#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, TIMESTAMP

from lib.database.DatabaseCore import Base
from datetime import datetime


class Storage(Base):
    __tablename__ = 'ma_storage'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    server_id = Column(Integer, nullable=False, index=True)
    device_name = Column(String(50))
    device_type = Column(String(15))
    size = Column(Integer)
    mount_path = Column(String(30))
    created_time = Column(TIMESTAMP, default=datetime.now, nullable=False)
    modified_time = Column(TIMESTAMP, default=datetime.now, nullable=False)

    def __repr__(self):
        return "<Storage(server_id='%s', device_name='%s', device_type='%s', size='%s', mount_path='%s', created_time='%s', modified_time='%s')>" % (
            self.server_id,
            self.device_name,
            self.device_type,
            self.size,
            self.mount_path,
            self.created_time,
            self.modified_time
        )
