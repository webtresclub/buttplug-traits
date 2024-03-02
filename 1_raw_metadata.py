import os
import random
import numpy as np
from itertools import product
import json
# import openai  # Import the OpenAI library

# # Set up your OpenAI API key here
# openai.api_key = ""

random.seed(31337)

root_dir = "./layers"  # directorio donde están las capas
frames_dir = "./buttplugs"  # directorio de salida
os.makedirs(frames_dir, exist_ok=True)

groups = []
optional_addons = None  # variable para almacenar la ruta a los addons
screen_group_index = None  # variable para almacenar el índice del grupo de pantalla

# Recorrer cada carpeta principal
for group_index, group_dir in enumerate(sorted(os.listdir(root_dir))):

    group_path = os.path.join(root_dir, group_dir)

    # Si la carpeta es la de "Addons", guardar la ruta para usarla más adelante
    if group_dir == "05 - Addons":
        optional_addons = [os.path.join(group_path, subgroup_dir)
                           for subgroup_dir in os.listdir(group_path)]
        continue

    # Almacenar el índice del grupo de pantalla para usarlo más tarde
    if group_dir == "04 - Screen":
        screen_group_index = group_index

    # Asegurarse de que es una carpeta y no un archivo
    if os.path.isdir(group_path):
        subgroups = os.listdir(group_path)
        # Asegurarse de que el directorio contiene algo
        if subgroups:
            # Seleccionar un subgrupo al azar
            subgroup_paths = [os.path.join(
                group_path, subgroup_dir) for subgroup_dir in subgroups]
            groups.append(subgroup_paths)

# Obtener todas las combinaciones posibles de subgrupos
combinations = list(product(*groups))

combination = random.shuffle(combinations)

# Limitar a X combinaciones
combinations = combinations[:1024]

def random_color():
    """Generate a random RGB color."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def generate_gradient(width, height, color1, color2):
    """Generate a horizontal gradient image of the given size."""
    
    # Create an empty image
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Fill the image with a gradient
    for y in range(height):
        alpha = y / (height - 1)
        color = (1 - alpha) * color1 + alpha * color2
        img[y, :] = color
    
    return img


def generate_properties(combination, idx):
    # Define the properties for the GIF based on the combination of subgroups
    properties = {
        "description": "",
        # The GIF filename will be based on the index
        "image": f"[placeholder]/{idx+1}.gif",
        "attributes": {}
    }

    trait_types = ["Box", "Buttons", "ArmsAndLegs", "Screen", "Addon"]

    for i, subgroup in enumerate(combination):
        trait_type = trait_types[i]
        trait_value = os.path.basename(subgroup)
        properties["attributes"][trait_type] = trait_value;

    return properties

rawdump = {}

for idx, combination in enumerate(combinations):
    gif_frames = []

    # Seleccionar un color de fondo aleatorio para cada GIF
    bg_color = (
        random.randint(150, 240),
        random.randint(150, 240),
        random.randint(150, 240),
        255  # Canal alfa siempre con valor 255 para ser completamente opaco
    )

    # Decidir aleatoriamente si incluir los addons en este gif
    include_addons = random.choice([True, False])

    # Comprueba si alguna de las caras se llama "laser"
    has_laser_face = any("laser" in face for face in combination)

    if include_addons and optional_addons is not None and not has_laser_face:
        addons_path = random.choice(optional_addons)
        combination = list(combination) + [addons_path]

    # Generate properties for the current combination
    properties = generate_properties(combination, idx)
    #properties["background_color"] = bg_color

    # # Generate the background story based on the properties
    # background_story = generate_background_story(properties)
    # properties["description"] = background_story

    # Save the properties to a JSON file
    #with open(os.path.join(frames_dir, f'{idx+1}.json'), 'w') as json_file:
    #    json.dump(properties, json_file, indent=2)

    # Generate the gradient image
    gradient_start = np.array(random_color())
    gradient_end = np.array(random_color())
    properties["gradient_start"] = gradient_start.tolist()
    properties["gradient_end"] = gradient_end.tolist()

    rawdump[idx] = properties

# save properties to a json file
with open(os.path.join(f'basedata-raw.json'), 'w') as json_file:
    json.dump(rawdump, json_file, indent=2)
