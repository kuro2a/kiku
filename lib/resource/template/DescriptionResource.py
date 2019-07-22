#!/usr/bin/python3

import falcon

from lib.resource import BaseHtmlTemplateResource


class DescriptionResource(BaseHtmlTemplateResource):
    def on_get(self, req, resp, hostname):
        resp.status = falcon.HTTP_200
        resp.body = self.get_content('description.html.j2', {})
