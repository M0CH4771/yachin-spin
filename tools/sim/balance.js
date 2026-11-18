const G = require('../../src/engine.js');
const TIER = { dragon: 10, oni: 6, rainbow: 9, torii: 6, moon: 6, hanafuda: 7, castle: 7, clover: 5,
  cat: 6, fox: 6, lantern: 8, koi: 4, chick: 4, chicken: 4, firework: 5, sake: 5, shooting: 3, purse: 4,
  oden: 3, yakiimo: 3, kakigori: 3, ika: 3, turtle: 3, crab: 2, pochi: 2, bomb: 2, bee: 3, ghost: 3, tanzaku: 4, nobori: 5, taiko: 5, piggy: 5, tanuki: 3, soroban: 4, honey: 4, misemono: 4, dog: 4, ramen: 4, bear: 6, fuji: 6, sun: 5, crystal: 6, kadomatsu: 5, hina: 5, mallet: 5, mirror: 7, whale: 7, tengu: 9, japan: 7,
  butterfly: 3, sparrow: 3, snail: 3, octopus: 4, snake: 4, sushi: 4, fugu: 3, kaminari: 4, eagle: 6, wave: 5, ninja: 6, kusudama: 7,
  mame: 2, senbei: 2, shika: 3, suzumushi: 3, tentou: 2, mikazuki: 3, tsubo: 4, fukurou: 4, koryu: 4, suika: 4, yabusame: 4, kujaku: 6, hanamaru: 5, kazan: 8, coin: 2, tea: 2, dango: 3, goldfish: 3, rice: 2, onigiri: 3, seed: 3, egg: 2, mouse: 3, dice: 3, rabbit: 3, frog: 3, furin: 2, sakura: 4 };
const IR = { C: 1, U: 2, R: 3 };
function play(diff, mode) {
  const st = G.newGame(diff);
  for (let guard = 0; guard < 400; guard++) {
    if (st.phase === 'item') {
      while (st.itemPicks > 0) {
        G.rollItems(st);
        const c = st.itemChoices; if (!c.length) { st.itemPicks = 0; break; }
        const k = mode === 'random' ? c[Math.floor(Math.random() * c.length)] : c.reduce((a, k) => IR[G.ITEMS[k].r] > IR[G.ITEMS[a].r] ? k : a, c[0]);
        G.addItem(st, k); st.itemPicks--;
      }
      st.phase = 'spin';
    }
    G.spin(st);
    const ch = G.rollChoices(st);
    if (mode === 'random') { const k = ch[Math.floor(Math.random() * (ch.length + 1))]; if (k) st.inv.push(G.mk(k)); }
    else {
      let best = ch.reduce((a, k) => TIER[k] > TIER[a] ? k : a, ch[0]);
      if (TIER[best] < 3 && G.canReroll(st)) { st.rerolls--; const c2 = G.rollChoices(st); best = c2.reduce((a, k) => TIER[k] > TIER[a] ? k : a, c2[0]); }
      if (best && (TIER[best] >= 3 || st.inv.length < 20)) st.inv.push(G.mk(best));
      while (st.removals > 0 && st.inv.length > 18) {
        const worst = st.inv.reduce((a, s) => TIER[s.key] < TIER[a.key] ? s : a);
        if (TIER[worst.key] > 2) break;
        G.removeSymbol(st, worst.key);
      }
    }
    if (G.rentDue(st)) {
      const info = G.payRent(st);
      if (!info.ok || st.phase === 'clear') return st.rentIdx;
      if (st.event) G.runEvent(st, Math.random() < 0.5 ? 0 : 1);
      st.phase = 'item';
    }
  }
  return st.rentIdx;
}
for (const diff of ['easy', 'normal', 'hard', 'super']) {
  for (const mode of ['random', 'smart']) {
    const R = G.totalRents({ diff }); const n = 1500; let clear = 0, sum = 0;
    const hist = new Array(R + 1).fill(0);
    for (let k = 0; k < n; k++) { const r = play(diff, mode); hist[r]++; if (r >= R) clear++; sum += r; }
    console.log(diff.padEnd(6), mode.padEnd(6), 'clear', (clear / n * 100).toFixed(1) + '%', 'avg paid', (sum / n).toFixed(1));
  }
}
