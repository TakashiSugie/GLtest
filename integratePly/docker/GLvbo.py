# coding: utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

s = 0.5
vertices = [
    -s,
    -s,
    -s,
    s,
    -s,
    -s,
    s,
    s,
    -s,
    -s,
    s,
    -s,
    -s,
    -s,
    s,
    s,
    -s,
    s,
    s,
    s,
    s,
    -s,
    s,
    s,
]
colors = [
    0,
    0,
    0,
    0,
    0,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
]


buffers = 0


def create_vbo():
    buffers = glGenBuffers(3)
    print(buffers)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
    glBufferData(
        GL_ARRAY_BUFFER,
        len(vertices) * 4,  # byte size
        (ctypes.c_float * len(vertices))(*vertices),  # 謎のctypes
        GL_STATIC_DRAW,
    )
    glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
    glBufferData(
        GL_ARRAY_BUFFER,
        len(colors) * 4,  # byte size
        (ctypes.c_float * len(colors))(*colors),  # 謎のctypes
        GL_STATIC_DRAW,
    )
    return buffers


def draw_vbo():
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
    glVertexPointer(3, GL_FLOAT, 0, None)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
    glColorPointer(3, GL_FLOAT, 0, None)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[2])
    glPointSize(30)
    glDrawArrays(GL_POINTS, 0, len(vertices))
    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)


def draw_cube2():
    global buffers
    if isinstance(buffers, int):
        buffers = create_vbo()
    draw_vbo()


def initialize():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)


def GLresize(Width, Height):
    # viewport
    if Height == 0:
        Height = 1
    glViewport(0, 0, Width, Height)
    # projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)


yaw = 0
pitch = 0


def draw():
    # global yaw, pitch
    # clear
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # view
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # yaw += 0.39  # 横
    # pitch += 1.27  # 縦
    glTranslatef(0.0, 0.0, -2.0)
    # glRotatef(yaw, 0, 1, 0)
    # glRotatef(pitch, 1, 0, 0)

    # cube
    draw_cube2()

    glFlush()


def reshape_func(w, h):
    GLresize(w, h == 0 and 1 or h)


def disp_func():
    draw()
    glutSwapBuffers()


if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(256, 256)
    glutCreateWindow(b"vbo")
    glutDisplayFunc(disp_func)
    glutIdleFunc(disp_func)
    glutReshapeFunc(reshape_func)

    initialize()

    glutMainLoop()
