#!/usr/bin/python
import cv2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# from callBack import keyboard, mouse, motion, cb_resize
# from callBack import Distance, Angle1, Angle2


LeftButtonOn = False
RightButtonOn = False
Angle1 = 0
Angle2 = 0
Distance = 7.0
px, py = -1, -1


def cb_resize(w, h):

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(100.0, w / h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    # glViewport(50, 150, int(w / 2), int(h / 2))


def mouse(button, state, x, y):
    global LeftButtonOn, RightButtonOn
    if button == GLUT_LEFT_BUTTON:
        if state == 1:
            LeftButtonOn = False
        elif state == 0:
            LeftButtonOn = True

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_UP:
            RightButtonOn = False
            # print("right up")
        elif state == GLUT_DOWN:
            RightButtonOn = True
            # print("right down")
    # print(x, y)


def motion(x, y):
    # print("motion:")
    global RightButtonOn, LeftButtonOn, Angle1, Angle2, Distance, px, py
    # px, py = -1, -1
    if LeftButtonOn == True and RightButtonOn == True:
        Angle1 = 0
        Angle2 = 0
        Distance = 7.0
        gluLookAt(0, 0, 7.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0)
    elif LeftButtonOn == True:
        if px >= 0 and py >= 0:
            Angle1 += float(-(x - px) / 50)
            Angle2 += float((y - py) / 50)
        # print((x - px) / 50)
        px = x
        py = y
    elif RightButtonOn == True:
        print("px reload", x, px)
        if px >= 0 and py >= 0:
            Distance += float(y - py) / 20
        px = x
        py = y
    else:
        px = -1
        py = -1

    print(LeftButtonOn, RightButtonOn, Angle1, Angle2, Distance, px, py, x, y)
    glutPostRedisplay()


def keyboard(key, x, y):
    global Angle2
    if key.decode() == "\033":  # Escape
        sys.exit()
    elif key.decode() == "q":
        sys.exit()
    elif key.decode() == "j":
        Angle2 += 1.0
    else:
        print(key.decode())


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
            # print(X, Y, Z)
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

    # gluLookAt(
    #     Distance * np.cos(Angle2) * np.sin(Angle1),
    #     Distance * np.sin(Angle2),
    #     Distance * np.cos(Angle2) * np.cos(Angle1),
    #     0.0,
    #     0.0,
    #     0.0,
    #     0.0,
    #     1.0,
    #     0.0,
    # )
    # print(Distance, Angle1, Angle2)
    gluLookAt(0, 0, 100.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # print("draw")

    glPointSize(100)
    glBegin(GL_POINTS)
    # print(len(verts))
    for vert in verts:
        glColor3d(vert[3], vert[4], vert[5])
        glVertex3f(vert[0], vert[1], vert[2])
    verts.clear()
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
    # print("dfaf")


def rendering():
    glutDisplayFunc(myDraw)
    glutMainLoop()


if __name__ == "__main__":
    setup()
    verts = setVerts(img, depthImg)
    rendering()
