import os

from flask import Flask, make_response

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

@app.route("/")
def index():
    response = make_response('Welcome to Stage 1!<br>Sniff to find the next url.')
    response.headers[app.config.get("NEXT_URL_HEADER")] = '/start.html'
    return response
