#!/usr/bin/python3

from lib.resource.template import LogResource, DescriptionResource, UserManagementSearchResource, UserManagementAddResource, UserManagementDeleteResource, ServerManagementSearchResource, ServerManagementAddResource, ServerManagementDeleteResource, BetaDummyResource
from lib.resource.static import PrototypeResource
from lib.const import Version


class PageRoute(object):
    @classmethod
    def get_routes(self):
        routes = []
        # Write your page resources here.
        routes.append(['/prototype', PrototypeResource()])
        routes.append(['/infrastructure', BetaDummyResource()])
        routes.append(['/service', BetaDummyResource()])
        routes.append(['/log/{hostname}', LogResource()])
        routes.append(['/description/{hostname}', DescriptionResource()])
        routes.append(['/manage/user', UserManagementSearchResource()])
        routes.append(['/manage/user/add', UserManagementAddResource()])
        routes.append(['/manage/user/delete', UserManagementDeleteResource()])
        routes.append(['/manage/server', ServerManagementSearchResource()])
        routes.append(['/manage/server/add', ServerManagementAddResource()])
        routes.append(['/manage/server/delete', ServerManagementDeleteResource()])

        return routes
