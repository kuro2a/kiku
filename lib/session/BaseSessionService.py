#!/usr/bin/python3


from lib.const import SessionKey
import lib.utility.SystemUtility


class BaseSessionService(object):
    def __init__(self, config):
        self.logger = lib.utility.SystemUtility.get_system_log()
        self.config = config

    def get_config(self):
        return self.config

    def createUserSession(self, account, role, username, nickname, timestamp):
        return {
            SessionKey.SESSION_KEY_ACCOUNT: account,
            SessionKey.SESSION_KEY_ROLE: role,
            SessionKey.SESSION_KEY_USERNAME: username,
            SessionKey.SESSION_KEY_NICKNAME: nickname,
            SessionKey.SESSION_KEY_TIMESTAMP: timestamp
        }
