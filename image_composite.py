import os
import random
import imageio
import numpy as np
from PIL import Image
from itertools import product
import json
import openai  # Import the OpenAI library

# Set up your OpenAI API key here
openai.api_key = ""

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

# Load the gradient image
gradient_image_path = os.path.join(root_dir, "Gradient.png")
gradient_image = Image.open(gradient_image_path).convert('RGBA')


def generate_background_story(properties):
    try:
        # Create a prompt for GPT-3.5 based on the NFT properties
        traits = ""
        for attribute in properties["attributes"]:
            # Convert to lowercase
            trait_type = attribute["trait_type"].lower()
            traits += f"{trait_type}: {attribute['value']}\n"

        # Use the GPT-3.5 API to generate the background story
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Generate a background story with this NFT traits, it is an osciloscope themed robot who is part of WebtrES club."
                },
                {
                    "role": "user",
                    "content": traits
                }
            ],
            temperature=0.8,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the generated text from the response
        generated_text = response.choices[0].message.content

        last_full_stop_index = generated_text.rfind('.')
        if last_full_stop_index != -1:
            generated_text = generated_text[:last_full_stop_index + 1]

        return generated_text

    except Exception as e:
        print("Error while generating background story:", e)
        return ""  # Return an empty string in case of error


def generate_properties(combination, idx):
    # Define the properties for the GIF based on the combination of subgroups
    properties = {
        "description": "Webtres community NFTs.",
        "external_url": "https://huffplug.com",
        # The GIF filename will be based on the index
        "image": f"[placeholder]{idx+1}.gif",
        "attributes": []
    }

    trait_types = ["Box", "Buttons", "ArmsAndLegs", "Screen", "Addon"]

    for i, subgroup in enumerate(combination):
        trait_type = trait_types[i]
        trait_value = os.path.basename(subgroup)
        properties["attributes"].append({
            "trait_type": trait_type,
            "value": trait_value
        })

    return properties


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

    # Generate the background story based on the properties
    background_story = generate_background_story(properties)
    properties["description"] = background_story

    # Save the properties to a JSON file
    with open(os.path.join(frames_dir, f'{idx+1}.json'), 'w') as json_file:
        json.dump(properties, json_file, indent=2)

    for i in range(1, 17):
        # Create a new image base with the background color
        base_image = Image.new('RGBA', (69*4, 69*4), bg_color)

        # Superimpose the gradient image over the base image
        base_image = Image.alpha_composite(base_image, gradient_image)

        for subgroup in combination:
            frame_file = os.path.join(subgroup, f"Frame{i}.png")
            if os.path.isfile(frame_file):
                # Open the image and convert it to a PIL Image object
                new_layer = Image.open(frame_file).convert('RGBA')
                base_image = Image.alpha_composite(base_image, new_layer)

        # Convert the PIL Image object into a numpy array for use with imageio
        numpy_image = np.array(base_image)
        gif_frames.append(numpy_image)

    # Create the GIF from the frames
    imageio.mimsave(os.path.join(
        frames_dir, f'{idx+1}.gif'), gif_frames, duration=0.1, loop=0)
