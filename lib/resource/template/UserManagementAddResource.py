#!/usr/bin/python3

import bcrypt
import falcon
from sqlalchemy.exc import IntegrityError

from lib.const import Message
from lib.resource import BaseHtmlTemplateResource
from lib.database import Session, User, Role
from lib.utility import SystemUtility


def get_role():
    try:
        SystemUtility.cache['db_cache_role_list']
    except KeyError as e:
        role_list = []
        session = Session()
        roles = session.query(Role).all()
        for e in roles:
            role_list.append({
                'id': e.id,
                'role_type': e.role_type
            })
        SystemUtility.cache['db_cache_role_list'] = role_list
    finally:
        return SystemUtility.cache['db_cache_role_list']


class UserManagementAddResource(BaseHtmlTemplateResource):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        index = {
            'title': 'Add User',
            'users': [],
            'roles': get_role(),
            'input_account': '',
            'input_username': '',
            'input_nickname': '',
            'input_mail': '',
            'error_message': ''
        }
        resp.body = self.get_content('user_add.html.j2', index)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        index = {
            'title': 'Manage User',
            'users': [],
            'roles': get_role(),
            'input_account': '',
            'input_username': '',
            'input_nickname': '',
            'input_mail': '',
            'error_message': ''
        }
        index['input_account'] = req.get_param('form-input-account')
        index['input_selected_role'] = req.get_param('form-select-role')
        index['input_password'] = req.get_param('form-input-password')
        index['input_username'] = req.get_param('form-input-username')
        index['input_nickname'] = req.get_param('form-input-nickname')
        index['input_mail'] = req.get_param('form-input-mail')

        self.logger.debug(index['input_account'])
        self.logger.debug(index['input_selected_role'])
        self.logger.debug(index['input_password'])
        self.logger.debug(index['input_username'])
        self.logger.debug(index['input_nickname'])
        self.logger.debug(index['input_mail'])

        if len(index['input_password']) < 8:
            index['error_message'] = Message.RESPONSE_REQUEST_INPUT_PASSWORD_LENGTH_ERROR
            resp.body = self.get_content('user_add.html.j2', index)
            return

        try:
            session = Session()
            role = session.query(Role).filter_by(
                id=index['input_selected_role']).first()
            hashed_password = bcrypt.hashpw(index['input_password'].encode(
                'utf-8'), bcrypt.gensalt(rounds=10, prefix=b'2a'))
            user = User(account=index['input_account'], password=hashed_password.decode(
            ), username=index['input_username'], nickname=index['input_nickname'], role_id=role.id, mail=index['input_mail'])
            session.add(user)
            session.commit()
        except IntegrityError as e:
            self.logger.warning(e)
            index['error_message'] = Message.RESPONSE_DATABASE_DUPLICATE_COMMIT_ERROR
        except Exception as e:
            self.logger.error(e)
            resp.status = falcon.HTTP_500
            raise falcon.HTTP_INTERNAL_SERVER_ERROR
        finally:
            session.close()

        index['error_message'] = '{0} :[{1}]'.format(
            Message.RESPONSE_USER_CREATED, index['input_account'])
        index['input_account'] = ''
        index['input_selected_role'] = 0
        index['input_password'] = ''
        index['input_username'] = ''
        index['input_nickname'] = ''
        index['input_mail'] = ''

        resp.body = self.get_content('user_add.html.j2', index)
