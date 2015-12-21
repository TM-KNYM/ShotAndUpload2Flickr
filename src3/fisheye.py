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
        self._mag = 0
        self._r = 0
        self._L = 0

    def setPos(self, x, y):
        self._x = x
        self._y = y

    def setMag(self, mag):
        self._mag = mag

    def setRadius(self, r):
        self._r = r

    def setFocusLength(self, l):
        self._L = l

    def canExecute(self):
        x = self._x   # x pos
        y = self._y  # y pos
        r = self._r
        return (r*r) > (x*x)+(y*y)

    def execute(self):
        x = self._x   # x pos
        y = self._y  # y pos
        r = self._r  # raidus
        #L = 2*r
        #L = self._L
        a = 400
        b = 162
        #length = math.sqrt((y*y)/(1-(x*x)/(L*L)))
        #length = math.sqrt((x*x) + (y*y))
        M = math.sqrt(r*r - (x*x + y*y))/math.sqrt(x*x + y*y)
        #thr = math.fabs(y/x)
        #if thr > 1:
        #    sy = length
        #    sx = math.fabs(x/y)*sy
        # else:
        #    sx = length
        #    sy = math.fabs(y/x)*sx
        #sy = length
        #sx = math.sqrt((x*x-0)+math.fabs((y*y)-(length*length)))
        sx = 0
        sx = math.sqrt((a*a*b*b)/(b*b+a*a*M*M))
        sy = sx*M
        sx = x * sx / math.sqrt((x*x) + (y*y))
        sy = y * sy / math.sqrt((r*r) - ((x*x) + (y*y)))
        
        #sx = L*x/math.sqrt((r*r)-((x*x)+(y*y)))
        #sy = L*y/math.sqrt((r*r)-((x*x)+(y*y)))

        #if sx < -1000 or sx > 1000:
        #    sx = 1000
        #if sy < -1000 or sy > 1000:
        #    sy = 1000
        return (int(round(sx)), int(round(sy)))


class tarnslator():

    def __init__(self, center_x, center_y):
        self.cx = center_x
        self.cy = center_y

    def px2coordinate(self, x, y):
        cvt_x = x - self.cx
        cvt_y = -1*(y-self.cy)
        return (cvt_x, cvt_y)


class cmd_executor():

    def __init__(self, r, l, tls):
        self.translator = tls
        self.cmd = FisheyeCorrectionCommand()
        self.cmd.setRadius(r)
        self.cmd.setFocusLength(l)
        self.re_list = []
        self.center_x = center_x
        self.center_y = center_y
        print('cmd init')

    def execute(self, pos):
        x = pos[0]
        y = pos[1]
        cx, cy = self.translator.px2coordinate(x, y)
        cmd = self.cmd
        cmd.setPos(cx, cy)
        if cmd.canExecute() is True:
            new_x, new_y = cmd.execute()
            return {'indexX': int(x), 'indexY': int(y), 'x': int(new_x), 'y': int(new_y)}
        else:
            return None

if __name__ == '__main__':
    fp = '360.jpg'
    im = load_image(fp)
    rim = im.resize((501, 501))
    dat = np.asarray(rim, dtype=np.uint8)
    print(dat.shape)
    shape = dat.shape
    org_w, org_h, clr = shape

    # convert
    r = org_w/2.0
    center_x = r
    center_y = r
    l = r / 0.25
    tls = tarnslator(center_x, center_y)
    exe = cmd_executor(r, l, tls)
    px_list = list(filter(lambda val: (val is not None), [exe.execute((x, y)) for x in range(0, org_w) for y in range(0, org_h)]))
    x_list = [px['x'] for px in px_list]
    y_list = [py['y'] for py in px_list]

    # calc width & height
    print(max(x_list))
    print(min(x_list))
    print(max(y_list))
    print(min(y_list))
    w = max(x_list) - min(x_list)
    h = max(y_list) - min(y_list)
    print(str(w) + ' :: ' + str(h))
    bImg = create_blank_image(w, h)
    for px in px_list:
        indexX = px['x'] + int(w/2)-1  # translate co ->px
        indexY = int(h/2) - px['y']-1
        px['x'] = indexX
        px['y'] = indexY
        bImg[indexY][indexX] = dat[px['indexY']][px['indexX']]
    from queue import Queue

    def oneLineProcess(y):
        line_list = [px for px in px_list if px['y'] == y]
        if len(line_list) == 0:
            return 0
        line_list = sorted(line_list, key=lambda p: p['x'])
        '''
        tmp_cl = [0, 0, 0]
        for x in range(0, w):
            print(y)
            if True in (bImg[x][y] != 0):
                tmp_cl = bImg[x][y]
            else:
                bImg[x][y] = tmp_cl
        '''
        def getFunc(x1, y1, x2, y2):
            if (y2 != 0 or y1 != 0) and y1 != y2:
                a = (y2-y1)/(x2-x1)
                b = y1 - (a*x1)
            else:
                a = 0
                b = 0
            print('-')
            print('x1='+str(x1)+' y1='+str(y1))
            print('x2='+str(x2)+' y2='+str(y2))
            print('a='+str(a)+' b='+str(b))
            print('-')
            return lambda x: int(a*x + b)
        n_info = bImg[y][0]
        R_method = getFunc(0,0,0,n_info[0])
        G_method = getFunc(0,0,0,n_info[1])
        B_method = getFunc(0,0,0,n_info[2])
        index = 0
        for x in range(0, w):
            px = line_list[index]
            if x == px['x'] and (index+1) < len(line_list):
                nx = line_list[index+1]['x']
                c_info = bImg[y][x]
                n_info = bImg[y][nx]
                print('----')

                R_method = getFunc(x, c_info[0], nx, n_info[0])
                G_method = getFunc(x, c_info[1], nx, n_info[1])
                B_method = getFunc(x, c_info[2], nx, n_info[2])
                index = index+1
            else:
                bImg[y][x][0] = R_method(x)
                bImg[y][x][1] = G_method(x)
                bImg[y][x][2] = B_method(x)
    q = Queue()

    def worker():
        while True:
            y = q.get()
            oneLineProcess(y)
            q.task_done()
    '''
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
