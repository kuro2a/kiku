#!/usr/bin/python3

import os
import falcon


from lib.utility import SystemUtility
from lib.resource import BaseHtmlTemplateResource


class IndexResource(BaseHtmlTemplateResource):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = self.get_content('index.html.j2', {'title': 'Login'})
