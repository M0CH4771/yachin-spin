// シンボル1種類ずつ「出たら必ず取る」で遊ばせて、強さの一覧を出す
// node tools/sim/each.js [回数]
const G = require(process.env.ENGINE || '../../src/engine.js');
const fs = require('fs'), path = require('path');
const src = fs.readFileSync(path.join(__dirname, 'builds.js'), 'utf8');
const play = new Function('G', 'require', src.slice(src.indexOf('const src ='), src.indexOf('const n = ')).replace("require('path').join(__dirname, 'balance.js')", JSON.stringify(path.join(__dirname, 'balance.js'))) + '; return play;')(G, require);
const n = +(process.argv[2] || 120);
const base = []; for (let k = 0; k < n; k++) base.push(play([], k * 2654435761).rents);
const med = a => { const b = a.slice().sort((x, y) => x - y); return b[Math.floor(b.length / 2)]; };
const avg = a => a.reduce((x, y) => x + y, 0) / a.length;
const B = avg(base);
const rows = [];
for (const k of Object.keys(G.SYM)) {
  if (G.SYM[k].r === 'X' || G.SYM[k].noPick) continue;
  const r = []; let cnt = 0;
  for (let j = 0; j < n; j++) { const o = play([k], j * 2654435761); r.push(o.rents); cnt += o.cnt; }
  rows.push({ k, n: G.SYM[k].n, r: G.SYM[k].r, avg: avg(r), med: med(r), cnt: cnt / n });
}
rows.sort((a, b) => b.avg - a.avg);
console.log(`基準（ねらいなし）平均 ${B.toFixed(1)} 回`);
rows.forEach((x, i) => console.log(`${String(i + 1).padStart(2)} ${(x.n + '（' + x.k + '）').padEnd(18, '　')} ${x.r}  平均 ${x.avg.toFixed(1)}  差 ${(x.avg - B >= 0 ? '+' : '') + (x.avg - B).toFixed(1)}  中央値 ${x.med}  集めた数 ${x.cnt.toFixed(1)}`));
