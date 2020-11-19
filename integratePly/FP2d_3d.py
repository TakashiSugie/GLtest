import numpy as np
import sys
import os
import scipy.io as sio
import re
from libs.libs import readCg, matLoad, pix2m_disp
from libs.variable import imgName1, imgName2


def readCVMatching(npyPath):
    featurePointList = []

    FP_data = np.load(npyPath)
    for y in range(FP_data.shape[0]):
        FP = (int(FP_data[y][0]), int(FP_data[y][1]))
        featurePointList.append(FP)
    return featurePointList


def FP2d_3d(imgIdx, FP_2d):
    FP_3d = []
    for FP in FP_2d:
        FP_3d.append(pix2m_disp(FP[0], FP[1], imgIdx))
    return FP_3d


if __name__ == "__main__":
    FP_2d_1 = readCVMatching("./FP_2d/FP_" + imgName1 + ".npy")
    FP_3d_1 = FP2d_3d(1, FP_2d_1)
    np.save("./FP_3d/" + imgName1, FP_3d_1)

    FP_2d_2 = readCVMatching("./FP_2d/FP_" + imgName2 + ".npy")
    FP_3d_2 = FP2d_3d(2, FP_2d_2)
    np.save("./FP_3d/" + imgName2, FP_3d_2)