#!/usr/bin/python3

import signal
import os
import sys
import falcon
import json
import paramiko
from datetime import datetime, timedelta
from threading import Thread

from lib.const import Const, Message, ConfigKey
from lib.utility import SystemUtility, SessionUtility, DocumentUtility
from lib.database import Base, engine, Session, Server, Specification

system_config = None
system_logger = None
document = None

SSH_PRIVATE_KEY = "/Users/kuro2/.ssh/id_rsa_ansible"


def signal_handler(signum, frame):
    return_val = 0
    if signum == signal.SIGTERM or signum == signal.SIGINT:
        return_val = 0
    else:
        return_val = 1
    system_logger.info("[END] Caught the signal: Signal({0})".format(signum))
    sys.exit(return_val)


def init():
    global system_config, system_logger, document
    # Init configure.
    system_config = dict(SystemUtility.get_config())  # Avoid pylint error.
    # Init logger.
    system_logger = SystemUtility.get_system_log(
        system_config[ConfigKey.CONF_KEY_SYSTEM])
    # Init database.
    Base.metadata.create_all(bind=engine)
    # Init document.
    document = DocumentUtility.get_document(
        system_config[ConfigKey.CONF_KEY_SYSTEM])
    system_logger.info(system_config)


def insert_os_log(session, document, server, now):
    print("data:", server.hostname)
    spec = session.query(Specification).filter(
        Specification.server_id == server.id).first()
    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    pkey = paramiko.RSAKey.from_private_key(
        open(SSH_PRIVATE_KEY, "r"))
    try:
        client.connect(server.ip, port=2222, username='ansible', pkey=pkey)
        s_in, s_out, s_err = client.exec_command('vmstat 1 2')
        res = dict(map(lambda x: (x[0], int(x[2])), zip(
            *map(str.split, s_out.read().decode('utf8').split("\n")[-4:-1]))))
        document.addVmstatLog(now, server.hostname, server.type_cd, server.group_cd, 100.0 - res["id"],
                          res["us"], res["sy"], res["id"], res["wa"], res["st"], 100.0 - 100.0 *
                          (res["free"] + res["buff"] +
                           res["cache"]) / spec.memory,
                          100.0 * res["free"] / spec.memory,
                          100.0 * res["buff"] / spec.memory,
                          100.0 * res["cache"] / spec.memory,
                          100.0 * res["swpd"] / spec.swap,
                          res["si"], res["so"], res["bi"], res["bo"])
        s_in, s_out, s_err = client.exec_command('df -Tl -x tmpfs -x squashfs -x devtmpfs')
        res = s_out.read().decode('utf8').split("\n")[:-1]
        for i in range(1, len(res)):
            row = dict(map(lambda x: (x[0], x[i]), zip(*map(str.split, res))))
            document.addDfLog(now, server.hostname, server.type_cd, server.group_cd, row['Filesystem'], row['Type'], int(row['1K-blocks']), int(row['Used']), int(row['Available']), float(row['Use%'].replace('%','')), row['Mounted'], option=None)
    except Exception as e:
        raise e
    finally:
        client.close()


def main():
    global system_config, system_logger
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    init()
    system_logger.info('[START] Collector started.')

    threads = []
    now = datetime.now()
    session = Session()
    try:
        servers = session.query(Server).all()
        for server in servers:
            thread = Thread(target=insert_os_log, args=(
                session, document, server, now))
            thread.setDaemon(True)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    system_logger.info('[END] Collector end.')


if __name__ == '__main__':
    main()
