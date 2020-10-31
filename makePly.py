#!env python

# plyを作成するコード
# makePly makePly Mを求める　統合　jiyuu.pyにしたい

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import cv2

LeftButtonOn = False
RightButtonOn = False
Angle1 = 0
Angle2 = 0
Distance = 7.0
px, py = -1, -1

img = cv2.imread("data/table/table.png")
depthImg = cv2.imread("data/table/tableD.png", 0)
width = img.shape[1]
height = img.shape[0]
maxD = np.max(depthImg)
minD = np.min(depthImg)
ratio = 0.00001
verts = []


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
        elif state == GLUT_DOWN:
            RightButtonOn = True


def motion(x, y):
    global RightButtonOn, LeftButtonOn, Angle1, Angle2, Distance, px, py
    if LeftButtonOn == True and RightButtonOn == True:
        Angle1 = 0
        Angle2 = 0
        Distance = 7.0
        gluLookAt(0, 0, 7.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0)
    elif LeftButtonOn == True:
        if px >= 0 and py >= 0:
            Angle1 += float(-(x - px) / 50)
            Angle2 += float((y - py) / 50)
        px = x
        py = y
    elif RightButtonOn == True:
        if px >= 0 and py >= 0:
            Distance += float(y - py) / 20
        px = x
        py = y
    else:
        px = -1
        py = -1

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


def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30.0, w / h, 1, 1000.0)
    glMatrixMode(GL_MODELVIEW)


def draw():
    global Angle1, Angle2, verts

    glClearColor(0.0, 0.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
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
    glPointSize(3)
    glBegin(GL_POINTS)
    for vert in verts:
        glColor3d(vert[3], vert[4], vert[5])
        glVertex3f(vert[0], vert[1], vert[2])
    glEnd()
    glFlush()
    glutSwapBuffers()


def setVerts(img, depthImg):
    global verts
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            colors = [
                float(img[y][x][0] / 255.0),
                float(img[y][x][1] / 255.0),
                float(img[y][x][2] / 255.0),
            ]
            X, Y, Z = calcVert(x, y)
            vert = np.array([X, Y, Z, colors[0], colors[1], colors[2]])
            verts.append(vert)
    return verts


def calcVert(x, y):
    X = (2.0 * float(x) / float(width)) - 1
    Y = 1 - (2.0 * float(y) / float(height))
    Z = ratio * float(maxD - minD) * float(depthImg[y][x])
    return X, Y, Z


glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(320, 320)
glutCreateWindow("PyOpenGL 11")
glutDisplayFunc(draw)
glutReshapeFunc(resize)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutMotionFunc(motion)

glClearColor(0.0, 0.0, 1.0, 0.0)
glEnable(GL_DEPTH_TEST)
verts = setVerts(img, depthImg)

glutMainLoop()
