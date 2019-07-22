#!/usr/bin/python3

import json
import falcon

from lib.const import Version, Message
from lib.utility import SystemUtility, DocumentUtility, CustomJSONEncoder
from lib.resource import BaseJsonApiResource
from lib.database import Session, Server, Application


class ServerApplicationApiResource(BaseJsonApiResource):
    def on_get(self, req, resp, hostname):
        resp.status = falcon.HTTP_200
        body = SystemUtility.get_response_base_with_body(Version.VERSION_1)

        session = Session()
        try:
            info = session.query(Application, Server).join(
                Server, Server.id == Application.server_id).filter(Server.hostname == hostname)
            self.logger.debug("data")
            self.logger.debug(info)
            body['data']['ip'] = info[0][1].ip
            body['data']['hostname'] = info[0][1].hostname
            body['data']['key'] = ['category', 'value', 'note']
            body['data']['data'] = list(map(lambda x: {'category': x[0].application_name, 'value': x[0].application_desc, 'note': x[0].note}, list(info)))
        except Exception as e:
            self.logger.error(e)
            session.rollback()
            resp.status = falcon.HTTP_500
            SystemUtility.set_response_metadata(
                Version.VERSION_1, body, Message.RESPONSE_NG, Message.RESPONSE_DATABASE_CONNECTION_ERROR)
        finally:
            session.close()

        resp.body = json.dumps(body, cls=CustomJSONEncoder)
