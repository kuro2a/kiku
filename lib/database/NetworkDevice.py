#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, TIMESTAMP

from lib.database.DatabaseCore import Base
from datetime import datetime


class NetworkDevice(Base):
    __tablename__ = 'ma_network_device'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    server_id = Column(Integer, nullable=False, index=True)
    nic_type = Column(Integer, nullable=False)
    device_name = Column(String(50))
    created_time = Column(TIMESTAMP, default=datetime.now, nullable=False)
    modified_time = Column(TIMESTAMP, default=datetime.now, nullable=False)

    def __repr__(self):
        return "<NetworkDevice(server_id='%s', nic_type='%s',device_name='%s', created_time='%s', modified_time='%s')>" % (
            self.server_id,
            self.nic_type,
            self.device_name,
            self.created_time,
            self.modified_time
        )
