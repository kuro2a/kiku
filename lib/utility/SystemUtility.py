#!/usr/bin/python3

import sys
import datetime
import json
import logging

from logging import getLogger, StreamHandler, FileHandler, Formatter
from lib.const import Const, ConfigKey, LogLevel, Version, Message


def get_log_level(level):
    if level == LogLevel.CRITICAL:
        return logging.CRITICAL
    elif level == LogLevel.ERROR:
        return logging.ERROR
    elif level == LogLevel.WARNING:
        return logging.WARNING
    elif level == LogLevel.INFO:
        return logging.INFO
    elif level == LogLevel.DEBUG:
        return logging.DEBUG
    else:
        return logging.DEBUG


class SystemUtility(object):
    system_log = None
    access_log = None
    config = None
    cache = {}
    session_service = None

    @classmethod
    def get_system_log(self, option=None):
        if SystemUtility.system_log is None:
            if option is None:
                raise Exception(Message.EXCEPTION_UNKNOWN_OPTION)
            log_option = option[ConfigKey.CONF_KEY_SYSTEM_SYSTEM_LOG]
            logger = getLogger(
                log_option[ConfigKey.CONF_KEY_SYSTEM_SYSTEM_LOG_LOG_NAME])
            log_format = Formatter(
                '%(asctime)s^%(name)s^%(levelname)s^%(funcName)s^%(message)s')
            logger.setLevel(get_log_level(
                log_option[ConfigKey.CONF_KEY_SYSTEM_SYSTEM_LOG_LOG_LEVEL]))
            file_handler = FileHandler(
                '/'.join([log_option[ConfigKey.CONF_KEY_SYSTEM_SYSTEM_LOG_PATH], log_option[ConfigKey.CONF_KEY_SYSTEM_SYSTEM_LOG_FILE_NAME]]), encoding='utf-8')
            file_handler.setFormatter(log_format)
            stream_handler = StreamHandler()
            stream_handler.setFormatter(log_format)
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)
            SystemUtility.system_log = logger
        return SystemUtility.system_log

    @classmethod
    def get_access_log(self, option=None):
        if SystemUtility.access_log is None:
            if option is None:
                raise Exception(Message.EXCEPTION_UNKNOWN_OPTION)
            log_option = option[ConfigKey.CONF_KEY_SYSTEM_ACCESS_LOG]
            logger = getLogger(
                log_option[ConfigKey.CONF_KEY_SYSTEM_ACCESS_LOG_LOG_NAME])
            logger.setLevel(get_log_level(
                log_option[ConfigKey.CONF_KEY_SYSTEM_ACCESS_LOG_LOG_LEVEL]))
            file_handler = FileHandler(
                '/'.join([log_option[ConfigKey.CONF_KEY_SYSTEM_ACCESS_LOG_PATH], log_option[ConfigKey.CONF_KEY_SYSTEM_ACCESS_LOG_FILE_NAME]]), encoding='utf-8')
            stream_handler = StreamHandler()
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)
            SystemUtility.access_log = logger
        return SystemUtility.access_log

    @classmethod
    def get_config(self):
        if SystemUtility.config is None:
            try:
                with open(Const.SETTING_FILE_PATH, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except:
                print("[ERROR] Configure file is not found.")
                sys.exit(1)
            SystemUtility.config = config
        return SystemUtility.config

    @classmethod
    def get_response_base(self, version):
        if version == Version.VERSION_1:
            data = {
                "meta": {
                    "status": Const.RESPONSE_STATUS_OK,
                    "message": Message.RESPONSE_OK,
                    "timestamp": datetime.datetime.strftime(datetime.datetime.now(), '%Y/%m/%d %H:%M:%S')
                },
                "data": None
            }
        else:
            data = None
        return data

    @classmethod
    def get_response_base_with_body(self, version):
        data = SystemUtility.get_response_base(version)
        data['data'] = {}
        return data

    @classmethod
    def set_response_metadata(self, version, data, status, message):
        if version == Version.VERSION_1:
            try:
                data["meta"]["status"] = status
                data["meta"]["message"] = message
                data["meta"]["timestamp"] = datetime.datetime.strftime(datetime.datetime.now(), '%Y/%m/%d %H:%M:%S')
            except KeyError as e:
                logger = SystemUtility.get_system_log()
                logger.info(str(e))
                SystemUtility.set_response_metadata(Version.VERSION_1, SystemUtility.get_response_base(
                    Version.VERSION_1), status, message)
        else:
            data = None
        return data
