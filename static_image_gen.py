import os
import imageio
import numpy as np
from PIL import Image
import json

f = open('basedata-raw.json')

# returns JSON object as
# a dictionary
combinations = json.load(f)

def transparent_canvas(width, height):
    """Generate a horizontal gradient image of the given size."""

    # Create an empty image
    img = np.zeros((height, width, 4), dtype=np.uint8)
    # set transparent alpha
    img[:,:, 3] = 0

    return img



root_dir = "layers"  # directorio donde están las capas
frames_dir = os.path.join("buttplugs", "static_images") # directorio de salida
os.makedirs(frames_dir, exist_ok=True)

layers = [
    { 'attr': 'Box', 'value': os.path.join('layers', '01 - Box') },
    { 'attr': 'Buttons', 'value': os.path.join('layers', '02 - Buttons') },
    { 'attr': 'ArmsAndLegs', 'value': os.path.join('layers', '03 - ArmsAndLegs') },
    { 'attr': 'Screen', 'value': os.path.join('layers', '04 - Screen') },
    { 'attr': 'Addon', 'value': os.path.join('layers', '05 - Addons') }
]

for idx, combination in combinations.items():
    ## idx start from 0 but the collection start from 1
    idx = int(idx) + 1

    print(idx,"/ 1024")
    # Comprueba si alguna de las caras se llama "laser"
    has_laser_face = combination['attributes']['Screen'] == 'laser'
    img_array = transparent_canvas(1280, 1280)

    frame = 1

    # Create a new image base with the background color
    base_image = Image.fromarray(img_array).convert('RGBA')

    # Superimpose the gradient image over the base image
    #base_image = Image.alpha_composite(base_image, gradient_image)

    for layerN in range(0, 5):
        attr = layers[layerN]['attr']
        val = layers[layerN]['value']

        if not attr in combination['attributes']:
            continue
        frame_file = os.path.join(val, combination['attributes'][attr], f"Frame{frame}.png")
        # Open the image and convert it to a PIL Image object
        new_layer = Image.open(frame_file).convert('RGBA').resize((1280,1280), Image.Resampling.NEAREST)
        base_image = Image.alpha_composite(base_image, new_layer)

    # write file
    filename = f'000000{idx}.png'[-8:]
    path = os.path.join(frames_dir, filename)
    imageio.imwrite(path, base_image)
