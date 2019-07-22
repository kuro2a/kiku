#!/usr/bin/python3

import json
import falcon

from lib.const import Version, Message
from lib.utility import SystemUtility, DocumentUtility, CustomJSONEncoder
from lib.resource import BaseJsonApiResource
from lib.database import Session, Server


class MasterInfoApiResource(BaseJsonApiResource):
    def on_get(self, req, resp, target):
        resp.status = falcon.HTTP_200
        body = SystemUtility.get_response_base_with_body(Version.VERSION_1)

        session = Session()
        try:
            if target == 'server':
                servers = session.query(Server).all()
                body['data']['data'] = []
                for server in servers:
                    body['data']['data'].append({
                        'hostname': server.hostname,
                        'ip': server.ip,
                        'role': server.rolename,
                        'region': server.region,
                        'zone': server.zone
                    })
            else:
                resp.status = falcon.HTTP_400
                SystemUtility.set_response_metadata(Version.VERSION_1, body, Message.RESPONSE_NG, Message.RESPONSE_REQUEST_URL_ERROR)
        except Exception as e:
            self.logger.error(e)
            session.rollback()
            resp.status = falcon.HTTP_500
            SystemUtility.set_response_metadata(
                Version.VERSION_1, body, Message.RESPONSE_NG, Message.RESPONSE_DATABASE_CONNECTION_ERROR)
        finally:
            session.close()

        resp.body = json.dumps(body, cls=CustomJSONEncoder)
