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

class UserManagementDeleteResource(BaseHtmlTemplateResource):
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        index = {
            'title': 'Manage User',
            'users': [],
            'roles': get_role(),
            'input_account': '',
            'input_username': '',
            'input_nickname': '',
            'input_mail': ''
        }
        index['input_delete_user_id'] = req.get_param('form-input-delete-user-id')

        self.logger.debug("input_delete_user_id: {0}".format(index['input_delete_user_id']))

        try:
            session = Session()
            target = session.query(User).filter(User.id == int(index['input_delete_user_id'])).first()
            session.delete(target)
            session.commit()
        except Exception as e:
            self.logger.error(e)
            resp.status = falcon.HTTP_500
            session.rollback()
            raise falcon.HTTP_INTERNAL_SERVER_ERROR
        finally:
            session.close()
        resp.body = self.get_content('user_search.html.j2', index)
