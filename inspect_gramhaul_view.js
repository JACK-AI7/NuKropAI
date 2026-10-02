const fs = require('fs');

const src = fs.readFileSync('app/src/main/assets/index.html', 'utf8');

let pos = src.indexOf("gramhaul: () =>");
if (pos !== -1) {
    console.log(src.substring(pos, pos + 3000));
}
