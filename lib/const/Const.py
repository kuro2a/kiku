#!/usr/bin/python3


class Const(object):
    SETTING_FILE_PATH = './config.json'
    PUBLIC_DIR = 'public'
    PRIVATE_DIR = 'private'
    RAW_VIEW_DIR = '/'.join([PRIVATE_DIR, 'views', 'raw'])
    TEMPLATE_VIEW_DIR = '/'.join([PRIVATE_DIR, 'views', 'template'])
    COOKIE_SESSION_ID = 'session_id'
    AUTHENTICATION_MODE_DEBUG = 'debug'
    AUTHENTICATION_MODE_PRODUCT = 'product'
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'
    SESSION_TYPE_LOCAL = 'local'
    SESSION_TYPE_REDIS = 'redis'
    SESSION_TYPE_MEMCACHED = 'memcached'
    DATABASE_TYPE_SQLITE = 'sqlite'
    DATABASE_TYPE_POSTGRESQL = 'postgresql'
    DATABASE_TYPE_MYSQL = 'mysql'
    DOCUMENT_TYPE_TINYDB = 'tinydb'
    DOCUMENT_TYPE_MONGODB = 'mongodb'
    RESPONSE_STATUS_OK = 'OK'
    RESPONSE_STATUS_NG = 'NG'
