#!/usr/bin/python3

import traceback
from datetime import datetime
from urllib.parse import urlparse

import redis

from lib.const import Const, ConfigKey, SessionKey
from lib.session import BaseSessionService


class RedisSessionService(BaseSessionService):
    def __init__(self, config):
        super(RedisSessionService, self).__init__(config)
        self.engine = urlparse(
            config[ConfigKey.CONF_KEY_SYSTEM_SESSION_ENGINE])
        self.pool = redis.ConnectionPool(host=self.engine.hostname, port=int(self.engine.port),
                                         db=int(self.engine.path.split('/')[1]), max_connections=Const.SESSION_POOL_SIZE,
                                         decode_responses=True)
        self.timeout = int(config[ConfigKey.CONF_KEY_SYSTEM_SESSION_TIMEOUT])

    def get_session(self, session_id):
        try:
            conn = redis.StrictRedis(connection_pool=self.pool)
            session = conn.hgetall(session_id)
            if session == {}:
                session = None
            session[SessionKey.SESSION_KEY_TIMESTAMP] = datetime.strptime(session[SessionKey.SESSION_KEY_TIMESTAMP], '%Y-%m-%d %H:%M:%S.%f')
        except Exception:
            session = None
            self.logger.error(traceback.format_exc())
        return session

    def set_session(self, session_id, data):
        try:
            conn = redis.StrictRedis(connection_pool=self.pool)
            self.logger.debug(data)
            for key in data.keys():
                conn.hset(session_id, key, str(data[key]))
            conn.expire(session_id, self.timeout)
            self.logger.debug(
                "session data >>> {0}, {1}".format(session_id, data))
        except Exception:
            self.logger.error(traceback.format_exc())

    def touch_session(self, session_id, data):
        try:
            conn = redis.StrictRedis(connection_pool=self.pool)
            conn.hset(session_id, SessionKey.SESSION_KEY_TIMESTAMP, datetime.now())
            conn.expire(session_id, self.timeout)
        except Exception:
            self.logger.error(traceback.format_exc())

    def remove_session(self, session_id):
        try:
            conn = redis.StrictRedis(connection_pool=self.pool)
            conn.delete(session_id)
        except Exception:
            self.logger.error(traceback.format_exc())
