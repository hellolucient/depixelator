from PIL import Image
import numpy as np
import json
import os
from collections import defaultdict

def analyze_pixel_art(image_path, pixel_size=25):
    print(f"\nDeconstructing image: {image_path}")
    
    # Get original image dimensions before processing
    with Image.open(image_path) as img:
        orig_width, orig_height = img.size
        
    pixel_data = deconstruct_pixel_art(image_path, pixel_size)
    
    # Check if dimensions are multiples of pixel size
    width_remainder = orig_width % pixel_size
    height_remainder = orig_height % pixel_size
    is_perfect_grid = width_remainder == 0 and height_remainder == 0
    
    # Analyze unique colors
    colors = defaultdict(int)
    for coord, color in pixel_data['pixels'].items():
        colors[color] += 1

    grid_width = pixel_data['metadata']['width'] // pixel_size
    grid_height = pixel_data['metadata']['height'] // pixel_size

    # Create analysis data structure
    analysis_data = {
        'metadata': pixel_data['metadata'],
        'pixels': pixel_data['pixels'],
        'analysis': {
            'original_dimensions': f"{orig_width}x{orig_height}",
            'dimensions': f"{pixel_data['metadata']['width']}x{pixel_data['metadata']['height']}",
            'grid_dimensions': f"{grid_width}x{grid_height}",
            'total_blocks': len(pixel_data['pixels']),
            'unique_colors': len(colors),
            'color_usage': {str(color): count for color, count in colors.items()}
        }
    }

    print("Analysis data:", analysis_data)  # Debug print
    return analysis_data

def deconstruct_pixel_art(image_path, pixel_size=25):
    img = Image.open(image_path).convert('RGB')
    pixel_array = np.array(img)

    pixel_data = {
        'metadata': {
            'width': pixel_array.shape[1],
            'height': pixel_array.shape[0],
            'pixel_size': pixel_size
        },
        'pixels': {}
    }

    for y in range(0, pixel_array.shape[0], pixel_size):
        y_index = y // pixel_size
        for x in range(0, pixel_array.shape[1], pixel_size):
            x_index = x // pixel_size
            color = tuple(int(v) for v in pixel_array[y, x])
            coord_key = f"{x_index},{y_index}"
            pixel_data['pixels'][coord_key] = color

    return pixel_data
