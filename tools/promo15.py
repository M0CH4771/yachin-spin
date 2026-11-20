# Ver.1.5 の告知画像（1200x675 を4枚）。描き方の部品は promo.py と同じものを使う
# 使い方：python3 tools/promo15.py   → art/promo/v15_*.png
import os
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'promo.py'), encoding='utf-8').read()
exec(_src[:_src.index('# ---- 1枚目')])

def center(img, s, y, size=10, scale=2, color=None):
    t = pixel_text(s, size, scale, color or MUTE, [(2, 2, EDGE)]); img.alpha_composite(t, ((W - t.width) // 2, y)); return y + t.height

# ---- 1枚目：表紙 ----
img = base()
y = header(img, 'アップデート Ver.1.5', None)
b = pixel_text('どの道でも 天井まで', 20, 4, GOLD, [(4, 4, RED), (8, 8, EDGE)]); img.alpha_composite(b, ((W - b.width) // 2, y + 20))
row = ['cat', 'kappa', 'oden', 'turtle', 'kagiya', 'tamaya', 'daruma', 'tsubo', 'tanuki']
size = 76; gap = 22; tot = len(row) * size + (len(row) - 1) * gap; x = (W - tot) // 2
for k in row: tile(img, k, x, 420, size); x += size + gap
center(img, '食べる系の強化　／　新しい道「おでん・かめ・かぎや」　／　つぼ・たぬき', 540, 11)
footer(img); img.convert('RGB').save(os.path.join(OUT, 'v15_1_cover.png'), optimize=True)

# ---- 2枚目：食べる系 ----
img = base(); y = header(img, '食べる系：食べるほど 育ちが加速', None)
EAT = ['mouse', 'sparrow', 'fox', 'cat', 'snake', 'kappa', 'bear', 'whale', 'purse', 'eagle', 'oden']
size = 64; gap = 24; tot = len(EAT) * size + (len(EAT) - 1) * gap; x = (W - tot) // 2
for k in EAT: tile(img, k, x, y + 6, size); x += size + gap
yy = y + 110
d = ImageDraw.Draw(img)
for n, (title, lines) in enumerate([
        ('ルール1　育つ量が 1ずつ増える', ['食べるたびに、次に育つ量が +1 ずつ増えていく', '例：ねこ（+2）→ 1匹目 +2、2匹目 +3、3匹目 +4 …', '食べた回数は、そのシンボルごとにずっと記録']),
        ('ルール2　10%で 今の育ちが ×2', ['食べるたびに 10%の確率で、今までの育ちが ×2', '×2 になるのは 1スピンにつき1回まで', 'お守り「えんむすび」の +1 も、毎回上乗せ'])]):
    bx = 70 + n * 545
    d.rectangle((bx, yy, bx + 515, yy + 250), fill=(24, 18, 40), outline=(120, 96, 160), width=3)
    text(img, title, bx + 22, yy + 18, 27, GOLD)
    for k, ln in enumerate(lines): text(img, ln, bx + 22, yy + 76 + k * 52, 21, INK if k == 0 else MUTE, stroke=2)
footer(img); img.convert('RGB').save(os.path.join(OUT, 'v15_2_eat.png'), optimize=True)

# ---- 3枚目：新しい道 ----
img = base(); y = header(img, '新しい道', None)
ROUTES = [('oden', 'おでん × やたい', 'となりの食べ物を煮込んで（食べて）、\nその稼ぎぶん育つ。やたいがとなりなら\n煮込んだスピンは 今の育ちが ×2'),
          ('turtle', 'かめ × おおなみ', 'となりの海の生き物1つにつき 育つ（+1）\nとなりに海の生き物＋盤面におおなみで\n10%の確率で 今の育ちが ×1.5'),
          ('kagiya', 'かぎや（新シンボル）', 'となりのたまや・はなびを ×5\nたまやからは 花火として数えられる\n「たまや〜」「かぎや〜」'),
          ('daruma', 'だるま', '縁起物の数だけ 育つ（今までどおり）\n育つとき 10%の確率で\n今の育ちが ×2')]
grid(img, ROUTES, y + 8, 2, 570, 200, 96, 420, 28, 20)
footer(img); img.convert('RGB').save(os.path.join(OUT, 'v15_3_routes.png'), optimize=True)

# ---- 4枚目：つぼ・たぬき・物語 ----
img = base(); y = header(img, 'つぼ・たぬき・物語モード', None)
OTH = [('tsubo', 'つぼ', '盤面で消えた・食べられたシンボルの\n稼ぎ（育った分も）を 吸い込んで育つ\n1つにつき さらに +3'),
       ('tanuki', 'たぬき', '化かされても 育ちはそのまま残る\n育ったシンボルが てんぐ などに\n化けることも…')]
grid(img, OTH, y + 8, 2, 570, 200, 96, 420, 28, 20)
yy = y + 230
d = ImageDraw.Draw(img); d.rectangle((70, yy, W - 70, yy + 200), fill=(24, 18, 40), outline=(120, 96, 160), width=3)
text(img, '物語モード：家賃の調整', 96, yy + 18, 27, GOLD)
text(img, 'コンボが伸びやすくなったぶん、「むずかしい」「ちょうむずかしい」の家賃を引き上げ', 96, yy + 70, 21, INK, stroke=2)
text(img, 'むずかしい　　　　　家賃の倍率 1.25 → 1.35　／　上がり方 0.13 → 0.17', 96, yy + 112, 21, MUTE, stroke=2)
text(img, 'ちょうむずかしい　　家賃の倍率 1.30 → 1.55　／　上がり方 0.12 → 0.16', 96, yy + 148, 21, MUTE, stroke=2)
footer(img); img.convert('RGB').save(os.path.join(OUT, 'v15_4_other.png'), optimize=True)
print('art/promo/ に v15 を4枚')
