#!/usr/bin/python3

from lib.const import Const, ConfigKey, Message
from lib.session import LocalSessionService


class SessionUtility(object):
    config = None
    session_service = None

    @classmethod
    def get_session_service(self, config=None):
        if SessionUtility.session_service is None:
            if config is None:
                raise Exception(Message.EXCEPTION_UNKNOWN_OPTION)
            session_config = config[ConfigKey.CONF_KEY_SYSTEM_SESSION]
            session_type = session_config[ConfigKey.CONF_KEY_SYSTEM_SESSION_TYPE]
            if session_type == Const.SESSION_TYPE_LOCAL:
                session_service = LocalSessionService(session_config)
            elif session_type == Const.SESSION_TYPE_REDIS:
                # TODO: Write Redis external session mode.
                pass
            elif session_type == Const.SESSION_TYPE_MEMCACHED:
                # TODO: Write Memcached external session mode.
                pass
            else:
                raise Exception(Message.EXCEPTION_UNKNOWN_TYPE)
            SessionUtility.session_service = session_service
        return SessionUtility.session_service
