# Ver.1.4 の告知画像（1200x675 を4枚）。描き方の部品は promo.py と同じものを使う
# 使い方：python3 tools/promo14.py   → art/promo/v14_*.png
import os
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'promo.py'), encoding='utf-8').read()
exec(_src[:_src.index('# ---- 1枚目')])

def arrow(img, x, y, size=44):
    text(img, '→', x, y, size, GOLD, 'mm')

def chain(img, ks, x, y, size, gap):
    """シンボルを → でつないで並べる（ks の '+' は ＋記号）"""
    for k in ks:
        if k in ('+', '→'):
            text(img, '＋' if k == '+' else '→', x + gap // 2, y + size // 2, 40, GOLD, 'mm'); x += gap
        else:
            tile(img, k, x, y, size); x += size
    return x

def chain_w(ks, size, gap): return sum(gap if k in ('+', '→') else size for k in ks)

# ---- 1枚目：表紙 ----
img = base()
y = header(img, 'アップデート Ver.1.4', None)
for i, (big, small) in enumerate((('合体', 'ならべて進化'), ('コンボ', 'がもっと強く'))):
    cx = W // 2 + (-230 if i == 0 else 230)
    b = pixel_text(big, 22, 5, GOLD, [(4, 4, RED), (8, 8, EDGE)]); img.alpha_composite(b, (cx - b.width // 2, y + 14))
    s = pixel_text(small, 12, 3, INK, [(3, 3, EDGE)]); img.alpha_composite(s, (cx - s.width // 2, y + 24 + b.height))
row = ['mikazuki', '→', 'hangetsu', '→', 'moon']
size, gap = 76, 60
x = (W - chain_w(row, size, gap)) // 2; chain(img, row, x, 452, size, gap)
c = pixel_text('みかづき → はんげつ → まんげつ　／　お茶 ＋ だんご → おちゃだんご', 11, 2, MUTE, [(2, 2, EDGE)])
img.alpha_composite(c, ((W - c.width) // 2, 572))
footer(img); img.convert('RGB').save(os.path.join(OUT, 'v14_1_cover.png'), optimize=True)

# ---- 2枚目：合体 ----
img = base(); y = header(img, 'となりに出ると 合体！', None)
ROWS = [(['tea', '+', 'dango', '→', 'chadango'], 'お茶 ＋ だんご → おちゃだんご', 'おちゃだんご同士がとなりにいると、どっちも育つ'),
        (['mikazuki', '+', 'mikazuki', '→', 'hangetsu'], 'みかづき ＋ みかづき → はんげつ', '盤面のうさぎ・だんご・おちゃだんごが +2'),
        (['hangetsu', '+', 'hangetsu', '→', 'moon'], 'はんげつ ＋ はんげつ → まんげつ', '合体でしか作れない。1つにつき うさぎ・だんごが ×2')]
size, gap = 64, 50
for n, (ks, name, desc) in enumerate(ROWS):
    yy = y + 4 + n * 130
    chain(img, ks, 60, yy, size, gap)
    text(img, name, 60 + chain_w(ks, size, gap) + 36, yy + 2, 28, INK)
    text(img, desc, 60 + chain_w(ks, size, gap) + 36, yy + 40, 20, MUTE, stroke=2)
footer(img); img.convert('RGB').save(os.path.join(OUT, 'v14_2_merge.png'), optimize=True)

# ---- 3枚目：コンボの育ち ----
img = base(); y = header(img, 'コンボで育つ量が 2倍に', None)
UPS = [('honey', 'はちみつ', '+1 → +2'), ('tentou', 'てんとうむし', '+1 → +2'), ('butterfly', 'ちょうちょ', '+1 → +2'), ('sushi', 'おすし', '+1 → +2'),
       ('kotatsu', 'こたつ', '+1 → +2'), ('rabbit', 'うさぎ', '+1 → +2\n最大 +8 → +30'), ('sparrow', 'すずめ', '+1 → +2'), ('fox', 'きつね', '+1 → +2'),
       ('mouse', 'ねずみ', '+1 → +2'), ('purse', 'がまぐち', '+2 → +3'), ('daruma', 'だるま', '縁起物の数\n×1 → ×2'), ('tamaya', 'たまや', 'はなびの数\n×2 → ×3')]
grid(img, UPS, y + 2, 4, 292, 108, 64, 196, 24, 19)
n1 = pixel_text('さらに、手持ちの相方が 候補に5倍 出やすく', 12, 2, GOLD, [(2, 2, EDGE)])
img.alpha_composite(n1, ((W - n1.width) // 2, 584)); footer(img)
img.convert('RGB').save(os.path.join(OUT, 'v14_3_combo.png'), optimize=True)

# ---- 4枚目：大物とお守り ----
img = base(); y = header(img, '大物も育つ ＆ 新しいお守り', None)
BIG = [('whale', 'くじら', '金魚をのみこむたび\n育つ（+4）'), ('bear', 'くま', 'はちみつを\n食べるたび 育つ（+4）'),
       ('eagle', 'わし', '食べた相手の稼ぎ\nまるごと わしが育つ'), ('i_enmusubi', 'えんむすび', 'お宝のお守り。コンボで\n育つとき さらに +1')]
grid(img, BIG, y + 20, 2, 560, 170, 104, 380, 34, 24)
footer(img); img.convert('RGB').save(os.path.join(OUT, 'v14_4_big.png'), optimize=True)
print('art/promo/ に v14 を4枚')
