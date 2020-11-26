# Npyからvertsを作成する


import numpy as np
import cv2
import re

# from normalization import checkMaxMin
# from matLoader import makeDepthImg
from sklearn import preprocessing
import scipy.io as sio
import os

# img = cv2.imread("tower/input_Cam000.png")
# depthImg = cv2.imread("tower/depth_0_0.png", 0)

# maxD = np.max(depthImg)
# minD = np.min(depthImg)
ratio = 0.000003
verts = []
vert_point = []

sameMin = []
sameMax = []


def readPly(mesh_fi):
    vertsList = []
    ply_fi = open(mesh_fi, "r")
    while True:
        line = ply_fi.readline().split("\n")[0]
        if line.startswith("element vertex"):
            num_vertex = int(line.split(" ")[-1])
        elif line.startswith("end_header"):
            break
    contents = ply_fi.readlines()
    vertex_infos = contents[:num_vertex]
    # print(num_vertex)
    for v_info in vertex_infos:
        str_info = [float(v) for v in v_info.split("\n")[0].split(" ")]
        if len(str_info) == 6:
            vx, vy, vz, r, g, b = str_info
        else:
            vx, vy, vz, r, g, b, _ = str_info
        vertsList.append(
            [
                float(vx),
                float(vy),
                float(vz),
                float(r / 255),
                float(g / 255),
                float(b / 255),
            ]
        )
    # vertsList
    # return np.reshape(np.array(vertsList), (img.shape[0], img.shape[1], 6))
    return np.array(vertsList)


def setVertsFromPly(mesh_fi):
    global verts
    # npyVerts = readPly("./mesh/new_%s_%s.ply" % (imgName1, imgName2))
    # npyVerts = readPly("./mesh/04_04.ply")
    npyVerts = readPly(mesh_fi)

    # print(npyVerts.shape)
    colors = npyVerts[:, 3:6]
    points = npyVerts[:, 0:3]
    # points_np3d = np.reshape(np.array(points), img.shape)
    points_np = mmNormalSameMinMax(np.array(points))
    # points_np = mmNormal(points_np3d)
    # colors_np = np.reshape(np.array(colors), img.shape)
    verts = np.concatenate((points_np, colors), axis=1)
    return verts


def pointsNormal(points_np3d):
    points_np3d_Normed = mmNormal(points_np3d)
    return points_np3d_Normed


def mmNormal(array):
    max, min = [], []
    scale = 0.5
    dst_3d = np.zeros(array.shape)
    for i in range(3):
        max.append(np.max(array[:, :, i]))
        min.append(np.min(array[:, :, i]))
        for x in range(array.shape[1]):
            for y in range(array.shape[0]):
                dst_3d[x][y][i] = (
                    scale * float(array[x][y][i] - min[i]) / float(max[i] - min[i])
                    - scale / 2.0
                )
    return dst_3d


def setMinMax(array):
    global sameMax, sameMin
    for i in range(3):
        if len(sameMax) < 4:
            sameMax.append(np.max(array[:, i]))
            sameMin.append(np.min(array[:, i]))


def mmNormalSameMinMax(array):
    # max, min = [], []
    setMinMax(array)
    scale = 0.5
    dst = np.zeros(array.shape)
    for i in range(3):
        for line in range(array.shape[0]):
            dst[line][i] = (
                scale
                * float(array[line][i] - sameMin[i])
                / float(sameMax[i] - sameMin[i])
                - scale / 2.0
            )
    return dst


def cvtVerts(verts):
    cList, vList = [], []
    for vert in verts:
        if len(vert) == 6:
            vx, vy, vz, r, g, b = vert
        else:
            vx, vy, vz, r, g, b, _ = vert
        cList.append([r, g, b])
        vList.append([vx, vy, vz])
    cNP, vNP = np.array(cList), np.array(vList)
    cFlat, vFlat = np.ravel(cNP), np.ravel(vNP)
    return cFlat, vFlat


if __name__ == "__main__":
    # verts = setVertsFromNpy()
    verts = setVertsFromPly()
    # print(verts.shape)
