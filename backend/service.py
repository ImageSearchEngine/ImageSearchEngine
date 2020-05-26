#! /usr/bin/env python3

from flask import Flask, request, Response, jsonify, current_app, make_response, abort
from flask.logging import create_logger
from urllib.parse import quote, unquote, urlencode
import requests
import json
import os
import random
import string
import imghdr
# from cbirCore.cbirSystem import CBIRSystem
# from cbirCore.image import Image
import config
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(config)
# core = CBIRSystem()
imgs = []


ALLOWED_EXTENSIONS = set(['png', 'jpg'])
 
def allowedImageExt(imgName):
    return '.' in imgName and imgName.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generateImageName():
    return ''.join(random.sample(string.ascii_letters + string.digits, 10))


@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    page = data['page'] if 'page' in data else 0
    num = data['num'] if 'num' in data else app.config['DEFAULT_PAGESIZE']
    ret = {
        'code': '0',
        'msg': '',
        'total': len(imgs),
        'page': page,
        'num': min(num, len(imgs)-page*num),
        'imgs': imgs[page*num: min((page+1)*num, len(imgs))]
    }
    return jsonify(ret)


@app.route('/api/relate', methods=['POST'])
def relate():
    data = request.get_json()
    num = data['num'] if 'num' in data else app.config['DEFAULT_PAGESIZE']
    ret = {
        'code': '0',
        'msg': '',
        'num': min(num, len(imgs)),
        'imgs': imgs[: min(num, len(imgs))]
    }
    return jsonify(ret)


@app.route('/api/upload', methods=['POST'])
def upload():
    img = request.files.get('image')
    if img == None:
        return jsonify({'code': '1', 'msg': 'image is None'})
    if allowedImageExt(img.filename) == False:
        return jsonify({'code': '2', 'msg': 'image extension is not allowed'})
    imgName = generateImageName()
    filePath = os.path.join(basedir, 'static', 'uploads', imgName)
    img.save(filePath)
    current_app.logger.info(f"upload image: {imgName}")
    ret = {
        'code': '0',
        'msg': '',
        'id': imgName
    }
    return jsonify(ret)


@app.route('/thumbnail/<string:filename>', methods=['GET'])
def getThumbnail(filename):
    path = os.path.join(basedir, 'static', 'imgs', 'small', filename) 
    if filename is None or filename.isalnum() == False or os.path.exists(path) == False or imghdr.what(path) is None:
        return abort(404)
    else:
        try:
            img = open(path, "rb").read()
        except IOError:
            return abort(404)
        response = make_response(img)
        response.headers['Content-Type'] = f'image/{imghdr.what(path)}'
        return response


@app.route('/img/<string:filename>', methods=['GET'])
def getImg(filename):
    path = os.path.join(basedir, 'static', 'imgs', 'origin', filename) 
    if filename is None or filename.isalnum() == False or os.path.exists(path) == False or imghdr.what(path) is None:
        return abort(404)
    else:
        try:
            img = open(path, "rb").read()
        except IOError:
            return abort(404)
        response = make_response(img)
        response.headers['Content-Type'] = f'image/{imghdr.what(path)}'
        return response


@app.route('/upload/<string:filename>', methods=['GET'])
def getUpload(filename):
    path = os.path.join(basedir, 'static', 'uploads', filename) 
    if filename is None or filename.isalnum() == False or os.path.exists(path) == False or imghdr.what(path) is None:
        return abort(404)
    else:
        try:
            img = open(path, "rb").read()
        except IOError:
            return abort(404)
        response = make_response(img)
        response.headers['Content-Type'] = f'image/{imghdr.what(path)}'
        return response


def dirInit():
    if not os.path.exists(os.path.join(basedir, 'static', 'imgs', 'origin')):
        os.makedirs(os.path.join(basedir, 'static', 'imgs', 'origin'))
    if not os.path.exists(os.path.join(basedir, 'static', 'imgs', 'small')):
        os.makedirs(os.path.join(basedir, 'static', 'imgs', 'small'))
    if not os.path.exists(os.path.join(basedir, 'static', 'uploads')):
        os.makedirs(os.path.join(basedir, 'static', 'uploads'))
    print(f"dir init completed")


def init():
    global imgs
    imgs = os.listdir(os.path.join(basedir, 'static', 'imgs', 'origin'))
    print(f"init completed")


def coreInit():
    # for filename in imgs:
    #     print(f"core load image: {filename}")
    #     core.load_image(Image(os.path.join(basedir, 'static', 'imgs', 'origin', filename)))
    print(f"core init completed")


if __name__ == '__main__':

    # the first run
    # dirInit()

    init()

    # development
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        coreInit()
    app.run(host='0.0.0.0', port=8388, debug=True)

    # production
    # from waitress import serve
    # coreInit()
    # serve(app, host="0.0.0.0", port=8388)
