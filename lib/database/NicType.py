#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, TIMESTAMP

from lib.database.DatabaseCore import Base
from datetime import datetime


class NicType(Base):
    __tablename__ = 'ma_nic_type'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    type_name = Column(String(15), nullable=False)
    link_speed = Column(Integer, nullable=False)
    created_time = Column(TIMESTAMP, default=datetime.now, nullable=False)
    modified_time = Column(TIMESTAMP, default=datetime.now, nullable=False)

    def __repr__(self):
        return "<NicType(type_name='%s', link_speed='%s', created_time='%s', modified_time='%s')>" % (
            self.type_name,
            self.link_speed,
            self.created_time,
            self.modified_time
        )
