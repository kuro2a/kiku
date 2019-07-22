#!/usr/bin/python3

from urllib.parse import urlparse

import lib.utility.SystemUtility
from lib.const import ConfigKey


class BaseDocument(object):
    def __init__(self, config):
        self.logger = lib.utility.SystemUtility.get_system_log()
        self.engine = urlparse(config[ConfigKey.CONF_KEY_DOCUMENT_ENGINE])
        self.dbType = None
        self.db = None

    def getType(self):
        return self.dbType

    def getHost(self):
        return self.engine.hostname

    def getPort(self):
        return self.engine.port
