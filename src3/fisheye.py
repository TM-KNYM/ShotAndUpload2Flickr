# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import math

im = Image.open('360.jpg')
print(im.size)
dat = np.asarray(im, dtype=np.uint8)
print(dat.shape)


diameter = 1807
x = 700.0 / 100.0  # x pos
y = 600.0 / 100.0  # y pos
r = 1807/2/100.0  # raidus
l = math.sqrt((pow(x, x)+pow(y, y)))
z = math.sqrt(pow(r, r)-(pow(x, x)+pow(y, y)))
pi = 3.14

L = 10  # focus

X = (L - np.tan(pi/2 - np.arctan(z/l)) - np.cos(np.arctan(z/l))) * 100.0
Y = (L - np.tan(pi/2 - np.arctan(z/l)) - np.sin(np.arctan(z/l))) * 100.0

print(X)
print(Y)
