const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

app.get('/', (req, res) => {
    fs.readdir('./results', (err, files) => {
        if (err) {
            res.send('Unable to scan directory: ' + err);
        } 

        let imgList = files.map(file => `<img src="./results/${file}" style="width: 200px; height: 200px; margin: 10px;">`).join('');

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

app.use('/results', express.static(path.join(__dirname, 'results')))

app.listen(port, () => {
    console.log(`App listening at http://localhost:${port}`);
});
