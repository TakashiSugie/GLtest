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


camNum1 = 0
camNum2 = 80
basePath = "/home/takashi/Desktop/dataset/lf_dataset/additional"
LFName = "tower"
cfgName = "parameters.cfg"
imgName1 = "input_Cam{:03}".format(camNum1)
imgName2 = "input_Cam{:03}".format(camNum2)
cgPath = os.path.join(basePath, LFName, cfgName)
imgPath1 = os.path.join(basePath, LFName, imgName1 + ".png")
imgPath2 = os.path.join(basePath, LFName, imgName2 + ".png")
img = cv2.imread(imgPath1)

width = img.shape[1]
height = img.shape[0]
# maxD = np.max(depthImg)
# minD = np.min(depthImg)
ratio = 0.000003
verts = []
vert_point = []

sameMin = []
sameMax = []


def makeDepthImg():
    file_name = "tower"

    mat = sio.loadmat(
        "/home/takashi/Desktop/dataset/from_iwatsuki/mat_file/additional_disp_mat/%s.mat"
        % file_name
    )
    depth_gt = mat["depth"]
    mm = preprocessing.MinMaxScaler()
    min0_max1 = mm.fit_transform(depth_gt[0][0])
    # cv2.imwrite(
    #     "./tower/depth_%d_%d.png" % (0, 0), min0_max1 * 255,
    # )
    print("depth", min0_max1.shape)
    return min0_max1


def setVertsFromNpy():
    global verts

    npyVerts = np.load("%s.npy" % imgName1)
    colors = npyVerts[:, :, 3:6]
    points = npyVerts[:, :, 0:3]
    points_np3d = np.reshape(np.array(points), img.shape)
    points_np = mmNormal(points_np3d)
    colors_np = np.reshape(np.array(colors), img.shape)
    verts = np.concatenate((points_np, colors_np), axis=2)
    return verts


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
    print(num_vertex)
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

    print(npyVerts.shape)
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


if __name__ == "__main__":
    # verts = setVertsFromNpy()
    verts = setVertsFromPly()
    print(verts.shape)
