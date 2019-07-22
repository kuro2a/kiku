#!/usr/bin/python3

from jinja2 import Template, Environment, FileSystemLoader

from lib.const import Const
from lib.resource import BaseResource
from lib.database import Session, Server
import lib.utility.SystemUtility


class BaseHtmlTemplateResource(BaseResource):
    def get_content_type(self):
        return 'text/html; charset=UTF-8'

    def get_content(self, content_name, index=None):
        env = Environment(loader=FileSystemLoader(Const.TEMPLATE_VIEW_DIR))
        template = env.get_template(content_name)
        try:
            lib.utility.SystemUtility.cache['db_cache_server_list']
        except KeyError as e:
            self.logger.info('Cannot get server list cache. Create cache...')
            server_list = []
            session = Session()
            servers = session.query(Server).all()
            for e in servers:
                server_list.append({
                    'ip': e.ip,
                    'hostname': e.hostname,
                    'rolename': e.rolename,
                    'type_cd': e.type_cd,
                    'group_cd': e.group_cd,
                    'region': e.region,
                    'zone': e.zone,
                    'description': e.description
                })
                self.logger.info(e)
            lib.utility.SystemUtility.cache['db_cache_server_list'] = server_list
        finally:
            index['menu_servers'] = lib.utility.SystemUtility.cache['db_cache_server_list']

        return template.render(index)
