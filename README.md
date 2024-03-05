# Buttplugy Traits Generator

This is a simple tool to generate traits for the Buttplugy project. It is a simple command line tool that takes a list of traits and generates the necessary code to add them to the project.

There are several different tools to create diffent types of metadata:
- First we precalculate the traits using a preseed random, since we see there were some issues with the random number generator from computer to computer and different python setups we decide to create a file with the precalculated traits. See the file [`basedata-raw.json`](./basedata-raw.json).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the differnt tooling we need.

```bash
pip install Pillow
```

## Usage

### Step 1 generate traits

Traits for each nft should always be the same, so we precalculate the traits using 31337 as a preseed random, since we see there were some issues with the random number generator from computer to computer and different python setups we decide to create a file with the precalculated traits. See the file [`basedata-raw.json`](./basedata-raw.json).

If you want to generate the traits again you can run the following command:
```bash
python 1_raw_metadata.py
```
This will generate a file called `basedata-raw.json` with the precalculated traits. It should be always the same traits. So you can use the file that its already in the repo.

### Step 2 generate images

We use the precalculated traits to generate the images. We use the following traits to generate the images for each nft, this images will be saved in the folder `./buttplugs/images/`:

```bash
python 2_generate_images.py
```

### Step 3 generate base traits meteadata

We use the precalculated traits to generate the traits in an opensea metadata, this metadata will be saved in the folder `./buttplugs/basemetadata/`:

```bash
python 3_generate_traits_data.py
```

Expected format example;
```json
{
  "description": "",
  "image": "[placeholder]/0014.gif",
  "attributes": [
    {
      "trait_type": "Box",
      "value": "shinyBlack"
    },
    {
      "trait_type": "Buttons",
      "value": "retroConsole"
    },
    {
      "trait_type": "ArmsAndLegs",
      "value": "foundry"
    },
    {
      "trait_type": "Screen",
      "value": "laser"
    }
  ]
}
```

### Step 4 upload images to ipfs

This will upload the Buttplugies image folder to the ipfs.

```bash
npx thirdweb upload ./buttplugs/images/
```
We are using the thirdweb cli to upload the images to ipfs. More info [here](https://portal.thirdweb.com/infrastructure/storage/how-to-use-storage/upload-files-to-ipfs).

The image on ipfs should be:
```bash
✔ Successfully uploaded directory to IPFS
✔ Files stored at the following IPFS URI: ipfs://QmV4s7NMmDh64Z2GkuqbUmRM7XyN5WcbTn9sSAVvCsK4xQ
✔ Open this link to view your upload: https://bafybeidd62ezqvyyviibduxaz2wuuyexkpuwbdfo34wukucxtav7qh3cbe.ipfs.cf-ipfs.com/
```

### TODO

Add more steps, since we still have to generate the metadata and the json file for the nft.


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)