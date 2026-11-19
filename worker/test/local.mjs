// D1 のかわりに node:sqlite で API を通しで試す（node --no-warnings test/local.mjs）
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import worker from '../src/index.js';
const require = createRequire(import.meta.url);

const db = new DatabaseSync(':memory:');
db.exec(readFileSync(new URL('../schema.sql', import.meta.url), 'utf8'));
const D1 = { prepare(sql) { const q = sql.replace(/\?(\d+)/g, '?'); let args = []; const order = [...sql.matchAll(/\?(\d+)/g)].map(m => +m[1] - 1);
  const o = { bind(...a) { args = order.map(i => a[i]); return o; },
    async run() { db.prepare(q).run(...args); return { success: true }; },
    async first() { return db.prepare(q).get(...args) || null; },
    async all() { return { results: db.prepare(q).all(...args) }; } };
  return o; } };
const env = { DB: D1, ADMIN_KEY: 'test-admin' };
const call = async (method, path, body, headers = {}) => {
  const r = await worker.fetch(new Request('https://x' + path, { method, body: body ? JSON.stringify(body) : undefined, headers }), env);
  return { status: r.status, data: await r.json() };
};
// 同じエンジンで、ボットにプレイさせる
const G = require('../../src/engine.js');
function bot(day, seed) {
  const st = G.newDaily(day, seed);
  for (let g = 0; g < 4000 && st.phase !== 'over'; g++) {
    const ph = st.phase;
    if (ph === 'item') G.act(st, 'i:' + ((st.itemChoices || [])[0] || ''));
    else if (ph === 'event') { if (!G.act(st, 'e:0')) G.act(st, 'e:1'); }
    else if (ph === 'rent') G.act(st, '$');
    else if (ph === 'spin') G.act(st, 's');
    else if (ph === 'choose') G.act(st, 'p:' + (st.choices[Math.floor(Math.random() * st.choices.length)] || ''));
  }
  G.setRng(null);
  return st;
}
let ok = 0, ng = 0; const check = (name, cond) => { console.log((cond ? '○' : '×') + ' ' + name); cond ? ok++ : ng++; };
let worstMs = 0;
// 画面と同じ送り方：12個ずつ順番に送る
async function sync(pid, run, log, from = 0) {
  let n = from, last = null;
  while (n < log.length) {
    const t = performance.now();
    last = await call('POST', '/api/step', { player: pid, run, from: n, codes: log.slice(n, n + 12) });
    worstMs = Math.max(worstMs, performance.now() - t);
    if (last.status !== 200) return last;
    n = last.data.n;
  }
  return last;
}
const players = [['aaaaaaaaaaaaaaaa-1', 'もち'], ['bbbbbbbbbbbbbbbb-2', 'たぬき<script>'], ['cccccccccccccccc-3', '  ']];
for (const [pid, name] of players) {
  for (let k = 0; k < 2; k++) {
    const s = await call('POST', '/api/start', { player: pid, name });
    const st = bot(s.data.day, s.data.seed);
    const f = await sync(pid, s.data.run, st.log);
    check(`${name.trim() || '(空)'} ${k + 1}回目：サーバーで確かめた結果が手元と同じ（家賃${st.rentIdx}回）`, f.status === 200 && f.data.over && f.data.rents === st.rentIdx && f.data.earned === Math.floor(st.totalEarned));
    if (k === 0) {
      const again = await call('POST', '/api/step', { player: pid, run: s.data.run, from: 0, codes: st.log.slice(0, 12) });
      check('同じ操作を送り直しても二重にならない', again.status === 200 && again.data.n === st.log.length);
    }
  }
}
// 途中のようす（リアルタイム）
{
  // テスト用のボットが家賃3回より前に負けた回は使わない（途中のようすを見るため）
  let s, st;
  do { s = await call('POST', '/api/start', { player: 'dddddddddddddddd-4', name: 'とちゅう' }); st = bot(s.data.day, s.data.seed); } while (st.rentIdx < 3);
  const cut = st.log.indexOf('$', st.log.indexOf('$') + 1) + 1;   // 家賃を2回払ったところまで
  const f = await sync('dddddddddddddddd-4', s.data.run, st.log.slice(0, cut));
  check('途中まで送ると、払った回数がそのまま入る', f.status === 200 && !f.data.over && f.data.rents === 2);
  const rk = await call('GET', '/api/ranking');
  check('ランキングに「挑戦中」で出る', rk.data.list.some(r => r.name === 'とちゅう' && r.live));
  const gap = await call('POST', '/api/step', { player: 'dddddddddddddddd-4', run: s.data.run, from: cut + 5, codes: st.log.slice(cut + 5, cut + 10) });
  check('間をとばして送ると、どこから送ればいいか返ってくる', gap.status === 409 && gap.data.n === cut);
  const rest = await sync('dddddddddddddddd-4', s.data.run, st.log, cut);
  check('つづきを送れば最後まで確かめられる', rest.data.over && rest.data.rents === st.rentIdx);
}
// 書きかえた記録
{
  const s = await call('POST', '/api/start', { player: 'aaaaaaaaaaaaaaaa-1', name: 'もち' });
  const st = bot(s.data.day, s.data.seed);
  const forged = st.log.slice(); const i = forged.findIndex(c => c.startsWith('p:')); forged[i] = 'p:dragon';
  const f = await sync('aaaaaaaaaaaaaaaa-1', s.data.run, forged);
  check('出ていないシンボルを取ったことにした記録は通らない', f.status === 400);
  const s2 = await call('POST', '/api/start', { player: 'aaaaaaaaaaaaaaaa-1', name: 'もち' });
  const st2 = bot(s2.data.day, s.data.seed);   // 配られたのと別のタネで遊んだ記録
  const f2 = await sync('aaaaaaaaaaaaaaaa-1', s2.data.run, st2.log);
  check('配られたタネと違うタネで遊んだ記録は通らない', f2.status !== 200 || f2.data.rents !== st2.rentIdx);
  const big = await call('POST', '/api/step', { player: 'aaaaaaaaaaaaaaaa-1', run: s2.data.run, from: 0, codes: Array(40).fill('s') });
  check('一度にたくさん送ると断られる', big.status === 400);
  const f4 = await call('POST', '/api/step', { player: 'bbbbbbbbbbbbbbbb-2', run: s2.data.run, from: 0, codes: ['s'] });
  check('他人の回には送れない', f4.status === 404);
}
// ランキング
const rk = await call('GET', '/api/ranking?player=aaaaaaaaaaaaaaaa-1');
console.log(JSON.stringify(rk.data.list.map(r => [r.rank, r.name, r.rents, r.live])), 'mine', JSON.stringify(rk.data.mine));
check('参加4人', rk.data.total === 4);
check('最終的な構成（シンボルとお守り）が見える', rk.data.list.every(r => r.build && r.build.inv.length && Array.isArray(r.build.items)));
console.log('構成の例', JSON.stringify(rk.data.list[0].build));
check('名前のタグが消えている', rk.data.list.some(r => r.name === 'たぬきscript'));
check('空の名前は「ななし」', rk.data.list.some(r => r.name === 'ななし'));
check('自分の順位が入っている', rk.data.mine && rk.data.mine.rank >= 1);
check('上から高い順', rk.data.list.every((r, i, a) => !i || a[i - 1].rents * 1e12 + a[i - 1].earned >= r.rents * 1e12 + r.earned));
await call('POST', '/api/name', { player: 'cccccccccccccccc-3', name: 'ツグミ' });
const rk2 = await call('GET', '/api/ranking');
check('名前を変えると順位表も変わる', rk2.data.list.some(r => r.name === 'ツグミ'));
const nb = await call('POST', '/api/admin', { ban: 'cccccccccccccccc-3' }, { 'X-Admin': 'wrong' });
check('管理キーなしでは何もできない', nb.status === 403);
await call('POST', '/api/admin', { ban: 'cccccccccccccccc-3' }, { 'X-Admin': 'test-admin' });
const rk3 = await call('GET', '/api/ranking');
check('出入り禁止にした人は順位表から消える', rk3.data.total === 3 && !rk3.data.list.some(r => r.name === 'ツグミ'));
console.log(`いちばん重かった1回の処理: ${worstMs.toFixed(1)} ms（DBの時間もふくむ）`);
console.log(`\n${ok} 件OK / ${ng} 件NG`);
process.exit(ng ? 1 : 0);
