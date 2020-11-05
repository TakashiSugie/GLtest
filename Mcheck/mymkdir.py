import os


def my_mkdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


if __name__ == "__main__":
    dirList = ["M", "FPImg", "FP_2d", "FP_3d", "mesh", "npy"]
    for dir in dirList:
        my_mkdir(dir)
