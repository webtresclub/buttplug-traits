import os
import json
import inflection


chatgpt_dir = os.path.join("buttplugs", "chatgpt")
final_dir = os.path.join("buttplugs", "final")
os.makedirs(final_dir, exist_ok=True)

f = open('basedata-raw.json')
combinations = json.load(f)


ipfs_url = "ipfs://QmV4s7NMmDh64Z2GkuqbUmRM7XyN5WcbTn9sSAVvCsK4xQ/"


def generate_background_story(idx, combination):
    filename = f'000000{idx}.gif'[-8:]
    image_url = ipfs_url+filename

    metadata = {}
    metadata['description'] = "A collection of 1024 unique buttplugs."
    metadata['external_url'] = f'https://www.buttpluggy.com/buttpluggy/{idx}'
    metadata['image'] = image_url
    metadata['name'] = ""
    metadata['attributes'] = []

    for attribute in combination["attributes"]:
        trait = {}
        trait["trait_type"] = inflection.humanize(attribute.replace('And', ' and ').replace('Addons', 'Addon'));
        trait["value"] = inflection.humanize(combination['attributes'][attribute])
        metadata['attributes'].append(trait)
    return metadata
    
    

for idx, combination in combinations.items():
    realid = int(idx) + 1
    print(realid,"/ 1024")
    metadata = generate_background_story(realid, combination)
    gpt_output = json.load(open(os.path.join(chatgpt_dir, f'000000{realid}.json'[-9:])))
    metadata['name'] = gpt_output['Name']
    metadata['description'] = gpt_output['Description']

    output_file = os.path.join(final_dir, f'000000{realid}'[-4:])
    with open(output_file, 'w') as json_file:
        json.dump(metadata, json_file, indent=2)
    

    
    
    # if file exist skip
    #if os.path.exists(output_file):
    #    continue

    #data = generate_background_story(combination, realid)

    #if data:
    #    with open(output_file, 'w') as json_file:
    #        json.dump(data, json_file, indent=2)
    