# create ply from npy

import numpy as np
import os
from variable import imgName1, imgName2


def getElement(line):
    # print(line)
    return (
        float(line[0]),
        float(line[1]),
        float(line[2]),
        int(line[3] * 255),
        int(line[4] * 255),
        int(line[5] * 255),
    )


def createPlyData(imgName, verts_np):
    pathPly = "./mesh/%s.ply" % imgName
    verts_flat = np.reshape(verts_np, (verts_np.shape[0] * verts_np.shape[1], 6))
    vertsList = list(verts_flat)
    with open(pathPly, mode="w") as ply_fi:
        ply_fi.write("ply\n" + "format ascii 1.0\n")
        ply_fi.write("comment H " + str(int(verts_np.shape[0])) + "\n")
        ply_fi.write("comment W " + str(int(verts_np.shape[1])) + "\n")
        ply_fi.write("comment hFov " + str(float(0.9272952180016122)) + "\n")
        ply_fi.write("comment vFov " + str(float(0.9272952180016122)) + "\n")
        ply_fi.write("element vertex " + str(len(verts_flat)) + "\n")
        ply_fi.write(
            "property float x\n"
            + "property float y\n"
            + "property float z\n"
            + "property uchar red\n"
            + "property uchar green\n"
            + "property uchar blue\n"
            + "property uchar alpha\n"
        )
        ply_fi.write("element face " + str(len(verts_flat)) + "\n")
        ply_fi.write("property list uchar int vertex_index\n")
        ply_fi.write("end_header\n")
        for line in vertsList:
            vx, vy, vz, c1, c2, c3 = getElement(line)
            ply_fi.write("%f %f %f %d %d %d 1\n" % (vx, vy, vz, c1, c2, c3))
        for Idx in range(len(verts_flat)):
            num1, num2, num3 = Idx + 1, Idx + 2, Idx + 3
            if int(num3) > int(len(verts_flat)):
                num3 = num3 - len(verts_flat)
            if num2 > len(verts_flat):
                num2 = num2 - len(verts_flat)
            if num1 > len(verts_flat):
                num1 = num1 - len(verts_flat)
            ply_fi.write("3 %d %d %d\n" % (num1, num2, num3))


if __name__ == "__main__":
    verts_np1 = np.load("./npy/%s.npy" % imgName1)
    verts_np2 = np.load("./npy/%s.npy" % imgName2)

    createPlyData(imgName1, verts_np1)
    createPlyData(imgName2, verts_np2)
