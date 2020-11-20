import numpy as np
import cv2
import os
import scipy.io as sio
import re
import glob

# from libs import matLoad, readCg


def readCg(cgPath):
    patternList = ["focal_length_mm", "sensor_size_mm", "baseline_mm"]
    paraDict = {}
    if cgPath:
        with open(cgPath) as f:
            s = f.read()
            sLines = s.split("\n")
            for sLine in sLines:
                for pattern in patternList:
                    if re.match(pattern, sLine):
                        sList = sLine.split()
                        paraDict[pattern] = float(sList[2])
    else:
        paraDict = {
            "focal_length_mm": 100.0,
            "sensor_size_mm": 35.0,
            "baseline_mm": 90.0,
        }
    return paraDict


def matLoad(u, v):
    mat = sio.loadmat(
        "/home/takashi/Desktop/dataset/from_iwatsuki/mat_file/additional_disp_mat/%s.mat"
        # "../../for_mac/mat_file/additional_disp_mat/%s.mat"
        % LFName
    )
    disp_gt = mat["depth"]
    return disp_gt[u][v]


def longerResize(img, longerSideLen=640):
    longer = max(img.shape[0], img.shape[1])
    fraq = float(longerSideLen) / float(longer)
    if fraq < 1:
        img = cv2.resize(img, (int(img.shape[1] * fraq), int(img.shape[0] * fraq)))
    return img


u1, v1 = 0, 0
u2, v2 = 8, 8  # 0~8(uが→方向　vが下方向)
camNum1 = u1 * 9 + v1
camNum2 = u2 * 9 + v2
cgPath = None
# content = "additional"
# content = "lf"
content = "ori"


if content == "ori":
    basePath = "/home/takashi/Desktop/dataset/image"
    LFName = "copyMachine"
    dirPath = os.path.join(basePath, LFName)
    imgPathList = glob.glob(dirPath + "/*")
    imgName1 = os.path.splitext(os.path.basename(imgPathList[0]))[0]
    imgName2 = os.path.splitext(os.path.basename(imgPathList[1]))[0]
    # print(imgName1)


else:
    basePath = os.path.join("/home/takashi/Desktop/dataset/lf_dataset", content)
    LFName = "dino"
    if content == "additional":
        imgName1 = "input_Cam{:03}".format(camNum1)
        imgName2 = "input_Cam{:03}".format(camNum2)
        cfgName = "parameters.cfg"
        cgPath = os.path.join(basePath, LFName, cfgName)
        # cgExist = os.path.isfile(cgPath)
    elif content == "lf":
        imgName1 = "%02d_%02d" % (u1, v1)
        imgName2 = "%02d_%02d" % (u2, v2)
paraDict = readCg(cgPath)


# basePath = "../../for_mac/lf_dataset/additional"
imgPath1 = os.path.join(basePath, LFName, imgName1 + ".png")
imgPath2 = os.path.join(basePath, LFName, imgName2 + ".png")
# print(imgPath1)

img1 = cv2.imread(imgPath1)
img2 = cv2.imread(imgPath2)
img1 = longerResize(img1, 640)
img2 = longerResize(img2, 640)

require_midas = True
if require_midas:
    if os.path.isfile("./depth/" + imgName1 + ".npy"):
        dispImg1 = np.load("./depth/" + imgName1 + ".npy")
        dispImg2 = np.load("./depth/" + imgName2 + ".npy")
else:
    dispImg1 = matLoad(u1, v1)
    dispImg2 = matLoad(u2, v2)

# ここをMidasOnlyから出てきたNpyに書き換える
# Depthとかは正直おかしいかもしれないが、そこに関してはスルー
# Depthか視差かも正直怪しい、disp→Depth変換をつけたりなしにする必要があるかも

width = img1.shape[1]
height = img1.shape[0]
saveName = LFName + "_" + str(camNum1) + "_" + str(camNum2)


# if __name__ == "__main__":
#     print(dispImg1.shape)
#     print(type(dispImg1))
