import os
import json

 
f = open('basedata-raw.json')
combinations = json.load(f)


basemedata_folder = os.path.join("buttplugs", "basemetadata") # directorio de salida
os.makedirs(basemedata_folder, exist_ok=True)

def generate_properties(attrs, idx):
    # Define the properties for the GIF based on the combination of subgroups
    properties = {
        "description": "",
        # The GIF filename will be based on the index
        "image": f"[placeholder]/{f'000000{idx}'[-4:]}.gif",
        "attributes": []
    }

    trait_types = ["Box", "Buttons", "ArmsAndLegs", "Screen", "Addon"]

    for i, attr in enumerate(trait_types):
        
        if not attr in attrs:
            continue
        properties["attributes"].append({
            "trait_type": attr,
            "value": attrs[attr]
        })
        
    return properties


for idx, combination in combinations.items():
    ## idx start from 0 but the collection start from 1
    idx = int(idx) + 1

    print(idx,"/ 1024")
    
    metadata_properties = generate_properties(combination['attributes'], idx);
    
    # Save the properties to a JSON file
    with open(os.path.join(basemedata_folder, f'000000{idx}.json'[-9:]), 'w') as json_file:
        json.dump(metadata_properties, json_file, indent=2)

