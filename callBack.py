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
    if button == GLUT_LEFT_BUTTON:
        print("left")
    elif button == GLUT_MIDDLE_BUTTON:
        print("middle")
    elif button == GLUT_RIGHT_BUTTON:
        print("right")
    else:
        print("unknown button:")

    if state == GLUT_DOWN:
        print("down")
    elif state == GLUT_UP:
        print("up")
    else:
        print("unknown state:")

    print(x, y)


def motion(x, y):
    # print("motion:")
    global RightButtonOn, LeftButtonOn, Angle1, Angle2, Distance
    px, py = -1, -1
    # static  int px = -1, py = -1
    if LeftButtonOn == True and RightButtonOn == True:
        Angle1 = 0
        Angle2 = 0
        gluLookAt(0, 0, 0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    # if(LeftButtonOn == true&&RightButtonOn == true){
    #     Angle1=0;
    #     Angle2=0;
    #     gluLookAt(0,0,0,0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
    # }
    elif LeftButtonOn == True:
        if px >= 0 and py >= 0:
            Angle1 += -(x - px) / 50
            Angle2 += (y - py) / 50
        px = x
        py = y
    # else if(LeftButtonOn == true){
    #     if(px >= 0 && py >= 0){
    #     Angle1 += (double)-(x - px)/50;
    #     Angle2 += (double)(y - py)/50;
    #     }
    #     px = x;
    #     py = y;
    # }
    elif RightButtonOn == True:
        if px >= 0 and py >= 0:
            Distance += float(y - py) / 20
        px = x
        py = y
    else:
        px = -1
        py = -1

    # else if(RightButtonOn == true){
    #     if(px >= 0 && py >= 0){
    #     Distance += (double)(y - py)/20;
    #     }
    #     px = x;
    #     py = y;
    # }else{
    #     px = -1;
    #     py = -1;
    # }
    glutPostRedisplay()


def keyboard(key, x, y):
    if key == "\033":  # Escape
        sys.exit()
    elif key == "q":
        sys.exit()
    else:
        print(key)
