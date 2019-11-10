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
    created_time = Column(TIMESTAMP, default=datetime.now, nullable=False)
    modified_time = Column(TIMESTAMP, default=datetime.now, nullable=False)

    def __repr__(self):
        return "<Specification(server_id='%s', cpu_core='%s', memory='%s', swap='%s', system_storage='%s', created_time='%s', modified_time='%s')>" % (
            self.server_id,
            self.cpu_core,
            self.memory,
            self.swap,
            self.system_storage,
            self.created_time,
            self.modified_time
        )
