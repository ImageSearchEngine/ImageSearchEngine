from PIL import Image
import os
import numpy as np
import json
import collections
import colorsys
import time
from math import pi, cos, sin

from queue import Queue
from threading import Thread, Lock

class TaskQueue(Queue):
    def __init__(self, num_workers=1):
        Queue.__init__(self)
        self.num_workers = num_workers
        self.start_workers()

    def start_workers(self):
        for _ in range(self.num_workers):
            t = Thread(target=self.do_task)
            t.daemon = True
            t.start()

    def add_task(self, func, *args, **kwargs):
        args = args or ()
        kwargs = kwargs or {}
        self.put((func, args, kwargs))

    def do_task(self):
        while True:
            func, args, kwargs = self.get()
            func(*args, **kwargs)
            self.task_done()

q = TaskQueue(num_workers=10)

basedir = os.path.abspath(os.path.dirname(__file__))
imgs = os.listdir(os.path.join(basedir, 'static', 'imgs'))
color = {}


def hsv_xyz(a):
    return np.array([a[1]*a[2]*cos(a[0]*2*pi), a[1]*a[2]*sin(a[0]*2*pi), 1-a[2]])


def hsv_dis(a, b):
    return np.sqrt(np.sum((hsv_xyz(a) - hsv_xyz(b)) ** 2))


def dis(a, b):
    return np.sqrt(np.sum((a-b) ** 2))


def getcolor(idx, filename, color, lock):
    global basedir
    img = Image.open(os.path.join(basedir, 'static', 'imgs', filename))
    img.thumbnail((200, 200))
    h, w = img.size
    limit = h * w // 200 # 0.5%
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
    print(idx, filename, [hist[x] for x in p1])
    
    rst = [np.mean( hsv[np.logical_and(bins[x] <= hsv[:, 0], hsv[:, 0] < bins[x+1]), :], axis=0 ) for x in p1]
    tmp = list(map(hsv_xyz, rst))
    cnt = np.zeros((len(rst)))

    for x in hsv:
        min_dis, min_idx = 9, 0
        _x = hsv_xyz(x)
        for idx, _y in enumerate(tmp):
            _dis = dis(_x, _y)
            if _dis < min_dis:
                min_dis, min_idx = _dis, idx
        cnt[min_idx] += 1

    lock.acquire()
    color[filename] = np.array([np.append( rst[x], cnt[x] / h / w) for x in range(len(rst))])
    lock.release()


if __name__ == '__main__':
    lock = Lock()

    for idx, filename in enumerate(imgs):
        q.add_task(getcolor, idx, filename, color, lock)

    q.join()
    print('Task all done')
    print(color)
    np.save('static/color.npy', color)
