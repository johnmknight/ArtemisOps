"""
Patch Image Processor
Downloads, checks transparency, and removes background from mission patches.
"""
from PIL import Image
import sys
from pathlib import Path
import colorsys

def has_transparency(img):
    """Check if image has any transparent pixels"""
    if img.mode == 'RGBA':
        # Get alpha channel stats
        alpha = img.split()[3]
        extrema = alpha.getextrema()
        # If min alpha < 255, there's some transparency
        return extrema[0] < 255
    return False

def get_dominant_corner_color(img, sample_size=20):
    """Sample corners to detect background color"""
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    pixels = img.load()
    width, height = img.size
    samples = []
    
    # Sample from all four corners
    for x in range(sample_size):
        for y in range(sample_size):
            samples.append(pixels[x, y])  # Top-left
    for x in range(width - sample_size, width):
        for y in range(sample_size):
            samples.append(pixels[x, y])  # Top-right
    for x in range(sample_size):
        for y in range(height - sample_size, height):
            samples.append(pixels[x, y])  # Bottom-left
    for x in range(width - sample_size, width):
        for y in range(height - sample_size, height):
            samples.append(pixels[x, y])  # Bottom-right
    
    # Calculate average
    avg_r = sum(c[0] for c in samples) // len(samples)
    avg_g = sum(c[1] for c in samples) // len(samples)
    avg_b = sum(c[2] for c in samples) // len(samples)
    
    return (avg_r, avg_g, avg_b)

def remove_background(img, bg_color, tolerance=30):
    """Remove pixels similar to background color"""
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    pixels = img.load()
    width, height = img.size
    transparent_count = 0
    
    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            
            # Check if pixel is close to background
            if (abs(r - bg_color[0]) <= tolerance and 
                abs(g - bg_color[1]) <= tolerance and 
                abs(b - bg_color[2]) <= tolerance):
                pixels[x, y] = (r, g, b, 0)
                transparent_count += 1
    
    print(f"  Made {transparent_count:,} pixels transparent ({100*transparent_count/(width*height):.1f}%)")
    return img

def process_patch(input_path, output_path=None, force_bg_color=None, tolerance=30):
    """Main processing function"""
    input_path = Path(input_path)
    
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}-transparent.png"
    else:
        output_path = Path(output_path)
    
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    
    # Open image
    img = Image.open(input_path)
    print(f"Format: {img.format}, Mode: {img.mode}, Size: {img.size}")
    
    # Convert to RGBA
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Check for existing transparency
    if has_transparency(img):
        print("Image already has transparency!")
        img.save(output_path, 'PNG')
        print(f"Saved to {output_path}")
        return output_path
    
    # Detect or use forced background color
    if force_bg_color:
        bg_color = force_bg_color
        print(f"Using forced background color: RGB{bg_color}")
    else:
        bg_color = get_dominant_corner_color(img)
        print(f"Detected background color: RGB{bg_color}")
    
    # Remove background
    print("Removing background...")
    img = remove_background(img, bg_color, tolerance)
    
    # Save
    img.save(output_path, 'PNG')
    print(f"Saved to {output_path}")
    
    return output_path

if __name__ == "__main__":
    # Process the Artemis II patch background image
    # The background is black (0,0,0)
    input_file = r"C:\Users\john_\ArtemisOps\client\assets\patches\artemis-ii-background.png"
    output_file = r"C:\Users\john_\ArtemisOps\client\assets\patches\artemis-ii-patch-transparent.png"
    
    process_patch(input_file, output_file, force_bg_color=(0, 0, 0), tolerance=25)
