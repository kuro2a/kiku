#!/usr/bin/python3

from sqlalchemy import UniqueConstraint, Column, Integer, BigInteger, String, TIMESTAMP

from lib.database.DatabaseCore import Base
from datetime import datetime


class Specification(Base):
    __tablename__ = 'ma_specification'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    server_id = Column(Integer, nullable=False, unique=True)
    os_id = Column(Integer, nullable=False)
    cpu_core = Column(Integer, nullable=False)
    memory = Column(BigInteger, nullable=False)
    swap = Column(BigInteger, nullable=False)
    system_storage = Column(BigInteger, nullable=False)
    data_storage_1 = Column(BigInteger)
    data_storage_2 = Column(BigInteger)
    data_storage_3 = Column(BigInteger)
    data_storage_4 = Column(BigInteger)
    nic_type_1 = Column(Integer)
    nic_type_2 = Column(Integer)
    nic_type_3 = Column(Integer)
    nic_type_4 = Column(Integer)
    ext_device_1 = Column(String(50))
    ext_device_2 = Column(String(50))
    ext_device_3 = Column(String(50))
    ext_device_4 = Column(String(50))
    created_time = Column(TIMESTAMP, default=datetime.now, nullable=False)
    modified_time = Column(TIMESTAMP, default=datetime.now, nullable=False)

    def __repr__(self):
        return "<Specification(server_id='%s', cpu_core='%s', memory='%s', swap='%s', system_storage='%s', data_storage_1='%s', data_storage_2='%s', data_storage_3='%s', data_storage_4='%s', nic_type_1='%s', nic_type_2='%s', nic_type_3='%s', nic_type_4='%s', ext_device_1='%s', ext_device_2='%s', ext_device_3='%s', ext_device_4='%s', created_time='%s', modified_time='%s')>" % (
            self.server_id,
            self.cpu_core,
            self.memory,
            self.swap,
            self.system_storage,
            self.data_storage_1,
            self.data_storage_2,
            self.data_storage_3,
            self.data_storage_4,
            self.nic_type_1,
            self.nic_type_2,
            self.nic_type_3,
            self.nic_type_4,
            self.ext_device_1,
            self.ext_device_2,
            self.ext_device_3,
            self.ext_device_4,
            self.created_time,
            self.modified_time
        )
