import sys
import os
import matplotlib.pyplot as plt
from sklearn import linear_model
import numpy as np
import glob


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

error = 0
count = 0


def read3Dnp(npPath):
    FPnp = np.load(npPath)
    print(FPnp.shape)
    FPDict = {}

    for idx in range(FPnp.shape[0]):
        # FPDict[FPnp[idx][0]] = [
        FPDict[str(idx)] = [
            float(FPnp[idx][0]),
            float(FPnp[idx][1]),
            float(FPnp[idx][2]),
        ]

    return FPDict


def LR_(X, Y):
    global error, count
    clf = linear_model.LinearRegression()
    X = np.array(X)
    Y = np.array(Y)
    clf.fit(X, Y)
    coef = list(clf.coef_)
    coef.append(clf.intercept_)
    predict = 0
    for sample_index in range(X.shape[0]):

        no_intercept = 0
        for i in range(3):
            no_intercept += clf.coef_[i] * X[sample_index][i]
        predict = clf.intercept_ + no_intercept
        print("predict:", predict, "  GT", Y[sample_index])
        error += np.abs(predict - Y[sample_index])
        count += 1
    return coef


def LR(X, Y):
    global error, count
    X = np.array(X)
    Y = np.array(Y)
    ones = np.ones((X.shape[0], 1))
    X = np.concatenate((X, ones), axis=1)
    a = np.dot(np.dot((np.linalg.inv(np.dot(X.T, X))), X.T), Y)
    predict = 0
    for sample_index in range(X.shape[0]):
        predict = 0
        for i in range(4):
            predict += a[i] * X[sample_index][i]
        # predict = +no_intercept
        print("predict:", predict, "  GT", Y[sample_index])
        error += np.abs(predict - Y[sample_index])
        count += 1
    # print("error_sum:", loss)
    print("")
    return a


def calcDot(M):  # ここからMに制約をつけて更に制度を上げることを考える
    FPDict1 = read3Dnp("./FP_3d/" + imgName1 + ".npy")  # ("key": (x1,y1,z1))
    FPDict2 = read3Dnp("./FP_3d/" + imgName2 + ".npy")  # ("key": (x1',y1',z1'))
    X_train, y_train = [], []
    for key, value1 in FPDict1.items():
        value2 = FPDict2[key]
        X_train.append(np.array(value1))
        y_train.append(np.array(value2))
    for idx in range(len(X_train)):
        vx, vy, vz = X_train[idx]
        oldV = np.array((vx, vy, vz, 1))
        NewV = np.dot(M, oldV)
        print("NewV", NewV, "y", y_train[idx])
        print("error", np.abs(NewV - y_train[idx]))


def createData():
    M = []
    FPDict1 = read3Dnp("./FP_3d/" + imgName1 + ".npy")  # ("key": (x1,y1,z1))
    FPDict2 = read3Dnp("./FP_3d/" + imgName2 + ".npy")  # ("key": (x1',y1',z1'))

    X_train, y_train = [], []

    for key, value1 in FPDict1.items():
        value2 = FPDict2[key]
        X_train.append(value1)  # (x1,y1,z1)
        y_train.append(value2)  # (x1',y1',z1')
    # [[x1'],[y1'],[z1']]なんでかというとx1'=f(x1,y1,z1にしたかったから)
    y_train = list(np.array(y_train).T)

    for i in range(3):
        M.append(LR(X_train, y_train[i]))
    return M


def main():
    M = np.array(createData())
    print("M:", M)
    print("error_per_sample", error / float(count))
    Path = "M_" + imgName1 + "_" + imgName2
    np.save(Path, M)


main()
