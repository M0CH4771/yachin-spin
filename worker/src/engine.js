// tools/build.py が src/engine.js から作るファイル。直接編集しない
// ===== ヤチンスピン ゲームエンジン（UI非依存） =====
const W = 5, H = 4, N = W * H;
let RNG_FN = null;
const rnd = () => RNG_FN ? RNG_FN() : Math.random();
function setRng(fn) { RNG_FN = fn; }

const RARITY = {
  C: { name: 'コモン', color: '#c9d1dc' },
  U: { name: 'アンコモン', color: '#5fd99b' },
  R: { name: 'レア', color: '#5aa9ff' },
  V: { name: 'ベリーレア', color: '#ffb547' },
  S: { name: 'とくべつ', color: '#ff86c3' },
};

const FOODL = ['dango', 'chadango', 'tea', 'onigiri', 'oden', 'yakiimo', 'kakigori', 'ika', 'ramen', 'honey', 'senbei', 'sushi', 'inari', 'mikan', 'kyuri'];
const ENGIL = ['kadomatsu', 'pochi', 'hina', 'kusudama', 'mallet', 'daruma', 'shishi'];
const YOKAIL = ['ghost', 'oni', 'tengu', 'tanuki', 'fox', 'kappa', 'kitsunebi', 'karakasa'];
const ENGI = new Set(ENGIL), YOKAI = new Set(YOKAIL);
const PLANTL = ['rice', 'sakura', 'tanzaku', 'kadomatsu', 'seed', 'susuki'];
const JAPANL = ['fuji', 'torii', 'castle', 'sakura', 'nobori'];
const SEAL = ['goldfish', 'ika', 'crab', 'turtle', 'whale', 'octopus', 'fugu'];
const SEA = new Set(SEAL);
const FOOD = new Set(FOODL), PLANTS = new Set(PLANTL), JAPAN = new Set(JAPANL);
const CORNERS = new Set([0, W - 1, W * (H - 1), W * H - 1]);
const CENTER = new Set([W + 1, W + 2, W + 3, 2 * W + 1, 2 * W + 2, 2 * W + 3]);
const isEdge = i => { const x = i % W, y = (i / W) | 0; return x === 0 || y === 0 || x === W - 1 || y === H - 1; };

// p: 処理フェーズ（0=食べる/壊す 1=加算 2=倍率） / likes: 相性のいいシンボル（'*' は全部）
const SYM = {
  coin:     { e: '🪙', n: '小銭', r: 'C', v: 1, likes: ['purse'], d: 'ただの1コイン。' },
  tea:      { e: '🍵', n: 'お茶', r: 'C', v: 1, likes: ['dango'], d: 'ただの1コイン。🍡のとなりに出ると、合体して🥮おちゃだんごになる。' },
  dango:    { e: '🍡', n: 'だんご', r: 'C', v: 1, p: 1, likes: ['tea', 'rabbit', 'moon'], d: 'となりの🍵と合体して🥮おちゃだんごになる',
              act(c, i) { const j = c.nb(i).find(j => c.key(j) === 'tea'); if (j !== undefined) { c.merge(i, j); c.transform(i, 'chadango', j); } } },
  chadango: { e: '🥮', n: 'おちゃだんご', r: 'S', v: 3, p: 1, store: true, likes: ['chadango', 'rabbit', 'moon'], d: '3コイン。となりの🥮 1つにつき +2。となりに🥮がいれば、どっちも育つ（+2）',
              act(c, i, s) { let hit = false; c.nb(i).forEach(j => { if (c.key(j) === 'chadango') { c.add(i, 2, j); hit = true; } }); if (hit) c.grow(s, 2); } },
  goldfish: { e: '🐟', n: '金魚', r: 'C', v: 1, likes: ['koi', 'cat'], d: 'ただの1コイン。🎏で増える、🐱に食べられる。' },
  rice:     { e: '🌾', n: 'いなほ', r: 'C', v: 1, likes: ['mouse'], d: 'ただの1コイン。🐭🐦のエサ。' },
  onigiri:  { e: '🍙', n: 'おにぎり', r: 'C', v: 2, likes: ['fox'], d: '2コイン。🦊のエサ。' },
  seed:     { e: '🌱', n: 'たね', r: 'C', v: 0, grow: 4, d: '盤面に4回出ると 🌸さくら（5コイン）に育つ' },
  egg:      { e: '🥚', n: 'たまご', r: 'C', v: 1, likes: ['chicken'], d: '盤面に出るたび 20%で 🐣ひよこ にかえる（🐔のとなりなら50%）' },
  mouse:    { e: '🐭', n: 'ねずみ', r: 'C', v: 1, p: 4, store: true, likes: ['rice', 'cat', 'fox', 'sake'], d: 'となりの🌾を食べる。1つにつき +5、育つ（+2、食べるたびに育つ量が+1ずつ増える。10%で今の育ちが ×2）',
              act(c, i, s) { c.nb(i).forEach(j => { if (c.key(j) === 'rice') { c.eat(i, j, 5); c.eatGrow(s, 2); } }); } },
  dice:     { e: '🎲', n: 'サイコロ', r: 'C', v: 0, p: 1, d: '毎回 0〜4コインのどれか',
              act(c, i) { c.add(i, Math.floor(rnd() * 5), 'サイコロの目'); } },
  rabbit:   { e: '🐰', n: 'うさぎ', r: 'C', v: 1, p: 1, store: true, likes: ['dango', 'moon', 'sake'], d: 'となりの🍡🥮 1つにつき +2。となりにいれば育つ（+2、最大+30）',
              act(c, i, s) { let hit = false; c.nb(i).forEach(j => { if (c.key(j) === 'dango' || c.key(j) === 'chadango') { c.add(i, 2, j); hit = true; } }); if (hit) c.grow(s, 2, 30); } },
  frog:     { e: '🐸', n: 'かえる', r: 'C', v: 1, p: 1, likes: ['frog', 'sake'], d: '盤面のほかの🐸 1匹につき +1（どこにいてもOK）',
              act(c, i) { c.all().forEach(j => { if (j !== i && c.key(j) === 'frog') c.add(i, 1, j); }); } },
  cat:      { e: '🐱', n: 'ねこ', r: 'U', v: 1, p: 4, store: true, likes: ['goldfish', 'mouse', 'sake', 'kotatsu'], d: 'となりの🐟と🐭を食べる。1匹につき +8、育つ（+2、食べるたびに育つ量が+1ずつ増える。10%で今の育ちが ×2）',
              act(c, i, s) { c.nb(i).forEach(j => { const k = c.key(j); if (k === 'goldfish' || k === 'mouse') { c.eat(i, j, 8); c.eatGrow(s, 2); } }); } },
  fox:      { e: '🦊', n: 'きつね', r: 'U', v: 2, p: 4, store: true, likes: ['mouse', 'onigiri', 'inari', 'torii', 'sake', 'kitsunebi'], d: 'となりの🐭を食べて +10、🍙🥟を食べて +5。食べるたび育つ（+2、食べるたびに育つ量が+1ずつ増える。10%で今の育ちが ×2）',
              act(c, i, s) { c.nb(i).forEach(j => { const k = c.key(j); if (k === 'mouse') { c.eat(i, j, 10); c.eatGrow(s, 2); } else if (k === 'onigiri' || k === 'inari') { c.eat(i, j, 5); c.eatGrow(s, 2); } }); } },
  lantern:  { e: '🏮', n: 'ちょうちん', r: 'U', v: 0, p: 2, likes: ['*'], d: 'となりのシンボル全部の稼ぎを ×2',
              act(c, i) { const m = c.has('candle') ? 3 : 2; c.nb(i).forEach(j => c.mul(j, m, i)); } },
  koi:      { e: '🎏', n: 'こいのぼり', r: 'U', v: 1, p: 2, likes: ['goldfish'], d: 'となりの🐟の稼ぎを ×4',
              act(c, i) { c.nb(i).forEach(j => { if (c.key(j) === 'goldfish') c.mul(j, 4, i); }); } },
  chick:    { e: '🐣', n: 'ひよこ', r: 'U', v: 1, grow: 3, likes: ['chicken'], d: '盤面に3回出ると 🐔にわとり に育つ' },
  chicken:  { e: '🐔', n: 'にわとり', r: 'U', v: 2, p: 1, store: true, likes: ['egg', 'chick', 'sake'], d: '盤面に出るたび 15%で🥚を産む。となりの🥚は50%で🐣にかえる。となりの🥚🐣 1つにつき育つ（+2）',
              act(c, i, s) { c.nb(i).forEach(j => { const k = c.key(j); if (k === 'egg' || k === 'chick') c.grow(s, 2); }); } },
  firework: { e: '🎆', n: 'はなび', r: 'U', v: 0, p: 1, d: '盤面に5回出ると打ち上がって +40。打ち上げ後はなくなる',
              act(c, i, s) { s.c = (s.c || 0) + 1; if (s.c >= 5) { c.add(i, 40, 'うちあげ'); c.vanish(i); } } },
  sake:     { e: '🍶', n: 'おさけ', r: 'U', v: 1, p: 1, likes: ['cat', 'fox', 'frog', 'rabbit', 'mouse', 'chicken', 'dog', 'tanuki', 'ika'], d: 'となりの動物（🐱🦊🐸🐰🐭🐔🐶🦝🐢🦀など）1匹につき +2',
              act(c, i) { c.nb(i).forEach(j => { if (ANIMALS.has(c.key(j))) c.add(i, 2, j); }); } },
  shooting: { e: '🎯', n: 'しゃてき', r: 'U', v: 1, p: 4, likes: ['*'], d: 'となりでいちばん安いシンボルを撃ち落とす（手持ちから消える）。その基本の稼ぎ（育った分もふくむ）×8を獲得',
              act(c, i) { const t = c.nb(i); if (!t.length) return; const j = t.reduce((a, b) => c.baseOf(b) < c.baseOf(a) ? b : a); c.eat(i, j, Math.max(1, c.baseOf(j)) * 8); } },
  purse:    { e: '👛', n: 'がまぐち', r: 'U', v: 0, p: 4, store: true, likes: ['coin'], d: 'となりの🪙を吸い込む。1枚につき、このがまぐちが育つ（+3 ＋ その🪙の稼ぎ。かどまつなどの倍がけも込み。食べるたびに育つ量が+1ずつ増える。10%で今の育ちが ×2）',
              act(c, i, s) { c.nb(i).forEach(j => { if (c.key(j) === 'coin') { const v = c.valueNow(j); c.eat(i, j, 0); c.eatGrow(s, 3 + v); } }); } },
  sakura:   { e: '🌸', n: 'さくら', r: 'S', v: 5, d: '5コイン。🌱から育つ。' },

  torii:    { e: '⛩️', n: 'とりい', r: 'R', v: 3, p: 1, likes: ['fox'], d: '盤面の🦊 1匹につき +6（どこにいてもOK）',
              act(c, i) { c.all().forEach(j => { if (c.key(j) === 'fox') c.add(i, 6, j); }); } },
  moon:     { e: '🌕', n: 'まんげつ', r: 'S', v: 3, p: 2, likes: ['rabbit', 'dango', 'chadango', 'mikazuki', 'hangetsu'], d: '🌓はんげつ どうしの合体でできる。盤面の🐰🍡🥮すべての稼ぎを ×2（🌕が2つなら ×4）',
              act(c, i) { c.all().forEach(j => { const k = c.key(j); if (k === 'rabbit' || k === 'dango' || k === 'chadango') c.mul(j, 2, i); }); } },
  hanafuda: { e: '🎴', n: 'はなふだ', r: 'R', v: 0, p: 1, d: '盤面に出ているシンボルの種類の数だけ +1',
              act(c, i) { c.add(i, new Set(c.all().map(j => c.key(j))).size, '種類の数'); } },
  clover:   { e: '🍀', n: 'よつば', r: 'R', v: 1, d: '1コイン。持っているだけで候補にレアが出やすくなる' },
  castle:   { e: '🏯', n: 'おしろ', r: 'R', v: 2, p: 1, likes: ['*'], d: 'となりのシンボル 1つにつき +2',
              act(c, i) { c.nb(i).forEach(j => c.add(i, 2, j)); } },

  dragon:   { e: '🐉', n: 'りゅう', r: 'V', v: 15, d: '15コイン。ただただ強い' },
  oni:      { e: '👹', n: 'おに', r: 'V', v: 0, p: 4, likes: ['*'], d: 'となりのシンボルを全部食べる（手持ちから消える）。1つにつき +12。となりに🫘があると、食べる前に追い払われる',
              // となりにまめがいると、食べる前に追い払われる（盤面の位置に関係なく、まめが勝つ）
              act(c, i) { const nb = c.nb(i); if (nb.some(j => c.key(j) === 'mame')) return; nb.forEach(j => c.eat(i, j, 12)); } },
  rainbow:  { e: '🌈', n: 'にじ', r: 'V', v: 0, p: 1, likes: ['*'], d: '盤面のすべてのシンボルに +1',
              act(c, i) { c.all().forEach(j => c.add(j, 1, i)); } },

  // ===== 追加シンボル =====
  oden:     { e: '🍢', n: 'おでん', r: 'C', v: 1, p: 4, store: true, likes: FOODL.concat(['yatai']), d: 'となりの食べ物を鍋に入れて煮込む（食べる）。1つにつき +1、その稼ぎ（育った分も）だけ育つ（食べるたびに育つ量が+1ずつ増える。10%で今の育ちが ×2）。となりに🛖があれば、煮込んだスピンは今の育ちが ×2',
              act(c, i, s) {
                let n = 0; c.nb(i).forEach(j => { const k = c.key(j); if (FOOD.has(k) && k !== 'oden') { const v = c.base(j); c.eat(i, j, 1); c.eatGrow(s, v); n++; } });
                if (n && c.nb(i).some(j => c.key(j) === 'yatai')) s.c = (s.c || 0) * 2;
              } },
  yakiimo:  { e: '🍠', n: 'やきいも', r: 'C', v: 1, p: 1, store: true, hint: '出るたび育つ', d: '盤面に出るたび育つ（+1、最大+5）',
              act(c, i, s) { if ((s.c || 0) < 5) s.c = (s.c || 0) + 1; } },
  kakigori: { e: '🍧', n: 'かきごおり', r: 'C', v: 4, p: 1, hint: '期間限定', d: '4コイン。でも盤面に3回出ると溶けてなくなる',
              act(c, i, s) { s.c = (s.c || 0) + 1; if (s.c >= 3) c.vanish(i, 'とけた'); } },
  ika:      { e: '🦑', n: 'いかやき', r: 'C', v: 2, p: 1, likes: ['sake'], d: 'となりの🍶 1本につき +4',
              act(c, i) { c.nb(i).forEach(j => { if (c.key(j) === 'sake') c.add(i, 4, j); }); } },
  turtle:   { e: '🐢', n: 'かめ', r: 'C', v: 1, p: 1, store: true, likes: SEAL.concat(['wave']), d: '盤面の4すみにいると +6。となりの海の生き物 1つにつき育つ（+1）。となりに海の生き物がいて、盤面に🌊がいると、10%で今の育ちが ×1.5',
              act(c, i, s) { if (CORNERS.has(i)) c.add(i, 6, 'すみっこ'); const n = c.nb(i).filter(j => SEA.has(c.key(j))).length; if (n) { c.grow(s, n); if (c.all().some(j => c.key(j) === 'wave') && rnd() < 0.1) s.c = Math.floor((s.c || 0) * 1.5); } } },
  crab:     { e: '🦀', n: 'かに', r: 'C', v: 1, p: 1, hint: '外周で強い', d: '盤面のふち（外周）にいると +2',
              act(c, i) { if (isEdge(i)) c.add(i, 2, 'ふち'); } },
  pochi:    { e: '🧧', n: 'ポチぶくろ', r: 'C', v: 0, p: 1, hint: '運しだい', d: '10%で +25。ハズレは0',
              act(c, i) { if (rnd() < 0.1) { c.add(i, 25, 'あたり！'); c.flag('pochi'); } } },
  bomb:     { e: '🧨', n: 'かんしゃくだま', r: 'C', v: 0, p: 1, likes: ['*'], d: '盤面に出るとはじけてなくなる。そのとき、となりのシンボル全部に +3',
              act(c, i) { c.nb(i).forEach(j => c.add(j, 3, i)); c.vanish(i, 'はじけた'); } },
  bee:      { e: '🐝', n: 'みつばち', r: 'C', v: 1, p: 1, store: true, likes: ['honey', 'bear'], d: '盤面に出るたび 20%で🍯を手持ちに追加。となりに🍯がいれば育つ（+2）',
              act(c, i, s) { if (rnd() < 0.2) c.spawn('honey', i); if (c.nb(i).some(j => c.key(j) === 'honey')) c.grow(s, 2); } },
  ghost:    { e: '👻', n: 'おばけ', r: 'C', v: 3, p: 1, likes: ['dog'], d: '3コイン。でも盤面に出るたび 15%でいなくなる',
              act(c, i) { if (rnd() < 0.15) c.vanish(i, 'きえた'); } },

  tanzaku:  { e: '🎋', n: 'たんざく', r: 'U', v: 1, p: 1, hint: '横の列に効く', d: '同じ横の列にいるほかのシンボル 1つにつき +1',
              act(c, i) { c.all().forEach(j => { if (j !== i && c.row(j) === c.row(i)) c.add(i, 1, j); }); } },
  nobori:   { e: '🎌', n: 'のぼり', r: 'U', v: 1, p: 1, hint: '縦の列に効く', d: '同じ縦の列にいるほかのシンボル 1つにつき +2',
              act(c, i) { c.all().forEach(j => { if (j !== i && c.col(j) === c.col(i)) c.add(i, 2, j); }); } },
  taiko:    { e: '🥁', n: 'たいこ', r: 'U', v: 1, p: 1, hint: '縦の列に効く', d: '同じ縦の列にいるほかのシンボル全部に +2',
              act(c, i) { c.all().forEach(j => { if (j !== i && c.col(j) === c.col(i)) c.add(j, 2, i); }); } },
  piggy:    { e: '🐷', n: 'ちょきんばこ', r: 'U', v: 0, p: 1, hint: 'ためるほど強い', d: 'もちコイン 25枚につき +1（最大 +10）',
              act(c, i) { const n = Math.min(10, Math.floor(c.coins / 25)); if (n) c.add(i, n, 'ちょきん'); } },
  tanuki:   { e: '🦝', n: 'たぬき', r: 'U', v: 2, p: 1, likes: ['*'], d: 'となりのシンボルを1つ、手持ちでいちばん多いシンボルに化かす（手持ちごと変わる）。化かされても、それまでの育ちはそのまま残る',
              act(c, i) { const top = c.topInv(['tanuki']); if (!top) return; const t = c.nb(i).filter(j => c.key(j) !== 'tanuki' && c.key(j) !== top); if (t.length) c.transform(t[Math.floor(rnd() * t.length)], top, i, 0, true); } },
  soroban:  { e: '🧮', n: 'そろばん', r: 'U', v: 1, p: 1, likes: ['coin'], d: '盤面の🪙 1枚につき +2（どこにいてもOK）',
              act(c, i) { c.all().forEach(j => { if (c.key(j) === 'coin') c.add(i, 2, j); }); } },
  honey:    { e: '🍯', n: 'はちみつ', r: 'U', v: 3, p: 1, store: true, likes: ['bee', 'bear'], d: '3コイン。となりの🐝 1匹につき +2。となりにいれば育つ（+2）',
              act(c, i, s) { let hit = false; c.nb(i).forEach(j => { if (c.key(j) === 'bee') { c.add(i, 2, j); hit = true; } }); if (hit) c.grow(s, 2); } },
  misemono: { e: '🎪', n: 'みせもの小屋', r: 'U', v: 1, p: 1, hint: 'まんなかで強い', d: '盤面のまんなか（中央の6マス）にいると +5',
              act(c, i) { if (CENTER.has(i)) c.add(i, 5, 'まんなか'); } },
  dog:      { e: '🐶', n: 'いぬ', r: 'U', v: 2, p: 4, likes: ['ghost', 'sake'], d: '2コイン。となりの👻をほえて追い払う（消える）。1匹につき +10',
              act(c, i) { c.nb(i).forEach(j => { if (c.key(j) === 'ghost') c.eat(i, j, 10); }); } },
  ramen:    { e: '🍜', n: 'ラーメン', r: 'U', v: 0, p: 1, likes: FOODL, d: '盤面に出ている食べ物の種類の数 ×2',
              act(c, i) { const n = new Set(c.all().map(j => c.key(j)).filter(k => FOOD.has(k))).size; c.add(i, n * 2, '食べ物の種類'); } },

  bear:     { e: '🐻', n: 'くま', r: 'R', v: 2, p: 4, store: true, likes: ['honey', 'bee'], d: 'となりの🍯を食べる。1つにつき +12、育つ（+4、食べるたびに育つ量が+1ずつ増える。10%で今の育ちが ×2）',
              act(c, i, s) { c.nb(i).forEach(j => { if (c.key(j) === 'honey') { c.eat(i, j, 12); c.eatGrow(s, 4); } }); } },
  fuji:     { e: '🗻', n: 'ふじさん', r: 'R', v: 3, p: 2, likes: ['japan'], hint: '上の段で強い', d: '3コイン。いちばん上の段にいると稼ぎ ×3',
              act(c, i) { if (c.row(i) === 0) c.mul(i, 3, i); } },
  sun:      { e: '☀️', n: 'おひさま', r: 'R', v: 2, p: 2, likes: PLANTL, d: '盤面の植物（🌾🌸🎋🎍）の稼ぎをすべて ×2。🌱も2倍速で育つ',
              act(c, i) { c.all().forEach(j => { if (PLANTS.has(c.key(j))) c.mul(j, 2, i); }); } },
  crystal:  { e: '🔮', n: 'すいしょう', r: 'R', v: 0, p: 1, hint: 'そろえるほど強い', d: '盤面でいちばん多い種類のシンボルの数 ×3',
              act(c, i) { const m = {}; c.all().forEach(j => { const k = c.key(j); m[k] = (m[k] || 0) + 1; }); const top = Object.entries(m).sort((a, b) => b[1] - a[1])[0]; if (top) c.add(i, top[1] * 3, `${SYM[top[0]].e}×${top[1]}`); } },
  kadomatsu:{ e: '🎍', n: 'かどまつ', r: 'R', v: 2, p: 2, likes: ['coin', 'purse', 'soroban'], d: '盤面の🪙すべての稼ぎを ×2。家賃を払うたびに 🪙を3枚 手持ちに追加',
              act(c, i) { c.all().forEach(j => { if (c.key(j) === 'coin') c.mul(j, 2, i); }); } },
  hina:     { e: '🎎', n: 'ひなにんぎょう', r: 'R', v: 3, p: 2, likes: ['hina'], d: '3コイン。盤面にほかの🎎がいると稼ぎ ×3',
              act(c, i) { if (c.all().some(j => j !== i && c.key(j) === 'hina')) { c.mul(i, 3, i); c.flag('hina'); } } },
  mallet:   { e: '🔨', n: 'うちでのこづち', r: 'R', v: 1, p: 1, likes: ['*'], d: '盤面に出るたび 1/3で、となりのシンボルを1つ手持ちに複製',
              act(c, i) { const t = c.nb(i); if (t.length && rnd() < 1 / 3) c.spawn(c.key(t[Math.floor(rnd() * t.length)]), i); } },
  mirror:   { e: '🪞', n: 'かがみ', r: 'R', v: 0, p: 3, likes: ['*'], d: 'となりで いちばん稼いだシンボルと同じだけ稼ぐ',
              act(c, i) { let best = 0, bj = null; c.nb(i).forEach(j => { if (c.key(j) === 'mirror') return; const v = c.valueNow(j); if (v > best) { best = v; bj = j; } }); if (bj !== null) c.add(i, best, bj); } },

  butterfly:{ e: '🦋', n: 'ちょうちょ', r: 'C', v: 1, p: 1, store: true, likes: ['sakura'], d: 'となりの🌸 1つにつき +4。となりにいれば育つ（+2）',
              act(c, i, s) { let hit = false; c.nb(i).forEach(j => { if (c.key(j) === 'sakura') { c.add(i, 4, j); hit = true; } }); if (hit) c.grow(s, 2); } },
  sparrow:  { e: '🐦', n: 'すずめ', r: 'C', v: 1, p: 4, store: true, likes: ['rice'], d: 'となりの🌾を食べる。1つにつき +4、育つ（+2、食べるたびに育つ量が+1ずつ増える。10%で今の育ちが ×2）',
              act(c, i, s) { c.nb(i).forEach(j => { if (c.key(j) === 'rice') { c.eat(i, j, 4); c.eatGrow(s, 2); } }); } },
  snail:    { e: '🐌', n: 'かたつむり', r: 'C', v: 0, p: 1, store: true, hint: 'ゆっくり育つ', d: '盤面に出るたび育つ（+1、上限なし）',
              act(c, i, s) { s.c = (s.c || 0) + 1; } },
  octopus:  { e: '🐙', n: 'たこ', r: 'C', v: 1, p: 1, likes: ['*'], d: 'となりのシンボル 1つにつき +1',
              act(c, i) { c.nb(i).forEach(j => c.add(i, 1, j)); } },
  snake:    { e: '🐍', n: 'へび', r: 'U', v: 1, p: 4, store: true, likes: ['mouse', 'frog', 'eagle'], d: 'となりの🐭と🐸を食べる。1匹につき +8、育つ（+2、食べるたびに育つ量が+1ずつ増える。10%で今の育ちが ×2）',
              act(c, i, s) { c.nb(i).forEach(j => { const k = c.key(j); if (k === 'mouse' || k === 'frog') { c.eat(i, j, 8); c.eatGrow(s, 2); } }); } },
  sushi:    { e: '🍣', n: 'おすし', r: 'U', v: 2, p: 1, store: true, likes: ['goldfish'], d: 'となりの🐟 1匹につき +3。となりにいれば育つ（+2）',
              act(c, i, s) { let hit = false; c.nb(i).forEach(j => { if (c.key(j) === 'goldfish') { c.add(i, 3, j); hit = true; } }); if (hit) c.grow(s, 2); } },
  fugu:     { e: '🐡', n: 'ふぐ', r: 'U', v: 7, p: 2, hint: 'ハイリスク', d: '7コイン。でも25%で毒にあたって、自分ととなりの稼ぎが0',
              act(c, i) { if (rnd() < 0.25) { c.mul(i, 0, 'どく'); c.nb(i).forEach(j => c.mul(j, 0, 'どく')); c.flag('fugu'); } } },
  kaminari: { e: '⚡', n: 'かみなり', r: 'U', v: 0, p: 1, hint: '運しだい', d: '盤面のランダムな3つのシンボルに +5',
              act(c, i) { const a = c.all(); for (let k = 0; k < 3 && a.length; k++) { const j = a.splice(Math.floor(rnd() * a.length), 1)[0]; c.add(j, 5, i); } } },
  eagle:    { e: '🦅', n: 'わし', r: 'R', v: 2, p: 4, store: true, likes: ['snake', 'goldfish', 'mouse'], d: 'となりの🐍🐟🐭を食べる。1匹につき +14。食べた相手の稼ぎ（育った分も）だけ、わしが育つ（食べるたびに育つ量が+1ずつ増える。10%で今の育ちが ×2）',
              act(c, i, s) { c.nb(i).forEach(j => { const k = c.key(j); if (k === 'snake' || k === 'goldfish' || k === 'mouse') { const v = c.base(j); c.eat(i, j, 14); c.eatGrow(s, v); } }); } },
  wave:     { e: '🌊', n: 'おおなみ', r: 'R', v: 1, p: 2, likes: SEAL, d: '盤面の海の生き物（🐟🦑🦀🐢🐙🐡🐋）の稼ぎをすべて ×2',
              act(c, i) { c.all().forEach(j => { if (SEA.has(c.key(j))) c.mul(j, 2, i); }); } },
  ninja:    { e: '🥷', n: 'にんじゃ', r: 'R', v: 0, p: 1, hint: '手持ちをへらす', d: '盤面に出るたび、盤面に出ていない手持ちから いちばん安いシンボルを1つ消して +15',
              act(c, i) { if (c.purgeCheapest()) c.add(i, 15, 'しのび'); } },
  kusudama: { e: '🎊', n: 'くすだま', r: 'V', v: 1, p: 1, hint: '運しだい', d: '盤面に出るたび 30%で割れて、盤面のすべてのシンボルに +5',
              act(c, i) { if (rnd() < 0.3) { c.all().forEach(j => c.add(j, 5, i)); c.flag('kusudama'); } } },
  mame:     { e: '🫘', n: 'まめ', r: 'C', v: 1, p: 4, likes: ['oni'], d: 'おには外！ となりの👹を追い払う（消える）。1匹につき +25',
              act(c, i) { c.nb(i).forEach(j => { if (c.key(j) === 'oni') c.eat(i, j, 25); }); } },
  senbei:   { e: '🍘', n: 'せんべい', r: 'C', v: 1, likes: ['shika'], d: 'ただの1コイン。🦌の大好物。' },
  shika:    { e: '🦌', n: 'しか', r: 'C', v: 1, p: 4, likes: ['senbei'], d: 'となりの🍘を食べる。1つにつき +6',
              act(c, i) { c.nb(i).forEach(j => { if (c.key(j) === 'senbei') c.eat(i, j, 6); }); } },
  tentou:   { e: '🐞', n: 'てんとうむし', r: 'C', v: 1, p: 1, store: true, likes: ['clover'], d: 'となりの🍀 1つにつき +4。となりにいれば育つ（+2）',
              act(c, i, s) { let hit = false; c.nb(i).forEach(j => { if (c.key(j) === 'clover') { c.add(i, 4, j); hit = true; } }); if (hit) c.grow(s, 2); } },
  mikazuki: { e: '🌙', n: 'みかづき', r: 'C', v: 1, p: 1, store: true, likes: ['mikazuki', 'moon', 'rabbit'], d: '盤面に🌓か🌕がいると +4、育つ（+2）。盤面の🐰 1匹につき +1。となりの🌙と合体して🌓はんげつになる',
              act(c, i, s) {
                const j = c.nb(i).find(j => c.key(j) === 'mikazuki');
                if (j !== undefined) { const o = c.sym(j); c.merge(i, j); c.transform(i, 'hangetsu', j, (s.c || 0) + (o.c || 0)); return; }
                const mj = c.all().find(j => c.key(j) === 'moon' || c.key(j) === 'hangetsu'); if (mj !== undefined) { c.add(i, 4, mj); c.grow(s, 2); }
                c.all().forEach(j => { if (c.key(j) === 'rabbit') c.add(i, 1, j); });
              } },
  hangetsu: { e: '🌓', n: 'はんげつ', r: 'S', v: 2, p: 1, store: true, likes: ['hangetsu', 'rabbit', 'dango', 'chadango'], d: '盤面の🐰🍡🥮すべての稼ぎが +2。となりの🌓と合体して🌕まんげつになる',
              act(c, i, s) {
                const j = c.nb(i).find(j => c.key(j) === 'hangetsu');
                if (j !== undefined) { c.merge(i, j); c.transform(i, 'moon', j); return; }
                c.all().forEach(j => { const k = c.key(j); if (k === 'rabbit' || k === 'dango' || k === 'chadango') c.add(j, 2, i); });
              } },
  tsubo:    { e: '🏺', n: 'つぼ', r: 'U', v: 0, p: 5, store: true, hint: '食べる・消える系と', d: '盤面で食べられたり消えたりしたシンボルの稼ぎ（育った分も）を吸い込んで育つ（1つにつき さらに +3）',
              act(c, i, s) { const n = c.goneCount(); if (n) c.grow(s, 3 * n + c.goneWorth()); } },
  fukurou:  { e: '🦉', n: 'ふくろう', r: 'U', v: 1, p: 1, hint: '支払い前に強い', d: '支払い前の最後の1回だけ +20',
              act(c, i) { if (c.spinsLeft <= 1) c.add(i, 20, '夜ふかし'); } },
  koryu:    { e: '🐲', n: 'こりゅう', r: 'U', v: 3, p: 2, likes: ['dragon'], d: '3コイン。盤面に🐉がいると稼ぎ ×3',
              act(c, i) { if (c.all().some(j => c.key(j) === 'dragon')) c.mul(i, 3, i); } },
  yabusame: { e: '🏹', n: 'やぶさめ', r: 'U', v: 1, p: 1, hint: '横の列に効く', d: '同じ横の列にいる動物 1匹につき +3',
              act(c, i) { c.all().forEach(j => { if (j !== i && c.row(j) === c.row(i) && ANIMALS.has(c.key(j))) c.add(i, 3, j); }); } },
  kujaku:   { e: '🦚', n: 'くじゃく', r: 'R', v: 0, p: 1, hint: 'レアが多いほど強い', d: '盤面のシンボルのレア度を合計して +（コモン1・アンコモン2・レア3・ベリーレア5）',
              act(c, i) { const w = { C: 1, U: 2, R: 3, V: 5, S: 2 }; let n = 0; c.all().forEach(j => { if (j !== i) n += w[SYM[c.key(j)].r]; }); c.add(i, n, 'レア度の合計'); } },
  hanamaru: { e: '💮', n: 'はなまる', r: 'R', v: 2, p: 1, hint: 'となりをバラバラに', d: 'となりに3つ以上いて、全部ちがう種類なら +20',
              act(c, i) { const t = c.nb(i).map(j => c.key(j)); if (t.length >= 3 && new Set(t).size === t.length) c.add(i, 20, 'はなまる！'); } },
  kazan:    { e: '🌋', n: 'かざん', r: 'V', v: 0, p: 1, store: true, hint: 'ためて爆発', d: '盤面に出るたび育つ（+4）。でも10%で噴火して育った分が0にもどり、となり全部の稼ぎ ×3',
              act(c, i, s) { if (rnd() < 0.1) { s.c = 0; c.nb(i).forEach(j => c.mul(j, 3, i)); c.flag('kazan'); } else s.c = (s.c || 0) + 4; } },
  whale:    { e: '🐋', n: 'くじら', r: 'V', v: 2, p: 4, store: true, likes: ['goldfish'], d: 'となりの🐟を全部のみこむ。1匹につき +15、育つ（+4、食べるたびに育つ量が+1ずつ増える。10%で今の育ちが ×2）',
              act(c, i, s) { c.nb(i).forEach(j => { if (c.key(j) === 'goldfish') { c.eat(i, j, 15); c.eatGrow(s, 4); } }); } },
  tengu:    { e: '👺', n: 'てんぐ', r: 'V', v: 2, p: 2, likes: ['*'], d: 'となりのシンボル全部の稼ぎを ×3',
              act(c, i) { c.nb(i).forEach(j => c.mul(j, 3, i)); } },
  japan:    { e: '🗾', n: 'にほんれっとう', r: 'V', v: 2, p: 1, likes: JAPANL, d: '盤面の 🗻⛩️🏯🌸🎌 の種類 1つにつき +12（そろえるほど強い）',
              act(c, i) { const n = new Set(c.all().map(j => c.key(j)).filter(k => JAPAN.has(k))).size; c.add(i, n * 12, '名所の数'); if (n >= 5) c.flag('japan5'); } },
  // ===== 追加（Ver.1.2） =====
  yatai:    { e: '🛖', n: 'やたい', r: 'U', v: 1, p: 2, likes: FOODL, d: 'となりの食べ物すべての稼ぎを ×2',
              act(c, i) { const m = c.has('noren') ? 3 : 2; c.nb(i).forEach(j => { if (FOOD.has(c.key(j))) c.mul(j, m, i); }); } },
  kingyosukui: { e: '🥅', n: '金魚すくい', r: 'U', v: 1, p: 1, likes: ['goldfish'], d: 'となりの🐟 1匹につき +1。となりに🐟がいると、🐟を1匹すくって手持ちに追加',
              act(c, i) { const f = c.nb(i).filter(j => c.key(j) === 'goldfish'); f.forEach(j => c.add(i, 1, j)); if (f.length) c.spawn('goldfish', i); } },
  bonodori: { e: '💃', n: 'ぼんおどり', r: 'R', v: 2, p: 1, likes: ['*'], hint: '同じものを集める', d: '盤面でいちばん多いシンボル全部に、その数だけ +（5つなら それぞれ +5）',
              act(c, i) { const m = {}; c.all().forEach(j => { const k = c.key(j); if (k !== 'bonodori') m[k] = (m[k] || 0) + 1; }); let top = null; for (const k in m) if (!top || m[k] > m[top]) top = k; if (top && m[top] >= 2) c.all().forEach(j => { if (c.key(j) === top) c.add(j, m[top] * (c.has('bachi') ? 2 : 1), i); }); } },
  kyuri:    { e: '🥒', n: 'きゅうり', r: 'C', v: 1, likes: ['kappa'], d: 'ただの1コイン。かっぱの大好物。' },
  kappa:    { e: '🧌', n: 'かっぱ', r: 'U', v: 1, p: 4, store: true, likes: ['kyuri'], d: 'となりの🥒を食べる。1本につき +6、育つ（+2、食べるたびに育つ量が+1ずつ増える。10%で今の育ちが ×2）',
              act(c, i, s) { c.nb(i).forEach(j => { if (c.key(j) === 'kyuri') { c.eat(i, j, 6); c.eatGrow(s, 2); } }); } },
  susuki:   { e: '🌿', n: 'すすき', r: 'C', v: 1, p: 1, store: true, likes: ['mikazuki', 'hangetsu', 'moon', 'sun'], d: '盤面に🌕がいると育つ（+1）。植物',
              act(c, i, s) { if (c.all().some(j => c.key(j) === 'moon')) c.grow(s, 1); } },
  daruma:   { e: '🪆', n: 'だるま', r: 'U', v: 1, p: 1, store: true, likes: ENGIL, d: '盤面のほかの縁起物（🎍🧧🎎🎊🔨🦁）1つにつき育つ（+2）。育つとき 10%で今の育ちが ×2',
              act(c, i, s) { const n = c.all().filter(j => j !== i && ENGI.has(c.key(j))).length; if (n) { c.grow(s, 2 * n); if (rnd() < 0.1) s.c = (s.c || 0) * 2; } } },
  tamaya:   { e: '🪭', n: 'たまや', r: 'U', v: 1, p: 1, store: true, likes: ['firework', 'kagiya'], d: '盤面の🎆🎐 1つにつき育つ（+3）。「たまや〜」のかけ声',
              act(c, i, s) { const n = c.all().filter(j => c.key(j) === 'firework' || c.key(j) === 'kagiya').length; if (n) c.grow(s, 3 * n); } },
  kagiya:   { e: '🎐', n: 'かぎや', r: 'U', v: 1, p: 2, likes: ['tamaya', 'firework'], d: 'となりの🪭🎆の稼ぎを ×5。たまやからは花火として数えられる。「かぎや〜」のかけ声',
              act(c, i) { c.nb(i).forEach(j => { const k = c.key(j); if (k === 'tamaya' || k === 'firework') c.mul(j, 5, i); }); } },
  mikan:    { e: '🍊', n: 'みかん', r: 'C', v: 1, likes: ['kotatsu'], d: 'ただの1コイン。こたつで食べたい。' },
  kotatsu:  { e: '🛋', n: 'こたつ', r: 'U', v: 1, p: 1, store: true, likes: ['mikan', 'cat'], d: 'となりの🍊と🐱 1つにつき育つ（+2）',
              act(c, i, s) { c.nb(i).forEach(j => { const k = c.key(j); if (k === 'mikan' || k === 'cat') c.grow(s, 2); }); } },
  shishi:   { e: '🦁', n: 'ししまい', r: 'R', v: 2, p: 2, likes: ENGIL, d: 'となりの縁起物（🎍🧧🎎🎊🔨🪆）の稼ぎを ×3',
              act(c, i) { c.nb(i).forEach(j => { if (ENGI.has(c.key(j))) c.mul(j, 3, i); }); } },
  inari:    { e: '🥟', n: 'いなりずし', r: 'C', v: 2, likes: ['fox'], d: '2コイン。🦊の大好物。' },
  kitsunebi:{ e: '🔥', n: 'きつねび', r: 'U', v: 1, p: 2, likes: ['fox'], d: 'となりの🦊の稼ぎを ×3',
              act(c, i) { c.nb(i).forEach(j => { if (c.key(j) === 'fox') c.mul(j, 3, i); }); } },
  karakasa: { e: '☂', n: 'からかさおばけ', r: 'U', v: 1, p: 1, store: true, likes: YOKAIL, d: '盤面のようかい（👻👹👺🦝🦊🧌🔥）1つにつき育つ（+2）',
              act(c, i, s) { const n = c.all().filter(j => j !== i && YOKAI.has(c.key(j))).length; if (n) c.grow(s, 2 * n); } },
};
const ANIMALS = new Set(['cat', 'fox', 'frog', 'rabbit', 'mouse', 'chicken', 'dog', 'bear', 'tanuki', 'turtle', 'crab', 'snake', 'sparrow', 'eagle', 'butterfly', 'shika', 'tentou', 'fukurou', 'kappa']);
const GROW = { seed: 'sakura', chick: 'chicken' };

// 2つのシンボルの相性（どちらかが相手を likes に持つ）
function partners(k) {
  const out = new Set();
  const d = SYM[k];
  if (d.likes && !d.likes.includes('*')) d.likes.forEach(x => out.add(x));
  Object.keys(SYM).forEach(o => { const l = SYM[o].likes; if (l && l.includes(k)) out.add(o); });
  out.delete(k === 'frog' ? '' : k);
  return [...out];
}

// ===== アイテム（お守り）=====
// board: 盤面の加算・倍率（シンボルの加算のあと、倍率の前に処理） / flat: 盤面とは別のボーナス / mult: 稼ぎ全体への倍率
const forKeys = (c, set, fn) => c.all().forEach(j => { if (set.has(c.key(j))) fn(j); });
const ITEMS = {
  kinchaku: { e: '💰', n: 'きんちゃく', r: 'C', d: 'まわすたびに +3コイン', flat: () => 3 },
  bell:     { e: '🔔', n: 'すず', r: 'C', d: '盤面の空きマス 1つにつき +1コイン', flat: (st, R) => R.empties },
  hashi:    { e: '🥢', n: 'おはし', r: 'C', d: '食べ物（🍡🍵🍙🍢🍠🍧🦑🍜🍯）の稼ぎがすべて +1', board: c => forKeys(c, FOOD, j => c.add(j, 1, '🥢おはし')) },
  paw:      { e: '🐾', n: 'にくきゅう', r: 'C', d: '動物（🐱🦊🐸🐰🐭🐔🐶🐻🦝🐢🦀🐍🐦🦅🦋）の稼ぎがすべて +1', board: c => forKeys(c, ANIMALS, j => c.add(j, 1, '🐾にくきゅう')) },
  rod:      { e: '🎣', n: 'つりざお', r: 'C', d: '🐟の稼ぎが +3', board: c => forKeys(c, new Set(['goldfish']), j => c.add(j, 3, '🎣つりざお')) },
  teapot:   { e: '🫖', n: 'きゅうす', r: 'C', d: '🍵の稼ぎが +3', board: c => forKeys(c, new Set(['tea']), j => c.add(j, 3, '🫖きゅうす')) },
  basket:   { e: '🧺', n: 'たまごかご', r: 'C', d: '🥚🐣🐔の稼ぎが +2', board: c => forKeys(c, new Set(['egg', 'chick', 'chicken']), j => c.add(j, 2, '🧺かご')) },
  magnet:   { e: '🧲', n: 'じしゃく', r: 'C', d: '🪙の稼ぎが +2', board: c => forKeys(c, new Set(['coin']), j => c.add(j, 2, '🧲じしゃく')) },
  broom:    { e: '🧹', n: 'ほうき', r: 'C', d: 'もらったとき ✂️除去+1。除去するたびに +8コイン' },
  yoyo:     { e: '🪀', n: 'ヨーヨー', r: 'C', d: '家賃を払うたびに 🔄引き直し がさらに +1' },
  scroll:   { e: '📜', n: 'まきもの', r: 'C', d: '家賃を払うたびに ✂️除去 がさらに +1' },
  kite:     { e: '🪁', n: 'たこあげ', r: 'C', d: 'いちばん上の段にいるシンボルの稼ぎが +1', board: c => c.all().forEach(j => { if (c.row(j) === 0) c.add(j, 1, '🪁たこあげ'); }) },
  tsukimi:  { e: '🎑', n: 'おつきみ', r: 'C', d: '🐰🍡🥮の稼ぎが +2', board: c => forKeys(c, new Set(['rabbit', 'dango', 'chadango']), j => c.add(j, 2, '🎑おつきみ')) },
  box:      { e: '📦', n: 'だんボール', r: 'C', d: '手持ちが20個より少ないと、1個たりないごとに +1コイン', flat: st => Math.max(0, 20 - st.inv.length) },

  candle:   { e: '🕯️', n: 'ろうそく', r: 'U', d: '🏮ちょうちんの倍率が ×2 → ×3 になる' },
  hourglass:{ e: '⏳', n: 'すなどけい', r: 'U', d: '次の期間から、支払いまでにまわせる回数 +1' },
  key:      { e: '🗝️', n: 'あいかぎ', r: 'U', d: '次の期間から、家賃が 10%やすくなる' },
  omamori:  { e: '📿', n: 'おまもり', r: 'U', d: 'レア以上のシンボルが出やすくなる' },
  bento:    { e: '🍱', n: 'べんとう', r: 'U', d: '盤面に食べ物が5つ以上あると +15コイン', flat: (st, R) => R.foods >= 5 ? 15 : 0 },
  sparkler: { e: '🎇', n: 'せんこうはなび', r: 'U', d: '消えた・食べられたシンボル 1つにつき +4コイン', flat: (st, R) => R.gone * 4 },
  mayoke:   { e: '🧿', n: 'まよけ', r: 'U', d: 'シンボルが何かを食べるたびに、さらに +3コイン', flat: (st, R) => R.eats * 3 },
  pot:      { e: '🪴', n: 'うえきばち', r: 'U', d: '植物（🌾🌸🎋🎍）の稼ぎが +2。🌱は2倍速で育つ', board: c => forKeys(c, PLANTS, j => { if (c.key(j) !== 'seed') c.add(j, 2, '🪴うえきばち'); }) },
  onsen:    { e: '♨️', n: 'おんせん', r: 'U', d: '家賃を払ったあと、残ったコインの10%がもらえる' },
  yukata:   { e: '👘', n: 'ゆかた', r: 'U', d: '盤面に10種類以上いると、その回の稼ぎ ×1.25', mult: (st, R) => R.kinds >= 10 ? 1.25 : 1 },
  teddy:    { e: '🧸', n: 'ぬいぐるみ', r: 'U', d: '手持ちに5個以上ある種類 1つにつき +4コイン', flat: st => { const m = {}; st.inv.forEach(s => m[s.key] = (m[s.key] || 0) + 1); return Object.values(m).filter(n => n >= 5).length * 4; } },
  bucket:   { e: '🪣', n: 'バケツ', r: 'U', d: '海の生き物（🐟🦑🦀🐢🐙🐡🐋）の稼ぎがすべて +2', board: c => forKeys(c, SEA, j => c.add(j, 2, '🪣バケツ')) },
  slot:     { e: '🎰', n: 'だいあたり台', r: 'U', d: '7回まわすごとに、その回の稼ぎ ×2', mult: st => (st.totalSpins + 1) % 7 === 0 ? 2 : 1 },

  tsuzura:  { e: '🧳', n: 'つづら', r: 'C', d: '盤面に出なかった手持ち 1個につき +1コイン（手持ちが多いほど得）', flat: (st, R) => R.offBoard },
  kawaraban:{ e: '🗞️', n: 'かわらばん', r: 'C', d: '次の期間から、大家の依頼の目標がかんたんになる' },
  hanakazari:{ e: '🏵️', n: 'はなかざり', r: 'C', d: '🌸と🦋の稼ぎが +3', board: c => forKeys(c, new Set(['sakura', 'butterfly']), j => c.add(j, 3, '🏵️はなかざり')) },
  hone:     { e: '🦴', n: 'ほね', r: 'C', d: '🐶🦊🐱の稼ぎが +2', board: c => forKeys(c, new Set(['dog', 'fox', 'cat']), j => c.add(j, 2, '🦴ほね')) },
  tebukuro: { e: '🧤', n: 'てぶくろ', r: 'C', d: 'もらったとき ✂️除去 +3' },
  horagai:  { e: '📯', n: 'ほらがい', r: 'U', d: '大家の依頼の報酬が 2倍になる' },
  telescope:{ e: '🔭', n: 'ぼうえんきょう', r: 'U', d: 'ベリーレアのシンボルが出やすくなる' },
  naruto:   { e: '🍥', n: 'なると', r: 'U', d: '盤面に3つ以上いる種類は、その種類すべての稼ぎ +2', board: c => { const m = {}; c.all().forEach(j => { const k = c.key(j); m[k] = (m[k] || 0) + 1; }); c.all().forEach(j => { if (m[c.key(j)] >= 3) c.add(j, 2, '🍥なると'); }); } },
  ofuda:    { e: '📃', n: 'おふだ', r: 'R', d: '次の期間から、大家の気まぐれが起きなくなる（デイリーのお題はのぞく）' },
  andon:    { e: '🪔', n: 'あんどん', r: 'R', d: '盤面の🏮 1つにつき、その回の稼ぎ ×1.25（最大×2）', mult: (st, R) => R.lanterns ? Math.min(2, Math.pow(1.25, R.lanterns)) : 1 },
  ticket:   { e: '🎟️', n: 'ふくびき券', r: 'R', d: 'シンボルの候補が 4つになる' },
  gem:      { e: '💎', n: 'ほうせき', r: 'R', d: 'ベリーレアのシンボルの稼ぎ ×2', board: c => c.all().forEach(j => { if (SYM[c.key(j)].r === 'V') c.mul(j, 2, '💎ほうせき'); }) },
  trophy:   { e: '🏆', n: 'トロフィー', r: 'R', d: '盤面だけで100コイン以上稼いだ回は さらに +40', flat: (st, R) => R.board >= 100 ? 40 : 0 },
  yobirin:  { e: '🛎️', n: 'よびりん', r: 'R', d: '支払い前の最後の1回の稼ぎ ×2', mult: st => st.spinsLeft === 1 ? 2 : 1 },
  hinode:   { e: '🌅', n: 'はつひので', r: 'R', d: '支払いのあと最初の1回の稼ぎ ×2', mult: st => st.spinsLeft === st.spinsMax ? 2 : 1, r2: true },
  crown:    { e: '👑', n: 'おうかん', r: 'R', d: 'レアとベリーレアのシンボルの稼ぎ +3', board: c => c.all().forEach(j => { const r = SYM[c.key(j)].r; if (r === 'R' || r === 'V') c.add(j, 3, '👑おうかん'); }) },
  compass:  { e: '🧭', n: 'らしんばん', r: 'R', d: 'まんなか6マスにいるシンボルの稼ぎ +2', board: c => c.all().forEach(j => { if (CENTER.has(j)) c.add(j, 2, '🧭らしんばん'); }) },
  wand:     { e: '🪄', n: 'まほうのつえ', r: 'R', d: 'まわすたびに、ランダムなシンボル1つの稼ぎ ×3', board: c => { const a = c.all(); if (a.length) c.mul(a[Math.floor(rnd() * a.length)], 3, '🪄つえ'); } },
  // ===== 追加（Ver.1.3） =====
  keito:    { e: '🧶', n: 'けいと', r: 'C', d: '🐱ねこと🛋こたつの稼ぎが +3', board: c => forKeys(c, new Set(['cat', 'kotatsu']), j => c.add(j, 3, '🧶けいと')) },
  hyotan:   { e: '🫙', n: 'ひょうたん', r: 'C', d: '🧌かっぱの稼ぎが +4', board: c => forKeys(c, new Set(['kappa']), j => c.add(j, 4, '🫙ひょうたん')) },
  aburaage: { e: '🧈', n: 'あぶらあげ', r: 'C', d: '🦊きつねと🥟いなりずしの稼ぎが +3', board: c => forKeys(c, new Set(['fox', 'inari']), j => c.add(j, 3, '🧈あぶらあげ')) },
  hachimaki:{ e: '🎽', n: 'はちまき', r: 'C', d: '縁起物（🎍🧧🎎🎊🔨🪆🦁）の稼ぎが +2', board: c => forKeys(c, ENGI, j => c.add(j, 2, '🎽はちまき')) },
  nukadoko: { e: '🥗', n: 'ぬかどこ', r: 'C', d: '🥒きゅうりと🍊みかんの稼ぎが +3', board: c => forKeys(c, new Set(['kyuri', 'mikan']), j => c.add(j, 3, '🥗ぬかどこ')) },
  chawan:   { e: '🍚', n: 'ちゃわん', r: 'C', d: '🍙おにぎりと🥟いなりずしと🌾いなほの稼ぎが +2', board: c => forKeys(c, new Set(['onigiri', 'inari', 'rice']), j => c.add(j, 2, '🍚ちゃわん')) },

  noren:    { e: '🚪', n: 'のれん', r: 'U', d: '🛖やたいの倍率が ×2 → ×3 になる' },
  kingyobachi:{ e: '🫧', n: 'きんぎょばち', r: 'U', d: '🐟金魚の稼ぎが ×2', board: c => forKeys(c, new Set(['goldfish']), j => c.mul(j, 2, '🫧きんぎょばち')) },
  bachi:    { e: '🔱', n: 'たいこのばち', r: 'U', d: '💃ぼんおどりで増える稼ぎが 2倍になる' },
  emaki:    { e: '🌃', n: 'ひゃっきやこう絵巻', r: 'U', d: 'ようかい（👻👹👺🦝🦊🧌🔥☂）の稼ぎが +3', board: c => forKeys(c, YOKAI, j => c.add(j, 3, '🌃絵巻')) },
  kintsugi: { e: '🥣', n: 'きんつぎ', r: 'U', d: '消えた・食べられたシンボル 1つにつき、手持ちの🏺つぼが育つ（+1）',
              flat: (st, R) => { if (R.gone) st.inv.forEach(x => { if (x.key === 'tsubo') x.c = (x.c || 0) + R.gone; }); return 0; } },
  fude:     { e: '🖌', n: 'ふで', r: 'U', d: '🪆だるまの稼ぎが ×2（目が入る）', board: c => forKeys(c, new Set(['daruma']), j => c.mul(j, 2, '🖌ふで')) },

  omikoshi: { e: '🛕', n: 'おみこし', r: 'R', d: '盤面でいちばん多い種類のシンボルの稼ぎが ×2',
              board: c => { const m = {}; c.all().forEach(j => { const k = c.key(j); m[k] = (m[k] || 0) + 1; }); let top = null; for (const k in m) if (!top || m[k] > m[top]) top = k; if (top && m[top] >= 2) c.all().forEach(j => { if (c.key(j) === top) c.mul(j, 2, '🛕おみこし'); }); } },
  tamatebako:{ e: '🧰', n: 'たまてばこ', r: 'R', d: '育つシンボルの稼ぎが ×2', board: c => c.all().forEach(j => { if (SYM[c.key(j)].store) c.mul(j, 2, '🎁たまてばこ'); }) },
  enmusubi: { e: '🎀', n: 'えんむすび', r: 'R', d: 'コンボで育つとき、さらに +1 育つ（ひとりで育つかたつむり・かざん・やきいもには効かない）' },
  kumade:   { e: '🪮', n: 'くまで', r: 'R', d: '盤面の縁起物 1つにつき、その回の稼ぎ ×1.15（最大 ×2）', mult: (st, R) => R.engi ? Math.min(2, Math.pow(1.15, R.engi)) : 1 },
};
const ITEM_RARITY = { C: { name: 'ふつう', color: '#c9d1dc' }, U: { name: 'いいもの', color: '#5fd99b' }, R: { name: 'お宝', color: '#ffb547' } };

// ===== 大家の気まぐれ（呪い）=====
const CURSES = {
  raise:   { e: '📈', n: 'ねあげ', d: 'この期間の家賃が 20%高い' },
  hurry:   { e: '⏱️', n: 'せっかち', d: '支払いまでにまわせる回数が 1回少ない' },
  soldout: { e: '🚫', n: 'しなぎれ', d: 'シンボルの候補が 1つ少ない' },
  rats:    { e: '🐀', n: 'ねずみさわぎ', d: 'まわすたびに 🐭が1匹 手持ちに入ってくる' },
  fog:     { e: '🌫️', n: 'きり', d: '盤面の4すみが使えない' },
  tax:     { e: '💸', n: 'ぜいきん', d: 'まわすたびに 稼ぎの15%を取られる' },
  cold:    { e: '🥶', n: 'さむぞら', d: '食べ物の稼ぎが それぞれ -1' },
  seal:    { e: '🔒', n: 'ふういん', d: '🔄引き直しが使えない' },
};

// ===== 難易度 =====
const DIFFS = {
  easy:   { n: 'EASY', jp: 'かんたん', color: '#5fd99b', rentMul: 0.8, ramp: 0, rents: 12, rerolls: 2, removals: 2, extra: ['coin', 'rice', 'mouse'], startItem: true, curseFrom: 99, curseChance: 0, luck: 0.03,
            desc: ['家賃が安い', '最初からアイテム1つ', '🔄2 ✂️2・シンボル多めでスタート'] },
  normal: { n: 'NORMAL', jp: 'ふつう', color: '#5aa9ff', rentMul: 1.1, ramp: 0.1, rents: 12, rerolls: 1, removals: 1, extra: [], startItem: true, curseFrom: 99, curseChance: 0, luck: 0,
            desc: ['おすすめのバランス', '最初からアイテム1つ', '家賃12回でクリア'] },
  hard:   { n: 'HARD', jp: 'むずかしい', color: '#ffb547', rentMul: 1.35, ramp: 0.17, rents: 12, rerolls: 0, removals: 1, extra: [], startItem: false, curseFrom: 2, curseChance: 0.5, luck: 0,
            desc: ['家賃が高く、後半ほど急に上がる', '初期アイテム・🔄なし', '3回目から ときどき大家の気まぐれ'] },
  super:  { n: 'SUPER HARD', jp: 'ちょうむずかしい', color: '#ff5d8f', rentMul: 1.55, ramp: 0.16, rents: 14, rerolls: 0, removals: 0, extra: [], startItem: false, curseFrom: 1, curseChance: 1, luck: -0.01,
            desc: ['家賃が高い上に全14回', '2回目から毎回 大家の気まぐれ', '🔄✂️なし・レアが出にくい'] },
  // ストーリークリアで解放。終わりなし。5回ごとに「段」が上がって、家賃と気まぐれがきつくなる
  endless: { n: 'エンドレス(?)', jp: 'どこまで住める？', color: '#f2c14e', rentMul: 1.25, ramp: 0, rents: Infinity, rerolls: 1, removals: 1, extra: [], startItem: true, curseFrom: 5, curseChance: 0, luck: 0, endless: true, growth: 1.2,
            desc: ['家賃を払いつづける', '5回ごとに段が上がる', '第2段から気まぐれ'] },
  // デイリー：お題（ずっと続く気まぐれ）・荷物・最初のおまけは全員同じ。そのあとは1回ごとにランダム。払えるかぎり続く
  daily: { n: 'デイリー', jp: '今日のお題', color: '#5ab0e8', rentMul: 1.15, ramp: 0, rents: Infinity, rerolls: 1, removals: 1, extra: [], startItem: true, curseFrom: 99, curseChance: 0, luck: 0, growth: 1.2,
            desc: ['お題は全員同じ', '家賃を払えるかぎり続く', '何回払えたかで競う'] },
};
const STAGE_LEN = 5;
const endlessStage = idx => Math.floor(idx / STAGE_LEN) + 1;
// 段ごとの気まぐれの出やすさ
const stageCurseChance = stage => stage <= 1 ? 0 : Math.min(1, 0.3 * (stage - 1));

// 家賃の基本スケジュール（難易度の倍率をかける）
const BASE_RENTS = [
  { rent: 25, spins: 5 }, { rent: 50, spins: 5 }, { rent: 100, spins: 6 },
  { rent: 170, spins: 6 }, { rent: 260, spins: 7 }, { rent: 360, spins: 7 },
  { rent: 500, spins: 8 }, { rent: 666, spins: 8 }, { rent: 850, spins: 9 },
  { rent: 1100, spins: 9 }, { rent: 1400, spins: 10 }, { rent: 1750, spins: 10 },
  { rent: 2150, spins: 10 }, { rent: 2700, spins: 11 },
];
const RENT_ACCEL = 0.004;
function baseRent(idx, growth) {
  if (idx < BASE_RENTS.length) return BASE_RENTS[idx];
  const last = BASE_RENTS[BASE_RENTS.length - 1];
  const m = idx - BASE_RENTS.length + 1;
  // 長く続くほど、上がり方そのものが少しずつ大きくなる（1回ごとの倍率が ×10^(0.004m) ずつ上乗せ）
  return { rent: Math.round(last.rent * Math.pow(growth || 1.3, m) * Math.pow(10, RENT_ACCEL * m * m / 2)), spins: 11 };
}
const round5 = x => Math.max(5, Math.round(x / 5) * 5);
const MAXC = Number.MAX_VALUE;                                  // 表示できる最大（カンスト）
const capN = x => (x > 0 ? Math.min(x, MAXC) : 0);              // 0〜最大におさめる（NaN は 0）
const pickOne = a => a[Math.floor(rnd() * a.length)];
const hasItem = (st, k) => st.items.includes(k);

// ===== 大家の依頼 =====
const QUESTS = {
  big:     { make: st => { const t = round5(st.rent / st.spinsMax * 1.6); return { target: t, txt: `1回で ${t}コイン以上かせぐ` }; } },
  eat:     { make: st => { const t = 3 + Math.floor(st.rentIdx / 2); return { target: t, txt: `シンボルに合計${t}回 食べさせる🍴` }; } },
  variety: { make: () => ({ target: 10, txt: '盤面に10種類以上を いっぺんに出す' }) },
  same:    { make: () => ({ target: 4, txt: '盤面に同じシンボルを4つ以上 いっぺんに出す' }) },
  earn:    { make: st => { const t = round5(st.rent * 1.3); return { target: t, txt: `この期間で合計${t}コイン かせぐ` }; } },
  lean:    { make: () => ({ target: 15, txt: '手持ち15個以下で 支払い日をむかえる' }) },
};
function makeQuest(st) {
  const type = pickOne(Object.keys(QUESTS).filter(t => !(t === 'eat' && st.rentIdx < 2)));
  const q = QUESTS[type].make(st);
  const oldT = q.target;
  if (hasItem(st, 'kawaraban') && type !== 'lean') q.target = Math.max(1, Math.round(q.target * (type === 'variety' || type === 'same' ? 0.85 : 0.7)));
  if (hasItem(st, 'kawaraban') && type === 'lean') q.target += 3;
  if (hasItem(st, 'kawaraban')) q.txt = q.txt.replace(String(oldT), String(q.target));
  const rewards = [
    { t: 'coins', n: round5(st.rent * 0.3) }, { t: 'reroll', n: 2 }, { t: 'removal', n: 2 }, { t: 'item', n: 1 },
  ];
  const rw = pickOne(rewards);
  rw.txt = rw.t === 'coins' ? `🪙+${rw.n}` : rw.t === 'reroll' ? '🔄+2' : rw.t === 'removal' ? '✂️+2' : '🎁アイテム+1';
  return { type, target: q.target, txt: q.txt, progress: 0, done: false, reward: rw };
}
function completeQuest(st) {
  const q = st.quest; if (!q || q.done) return false;
  q.done = true; st.stats.quests++;
  const r = q.reward, x = hasItem(st, 'horagai') ? 2 : 1;
  if (r.t === 'coins') st.coins += r.n * x;
  else if (r.t === 'reroll') st.rerolls += r.n * x;
  else if (r.t === 'removal') st.removals += r.n * x;
  else st.itemPicks += x;
  return true;
}

let UID = 1;
function mk(key) { return { key, id: UID++, c: 0 }; }

function startPeriod(st) {
  const D = DIFFS[st.diff], b = baseRent(st.rentIdx, D.growth);
  const chance = D.endless ? stageCurseChance(endlessStage(st.rentIdx)) : D.curseChance;
  st.curse = st.fixedCurse || ((st.rentIdx >= D.curseFrom && rnd() < chance && !hasItem(st, 'ofuda')) ? pickOne(Object.keys(CURSES)) : null);
  let rent = b.rent * D.rentMul * (1 + (D.ramp || 0) * Math.min(st.rentIdx, 13));
  if (st.curse === 'raise') rent *= 1.2;
  if (hasItem(st, 'key')) rent *= 0.9;
  st.rent = Math.min(round5(rent), MAXC);
  st.spinsMax = Math.max(2, b.spins + (hasItem(st, 'hourglass') ? 1 : 0) - (st.curse === 'hurry' ? 1 : 0));
  st.spinsLeft = st.spinsMax;
  st.periodEarned = 0;
  st.quest = st.rentIdx >= 1 ? makeQuest(st) : null;
}
function totalRents(st) { return DIFFS[st.diff].rents; }
const isEndlessMode = st => !!DIFFS[st.diff].endless;
// エンドレスで払った回数（ストーリーのあとに続けた分もふくむ）
const endlessCount = st => isEndlessMode(st) ? st.rentIdx : st.endless ? st.rentIdx - totalRents(st) : 0;

// ===== はじめの荷物 =====
const STARTERS = {
  basic:  { e: '🎒', n: 'ふつうの荷物', inv: ['coin', 'coin', 'dango', 'tea', 'goldfish'], d: 'バランスのいい基本セット' },
  kingyo: { e: '🐟', n: '金魚すくいセット', inv: ['goldfish', 'goldfish', 'goldfish', 'cat', 'coin'], item: 'rod', d: '🐟×3と🐱。🎣つりざお付き', unlock: { story: 1 } },
  dangoya:{ e: '🍡', n: 'だんご屋セット', inv: ['dango', 'dango', 'tea', 'tea', 'rabbit'], item: 'tsukimi', d: '🍡🍵のコンボ。🎑おつきみ付き', unlock: { story: 1 } },
  inari:  { e: '🦊', n: 'おいなりセット', inv: ['fox', 'mouse', 'mouse', 'rice', 'rice', 'onigiri'], d: '🦊の食物連鎖からスタート', unlock: { story: 2 } },
  yomise: { e: '🏮', n: 'よみせセット', inv: ['lantern', 'coin', 'coin', 'coin'], d: '🏮と🪙。倍率の基本', unlock: { ach: 's150' } },
  niwashi:{ e: '🌱', n: 'にわしセット', inv: ['seed', 'seed', 'seed', 'butterfly', 'rice'], item: 'pot', d: '育てて稼ぐ。🪴うえきばち付き', unlock: { ach: 'dex40' } },
  bakuchi:{ e: '🎲', n: 'ばくち打ちセット', inv: ['dice', 'dice', 'pochi', 'pochi', 'kaminari'], d: '運まかせの一発勝負', unlock: { ach: 'pochi' } },
  shinobi:{ e: '🥷', n: 'しのびセット', inv: ['coin', 'octopus', 'ninja'], item: 'box', d: '少数精鋭。📦だんボール付き', unlock: { ach: 'mini' } },
  oninoko:{ e: '👹', n: 'おにの子セット', inv: ['oni', 'rice', 'rice', 'rice', 'rice', 'coin'], d: 'いきなり👹。エサをあげて稼ぐ', unlock: { story: 3 } },
};

function newGame(diff, opt) {
  opt = opt || {};
  diff = DIFFS[diff] ? diff : 'normal';
  const D = DIFFS[diff], S = STARTERS[opt.starter] || STARTERS.basic;
  const st = {
    diff, starter: STARTERS[opt.starter] ? opt.starter : 'basic', story: opt.story || null, daily: opt.daily || null,
    inv: [...S.inv, ...D.extra].map(mk), items: [],
    coins: 0, rentIdx: 0, rerolls: D.rerolls, removals: D.removals, totalSpins: 0, totalEarned: 0, best: 0,
    board: null, last: null, choices: null, itemChoices: null, itemPicks: 0, endless: !!D.endless, event: null, fixedCurse: opt.fixedCurse || null,
    stats: { eats: 0, gone: 0, quests: 0, curses: 0, removed: 0, maxInv: 0, events: 0, flags: [] },
    phase: 'spin',
  };
  if (S.item) addItem(st, S.item);
  if (opt.item) addItem(st, opt.item);
  startPeriod(st);
  if (D.startItem) { st.itemPicks = 1; rollItems(st); st.phase = 'item'; }
  return st;
}

// ===== 横丁のできごと =====
const cost = (st, r) => round5(st.rent * r);
const symOfRarity = r => Object.keys(SYM).filter(k => SYM[k].r === r);
const EVENTS = {
  peddler:   { e: '🎪', n: '藁人の夜店', who: 'gyosho', txt: '藁をかぶった藁人が、灯籠のとなりに見慣れない品を並べている。「珍しいのが入りました。安くはありませんよ」', opts: [
    { l: st => `コイン${cost(st, .25)}で レアのシンボルを買う`, can: st => st.coins >= cost(st, .25), run: st => { st.coins -= cost(st, .25); const k = pickOne(symOfRarity('R')); st.inv.push(mk(k)); return { msg: `${SYM[k].e} ${SYM[k].n} を手に入れた`, got: [k] }; } },
    { l: () => 'ひやかして帰る（🔄+1）', run: st => { st.rerolls++; return { msg: '🔄+1' }; } }] },
  omikuji:   { e: '⛩️', n: '夜のおみくじ', txt: '神社の裏に、だれも番をしていないおみくじ箱。料金箱には「お気持ちで」と書いてある。', opts: [
    { l: st => `引く（コイン${cost(st, .1)}）`, can: st => st.coins >= cost(st, .1), run: st => {
      st.coins -= cost(st, .1); const x = rnd();
      if (x < .2) { st.itemPicks++; return { msg: '🎉 大吉！ アイテムをもう1つもらえる' }; }
      if (x < .6) { const n = cost(st, .3); st.coins += n; return { msg: `吉！ 🪙+${n}` }; }
      if (x < .85) { st.rerolls++; return { msg: '小吉。🔄+1' }; }
      if (!st.inv.length) return { msg: '凶……でも何も起きなかった' };
      const v = st.inv.splice(Math.floor(rnd() * st.inv.length), 1)[0]; return { msg: `凶…… 手持ちの${SYM[v.key].e}がどこかへ消えた` }; } },
    { l: () => '手を合わせるだけ', run: () => ({ msg: '手を合わせた。それだけ。' }) }] },
  sakamori:  { e: '🍶', n: '長屋の酒盛り', who: 'gonzo', txt: '長屋の前で、ゴンゾウたちが樽をかこんでいる。「おう。一杯つきあえ」', opts: [
    { l: () => '一杯だけつきあう（🍶×2 が手持ちに）', run: st => { st.inv.push(mk('sake'), mk('sake')); return { msg: '🍶×2 を手に入れた', got: ['sake'] }; } },
    { l: () => '断って寝る（✂️+1）', run: st => { st.removals++; return { msg: '✂️+1' }; } }] },
  ponta:     { e: '🦝', n: 'ポン太のいたずら', who: 'ponta', txt: 'ポン太が荷物の中をのぞきこんでいる。「ちょっと見てただけだって。ほんとほんと」', opts: [
    { l: () => '追い払う（✂️-1）', can: st => st.removals > 0, run: st => { st.removals--; return { msg: 'ポン太はしっぽを丸めて逃げていった。' }; } },
    { l: () => 'ほっとく（🦝が住みつく）', run: st => { st.inv.push(mk('tanuki')); return { msg: '🦝 が住みついた', got: ['tanuki'] }; } }] },
  kingyo:    { e: '🎣', n: '金魚すくい大会', txt: '金魚すくいの屋台で、店番の河童が網を差し出してくる。「一回どうだい」', opts: [
    { l: st => `参加する（コイン${cost(st, .1)}）`, can: st => st.coins >= cost(st, .1), run: st => { st.coins -= cost(st, .1); st.inv.push(mk('goldfish'), mk('goldfish'), mk('goldfish')); let m = '🐟×3 をすくった'; const got = ['goldfish']; if (rnd() < .5) { st.inv.push(mk('koi')); m += '。おまけに🎏も！'; got.push('koi'); } return { msg: m, got }; } },
    { l: () => '見物する', run: () => ({ msg: '河童がつまらなそうに網をしまった。' }) }] },
  osouji:    { e: '🧹', n: '長屋の大そうじ', who: 'okon', txt: 'おコンさんが、はたきを突き出してきた。「暇そうだね。手伝いな」', opts: [
    { l: () => '手伝う（✂️+2）', run: st => { st.removals += 2; return { msg: '✂️+2' }; } },
    { l: st => `サボる（コイン+${cost(st, .15)}）`, run: st => { const n = cost(st, .15); st.coins += n; return { msg: `🪙+${n}…… 背中に視線を感じる` }; } }] },
  otoshimono:{ e: '👛', n: '落とし物', txt: '道ばたに、がま口の財布が落ちている。持ち上げると、ずっしり重い。', opts: [
    { l: () => '届ける（アイテムをもう1つ）', run: st => { st.itemPicks++; return { msg: '持ち主の狸のおばあさんが、お礼に小さなお守りをくれた。' }; } },
    { l: st => `もらっておく（コイン+${cost(st, .35)}・🦝×2が手持ちに）`, run: st => { const n = cost(st, .35); st.coins += n; st.inv.push(mk('tanuki'), mk('tanuki')); return { msg: `🪙+${n}…… 中身の半分は葉っぱだった`, got: ['tanuki'] }; } }] },
  hanami:    { e: '🌸', n: 'おハナの夜桜', who: 'ohana', txt: 'おハナが枝をゆらしている。「たくさん咲いちゃったの。どっちか持ってって」', opts: [
    { l: () => '🌱たね×3 をもらう', run: st => { for (let k = 0; k < 3; k++) st.inv.push(mk('seed')); return { msg: '🌱×3 を手に入れた', got: ['seed'] }; } },
    { l: () => '🌸さくら×1 をもらう', run: st => { st.inv.push(mk('sakura')); return { msg: '🌸 を手に入れた', got: ['sakura'] }; } }] },
  gonzo:     { e: '💪', n: 'ゴンゾウの力くらべ', who: 'gonzo', txt: 'ゴンゾウが樽にひじをついた。「……勝ったら、なんかやる」', opts: [
    { l: st => `挑む（勝てばコイン+${cost(st, .5)}、負けたら-${cost(st, .2)}）`, run: st => { if (rnd() < .5) { const n = cost(st, .5); st.coins += n; return { msg: `勝った！ 🪙+${n}` }; } const n = Math.min(st.coins, cost(st, .2)); st.coins -= n; return { msg: `負けた…… 🪙-${n}` }; } },
    { l: () => 'やめておく', run: () => ({ msg: 'ゴンゾウは「そうか」とだけ言った。' }) }] },
  fukubukuro:{ e: '🛍️', n: '福袋の屋台', txt: '「中身はお楽しみ」と書かれた袋が積んである。お楽しみのわりに、値段が高い。', opts: [
    { l: st => `買う（コイン${cost(st, .15)}・シンボル3つ入り）`, can: st => st.coins >= cost(st, .15), run: st => { st.coins -= cost(st, .15); const got = []; const ks = Object.keys(SYM).filter(x => SYM[x].r !== 'S'); for (let k = 0; k < 3; k++) { const x = pickOne(ks); st.inv.push(mk(x)); got.push(x); } return { msg: `${got.map(x => SYM[x].e).join('')} が入っていた`, got }; } },
    { l: () => '買わない', run: () => ({ msg: '通りすぎた。袋の山が、少し低くなっていた。' }) }] },
  karakuri:  { e: '🔧', n: 'からくりの手入れ', who: 'maneki', txt: 'マネキが台の裏をのぞいている。「ネジがゆるんどる。わしに任せるか？」', opts: [
    { l: () => 'マネキに任せる（🔄+2）', run: st => { st.rerolls += 2; return { msg: '🔄+2' }; } },
    { l: () => '自分でいじる（半々で、おまけが1つ）', run: st => { if (rnd() < .5) { st.itemPicks++; return { msg: 'うまくいった！ アイテムをもう1つ' }; } return { msg: '……何も変わらなかった' }; } }] },
  chaya:     { e: '🍵', n: '茶屋で一服', txt: '茶屋の縁台。湯気の向こうで、店のおばあさんが手招きしている。', opts: [
    { l: () => 'ゆっくり休む（この期間 まわせる回数+1）', run: st => { st.spinsLeft++; st.spinsMax++; return { msg: 'まわせる回数 +1' }; } },
    { l: () => 'お茶だけもらう（🍵×2）', run: st => { st.inv.push(mk('tea'), mk('tea')); return { msg: '🍵×2 を手に入れた', got: ['tea'] }; } }] },
  ryujin:    { e: '🌌', n: '龍神さまの通り道', txt: '雲が、ゆっくりと長い形にほどけていく。うろこが一枚、足もとに落ちてきた。', opts: [
    { l: st => `お供えする（コイン${cost(st, .4)}）`, can: st => st.coins >= cost(st, .4), run: st => { st.coins -= cost(st, .4); const k = rnd() < .3 ? 'dragon' : 'koryu'; st.inv.push(mk(k)); return { msg: `龍の加護！ ${SYM[k].e} を手に入れた`, got: [k] }; } },
    { l: () => '見送る', run: () => ({ msg: '雲は山のほうへ流れていった。' }) }] },
  setsubun:  { e: '🫘', n: '豆まき', txt: '長屋の子どもたちが、豆の入ったますを抱えて走ってきた。「おに役、いないんだよね」', opts: [
    { l: () => '豆をもらう（🫘×3）', run: st => { for (let k = 0; k < 3; k++) st.inv.push(mk('mame')); return { msg: '🫘×3 を手に入れた', got: ['mame'] }; } },
    { l: () => 'おに役をやる（👹が手持ちに）', run: st => { st.inv.push(mk('oni')); return { msg: '👹 が手持ちに入った', got: ['oni'] }; } }] },
};
function rollEvent(st, chance) { st.event = (st.rentIdx >= 1 && rnd() < chance) ? pickOne(Object.keys(EVENTS)) : null; return st.event; }
function runEvent(st, idx) {
  const ev = EVENTS[st.event]; if (!ev) return null;
  const o = ev.opts[idx]; if (!o || (o.can && !o.can(st))) return null;
  const r = o.run(st); st.event = null; st.stats.events++;
  return r;
}

// ===== デイリー用の乱数 =====
function seedFrom(str) { let h = 1779033703 ^ str.length; for (let i = 0; i < str.length; i++) { h = Math.imul(h ^ str.charCodeAt(i), 3432918353); h = h << 13 | h >>> 19; } return h >>> 0; }
function seededRng(st) {
  return () => { st.rng = (st.rng + 0x6D2B79F5) | 0; let t = st.rng; t = Math.imul(t ^ t >>> 15, t | 1); t ^= t + Math.imul(t ^ t >>> 7, t | 61); return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}
// 日付で決まるお題（気まぐれ・荷物・おまけ）。全員同じ
function dailySetup(dateStr) {
  const tmp = { rng: seedFrom('yachin-' + dateStr) };
  const keep = RNG_FN; setRng(seededRng(tmp));
  const curse = pickOne(Object.keys(CURSES).filter(k => k !== 'seal'));
  const starter = pickOne(Object.keys(STARTERS));
  const item = pickOne(Object.keys(ITEMS).filter(k => ITEMS[k].r !== 'R' && k !== 'ofuda'));
  setRng(keep);
  return { curse, starter, item, rng: tmp.rng };
}
// runSeed：1回ごとのタネ（ランキングではサーバーが配る）。最初のおまけの候補までは日付のタネで決めるので全員同じ
function newDaily(dateStr, runSeed) {
  const D0 = dailySetup(dateStr);
  const tmp = { rng: D0.rng };
  setRng(seededRng(tmp));
  const st = newGame('daily', { starter: D0.starter, daily: dateStr, fixedCurse: D0.curse, item: D0.item });
  st.runSeed = (runSeed === undefined ? 0 : runSeed) >>> 0;
  st.rng = (seedFrom('run-' + st.runSeed) ^ tmp.rng) | 0;
  st.log = [];
  setRng(seededRng(st));
  return st;
}

// ===== 操作の入口（画面もサーバーの検証も、ここを通す） =====
// 操作は短い文字列で記録する： s=まわす p:k=シンボルを取る（p:=取らない） r=引き直し i:k=おまけ（i:=取らない）
// e:n=できごとの選択 $=家賃を払う x:k=シンボルを除去
function afterItems(st) { st.itemChoices = null; st.phase = st.event ? 'event' : 'spin'; }
function prepItems(st) {
  if (st.itemPicks <= 0) { afterItems(st); return; }
  rollItems(st);
  if (!st.itemChoices.length) { st.itemPicks = 0; afterItems(st); }
}
function act(st, code) {
  const c = code[0], arg = code.length > 2 ? code.slice(2) : '';
  let r = null;
  if (c === 's') {
    if (st.phase !== 'spin') return null;
    r = spin(st); st.last.questDone = r.questDone; rollChoices(st); st.phase = 'choose';
  } else if (c === 'p') {
    if (st.phase !== 'choose' || (arg && !(st.choices || []).includes(arg))) return null;
    if (arg) st.inv.push(mk(arg));
    st.choices = null; st.phase = rentDue(st) ? 'rent' : 'spin'; r = { k: arg };
  } else if (c === 'r') {
    if (st.phase !== 'choose' || !canReroll(st)) return null;
    st.rerolls--; rollChoices(st); r = {};
  } else if (c === 'i') {
    if (st.phase !== 'item' || (arg && !(st.itemChoices || []).includes(arg))) return null;
    if (arg) addItem(st, arg);
    st.itemPicks = Math.max(0, st.itemPicks - 1); st.itemChoices = null;
    if (st.itemPicks > 0) { st.phase = 'item'; prepItems(st); } else afterItems(st);
    r = { k: arg };
  } else if (c === 'e') {
    if (st.phase !== 'event') return null;
    r = runEvent(st, +arg); if (!r) return null;
    if (st.itemPicks > 0) { st.phase = 'item'; prepItems(st); } else st.phase = 'spin';
  } else if (c === '$') {
    if (st.phase !== 'rent') return null;
    r = payRent(st);
    if (r.ok && st.phase !== 'clear' && st.phase !== 'kanst') { st.phase = 'item'; prepItems(st); }
  } else if (c === 'x') {
    if (!['spin', 'choose', 'item'].includes(st.phase) || !removeSymbol(st, arg)) return null;
    r = {};
  } else return null;
  if (st.log) st.log.push(code);
  return r;
}
// サーバーで少しずつ確かめるための、途中の状態の書き出しと読み込み（操作の記録は入れない）
function exportDaily(st) { const o = Object.assign({}, st); delete o.log; return JSON.stringify(o); }
function importDaily(json) {
  const st = JSON.parse(json); st.log = null;
  UID = Math.max(1, ...st.inv.map(x => x.id + 1), ...((st.board || []).filter(Boolean).map(x => (x.id || 0) + 1)));
  setRng(seededRng(st));
  return st;
}
// 状態に操作をまとめて当てる。全部通れば true
function stepDaily(st, codes) {
  for (const code of codes) { if (typeof code !== 'string' || code.length > 40 || !act(st, code)) return false; }
  return true;
}
// 記録を最初から再生して、最後の状態を返す（おかしな操作があれば null）
function replayDaily(dateStr, runSeed, log) {
  const keepUID = UID;
  const st = newDaily(dateStr, runSeed);
  for (const code of log) { if (typeof code !== 'string' || code.length > 40 || !act(st, code)) { setRng(null); UID = keepUID; return null; } }
  setRng(null); UID = keepUID;
  return st;
}

function neighbors(i) {
  const x = i % W, y = (i / W) | 0, out = [];
  for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
    if (!dx && !dy) continue;
    const nx = x + dx, ny = y + dy;
    if (nx >= 0 && nx < W && ny >= 0 && ny < H) out.push(ny * W + nx);
  }
  return out;
}
function shuffle(a) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }

// 1スピン実行
function spin(st) {
  const blocked = st.curse === 'fog' ? CORNERS : new Set();
  const open = [...Array(N).keys()].filter(i => !blocked.has(i));
  const pool = shuffle(st.inv.slice()).slice(0, open.length);
  const cells = new Array(N).fill(null);
  const slots = shuffle(open.slice());
  pool.forEach((s, k) => { cells[slots[k]] = s; });
  const onBoard = new Set(pool.map(s => s.id));

  const cell = cells.map(s => s ? { parts: [], muls: [], add: 0, mul: 1, dead: false, vanish: false, eatenBy: null } : null);
  const ev = [], flags = new Set(), transforms = [], spawns = [], purged = [];
  const grownValue = s => { const d = SYM[s.key]; return d.v + (d.store ? (s.c || 0) : 0) + (s.b || 0); };
  const baseOf = j => grownValue(cells[j]);
  const src = x => typeof x === 'number' ? cells[x].key : x;
  let eats = 0;
  const ctx = {
    key: j => cells[j] ? cells[j].key : null,
    base: j => cells[j] ? baseOf(j) : 0,
    sym: j => cells[j],
    merge: (i, j) => { if (cell[j].dead) return; cell[j].was = baseOf(j); cell[j].dead = true; cell[j].eatenBy = cells[i].key; ev.push({ t: 'eat', a: i, b: j, n: 0 }); },
    empty: j => !cells[j] && !blocked.has(j),
    nbAll: i => neighbors(i),
    nb: i => neighbors(i).filter(j => cells[j] && !cell[j].dead),
    all: () => cells.map((s, j) => j).filter(j => cells[j] && !cell[j].dead),
    add: (i, n, from) => {
      if (!n || !cell[i]) return;
      cell[i].add += n; cell[i].parts.push({ n, src: src(from) });
      if (typeof from === 'number' && from !== i) ev.push({ t: 'link', a: from, b: i });
    },
    mul: (j, m, from) => { cell[j].mul *= m; cell[j].muls.push({ m, src: src(from) }); ev.push({ t: 'mul', a: typeof from === 'number' ? from : j, b: j, m }); },
    eat: (i, j, bonus) => {
      if (cell[j].dead) return;
      cell[j].was = baseOf(j);
      cell[j].dead = true; cell[j].eatenBy = cells[i].key; eats++;
      cell[i].add += bonus; cell[i].parts.push({ n: bonus, ate: cells[j].key });
      ev.push({ t: 'eat', a: i, b: j, n: bonus });
    },
    vanish: (i, why) => { cell[i].was = baseOf(i); cell[i].vanish = why || true; ev.push({ t: 'boom', a: i }); },
    transform: (j, key, from, keep, inherit) => { transforms.push({ j, key, keep, inherit }); ev.push({ t: 'magic', a: from, b: j }); },
    spawn: (key, from) => { spawns.push({ i: from, key }); ev.push({ t: 'spawn', a: from }); },
    purgeCheapest: () => {
      const cand = st.inv.filter(s => !onBoard.has(s.id) && !purged.includes(s) && s.key !== 'ninja');
      if (!cand.length) return false;
      const min = Math.min(...cand.map(grownValue));
      purged.push(pickOne(cand.filter(s => grownValue(s) === min)));
      return true;
    },
    flag: f => flags.add(f),
    spinsLeft: st.spinsLeft,
    goneWorth: () => cells.reduce((t, s, j) => t + (s && (cell[j].dead || cell[j].vanish) ? (cell[j].was || 0) : 0), 0),
    goneCount: () => cells.filter((s, j) => s && (cell[j].dead || cell[j].vanish)).length,
    has: k => hasItem(st, k),
    eatGrow: (s, n) => { const e = hasItem(st, 'enmusubi') ? 1 : 0; const add = n + (s.g || 0) + e; s.g = (s.g || 0) + 1; if (s.xs !== st.totalSpins && rnd() < 0.1) { s.xs = st.totalSpins; s.c = (s.c || 0) * 2 + add; } else s.c = (s.c || 0) + add; },   // 食べて育つ：食べるたびに育つ量が+1ずつ増える。10%で今の育ちが ×2（1スピンに1回まで）
    grow: (s, n, cap) => { s.c = Math.min(cap || Infinity, (s.c || 0) + n + (hasItem(st, 'enmusubi') ? 1 : 0)); },   // コンボで育つ（えんむすびで +1）
    topInv: skip => { const m = {}; st.inv.forEach(x => { if (!skip.includes(x.key)) m[x.key] = (m[x.key] || 0) + 1; }); let top = null; for (const k in m) if (!top || m[k] > m[top]) top = k; return top; },
    row: i => (i / W) | 0, col: i => i % W,
    coins: st.coins,
    valueNow: j => (!cells[j] || cell[j].dead) ? 0 : Math.max(0, (baseOf(j) + cell[j].add) * cell[j].mul),
    baseOf,
  };
  const runPhase = ph => {
    for (let i = 0; i < N; i++) {
      const s = cells[i]; if (!s || cell[i].dead) continue;
      const d = SYM[s.key];
      if (d.act && (d.p || 0) === ph) d.act(ctx, i, s);
    }
  };
  runPhase(0); runPhase(1);
  st.items.forEach(k => { if (ITEMS[k].board) ITEMS[k].board(ctx); });
  if (st.curse === 'cold') ctx.all().forEach(j => { if (FOOD.has(ctx.key(j))) ctx.add(j, -1, '🥶さむぞら'); });
  runPhase(2); runPhase(3);
  runPhase(4);   // 食べるのはいちばん最後（ほかの効果が出たあと）
  runPhase(5);   // 食べられた・消えた数を見るもの（つぼ）

  const values = cells.map((s, i) => (!s || cell[i].dead) ? 0 : capN((baseOf(i) + cell[i].add) * cell[i].mul));
  const boardTotal = values.reduce((a, b) => a + b, 0);
  const keysAtSpin = cells.map(s => s && s.key);
  const detail = cells.map((s, i) => s ? {
    key: s.key, base: baseOf(i), parts: cell[i].parts, muls: cell[i].muls,
    value: values[i], eatenBy: cell[i].eatenBy, vanish: cell[i].vanish,
  } : null);

  // アイテム・呪いのボーナス
  const alive = ctx.all();
  const R = {
    board: boardTotal, eats,
    empties: open.filter(i => !cells[i]).length,
    gone: cells.filter((s, i) => s && (cell[i].dead || cell[i].vanish)).length,
    kinds: new Set(alive.map(j => ctx.key(j))).size,
    foods: alive.filter(j => FOOD.has(ctx.key(j))).length,
    lanterns: alive.filter(j => ctx.key(j) === 'lantern').length,
    engi: alive.filter(j => ENGI.has(ctx.key(j))).length,
    offBoard: Math.max(0, st.inv.length - pool.length),
  };
  const bonuses = [];
  let flat = 0, mult = 1;
  st.items.forEach(k => {
    const it = ITEMS[k];
    if (it.flat) { const n = it.flat(st, R); if (n) { flat += n; bonuses.push({ e: it.e, n: it.n, v: '+' + n }); } }
    if (it.mult) { const m = it.mult(st, R); if (m !== 1) { mult *= m; bonuses.push({ e: it.e, n: it.n, v: '×' + (Math.round(m * 100) / 100) }); } }
  });
  let total = capN(Math.floor(capN(boardTotal + flat) * mult));
  if (st.curse === 'tax') { const t = Math.floor(total * 0.15); if (t) { total -= t; bonuses.push({ e: '💸', n: 'ぜいきん', v: '-' + t }); } }

  // 後処理：消滅、変身、成長、誕生
  const removed = new Set(purged.map(s => s.id));
  cells.forEach((s, i) => { if (s && (cell[i].dead || cell[i].vanish)) removed.add(s.id); });
  const changes = [];
  const fast = alive.some(j => ctx.key(j) === 'sun') || hasItem(st, 'pot');
  const transformed = new Set();
  transforms.forEach(t => { const s = cells[t.j]; if (!s || removed.has(s.id) || transformed.has(s.id)) return; changes.push({ i: t.j, from: s.key, to: t.key, magic: true }); if (t.inherit) { const d0 = SYM[s.key]; s.b = (s.b || 0) + (d0.store ? (s.c || 0) : 0); } s.key = t.key; s.c = t.keep || 0; transformed.add(s.id); });
  cells.forEach((s, i) => {
    if (!s || removed.has(s.id) || transformed.has(s.id)) return;
    const d = SYM[s.key];
    if (d.grow) { s.c = (s.c || 0) + (fast && s.key === 'seed' ? 2 : 1); if (s.c >= d.grow) { changes.push({ i, from: s.key, to: GROW[s.key] }); s.key = GROW[s.key]; s.c = 0; } }
    else if (s.key === 'egg' && rnd() < (neighbors(i).some(j => cells[j] && !removed.has(cells[j].id) && cells[j].key === 'chicken') ? 0.5 : 0.2)) { changes.push({ i, from: 'egg', to: 'chick' }); s.key = 'chick'; s.c = 0; }
  });
  const born = spawns.map(x => ({ i: x.i, key: x.key }));
  cells.forEach((s, i) => { if (s && !removed.has(s.id) && s.key === 'chicken' && changes.every(c => c.i !== i) && rnd() < 0.15) born.push({ i, key: 'egg' }); });
  if (st.curse === 'rats') born.push({ i: null, key: 'mouse' });
  st.inv = st.inv.filter(s => !removed.has(s.id));
  born.forEach(b => st.inv.push(mk(b.key)));

  // 進行と記録
  const wasLast = st.spinsLeft === 1;
  st.coins = capN(st.coins + total); st.totalEarned = capN(st.totalEarned + total); st.totalSpins++; st.periodEarned = capN(st.periodEarned + total);
  st.inv.forEach(x => { if (x.c > MAXC) x.c = MAXC; if (x.b > MAXC) x.b = MAXC; });   // 育ちもカンストまで
  st.best = Math.max(st.best, total);
  st.spinsLeft--;
  st.stats.eats += eats; st.stats.gone += R.gone;
  st.stats.maxInv = Math.max(st.stats.maxInv, st.inv.length);
  if (pool.length >= open.length && open.length === N) flags.add('full');
  flags.forEach(f => { if (!st.stats.flags.includes(f)) st.stats.flags.push(f); });
  st.board = cells.map(s => s && !removed.has(s.id) ? { key: s.key, c: s.c, id: s.id } : null);

  // 依頼の判定
  let questDone = false;
  const q = st.quest;
  if (q && !q.done) {
    if (q.type === 'big') q.progress = Math.max(q.progress, total);
    if (q.type === 'eat') q.progress += eats;
    if (q.type === 'variety') q.progress = Math.max(q.progress, R.kinds);
    if (q.type === 'same') { const m = {}; alive.forEach(j => { const k = ctx.key(j); m[k] = (m[k] || 0) + 1; }); q.progress = Math.max(q.progress, ...Object.values(m), 0); }
    if (q.type === 'earn') q.progress = st.periodEarned;
    if (q.type === 'lean') q.progress = st.inv.length;
    if (q.type !== 'lean' && q.progress >= q.target) questDone = completeQuest(st);
  }

  const res = { keys: keysAtSpin, values, dead: cell.map(c => !!(c && (c.dead || c.vanish))), ev, total, boardTotal, bonuses, changes, born, detail, blocked: [...blocked], purged: purged.map(s => s.key), flags: [...flags], questDone, wasLast };
  st.last = { detail, total, boardTotal, bonuses, changes, born, blocked: [...blocked], purged: res.purged };
  return res;
}

function rarityOdds(st) {
  const r = st.rentIdx;
  const clovers = st.inv.filter(s => s.key === 'clover').length;
  const luck = DIFFS[st.diff].luck + (hasItem(st, 'omamori') ? 0.05 : 0);
  const scope = hasItem(st, 'telescope') ? 0.03 : 0;
  let U = 0.22 + 0.03 * r, R = 0.04 + 0.015 * r + 0.03 * clovers + luck, V = 0.005 + 0.004 * r + 0.008 * clovers + luck / 3 + scope;
  U = Math.min(U, 0.45); R = Math.max(0.01, Math.min(R, 0.32)); V = Math.max(0.002, Math.min(V, 0.13));
  return { C: Math.max(0, 1 - U - R - V), U, R, V };
}
function choiceCount(st) { return 3 + (hasItem(st, 'ticket') ? 1 : 0) - (st.curse === 'soldout' ? 1 : 0); }

function rollChoices(st) {
  const odds = rarityOdds(st), picks = [], n = choiceCount(st);
  const pal = new Set(st.inv.flatMap(x => partners(x.key)));
  let guard = 0;
  while (picks.length < n && guard++ < 200) {
    let x = rnd(), rar = 'C';
    for (const k of ['V', 'R', 'U', 'C']) { if (x < odds[k]) { rar = k; break; } x -= odds[k]; }
    const opts = Object.keys(SYM).filter(k => SYM[k].r === rar && !picks.includes(k));
    if (opts.length) {
      // 手持ちのシンボルと相性のいいもの（相方）は 5倍 出やすい
      const w = opts.map(k => pal.has(k) ? 5 : 1);
      let y = rnd() * w.reduce((p, q) => p + q, 0), idx = 0;
      while (idx < opts.length - 1 && y >= w[idx]) { y -= w[idx]; idx++; }
      picks.push(opts[idx]);
    }
  }
  st.choices = picks;
  return picks;
}
function canReroll(st) { return st.rerolls > 0 && st.curse !== 'seal'; }

function rollItems(st) {
  const luck = hasItem(st, 'omamori') ? 0.05 : 0;
  const odds = { R: 0.1 + 0.01 * st.rentIdx + luck, U: 0.33 };
  const picks = [];
  let guard = 0;
  while (picks.length < 3 && guard++ < 200) {
    const x = rnd(), rar = x < odds.R ? 'R' : x < odds.R + odds.U ? 'U' : 'C';
    const opts = Object.keys(ITEMS).filter(k => ITEMS[k].r === rar && !picks.includes(k) && !st.items.includes(k));
    if (opts.length) picks.push(pickOne(opts));
    else if (!Object.keys(ITEMS).some(k => !picks.includes(k) && !st.items.includes(k))) break;
  }
  st.itemChoices = picks;
  return picks;
}
function addItem(st, k) {
  if (!ITEMS[k] || st.items.includes(k)) return;
  st.items.push(k);
  if (k === 'broom') st.removals++;
  if (k === 'tebukuro') st.removals += 3;
}
function removeSymbol(st, key) {
  if (st.removals <= 0) return false;
  // 同じ種類でも個体ごとに成長度が違うため、現在の基礎稼ぎが一番低いものを除去する
  let idx = -1, minValue = Infinity;
  st.inv.forEach((s, i) => {
    if (s.key !== key) return;
    const d = SYM[s.key];
    const value = d.v + (d.store ? (s.c || 0) : 0) + (s.b || 0);
    if (value < minValue) { idx = i; minValue = value; }
  });
  if (idx < 0) return false;
  st.inv.splice(idx, 1); st.removals--; st.stats.removed++;
  if (hasItem(st, 'broom')) st.coins += 8;
  return true;
}

function rentDue(st) { return st.spinsLeft <= 0; }
// 家賃を払う。結果の情報を返す
function payRent(st) {
  const info = { ok: false, paid: st.rent, bonus: [], questDone: false };
  const q = st.quest;
  if (q && !q.done && q.type === 'lean' && st.inv.length <= q.target) info.questDone = completeQuest(st);
  if (st.rent >= MAXC && st.coins >= MAXC) { info.ok = true; info.kanst = true; st.phase = 'kanst'; return info; }   // コインも家賃も最大：カンスト
  if (st.coins < st.rent) { st.phase = 'over'; return info; }
  info.ok = true;
  st.coins -= st.rent;
  if (st.curse) st.stats.curses++;
  const kd = st.inv.filter(s => s.key === 'kadomatsu').length;
  if (kd) { for (let k = 0; k < kd * 3; k++) st.inv.push(mk('coin')); info.bonus.push(`🎍→🪙×${kd * 3}`); }
  if (hasItem(st, 'onsen')) { const n = Math.floor(st.coins * 0.1); if (n) { st.coins += n; info.bonus.push(`♨️+${n}`); } }
  st.rerolls++; st.removals++;
  if (hasItem(st, 'yoyo')) { st.rerolls++; info.bonus.push('🪀🔄+1'); }
  if (hasItem(st, 'scroll')) { st.removals++; info.bonus.push('📜✂️+1'); }
  st.rentIdx++;
  if (!st.endless && st.rentIdx >= totalRents(st)) { st.phase = 'clear'; return info; }
  startPeriod(st);
  st.itemPicks++;
  rollEvent(st, 0.45);
  return info;
}
function goEndless(st) { st.endless = true; startPeriod(st); st.itemPicks++; rollItems(st); st.phase = 'item'; }

if (typeof module !== 'undefined') module.exports = { exportDaily, importDaily, stepDaily, act, prepItems, afterItems, dailySetup, replayDaily, seedFrom, STAGE_LEN, endlessStage, stageCurseChance, isEndlessMode, endlessCount, W, H, N, SYM, ITEMS, CURSES, DIFFS, RARITY, STARTERS, EVENTS, newGame, newDaily, runEvent, setRng, seededRng, spin, rollChoices, rollItems, addItem, removeSymbol, rentDue, payRent, goEndless, canReroll, mk, rarityOdds, neighbors, partners, totalRents, hasItem };

export default { act, exportDaily, importDaily, stepDaily, replayDaily, newDaily, dailySetup, setRng, SYM, ITEMS, CURSES, DIFFS };
