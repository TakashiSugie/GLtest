import cv2
import numpy as np

img1 = cv2.imread("../capture/antinous_0_80_100_h15.png")
# img2 = cv2.imread("../capture/antinous_0_80_none_h15.png")
img2 = cv2.imread("../capture/antinous_0_80_100.png")
absImg = np.abs(img1 - img2)
print(absImg.shape)
cv2.imwrite("../capture/abs.png", absImg * 100)
