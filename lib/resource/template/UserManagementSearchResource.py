#!/usr/bin/python3

import falcon

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

class UserManagementSearchResource(BaseHtmlTemplateResource):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        index = {
            'title': 'Search User',
            'users': [],
            'roles': get_role(),
            'input_account': '',
            'input_username': '',
            'input_nickname': '',
            'input_mail': ''
        }
        resp.body = self.get_content('user_search.html.j2', index)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        index = {
            'title': 'Search User',
            'users': [],
            'roles': get_role(),
            'input_account': '',
            'input_username': '',
            'input_nickname': '',
            'input_mail': ''
        }
        index['input_account'] = req.get_param('form-input-account')
        index['input_password'] = req.get_param('form-input-password')
        index['input_username'] = req.get_param('form-input-username')
        index['input_nickname'] = req.get_param('form-input-nickname')
        index['input_mail'] = req.get_param('form-input-mail')

        self.logger.debug("input_account: {0}".format(index['input_account']))
        self.logger.debug("input_username: {0}".format(
            index['input_username']))
        self.logger.debug("input_nickname: {0}".format(
            index['input_nickname']))
        self.logger.debug("input_mail: {0}".format(index['input_mail']))

        try:
            session = Session()
            query = session.query(User, Role).join(
                Role, User.role_id == Role.id)
            if len(index['input_account']) > 0:
                query = query.filter(User.account.like(
                    '%{0}%'.format(index['input_account'])))
            if len(index['input_username']) > 0:
                query = query.filter(User.username.like(
                    '%{0}%'.format(index['input_username'])))
            if len(index['input_nickname']) > 0:
                query = query.filter(User.nickname.like(
                    '%{0}%'.format(index['input_nickname'])))
            if len(index['input_mail']) > 0:
                query = query.filter(User.mail.like(
                    '%{0}%'.format(index['input_mail'])))
            users = query.order_by(User.id).limit(100).all()
            for user in users:
                self.logger.debug(user)
                index['users'].append(
                    {
                        'id': user[0].id,
                        'account': user[0].account,
                        'role': user[1].role_type,
                        'username': user[0].username,
                        'nickname': user[0].nickname,
                        'mail': user[0].mail
                    }
                )
        except Exception as e:
            self.logger.error(e)
            resp.status = falcon.HTTP_500
            raise falcon.HTTP_INTERNAL_SERVER_ERROR
        finally:
            session.close()
        resp.body = self.get_content('user_search.html.j2', index)
