#!/usr/bin/python3

import bcrypt
import falcon
from sqlalchemy.exc import IntegrityError

from lib.const import Message
from lib.resource import BaseHtmlTemplateResource
from lib.database import Session, Os, Server, Specification, Application
from lib.utility import SystemUtility


def get_os():
    try:
        SystemUtility.cache['db_cache_os_list']
    except KeyError as e:
        oses = []
        session = Session()
        os = session.query(Os).all()
        for e in os:
            oses.append({
                'id': e.id,
                'os_type': e.os_type,
                'os_version': e.os_version
            })
        SystemUtility.cache['db_cache_os_list'] = oses
    finally:
        return SystemUtility.cache['db_cache_os_list']


class ServerManagementAddResource(BaseHtmlTemplateResource):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        index = {
            'title': 'Add Server',
            'servers': [],
            'oses': get_os(),
            'input_ip': '',
            'input_hostname': '',
            'input_rolename': '',
            'input_type_cd': '',
            'input_group_cd': '',
            'input_region': '',
            'input_zone': '',
            'input_description': '',
            'input_cpu_core': '',
            'input_memory': '',
            'input_swap': '',
            'input_system_storage': ''
        }
        resp.body = self.get_content('server_add.html.j2', index)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        index = {
            'title': 'Manage Server',
            'servers': [],
            'oses': get_os(),
            'input_ip': '',
            'input_os_id': '',
            'input_hostname': '',
            'input_rolename': '',
            'input_type_cd': '',
            'input_group_cd': '',
            'input_region': '',
            'input_zone': '',
            'input_description': '',
            'input_cpu_core': '',
            'input_memory': '',
            'input_swap': '',
            'input_system_storage': ''
        }
        form_params = [
            # Server Information.
            ('ip', 'input_ip', 'form-input-ip'),
            ('os_id', 'input_os_id', 'form-select-os-id'),
            ('hostname', 'input_hostname', 'form-input-hostname'),
            ('rolename', 'input_rolename', 'form-input-rolename'),
            ('type_cd', 'input_type_cd', 'form-input-type-cd'),
            ('group_cd', 'input_group_cd', 'form-input-group-cd'),
            ('region', 'input_region', 'form-input-region'),
            ('zone', 'input_zone', 'form-input-zone'),
            ('description', 'input_description', 'form-input-description'),
            # Server Specification.
            ('cpu_core', 'input_cpu_core', 'form-input-cpu-core'),
            ('memory', 'input_memory', 'form-input-memory'),
            ('swap', 'input_swap', 'form-input-swap'),
            ('system_storage', 'input_system_storage', 'form-input-system-storage')
            # Server Storages.
        ]
        for i in form_params:
            index[i[1]] = req.get_param(i[2])
            self.logger.debug("{0}: {1}".format(i[1], index[i[1]]))

        try:
            session = Session()
            os = session.query(Os).filter_by(id=index['input_os_id']).first()
            server = Server(ip=index['input_ip'], hostname=index['input_hostname'], rolename=index['input_rolename'], type_cd=index['input_type_cd'],
                            group_cd=index['input_group_cd'], region=index['input_region'], zone=index['input_zone'], description=index['input_description'])
            session.add(server)
            self.logger.debug('Servers IP addr :{0}'.format(server.ip))
            server = session.query(Server).filter_by(ip=index['input_ip'], hostname=index['input_hostname']).first()
            specification = Specification(server_id=server.id, os_id=os.id, cpu_core=index['input_cpu_core'], memory=index[
                                          'input_memory'], swap=index['input_swap'], system_storage=index['input_system_storage'])
            session.add(specification)
            session.commit()
        except IntegrityError as e:
            self.logger.warning(e)
            index['error_message'] = Message.RESPONSE_DATABASE_DUPLICATE_COMMIT_ERROR
            session.rollback()
        except Exception as e:
            self.logger.error(e)
            resp.status = falcon.HTTP_500
            session.rollback()
            raise falcon.HTTP_INTERNAL_SERVER_ERROR
        finally:
            session.close()

        index['error_message'] = '{0} :[{1}]'.format(
            Message.RESPONSE_SERVER_CREATED, index['input_ip'])
        index['input_ip'] = ''
        index['input_hostname'] = ''
        index['input_rolename'] = ''
        index['input_type_cd'] = ''
        index['input_group_cd'] = ''
        index['input_region'] = ''
        index['input_zone'] = ''
        index['input_description'] = ''
        index['input_cpu_core'] = ''
        index['input_memory'] = ''
        index['input_swap'] = ''
        index['input_system_storage'] = ''

        resp.body = self.get_content('server_add.html.j2', index)
