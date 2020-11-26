import numpy as np
from libs.libs import pix2m_disp
import cv2


class Ply:
    def __init__(self, mesh_fi=None, img=None, imgIdx=None):
        if mesh_fi:
            self.plyName = mesh_fi
            self.ClassReadPly()
        elif imgIdx:
            # img = cv2.imread(imgPath)
            self.PlyFromImg(img, imgIdx)
        else:
            print("Ply init  error")

    def ClassReadPly(self):
        self.ply_fi = open(self.plyName, "r")
        self.f_infos = []
        self.v_infos = []
        while True:
            line = self.ply_fi.readline().split("\n")[0]
            if line.startswith("element vertex"):
                self.num_vertex = int(line.split(" ")[-1])
            elif line.startswith("element face"):
                self.num_face = int(line.split(" ")[-1])
            elif line.startswith("comment"):
                if line.split(" ")[1] == "H":
                    self.Height = int(line.split(" ")[-1].split("\n")[0])
                if line.split(" ")[1] == "W":
                    self.Width = int(line.split(" ")[-1].split("\n")[0])
                if line.split(" ")[1] == "hFov":
                    self.hFov = float(line.split(" ")[-1].split("\n")[0])
                if line.split(" ")[1] == "vFov":
                    self.vFov = float(line.split(" ")[-1].split("\n")[0])
            elif line.startswith("end_header"):
                break
        contents = self.ply_fi.readlines()
        vertex_infos = contents[: self.num_vertex]
        face_infos = contents[self.num_vertex :]

        for vertex_info in vertex_infos:
            self.v_infos.append(vertex_info)

        for f_info in face_infos:
            self.f_infos.append(f_info)

    def ClassWritePly(self, save_fi, npyPath=None):
        if npyPath == None:
            self.convertForWrite()
        else:
            self.dotsM(npyPath)
        self.changeRound(roundNum=4)
        print("Writing mesh file %s ..." % save_fi)
        with open(save_fi, "w") as ply_fi:
            ply_fi.write("ply\n" + "format ascii 1.0\n")
            ply_fi.write("comment H " + str(self.Height) + "\n")
            ply_fi.write("comment W " + str(self.Width) + "\n")
            ply_fi.write("comment hFov " + str(self.hFov) + "\n")
            ply_fi.write("comment vFov " + str(self.vFov) + "\n")
            ply_fi.write("element vertex " + str(self.num_vertex) + "\n")
            ply_fi.write(
                "property float x\n"
                + "property float y\n"
                + "property float z\n"
                + "property uchar red\n"
                + "property uchar green\n"
                + "property uchar blue\n"
                + "property uchar alpha\n"
            )
            ply_fi.write("element face " + str(self.num_face) + "\n")
            ply_fi.write("property list uchar int vertex_index\n")
            ply_fi.write("end_header\n")
            ply_fi.writelines(self.v_line + "\n")
            ply_fi.writelines(self.f_line)
        ply_fi.close()

    def convertForWrite(self):  # listで来たv_infosの各要素を取り出して、変換を行わずにstr型に変換する
        self.v_line = "".join(self.v_infos)
        self.f_line = "".join(self.f_infos)

    def dotsM(self, npyPath):  # listで来たv_infosの各要素を取り出して、変換Mを行う、その後、str型に変換する
        vertex_infos = []
        M = np.load(npyPath)
        for v_info in self.v_infos:
            str_info = [float(v) for v in v_info.split("\n")[0].split(" ")]
            if len(str_info) == 6:
                vx, vy, vz, r, g, b = str_info
            else:
                vx, vy, vz, r, g, b, hi = str_info
            oldV = np.array((vx, vy, vz, 1))
            NewV = np.dot(M, oldV)
            NewVx, NewVy, NewVz = NewV
            vertex_infos.append(
                " ".join(
                    list(
                        map(str, [NewVx, NewVy, NewVz, int(r), int(g), int(b), int(hi)])
                    )
                )
                + "\n"
            )
        # self.v_line = "\n".join(vertex_infos)
        del self.v_infos
        self.v_infos = []
        for vertex_info in vertex_infos:
            self.v_infos.append(vertex_info)
        self.v_line = "".join(vertex_infos)
        self.f_line = "".join(self.f_infos)
        return self

    def integrate(self, v_infos_add):
        self.v_infos += v_infos_add[0]
        self.num_vertex += v_infos_add[1]

    def PlyFromImg(self, img, imgIdx):
        v_list = []
        for y in range(img.shape[1]):
            for x in range(img.shape[0]):
                X, Y, Z = pix2m_disp(x, y, imgIdx)
                v_list.append(
                    " ".join(
                        list(
                            map(
                                str,
                                [X, Y, Z, img[x][y][2], img[x][y][1], img[x][y][0], 1,],
                            )
                        )
                    )
                    + "\n"
                )
        self.num_vertex = len(v_list)
        self.num_face = len(v_list)
        self.v_infos = v_list
        self.f_infos = []
        self.Height = img.shape[0]
        self.Width = img.shape[1]
        self.hFov = 0.9272952180016122
        self.vFov = 0.9272952180016122

    def changeColor(self, r=255, g=255, b=255, sigma=1):
        vertex_infos = []
        for v_info in self.v_infos:
            str_info = [float(v) for v in v_info.split("\n")[0].split(" ")]
            if len(str_info) == 6:
                vx, vy, vz, oriR, oriG, oriB = str_info
            else:
                vx, vy, vz, oriR, oriG, oriB, hi = str_info
            if sigma < 1:
                vertex_infos.append(
                    " ".join(
                        list(
                            map(
                                str,
                                [
                                    vx,
                                    vy,
                                    vz,
                                    int(oriR * sigma),
                                    int(oriG * sigma),
                                    int(oriB * sigma),
                                    int(hi),
                                ],
                            )
                        )
                    )
                    + "\n"
                )
            else:
                vertex_infos.append(
                    " ".join(list(map(str, [vx, vy, vz, r, g, b, int(hi)]))) + "\n"
                )
        # self.v_line = "\n".join(vertex_infos)
        del self.v_infos
        self.v_infos = []
        for vertex_info in vertex_infos:
            self.v_infos.append(vertex_info)

    def changeRound(self, roundNum=4):
        vertex_infos = []
        for v_info in self.v_infos:
            str_info = [float(v) for v in v_info.split("\n")[0].split(" ")]
            if len(str_info) == 6:
                vx, vy, vz, r, g, b = str_info
            else:
                vx, vy, vz, r, g, b, hi = str_info
            # print("old:", vx, vy, vx)
            vx, vy, vz = round(vx, roundNum), round(vy, roundNum), round(vz, roundNum)
            # print("change:", vx, vy, vx)

            vertex_infos.append(
                " ".join(list(map(str, [vx, vy, vz, int(r), int(g), int(b), int(hi)])))
                + "\n"
            )
        del self.v_infos
        self.v_infos = []
        for vertex_info in vertex_infos:
            self.v_infos.append(vertex_info)


if __name__ == "__main__":
    mesh_fi = "./mesh/input_Cam000.ply"
    mesh1 = Ply(mesh_fi)
    # print(mesh1.num_vertex)
