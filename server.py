#!/usr/bin/env python
import json
import logging

from flask import Flask, Response

from lib.get_stats import get_stats
from lib.get_bugs import get_bugs
from lib.get_prs import get_prs


app = Flask(__name__)
app.debug = True


@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


@app.route('/')
def index():
    with open('templates/index.html') as f:
        return f.read()


@app.route('/stats.json')
def stats():
    return Response(response=json.dumps(get_stats(), sort_keys=False),
                    status=200, mimetype="application/json")


@app.route('/bugs.json')
def bugs():
    return Response(response=json.dumps(get_bugs(), sort_keys=False),
                    status=200, mimetype="application/json")


@app.route('/prs.json')
def prs():
    return Response(response=json.dumps(get_prs(), sort_keys=False),
                    status=200, mimetype="application/json")


if __name__ == '__main__':
    app.run(port=5678)
