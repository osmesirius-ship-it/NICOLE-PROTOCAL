import { mkdir, rm, stat, readdir } from 'node:fs/promises';
import { createReadStream, createWriteStream } from 'node:fs';
import { join, resolve } from 'node:path';

const root = resolve(process.cwd());
const distDir = join(root, 'dist');

async function ensureCleanDist() {
  await rm(distDir, { recursive: true, force: true });
  await mkdir(distDir, { recursive: true });
}

async function copyPath(src, dest) {
  const info = await stat(src);
  if (info.isDirectory()) {
    await mkdir(dest, { recursive: true });
    const entries = await readdir(src);
    for (const entry of entries) {
      await copyPath(join(src, entry), join(dest, entry));
    }
  } else {
    await new Promise((resolveCopy, rejectCopy) => {
      const input = createReadStream(src);
      const output = createWriteStream(dest);
      input.on('error', rejectCopy);
      output.on('error', rejectCopy);
      output.on('finish', resolveCopy);
      input.pipe(output);
    });
  }
}

async function build() {
  await ensureCleanDist();
  await copyPath(join(root, 'index.html'), join(distDir, 'index.html'));
  await copyPath(join(root, 'src'), join(distDir, 'src'));
  console.log('Build complete. Output in dist/.');
}

build().catch((error) => {
  console.error('Build failed:', error);
  process.exitCode = 1;
});
