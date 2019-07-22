#!/usr/bin/python3

import sys
import pathlib
from datetime import datetime
import bcrypt
import pytest

sys.path.append( str(pathlib.Path(__file__).resolve().parent) + '/../' )

from lib.database import Base, engine, Session, User, Server, Specification, NicType, Os, Role

@pytest.fixture()
def init_db():
    Base.metadata.create_all(bind=engine)

def test_table_create_role_and_delete(init_db):
    role_list = [
        {
            "role_type": "admin"
        },
        {
            "role_type": "user"
        }
    ]

    try:
        session = Session()
        session.query(Role).delete()

        for e in role_list:
            role = Role(role_type=e['role_type'])
            session.add(role)
        
        role = session.query(Role).filter_by(role_type='user').first()
        print(role.role_type)
        session.delete(role)

        session.commit()
    except:
        session.rollback()
        assert False
    finally:
        session.close()

    assert True

def test_table_create_user_and_delete(init_db):
    salt = bcrypt.gensalt(rounds=10, prefix=b'2a')
    plain_password = 'testpassword'.encode('utf-8')
    hashed_password = bcrypt.hashpw(plain_password, salt)
    user = User(account='testuser', password=hashed_password.decode(), username='testuserfullname', nickname='testusernickname', role_id=0)
    session = Session()
    session.add(user)

    u = session.query(User).filter_by(account='testuser').first()
    print(u.account)
    session.delete(u)
    session.close()

    assert user.account == u.account
#    assert all(v == u[k] for k,v user.dict.items()) and len(u) == len(user.dict)

def test_table_create_server_and_delete(init_db):
    servers = [
        {
            'ip' : '192.168.12.1',
            'hostname' : 'lily',
            'rolename' : 'AP Server#1',
            'type_cd' : 'ap',
            'group_cd' : '1',
            'region' : 'east_japan',
            'zone' : 'rack_1',
            'description' : 'test_code'
#            'description' : ''
        },
        {
            'ip' : '192.168.12.2',
            'hostname' : 'rose',
            'rolename' : 'AP Server#2',
            'type_cd' : 'ap',
            'group_cd' : '1',
            'region' : 'east_japan',
            'zone' : 'rack_1',
            'description' : 'test_code'
#            'description' : ''
        },
        {
            'ip' : '192.168.12.3',
            'hostname' : 'iris',
            'rolename' : 'AP Server#3',
            'type_cd' : 'ap',
            'group_cd' : '1',
            'region' : 'east_japan',
            'zone' : 'rack_2',
            'description' : 'test_code'
#            'description' : ''
        }
    ]
    session = Session()
    for e in servers:
        server = Server(ip=e['ip'], hostname=e['hostname'], rolename=e['rolename'], type_cd=e['type_cd'], group_cd=e['group_cd'], region=e['region'], zone=e['zone'], description=e['description'])
        session.add(server)

    for e in session.query(Server).filter(Server.description == 'test_code'):
        session.delete(e)


#    session.commit()
    session.close()

    assert True


def test_table_create_specifcation_and_delete(init_db):
    specs = [
        {
            'server_id' : 1,
            'os_id': 1,
            'cpu_core' : 4,
            'memory' : 16 * 1024**3,
            'swap': 2 * 1024**3,
            'system_storage' : 50 * 1024**3,
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
        {
            'server_id' : 2,
            'os_id': 1,
            'cpu_core' : 4,
            'memory' : 8 * 1024**3,
            'swap': 2 * 1024**3,
            'system_storage' : 50 * 1024**3,
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
        {
            'server_id' : 3,
            'os_id': 1,
            'cpu_core' : 4,
            'memory' : 8 * 1024**3,
            'swap': 2 * 1024**3,
            'system_storage' : 50 * 1024**3,
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
        }
    ]
    session = Session()
    for e in specs:
        spec = Specification(server_id=e['server_id'], os_id=e['os_id'], cpu_core=e['cpu_core'], memory=e['memory'], swap=e['swap'], system_storage=e['system_storage'], data_storage_1=e['data_storage_1'], data_storage_2=e['data_storage_2'], data_storage_3=e['data_storage_3'], data_storage_4=e['data_storage_4'], nic_type_1=e['nic_type_1'], nic_type_2=e['nic_type_2'], nic_type_3=e['nic_type_3'], nic_type_4=e['nic_type_4'], ext_device_1=e['ext_device_1'], ext_device_2=e['ext_device_2'], ext_device_3=e['ext_device_3'], ext_device_4=e['ext_device_4'])
        session.add(spec)

    for e in session.query(Specification).all():
        print(e)
        session.delete(e)

#    session.commit()
    session.close()

    assert True


def test_table_create_nictype_and_delete(init_db):
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
    for e in nic_types:
        nic_type = NicType(type_name=e['type_name'], link_speed=e['link_speed'])
        session.add(nic_type)

    for e in session.query(NicType).all():
        print(e)
        session.delete(e)

#    session.commit()
    session.close()

    assert True

def test_table_create_os_and_delete(init_db):
    os_list = [
        {
            "os_type": "Windows",
            "os_version": "Windows 10"
        },
        {
            "os_type": "Windows",
            "os_version": "Windows Server 2016"
        },
        {
            "os_type": "Windows",
            "os_version": "Windows Server 2019"
        },
        {
            "os_type": "Linux",
            "os_version": "Ubuntu 18.04"
        },
        {
            "os_type": "Linux",
            "os_version": "CentOS 7"
        },
        {
            "os_type": "Linux",
            "os_version": "Ubuntu 8"
        }
    ]
    session = Session()
    for e in os_list:
        target_os = Os(os_type=e['os_type'], os_version=e['os_version'])
        session.add(target_os)

    for e in session.query(Os).all():
        print(e)
        session.delete(e)

#    session.commit()
    session.close()

    assert True


