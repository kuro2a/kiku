#!/usr/bin/python3

from lib.resource.template import IndexResource, LoginResource
from lib.resource.static import LogoutResource
from lib.const import Version


class CommonRoute(object):
    @classmethod
    def get_routes(self):
        routes = []
        routes.append(['/', IndexResource()])
        routes.append(['/login', LoginResource()])
        routes.append(['/logout', LogoutResource()])

        return routes
