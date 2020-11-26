import glob
import cv2
import os

os.makedirs("../image", exist_ok=True)
imgList = glob.glob("./*.JPG")
for imgPath in imgList:
    img = cv2.imread(imgPath)
    cv2.imwrite("../image/" + imgPath + ".png", img)
