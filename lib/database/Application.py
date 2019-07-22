#!/usr/bin/python3

from sqlalchemy import UniqueConstraint, Column, Integer, BigInteger, String, TIMESTAMP

from lib.database.DatabaseCore import Base
from datetime import datetime


class Application(Base):
    __tablename__ = 'ma_application'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    server_id = Column(Integer, nullable=False)
    application_name = Column(String(20), nullable=False)
    application_desc = Column(String(100), nullable=False)
    note = Column(String(100))
    created_time = Column(TIMESTAMP, default=datetime.now, nullable=False)
    modified_time = Column(TIMESTAMP, default=datetime.now, nullable=False)

    def __repr__(self):
        return "<Application(server_id='%s', application_name='%s', application_desc='%s', note='%s', created_time='%s', modified_time='%s')>" % (
            self.server_id,
            self.application_name,
            self.application_desc,
            self.note,
            self.created_time,
            self.modified_time
        )
