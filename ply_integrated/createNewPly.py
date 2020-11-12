# read np.dot write
import numpy as np
import os
import sys
import glob

from plyClass import Ply
from variable import imgName1, imgName2, saveName


def main():
    mesh1_fi = "./mesh/" + imgName1 + ".ply"
    save_fi = "./mesh/" + imgName1 + "_integrated.ply"
    npyPath = "./M/" + saveName + ".npy"
    mesh1 = Ply(mesh1_fi)
    # mesh1.ClassWritePly(save_fi, npyPath=None)
    mesh1.ClassWritePly(save_fi, npyPath=npyPath)
    for key in mesh1.__dict__.keys():
        # print(key)
        pass


main()
