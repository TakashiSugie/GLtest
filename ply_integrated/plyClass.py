class Ply:
    def __init__(self, mesh_fi):
        self.plyName = mesh_fi
        self.ClassReadPly()
        # self.save_fi = save_fi

    #
    def ClassWritePly(self, save_fi):
        self.convertForWrite()
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

    def convertForWrite(self):
        v_list = []
        for v_info in self.v_infos:
            str_info = [float(v) for v in v_info.split("\n")[0].split(" ")]
            if len(str_info) == 6:
                vx, vy, vz, r, g, b = str_info
            else:
                vx, vy, vz, r, g, b, hi = str_info
            v_list.append(
                " ".join(list(map(str, [vx, vy, vz, int(r), int(g), int(b), int(hi)])))
            )
        self.v_line = "\n".join(v_list)
        self.f_line = "".join(self.f_infos)
    def dotsM(self, M):



if __name__ == "__main__":
    mesh_fi = "./mesh/input_Cam000.ply"
    mesh1 = Ply(mesh_fi)
    # print(mesh1.num_vertex)
