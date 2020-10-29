def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON:
        print "left",
    elif button == GLUT_MIDDLE_BUTTON:
        print "middle",
    elif button == GLUT_RIGHT_BUTTON:
        print "right",
    else:
        print "unknown button:", button,

    if state == GLUT_DOWN:
        print "down",
    elif state == GLUT_UP:
        print "up",
    else:
        print "unknown state:", state,

    print (x, y)


def motion(x, y):
    print "motion:", x, y
