#!/usr/bin/python3

from jinja2 import Template, Environment, FileSystemLoader

from lib.const import Const
from lib.resource import BaseResource
import lib.utility.SystemUtility


class BaseHtmlStaticResource(BaseResource):
    def get_content_type(self):
        return 'text/html; charset=UTF-8'

    def get_content(self, content_name, index=None):
        with open('/'.join([Const.RAW_VIEW_DIR, content_name]), 'rb') as f:
            body = f.read()
        return body
