#!/usr/bin/python3

import json

from datetime import datetime
from bson import ObjectId

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj): # pylint: disable=E0202
        if isinstance(obj, datetime):
            return datetime.strftime(obj, '%Y/%m/%d %H:%M:%S')
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(CustomJSONEncoder, self).default(obj)
