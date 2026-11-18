// エンドレスの到達回数の分布を調べる
const G = require('../../src/engine.js');
const src = require('fs').readFileSync(require('path').join(__dirname, 'balance.js'), 'utf8');
const body = src.slice(0, src.indexOf("for (const diff of"));
const play = new Function('G', 'require', body.replace("const G = require('../../src/engine.js');", '').replace('guard < 400', 'guard < 3000') + '; return play;')(G, require);
const growth = +(process.argv[2] || 1.22), mul = +(process.argv[3] || 0.9);
G.DIFFS.endless.growth = growth; G.DIFFS.endless.rentMul = mul;
for (const mode of ['random', 'smart']) {
  const n = 1200, res = [];
  for (let k = 0; k < n; k++) res.push(play('endless', mode));
  res.sort((a, b) => a - b);
  const q = p => res[Math.floor(p * (n - 1))];
  console.log(`growth ${growth} mul ${mul} ${mode.padEnd(6)} 中央値 ${q(.5)}  上位25% ${q(.75)}  上位10% ${q(.9)}  上位1% ${q(.99)}  最高 ${res[n - 1]}`);
}
