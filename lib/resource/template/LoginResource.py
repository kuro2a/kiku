#!/usr/bin/python3

from datetime import datetime, timedelta
import falcon
from jinja2 import Template, Environment, FileSystemLoader
from bcrypt import checkpw

from lib.utility import SystemUtility, SessionUtility
from lib.const import Const, ConfigKey, SessionKey
from lib.resource import BaseHtmlTemplateResource
from lib.database import Session, User


class LoginResource(BaseHtmlTemplateResource):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = self.get_content(
            'login.html.j2', {'title': 'Login', 'error_message': ''})

    def on_post(self, req, resp):
        security_config = dict(SystemUtility.get_config())[
            ConfigKey.CONF_KEY_SYSTEM][ConfigKey.CONF_KEY_SYSTEM_SECURITY]
        session_id = req.get_cookie_values('session_id')[0]
        self.logger.debug(session_id)
        input_account = req.get_param('account')
        input_password = req.get_param('password')

        if security_config[ConfigKey.CONF_KEY_SYSTEM_SECURITY_MODE] == Const.AUTHENTICATION_MODE_DEBUG:
            # DEBUG mode.
            if input_account == security_config[ConfigKey.CONF_KEY_SYSTEM_SECURITY_USER] and input_password == security_config[ConfigKey.CONF_KEY_SYSTEM_SECURITY_PASSWORD]:
                session_service = SessionUtility.get_session_service()
                session_data = session_service.createUserSession(
                    security_config[ConfigKey.CONF_KEY_SYSTEM_SECURITY_USER],
                    Const.ROLE_ADMIN,
                    'Administrator',
                    'Adam',
                    datetime.now()
                )
                session_service.set_session(session_id, session_data)
                self.logger.info(
                    "Login success. account: {0}, session_id: {1}".format(input_account, session_id))
                raise falcon.HTTPFound('/')
            else:
                resp.status = falcon.HTTP_200
                resp.body = self.get_content(
                    'login.html.j2', {'title': 'Login', 'error_message': 'Access denied.'})
                self.logger.info(
                    'Login denied. Account: {0}'.format(input_account))
        else:
            # Product mode.
            resp.status = falcon.HTTP_200
            try:
                session = Session()
                user = session.query(User).filter_by(
                    account=input_account).first()
                self.logger.debug(str(user))
                if checkpw(input_password.encode('utf-8'), user.password.encode('utf-8')):
                    session_service = SessionUtility.get_session_service()
                    session_data = session_service.createUserSession(
                        user.account,
                        user.role_id,
                        user.username,
                        user.nickname,
                        datetime.now()
                    )
                    session_service.set_session(session_id, session_data)
                    self.logger.info(
                        "Login success. account: {0}, session_id: {1}".format(input_account, session_id))
                    raise falcon.HTTPFound('/')
                else:
                    resp.body = self.get_content(
                        'login.html.j2', {'title': 'Login', 'error_message': 'Access denied.'})
                    self.logger.info(
                        'Login denied. Account: {0}'.format(input_account))
            except falcon.HTTPFound as e:
                raise e
            except Exception as e:
                resp.body = self.get_content(
                    'login.html.j2', {'title': 'Login', 'error_message': 'Access denied.'})
                self.logger.info(
                    'Login denied. Account: {0}, message: {1}'.format(input_account, str(e)))
            finally:
                session.close()
