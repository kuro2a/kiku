#!/usr/bin/python3

from jinja2 import Template, Environment, FileSystemLoader

from lib.const import Const
import lib.utility.SystemUtility


class BaseResource(object):
    def __init__(self):
        self.logger = lib.utility.SystemUtility.get_system_log()
        self.config = lib.utility.SystemUtility.get_config()

    def get_content(self, content_name, index=None):
        pass

    def get_content_type(self):
        return 'text/plain; charset=UTF-8'
