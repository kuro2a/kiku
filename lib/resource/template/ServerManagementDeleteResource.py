#!/usr/bin/python3

import falcon

from lib.resource import BaseHtmlTemplateResource
from lib.database import Session, Server, Specification
from lib.utility import SystemUtility


class ServerManagementDeleteResource(BaseHtmlTemplateResource):
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
        index['input_delete_server_id'] = req.get_param('form-input-delete-server-id')

        self.logger.debug("input_delete_server_id: {0}".format(index['input_delete_server_id']))

        try:
            session = Session()
            target = session.query(Specification).filter(Specification.server_id == int(index['input_delete_server_id'])).first()
            session.delete(target)
            target = session.query(Server).filter(Server.id == int(index['input_delete_server_id'])).first()
            session.delete(target)
            session.commit()
        except Exception as e:
            self.logger.error(e)
            resp.status = falcon.HTTP_500
            session.rollback()
            raise falcon.HTTP_INTERNAL_SERVER_ERROR
        finally:
            session.close()
        resp.body = self.get_content('server_search.html.j2', index)
