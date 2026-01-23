"""
Check and process the NASA Artemis II patch image.
"""
from PIL import Image
from pathlib import Path

def analyze_image(img_path):
    """Analyze an image for transparency and dominant colors"""
    img = Image.open(img_path)
    print(f"File: {img_path}")
    print(f"Format: {img.format}, Mode: {img.mode}, Size: {img.size}")
    
    # Check for transparency
    if img.mode == 'RGBA':
        alpha = img.split()[3]
        extrema = alpha.getextrema()
        print(f"Alpha range: {extrema}")
        if extrema[0] < 255:
            print("Has transparency!")
        else:
            print("No transparency (all opaque)")
    else:
        print("No alpha channel")
    
    # Sample corners
    if img.mode != 'RGB':
        img_rgb = img.convert('RGB')
    else:
        img_rgb = img
    
    pixels = img_rgb.load()
    w, h = img_rgb.size
    
    corners = [
        ("Top-left", pixels[10, 10]),
        ("Top-right", pixels[w-10, 10]),
        ("Bottom-left", pixels[10, h-10]),
        ("Bottom-right", pixels[w-10, h-10]),
        ("Center", pixels[w//2, h//2]),
    ]
    
    print("\nSample pixel colors:")
    for name, color in corners:
        print(f"  {name}: RGB{color}")
    
    return img

def process_with_black_bg(input_path, output_path, tolerance=30):
    """Remove black background from image"""
    img = Image.open(input_path)
    
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    pixels = img.load()
    width, height = img.size
    transparent_count = 0
    
    print(f"\nProcessing {width}x{height} image...")
    
    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            
            # Check if pixel is near black
            if r <= tolerance and g <= tolerance and b <= tolerance:
                pixels[x, y] = (r, g, b, 0)
                transparent_count += 1
    
    print(f"Made {transparent_count:,} pixels transparent ({100*transparent_count/(width*height):.1f}%)")
    
    img.save(output_path, 'PNG')
    print(f"Saved to {output_path}")
    
    return img

if __name__ == "__main__":
    input_file = r"C:\Users\john_\ArtemisOps\client\assets\patches\artemis-ii-patch-nasa.jpg"
    output_file = r"C:\Users\john_\ArtemisOps\client\assets\patches\artemis-ii-patch.png"
    
    # First analyze
    analyze_image(input_file)
    
    # Then process
    process_with_black_bg(input_file, output_file, tolerance=25)
