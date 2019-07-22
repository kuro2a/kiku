#!/usr/bin/python3

import uuid
import falcon
import re
from datetime import datetime, timedelta

from lib.const import ConfigKey, SessionKey
from lib.middleware import BaseMiddleware
from lib.utility import SystemUtility, SessionUtility


class CommonMiddleware(BaseMiddleware):
    def process_resource(self, req, resp, resource, params):
        super(CommonMiddleware, self).process_resource(
            req, resp, resource, params)
        # Avoid pylint error.
        system_config = dict(self.config)[ConfigKey.CONF_KEY_SYSTEM]
        # API Check.
        if re.match('/api/', req.path) != None:
            return
        # Login check.
        try:
            session_id = req.get_cookie_values('session_id')[0]
            self.logger.debug("Session ID:{0}".format(session_id))
        except:
            cookie_max_age = system_config[ConfigKey.CONF_KEY_SYSTEM_COOKIE][ConfigKey.CONF_KEY_SYSTEM_COOKIE_MAX_AGE]
            session_id = str(uuid.uuid4())
            resp.set_cookie('session_id', session_id,
                            max_age=cookie_max_age, path='/', secure=False)
            resp.status = falcon.HTTP_200
            self.logger.debug(
                "Set cookie, Session ID:{0}".format(session_id))
            raise falcon.HTTPMovedPermanently('/login')
        try:
            session_service = SessionUtility.get_session_service()
            session_config = session_service.get_config()
            session = session_service.get_session(session_id)
            diff = (datetime.now() -
                    session[SessionKey.SESSION_KEY_TIMESTAMP]).seconds
            if session_config[ConfigKey.CONF_KEY_SYSTEM_SESSION_TIMEOUT] - diff < 0:
                self.logger.debug("session timeout: {0}".format(session_id))
                session_service.remove_session(session_id)
                raise falcon.HTTPMovedPermanently('/login')
        except KeyError:
            self.logger.debug("session error.")
            raise falcon.HTTPMovedPermanently('/login')
        except TypeError:
            self.logger.debug("request path: {0}".format(req.path))
            if req.path != '/login':
                raise falcon.HTTPMovedPermanently('/login')
