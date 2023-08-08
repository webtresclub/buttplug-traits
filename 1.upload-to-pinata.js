const fs = require('fs');
const pinataSDK = require('@pinata/sdk');
require('dotenv').config();

async function upload(file) {
    const pinata = new pinataSDK(process.env.PINATA_API_KEY, process.env.PINATA_SECRET_API_KEY);
    const readableStreamForFile = fs.createReadStream(file);
    const options = {
        pinataMetadata: {
            name: file,
        },
        pinataOptions: {
            cidVersion: 0,
        },
    };
    return pinata.pinFileToIPFS(readableStreamForFile, options);
}

async function run() {
    const buttplugsDir = fs.readdirSync('./buttplugs/').filter(e => e.includes('.gif'));
    const buttplugsIpfs = {};

    for (const file of buttplugsDir) {
        console.log(`./buttplugs/${file}`);

        buttplugsIpfs[file] = await upload(`./buttplugs/${file}`);
        fs.writeFileSync('./buttplugs-ipfs.json', JSON.stringify(buttplugsIpfs, null, 2));
    }

}

run();


