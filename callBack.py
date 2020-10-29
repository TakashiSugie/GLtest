from OpenGL.GL import *
from OpenGL.GLUT import *


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
    print("motion:")


def keyboard(key, x, y):
    if key == "\033":  # Escape
        sys.exit()
    elif key == "q":
        sys.exit()
    else:
        print(key)
