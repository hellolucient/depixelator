from PIL import Image

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
                if actual_x < metadata['width'] and actual_y < metadata['height']:
                    pixels[actual_x, actual_y] = color

    return new_img
