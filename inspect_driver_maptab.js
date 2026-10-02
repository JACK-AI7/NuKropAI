const fs = require('fs');

const src = fs.readFileSync('app/src/main/assets/index.html', 'utf8');

let posD = src.indexOf("driver_dashboard:");
let posMap = src.indexOf("const mapTab =", posD);
if (posMap !== -1) {
    console.log('--- mapTab ---');
    console.log(src.substring(posMap, posMap + 3000));
}
