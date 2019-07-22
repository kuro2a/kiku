#!/usr/bin/python3

import sys
import pathlib
from datetime import datetime
import pytest

from falcon import testing

sys.path.append( str(pathlib.Path(__file__).resolve().parent) + '/../' )

import main


@pytest.fixture()
def client():
    return testing.TestClient(main.create_service())


def test_api_version(client):
    doc = {
        u'meta': {
            u'status': u'OK',
            u'message': u'OK',
            u'timestamp': datetime.now()
        }, u'data': None
    }

    result = client.simulate_get('/api/v1/version')
    assert result.json == doc
