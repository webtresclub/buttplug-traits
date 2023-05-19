import os
import random
import imageio
import numpy as np
from PIL import Image

root_dir = "."  # directorio donde están las capas
frames_dir = "./results"  # directorio de salida
os.makedirs(frames_dir, exist_ok=True)

# Lista de nombres de archivos y directorios para ignorar
ignore = ['image_composite.py', 'results']

selected_subgroups = []

# Recorrer cada carpeta principal
for group_dir in sorted(os.listdir(root_dir)):
    if group_dir in ignore:
        continue

    group_path = os.path.join(root_dir, group_dir)
    
    # Asegurarse de que es una carpeta y no un archivo
    if os.path.isdir(group_path):
        subgroups = os.listdir(group_path)
        # Asegurarse de que el directorio contiene algo
        if subgroups:
            # Seleccionar un subgrupo al azar
            subgroup_dir = random.choice(subgroups)
            subgroup_path = os.path.join(group_path, subgroup_dir)

            # Añadir el subgrupo seleccionado a la lista
            selected_subgroups.append(subgroup_path)

# crear una lista para almacenar los frames del gif
gif_frames = []

for i in range(1, 17):  # Recorre los 16 frames
    base_image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))  # Crear una nueva imagen base para cada frame

    for subgroup in selected_subgroups:
        frame_file = os.path.join(subgroup, f"Frame{i}.png")
        if os.path.isfile(frame_file):
            # Abre la imagen y la convierte en un objeto Image de PIL
            new_layer = Image.open(frame_file)
            base_image = Image.alpha_composite(base_image, new_layer)

    # Convertir el objeto Image de PIL en una matriz numpy para usarlo con imageio
    numpy_image = np.array(base_image)
    gif_frames.append(numpy_image)

# Crea el GIF a partir de los frames
imageio.mimsave(os.path.join(frames_dir, 'output.gif'), gif_frames, duration=0.1, loop=0)
