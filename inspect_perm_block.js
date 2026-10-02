const fs = require('fs');

const src = fs.readFileSync('app/src/main/assets/index.html', 'utf8');

const camIdx = src.indexOf('function renderCameraPermissionScreen');
const cropsIdx = src.indexOf('function renderPlantixCropsScreen');

console.log('Permission block length:', cropsIdx - camIdx);
console.log(src.substring(camIdx, camIdx + 3000));
