const fs = require('fs');

const src = fs.readFileSync('app/src/main/assets/index.html', 'utf8');

let posD = src.indexOf("driver_dashboard:");
let posEarn = src.indexOf("const earningsTab =", posD);
if (posEarn !== -1) {
    console.log('--- earningsTab ---');
    console.log(src.substring(posEarn, posEarn + 2500));
}
