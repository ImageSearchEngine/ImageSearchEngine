#! /usr/bin/env python3

from flask import Flask, request, Response, jsonify
from flask.logging import create_logger
from urllib.parse import quote, unquote, urlencode
import requests
import json
import os
import random
import string
from cbirCore.cbirSystem import CBIRSystem
from cbirCore.image import Image
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
log = create_logger(app)


def generateImageName():
    return ''.join(random.sample(string.ascii_letters + string.digits, 10))+'.png'


@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    print(data)
    # log.info(color)
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


@app.route('/api/upload', methods=['POST'])
def upload():
    img = request.files.get('image')
    # log.info(request.files)
    imgName = generateImageName()
    file_path = f"{basedir}/static/imgs/{imgName}"
    img.save(file_path)
    ret = {
        'id': imgName[:-4]
    }
    log.info(f"upload image :{imgName}")
    return jsonify(ret)


@app.route('/api/geturl', methods=['POST'])
def geturl():
    ret = {
        'imgURL': 'http://file.c-4.me/jpg/1.jpg',
    }
    log.info(f"get urls")
    return jsonify(ret)


if __name__ == '__main__':

    if not os.path.exists(os.path.join(basedir, 'static', 'imgs')):
        os.makedirs(os.path.join(basedir, 'static', 'imgs'))
    # development
    app.run(host='0.0.0.0', port=8388, debug=True)

    # production
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8388)
