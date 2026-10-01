const fs = require('fs');
['nukrop_emulator.html', 'app/src/main/assets/index.html'].forEach(file => {
  console.log('=== ' + file + ' ===');
  const lines = fs.readFileSync(file, 'utf8').split('\n');
  lines.forEach((l, i) => {
    if (l.includes('Warangal') || l.includes('Telangana')) {
      if (l.includes('||') || l.includes('default') || l.includes('alert') || l.includes('ticker') || l.includes('mandi') || l.includes('geo') || l.includes('location') || l.includes('notif')) {
        console.log(`${i + 1}: ${l.trim()}`);
      }
    }
  });
});
