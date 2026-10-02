const fs = require('fs');
const content = fs.readFileSync('app/src/main/assets/index.html', 'utf8');

const p = content.indexOf('function renderPlantixFlow');
console.log('p:', p);
if (p !== -1) {
  const chunk = content.substring(p, p + 10000);
  const regex = /case\s+['"]([^'"]+)['"]\s*:/g;
  let match;
  while ((match = regex.exec(chunk)) !== null) {
    console.log('Case:', match[1]);
  }
}
