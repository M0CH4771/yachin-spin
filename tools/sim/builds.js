// 作戦（ねらうシンボル）ごとに、エンドレスで何回払えるかをくらべる
// node tools/sim/builds.js [回数]
const G = require(process.env.ENGINE || '../../src/engine.js');
const src = require('fs').readFileSync(require('path').join(__dirname, 'balance.js'), 'utf8');
const TIER = eval('(' + src.slice(src.indexOf('const TIER = ') + 13, src.indexOf('};', src.indexOf('const TIER = ')) + 1) + ')');
const IR = { C: 1, U: 2, R: 3 };
const BUILDS = {
  'ふつう（強いものを取る）': [],
  'かたつむり': ['snail'],
  'かざん': ['kazan'],
  'やきいも': ['yakiimo'],
  'がまぐち＋小銭': ['purse', 'coin'],
  'つぼ＋食べる系': ['tsubo', 'oni', 'whale', 'goldfish', 'ninja'],
  'てんぐ（倍がけ）': ['tengu'],
  'ねこ＋さかな': ['cat', 'goldfish', 'sushi'],
  'りゅう': ['dragon'],
  'お茶＋だんご＋うさぎ＋みかづき': ['tea', 'dango', 'rabbit', 'mikazuki'],
  'にわとり＋たまご': ['chicken', 'egg', 'chick', 'basket'],
  'はち＋はちみつ': ['bee', 'honey', 'bear'],
  'いなほ＋ねずみ・すずめ': ['rice', 'mouse', 'sparrow', 'sun'],
  'かっぱ＋きゅうり': ['kappa', 'kyuri'],
  'こたつ＋みかん＋ねこ': ['kotatsu', 'mikan', 'cat'],
  'だるま＋ししまい（縁起物）': ['daruma', 'shishi', 'kadomatsu', 'pochi', 'hina'],
  'やたい＋食べ物': ['yatai', 'dango', 'onigiri', 'oden', 'tea'],
  'きつね＋きつねび＋いなり': ['fox', 'kitsunebi', 'inari', 'onigiri'],
  'ようかい（からかさ）': ['karakasa', 'ghost', 'tanuki', 'fox', 'kappa'],
  'たまや＋はなび': ['tamaya', 'firework'],
  'すすき＋みかづき': ['susuki', 'mikazuki', 'sun'],
  'ぼんおどり＋同じもの': ['bonodori', 'coin'],
  '金魚すくい＋さかな': ['kingyosukui', 'goldfish', 'koi', 'sushi', 'cat'],
  '小銭＋かどまつ＋がまぐち': ['coin', 'kadomatsu', 'purse', 'soroban'],
  'すずめ＋ねずみ＋へび': ['rice', 'mouse', 'sparrow', 'snake', 'sun'],
  'ちょうちょ＋さくら': ['butterfly', 'sakura'],
  'てんとう＋よつば': ['tentou', 'clover'],
};
function play(fav, seed) {
  const st = G.newGame('endless', { starter: 'basic' });
  let s = seed >>> 0; G.setRng(() => { s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; });
  const score = k => (fav.includes(k) ? 50 : 0) + (TIER[k] || 3);
  for (let g = 0; g < 8000 && st.phase !== 'over'; g++) {
    const ph = st.phase;
    if (ph === 'item') { const c = st.itemChoices || []; G.act(st, 'i:' + (c.length ? c.reduce((a, k) => IR[G.ITEMS[k].r] > IR[G.ITEMS[a].r] ? k : a, c[0]) : '')); }
    else if (ph === 'event') { if (!G.act(st, 'e:0')) G.act(st, 'e:1'); }
    else if (ph === 'rent') G.act(st, '$');
    else if (ph === 'spin') G.act(st, 's');
    else if (ph === 'choose') {
      const ch = st.choices, best = ch.reduce((a, k) => score(k) > score(a) ? k : a, ch[0]);
      if (score(best) < 3 && G.canReroll(st)) { G.act(st, 'r'); continue; }
      G.act(st, 'p:' + (best && (score(best) >= 50 || st.inv.length < 20) ? best : ''));
      while (st.removals > 0 && st.inv.length > 18 && st.phase === 'spin') {
        const worst = st.inv.reduce((a, x) => score(x.key) < score(a.key) ? x : a);
        if (score(worst.key) > 3) break; G.act(st, 'x:' + worst.key);
      }
    } else break;
  }
  G.setRng(null);
  return { rents: st.rentIdx, best: st.best, cnt: fav.length ? st.inv.filter(x => fav.includes(x.key)).length : 0 };
}
const n = +(process.argv[2] || 400);
for (const [name, fav] of Object.entries(BUILDS)) {
  const r = []; let bestSum = 0, cnt = 0;
  for (let k = 0; k < n; k++) { const o = play(fav, k * 2654435761); r.push(o.rents); bestSum += o.best; cnt += o.cnt; }
  r.sort((a, b) => a - b); const q = p => r[Math.min(n - 1, Math.floor(n * p))];
  console.log(`${name.padEnd(14, '　')} 中央値 ${String(q(.5)).padStart(3)}  上位25% ${String(q(.75)).padStart(3)}  上位10% ${String(q(.9)).padStart(3)}  最高 ${String(r[n - 1]).padStart(3)}  ｜最高の1スピン平均 ${Math.round(bestSum / n)}  ねらいの数 ${(cnt / n).toFixed(1)}`);
}
