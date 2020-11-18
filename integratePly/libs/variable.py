import numpy as np
import cv2
import os
import scipy.io as sio
import re

# from libs import matLoad, readCg


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
    return paraDict


def matLoad(u, v):
    mat = sio.loadmat(
        "/home/takashi/Desktop/dataset/from_iwatsuki/mat_file/additional_disp_mat/%s.mat"
        # "../../for_mac/mat_file/additional_disp_mat/%s.mat"
        % LFName
    )
    disp_gt = mat["depth"]
    return disp_gt[u][v]


u1, v1 = 0, 0
u2, v2 = 8, 8  # 0~8(uが→方向　vが下方向)
camNum1 = u1 * 9 + v1
camNum2 = u2 * 9 + v2
basePath = "/home/takashi/Desktop/dataset/lf_dataset/additional"
# basePath = "../../for_mac/lf_dataset/additional"
LFName = "dishes"
cfgName = "parameters.cfg"
cgPath = os.path.join(basePath, LFName, cfgName)
paraDict = readCg(cgPath)

imgName1 = "input_Cam{:03}".format(camNum1)
imgName2 = "input_Cam{:03}".format(camNum2)
imgPath1 = os.path.join(basePath, LFName, imgName1 + ".png")
imgPath2 = os.path.join(basePath, LFName, imgName2 + ".png")
img1 = cv2.imread(imgPath1)
img2 = cv2.imread(imgPath2)
dispImg1 = matLoad(u1, v1)
dispImg2 = matLoad(u2, v2)

width = img1.shape[1]
height = img1.shape[0]
saveName = LFName + "_" + str(camNum1) + "_" + str(camNum2)
