#!/usr/bin/python3

from lib.resource.template import SystemResource, OsResource, MiddlewareResource, LogResource, DescriptionResource, UserManagementSearchResource, UserManagementAddResource, UserManagementDeleteResource, BetaDummyResource
from lib.resource.static import PrototypeResource
from lib.const import Version


class PageRoute(object):
    @classmethod
    def get_routes(self):
        routes = []
        # Write your page resources here.
        routes.append(['/prototype', PrototypeResource()])
        routes.append(['/system', BetaDummyResource()])
        routes.append(['/os', BetaDummyResource()])
        routes.append(['/middleware', BetaDummyResource()])
        routes.append(['/log/{hostname}', LogResource()])
        routes.append(['/description/{hostname}', DescriptionResource()])
        routes.append(['/manage/user', UserManagementSearchResource()])
        routes.append(['/manage/user/add', UserManagementAddResource()])
        routes.append(['/manage/user/delete', UserManagementDeleteResource()])
        routes.append(['/manage/server', BetaDummyResource()])

        return routes
