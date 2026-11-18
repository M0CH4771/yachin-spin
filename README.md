# ヤチン・スピン — 縁日スロットで家賃を払え

ばあちゃんのスロット台と、ツケの残った長屋の話。

妖怪の住む夜の縁日「よいまつり横丁」で、スロット台をまわして縁銭（えんせん）を稼ぎ、長屋の家賃を払いつづけるブラウザゲームです。手持ちのシンボルを育てるデッキ構築型のスロットで、となり同士の相性で稼ぎが伸びます。

**遊ぶ** → https://m0ch4771.github.io/yachin-spin/

## 遊べるもの

- **ストーリー**：序章＋全4話＋エピローグ。祖母ハナの残した三十縁銭のツケをめぐる話
- **フリープレイ**：EASY / NORMAL / HARD / SUPER HARD。払いきったあとはエンドレス
- **デイリー**：日付ごとにお題と台の出方が全員同じ
- シンボル 89種・お守り 45種・横丁のできごと 14種・大家の気まぐれ 8種・実績 44個・図鑑

スマホの縦画面向けです。進み具合はブラウザに保存されます。

## ファイル

```
index.html            組み立て済みのゲーム本体（これ1つで動く）
src/ui.html           画面・演出・会話シーン（組み立て前のひな形）
src/engine.js         ルール（シンボル・お守り・家賃・難易度・デイリー）
src/story.js          台本・背景・章立て
art/sheet.png         ドット絵シート（32×32、16列）
art/sheet.json        シート内の並び
art/busts.json        会話の顔窓（8人×4表情）
tools/build.py        src/ と art/ から index.html を組み立てる
tools/pixel/          ドット絵の描画コード（Python）
tools/sim/balance.js  難易度ごとのクリア率を調べるシミュレーター
```

## 組み立て方

```
# ドット絵シートを描き直す（art/sheet.png・sheet.json・preview.png を書き出す）
python3 tools/pixel/build_sheet.py

# index.html を組み立てる
python3 tools/build.py

# 難易度バランスを確認する
node tools/sim/balance.js
```

Python 3 と Pillow、Node.js が必要です。

## クレジット

- 企画：M0CH4771
- フォント：[DotGothic16](https://fonts.google.com/specimen/DotGothic16)（SIL Open Font License）
- ゲームの仕組みは [Luck be a Landlord](https://store.steampowered.com/app/1404850/) に着想を得ています。シンボル・ルール・絵・物語はすべてオリジナルです。
