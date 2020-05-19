#! /usr/bin/env python3

from flask import Flask, request, Response, jsonify
from urllib.parse import quote, unquote, urlencode
import requests
import json

app = Flask(__name__)


@app.route('/api/search', methods=['POST'])
def search():
    ret = {
        'total': 87,
        'page': 0,
        'pagesize': 20,
        'imgURLs': [
            'http://file.c-4.me/jpg/1.jpg',
        ]
    }
    return jsonify(ret)


@app.route('/api/relate', methods=['POST'])
def relate():
    ret = {
        'maxsize': 20,
        'imgURLs': [
            'http://file.c-4.me/jpg/1.jpg',
        ]
    }
    return jsonify(ret)


if __name__ == '__main__':

    # development
    app.run(host='0.0.0.0', port=8388, debug=True)

    # production
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8388)
