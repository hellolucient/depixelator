from PIL import Image
import numpy as np
import json
import os
from collections import defaultdict

def analyze_pixel_art(image_path, pixel_size=25):
    # Deconstruct
    print(f"\nDeconstructing image: {image_path}")
    pixel_data = deconstruct_pixel_art(image_path)

    # Print basic analysis
    print("\nBASIC IMAGE ANALYSIS:")
    print(f"Image dimensions: {pixel_data['metadata']['width']}x{pixel_data['metadata']['height']}")
    grid_width = pixel_data['metadata']['width'] // pixel_size
    grid_height = pixel_data['metadata']['height'] // pixel_size
    print(f"Grid dimensions: {grid_width}x{grid_height}")
    print(f"Total pixel blocks: {len(pixel_data['pixels'])}")

    # Analyze unique colors
    colors = defaultdict(int)
    for coord, color in pixel_data['pixels'].items():
        colors[color] += 1

    print(f"\nUNIQUE COLORS FOUND: {len(colors)}")
    print("\nColor usage (RGB: count):")
    for color, count in sorted(colors.items(), key=lambda x: x[1], reverse=True):
        print(f"RGB{color}: {count} blocks")

    # Print grid analysis
    print("\nGRID ANALYSIS:")
    print("Format: (x,y): RGB(r,g,b)")
    for coord, color in sorted(pixel_data['pixels'].items()):
        print(f"Position {coord}: RGB{color}")

    # Save detailed analysis to file
    analysis_data = {
        'metadata': pixel_data['metadata'],
        'grid_dimensions': {
            'width': grid_width,
            'height': grid_height
        },
        'unique_colors': {
            str(color): count for color, count in colors.items()
        },
        'pixel_grid': {
            coord: list(color) for coord, color in pixel_data['pixels'].items()
        }
    }

    with open('detailed_analysis.json', 'w') as f:
        json.dump(analysis_data, f, indent=2)
    print("\nDetailed analysis saved to 'detailed_analysis.json'")

    # Reconstruct
    print("\nReconstructing image...")
    reconstructed = reconstruct_pixel_art(pixel_data)

    # Save reconstructed image
    output_path = 'reconstructed_' + os.path.basename(image_path)
    reconstructed.save(output_path)
    print(f"\nSaved reconstructed image as: {output_path}")

    return pixel_data

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
            # Convert numpy values to regular integers
            color = tuple(int(v) for v in pixel_array[y, x])
            coord_key = f"{x_index},{y_index}"
            pixel_data['pixels'][coord_key] = color

    return pixel_data

def reconstruct_pixel_art(pixel_data):
    metadata = pixel_data['metadata']
    pixel_size = metadata['pixel_size']

    new_img = Image.new('RGB', (metadata['width'], metadata['height']))
    pixels = new_img.load()

    for coord, color in pixel_data['pixels'].items():
        x_index, y_index = map(int, coord.split(','))
        for py in range(pixel_size):
            for px in range(pixel_size):
                actual_x = (x_index * pixel_size) + px
                actual_y = (y_index * pixel_size) + py
                # Make sure we don't go outside image boundaries
                if actual_x < metadata['width'] and actual_y < metadata['height']:
                    pixels[actual_x, actual_y] = color

    return new_img

# Test with your image
if __name__ == "__main__":
    IMAGE_PATH = '/Users/trentmunday/depixelator/mick dundee dud.jpeg'

    try:
        # Make sure Pillow is installed
        try:
            import PIL
        except ImportError:
            print("Installing required package...")
            os.system('pip install Pillow')

        # Process the image
        if os.path.exists(IMAGE_PATH):
            pixel_data = analyze_pixel_art(IMAGE_PATH)
            print("\nProcessing completed successfully!")

            # Save the raw pixel data to a JSON file
            with open('pixel_data.json', 'w') as f:
                serializable_data = {
                    'metadata': pixel_data['metadata'],
                    'pixels': {
                        coord: list(color)
                        for coord, color in pixel_data['pixels'].items()
                    }
                }
                json.dump(serializable_data, f, indent=2)
                print("\nRaw pixel data saved to: pixel_data.json")

            # Let user know about the files created
            print("\nFiles created:")
            print(f"1. reconstructed_{os.path.basename(IMAGE_PATH)} - The reconstructed image")
            print("2. pixel_data.json - Raw pixel data")
            print("3. detailed_analysis.json - Detailed color and position analysis")

    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("Please check that your image file is valid and try again.")