#!env python

# plyを作成するコード
# makePly makePly Mを求める　統合　jiyuu.pyにしたい
# xは全体を
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import cv2
from readFile import readCg
import os
import scipy.io as sio


def matLoad():
    mat = sio.loadmat("../../dataset/%s.mat" % LFName)
    depth_gt = mat["depth"]
    print(depth_gt.shape)
    return depth_gt[0][0]


basePath = "/home/takashi/Desktop/dataset/lf_dataset/additional"
LFName = "tower"
cfgName = "parameters.cfg"
imgName = "input_Cam000.png"
cgPath = os.path.join(basePath, LFName, cfgName)
imgPath = os.path.join(basePath, LFName, imgName)
img = cv2.imread(imgPath)
dispImg = matLoad()


width = img.shape[1]
height = img.shape[0]
verts = []


def setVerts(img, depthImg, paraDict):
    global verts
    print(img.shape, depthImg.shape)
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            colors = [
                float(img[y][x][0] / 255.0),
                float(img[y][x][1] / 255.0),
                float(img[y][x][2] / 255.0),
            ]
            # X, Y, Z = calcVert(x, y)
            X, Y, Z = pix2m_disp(x, y, paraDict)

            vert = np.array([X, Y, Z, colors[0], colors[1], colors[2]])
            verts.append(vert)
    return verts


def pix2m_depth(x, y):
    f_mm = 0.01
    B_m = 0.001
    Z = float(depthImg[x][y])
    X = x * Z / f_pix
    Y = y * Z / f_pix
    return X, Y, Z


def pix2m_disp(x, y, paraDict):
    f_mm = paraDict["focal_length_mm"]
    s_mm = paraDict["sensor_size_mm"]
    b_mm = paraDict["baseline_mm"]
    f_pix = (f_mm * dispImg.shape[1]) / s_mm
    if dispImg[x][y]:
        Z = b_mm * f_pix / float(dispImg[x][y])
    else:
        print("zero!!")
        Z = 0
    X = x * Z / f_pix
    Y = y * Z / f_pix
    return X, Y, Z


def calcVert(x, y):
    X = (2.0 * float(x) / float(width)) - 1
    Y = 1 - (2.0 * float(y) / float(height))
    Z = ratio * float(maxD - minD) * float(depthImg[y][x])
    return X, Y, Z


if __name__ == "__main__":

    paraDict = readCg(cgPath)
    verts = setVerts(img, dispImg, paraDict)
