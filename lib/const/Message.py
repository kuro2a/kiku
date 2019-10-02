#!/usr/bin/python3


class Message(object):
    EXCEPTION_UNKNOWN_OPTION = 'Unknown option injected.'
    EXCEPTION_UNKNOWN_TYPE = 'Unknown service type selected.'
    RESPONSE_OK = 'OK'
    RESPONSE_NG = 'NG'
    RESPONSE_FORMAT_ERROR = 'Format error.'
    RESPONSE_REQUEST_URL_ERROR = 'Request URL error.'
    RESPONSE_REQUEST_INPUT_PASSWORD_LENGTH_ERROR = 'Password must be at least 8 characters.'
    RESPONSE_DATABASE_CONNECTION_ERROR = 'Database connection error.'
    RESPONSE_DATABASE_COMMIT_ERROR = 'Database commit error.'
    RESPONSE_DATABASE_DUPLICATE_COMMIT_ERROR = 'Database duplicate commit error.'
    RESPONSE_USER_CREATED = 'User created.'
    RESPONSE_SERVER_CREATED = 'Server created.'
