// ブラウザで試すための、ローカルのランキングサーバー（node --no-warnings test/serve.mjs [port]）
// D1 のかわりに node:sqlite を使う。本番では使わない
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';
import http from 'node:http';
import worker from '../src/index.js';
const db = new DatabaseSync(process.env.DB_FILE || ':memory:');
db.exec(readFileSync(new URL('../schema.sql', import.meta.url), 'utf8'));
const D1 = { prepare(sql) { const q = sql.replace(/\?(\d+)/g, '?'); let args = []; const order = [...sql.matchAll(/\?(\d+)/g)].map(m => +m[1] - 1);
  const o = { bind(...a) { args = order.map(i => a[i]); return o; },
    async run() { db.prepare(q).run(...args); return { success: true }; },
    async first() { return db.prepare(q).get(...args) || null; },
    async all() { return { results: db.prepare(q).all(...args) }; } };
  return o; } };
const env = { DB: D1, ADMIN_KEY: 'local' };
const port = +(process.argv[2] || 8787);
http.createServer(async (req, res) => {
  const chunks = []; for await (const c of req) chunks.push(c);
  const body = chunks.length ? Buffer.concat(chunks) : undefined;
  const r = await worker.fetch(new Request('http://127.0.0.1:' + port + req.url, { method: req.method, headers: req.headers, body: ['GET', 'HEAD'].includes(req.method) ? undefined : body }), env);
  res.writeHead(r.status, Object.fromEntries(r.headers)); res.end(Buffer.from(await r.arrayBuffer()));
}).listen(port, () => console.log('rank server on', port));
