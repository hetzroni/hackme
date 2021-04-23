#!/usr/bin/env python3

import os
import random
import string
import uuid
from datetime import datetime
from functools import lru_cache

from flask import Flask, abort, make_response, render_template, request
from werkzeug.http import http_date

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)


class Page:
    def __init__(self, url, next_url=None):
        self.url = url
        self.next_url = next_url


class Session:
    def __init__(self, session_id):
        self.session_id = session_id
        self.pages = {}
        url = "/"
        for i in range(app.config.get("NUM_URLS")):
            next_url = generate_random_url()
            self.pages[url] = Page(url, next_url)
            url = next_url
        self.pages[url] = Page(url)  # add the last page



@lru_cache(app.config.get("NUM_SESSIONS"))
def get_session(session_id):
    return Session(session_id)


def generate_random_url():
    return ''.join(random.choices(string.ascii_lowercase, k=app.config.get("RANDOM_URL_LENGTH"))) + ".html"


def generate_new_session_id():
    return str(uuid.uuid4())


def get_response(url):
    now = http_date(datetime.utcnow())
    return make_response(render_template(url, now=now))


@app.route("/")
def index():
    session = get_session(generate_new_session_id())
    now = http_date(datetime.utcnow())
    response = get_response('index.html')
    response.headers[app.config.get("NEXT_URL_HEADER")] = session.pages["/"].next_url
    response.headers[app.config.get("NEW_SESSION_ID_HEADER")] = session.session_id
    return response


@app.route("/<path>")
def random_url(path):
    session_id = request.args.get('session-id')
    session = get_session(session_id)
    if path not in session.pages:
        print(path)
        abort(404)
    page = session.pages[path]
    is_last = page.next_url is None
    if is_last:
        response = get_response('random_url_last.html')
    else:
        response = get_response('random_url_middle.html')
        response.headers[app.config.get("NEXT_URL_HEADER")] = page.next_url
    return response
