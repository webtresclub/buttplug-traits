import os
from itertools import product
import json
import openai  # Import the OpenAI library

# # Set up your OpenAI API key here
openai.api_key = ""




def generate_background_story(properties):
    # Create a prompt for GPT-3.5 based on the NFT properties
    traits = ""
    for attribute in properties["attributes"]:
        # Convert to lowercase
        trait_type = attribute["trait_type"].lower()
        traits += f"{trait_type}: {attribute['value']}\n"
        
    # Use the GPT-3.5 API to generate the background story
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {
                "role": "system",
                "content": "Generate a name and a background story with this NFT traits, it is an osciloscope themed robot who is part of WebtrES club. Output should be JSON, including name, description, should also have numeric ability_scores from 0 to 10 of 'hp,charisma,constitution,dexterity,intelligence,strength,wisdom', skills and alignment"
            },
            {
                "role": "user",
                "content": traits
            }
        ],
        temperature=0.8,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the generated text from the response
    generated_text = response.choices[0].message.content
    return generated_text

#         last_full_stop_index = generated_text.rfind('.')
#         if last_full_stop_index != -1:
#             generated_text = generated_text[:last_full_stop_index + 1]

#         return generated_text



data_dir = "./buttplugs/data"  # directorio de salida
os.makedirs(data_dir, exist_ok=True)

for group_index, _file in enumerate(sorted(os.listdir(data_dir))):
    #if group_index < 968:
    #    continue
    print("fetch ID:", group_index, _file)
    metadata_file = os.path.join(data_dir, _file)
    metadata = json.load(open(metadata_file))
    if metadata["description"] == "":
        print("do fetch ID:", group_index)

    metadata["name"] = "222"
    metadata["description"] = "222"

    new_metadata = generate_background_story(metadata)

    with open(_file, "w") as outfile:
        outfile.write(new_metadata)
        #json.dump(new_metadata, outfile, indent=4)

# Writing to sample.json
#with open("sample.json", "w") as outfile:
#    outfile.write(json_object)
