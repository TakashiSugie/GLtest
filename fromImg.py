import numpy as np
import cv2

# img = cv2.imread("data/table/table.png")
# depthImg = cv2.imread("data/table/tableD.png", 0)
img = cv2.imread("data/lf/tower/input_Cam000.png")
depthImg = cv2.imread("depth/tower/depth_0_0.png", 0)

width = img.shape[1]
height = img.shape[0]
maxD = np.max(depthImg)
minD = np.min(depthImg)
ratio = 0.00001
verts = []


def setVerts():
    global verts
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            colors = [
                float(img[y][x][0] / 255.0),
                float(img[y][x][1] / 255.0),
                float(img[y][x][2] / 255.0),
            ]
            X, Y, Z = calcVert(x, y)
            vert = np.array([X, Y, Z, colors[2], colors[1], colors[0]])
            verts.append(vert)
    return verts


def calcVert(x, y):
    X = (2.0 * float(x) / float(width)) - 1
    Y = 1 - (2.0 * float(y) / float(height))
    Z = ratio * float(maxD - minD) * float(depthImg[y][x])
    return X, Y, Z
