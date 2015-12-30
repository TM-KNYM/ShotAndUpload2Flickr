# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import math


def load_image(fp):
    return Image.open(fp)

def create_blank_image(w, h):
    return np.zeros((h, w, 3), np.uint8)

class FisheyeCorrectionCommand():

    def __init__(self):
        self._x = 0
        self._y = 0
        self._r = 0

    def setPos(self, x, y):
        self._x = x
        self._y = y

    def setRadius(self, r):
        self._r = r

    def canExecute(self):
        x = self._x  # x pos
        y = self._y  # y pos
        r = self._r
        return (r*r) > (x*x)+(y*y)

    def execute(self):
        x = self._x   # x pos
        y = self._y  # y pos
        r = self._r  # raidus
        a = 350  # Ellipse long side (summit)
        b = 132  # Ellipse short side (base)
        # slope of vertex
        M = math.sqrt(r*r - (x*x + y*y))/math.sqrt(x*x + y*y)
        sx = 0
        sx = math.sqrt((a*a*b*b)/(b*b+a*a*M*M))
        sy = sx*M
        sx = x * sx / math.sqrt((x*x) + (y*y))
        sy = y * sy / math.sqrt((r*r) - ((x*x) + (y*y)))
        return (int(round(sx)), int(round(sy)))


def createCo2PxFunc(width, height):
    w = width
    h = height

    def co2px(x, y):
        cvt_x = x + int(w/2)-1  # translate co ->px
        cvt_y = int(h/2) - y-1
        return (cvt_x, cvt_y)
    return co2px


def createPx2CoFunc(center_x, center_y):
    cx = center_x
    cy = center_y

    def px2coordinate(x, y):
        cvt_x = x - cx
        cvt_y = -1*(y-cy)
        return (cvt_x, cvt_y)
    return px2coordinate


class cmd_executor():

    def __init__(self, r, px2co):
        self.px2co = px2co
        self.cmd = FisheyeCorrectionCommand()
        self.cmd.setRadius(r)
        self.tmp_list = []
        self.center_x = center_x
        self.center_y = center_y
        print('cmd init')

    def execute(self, pos):
        x = pos[0]
        y = pos[1]
        cx, cy = self.px2co(x, y)
        cmd = self.cmd
        cmd.setPos(cx, cy)
        if cmd.canExecute() is True:
            new_point = cmd.execute()
            return {'srcX': int(x), 'srcY': int(y), 'dst_x': int(new_point[0]), 'dst_y': int(new_point[1])}
        else:
            return None

if __name__ == '__main__':
    # fp = '360.jpg'
    fp = 'sample.jpg'
    im = load_image(fp)
    rim = im.resize((701, 701))
    dat = np.asarray(rim, dtype=np.uint8)
    print(dat.shape)
    shape = dat.shape
    org_w, org_h, clr = shape

    # convert
    r = org_w/2.0
    center_x = r
    center_y = r
    px2co = createPx2CoFunc(center_x, center_y)
    exe = cmd_executor(r, px2co)
    px_list = list(filter(lambda val: (val is not None), [exe.execute((x, y)) for x in range(0, org_w) for y in range(0, org_h)]))
    x_list = [px['dst_x'] for px in px_list]
    y_list = [py['dst_y'] for py in px_list]

    # calc width & height
    w = max(x_list) - min(x_list)
    h = max(y_list) - min(y_list)
    print(str(w) + ' :: ' + str(h))
    bImg = create_blank_image(w, h)
    pxEnableMap = np.zeros((h, w), dtype=bool)
    co2px = createCo2PxFunc(w, h)
    for px in px_list:
        dstX, dstY = co2px(px['dst_x'], px['dst_y'])
        bImg[dstY][dstX] = dat[px['srcY']][px['srcX']]
        pxEnableMap[dstY][dstX] = True
    for y in range(0, h-1):
        tmpColor = None
        for x in range(0, w-1):
            if pxEnableMap[y][x] == True:
                tmpColor = bImg[y][x]
            elif tmpColor is not None:
                bImg[y][x] = tmpColor

    '''
    from queue import Queue
    q = Queue()

    def worker():
        while True:
            y = q.get()
            oneLineProcess(y)
            q.task_done()
    import threading
    for i in range(2):
        t = threading.Thread(target=worker)
        t.deamon = True
        t.start()
    tmp_cl = [0, 0, 0]
    for y in range(0, h):
        q.put(y)
    q.join()
    '''

    out = Image.fromarray(np.uint8(bImg))
    out.save('test.jpg', 'JPEG')
    # import scipy as sp
    # import scipy.misc
    # sp.misc.imsave('test.jpg', bImg)

    print('comp')
