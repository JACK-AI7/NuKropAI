import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const candidates = [
  path.resolve(__dirname, '../NuKropAI.apk'),
  path.resolve(__dirname, '../app/build/outputs/apk/release/app-release.apk'),
  path.resolve(__dirname, '../app/build/outputs/apk/debug/app-debug.apk'),
  path.resolve(__dirname, 'public/NuKropAI.apk'),
  path.resolve(__dirname, 'public/NuKropAI_v2.0.apk'),
];

let sourceApk = null;
for (const cand of candidates) {
  if (fs.existsSync(cand)) {
    const stat = fs.statSync(cand);
    // Prefer APKs that are larger than 45MB (real full app bundles)
    if (stat.size > 40 * 1024 * 1024) {
      if (!sourceApk || stat.mtimeMs > sourceApk.mtimeMs) {
        sourceApk = { path: cand, size: stat.size, mtimeMs: stat.mtimeMs };
      }
    }
  }
}

if (!sourceApk) {
  console.log('ℹ️ [sync-apk] No external APK found to sync. Keeping existing public APKs.');
  process.exit(0);
}

const pubDir = path.resolve(__dirname, 'public');
if (!fs.existsSync(pubDir)) {
  fs.mkdirSync(pubDir, { recursive: true });
}

const targets = [
  path.join(pubDir, 'NuKropAI.apk'),
  path.join(pubDir, 'NuKropAI_v2.0.apk'),
  path.join(pubDir, 'NuKropAI_latest.apk'),
];

const distDir = path.resolve(__dirname, 'dist');
if (fs.existsSync(distDir)) {
  targets.push(
    path.join(distDir, 'NuKropAI.apk'),
    path.join(distDir, 'NuKropAI_v2.0.apk'),
    path.join(distDir, 'NuKropAI_latest.apk')
  );
}

const sizeMb = (sourceApk.size / (1024 * 1024)).toFixed(1);
console.log(`🚀 [sync-apk] Syncing latest APK from ${sourceApk.path} (${sizeMb} MB)...`);

for (const target of targets) {
  try {
    if (path.resolve(sourceApk.path) !== path.resolve(target)) {
      fs.copyFileSync(sourceApk.path, target);
      console.log(`  ✓ Synced -> ${path.relative(__dirname, target)}`);
    }
  } catch (err) {
    console.warn(`  ⚠️ Could not sync to ${target}:`, err.message);
  }
}

console.log(`✅ [sync-apk] All website APK download endpoints are now serving the latest ${sizeMb} MB release build!`);
