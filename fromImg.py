import numpy as np
import cv2
from normalization import checkMaxMin

# img = cv2.imread("data/table/table.png")
# depthImg = cv2.imread("data/table/tableD.png", 0)
img = cv2.imread("data/lf/tower/input_Cam000.png")
depthImg = cv2.imread("depth/tower/depth_0_0.png", 0)

width = img.shape[1]
height = img.shape[0]
maxD = np.max(depthImg)
minD = np.min(depthImg)
ratio = 0.000003
verts = []
vert_point = []


def setVerts():
    global verts
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            colors = [
                float(img[y][x][0] / 255.0),
                float(img[y][x][1] / 255.0),
                float(img[y][x][2] / 255.0),
            ]
            X, Y, Z = calcVert(x, y)
            vert = np.array([X, Y, Z, colors[2], colors[1], colors[0]])
            verts.append(vert)
    return verts


def calcVert(x, y):
    X = (2.0 * float(x) / float(width)) - 1
    Y = 1 - (2.0 * float(y) / float(height))
    Z = ratio * float(maxD - minD) * float(depthImg[y][x])
    return X, Y, Z


def setVerts2():
    global verts, vert_point
    #print()
    colors=[]
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            color = [
                float(img[x][y][2] / 255.0),
                float(img[x][y][1] / 255.0),
                float(img[x][y][0] / 255.0),
            ]
            colors.append(color)
            vert_point.append(np.array([x,y,depthImg[x][y]]))
    pre_verts_3d=np.reshape(np.array(vert_point),img.shape)
    verts_3d=XYZnormalization2(pre_verts_3d)
    colors_3d=np.reshape(np.array(colors),img.shape)
    verts=np.concatenate((verts_3d,colors_3d),axis=2)
    verts_2d=np.reshape(verts,(img.shape[0]*img.shape[1],6))
    return list(verts_2d)


def XYZnormalization2(array):
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

if __name__ == "__main__":
    verts=setVerts2()
    #verts=setVerts()
    #print(len(verts))
    checkMaxMin(list(verts))
