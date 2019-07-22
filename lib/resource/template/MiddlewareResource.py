#!/usr/bin/python3

import falcon

from lib.resource import BaseHtmlTemplateResource


class MiddlewareResource(BaseHtmlTemplateResource):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = self.get_content('middleware.html.j2', {
                                     'title': 'Middleware'})
