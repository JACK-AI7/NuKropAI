const fs = require('fs');

const src = fs.readFileSync('app/src/main/assets/index.html', 'utf8');

let pos = src.indexOf("function renderPlantixCropsScreen(");
if (pos !== -1) {
    console.log(src.substring(pos + 2000, pos + 4000));
}
