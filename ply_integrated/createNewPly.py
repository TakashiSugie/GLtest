# read np.dot write
import numpy as np
import os
import sys
import glob

from plyClass import Ply
from variable import imgName1, imgName2, saveName


def write_ply(v_line, f_line, Height, Width, hFov, vFov, num_vertex, num_face):
    # ply_name = "./mesh/new_" + imgName1 + "_" + imgName2 + ".ply"
    ply_name = "./mesh/" + saveName + ".ply"
    print("Writing mesh file %s ..." % ply_name)
    with open(ply_name, "w") as ply_fi:
        ply_fi.write("ply\n" + "format ascii 1.0\n")
        ply_fi.write("comment H " + str(Height) + "\n")
        ply_fi.write("comment W " + str(Width) + "\n")
        ply_fi.write("comment hFov " + str(hFov) + "\n")
        ply_fi.write("comment vFov " + str(vFov) + "\n")
        ply_fi.write("element vertex " + str(num_vertex) + "\n")
        ply_fi.write(
            "property float x\n"
            + "property float y\n"
            + "property float z\n"
            + "property uchar red\n"
            + "property uchar green\n"
            + "property uchar blue\n"
            + "property uchar alpha\n"
        )
        ply_fi.write("element face " + str(num_face) + "\n")
        ply_fi.write("property list uchar int vertex_index\n")
        ply_fi.write("end_header\n")
        ply_fi.writelines(v_line + "\n")
        ply_fi.writelines(f_line)
    ply_fi.close()
    return 1


def read_ply(mesh_fi):
    ply_fi = open(mesh_fi, "r")
    Height = None
    Width = None
    hFov = None
    vFov = None
    faces = []
    while True:
        line = ply_fi.readline().split("\n")[0]
        if line.startswith("element vertex"):
            num_vertex = int(line.split(" ")[-1])
        elif line.startswith("element face"):
            num_face = int(line.split(" ")[-1])
        elif line.startswith("comment"):
            if line.split(" ")[1] == "H":
                Height = int(line.split(" ")[-1].split("\n")[0])
            if line.split(" ")[1] == "W":
                Width = int(line.split(" ")[-1].split("\n")[0])
            if line.split(" ")[1] == "hFov":
                hFov = float(line.split(" ")[-1].split("\n")[0])
            if line.split(" ")[1] == "vFov":
                vFov = float(line.split(" ")[-1].split("\n")[0])
        elif line.startswith("end_header"):
            break
    contents = ply_fi.readlines()
    vertex_infos = contents[:num_vertex]
    face_infos = contents[num_vertex:]

    for f_info in face_infos:
        faces.append(f_info)

    return faces, Height, Width, hFov, vFov, num_vertex, num_face, vertex_infos


def main():
    mesh1_fi = "./mesh/" + imgName1 + ".ply"
    save_fi = "./mesh/" + imgName1 + "_integrated.ply"

    mesh1 = Ply(mesh1_fi)
    # mesh1.convertForWrite()
    mesh1.ClassWritePly(save_fi)
    # print(type(mesh1.v_infos))
    print(len(mesh1.v_infos))
    print(type(mesh1.v_line))
    print(len(mesh1.v_line))

    for key in mesh1.__dict__.keys():
        # print(key)
        pass


main()
