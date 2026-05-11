#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Remove .git directory to stay under Cloudflare's 25MB asset limit
const gitPath = path.join(__dirname, '..', '.git');
if (fs.existsSync(gitPath)) {
  console.log('Removing .git directory for deployment...');
  fs.rmSync(gitPath, { recursive: true, force: true });
  console.log('✓ Removed .git directory');
}

// Remove other large directories
const dirsToRemove = [
  path.join(__dirname, '..', 'node_modules'),
  path.join(__dirname, '..', '.claude'),
  path.join(__dirname, '..', '_raw')
];

dirsToRemove.forEach(dir => {
  if (fs.existsSync(dir)) {
    console.log(`Removing ${path.basename(dir)}...`);
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

console.log('✓ Build preparation complete');
