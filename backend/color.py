from PIL import Image
import os
import numpy as np
import json
import collections
import colorsys
import time

basedir = os.path.abspath(os.path.dirname(__file__))
imgs = os.listdir(os.path.join(basedir, 'static', 'imgs'))
color = {}

for idx, filename in enumerate(imgs):
    img = Image.open(os.path.join(basedir, 'static', 'imgs', filename))
    img.thumbnail((200, 200))
    h, w = img.size
    limit = h * w // 100 # 1%
    img = np.array(img).reshape((h*w, 3))
    hsv = np.array([colorsys.rgb_to_hsv(*x) for x in img/255])
    hist, bins = np.histogram(hsv[:,0], bins=np.arange(256)/255)
    p0 = []
    for i in range(255):
        if hist[i-1] <= hist[i] and hist[i] >= hist[(i+1)%255]:
            p0.append(i)
    p1 = []
    for i in range(len(p0)):
        if hist[p0[i-1]] <= hist[p0[i]] and hist[p0[i]] >= hist[p0[(i+1)%len(p0)]] and hist[p0[i]] > limit:
            p1.append(p0[i])
    tmp = []
    while len(tmp) != len(p1) and len(p1) != 1:
        tmp = []
        for i in range(len(p1)):
            if (p1[i] + 255 - p1[i-1]) % 255 <= 20 and hist[p1[i]] <= hist[p1[i-1]]:
                pass
            elif (p1[(i+1)%len(p1)] + 255 - p1[i]) % 255 <= 20 and hist[p1[i]] <= hist[p1[(i+1)%len(p1)]]:
                pass
            else:
                tmp.append(p1[i])
        p1, tmp = tmp, p1
    print(idx, [hist[x] for x in p1])
    color[filename] = np.array([np.append( np.mean( hsv[np.logical_and(bins[x] <= hsv[:, 0], hsv[:, 0] < bins[x+1]), :], axis=0 ), hist[x] / h / w) for x in p1])

np.save('static/color.npy', color)
