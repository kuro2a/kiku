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

def test_insert_search_cpu_log(init_document):
    doc = DocumentUtility.get_document()
    doc.addCpuLog(datetime.now()-timedelta(minutes=15), "iris", "web/ap", "front", 0.05)
    doc.addCpuLog(datetime.now()-timedelta(minutes=14), "iris", "web/ap", "front", 0.27)
    doc.addCpuLog(datetime.now()-timedelta(minutes=13), "iris", "web/ap", "front", 0.42)
    doc.addCpuLog(datetime.now()-timedelta(minutes=12), "iris", "web/ap", "front", 0.21)
    doc.addCpuLog(datetime.now()-timedelta(minutes=11), "iris", "web/ap", "front", 0.11)
    doc.addCpuLog(datetime.now()-timedelta(minutes=10), "iris", "web/ap", "front", 0.86)
    doc.addCpuLog(datetime.now()-timedelta(minutes=9),  "iris", "web/ap", "front", 0.33)
    doc.addCpuLog(datetime.now()-timedelta(minutes=8),  "iris", "web/ap", "front", 0.48)
    doc.addCpuLog(datetime.now()-timedelta(minutes=7),  "iris", "web/ap", "front", 0.34)
    doc.addCpuLog(datetime.now()-timedelta(minutes=6),  "iris", "web/ap", "front", 0.01)
    doc.addCpuLog(datetime.now()-timedelta(minutes=5),  "iris", "web/ap", "front", 0.23)
    doc.addCpuLog(datetime.now()-timedelta(minutes=4),  "iris", "web/ap", "front", 0.11)
    doc.addCpuLog(datetime.now()-timedelta(minutes=3),  "iris", "web/ap", "front", 0.91)
    doc.addCpuLog(datetime.now()-timedelta(minutes=2),  "iris", "web/ap", "front", 0.42)
    doc.addCpuLog(datetime.now()-timedelta(minutes=1),  "iris", "web/ap", "front", 0.65)
    res = doc.searchCpuLog("iris", datetime.now()-timedelta(minutes=3), datetime.now())
    print(res)

    assert True


def test_insert_search_memory_log(init_document):
    doc = DocumentUtility.get_document()
    doc.addMemoryLog(datetime.now()-timedelta(minutes=15), "iris", "web/ap", "front", 0.33)
    doc.addMemoryLog(datetime.now()-timedelta(minutes=14), "iris", "web/ap", "front", 0.55)
    doc.addMemoryLog(datetime.now()-timedelta(minutes=13), "iris", "web/ap", "front", 0.63)
    doc.addMemoryLog(datetime.now()-timedelta(minutes=12), "iris", "web/ap", "front", 0.64)
    doc.addMemoryLog(datetime.now()-timedelta(minutes=11), "iris", "web/ap", "front", 0.65)
    doc.addMemoryLog(datetime.now()-timedelta(minutes=10), "iris", "web/ap", "front", 0.66)
    doc.addMemoryLog(datetime.now()-timedelta(minutes=9),  "iris", "web/ap", "front", 0.67)
    doc.addMemoryLog(datetime.now()-timedelta(minutes=8),  "iris", "web/ap", "front", 0.22)
    doc.addMemoryLog(datetime.now()-timedelta(minutes=7),  "iris", "web/ap", "front", 0.24)
    doc.addMemoryLog(datetime.now()-timedelta(minutes=6),  "iris", "web/ap", "front", 0.24)
    doc.addMemoryLog(datetime.now()-timedelta(minutes=5),  "iris", "web/ap", "front", 0.24)
    doc.addMemoryLog(datetime.now()-timedelta(minutes=4),  "iris", "web/ap", "front", 0.24)
    doc.addMemoryLog(datetime.now()-timedelta(minutes=3),  "iris", "web/ap", "front", 0.33)
    doc.addMemoryLog(datetime.now()-timedelta(minutes=2),  "iris", "web/ap", "front", 0.34)
    doc.addMemoryLog(datetime.now()-timedelta(minutes=1),  "iris", "web/ap", "front", 0.33)
    res = doc.searchMemoryLog("iris", datetime.now()-timedelta(minutes=3), datetime.now())
    print(res)

    assert True

def test_insert_search_swap_log(init_document):
    doc = DocumentUtility.get_document()
    doc.addSwapLog(datetime.now()-timedelta(minutes=15), "iris", "web/ap", "front", 0.0)
    doc.addSwapLog(datetime.now()-timedelta(minutes=14), "iris", "web/ap", "front", 0.0)
    doc.addSwapLog(datetime.now()-timedelta(minutes=13), "iris", "web/ap", "front", 0.0)
    doc.addSwapLog(datetime.now()-timedelta(minutes=12), "iris", "web/ap", "front", 0.0)
    doc.addSwapLog(datetime.now()-timedelta(minutes=11), "iris", "web/ap", "front", 0.0)
    doc.addSwapLog(datetime.now()-timedelta(minutes=10), "iris", "web/ap", "front", 0.0)
    doc.addSwapLog(datetime.now()-timedelta(minutes=9),  "iris", "web/ap", "front", 0.0)
    doc.addSwapLog(datetime.now()-timedelta(minutes=8),  "iris", "web/ap", "front", 0.1)
    doc.addSwapLog(datetime.now()-timedelta(minutes=7),  "iris", "web/ap", "front", 0.1)
    doc.addSwapLog(datetime.now()-timedelta(minutes=6),  "iris", "web/ap", "front", 0.1)
    doc.addSwapLog(datetime.now()-timedelta(minutes=5),  "iris", "web/ap", "front", 0.1)
    doc.addSwapLog(datetime.now()-timedelta(minutes=4),  "iris", "web/ap", "front", 0.1)
    doc.addSwapLog(datetime.now()-timedelta(minutes=3),  "iris", "web/ap", "front", 0.1)
    doc.addSwapLog(datetime.now()-timedelta(minutes=2),  "iris", "web/ap", "front", 0.2)
    doc.addSwapLog(datetime.now()-timedelta(minutes=1),  "iris", "web/ap", "front", 0.2)
    res = doc.searchSwapLog("iris", datetime.now()-timedelta(minutes=3), datetime.now())
    print(res)

    assert True

