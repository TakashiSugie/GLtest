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
from time import time

# from evaluation import checkMaxMin
from setVerts import setVertsFromPly, cvtVerts

# from libs.variable import saveName, imgName1, imgName2, renderingMode, renderingPly

# from libs import capture

LeftButtonOn = False
RightButtonOn = False
Angle1 = 0
Angle2 = 0
Distance = 1.0
px, py = -1, -1
windowSize = 512
angleRange = 5.0
key = input()
if key == "in":
    plyName = "integrated"
elif key == "0":
    plyName = "0"
else:
    raise Exception("plyName is invalid")
mesh_fi = "./mesh/" + plyName + ".ply"
# print(renderingPly[renderingMode])


def capture():
    if not os.path.isdir("./capture/%s" % plyName):
        os.makedirs("./capture/%s" % plyName)
    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)
    # キャプチャ
    glReadBuffer(GL_FRONT)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_BGRA, GL_UNSIGNED_BYTE, None)

    image = np.frombuffer(data, dtype=np.uint8).reshape(width, height, 4)
    # capturePath = mesh_fi.replace("ply", "png")
    cv2.imwrite(
        "./capture/%s/%s_%.1f_%.1f_%d.png"
        % (plyName, plyName, Angle1, Angle2, Distance),
        np.flipud(image),
    )
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
    global Angle2, Angle1, Distance
    if key.decode() == "\033":  # Escape
        sys.exit()
    elif key.decode() == "q":
        sys.exit()
    elif key.decode() == "h":
        Angle2 += 0.1
        glutPostRedisplay()
    elif key.decode() == "H":
        Angle2 -= 0.1
        glutPostRedisplay()
    elif key.decode() == "v":
        Angle1 += 0.1
        glutPostRedisplay()

    elif key.decode() == "V":
        Angle1 -= 0.1
        glutPostRedisplay()
    elif key.decode() == "d":
        Distance += 3
        glutPostRedisplay()

    elif key.decode() == "D":
        Distance -= 3
        glutPostRedisplay()

    elif key.decode() == "s":
        capture()
    else:
        print(key.decode())


def resize_cb(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(angleRange, w / h, 1, 1000.0)  # 視体積を設定することができる
    glMatrixMode(GL_MODELVIEW)


def draw_():
    global Angle1, Angle2, verts

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
    glPointSize(3)
    glBegin(GL_POINTS)
    start = time()
    for vert in verts:
        glColor3d(vert[3], vert[4], vert[5])
        glVertex3f(vert[0], vert[1], -vert[2])

    print("now loop", time() - start)

    glEnd()
    glFlush()
    glutSwapBuffers()


buffers = 0


def create_vbo():
    buffers = glGenBuffers(3)
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
    glPointSize(3)
    glDrawArrays(GL_POINTS, 0, len(vertices))
    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)


def draw_cube2():
    global buffers
    if isinstance(buffers, int):
        buffers = create_vbo()
    draw_vbo()


def draw():
    global Angle1, Angle2, verts

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glLoadIdentity()

    glMatrixMode(GL_MODELVIEW)
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
    draw_cube2()
    glFlush()
    glutSwapBuffers()


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


def reshape_func(w, h):
    GLresize(w, h == 0 and 1 or h)


def disp_func():
    draw()
    glutSwapBuffers()


glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(windowSize, windowSize)
glutCreateWindow("PyOpenGL 11")
glutDisplayFunc(disp_func)
glutIdleFunc(disp_func)
glutReshapeFunc(reshape_func)

initialize()

glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutMotionFunc(motion)
# print("GPU: ", glGetString(GL_VERSION))
# verts_np3d = setVertsFromNpy()
verts = setVertsFromPly(mesh_fi)
colors, vertices = cvtVerts(verts)

# verts = list(verts_np)
# cNP, vNP = splitVerts(verts)
# print("before loop", time() - start)
# print("len_verts:", len(verts))

glutMainLoop()
