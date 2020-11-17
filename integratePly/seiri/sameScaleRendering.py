#!env python

# レンダリング三枚の縮尺を揃える（max minを共有すれば行けそう）
# 実際にW座標系で統合を行う（両方の点群を足し合わせるだけで良い）


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import cv2

from PIL import Image
from PIL import ImageOps


# from evaluation import checkMaxMin
from setVerts import setVertsFromNpy, setVertsFromPly  # , setVertsFromPlySameMinMax
from libs.variable import saveName

# from libs import capture

LeftButtonOn = False
RightButtonOn = False
Angle1 = 0
Angle2 = 0
Distance = 7.0
px, py = -1, -1
windowSize = 512
angleRange = 5.0
plyName1 = "input_Cam080"
plyName2 = "input_Cam000"
plyName3 = saveName

mesh_fi1 = "./mesh/" + plyName1 + ".ply"
mesh_fi2 = "./mesh/" + plyName2 + ".ply"
mesh_fi3 = "./mesh/" + plyName3 + ".ply"

mesh_fiList = [mesh_fi1, mesh_fi2, mesh_fi3]
vertsList = []
winnum = []
captureNum = 0
# mesh_fiList.append(mesh_fi1)


def capture():
    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)
    # キャプチャ
    glReadBuffer(GL_FRONT)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_BGRA, GL_UNSIGNED_BYTE, None)

    image = np.frombuffer(data, dtype=np.uint8).reshape(width, height, 4)
    # capturePath = mesh_fi.replace("ply", "png")
    # cv2.imwrite("./capture/" + plyName1 + ".png", np.flipud(image))
    cv2.imwrite("./capture/" + str(captureNum) + ".png", np.flipud(image))
    print("capture now...")


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
            Angle1 += float(-(x - px) / 100)
            Angle2 += float((y - py) / 100)
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

    # print(LeftButtonOn, RightButtonOn, Angle1, Angle2, Distance, px, py, x, y)
    glutPostRedisplay()


def keyboard(key, x, y):
    global Angle2, captureNum
    if key.decode() == "\033":  # Escape
        sys.exit()
    elif key.decode() == "q":
        sys.exit()
    elif key.decode() == "j":
        Angle2 += 10.0
    elif key.decode() == "s":
        capture()
    elif key.decode() == "+":
        captureNum += 1
    else:
        print(key.decode())


def resize_cb(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(angleRange, w / h, 1, 1000.0)  # 視体積を設定することができる
    glMatrixMode(GL_MODELVIEW)


def draw1():
    glutSetWindow(winnum[0])
    global Angle1, Angle2, vertsList

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(
        Distance * np.cos(Angle2) * np.sin(Angle1),
        Distance * np.sin(Angle2),
        Distance * np.cos(Angle2) * np.cos(Angle1),
        0.0,
        0.0,
        0.0,
        -1.0,
        0.0,
        0.0,
    )
    glPointSize(2)
    glBegin(GL_POINTS)
    for vert in vertsList[0]:
        glColor3d(vert[3], vert[4], vert[5])
        glVertex3f(vert[0], vert[1], -vert[2])
    glEnd()
    glFlush()
    glutSwapBuffers()


def draw2():
    global Angle1, Angle2, vertsList
    glutSetWindow(winnum[1])

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(
        Distance * np.cos(Angle2) * np.sin(Angle1),
        Distance * np.sin(Angle2),
        Distance * np.cos(Angle2) * np.cos(Angle1),
        0.0,
        0.0,
        0.0,
        -1.0,
        0.0,
        0.0,
    )
    glPointSize(2)
    glBegin(GL_POINTS)
    for vert in vertsList[1]:
        glColor3d(vert[3], vert[4], vert[5])
        glVertex3f(vert[0], vert[1], -vert[2])
    glEnd()
    glFlush()
    glutSwapBuffers()


def draw3():
    global Angle1, Angle2, vertsList
    glutSetWindow(winnum[2])

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(
        Distance * np.cos(Angle2) * np.sin(Angle1),
        Distance * np.sin(Angle2),
        Distance * np.cos(Angle2) * np.cos(Angle1),
        0.0,
        0.0,
        0.0,
        -1.0,
        0.0,
        0.0,
    )
    glPointSize(2)
    glBegin(GL_POINTS)
    for vert in vertsList[2]:
        glColor3d(vert[3], vert[4], vert[5])
        glVertex3f(vert[0], vert[1], -vert[2])
    glEnd()
    glFlush()
    glutSwapBuffers()


glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(windowSize, windowSize)
winnum.append(glutCreateWindow(plyName1))
# glutCreateWindow()
glutDisplayFunc(draw1)
glutReshapeFunc(resize_cb)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutMotionFunc(motion)

glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(windowSize, windowSize)
winnum.append(glutCreateWindow(plyName2))
# glutCreateWindow()
glutDisplayFunc(draw2)
glutReshapeFunc(resize_cb)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutMotionFunc(motion)

glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(windowSize, windowSize)
winnum.append(glutCreateWindow(plyName3))
# glutCreateWindow()
glutDisplayFunc(draw3)
glutReshapeFunc(resize_cb)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutMotionFunc(motion)


glClearColor(0.0, 0.0, 1.0, 0.0)
glEnable(GL_DEPTH_TEST)
for mesh_fi in mesh_fiList:
    verts_np3d = setVertsFromPly(mesh_fi)
    verts = list(np.reshape(verts_np3d, (verts_np3d.shape[0] * verts_np3d.shape[1], 6)))
    vertsList.append(verts)
print("len_verts:", len(verts))

glutMainLoop()
