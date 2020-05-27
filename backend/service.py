#! /usr/bin/env python3

from flask import Flask, request, Response, jsonify, current_app, make_response, abort
from flask.logging import create_logger
from urllib.parse import quote, unquote, urlencode
import requests
import json
import os
import io
import random
import string
import imghdr
from PIL import Image
from cbirCore.cbirSystem import CBIRSystem
from cbirCore.image import Image as CBIRImage
import config
basedir = os.path.abspath(os.path.dirname(__file__))
import numpy as np
import colorsys

# the first run
# if not os.path.exists(os.path.join(basedir, 'static', 'imgs')):
#     os.makedirs(os.path.join(basedir, 'static', 'imgs'))
# if not os.path.exists(os.path.join(basedir, 'static', 'uploads')):
#     os.makedirs(os.path.join(basedir, 'static', 'uploads'))
# print(f"dir init completed")

app = Flask(__name__)
app.config.from_object(config)
core = CBIRSystem()
color = np.load('static/color.npy').item()
colorRate = {}
imgs = os.listdir(os.path.join(basedir, 'static', 'imgs'))


ALLOWED_EXTENSIONS = set(['png', 'jpg'])


def allowedImageExt(imgName):
    return '.' in imgName and imgName.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generateImageName():
    return ''.join(random.sample(string.ascii_letters + string.digits, 10))


def filterSize(filename):
    size = max(Image.open(os.path.join(basedir, 'static', 'imgs', filename)).size)
    if size < 2000:
        return 'small'
    elif size < 3000:
        return 'medium'
    else:
        return 'large'


def filterColor(filename, colorHex):
    r = int(colorHex[1:3], 16) / 255
    g = int(colorHex[3:5], 16) / 255
    b = int(colorHex[5:7], 16) / 255
    c = np.array(colorsys.rgb_to_hsv(r, g, b))
    for x in color[filename]:
        # print(filename, np.sum((x[:3] - c) ** 2))
        if np.sum((x[:3] - c) ** 2) < 0.05:
            colorRate[filename] = x[3]
            return True
    return False


def getColorRate(filename):
    return colorRate[filename]


@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    page = int(data['page']) if 'page' in data else 0
    num = int(data['num']) if 'num' in data else app.config['DEFAULT_PAGESIZE']
    # TODO check if all is legal
    if 'img' in data:
        retImg = [x.ID for x in core.retrieve_image(CBIRImage(os.path.join(basedir, 'static', 'uploads', data['img'])))]
    else:
        retImg = imgs

    if 'size' in data:
        retImg = list(filter(lambda x: filterSize(x) == data['size'], retImg))

    if 'color' in data:
        retImg = list(filter(lambda x: filterColor(x, data['color']), retImg))
        if 'img' not in data:
            retImg.sort(key=getColorRate, reverse=True)
            # print([colorRate[x] for x in retImg[:10]])
    
    ret = {
        'code': '0',
        'msg': '',
        'total': len(retImg),
        'page': page,
        'num': min(num, len(retImg)-page*num),
        'imgs': retImg[page*num: min((page+1)*num, len(retImg))]
    }
    return jsonify(ret)


@app.route('/api/relate', methods=['POST'])
def relate():
    data = request.get_json()
    num = int(data['num']) if 'num' in data else app.config['DEFAULT_PAGESIZE']
    # TODO check if all is legal
    if 'img' not in data:
        return jsonify({'code': '1', 'msg': 'param[img] is None'})
    retImg = core.retrieve_image(CBIRImage(os.path.join(basedir, 'static', 'imgs', data['img'])), num)
    ret = {
        'code': '0',
        'msg': '',
        'num': len(retImg),
        'imgs': [x.ID for x in retImg]
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
        'img': imgName
    }
    return jsonify(ret)


@app.route('/img/<string:filename>', methods=['GET'])
def getImg(filename):
    path = os.path.join(basedir, 'static', 'imgs', filename)
    if filename is None or filename.isalnum() == False or os.path.exists(path) == False or imghdr.what(path) is None:
        return abort(404)
    else:
        img = Image.open(path)
        imgByteArr = io.BytesIO()
        if 's' in request.args:
            try:
                x = int(request.args['s'].split('y')[0])
                y = int(request.args['s'].split('y')[1])
                img.thumbnail((x, y))
            except:
                pass
        img.save(imgByteArr, imghdr.what(path))
        response = make_response(imgByteArr.getvalue())
        response.headers['Content-Type'] = f'image/{imghdr.what(path)}'
        return response


@app.route('/upload/<string:filename>', methods=['GET'])
def getUpload(filename):
    path = os.path.join(basedir, 'static', 'uploads', filename)
    if filename is None or filename.isalnum() == False or os.path.exists(path) == False or imghdr.what(path) is None:
        return abort(404)
    else:
        img = Image.open(path)
        imgByteArr = io.BytesIO()
        if 's' in request.args:
            try:
                x = int(request.args['s'].split('y')[0])
                y = int(request.args['s'].split('y')[1])
                img.thumbnail((x, y))
            except:
                pass
        img.save(imgByteArr, imghdr.what(path))
        response = make_response(imgByteArr.getvalue())
        response.headers['Content-Type'] = f'image/{imghdr.what(path)}'
        return response


def coreInit():
    core.load_checkpoint('static/pnasnet5large-finetune500.pth')
    core.load_data('static/')
    print(f"core init completed")


if __name__ == '__main__':

    # development
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        coreInit()
    app.run(host='0.0.0.0', port=8388, debug=True)

    # production
    # from waitress import serve
    # coreInit()
    # serve(app, host="0.0.0.0", port=8388)
