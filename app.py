#!/usr/bin/env python3

import os
import random
import string
import uuid
from datetime import datetime
from functools import lru_cache
from http import HTTPStatus

from flask import Flask, abort, make_response, render_template, request
from werkzeug.http import http_date

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)


RESPONSE_CODES = [
    HTTPStatus.OK,
    HTTPStatus.CREATED,
    HTTPStatus.ACCEPTED,
    # HTTPStatus.NO_CONTENT,  # TODO: is there indeed no content?
    HTTPStatus.IM_USED,
    HTTPStatus.NOT_MODIFIED,
]


class Page:
    def __init__(self, url, next_url=None, status=HTTPStatus.OK):
        self.url = url
        self.next_url = next_url
        self.status = status


class Session:
    def __init__(self, session_id):
        self.session_id = session_id
        self.pages = {}
        self.pages_ordered = []
        url = "/"
        for i in range(app.config.get("NUM_URLS") + 1):
            next_url = generate_random_url(session_id, i + 1)
            self.pages[url] = Page(url, next_url=next_url, status=get_random_status(session_id, i))
            self.pages_ordered.append(self.pages[url])
            url = next_url



@lru_cache(app.config.get("NUM_SESSIONS"))
def get_session(session_id):
    return Session(session_id)


def generate_random_url(session_id, i):
    if i > app.config.get("NUM_URLS"):
        return None  # last page doesn't point anywhere
    if app.debug and session_id == 'test-session':
        return f'page_{i}.html'
    return ''.join(random.choices(string.ascii_lowercase, k=app.config.get("RANDOM_URL_LENGTH"))) + ".html"


def get_random_status(session_id, i):
    if i == 1:  # just so the first random page will return 200
        return HTTPStatus.OK
    return random.choice(RESPONSE_CODES)


def generate_new_session_id():
    return str(uuid.uuid4())


def get_response(url, status=HTTPStatus.OK):
    now = http_date(datetime.utcnow())
    return make_response(render_template(url, now=now), status)


@app.route("/")
def index():
    session = get_session(generate_new_session_id())
    now = http_date(datetime.utcnow())
    response = get_response('index.html')
    response.headers[app.config.get("NEXT_URL_HEADER")] = session.pages["/"].next_url
    response.headers[app.config.get("NEW_SESSION_ID_HEADER")] = session.session_id
    return response


def random_url_get(page, is_last):
    if is_last:
        response = get_response('random_url_last.html', page.status)
    else:
        response = get_response('random_url_middle.html', page.status)
        response.headers[app.config.get("NEXT_URL_HEADER")] = page.next_url
    return response


def random_url_post(session, is_last):
    if not is_last:
        return '', HTTPStatus.METHOD_NOT_ALLOWED
    expected_data = ','.join(f'{p.status.value}' for p in session.pages_ordered[1:])
    if request.data != expected_data.encode('utf-8'):
        return '', HTTPStatus.BAD_REQUEST
    return get_response('random_url_last_post.html')


@app.route("/<path>", methods=['GET', 'POST'])
def random_url(path):
    session_id = request.args.get('session-id')
    session = get_session(session_id)
    if path not in session.pages:
        print(path)
        abort(404)
    page = session.pages[path]
    is_last = page.next_url is None
    if request.method == 'GET':
        return random_url_get(page, is_last)
    else:
        return random_url_post(session, is_last)
