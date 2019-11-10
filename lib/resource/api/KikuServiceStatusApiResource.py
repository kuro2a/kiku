#!/usr/bin/python3

import json
import falcon
from datetime import datetime

from lib.const import Version, Message
from lib.utility import SystemUtility, DocumentUtility, CustomJSONEncoder
from lib.resource import BaseJsonApiResource
from lib.database import Session, Server, User


class KikuServiceStatusApiResource(BaseJsonApiResource):
    def on_get(self, req, resp, service_name):
        resp.status = falcon.HTTP_200
        body = SystemUtility.get_response_base_with_body(Version.VERSION_1)

        session = Session()
        try:
            body['data']['data'] = {'service_name': service_name}
            if service_name == 'registered_server':
                servers = session.query(Server).count()
                body['data']['data'] = [
                    {'timestamp': datetime.now(), 'servers': servers}]
                body['data']['key'] = ['servers']
            elif service_name == 'registered_user':
                users = session.query(User).count()
                body['data']['data'] = [
                    {'timestamp': datetime.now(), 'users': users}]
                body['data']['key'] = ['users']
            else:
                resp.status = falcon.HTTP_400
                body['data']['data'] = None
                SystemUtility.set_response_metadata(
                    Version.VERSION_1, body, Message.RESPONSE_NG, Message.RESPONSE_REQUEST_PARAMETER_ERROR)
        except Exception as e:
            self.logger.error(e)
            session.rollback()
            resp.status = falcon.HTTP_500
            SystemUtility.set_response_metadata(
                Version.VERSION_1, body, Message.RESPONSE_NG, Message.RESPONSE_DATABASE_CONNECTION_ERROR)
        finally:
            session.close()

        resp.body = json.dumps(body, cls=CustomJSONEncoder)
