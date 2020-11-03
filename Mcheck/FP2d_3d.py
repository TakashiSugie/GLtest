import numpy as np
import sys
import os
import scipy.io as sio
import re


def readCg(cgPath):
    patternList = ["focal_length_mm", "sensor_size_mm", "baseline_mm"]
    paraDict = {}
    with open(cgPath) as f:
        s = f.read()
        sLines = s.split("\n")
        for sLine in sLines:
            for pattern in patternList:
                if re.match(pattern, sLine):
                    sList = sLine.split()
                    paraDict[pattern] = float(sList[2])
    print(paraDict)
    return paraDict


def matLoad(u, v, LFName):
    mat = sio.loadmat(
        "/home/takashi/Desktop/dataset/from_iwatsuki/mat_file/additional_disp_mat/%s.mat"
        % LFName
    )
    disp_gt = mat["depth"]
    return disp_gt[u][v]


sys.path.append("/home/takashi/Desktop/libs")
# from libs import loader
# from loader import readCg, matLoad

camNum = 80
basePath = "/home/takashi/Desktop/dataset/lf_dataset/additional"
LFName = "tower"
cfgName = "parameters.cfg"
imgName1 = "input_Cam{:03}".format(camNum)
cgPath = os.path.join(basePath, LFName, cfgName)
imgPath = os.path.join(basePath, LFName, imgName1 + ".png")
dispImg = matLoad(0, 0, LFName)

paraDict = readCg(cgPath)
f_mm = paraDict["focal_length_mm"]
s_mm = paraDict["sensor_size_mm"]
b_mm = paraDict["baseline_mm"]
longerSide = max(dispImg.shape[0], dispImg.shape[1])
beta = b_mm * f_mm * longerSide
f_pix = (f_mm * longerSide) / s_mm


def readCVMatching(npyPath):
    featurePointList = []

    FP_data = np.load(npyPath)
    for y in range(FP_data.shape[0]):
        FP = (int(FP_data[y][0]), int(FP_data[y][1]))
        featurePointList.append(FP)
    return featurePointList


def FP2d_3d(FP_2d):
    FP_3d = []
    for FP in FP_2d:
        FP_3d.append(pix2m_disp(FP[0], FP[1]))
    return FP_3d


def pix2m_disp(x, y):
    if dispImg[x][y]:
        Z = float(beta * f_mm) / float((dispImg[x][y] * f_mm * s_mm + beta))
    else:
        print("zero!!")
        Z = 0
    X = float(x) * Z / f_pix
    Y = float(y) * Z / f_pix
    return [X, Y, Z]


if __name__ == "__main__":
    FP_2d = readCVMatching("./FP_2d/FP_" + imgName1 + ".npy")
    FP_3d = FP2d_3d(FP_2d)
    np.save("./FP_3d/" + imgName1, FP_3d)
    # print(FP_3d)
