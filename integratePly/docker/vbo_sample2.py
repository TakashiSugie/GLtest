import moderngl
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

# OpenGL コンテキスト
ctx = moderngl.create_standalone_context()

# 頂点情報 (x,y,z,r,g,b)
vertices = np.array(
    [
        0.5,
        0.5,
        0.0,
        1.0,
        0.0,
        0.0,
        -0.5,
        0.5,
        0.0,
        0.0,
        1.0,
        0.0,
        -0.5,
        -0.5,
        0.0,
        0.0,
        0.0,
        1.0,
    ]
)
vbo = ctx.buffer(vertices.astype("float32").tobytes())

# シェーダープログラム
prog = ctx.program(
    vertex_shader="""
        #version 330
        in vec3 in_vert;
        in vec3 in_color;
        out vec3 v_color;

        void main() {
            v_color = in_color;
            gl_Position = vec4(in_vert, 1.0);
        }
    """,
    fragment_shader="""
        #version 330
        in vec3 v_color;
        out vec4 f_color;
        void main() {
            f_color = vec4(v_color, 1.0);
        }
    """,
)

# 色情報の引数を増やしています
vao = ctx.simple_vertex_array(prog, vbo, "in_vert", "in_color")

# 2D フレームの作成
fbo = ctx.simple_framebuffer((500, 500))
fbo.use()
fbo.clear(0.0, 0.0, 0.0, 1.0)

# レンダリングの実行
vao.render()

# RAW 画像から ndarray に変換して描画
myimg = Image.frombytes("RGB", fbo.size, fbo.read(), "raw", "RGB", 0, -1)
plt.imshow(myimg)
plt.show()
