from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys


buffers = None
buffers = glGenBuffers(3)
print(buffers[0])
print(type(buffers))
