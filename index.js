
const fs = require("fs");
const GIFEncoder = require('gifencoder');
const mergeImages = require('merge-images');
const { Canvas, Image, createCanvas } = require('canvas');

// este helper hace que si un frame no existe, se busque el anterior.
// esto es util en caso de frames repetidos
function getImageFile(part, seed, frame) {
  let file = `assets/${part}/${seed}/Frame${frame}.png`;
  
  while(!fs.existsSync(file)) {
    if(frame === 1) {
      return file;
    }
    frame--;
    file = `assets/${part}/${seed}/Frame${frame}.png`;
  }
  return file;
}

async function genFrames() {
  const framesPromises = [];
  for(let i = 1; i <= 16; i++) {
    framesPromises.push(mergeImages([
      { src: getImageFile('Extremidades', 1, i), x: 0, y: 0 },
      { src: getImageFile('Body', 1, i), x: 0, y: 0 },
      { src: getImageFile('Pantalla', 1, i), x: 0, y: 0 },
      { src: getImageFile('Faces', 1, i), x: 0, y: 0 },
      { src: getImageFile('Botonera', 1, i), x: 0, y: 0 },
    ], { Canvas, Image, quality: 1, width:64, height:64 }));
  }

  return await Promise.all(framesPromises);
  // data:image/png;base64,iVBORw0KGgoAA...
  //const buffer = Buffer.from(stringB64.replace(/^data:image\/png;base64,/, ""), 'base64');
}

async function genImage() {
  const encoder = new GIFEncoder(64, 64);
  // stream the results as they are available into myanimated.gif
  encoder.createReadStream().pipe(fs.createWriteStream('myanimated.gif'));

  encoder.start();
  encoder.setRepeat(0); // 0 for repeat, -1 for no-repeat
  encoder.setDelay(50); // frame delay in ms
  encoder.setQuality(10); // image quality. 10 is default.

  const canvas = createCanvas(64, 64);

  frames = await genFrames();
  frames.forEach((frame) => {
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, 64, 64);

    const img = new Image()
    img.src = frame;
    // const buffer = Buffer.from(stringB64.replace(/^data:image\/png;base64,/, ""), 'base64');
    ctx.drawImage(img, 0, 0, 64, 64);
    encoder.addFrame(ctx);
  });
  encoder.finish();
}

genImage();