#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, TIMESTAMP

from lib.database.DatabaseCore import Base
from datetime import datetime


class News(Base):
    __tablename__ = 'ma_news'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    news_title = Column(String(15), nullable=False)
    news_message = Column(String(80), nullable=False)
    created_time = Column(TIMESTAMP, default=datetime.now, nullable=False)
    modified_time = Column(TIMESTAMP, default=datetime.now, nullable=False)

    def __repr__(self):
        return "<News(news_title='%s', news_message='%s', created_time='%s', modified_time='%s')>" % (
            self.news_title,
            self.news_message,
            self.created_time,
            self.modified_time
        )
