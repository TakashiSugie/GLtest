#!/usr/bin/python

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


vertex = [
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [1.0, 1.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0],
    [1.0, 0.0, 1.0],
    [1.0, 1.0, 1.0],
    [0.0, 1.0, 1.0],
]

edge = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 0],
    [4, 5],
    [5, 6],
    [6, 7],
    [7, 4],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7],
]


def resize1(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30.0, w / h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)


def resize2(w, h):
    glViewport(0, 0, w, h)
    glLoadIdentity()
    glOrtho(-2.0, 2.0, -2.0, 2.0, -2.0, 2.0)


def draw1():
    glutSetWindow(winnum[0])

    glClearColor(0.0, 0.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    gluLookAt(3.0, 4.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glBegin(GL_LINES)
    for i in range(0, 12):
        glVertex(vertex[edge[i][0]])
        glVertex(vertex[edge[i][1]])
    glEnd()

    glFlush()
    glutSwapBuffers()


def draw2():
    glutSetWindow(winnum[1])

    glClearColor(0.0, 0.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glBegin(GL_LINES)
    for i in range(0, 12):
        glVertex(vertex[edge[i][0]])
        glVertex(vertex[edge[i][1]])
    glEnd()

    glFlush()
    glutSwapBuffers()


def keyboard(key, x, y):
    if key == "q":
        sys.exit()


winnum = []

glutInit(sys.argv)

glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(320, 320)
winnum.append(glutCreateWindow("PyOpenGL 22 1"))
glutDisplayFunc(draw1)
glutReshapeFunc(resize1)
glutKeyboardFunc(keyboard)

glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(320, 320)
winnum.append(glutCreateWindow("PyOpenGL 22 2"))
glutDisplayFunc(draw2)
glutReshapeFunc(resize2)
glutKeyboardFunc(keyboard)

glutMainLoop()
