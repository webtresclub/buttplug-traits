import os
import random
import imageio
import numpy as np
from PIL import Image
from itertools import product

root_dir = "."  # directorio donde están las capas
frames_dir = "./results"  # directorio de salida
os.makedirs(frames_dir, exist_ok=True)

# Lista de nombres de archivos y directorios para ignorar
ignore = ['image_composite.py', 'results']

groups = []
optional_addons = None  # variable para almacenar la ruta a los addons
screen_group_index = None  # variable para almacenar el índice del grupo de pantalla

# Recorrer cada carpeta principal
for group_index, group_dir in enumerate(sorted(os.listdir(root_dir))):
    if group_dir in ignore:
        continue

    group_path = os.path.join(root_dir, group_dir)
    
    # Si la carpeta es la de "Addons", guardar la ruta para usarla más adelante
    if group_dir == "05 - Addons":
        optional_addons = [os.path.join(group_path, subgroup_dir) for subgroup_dir in os.listdir(group_path)]
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
            subgroup_paths = [os.path.join(group_path, subgroup_dir) for subgroup_dir in subgroups]
            groups.append(subgroup_paths)

# Obtener todas las combinaciones posibles de subgrupos
combinations = list(product(*groups))

# Limitar a X combinaciones
combinations = combinations[:1000]

for idx, combination in enumerate(combinations):
    gif_frames = []
    
    # Crear un nuevo color de fondo aleatorio para cada GIF
    bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
    
    # Decidir aleatoriamente si incluir los addons en este gif
    include_addons = random.choice([True, False])
    if include_addons and optional_addons is not None and 'classic' in combination[screen_group_index]:
        addons_path = random.choice(optional_addons)
        combination = list(combination) + [addons_path]

    for i in range(1, 17):  # Recorre los 16 frames
        # Crear una nueva imagen base completamente opaca para cada frame con el color aleatorio
        base_image = Image.new('RGBA', (64*4, 64*4), bg_color)

        for subgroup in combination:
            frame_file = os.path.join(subgroup, f"Frame{i}.png")
            if os.path.isfile(frame_file):
                # Abre la imagen y la convierte en un objeto Image de PIL
                new_layer = Image.open(frame_file)
                base_image = Image.alpha_composite(base_image, new_layer)

        # Convertir el objeto Image de PIL en una matriz numpy para usarlo con imageio
        numpy_image = np.array(base_image)
        gif_frames.append(numpy_image)

    # Crea el GIF a partir de los frames
    imageio.mimsave(os.path.join(frames_dir, f'output_{idx}.gif'), gif_frames, duration=0.1, loop=0)
