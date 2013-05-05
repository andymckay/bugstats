import json
import logging

from flask import Flask

from get_stats import get_stats


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


@app.route('/data.json')
def data():
    return json.dumps(get_stats(), sort_keys=False)


if __name__ == '__main__':
    app.run()
