const fs = require('fs');

const src = fs.readFileSync('app/src/main/assets/index.html', 'utf8');

let posD = src.indexOf("driver_dashboard:");
let posMap = src.indexOf("const mapTab =", posD);
if (posMap !== -1) {
    console.log(src.substring(posMap + 3000, posMap + 6500));
}
