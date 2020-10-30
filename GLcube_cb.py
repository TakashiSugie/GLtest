#!env python

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

# ひとまずこいつをいい感じに回すことを考えたい

vertex = [
    [-1.0, -1.0, 1.0],
    [1.0, -1.0, 1.0],
    [-1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0],
    [-1.0, 1.0, -1.0],
    [1.0, 1.0, -1.0],
    [-1.0, -1.0, -1.0],
    [1.0, -1.0, -1.0],
]

face = [
    [0, 1, 3, 2],
    [2, 3, 5, 4],
    [4, 5, 7, 6],
    [6, 7, 1, 0],
    [1, 7, 5, 3],
    [6, 0, 2, 4],
]

color = [
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.5, 0.5],
    [1.0, 1.0, 0.0],
    [1.0, 0.0, 1.0],
    [0.0, 1.0, 1.0],
]
LeftButtonOn = False
RightButtonOn = False
Angle1 = 0
Angle2 = 0
Distance = 7.0
px, py = -1, -1


def cb_resize(w, h):
    glViewport(50, 150, int(w / 2), int(h / 2))


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


def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30.0, w / h, 1, 1000.0)  # 視体積を設定することができる
    glMatrixMode(GL_MODELVIEW)


def draw():
    global Angle1, Angle2

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
    glBegin(GL_QUADS)
    for j in range(0, len(face)):
        glColor3dv(color[j])
        for i in range(0, 4):
            glVertex(vertex[face[j][i]])
    glEnd()

    glFlush()
    glutSwapBuffers()


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
glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)

glutMainLoop()
