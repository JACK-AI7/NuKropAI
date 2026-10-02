const fs = require('fs');
const content = fs.readFileSync('app/src/main/assets/index.html', 'utf8');

const p = content.indexOf('driver_dashboard: () => {');
const pEnd = content.indexOf('profile: () => {', p);
console.log(content.substring(p, p + 2500));
