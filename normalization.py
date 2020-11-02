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
    max, min = [], []
    dst_3d = np.zeros(array.shape)
    for i in range(3):
        max.append(np.max(array[:, :, i]))
        min.append(np.min(array[:, :, i]))

        for x in range(array.shape[1]):
            for y in range(array.shape[0]):
                dst_3d[x][y][i] = (
                    2 * float(array[x][y][i] - min[i]) / float(max[i] - min[i]) - 1
                )
    return dst_3d


def XYZnormalization2(array):
    max, min = [], []
    dst_3d = np.zeros(array.shape)
    for i in range(3):
        max.append(np.max(array[:, :, i]))
        min.append(np.min(array[:, :, i]))

        for x in range(array.shape[1]):
            for y in range(array.shape[0]):
                dst_3d[x][y][i] = float(array[x][y][i] - min[i]) / float(
                    max[i] - min[i]
                )
    return dst_3d


def vertsNormalization(verts):
    xyz = verts[:, :, :3]
    # verts_c=verts[:,:,5]
    xyzNormed = XYZnormalization(xyz)
    vertsNormed = np.concatenate((xyzNormed, verts[:, :, 3:6]), axis=2)
    verts_Normed_2d = np.reshape(vertsNormed, (verts.shape[0] * verts.shape[1], 6))

    return list(verts_Normed_2d)


def checkMaxMin(verts_list):
    max, min, view = [], [], []
    # print(verts.ndim)
    verts = np.array(verts_list)
    if verts.ndim == 2:
        for i in range(6):
            max.append(np.max(verts[:, i]))
            min.append(np.min(verts[:, i]))

    elif verts.ndim == 3:
        for i in range(6):
            max.append(np.max(verts[:, :, i]))
            min.append(np.min(verts[:, :, i]))
    # print(max)
    # print(min)
    view.append(max)
    view.append(min)

    print(np.array(view))


if __name__ == "__main__":
    pre_verts = np.load("verts_reshape.npy")
    verts = vertsNormalization(pre_verts)
    checkMaxMin(np.array(verts))

    if checkC_F and np.array(verts).ndim == 3:
        cv2.imwrite("./c1_c6/x.png", verts[:, :, 0])
        cv2.imwrite("./c1_c6/y.png", verts[:, :, 1])
        cv2.imwrite("./c1_c6/z.png", verts[:, :, 2])
        cv2.imwrite("./c1_c6/c1.png", verts[:, :, 3] * 255)
        cv2.imwrite("./c1_c6/c2.png", verts[:, :, 4] * 255)
        cv2.imwrite("./c1_c6/c3.png", verts[:, :, 5] * 255)
