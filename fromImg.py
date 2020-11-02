import numpy as np
import cv2
from normalization import checkMaxMin
from matLoader import makeDepthImg
from sklearn import preprocessing

img = cv2.imread("tower/input_Cam000.png")
depthImg = cv2.imread("tower/depth_0_0.png", 0)

width = img.shape[1]
height = img.shape[0]
maxD = np.max(depthImg)
minD = np.min(depthImg)
ratio = 0.000003
verts = []
vert_point = []


def setVerts():
    global verts
    colors=[]
    points=[]
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            point = [
                float(x),float(y),float(depthImg[x][y])
            ]
            color = [
                float(img[x][y][0] / 255.0),
                float(img[x][y][1] / 255.0),
                float(img[x][y][2] / 255.0),
            ]
            colors.append(color)
            points.append(point)
    #この時点でcolorがlenは256*256,3ch
    #この時点でpointがlenは256*256,3ch
    #pointを正規化して、全て0~1に変更
    points_np3d=np.reshape(np.array(points),img.shape)
    points_np=pointsNormal(points_np3d)
    colors_np = np.reshape(np.array(colors),img.shape)
    verts=np.concatenate((points_np,colors_np),axis=2)
    return verts

def pointsNormal(points_np3d):
    mm = preprocessing.MinMaxScaler()
    points_tuple=(mm.fit_transform(points_np3d[:,:,0])[:,:,np.newaxis],mm.fit_transform(points_np3d[:,:,1])[:,:,np.newaxis],mm.fit_transform(points_np3d[:,:,2])[:,:,np.newaxis])
    points_np3d_Normed=np.concatenate(points_tuple,axis=2)
    return points_np3d_Normed

if __name__ == "__main__":
    verts=setVerts()
    print(verts.shape)
