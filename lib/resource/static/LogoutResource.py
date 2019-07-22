#!/usr/bin/python3

import falcon

from lib.utility import SystemUtility, SessionUtility
from lib.resource import BaseHtmlStaticResource


class LogoutResource(BaseHtmlStaticResource):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        session_id = req.get_cookie_values('session_id')[0]
        session_service = SessionUtility.get_session_service()
        session_service.remove_session(session_id)
        resp.unset_cookie('session_id')
        resp.body = self.get_content('logout.html')
