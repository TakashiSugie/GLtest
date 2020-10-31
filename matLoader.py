from LF_data_loader import LF_data_loader
import scipy.io as sio
import cv2
from sklearn import preprocessing


if __name__ == "__main__":
    file_name = "tower"

    mat = sio.loadmat(
        "/home/takashi/Desktop/study/OpenGL/data/lf/tower/%s.mat" % file_name
    )
    # print(mat.keys())
    # print(type(mat))
    depth_gt = mat["depth"]
    mm = preprocessing.MinMaxScaler()
    for i in range(3):
        print("depth", depth_gt[i * 4][i * 4].shape)
        min0_max1 = mm.fit_transform(depth_gt[i * 4][i * 4])
        cv2.imwrite(
            "./depth/tower/depth_%d_%d.png" % (i * 4, i * 4),
            min0_max1 * 255,
        )
