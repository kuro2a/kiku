#!/usr/bin/python3

from datetime import datetime

from lib.utility import SystemUtility
from lib.session import BaseSessionService
from lib.const import SessionKey


class LocalSessionService(BaseSessionService):
    def __init__(self, config):
        super(LocalSessionService, self).__init__(config)
        self.session_database = {}

    def get_session(self, session_id):
        try:
            session = self.session_database[session_id]
        except KeyError:
            session = None
        return session

    def set_session(self, session_id, data):
        self.session_database[session_id] = data
        self.logger.debug("session data >>> {0}, {1}".format(session_id, data))

    def touch_session(self, session_id, data):
        try:
            session = self.session_database[session_id]
            session[SessionKey.SESSION_KEY_TIMESTAMP] = datetime.now()
            return session[SessionKey.SESSION_KEY_TIMESTAMP]
        except KeyError:
            return False

    def remove_session(self, session_id):
        try:
            del self.session_database[session_id]
            return True
        except KeyError:
            return False

