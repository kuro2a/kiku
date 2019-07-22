#!/usr/bin/python3

import falcon

from lib.resource import BaseHtmlStaticResource


class PrototypeResource(BaseHtmlStaticResource):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = self.get_content('prototype.html')
