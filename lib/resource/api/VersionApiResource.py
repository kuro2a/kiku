#!/usr/bin/python3

import json
import falcon

from lib.utility import SystemUtility
from lib.const import Version
from lib.resource import BaseJsonApiResource


class VersionApiResource(BaseJsonApiResource):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        data = SystemUtility.get_response_base(Version.VERSION_1)
        resp.body = json.dumps(data)
