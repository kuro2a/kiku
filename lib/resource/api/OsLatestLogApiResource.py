#!/usr/bin/python3

import json
import falcon

from lib.const import Version, Message
from lib.utility import SystemUtility, DocumentUtility, CustomJSONEncoder
from lib.resource import BaseJsonApiResource


class OsLatestLogApiResource(BaseJsonApiResource):
    def on_get(self, req, resp, hostname, resource):
        resp.status = falcon.HTTP_200
        body = SystemUtility.get_response_base_with_body(Version.VERSION_1)
        doc_db = DocumentUtility.get_document()
        if resource == 'cpu':
            data = doc_db.latestCpuLog(hostname)
            body['data']['data'] = list(map(lambda x: {'timestamp': x['timestamp'], 'ratio': x['cpu']['ratio']}, data))
            body['data']['key'] = ['ratio']
            self.logger.debug(str(data))
        elif resource == 'memory':
            data = doc_db.latestMemoryLog(hostname)
            body['data']['data'] = list(map(lambda x: {'timestamp': x['timestamp'], 'ratio': x['memory']['ratio']}, data))
            body['data']['key'] = ['ratio']
            self.logger.debug(str(data))
        elif resource == 'swap':
            data = doc_db.latestSwapLog(hostname)
            body['data']['data'] = list(map(lambda x: {'timestamp': x['timestamp'], 'swapped': x['memory']['swapped']}, data))
            body['data']['key'] = ['swapped']
            self.logger.debug(str(data))
        elif resource == 'storage':
            data = doc_db.latestTargetStorageLog(hostname, '/')
            body['data']['data'] = list(map(lambda x: {'timestamp': x['timestamp'], 'ratio': x['storage']['ratio']}, data))
            body['data']['key'] = ['ratio']
            self.logger.debug(str(data))
        elif resource == 'diskio':
            data = doc_db.latestIoLog(hostname)
            body['data']['data'] = list(map(lambda x: {'timestamp': x['timestamp'], 'block_in': x['io']['block_in'], 'block_out': x['io']['block_out']}, data))
            body['data']['key'] = ['block_in', 'block_out']
            self.logger.debug(str(data))
        elif resource == 'network':
            pass
        else:
            resp.status = falcon.HTTP_400
            SystemUtility.set_response_metadata(Version.VERSION_1, body, Message.RESPONSE_NG, Message.RESPONSE_REQUEST_URL_ERROR)

        resp.body = json.dumps(body, cls=CustomJSONEncoder)
