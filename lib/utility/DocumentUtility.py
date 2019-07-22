#!/usr/bin/python3

from urllib.parse import urlparse

from lib.const import Const, ConfigKey, Message
from lib.document import MongoDbDocument, TinyDbDocument

class DocumentUtility(object):
    config = None
    database = None

    @classmethod
    def get_document(self, config=None):
        if DocumentUtility.database is None:
            if config is None:
                raise Exception(Message.EXCEPTION_UNKNOWN_OPTION)
            document_config = config[ConfigKey.CONF_KEY_DOCUMENT]
            document_type = urlparse(document_config[ConfigKey.CONF_KEY_DOCUMENT_ENGINE]).scheme
            if document_type == Const.DOCUMENT_TYPE_TINYDB:
                database = TinyDbDocument(document_config)
            elif document_type == Const.DOCUMENT_TYPE_MONGODB:
                database = MongoDbDocument(document_config)
            else:
                raise Exception(Message.EXCEPTION_UNKNOWN_TYPE)
            DocumentUtility.config = config
            DocumentUtility.database = database
        return DocumentUtility.database
