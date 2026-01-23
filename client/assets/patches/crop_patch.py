"""
Extract and crop the Artemis II patch from the virtual background image.
The patch is located on the left side of the image.
"""
from PIL import Image
from pathlib import Path

def find_patch_bounds(img):
    """Find the bounding box of non-transparent content"""
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Get alpha channel
    alpha = img.split()[3]
    bbox = alpha.getbbox()  # Returns (left, top, right, bottom)
    
    return bbox

def extract_patch(input_path, output_path):
    """Extract just the patch from the larger image"""
    img = Image.open(input_path)
    print(f"Input size: {img.size}")
    
    # Find non-transparent bounds
    bbox = find_patch_bounds(img)
    print(f"Content bounds: {bbox}")
    
    if bbox:
        # Add some padding
        padding = 20
        left = max(0, bbox[0] - padding)
        top = max(0, bbox[1] - padding)
        right = min(img.width, bbox[2] + padding)
        bottom = min(img.height, bbox[3] + padding)
        
        # Crop to content
        cropped = img.crop((left, top, right, bottom))
        print(f"Cropped size: {cropped.size}")
        
        # Save
        cropped.save(output_path, 'PNG')
        print(f"Saved to {output_path}")
        
        return cropped
    else:
        print("No content found!")
        return None

if __name__ == "__main__":
    input_file = r"C:\Users\john_\ArtemisOps\client\assets\patches\artemis-ii-patch-transparent.png"
    output_file = r"C:\Users\john_\ArtemisOps\client\assets\patches\artemis-ii-patch-cropped.png"
    
    extract_patch(input_file, output_file)
