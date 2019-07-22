#!/usr/bin/python3

import sys
import pathlib
from datetime import datetime
import bcrypt
import pytest

sys.path.append( str(pathlib.Path(__file__).resolve().parent) + '/../' )

from lib.database import Base, engine, Session, Role, User, Server, Specification, NicType, Os, Application
from lib.const import ConfigKey
from lib.utility import SystemUtility, DocumentUtility

@pytest.fixture()
def init_db():
    Base.metadata.create_all(bind=engine)

@pytest.fixture()
def init_document():
    conf = dict(SystemUtility.get_config())
    SystemUtility.get_system_log(conf[ConfigKey.CONF_KEY_SYSTEM])
    SystemUtility.get_access_log(conf[ConfigKey.CONF_KEY_SYSTEM])
    DocumentUtility.get_document(conf[ConfigKey.CONF_KEY_SYSTEM])

def test_create_user(init_db):
    user_roles = [
        {
            "role_type": "admin"
        },
        {
            "role_type": "user"
        }
    ]

    users = [
        {
            "account": "admin",
            "password": "admin",
            "username": "Administrator",
            "nickname": "admin",
            "role_id": "admin",
            "mail": "admin@master.com",
        },
        {
            "account": "test1",
            "password": "test1",
            "username": "Test User1",
            "nickname": "test1",
            "role_id": "user",
            "mail": "test1@master.com",
        },
        {
            "account": "test2",
            "password": "test2",
            "username": "Test User2",
            "nickname": "test2",
            "role_id": "user",
            "mail": "test2@master.com",
        }
    ]

    session = Session()
    try:
        session.query(Role).delete()
        session.query(User).delete()

        for e in user_roles:
            role = Role(role_type=e['role_type'])
            session.add(role)

        for e in users:
            salt = bcrypt.gensalt(rounds=10, prefix=b'2a')
            role = session.query(Role).filter_by(role_type=e['role_id']).first()
            user = User(account=e['account'], password=bcrypt.hashpw(e['password'].encode('utf-8'), salt).decode(), username=e['username'], nickname=e['nickname'], role_id=role.id, mail=e['mail'])
            session.add(user)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    assert True


def test_create_master(init_db):
    os_types = [
        {
            "os_type": "Linux",
            "os_version": "Ubuntu 16.04"
        },
        {
            "os_type": "Linux",
            "os_version": "Ubuntu 18.04"
        }
    ]

    servers = [
        {
            'common': {
                'ip' : '192.168.3.4',
                'hostname' : 'iris',
                'rolename' : 'Infra Server#1',
                'type_cd' : 'infra',
                'group_cd' : '1',
                'region' : 'east_japan',
                'zone' : 'rack_1',
                'description' : ''
            },
            'spec': {
                'os_id' : "Ubuntu 18.04",
                'cpu_core' : 4,
                'memory' : 32*1024**2,
                'swap' : 8*1024**2,
                'system_storage' : 500*1024**2,
                'data_storage_1' : None,
                'data_storage_2' : None,
                'data_storage_3' : None,
                'data_storage_4' : None,
                'nic_type_1' : None,
                'nic_type_2' : None,
                'nic_type_3' : None,
                'nic_type_4' : None,
                'ext_device_1' : None,
                'ext_device_2' : None,
                'ext_device_3' : None,
                'ext_device_4' : None
            },
            'app':[
                {'name':'Hypervisor', 'desc':'KVM', 'note':''}
            ]
        },
        {
            'common': {
                'ip' : '192.168.3.10',
                'hostname' : 'rose',
                'rolename' : 'Docker Server#1',
                'type_cd' : 'ap',
                'group_cd' : '2',
                'region' : 'east_japan',
                'zone' : 'rack_1',
                'description' : ''
            },
            'spec': {
                'os_id' : "Ubuntu 18.04",
                'cpu_core' : 2,
                'memory' : 8*1024**2,
                'swap' : 2*1024**2,
                'system_storage' : 50*1024**2,
                'data_storage_1' : None,
                'data_storage_2' : None,
                'data_storage_3' : None,
                'data_storage_4' : None,
                'nic_type_1' : None,
                'nic_type_2' : None,
                'nic_type_3' : None,
                'nic_type_4' : None,
                'ext_device_1' : None,
                'ext_device_2' : None,
                'ext_device_3' : None,
                'ext_device_4' : None
            },
            'app':[
                {'name':'Container', 'desc':'Docker', 'note':''},
                {'name':'Database', 'desc':'PostgreSQL', 'note':''},
                {'name':'Database', 'desc':'MongoDB', 'note':''},
                {'name':'Database', 'desc':'Elasticsearch', 'note':''}
            ]
        }, 
        {
            'common': {
                'ip' : '192.168.3.2',
                'hostname' : 'lily',
                'rolename' : 'Network Server#1',
                'type_cd' : 'nw',
                'group_cd' : '1',
                'region' : 'east_japan',
                'zone' : 'rack_1',
                'description' : ''
            },
            'spec': {
                'os_id' : "Ubuntu 18.04",
                'cpu_core' : 1,
                'memory' : 2*1024**2,
                'swap' : 2*1024**2,
                'system_storage' : 30*1024**2,
                'data_storage_1' : None,
                'data_storage_2' : None,
                'data_storage_3' : None,
                'data_storage_4' : None,
                'nic_type_1' : None,
                'nic_type_2' : None,
                'nic_type_3' : None,
                'nic_type_4' : None,
                'ext_device_1' : None,
                'ext_device_2' : None,
                'ext_device_3' : None,
                'ext_device_4' : None
            },
            'app':[
                {'name':'Proxy', 'desc':'nginx', 'note':''}
            ]
        }, 
        {
            'common': {
                'ip' : '192.168.3.5',
                'hostname' : 'lotus',
                'rolename' : 'NFS Server#1',
                'type_cd' : 'nw',
                'group_cd' : '1',
                'region' : 'east_japan',
                'zone' : 'rack_1',
                'description' : ''
            },
            'spec': {
                'os_id' : "Ubuntu 18.04",
                'cpu_core' : 1,
                'memory' : 2*1024**2,
                'swap' : 2*1024**2,
                'system_storage' : 30*1024**2,
                'data_storage_1' : None,
                'data_storage_2' : None,
                'data_storage_3' : None,
                'data_storage_4' : None,
                'nic_type_1' : None,
                'nic_type_2' : None,
                'nic_type_3' : None,
                'nic_type_4' : None,
                'ext_device_1' : None,
                'ext_device_2' : None,
                'ext_device_3' : None,
                'ext_device_4' : None
            },
            'app':[
                {'name':'nfs', 'desc':'samba', 'note':''}
            ]
        }, 
        {
            'common': {
                'ip' : '192.168.3.21',
                'hostname' : 'daisy',
                'rolename' : 'Gitlab Server#1',
                'type_cd' : 'ap',
                'group_cd' : '2',
                'region' : 'east_japan',
                'zone' : 'rack_1',
                'description' : ''
            },
            'spec': {
                'os_id' : "Ubuntu 18.04",
                'cpu_core' : 1,
                'memory' : 6*1024**2,
                'swap' : 2*1024**2,
                'system_storage' : 30*1024**2,
                'data_storage_1' : None,
                'data_storage_2' : None,
                'data_storage_3' : None,
                'data_storage_4' : None,
                'nic_type_1' : None,
                'nic_type_2' : None,
                'nic_type_3' : None,
                'nic_type_4' : None,
                'ext_device_1' : None,
                'ext_device_2' : None,
                'ext_device_3' : None,
                'ext_device_4' : None
            },
            'app':[
                {'name':'Application', 'desc':'Gitlab', 'note':''}
            ]
        }
    ]
    nic_types = [
        {
            'type_name' : '10BASE-T',
            'link_speed' : 10
        },
        {
            'type_name' : '100BASE-T',
            'link_speed' : 100
        },
        {
            'type_name' : '1000BASE-T',
            'link_speed' : 1000
        },
        {
            'type_name' : '10GBASE-T',
            'link_speed' : 10000
        },
        {
            'type_name' : '802.11b_11',
            'link_speed' : 11
        },
        {
            'type_name' : '802.11b_22',
            'link_speed' : 22
        },
        {
            'type_name' : '802.11a',
            'link_speed' : 54
        },
        {
            'type_name' : '802.11g',
            'link_speed' : 54
        },
        {
            'type_name' : '802.11n_150',
            'link_speed' : 150
        },
        {
            'type_name' : '802.11n_300',
            'link_speed' : 300
        },
        {
            'type_name' : '802.11n_450',
            'link_speed' : 450
        },
        {
            'type_name' : '802.11ac_433',
            'link_speed' : 433
        },
        {
            'type_name' : '802.11ac_866',
            'link_speed' : 866
        },
        {
            'type_name' : '802.11ac_1300',
            'link_speed' : 1300
        },
        {
            'type_name' : '802.11ac_1733',
            'link_speed' : 1733
        },
        {
            'type_name' : '802.11ac_2600',
            'link_speed' : 2600
        },
        {
            'type_name' : '802.11ac_3467',
            'link_speed' : 3467
        },
        {
            'type_name' : '802.11ac_6933',
            'link_speed' : 6933
        },
        {
            'type_name' : '802.11ax_*',
            'link_speed' : 0
        }
    ]
    session = Session()
    try:
        session.query(Server).delete()
        session.query(Specification).delete()
        session.query(NicType).delete()
        session.query(Os).delete()
        session.query(Application).delete()

        for e in os_types:
            os_type = Os(os_type=e['os_type'], os_version=e['os_version'])
            session.add(os_type)

        for e in nic_types:
            nic_type = NicType(type_name=e['type_name'], link_speed=e['link_speed'])
            session.add(nic_type)

        for sv in servers:
            common = sv["common"]
            spec = sv["spec"]
            server = Server(ip=common['ip'], hostname=common['hostname'], rolename=common['rolename'], type_cd=common['type_cd'], group_cd=common['group_cd'], region=common['region'], zone=common['zone'], description=common['description'])
            session.add(server)
            t_server = session.query(Server).filter_by(hostname=common['hostname']).first()
            t_os = session.query(Os).filter_by(os_version=spec['os_id']).first()
            spec = Specification(server_id=t_server.id, os_id=t_os.id, cpu_core=spec['cpu_core'], memory=spec['memory'], swap=spec['swap'], system_storage=spec['system_storage'], data_storage_1=spec['data_storage_1'], data_storage_2=spec['data_storage_2'], data_storage_3=spec['data_storage_3'], data_storage_4=spec['data_storage_4'], nic_type_1=spec['nic_type_1'], nic_type_2=spec['nic_type_2'], nic_type_3=spec['nic_type_3'], nic_type_4=spec['nic_type_4'], ext_device_1=spec['ext_device_1'], ext_device_2=spec['ext_device_2'], ext_device_3=spec['ext_device_3'], ext_device_4=spec['ext_device_4'])
            session.add(spec)
            for app in sv["app"]:
                t_app = Application(server_id=t_server.id, application_name=app['name'], application_desc=app['desc'], note=app['note'])
                session.add(t_app)
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    assert True
