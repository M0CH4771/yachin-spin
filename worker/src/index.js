// ヤチンスピン デイリーランキング API（Cloudflare Workers + D1）
// 送られてきた操作の記録をサーバーでゲームごと再生して、記録が本物か確かめてから順位に入れる
import G from './engine.js';


const DAY_MS = 86400000;
const jstDay = (t = Date.now()) => new Date(t + 9 * 3600000).toISOString().slice(0, 10);
const SCORE_K = 1e12;
const MAX_CODES = 16;         // 1回に受け取る操作の数（無料プランの計算時間 10ms に収めるため）
const MAX_STARTS_PER_DAY = 300;

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-Admin',
  'Access-Control-Max-Age': '86400',
};
const json = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...cors } });
const bad = (msg, status = 400) => json({ error: msg }, status);

const okId = s => typeof s === 'string' && /^[A-Za-z0-9-]{16,64}$/.test(s);
const okDay = s => typeof s === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(s);
function cleanName(s) {
  s = String(s || '').normalize('NFKC').replace(/[\u0000-\u001f\u007f-\u009f\u200b-\u200f\u2028-\u202e\u2060-\u206f<>]/g, '').trim();
  s = [...s].slice(0, 12).join('');
  return s || 'ななし';
}
function seed32() { const a = new Uint32Array(1); crypto.getRandomValues(a); return a[0]; }

async function upsertPlayer(env, id, name) {
  const now = Date.now();
  await env.DB.prepare('INSERT INTO players (id, name, created_at) VALUES (?1, ?2, ?3) ON CONFLICT(id) DO UPDATE SET name = excluded.name')
    .bind(id, cleanName(name), now).run();
}

// その日の、プレイヤーごとの最高記録で並べた順位
async function rankOf(env, day, score) {
  const r = await env.DB.prepare(
    `SELECT COUNT(*) AS n FROM (SELECT r.player_id, MAX(r.score) AS s FROM runs r JOIN players p ON p.id = r.player_id
       WHERE r.day = ?1 AND r.score IS NOT NULL AND p.banned = 0 GROUP BY r.player_id) WHERE s > ?2`).bind(day, score).first();
  return (r ? r.n : 0) + 1;
}
async function countPlayers(env, day) {
  const r = await env.DB.prepare(
    `SELECT COUNT(DISTINCT r.player_id) AS n FROM runs r JOIN players p ON p.id = r.player_id WHERE r.day = ?1 AND r.score IS NOT NULL AND p.banned = 0`).bind(day).first();
  return r ? r.n : 0;
}
async function bestOf(env, day, player) {
  const r = await env.DB.prepare('SELECT MAX(score) AS s FROM runs WHERE day = ?1 AND player_id = ?2 AND score IS NOT NULL').bind(day, player).first();
  return r && r.s != null ? r.s : null;
}
const split = s => ({ rents: Math.floor(s / SCORE_K), earned: s % SCORE_K });
// 構成：シンボルを多い順に [キー, 数]、お守りのキー、最高の1スピン
function buildOf(st) {
  const m = {}; st.inv.forEach(x => { m[x.key] = (m[x.key] || 0) + 1; });
  return JSON.stringify({ inv: Object.entries(m).sort((a, b) => b[1] - a[1]), items: st.items, best: st.best || 0 });
}

async function start(env, body) {
  if (!okId(body.player)) return bad('player');
  const day = jstDay();
  const c = await env.DB.prepare('SELECT COUNT(*) AS n FROM runs WHERE player_id = ?1 AND day = ?2').bind(body.player, day).first();
  if (c && c.n >= MAX_STARTS_PER_DAY) return bad('今日はこれ以上ランキングに挑戦できません', 429);
  await upsertPlayer(env, body.player, body.name);
  const run = crypto.randomUUID(), seed = seed32(), now = Date.now();
  const state = G.exportDaily(G.newDaily(day, seed)); G.setRng(null);
  await env.DB.prepare('INSERT INTO runs (id, player_id, day, seed, state, started_at, updated_at) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?6)')
    .bind(run, body.player, day, seed, state, now).run();
  return json({ run, seed, day });
}

// 操作を少しずつ受け取って、サーバーの状態に当てて確かめる
async function step(env, body) {
  if (!okId(body.player) || !okId(body.run)) return bad('id');
  const from = Number.isInteger(body.from) ? body.from : -1, codes = body.codes;
  if (from < 0 || !Array.isArray(codes) || codes.length > MAX_CODES) return bad('codes');
  const row = await env.DB.prepare('SELECT id, day, state, n, over, rents, earned, started_at FROM runs WHERE id = ?1 AND player_id = ?2').bind(body.run, body.player).first();
  if (!row) return bad('run', 404);
  const done = async () => {
    const best = await bestOf(env, row.day, body.player);
    return json({ n: row.n, over: !!row.over, rents: row.rents || 0, earned: row.earned || 0, rank: best == null ? null : await rankOf(env, row.day, best), total: await countPlayers(env, row.day) });
  };
  if (from > row.n) return json({ error: 'gap', n: row.n }, 409);
  const fresh = codes.slice(row.n - from);                 // すでに受け取ったぶんは飛ばす（送り直しに強くする）
  if (!fresh.length || row.over) return done();
  if (Date.now() - row.started_at > 2 * DAY_MS) return bad('期限切れ', 410);
  const st = G.importDaily(row.state);
  const ok = G.stepDaily(st, fresh);
  G.setRng(null);
  if (!ok) return bad('記録を確かめられませんでした');
  const over = st.phase === 'over' || st.phase === 'kanst' ? 1 : 0;
  const rents = st.rentIdx, earned = Math.min(SCORE_K - 1, Math.max(0, Math.floor(st.totalEarned || 0)));
  const score = (rents > 0 || over) ? rents * SCORE_K + earned : null;
  if (body.name) await upsertPlayer(env, body.player, body.name);
  await env.DB.prepare('UPDATE runs SET state = ?1, n = ?2, over = ?3, rents = ?4, earned = ?5, score = ?6, updated_at = ?7, build = ?10 WHERE id = ?8 AND n = ?9')
    .bind(G.exportDaily(st), row.n + fresh.length, over, rents, earned, score, Date.now(), row.id, row.n, buildOf(st)).run();
  Object.assign(row, { n: row.n + fresh.length, over, rents, earned });
  return done();
}

async function ranking(env, url) {
  const day = okDay(url.searchParams.get('day')) ? url.searchParams.get('day') : jstDay();
  const limit = Math.max(1, Math.min(100, +url.searchParams.get('limit') || 50));
  const rows = await env.DB.prepare(
    `SELECT p.name AS name, r.player_id AS pid, MAX(r.score) AS score, r.over AS over, r.updated_at AS upd, r.build AS build FROM runs r JOIN players p ON p.id = r.player_id
       WHERE r.day = ?1 AND r.score IS NOT NULL AND p.banned = 0 GROUP BY r.player_id ORDER BY score DESC LIMIT ?2`).bind(day, limit).all();
  const me = url.searchParams.get('player');
  const list = [];
  let rank = 0, prev = null;
  (rows.results || []).forEach((r, i) => { if (r.score !== prev) { rank = i + 1; prev = r.score; } list.push({ rank, name: r.name, ...split(r.score), live: !r.over && Date.now() - r.upd < 10 * 60000, build: r.build ? JSON.parse(r.build) : null, me: okId(me) && r.pid === me }); });
  const out = { day, total: await countPlayers(env, day), list, now: Date.now() };
  if (okId(me)) { const b = await bestOf(env, day, me); if (b != null) out.mine = { rank: await rankOf(env, day, b), ...split(b) }; }
  return json(out);
}

async function rename(env, body) {
  if (!okId(body.player)) return bad('player');
  await upsertPlayer(env, body.player, body.name);
  return json({ name: cleanName(body.name) });
}

async function admin(env, req, body) {
  if (!env.ADMIN_KEY || req.headers.get('X-Admin') !== env.ADMIN_KEY) return bad('forbidden', 403);
  if (body.ban && okId(body.ban)) { await env.DB.prepare('UPDATE players SET banned = 1 WHERE id = ?1').bind(body.ban).run(); return json({ banned: body.ban }); }
  if (body.find) { const r = await env.DB.prepare('SELECT id, name, banned FROM players WHERE name = ?1').bind(cleanName(body.find)).all(); return json(r.results || []); }
  return bad('admin');
}

export default {
  async fetch(req, env) {
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    const url = new URL(req.url);
    try {
      if (req.method === 'GET' && url.pathname === '/api/ranking') return await ranking(env, url);
      if (req.method === 'GET' && url.pathname === '/api/today') return json({ day: jstDay(), now: Date.now() });
      if (req.method === 'POST') {
        const text = await req.text();
        if (text.length > 20000) return bad('too large', 413);
        let body; try { body = JSON.parse(text); } catch { return bad('json'); }
        if (url.pathname === '/api/start') return await start(env, body);
        if (url.pathname === '/api/step') return await step(env, body);
        if (url.pathname === '/api/name') return await rename(env, body);
        if (url.pathname === '/api/admin') return await admin(env, req, body);
      }
      return bad('not found', 404);
    } catch (e) {
      return json({ error: 'server', detail: String(e && e.message || e) }, 500);
    }
  },
};
