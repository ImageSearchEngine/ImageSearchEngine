import os
from PIL import Image

basedir = os.path.abspath(os.path.dirname(__file__))
imgs = os.listdir(os.path.join(basedir, 'static', 'imgs', 'origin'))

for filename in imgs:
    img = Image.open(os.path.join(basedir, 'static', 'imgs', 'origin', filename))
    img.thumbnail((200, 200))
    img.save(os.path.join(basedir, 'static', 'imgs', 'small', filename), 'JPEG')
