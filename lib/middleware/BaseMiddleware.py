#!/usr/bin/python3

from datetime import datetime

import lib.utility.SystemUtility


class BaseMiddleware(object):
    def __init__(self):
        self.logger = lib.utility.SystemUtility.get_system_log()
        self.config = lib.utility.SystemUtility.get_config()

    def process_request(self, req, resp):
        pass

    def process_resource(self, req, resp, resource, params):
        self.commonLogging(req, resp)

    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Cache-Control', 'no-store,no-transform')
        if resource is not None:
            resp.content_type = resource.get_content_type()

    def commonLogging(self, req=None, resp=None):
        # For debuging.
        self.logger.debug("{0}>{1}".format("headers", req.headers))
        self.logger.debug("{0}>{1}".format("params", req.params))
        self.logger.debug("{0}>{1}".format("cookies", req.cookies))
