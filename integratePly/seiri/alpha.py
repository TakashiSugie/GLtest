from libs.variable import img1, img2, dispImg1, dispImg2
from libs.libs import alphaCompositing

if __name__ == "__main__":
    print(type(img1), type(dispImg2))
    print(img1.shape, dispImg2.shape)
    alphaCompositing(img1, dispImg1)
    alphaCompositing(img2, dispImg2)
