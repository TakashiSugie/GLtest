from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


LeftButtonOn = False
RightButtonOn = False
Angle1 = 0
Angle2 = 0
Distance = 7.0


def resize(w, h):
    print("resize", w, h)
    # Windowの左から100, 下から100, 幅w/2, 高さh/2をビューポートにする
    glViewport(50, 150, w / 2, h / 2)


def mouse(button, state, x, y):
    global LeftButtonOn, RightButtonOn
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_UP:
            LeftButtonOn = False
        elif state == GLUT_DOWN:
            LeftButtonOn = True

    # if(button == GLUT_LEFT_BUTTON){
    #     if(state == GLUT_UP){
    #     LeftButtonOn = false;
    #     }else if(state == GLUT_DOWN){
    #     LeftButtonOn = true;
    #     }
    # }

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_UP:
            RightButtonOn = False
        elif state == GLUT_DOWN:
            RightButtonOn = True

    # if(button == GLUT_RIGHT_BUTTON){
    #     if(state == GLUT_UP){
    #     RightButtonOn = false;
    #     }else if(state == GLUT_DOWN){
    #     RightButtonOn = true;
    #     }
    # }
    print(x, y)


def motion(x, y):
    # print("motion:")
    global RightButtonOn, LeftButtonOn, Angle1, Angle2, Distance
    px, py = -1, -1
    if LeftButtonOn == True and RightButtonOn == True:
        Angle1 = 0
        Angle2 = 0
        gluLookAt(0, 0, 0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    elif LeftButtonOn == True:
        if px >= 0 and py >= 0:
            Angle1 += -(x - px) / 50
            Angle2 += (y - py) / 50
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
    if key == "\033":  # Escape
        sys.exit()
    elif key == "q":
        sys.exit()
    else:
        print(key)
