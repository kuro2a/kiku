#!/usr/bin/python3

import sys
import pathlib
from datetime import datetime, timedelta
import bcrypt
import pytest

sys.path.append( str(pathlib.Path(__file__).resolve().parent) + '/../' )

from lib.const import ConfigKey
from lib.utility import SystemUtility, DocumentUtility

@pytest.fixture()
def init_document():
    conf = dict(SystemUtility.get_config())
    SystemUtility.get_system_log(conf[ConfigKey.CONF_KEY_SYSTEM])
    SystemUtility.get_access_log(conf[ConfigKey.CONF_KEY_SYSTEM])
    DocumentUtility.get_document(conf[ConfigKey.CONF_KEY_SYSTEM])

def test_insert_vmstat_log(init_document):
    doc = DocumentUtility.get_document()
    now = datetime.now()
    doc.addVmstatLog(now-timedelta(minutes=5), 'iris', 'web/ap', 'front', 0.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.3, 0.0, 0, 0, 0, 0)
    doc.addVmstatLog(now-timedelta(minutes=4), 'iris', 'web/ap', 'front', 0.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.3, 0.0, 0, 0, 0, 0)
    doc.addVmstatLog(now-timedelta(minutes=3), 'iris', 'web/ap', 'front', 0.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.3, 0.0, 0, 0, 0, 0)
    doc.addVmstatLog(now-timedelta(minutes=2), 'iris', 'web/ap', 'front', 0.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.3, 0.0, 0, 0, 0, 0)
    doc.addVmstatLog(now-timedelta(minutes=1), 'iris', 'web/ap', 'front', 0.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.3, 0.0, 0, 0, 0, 0)
    doc.addVmstatLog(now, 'iris', 'web/ap', 'front', 0.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.3, 0.0, 0, 0, 0, 0)
    res = doc.searchCpuLog("iris", now-timedelta(minutes=3), now)
    print(res)

    assert True
