#!/usr/bin/python3

from lib.resource.api import VersionApiResource, OsLogApiResource, OsMultipleLogApiResource, OsLatestLogApiResource, ServerInfoApiResource, ServerSpecificationApiResource, ServerApplicationApiResource, MasterInfoApiResource, KikuServiceStatusApiResource, KikuNewsApiResource
from lib.const import Version


class ApiRoute(object):
    @classmethod
    def get_routes(self):
        routes = []
        # API resources.
        routes.append(
            ['/'.join(['/api', Version.VERSION_1, 'version']), VersionApiResource()])
        routes.append(['/'.join(['/api',
                                 Version.VERSION_1,
                                 'os',
                                 '{hostname}',
                                 '{resource}',
                                 '{from_date:dt("%Y%m%d%H%M%S")}',
                                 '{to_date:dt("%Y%m%d%H%M%S")}']), OsLogApiResource()])
        routes.append(['/'.join(['/api',
                                 Version.VERSION_1,
                                 'os_multiple',
                                 '{resource}',
                                 '{from_date:dt("%Y%m%d%H%M%S")}',
                                 '{to_date:dt("%Y%m%d%H%M%S")}']), OsMultipleLogApiResource()])
        routes.append(['/'.join(['/api',
                                 Version.VERSION_1,
                                 'os_latest',
                                 '{hostname}',
                                 '{resource}']), OsLatestLogApiResource()])
        routes.append(['/'.join(['/api',
                                 Version.VERSION_1,
                                 'server',
                                 '{hostname}']), ServerInfoApiResource()])
        routes.append(['/'.join(['/api',
                                 Version.VERSION_1,
                                 'server_spec',
                                 '{hostname}']), ServerSpecificationApiResource()])
        routes.append(['/'.join(['/api',
                                 Version.VERSION_1,
                                 'server_application',
                                 '{hostname}']), ServerApplicationApiResource()])
        routes.append(['/'.join(['/api',
                                 Version.VERSION_1,
                                 'master',
                                 '{target}']), MasterInfoApiResource()])
        routes.append(['/'.join(['/api',
                                 Version.VERSION_1,
                                 'kiku',
                                 'service_status',
                                 '{service_name}']), KikuServiceStatusApiResource()])
        routes.append(['/'.join(['/api',
                                 Version.VERSION_1,
                                 'kiku',
                                 'news',
                                 'latest']), KikuNewsApiResource()])

        return routes
