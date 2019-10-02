#!/usr/bin/python3

import falcon

from lib.resource import BaseHtmlTemplateResource
from lib.database import Session, Server
from lib.utility import SystemUtility


class ServerManagementSearchResource(BaseHtmlTemplateResource):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        index = {
            'title': 'Manage Server',
            'servers': [],
            'input_hostname': '',
            'input_rolename': '',
            'input_type_cd': '',
            'input_group_cd': '',
            'input_region': '',
            'input_zone': ''
        }
        resp.body = self.get_content('server_search.html.j2', index)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        index = {
            'title': 'Manage Server',
            'servers': [],
            'input_hostname': '',
            'input_rolename': '',
            'input_type_cd': '',
            'input_group_cd': '',
            'input_region': '',
            'input_zone': ''
        }
        form_params = [
            ('ip', 'input_ip', 'form-input-ip'),
            ('hostname', 'input_hostname', 'form-input-hostname'),
            ('rolename', 'input_rolename', 'form-input-rolename'),
            ('type_cd', 'input_type_cd', 'form-input-type-cd'),
            ('group_cd', 'input_group_cd', 'form-input-group-cd'),
            ('region', 'input_region', 'form-input-region'),
            ('zone', 'input_zone', 'form-input-zone')
        ]
        for i in form_params:
            index[i[1]] = req.get_param(i[2])
            self.logger.debug("{0}: {1}".format(i[1], index[i[1]]))

        try:
            session = Session()
            query = session.query(Server)
            for i in form_params:
                if len(index[i[1]]) > 0:
                    query = query.filter(getattr(Server, i[0]).like(
                        '%{0}%'.format(index[i[1]])))
            servers = query.order_by(Server.id).limit(100).all()
            for server in servers:
                self.logger.debug(server)
                index['servers'].append(
                    {
                        'id': server.id,
                        'ip': server.ip,
                        'hostname': server.hostname,
                        'rolename': server.rolename,
                        'type_cd': server.type_cd,
                        'group_cd': server.group_cd,
                        'region': server.region,
                        'zone': server.zone
                    }
                )
        except Exception as e:
            self.logger.error(e)
            resp.status = falcon.HTTP_500
            raise falcon.HTTP_INTERNAL_SERVER_ERROR
        finally:
            session.close()
        resp.body = self.get_content('server_search.html.j2', index)
