#!/usr/bin/python3

import json
import falcon

from lib.const import Version, Message
from lib.utility import SystemUtility, DocumentUtility, CustomJSONEncoder
from lib.resource import BaseJsonApiResource

def _get_multiple_result(data, category, key):
    buf_dict = {}
    buf_array = []
    for e in data:
        if type is None:
            try:
                buf_dict[e['timestamp']][e['hostname']] = e[key]
            except:
                buf_dict[e['timestamp']] = {'timestamp': e['timestamp'], e['hostname']: e[key]}
        else:
            try:
                buf_dict[e['timestamp']][e['hostname']] = e[category][key]
            except:
                buf_dict[e['timestamp']] = {'timestamp': e['timestamp'], e['hostname']: e[category][key]}
    for e in buf_dict.keys():
        buf_array.append(buf_dict[e])
    return buf_array

class OsMultipleLogApiResource(BaseJsonApiResource):
    def on_get(self, req, resp, resource, from_date, to_date):
        resp.status = falcon.HTTP_200
        body = SystemUtility.get_response_base_with_body(Version.VERSION_1)
        doc_db = DocumentUtility.get_document()
        hostnames = req.get_param('hostnames').split(',')
        if resource == 'cpu':
            data = doc_db.searchMultipleCpuLog(hostnames, from_date, to_date)
            body['data']['data'] = _get_multiple_result(data, 'cpu', 'ratio')
            body['data']['key'] = hostnames
            self.logger.debug(str(data))
        elif resource == 'memory':
            data = doc_db.searchMultipleMemoryLog(hostnames, from_date, to_date)
            body['data']['data'] = _get_multiple_result(data, 'memory', 'ratio')
            body['data']['key'] = hostnames
            self.logger.debug(str(data))
        elif resource == 'swap':
            data = doc_db.searchMultipleSwapLog(hostnames, from_date, to_date)
            body['data']['data'] = _get_multiple_result(data, 'memory', 'swapped')
            body['data']['key'] = hostnames
            self.logger.debug(str(data))
        elif resource == 'storage':
            data = doc_db.searchMultipleStorageLog(hostnames, 'SYSTEM', from_date, to_date)
            body['data']['data'] = _get_multiple_result(data, None, 'ratio')
            body['data']['key'] = hostnames
            self.logger.debug(str(data))
        elif resource == 'diskio':
            io_type = hostnames = req.get_param('io_type')
            data = doc_db.searchMultipleIoLog(hostnames, io_type, from_date, to_date)
            body['data']['data'] = _get_multiple_result(data, 'io', io_type)
            body['data']['key'] = hostnames
            self.logger.debug(str(data))
        elif resource == 'network':
            pass
        else:
            resp.status = falcon.HTTP_400
            SystemUtility.set_response_metadata(Version.VERSION_1, body, Message.RESPONSE_NG, Message.RESPONSE_REQUEST_URL_ERROR)

        resp.body = json.dumps(body, cls=CustomJSONEncoder)
