from http import HTTPStatus

import pytest

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test that '/' gives the proper headers."""

    rv = client.get('/')
    assert rv.headers[app.config['NEXT_URL_HEADER']].endswith('.html')
    assert len(rv.headers[app.config['NEW_SESSION_ID_HEADER']]) > 0

def test_stage1(client):
    rv = client.get('/')
    next_url = rv.headers[app.config['NEXT_URL_HEADER']]
    session_id = rv.headers[app.config['NEW_SESSION_ID_HEADER']]
    num_pages = 0
    while next_url is not None:
        num_pages += 1
        rv = client.get(next_url, query_string={'session-id': session_id})
        next_url = rv.headers.get(app.config['NEXT_URL_HEADER'])
    assert num_pages == app.config['NUM_URLS']

def test_stage2(client):
    status_codes = []
    rv = client.post(f'page_{app.config["NUM_URLS"]}.html?session-id=test-session', data='hello')
    assert rv.status_code == HTTPStatus.BAD_REQUEST
    for i in range(1, app.config['NUM_URLS'] + 1):
        rv = client.get(f'page_{i}.html?session-id=test-session')
        status_codes.append(rv.status_code)
    assert status_codes[0] == HTTPStatus.OK
    rv = client.post(f'page_{i}.html?session-id=test-session', data=','.join(map(str, status_codes)))
    assert rv.status_code == HTTPStatus.OK
