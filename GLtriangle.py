#!/usr/bin/python
# 複数に分けたかったけど、多分きびしいかな。。。変更されない
import cv2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from callBack import keyboard, mouse, motion, cb_resize
from callBack import Distance, Angle1, Angle2


img = cv2.imread("data/04_04.png")
depthImg = cv2.imread("data/04_04_depth.png", 0)
width = img.shape[1]
height = img.shape[0]
maxD = np.max(depthImg)
minD = np.min(depthImg)
ratio = 0.00001
verts = []


def setVerts(img, depthImg):
    global verts
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            colors = [
                float(img[y][x][0] / 255.0),
                float(img[y][x][1] / 255.0),
                float(img[y][x][2] / 255.0),
            ]
            # vert = np.array([x, y, depthImg[x][y], colors[0], colors[1], colors[2]])
            X, Y, Z = calcVert(x, y)
            vert = np.array([X, Y, Z, colors[0], colors[1], colors[2]])
            verts.append(vert)
    return verts


def calcVert(x, y):
    X = (2.0 * float(x) / float(width)) - 1
    Y = 1 - (2.0 * float(y) / float(height))
    Z = ratio * float(maxD - minD) * float(depthImg[y][x])
    return X, Y, Z


def myDraw():
    global verts
    glClearColor(0.0, 0.0, 0.0, 0.0)

    gluLookAt(
        Distance * np.cos(Angle2) * np.sin(Angle1),
        Distance * np.sin(Angle2),
        Distance * np.cos(Angle2) * np.cos(Angle1),
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
    )
    print(Distance, Angle1, Angle2)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPointSize(1)
    glBegin(GL_POINTS)
    print(len(verts))
    for vert in verts:
        glColor3d(vert[3], vert[4], vert[5])
        glVertex3f(vert[0], vert[1], vert[2])
    glEnd()
    glFlush()
    glutSwapBuffers()


def setup():
    glutInit(sys.argv)
    # RGBAモード、ダブルバッファリング有効、Zバッファ有効で初期化
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutCreateWindow("glut sample")
    # Windowのサイズが変わった時に呼ばれる関数を登録
    glutReshapeFunc(cb_resize)
    # 描画時に呼ばれる関数を登録
    glutDisplayFunc(myDraw)
    # マウスボタン押し上げ時に呼ばれる関数
    glutMouseFunc(mouse)
    # マウスドラッグ時に呼ばれる関数
    glutMotionFunc(motion)
    # キーボードが押された時に呼ばれる関数
    glutKeyboardFunc(keyboard)


def rendering():
    glutDisplayFunc(myDraw)
    glutMainLoop()


if __name__ == "__main__":
    setup()
    verts = setVerts(img, depthImg)
    rendering()
