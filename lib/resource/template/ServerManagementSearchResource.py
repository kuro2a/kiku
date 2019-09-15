#!/usr/bin/python3

import falcon

from lib.resource import BaseHtmlTemplateResource
from lib.database import Session, Server
from lib.utility import SystemUtility


class ServerManagementSearchResource(BaseHtmlTemplateResource):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        index = {
            'title': 'Search User',
            'servers': [],
            'input_hostname': '',
            'input_rolename': '',
            'input_type_cd': '',
            'input_group_cd': '',
            'region': '',
            'zone': ''
        }
        resp.body = self.get_content('server_search.html.j2', index)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        index = {
            'title': 'Search User',
            'servers': [],
            'input_hostname': '',
            'input_rolename': '',
            'input_type_cd': '',
            'input_group_cd': '',
            'region': '',
            'zone': ''
        }
        index['input_ip'] = req.get_param('form-input-ip')
        index['input_hostname'] = req.get_param('form-input-hostname')
        index['input_rolename'] = req.get_param('form-input-rolename')
        index['input_type_cd'] = req.get_param('form-input-type-cd')
        index['input_group_cd'] = req.get_param('form-input-group-cd')
        index['input_region'] = req.get_param('form-input-region')
        index['input_zone'] = req.get_param('form-input-zone')
        self.logger.debug("input_ip: {0}".format(index['input_ip']))
        self.logger.debug("input_hostname: {0}".format(
            index['input_hostname']))
        self.logger.debug("input_rolename: {0}".format(
            index['input_rolename']))
        self.logger.debug("input_type_cd: {0}".format(index['input_type_cd']))
        self.logger.debug("input_group_cd: {0}".format(index['input_group_cd']))
        self.logger.debug("input_region: {0}".format(index['input_region']))
        self.logger.debug("input_zone: {0}".format(index['input_zone']))

        try:
            session = Session()
            query = session.query(Server)
            if len(index['input_ip']) > 0:
                query = query.filter(Server.ip.like(
                    '%{0}%'.format(index['input_ip'])))
            if len(index['input_hostname']) > 0:
                query = query.filter(Server.hostname.like(
                    '%{0}%'.format(index['input_hostname'])))
            if len(index['input_rolename']) > 0:
                query = query.filter(Server.rolename.like(
                    '%{0}%'.format(index['input_rolename'])))
            if len(index['input_type_cd']) > 0:
                query = query.filter(Server.type_cd.like(
                    '%{0}%'.format(index['input_type_cd'])))
            if len(index['input_group_cd']) > 0:
                query = query.filter(Server.group_cd.like(
                    '%{0}%'.format(index['input_group_cd'])))
            if len(index['input_region']) > 0:
                query = query.filter(Server.region.like(
                    '%{0}%'.format(index['input_region'])))
            if len(index['input_zone']) > 0:
                query = query.filter(Server.zone.like(
                    '%{0}%'.format(index['input_zone'])))
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
