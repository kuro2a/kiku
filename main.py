#!/usr/bin/python3

import signal
import os
import sys
import falcon
import json
from wsgiref.simple_server import make_server, WSGIServer, WSGIRequestHandler
from socketserver import ThreadingMixIn
from http.cookies import SimpleCookie

from lib.route import CommonRoute, PageRoute, ApiRoute
from lib.const import Const, Message, ConfigKey
from lib.utility import SystemUtility, SessionUtility, DocumentUtility
from lib.middleware import CommonMiddleware
from lib.database import Base, engine

system_config = None
system_logger = None
access_logger = None
session_service = None
document = None


def signal_handler(signum, frame):
    return_val = 0
    if signum == signal.SIGTERM or signum == signal.SIGINT:
        return_val = 0
    else:
        return_val = 1
    system_logger.info("[END] Caught the signal: Signal({0})".format(signum))
    sys.exit(return_val)


class ThreadedSWGIServer(ThreadingMixIn, WSGIServer):
    pass


class CustomLoggingWSGIRequestHandler(WSGIRequestHandler):
    def log_message(self, format, *args):
        global access_logger
        env = self.get_environ()
        try:
            cookie = SimpleCookie(env['HTTP_COOKIE'])
            session_id = cookie[Const.COOKIE_SESSION_ID].value
        except:
            session_id = ''
        access_logger.info('{0}^{1}^{2}^{3}^{4}'.format(
            self.client_address[0], self.log_date_time_string(), format % args, env['HTTP_USER_AGENT'], session_id))


def create_service():
    global system_config, system_logger, access_logger, session_service, document
    # Init configure.
    system_config = dict(SystemUtility.get_config())  # Avoid pylint error.
    # Init logger.
    system_logger = SystemUtility.get_system_log(
        system_config[ConfigKey.CONF_KEY_SYSTEM])
    access_logger = SystemUtility.get_access_log(
        system_config[ConfigKey.CONF_KEY_SYSTEM])
    # Init session service.
    session_service = SessionUtility.get_session_service(
        system_config[ConfigKey.CONF_KEY_SYSTEM])
    # Init database.
    Base.metadata.create_all(bind=engine)
    # Init document.
    document = DocumentUtility.get_document(
        system_config[ConfigKey.CONF_KEY_SYSTEM])
    system_logger.info(system_config)
    app = falcon.API(middleware=[CommonMiddleware()])
    app.req_options.auto_parse_form_urlencoded = True
    app.add_static_route('/' + Const.PUBLIC_DIR, '/'.join(
        [os.path.dirname(os.path.abspath(__file__)), Const.PUBLIC_DIR]))
    for i in CommonRoute.get_routes() + PageRoute.get_routes() + ApiRoute.get_routes():
        system_logger.info('add_route: {0}'.format(i[0]))
        app.add_route(i[0], i[1])
    return app


def main():
    global system_config, system_logger
    app = create_service()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    httpd = make_server(system_config[ConfigKey.CONF_KEY_SYSTEM][ConfigKey.CONF_KEY_SYSTEM_SERVER][ConfigKey.CONF_KEY_SYSTEM_SERVER_HOST],
                        system_config[ConfigKey.CONF_KEY_SYSTEM][ConfigKey.CONF_KEY_SYSTEM_SERVER][
                            ConfigKey.CONF_KEY_SYSTEM_SERVER_PORT], app,
                        server_class=ThreadedSWGIServer, handler_class=CustomLoggingWSGIRequestHandler)
    system_logger.info('[START] http server.')
    httpd.serve_forever()


if __name__ == '__main__':
    main()
