#!env python

# レンダリング三枚の縮尺を揃える（max minを共有すれば行けそう）
# 実際にW座標系で統合を行う（両方の点群を足し合わせるだけで良い）


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import cv2

# from evaluation import checkMaxMin
from setVerts import setVertsFromPly, cvtVerts, setVertsFromPlySame
from libs.variable import saveName, imgName1, imgName2, renderingMode, renderingPly

# from libs import capture

LeftButtonOn = False
RightButtonOn = False
Angle1 = 0
Angle2 = 0
Distance = 1.0
px, py = -1, -1
windowSize = 512
angleRange = 5.0

# if renderingMode == 1:
#     plyName = imgName1
# elif renderingMode == 2:
#     plyName = imgName2
# elif renderingMode == 3:
#     plyName = saveName
# elif renderingMode == 4:
#     plyName = saveName + "_integrated"
mesh_fi1 = "./mesh/" + imgName1 + ".ply"
mesh_fi2 = "./mesh/" + imgName2 + ".ply"
mesh_fi3 = "./mesh/" + saveName + "_integrated" + ".ply"
# print(renderingPly[renderingMode])

mesh_fiList = [mesh_fi1, mesh_fi2, mesh_fi3]


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
        Distance = 1.0
        gluLookAt(0, 0, 7.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    elif LeftButtonOn == True:
        if py >= 0 and px >= 0:
            Angle1 += float(-(y - py) / 50)
            Angle2 += float((x - px) / 50)
        px = x
        py = y
    elif RightButtonOn == True:
        if px >= 0 and py >= 0:
            Distance += float(y - py) / 200
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
    elif key.decode() == "d":
        Angle2 += 1.0
        glutPostRedisplay()
    elif key.decode() == "a":
        Angle2 -= 1.0
        glutPostRedisplay()
    elif key.decode() == "w":
        Angle1 += 1.0
        glutPostRedisplay()

    elif key.decode() == "s":
        Angle1 -= 1.0
        glutPostRedisplay()
    elif key.decode() == "d":
        Distance += 0.5
        glutPostRedisplay()

    elif key.decode() == "D":
        Distance -= 0.5
        glutPostRedisplay()

    elif key.decode() == "c":
        capture()
    else:
        print(key.decode())


buffers = 0


def create_vbo(mode):
    buffers = glGenBuffers(3)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
    if mode == 1:
        glBufferData(
            GL_ARRAY_BUFFER,
            len(verticesList[0]) * 4,  # byte size
            (ctypes.c_float * len(verticesList[0]))(*verticesList[0]),  # 謎のctypes
            GL_STATIC_DRAW,
        )
        glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
        glBufferData(
            GL_ARRAY_BUFFER,
            len(colorsList[0]) * 4,  # byte size
            (ctypes.c_float * len(colorsList[0]))(*colorsList[0]),  # 謎のctypes
            GL_STATIC_DRAW,
        )
    elif mode == 2:
        glBufferData(
            GL_ARRAY_BUFFER,
            len(verticesList[1]) * 4,  # byte size
            (ctypes.c_float * len(verticesList[1]))(*verticesList[1]),  # 謎のctypes
            GL_STATIC_DRAW,
        )
        glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
        glBufferData(
            GL_ARRAY_BUFFER,
            len(colorsList[1]) * 4,  # byte size
            (ctypes.c_float * len(colorsList[1]))(*colorsList[1]),  # 謎のctypes
            GL_STATIC_DRAW,
        )
    elif mode == 3:
        glBufferData(
            GL_ARRAY_BUFFER,
            len(verticesList[2]) * 4,  # byte size
            (ctypes.c_float * len(verticesList[2]))(*verticesList[2]),  # 謎のctypes
            GL_STATIC_DRAW,
        )
        glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
        glBufferData(
            GL_ARRAY_BUFFER,
            len(colorsList[2]) * 4,  # byte size
            (ctypes.c_float * len(colorsList[2]))(*colorsList[2]),  # 謎のctypes
            GL_STATIC_DRAW,
        )

    return buffers


def draw_vbo(mode):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
    glVertexPointer(3, GL_FLOAT, 0, None)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
    glColorPointer(3, GL_FLOAT, 0, None)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[2])
    glPointSize(3)
    if mode == 1:
        glDrawArrays(GL_POINTS, 0, len(verticesList[0]))
    elif mode == 2:
        glDrawArrays(GL_POINTS, 0, len(verticesList[1]))
    elif mode == 3:
        glDrawArrays(GL_POINTS, 0, len(verticesList[2]))

    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)


def draw_ply(mode):
    global buffers
    if isinstance(buffers, int):
        buffers = create_vbo(mode)
    draw_vbo(mode)


def draw():
    global Angle1, Angle2, verts

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, Distance, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0)
    glRotatef(Angle1, 0, 1, 0)
    glRotatef(Angle2, 1, 0, 0)
    draw_ply()
    glFlush()
    glutSwapBuffers()


def drawImg1():
    global Angle1, Angle2, verts
    glutSetWindow(winnum[0])

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, Distance, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0)
    glRotatef(Angle1, 0, 1, 0)
    glRotatef(Angle2, 1, 0, 0)
    draw_ply(mode=1)
    glFlush()
    glutSwapBuffers()


def drawImg2():
    global Angle1, Angle2, verts
    glutSetWindow(winnum[1])

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, Distance, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0)
    glRotatef(Angle1, 0, 1, 0)
    glRotatef(Angle2, 1, 0, 0)
    draw_ply(mode=2)
    glFlush()
    glutSwapBuffers()


def drawIntegrated():
    global Angle1, Angle2, verts
    glutSetWindow(winnum[2])

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, Distance, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0)
    glRotatef(Angle1, 0, 1, 0)
    glRotatef(Angle2, 1, 0, 0)
    draw_ply(mode=3)
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


def disp_func(mode):
    if mode == 1:
        drawImg1()
    elif mode == 2:
        drawImg2()
    if mode == 3:
        drawIntegrated()
    glutSwapBuffers()


# def myGLinit():

winnum = []
verticesList, colorsList = [], []
for mesh_fi in mesh_fiList:
    # verts = setVertsFromPly(mesh_fi)
    verts = setVertsFromPlySame(mesh_fi)
    colors, vertices = cvtVerts(verts)
    colorsList.append(colors)
    verticesList.append(vertices)
print("verts loaded")
glutInit(sys.argv)

glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(windowSize, windowSize)
winnum.append(glutCreateWindow(imgName1))
print("test")
# glutCreateWindow(renderingPly[renderingMode])
glutDisplayFunc(disp_func(1))
glutIdleFunc(disp_func(1))
glutReshapeFunc(reshape_func)
initialize()
print("test")
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutMotionFunc(motion)
print("test")


glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(windowSize, windowSize)
winnum.append(glutCreateWindow(imgName2))
# glutCreateWindow(renderingPly[renderingMode])
glutDisplayFunc(disp_func(2))
glutIdleFunc(disp_func(2))
glutReshapeFunc(reshape_func)
initialize()
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutMotionFunc(motion)

glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(windowSize, windowSize)
winnum.append(glutCreateWindow("integrated"))
# glutCreateWindow(renderingPly[renderingMode])
glutDisplayFunc(disp_func(3))
glutIdleFunc(disp_func(3))
glutReshapeFunc(reshape_func)
initialize()
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutMotionFunc(motion)


glutMainLoop()
