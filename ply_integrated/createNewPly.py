# read np.dot write
import numpy as np
import os
import sys
import glob

from plyClass import Ply
from variable import imgName1, imgName2, saveName


def main():
    mesh2_fi = "./mesh/" + imgName2 + ".ply"
    # save_fi = "./mesh/" + imgName2 + "_integrated.ply"
    # npyPath = "./M/" + saveName + ".npy"
    mesh2 = Ply(mesh2_fi)
    # mesh1.ClassWritePly(save_fi, npyPath=None)
    # mesh1.ClassWritePly(save_fi, npyPath=npyPath)
    mesh1_2_fi = "./mesh/" + saveName + ".ply"
    save_fi = "./mesh/" + saveName + "_integrated.ply"
    npyPath = "./M/" + saveName + ".npy"
    mesh1_2 = Ply(mesh1_2_fi)
    mesh1_2.integrate([mesh2.v_infos, mesh2.num_vertex])
    mesh1_2.ClassWritePly(save_fi, npyPath=npyPath)

    for key in mesh2.__dict__.keys():
        # print(key)
        pass


main()
