import fs from 'fs';

const code1 = `
const obj = {
  profile: () => \`hello\`,
  driver_login: () => \`world\`
};
`;

fs.writeFileSync('test3.js', code1);
