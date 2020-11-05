#!env python

# npyを作成するコード
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import cv2

import os
import scipy.io as sio
import re
from variable import (
    paraDict,
    imgName1,
    imgName2,
    img1,
    img2,
    dispImg1,
    dispImg2,
)
from libs import pix2m_disp


def setVerts(verts, imgIdx):
    # global verts
    if imgIdx == 1:
        img = img1
    else:
        img = img2
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            colors = [
                float(img[x][y][2] / 255.0),
                float(img[x][y][1] / 255.0),
                float(img[x][y][0] / 255.0),
            ]
            X, Y, Z = pix2m_disp(x, y, imgIdx)

            vert = np.array([X, Y, Z, colors[0], colors[1], colors[2]])
            verts.append(vert)
    return verts


if __name__ == "__main__":
    # global verts
    verts = []
    verts1 = setVerts(verts, imgIdx=1)
    verts_np1 = np.array(verts1)
    verts_reshape1 = np.reshape(verts_np1, (512, 512, 6))
    np.save("./npy/%s" % imgName1, verts_reshape1)
    del verts
    # print(leverts)
    verts = []
    verts2 = setVerts(verts, imgIdx=2)
    verts_np2 = np.array(verts2)
    verts_reshape2 = np.reshape(verts_np2, (512, 512, 6))
    np.save("./npy/%s" % imgName2, verts_reshape2)
    # ここで出てくるplyはワールド座標、x,y,zともに単位はmm
    # OpenGLで描画するときはこれを正規化して、見やすくする
    del verts
