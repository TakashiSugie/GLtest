import numpy as np
import cv2

checkC_F = True


def normalization(array):
    max = np.max(array)
    min = np.min(array)
    dst = np.zeros(array.shape)
    for x in range(array.shape[1]):
        for y in range(array.shape[0]):
            dst[x][y] = float(array[x][y] - min) / float(max - min)
    return dst


def XYZnormalization(array):
    max = np.max(array[:, :, 0])
    min = np.min(array[:, :, 0])
    dst = np.zeros(array.shape)
    for i in range(3):
        for x in range(array.shape[1]):
            for y in range(array.shape[0]):
                dst[x][y][i] = float(array[x][y][i] - min) / float(max - min)
    return dst


def vertsNormalization(verts):
    xyz = verts[:, :, :3]
    xyzNormed = XYZnormalization(xyz)
    # print(np.min(xyzNormed))
    vertsNormed = np.concatenate((xyzNormed, verts[:, :, 3:6]), axis=2)
    return vertsNormed


if __name__ == "__main__":
    pre_verts = np.load("verts_reshape.npy")
    verts = vertsNormalization(pre_verts)
    print(verts.shape)

    if checkC_F:
        cv2.imwrite("./c1_c6/x.png", verts[:, :, 0])
        cv2.imwrite("./c1_c6/y.png", verts[:, :, 1])
        cv2.imwrite("./c1_c6/z.png", verts[:, :, 2])
        cv2.imwrite("./c1_c6/c1.png", verts[:, :, 3] * 255)
        cv2.imwrite("./c1_c6/c2.png", verts[:, :, 4] * 255)
        cv2.imwrite("./c1_c6/c3.png", verts[:, :, 5] * 255)
