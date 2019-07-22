#!/usr/bin/python3

from jinja2 import Template, Environment, FileSystemLoader

from lib.const import Const
from lib.resource import BaseResource
import lib.utility.SystemUtility


class BaseJsonApiResource(BaseResource):
    def get_content_type(self):
        return 'application/json; charset=UTF-8'
