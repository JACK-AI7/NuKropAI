import fs from 'fs';

let content = fs.readFileSync('web/src/App.tsx', 'utf8');

// 1. Fix grid responsiveness (prevent mobile overflow)
content = content.replace(/minmax\(400px/g, 'minmax(280px');
content = content.replace(/minmax\(320px/g, 'minmax(280px');
content = content.replace(/minmax\(300px/g, 'minmax(280px');

// 2. Remove the "Download Hub" section entirely to remove "doubly downloads"
// The section starts with "{/* Download Hub */}" and ends with "</section>"
const downloadHubRegex = /\{\/\*\s*Download Hub\s*\*\/\}.*?<\/section>/s;
content = content.replace(downloadHubRegex, '');

// Also remove duplicate iOS buttons just in case there are others
const iosButtonRegex = /<button[^>]*>[\s\S]*?Download for iOS[\s\S]*?<\/button>/gi;
content = content.replace(iosButtonRegex, '');

fs.writeFileSync('web/src/App.tsx', content);
console.log('App.tsx updated successfully');
