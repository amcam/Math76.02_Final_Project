import numpy as np
import extract_array
from matplotlib import pyplot as plt 
import time as tm
import open3d as o3d 


# Create Simple PLY Array of Points and Array of Triangles
pointsOut = [(0,0,0),(0,0,1),(0,1,1),(0,1,0),(1,0,0),(1,0,1),(1,1,1),(1,1,0)]
							#fl0     bl1     fr2     br3      btm4         top5

trianglesOut = [(0,1,2),(0,2,3),(7,6,5),(7,5,4),(0,4,5),(0,5,1),(1,5,6),(1,6,2),(2,6,7),(2,7,3),(3,7,4),(3,4,0)]



# Write to file

# open file for writing
file = open("examplePrism.ply","w")

file.write("ply\n")
file.write("format ascii 1.0\n")
file.write("element vertex " + str(len(pointsOut)) + "\n")
file.write("property float x\n")
file.write("property float y\n")
file.write("property float z\n")
file.write("element face " + str(len(trianglesOut)) + "\n")
file.write("property list uchar int vertex_index\n")
file.write("end_header\n")


for i in range(0,len(pointsOut)):
	print(pointsOut[i])
	file.write(str(pointsOut[i][0]) + " " + str(pointsOut[i][1]) + " " + str(pointsOut[i][2]) + "\n")

for i in range(0, len(trianglesOut)):
	print(trianglesOut[i])
	file.write("3 " + str(trianglesOut[i][0]) + " " + str(trianglesOut[i][1]) + " " + str(trianglesOut[i][2]) + "\n")

file.close()

# open file for

mesh = o3d.io.read_triangle_mesh("examplePrism.ply")

"""
print("Testing IO for meshes ...")
knot_data = o3d.data.KnotMesh()
mesh = o3d.io.read_triangle_mesh(knot_data.path)
print(mesh)
o3d.io.write_triangle_mesh("copy_of_knot.ply", mesh)
"""
""
print("Computing normal and rendering it.")
mesh.compute_vertex_normals()
print(np.asarray(mesh.triangle_normals))
o3d.visualization.draw_geometries([mesh])
