import os
from dotenv import load_dotenv

import json
from openai import OpenAI

load_dotenv()

f = open('basedata-raw.json')
combinations = json.load(f)

client = OpenAI(
    api_key=os.getenv("OPENIA_APIKEY"),
)

chatgpt_dir = os.path.join("buttplugs", "chatgpt")
os.makedirs(chatgpt_dir, exist_ok=True)


def generate_background_story(properties, idx):
    filename = f'000000{idx}.gif'[-8:]
    image_url = f"https://bafybeidd62ezqvyyviibduxaz2wuuyexkpuwbdfo34wukucxtav7qh3cbe.ipfs.cf-ipfs.com/{filename}"
    
    try:
        traits = ""
        for attribute in properties["attributes"]:
            # Convert to lowercase
            prop = properties['attributes'][attribute];
            traits += f"{attribute}: {prop}\n"

        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": "Generate a name and a background story with this NFT who is part of WebtrES club, use the the traits, and also the attached image as reference. The expected output is in json format, { Name: [name], Description: [background] }"
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": traits},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                                "detail": "high"
                            },
                        },
                    ]                    
                }
            ],
            temperature=0.8,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the generated text from the response
        generated_text = response.choices[0].message.content

        return generated_text

    except Exception as e:
        print("Error while generating background story:", e)
        return ""  # Return an empty string in case of error

for idx, combination in combinations.items():
    realid = int(idx) + 1
    print(realid,"/ 1024")
    output_file = os.path.join(chatgpt_dir, f'000000{realid}.json'[-9:])
    
    # if file exist skip
    if os.path.exists(output_file):
        continue

    data = generate_background_story(combination, realid)

    if data:
        with open(output_file, 'w') as json_file:
            json.dump(data, json_file, indent=2)
    