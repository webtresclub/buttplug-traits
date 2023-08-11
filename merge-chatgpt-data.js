const fs = require('fs');

for(let i = 1; i < 1025; i++) {
    console.log(i);
    const dataGpt = JSON.parse(fs.readFileSync(`./buttplugs/chatgpt/${i}.json`));
    const data = JSON.parse(fs.readFileSync(`./buttplugs/data/${i}.json`));
    data.name = dataGpt.name;
    data.description = dataGpt.description;
    fs.writeFileSync(`./buttplugs/merge-data/${i}.json`, JSON.stringify(data, null, 2));
}
