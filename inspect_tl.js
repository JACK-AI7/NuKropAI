const fs = require('fs');

const src = fs.readFileSync('app/src/main/assets/index.html', 'utf8');

let pos = src.indexOf("function TL(");
if (pos !== -1) {
    console.log('--- function TL ---');
    console.log(src.substring(pos, pos + 800));
}

let posU = src.indexOf("function updateAllTranslations(");
if (posU !== -1) {
    console.log('--- function updateAllTranslations ---');
    console.log(src.substring(posU, posU + 1200));
}
