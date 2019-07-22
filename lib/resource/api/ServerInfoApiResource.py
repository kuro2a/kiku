#!/usr/bin/python3

import json
import falcon

from lib.const import Version, Message
from lib.utility import SystemUtility, DocumentUtility, CustomJSONEncoder
from lib.resource import BaseJsonApiResource
from lib.database import Session, Server


class ServerInfoApiResource(BaseJsonApiResource):
    def on_get(self, req, resp, hostname):
        resp.status = falcon.HTTP_200
        body = SystemUtility.get_response_base_with_body(Version.VERSION_1)

        session = Session()
        try:
            info = session.query(Server).filter(Server.hostname == hostname).first()
            self.logger.debug(info)
            body['data']['ip'] = info.ip
            body['data']['hostname'] = info.hostname
            body['data']['key'] = ['category', 'value', 'note']
            body['data']['data'] = [
                {'category': 'Hostname', 'value': info.hostname, 'note': ''},
                {'category': 'IP', 'value': info.ip, 'note': ''},
                {'category': 'Role', 'value': info.rolename, 'note': ''},
                {'category': 'Region', 'value': info.region, 'note': ''},
                {'category': 'Zone', 'value': info.zone, 'note': ''}
            ]
        except Exception as e:
            self.logger.error(e)
            session.rollback()
            resp.status = falcon.HTTP_500
            SystemUtility.set_response_metadata(
                Version.VERSION_1, body, Message.RESPONSE_NG, Message.RESPONSE_DATABASE_CONNECTION_ERROR)
        finally:
            session.close()

        resp.body = json.dumps(body, cls=CustomJSONEncoder)
