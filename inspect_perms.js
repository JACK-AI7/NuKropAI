const fs = require('fs');

const src = fs.readFileSync('app/src/main/assets/index.html', 'utf8');

let posL = src.indexOf("function renderLocationPermissionScreen(");
if (posL !== -1) {
    console.log('--- Location Perm ---');
    console.log(src.substring(posL, posL + 1200));
}

let posN = src.indexOf("function renderNotificationPermissionScreen(");
if (posN !== -1) {
    console.log('--- Notif Perm ---');
    console.log(src.substring(posN, posN + 1200));
}
