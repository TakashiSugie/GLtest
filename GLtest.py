import moderngl
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import cv2

# OpenGL コンテキスト
ctx = moderngl.create_standalone_context()


def setVerts(img, depthImg):
    verts = []
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            colors = float(img[x][y])/255.0
            vert = np.array(
                [x, y, depthImg[x][y], colors[0], colors[1], colors[2]])
            verts.append(vert)
    return np.array(verts)

# 中心は0 0 0


def testVerts():
    # 頂点情報 (x,y,z,r,g,b)
    verts = np.array([
        0.5,  0.5, 0.0, 1.0, 1.0, 1.0,
        -0.5,  0.5, 0.0, 1.0, 1.0, 1.0,
        -0.5, -0.2, 0.0, 1.0, 1.0, 1.0,
        0.0, 0.0, 0.0, 0.0, 1.0, 1.0
    ])
    return verts


def renderingSet(verts):
    vbo = ctx.buffer(verts.astype('float32').tobytes())
    prog = ctx.program(
        vertex_shader='''
            # version 330
            in vec3 in_vert;
            in vec3 in_color;
            out vec3 v_color;

            void main() {
                v_color = in_color;
                gl_Position = vec4(in_vert, 1.0);
            }
        ''',
        fragment_shader='''
            # version 330
            in vec3 v_color;
            out vec4 f_color;
            void main() {
                f_color = vec4(v_color, 1.0);
            }
        '''
    )
    vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_color')
    fbo = ctx.simple_framebuffer((500, 500))
    fbo.use()
    fbo.clear(0.0, 0.0, 0.0, 1.0)
    return vao, fbo


def rendering(vao, fbo):
    vao.render()
    myimg = Image.frombytes('RGB', fbo.size, fbo.read(), 'raw', 'RGB', 0, -1)
    plt.imshow(myimg)
    plt.show()


if __name__ == "__main__":
    verts = testVerts()
    img = cv2.imread("./data/04_04.png")
    depthImg = cv2.imread("./data/04_04_depth.png", 0)
    #verts = setVerts(img, depthImg)
    print(verts.shape)
    vao, fbo = renderingSet(verts)
    rendering(vao, fbo)
