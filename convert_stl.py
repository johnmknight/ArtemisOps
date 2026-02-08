import trimesh
import os

stl_path = r"C:\Users\john_\dev\ArtemisOps\client\assets\models\orion_capsule.stl"
glb_path = r"C:\Users\john_\dev\ArtemisOps\client\assets\models\orion_capsule.glb"

print(f"Loading STL: {stl_path}")
print(f"File size: {os.path.getsize(stl_path)} bytes")

mesh = trimesh.load(stl_path)
print(f"Vertices: {len(mesh.vertices)}, Faces: {len(mesh.faces)}")
print(f"Bounds: {mesh.bounds}")

# Center the mesh
mesh.vertices -= mesh.centroid

# Export as GLB
mesh.export(glb_path, file_type='glb')
print(f"Exported GLB: {os.path.getsize(glb_path)} bytes")
print("Done!")
