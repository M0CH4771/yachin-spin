# ヤチンスピン — 縁日スロットで家賃を払え

ばあちゃんのスロット台と、ツケの残った長屋の話。

妖怪の住む夜の縁日「よいまつり横丁」で、スロット台をまわして縁銭（えんせん）を稼ぎ、長屋の家賃を払いつづけるブラウザゲームです。手持ちのシンボルを育てるデッキ構築型のスロットで、となり同士の相性で稼ぎが伸びます。

**遊ぶ** → https://m0ch4771.github.io/yachin-spin/

## 遊べるもの

- **ストーリー**：序章＋全4話＋エピローグ。祖母ハナの残した三十縁銭のツケをめぐる話。最初はこれだけ
- **エンドレス**（最終話クリアで解放）：家賃を払いつづけて、どこまで住めるか。5回ごとに段が上がり、家賃も大家の気まぐれもきつくなる。結果は 𝕏 にポストして #ヤチンスピン でくらべられる
- **デイリー**（最終話クリアで解放）：その日のお題（ずっと続く気まぐれ・はじめの荷物・最初のおまけ）は全員同じで、そのあとは毎回ランダム。家賃を何回払えたかを、リアルタイムのランキングで競う。各プレイヤーの最終的な構成も見られる
- 結果は画像つきで 𝕏 にポストできる（スマホは共有シートから、PCは画像を保存してポスト画面をひらく）
- ホーム画面に追加すると、アプリのように開ける（オフラインでも起動できる）
- シンボル 89種・お守り 45種・横丁のできごと 14種・大家の気まぐれ 8種・実績 44個・図鑑

スマホの縦画面向けです。進み具合はブラウザに保存されます。

## ファイル

```
index.html            組み立て済みのゲーム本体（bg/・cg/ と同じ場所に置く）
src/ui.html           画面・演出・会話シーン（組み立て前のひな形）
src/engine.js         ルール（シンボル・お守り・家賃・難易度・デイリー）
src/story.js          台本・背景・章立て
art/sheet.png         ドット絵シート（32×32、16列）
art/sheet.json        シート内の並び
art/busts.json        会話の顔窓（8人×4表情）
bg/                   会話シーンの背景（14枚、720px幅のJPEG）
cg/                   物語の挿絵（15枚。見た挿絵はストーリー画面のギャラリーで見返せる）
ogp.png               URLを貼ったときに出る共有用の画像（1200×630、元絵は art/ogp/ogp_original.png）
favicon.png           タブのアイコン
tools/build.py        src/ と art/ から index.html を組み立てる
tools/ogp.py          アイコン（favicon.png）と、ドット版の共有画像の試作（art/ogp/ogp_dot.png）を作る
tools/pixel/          ドット絵の描画コード（Python）
tools/sim/balance.js  ストーリー各話のクリア率を調べるシミュレーター
tools/sim/endless.js  エンドレスで何回払えるかの分布を調べるシミュレーター
tools/sim/daily.js    デイリーの分布と、記録を再生したとき結果が一致するかを調べる
manifest.webmanifest  ホーム画面に追加するための設定
sw.js                 オフラインでも起動できるようにするキャッシュ
icons/                ホーム画面のアイコン
worker/               デイリーランキングのサーバー（Cloudflare Workers + D1）
```

## 組み立て方

```
# ドット絵シートを描き直す（art/sheet.png・sheet.json・preview.png を書き出す）
python3 tools/pixel/build_sheet.py

# index.html を組み立てる
python3 tools/build.py

# 難易度バランスを確認する
node tools/sim/balance.js
node tools/sim/endless.js 1.2 1.25    # 家賃の伸び率と倍率を変えて試せる
```

Python 3 と Pillow、Node.js が必要です。

## デイリーランキングのサーバー（Cloudflare Workers + D1）

ゲームは GitHub Pages だけで動きます。ランキングを出すには、`worker/` を Cloudflare に置いて、その URL を `src/ui.html` の `RANK_API_DEFAULT` に書きます（空のあいだはランキングなしで遊べます）。

**しくみ**

- 1回ごとに、サーバーが乱数のタネを配ります。お題と最初のおまけは日付で決まるので全員同じ
- プレイヤーの操作（まわす・取る・家賃を払う…）を、家賃を払うたびに12個ずつ送ります
- サーバーは同じエンジン（`worker/src/engine.js`、`tools/build.py` が `src/engine.js` から作る）で、その操作をゲームの状態に当てて確かめます。手元で数字を書きかえても、ランキングには入りません
- 1回の処理は数ミリ秒なので、無料プランの「1回 10ms まで」に収まります
- ランキングは「その日の、プレイヤーごとのいちばんいい回」。家賃の回数 → かせいだコインの順。挑戦中の人は「挑戦中」と出ます

**はじめて置くとき**（`worker/` の中で）

```
cd worker
npx wrangler login
npx wrangler d1 create yachin-spin
#   → 出てきた database_id を wrangler.toml の database_id に貼る
npx wrangler d1 execute yachin-spin --remote --file=schema.sql
npx wrangler secret put ADMIN_KEY
#   → 管理用の合言葉を入力（出入り禁止にするときに使う）
npx wrangler deploy
#   → https://yachin-spin-rank.＜あなたのサブドメイン＞.workers.dev が出る
```

出てきた URL を `src/ui.html` の `const RANK_API_DEFAULT = '';` に入れて、`python3 tools/build.py` で組み立て直します。

**エンジンを変えたとき**は、`python3 tools/build.py` のあと `cd worker && npx wrangler deploy` で、サーバーのエンジンもそろえてください（ずれると記録が確かめられなくなります）。

**手元で試す**

```
cd worker
npm test                                   # node:sqlite で API を通しで試す
node --no-warnings test/serve.mjs 8787     # ブラウザ用のローカルサーバー
#   ブラウザの開発者ツールで localStorage.setItem('yachin-spin-api', '"http://127.0.0.1:8787"') として再読みこみ
```

**困った名前の人を消す**

```
curl -X POST https://＜workerのURL＞/api/admin -H "X-Admin: ＜ADMIN_KEY＞" -H "Content-Type: application/json" -d '{"find":"名前"}'
curl -X POST https://＜workerのURL＞/api/admin -H "X-Admin: ＜ADMIN_KEY＞" -H "Content-Type: application/json" -d '{"ban":"＜上で出たid＞"}'
```

## クレジット

- 企画：M0CH4771
- フォント：[DotGothic16](https://fonts.google.com/specimen/DotGothic16)（SIL Open Font License）
- ゲームの仕組みは [Luck be a Landlord](https://store.steampowered.com/app/1404850/) に着想を得ています。シンボル・ルール・絵・物語はすべてオリジナルです。
