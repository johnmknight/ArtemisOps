"""
Process the Artemis II patch - handle white background.
"""
from PIL import Image
from pathlib import Path

def process_with_white_bg(input_path, output_path, tolerance=30):
    """Remove white background from image"""
    img = Image.open(input_path)
    
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    pixels = img.load()
    width, height = img.size
    transparent_count = 0
    
    print(f"Processing {width}x{height} image...")
    print(f"Removing white background (tolerance={tolerance})...")
    
    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            
            # Check if pixel is near white
            if r >= (255 - tolerance) and g >= (255 - tolerance) and b >= (255 - tolerance):
                pixels[x, y] = (r, g, b, 0)
                transparent_count += 1
    
    print(f"Made {transparent_count:,} pixels transparent ({100*transparent_count/(width*height):.1f}%)")
    
    img.save(output_path, 'PNG')
    print(f"Saved to {output_path}")
    
    return img

if __name__ == "__main__":
    input_file = r"C:\Users\john_\ArtemisOps\client\assets\patches\artemis-ii-patch-nasa.jpg"
    output_file = r"C:\Users\john_\ArtemisOps\client\assets\patches\artemis-ii-patch.png"
    
    process_with_white_bg(input_file, output_file, tolerance=20)
