#!/usr/bin/python3

import json
import falcon

from lib.const import Version, Message
from lib.utility import SystemUtility, DocumentUtility, CustomJSONEncoder
from lib.resource import BaseJsonApiResource
from lib.database import Session, Server, Specification, Storage, NicType, Os


class ServerSpecificationApiResource(BaseJsonApiResource):
    def on_get(self, req, resp, hostname):
        resp.status = falcon.HTTP_200
        body = SystemUtility.get_response_base_with_body(Version.VERSION_1)
        doc_db = DocumentUtility.get_document()

        session = Session()
        try:
            info = session.query(Server, Specification, Os).join(
                Specification, Server.id == Specification.server_id).join(
                    Os, Specification.os_id == Os.id
                ).filter(Server.hostname == hostname).first()
            self.logger.debug(info)
            body['data']['ip'] = info[0].ip
            body['data']['hostname'] = info[0].hostname
            body['data']['key'] = ['category', 'value', 'note']
            body['data']['data'] = [
                {'category': 'OS', 'value': info[2].os_version, 'note': ''},
                {'category': 'CPUs',
                    'value': info[1].cpu_core, 'note': ''},
                {'category': 'Memory', 'value': "{0:.2f}GB".format(
                    info[1].memory/1024**2), 'note': ''},
                {'category': 'Swap', 'value': "{0:.2f}GB".format(
                    info[1].swap/1024**2), 'note': ''},
                {'category': 'Storage', 'value': "{0:.2f}GB".format(
                    info[1].system_storage/1024**2), 'note': ''}
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
