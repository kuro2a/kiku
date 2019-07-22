#!/usr/bin/python3

from sqlalchemy import UniqueConstraint, Column, Integer, String, TIMESTAMP

from lib.database.DatabaseCore import Base
from datetime import datetime


class Server(Base):
    __tablename__ = 'ma_server'
    __table_args__ = (UniqueConstraint('ip', 'hostname'),{})

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    ip = Column(String(16), nullable=False)
    hostname = Column(String(20), nullable=False)
    rolename = Column(String(30))
    type_cd = Column(String(10))
    group_cd = Column(String(10))
    region = Column(String(20))
    zone = Column(String(20))
    description = Column(String(30))
    created_time = Column(TIMESTAMP, default=datetime.now, nullable=False)
    modified_time = Column(TIMESTAMP, default=datetime.now, nullable=False)

    def __repr__(self):
        return "<Server(ip='%s', hostname='%s', rolename='%s', type_cd='%s', group_cd='%s', description='%s', region='%s', zone='%s', created_time='%s', modified_time='%s')>" % (
            self.ip,
            self.hostname,
            self.rolename,
            self.type_cd,
            self.group_cd,
            self.region,
            self.zone,
            self.description,
            self.created_time,
            self.modified_time
        )
