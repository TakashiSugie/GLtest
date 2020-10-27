import copy
import numpy as np
import open3d as o3d
# fdsafd

if __name__ == "__main__":
    #mesh = o3d.io.read_triangle_mesh("04_04.ply")
    mesh = o3d.io.read_triangle_mesh("sample.obj")
    print(mesh)
    print(np.asarray(mesh.vertices))  # verts
    print(np.asarray(mesh.triangles))  # faces

    o3d.visualization.draw_geometries([mesh])
    print("tew")
