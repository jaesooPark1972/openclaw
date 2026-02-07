const fs = require('fs');
const path = require('path');
const configDir = path.join(process.cwd(), 'src', 'config');

fs.readdirSync(configDir).forEach(file => {
    if (file.endsWith('.ts')) {
        const filePath = path.join(configDir, file);
        const content = fs.readFileSync(filePath, 'utf8');
        const newContent = content.replace(/\.strict\(\)/g, '');
        if (content !== newContent) {
            fs.writeFileSync(filePath, newContent, 'utf8');
            console.log(`Updated: ${file}`);
        }
    }
});
