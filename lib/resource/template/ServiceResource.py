#!/usr/bin/python3

import falcon

from lib.resource import BaseHtmlTemplateResource


class ServiceResource(BaseHtmlTemplateResource):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = self.get_content('system.html.j2', {'title': 'OS'})
