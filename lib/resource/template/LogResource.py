#!/usr/bin/python3

import falcon

from lib.resource import BaseHtmlTemplateResource


class LogResource(BaseHtmlTemplateResource):
    def on_get(self, req, resp, hostname):
        resp.status = falcon.HTTP_200
        resp.body = self.get_content('log.html.j2', {})
