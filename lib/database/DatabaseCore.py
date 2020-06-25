#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from lib.const import ConfigKey
from lib.utility import SystemUtility

config = dict(SystemUtility.get_config())  # Avoid pylint error.

engine = create_engine(config[ConfigKey.CONF_KEY_SYSTEM][ConfigKey.CONF_KEY_SYSTEM_DATABASE][ConfigKey.CONF_KEY_SYSTEM_DATABASE_ENGINE],
                       pool_size=config[ConfigKey.CONF_KEY_SYSTEM][ConfigKey.CONF_KEY_SYSTEM_DATABASE][ConfigKey.CONF_KEY_SYSTEM_DATABASE_POOL_SIZE], max_overflow=0, encoding="utf-8", echo=True)

Base = declarative_base()
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
