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
from libs.variable import saveName, imgName1, imgName2, renderingPly

# from libs import capture

LeftButtonOn = False
RightButtonOn = False
Angle1 = 0
Angle2 = 0
Distance = 1.0
px, py = -1, -1
windowSize = 512
angleRange = 5.0


mesh_fi1 = "./mesh/" + imgName1 + ".ply"
mesh_fi2 = "./mesh/" + imgName2 + ".ply"
mesh_fi3 = "./mesh/" + saveName + "_integrated" + ".ply"
mesh_fi4 = "./mesh/" + saveName + ".ply"

mesh_fiList = [mesh_fi1, mesh_fi2, mesh_fi3, mesh_fi4]


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


def create_vbo0():
    buffers = glGenBuffers(3)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
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
    return buffers


def draw_vbo0():
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
    glVertexPointer(3, GL_FLOAT, 0, None)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
    glColorPointer(3, GL_FLOAT, 0, None)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[2])
    glPointSize(3)
    glDrawArrays(GL_POINTS, 0, len(verticesList[0]))
    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)


def draw_ply0():
    global buffers
    if isinstance(buffers, int):
        buffers = create_vbo0()
    draw_vbo0()


def draw0():
    global Angle1, Angle2, verts

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, Distance, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0)
    glRotatef(Angle1, 0, 1, 0)
    glRotatef(Angle2, 1, 0, 0)
    draw_ply0()
    glFlush()
    glutSwapBuffers()


def disp_func0():
    draw0()
    glutSwapBuffers()


def create_vbo1():
    buffers = glGenBuffers(3)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
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
    return buffers


def draw_vbo1():
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
    glVertexPointer(3, GL_FLOAT, 0, None)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
    glColorPointer(3, GL_FLOAT, 0, None)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[2])
    glPointSize(3)
    glDrawArrays(GL_POINTS, 0, len(verticesList[1]))
    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)


def draw_ply1():
    global buffers
    if isinstance(buffers, int):
        buffers = create_vbo1()
    draw_vbo1()


def draw1():
    global Angle1, Angle2, verts

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, Distance, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0)
    glRotatef(Angle1, 0, 1, 0)
    glRotatef(Angle2, 1, 0, 0)
    draw_ply1()
    glFlush()
    glutSwapBuffers()


def disp_func1():
    draw1()
    glutSwapBuffers()


def create_vbo2():
    buffers = glGenBuffers(3)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
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


def draw_vbo2():
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
    glVertexPointer(3, GL_FLOAT, 0, None)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
    glColorPointer(3, GL_FLOAT, 0, None)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[2])
    glPointSize(3)
    glDrawArrays(GL_POINTS, 0, len(verticesList[2]))
    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)


def draw_ply2():
    global buffers
    if isinstance(buffers, int):
        buffers = create_vbo2()
    draw_vbo2()


def draw2():
    global Angle1, Angle2, verts

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, Distance, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0)
    glRotatef(Angle1, 0, 1, 0)
    glRotatef(Angle2, 1, 0, 0)
    draw_ply2()
    glFlush()
    glutSwapBuffers()


def disp_func2():
    draw2()
    glutSwapBuffers()


def create_vbo3():
    buffers = glGenBuffers(3)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
    glBufferData(
        GL_ARRAY_BUFFER,
        len(verticesList[3]) * 4,  # byte size
        (ctypes.c_float * len(verticesList[3]))(*verticesList[3]),  # 謎のctypes
        GL_STATIC_DRAW,
    )
    glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
    glBufferData(
        GL_ARRAY_BUFFER,
        len(colorsList[3]) * 4,  # byte size
        (ctypes.c_float * len(colorsList[3]))(*colorsList[3]),  # 謎のctypes
        GL_STATIC_DRAW,
    )
    return buffers


def draw_vbo3():
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
    glVertexPointer(3, GL_FLOAT, 0, None)
    glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
    glColorPointer(3, GL_FLOAT, 0, None)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[2])
    glPointSize(3)
    glDrawArrays(GL_POINTS, 0, len(verticesList[3]))
    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)


def draw_ply3():
    global buffers
    if isinstance(buffers, int):
        buffers = create_vbo3()
    draw_vbo3()


def draw3():
    global Angle1, Angle2, verts

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, Distance, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0)
    glRotatef(Angle1, 0, 1, 0)
    glRotatef(Angle2, 1, 0, 0)
    draw_ply3()
    glFlush()
    glutSwapBuffers()


def disp_func3():
    draw3()
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
mode = 4
print(mode)
# mode = input()
if mode == 1:
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(windowSize, windowSize)
    winnum.append(glutCreateWindow(imgName1))
    glutDisplayFunc(disp_func0)
    glutIdleFunc(disp_func0)
    glutReshapeFunc(reshape_func)
    initialize()
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)

elif mode == 2:
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(windowSize, windowSize)
    winnum.append(glutCreateWindow(imgName2))
    glutDisplayFunc(disp_func1)
    glutIdleFunc(disp_func1)
    glutReshapeFunc(reshape_func)
    initialize()
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)

elif mode == 3:
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(windowSize, windowSize)
    winnum.append(glutCreateWindow("integrated"))
    glutDisplayFunc(disp_func2)
    glutIdleFunc(disp_func2)
    glutReshapeFunc(reshape_func)
    initialize()
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    # print("test")
elif mode == 4:
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(windowSize, windowSize)
    winnum.append(glutCreateWindow("M"))
    glutDisplayFunc(disp_func3)
    glutIdleFunc(disp_func3)
    glutReshapeFunc(reshape_func)
    initialize()
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    # print("test")
glutMainLoop()
