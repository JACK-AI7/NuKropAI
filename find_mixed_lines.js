const fs = require('fs');

const src = fs.readFileSync('app/src/main/assets/index.html', 'utf8');
const lines = src.split('\n');

const mixedLines = [];
lines.forEach((line, i) => {
    // Ignore script/link tags, translations definitions (like TL('...', '...', '...')), comments, urls
    if (line.includes('TL(') || line.includes('function TL') || line.includes('http') || line.includes('//') || line.includes('console.log')) return;
    
    const hasEnglishWords = /[a-zA-Z]{3,}/.test(line);
    const hasIndic = /[\u0C00-\u0C7F\u0900-\u097F]/.test(line);
    
    if (hasEnglishWords && hasIndic) {
        mixedLines.push({ lineNum: i + 1, content: line.trim() });
    }
});

console.log(`Found ${mixedLines.length} mixed lines.`);
mixedLines.slice(0, 40).forEach(l => console.log(`${l.lineNum}: ${l.content.substring(0, 120)}`));
