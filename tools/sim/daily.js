// デイリーの到達回数の分布と、記録の再生が一致するかを調べる
// node tools/sim/daily.js [回数] [日付]
const G = require(process.env.ENGINE || '../../src/engine.js');
const src = require('fs').readFileSync(require('path').join(__dirname, 'balance.js'), 'utf8');
const TIER = eval('(' + src.slice(src.indexOf('const TIER = ') + 13, src.indexOf('};', src.indexOf('const TIER = ')) + 1) + ')');
const IR = { C: 1, U: 2, R: 3 };
function play(date, seed, mode) {
  const st = G.newDaily(date, seed);
  const A = code => { const r = G.act(st, code); if (!r) throw new Error('bad ' + code + ' @' + st.phase); return r; };
  for (let guard = 0; guard < 5000; guard++) {
    if (st.phase === 'over') break;
    if (st.phase === 'item') {
      const c = st.itemChoices || [];
      const k = !c.length ? '' : mode === 'random' ? c[Math.floor(Math.random() * c.length)] : c.reduce((a, k) => IR[G.ITEMS[k].r] > IR[G.ITEMS[a].r] ? k : a, c[0]);
      A('i:' + k); continue;
    }
    if (st.phase === 'event') { if (!G.act(st, 'e:0')) A('e:1'); continue; }
    if (st.phase === 'rent') { A('$'); continue; }
    if (st.phase === 'spin') { A('s'); continue; }
    if (st.phase === 'choose') {
      const ch = st.choices;
      if (mode === 'random') { const k = ch[Math.floor(Math.random() * (ch.length + 1))]; A('p:' + (k || '')); continue; }
      let best = ch.reduce((a, k) => (TIER[k] || 3) > (TIER[a] || 3) ? k : a, ch[0]);
      if ((TIER[best] || 3) < 3 && G.canReroll(st)) { A('r'); continue; }
      A('p:' + (best && ((TIER[best] || 3) >= 3 || st.inv.length < 20) ? best : ''));
      while (st.removals > 0 && st.inv.length > 18 && st.phase === 'spin') {
        const worst = st.inv.reduce((a, s) => (TIER[s.key] || 3) < (TIER[a.key] || 3) ? s : a);
        if ((TIER[worst.key] || 3) > 2) break;
        A('x:' + worst.key);
      }
      continue;
    }
    throw new Error('phase ' + st.phase);
  }
  return st;
}
const n = +(process.argv[2] || 400), date = process.argv[3] || '2026-11-18';
let mismatch = 0;
for (const mode of ['random', 'smart']) {
  const res = [];
  for (let k = 0; k < n; k++) {
    const seed = (Math.random() * 4294967296) >>> 0;
    const st = play(date, seed, mode);
    const rp = G.replayDaily(date, seed, st.log);
    if (!rp || rp.rentIdx !== st.rentIdx || rp.totalEarned !== st.totalEarned || rp.phase !== st.phase) mismatch++;
    res.push(st.rentIdx);
  }
  res.sort((a, b) => a - b); const q = p => res[Math.min(res.length - 1, Math.floor(res.length * p))];
  const f0 = res.filter(x => x === 0).length / res.length * 100;
  console.log(`${date} ${mode.padEnd(6)} 最初の家賃で負け ${f0.toFixed(1)}%  中央値 ${q(.5)}  上位25% ${q(.75)}  上位10% ${q(.9)}  上位1% ${q(.99)}  最高 ${res[res.length - 1]}`);
}
console.log('再生の不一致', mismatch);
