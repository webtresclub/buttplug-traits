const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

app.get('/', (req, res) => {
    fs.readdir('./buttplugs', (err, files) => {
        console.log(files)
        if (err) {
            res.send('Unable to scan directory: ' + err);
        } 

        let imgList = files.map(file => `<img src="./buttplugs/${file}" style="height: 200px; margin: 10px;">`).join('');

        res.send(`
            <html>
                <body>
                    <div style="display: flex; flex-wrap: wrap;">
                        ${imgList}
                    </div>
                </body>
            </html>
        `);
    });
});

app.use('/buttplugs', express.static(path.join(__dirname, 'buttplugs')))

app.listen(port, () => {
    console.log(`App listening at http://localhost:${port}`);
});
