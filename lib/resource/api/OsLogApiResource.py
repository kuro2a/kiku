#!/usr/bin/python3

import json
import falcon

from lib.const import Version, Message
from lib.utility import SystemUtility, DocumentUtility, CustomJSONEncoder
from lib.resource import BaseJsonApiResource


class OsLogApiResource(BaseJsonApiResource):
    def on_get(self, req, resp, hostname, resource, from_date, to_date):
        resp.status = falcon.HTTP_200
        body = SystemUtility.get_response_base_with_body(Version.VERSION_1)
        doc_db = DocumentUtility.get_document()
        if resource == 'cpu':
            data = doc_db.searchCpuLog(hostname, from_date, to_date)
            body['data']['data'] = list(map(lambda x: {'timestamp': x['timestamp'], 'ratio': x['cpu']['ratio'], 'user': x['cpu']['user'], 'sys': x['cpu']['sys'], 'idle': x['cpu']['idle'], 'wait': x['cpu']['wait'], 'steal': x['cpu']['steal']}, data))
            body['data']['key'] = ['user', 'sys', 'idle', 'wait', 'steal']
            self.logger.debug(str(data))
        elif resource == 'memory':
            data = doc_db.searchMemoryLog(hostname, from_date, to_date)
            body['data']['data'] = list(map(lambda x: {'timestamp': x['timestamp'], 'ratio': x['memory']['ratio'], 'free': x['memory']['free'], 'buff': x['memory']['buff'], 'cache': x['memory']['cache']}, data))
            body['data']['key'] = ['free', 'buff', 'cache']
            self.logger.debug(str(data))
        elif resource == 'swap':
            data = doc_db.searchSwapLog(hostname, from_date, to_date)
            body['data']['data'] = list(map(lambda x: {'timestamp': x['timestamp'], 'swapped': x['memory']['swapped']}, data))
            body['data']['key'] = ['swapped']
            self.logger.debug(str(data))
        elif resource == 'storage':
            data = doc_db.searchStorageLog(hostname, 'SYSTEM', from_date, to_date)
            body['data']['data'] = data
            body['data']['key'] = ['ratio']
            self.logger.debug(str(data))
        elif resource == 'diskio':
            data = doc_db.searchIoLog(hostname, from_date, to_date)
            body['data']['data'] = list(map(lambda x: {'timestamp': x['timestamp'], 'block_in': x['io']['block_in'], 'block_out': x['io']['block_out']}, data))
            body['data']['key'] = ['block_in', 'block_out']
            self.logger.debug(str(data))
        elif resource == 'network':
            pass
        else:
            resp.status = falcon.HTTP_400
            SystemUtility.set_response_metadata(Version.VERSION_1, body, Message.RESPONSE_NG, Message.RESPONSE_REQUEST_URL_ERROR)

        resp.body = json.dumps(body, cls=CustomJSONEncoder)
