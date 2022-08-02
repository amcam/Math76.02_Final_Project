import numpy as np
import open3d as o3d

mesh = o3d.io.read_triangle_mesh("OUTPUT_ROCKS.ply")

"""
print("Testing IO for meshes ...")
knot_data = o3d.data.KnotMesh()
mesh = o3d.io.read_triangle_mesh(knot_data.path)
print(mesh)
o3d.io.write_triangle_mesh("copy_of_knot.ply", mesh)
"""

print("Computing normal and rendering it.")
mesh.compute_vertex_normals()
print(np.asarray(mesh.triangle_normals))
print("Painting the mesh")
mesh.paint_uniform_color([1, 0.706, 0])
o3d.visualization.draw_geometries([mesh])
