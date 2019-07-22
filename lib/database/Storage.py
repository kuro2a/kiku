#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, TIMESTAMP

from lib.database.DatabaseCore import Base
from datetime import datetime


class Storage(Base):
    __tablename__ = 'ma_storage'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    server_id = Column(Integer, nullable=False, index=True)
    device_type = Column(String(30))
    device_id = Column(String(64))
    partition_no = Column(Integer)
    size = Column(Integer)
    mount_path = Column(String(30))
    created_time = Column(TIMESTAMP, default=datetime.now, nullable=False)
    modified_time = Column(TIMESTAMP, default=datetime.now, nullable=False)

    def __repr__(self):
        return "<Storage(server_id='%s', device_type='%s', device_id='%s', partition_no='%s', size='%s', mount_path='%s', created_time='%s', modified_time='%s')>" % (
            self.server_id,
            self.device_type,
            self.device_id,
            self.partition_no,
            self.size,
            self.mount_path,
            self.created_time,
            self.modified_time
        )
