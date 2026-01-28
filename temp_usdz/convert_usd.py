"""
Convert USDC (Universal Scene Description) to GLB format
"""

from pxr import Usd, UsdGeom, UsdShade, Gf
import json
import struct
import base64
import os

def convert_usd_to_gltf(usd_path, output_path, texture_dir):
    """Convert USD file to GLB/GLTF format"""
    
    # Open USD stage
    stage = Usd.Stage.Open(usd_path)
    if not stage:
        print(f"Failed to open {usd_path}")
        return False
    
    print(f"Opened USD stage: {usd_path}")
    print(f"Default prim: {stage.GetDefaultPrim()}")
    
    # List all prims
    print("\nPrims in stage:")
    for prim in stage.Traverse():
        print(f"  {prim.GetPath()} - Type: {prim.GetTypeName()}")
    
    return True

if __name__ == "__main__":
    usd_path = r"C:\Users\john_\ArtemisOps\temp_usdz\extracted\ISS_stationary.usdc"
    texture_dir = r"C:\Users\john_\ArtemisOps\temp_usdz\extracted\0"
    output_path = r"C:\Users\john_\ArtemisOps\client\assets\iss-stationary.glb"
    
    convert_usd_to_gltf(usd_path, output_path, texture_dir)
