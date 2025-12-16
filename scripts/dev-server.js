import { createServer } from 'node:http';
import { createReadStream, existsSync } from 'node:fs';
import { stat } from 'node:fs/promises';
import { extname, join, resolve, sep } from 'node:path';

const root = resolve(process.env.STATIC_ROOT || process.argv[2] || process.cwd());
const port = process.env.PORT || 5173;

const mimeTypes = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8'
};

function sendFile(res, filePath) {
  const contentType = mimeTypes[extname(filePath)] || 'application/octet-stream';
  res.writeHead(200, { 'Content-Type': contentType });
  createReadStream(filePath).pipe(res);
}

async function handleRequest(req, res) {
  const urlPath = decodeURIComponent(req.url.split('?')[0]);
  const target = urlPath === '/' ? 'index.html' : urlPath.slice(1);
  const candidate = resolve(root, target);
  const rootWithSep = root.endsWith(sep) ? root : `${root}${sep}`;

  if (candidate !== root && !candidate.startsWith(rootWithSep)) {
    res.writeHead(403);
    res.end('Forbidden');
    return;
  }

  try {
    const info = await stat(candidate);
    if (info.isFile()) {
      sendFile(res, candidate);
      return;
    }
  } catch (err) {
    // fall through to index.html
  }

  const indexPath = join(root, 'index.html');
  if (existsSync(indexPath)) {
    sendFile(res, indexPath);
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
}

createServer((req, res) => {
  handleRequest(req, res).catch((error) => {
    console.error('Server error:', error);
    res.writeHead(500);
    res.end('Internal server error');
  });
}).listen(port, () => {
  console.log(`Dev server running at http://localhost:${port}`);
});
