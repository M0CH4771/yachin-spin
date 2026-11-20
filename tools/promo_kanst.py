# 番外エンディング追加の告知画像（1200x675 を2枚）。部品は promo.py と同じ
# 使い方：python3 tools/promo_kanst.py   → art/promo/kanst_*.png
import os
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'promo.py'), encoding='utf-8').read()
exec(_src[:_src.index('# ---- 1枚目')])

def center(img, s, y, size=10, scale=2, color=None):
    t = pixel_text(s, size, scale, color or MUTE, [(2, 2, EDGE)]); img.alpha_composite(t, ((W - t.width) // 2, y)); return y + t.height

def cg_bg(name, blur, dark):
    bg = Image.open(p('cg', name + '.jpg')).convert('RGB')
    bg = bg.resize((W, round(bg.height * W / bg.width)), Image.LANCZOS)
    top = max(0, int((bg.height - H) * 0.3))
    bg = bg.crop((0, top, W, top + H)).filter(ImageFilter.GaussianBlur(blur))
    return Image.blend(bg, Image.new('RGB', (W, H), (16, 11, 28)), dark).convert('RGBA')

# ---- 1枚目：番外エンディング（ネタバレなし：ぼかした挿絵）----
img = cg_bg('kanst_sora', 10, 0.55)
for k in range(13):
    t = cell('lantern').resize((36, 36), Image.NEAREST); img.alpha_composite(t, (14 + k * 92, 10))
y = header(img, '隠しエンディング 追加', None)
b = pixel_text('番外「カンスト」', 20, 4, GOLD, [(4, 4, RED), (8, 8, EDGE)]); img.alpha_composite(b, ((W - b.width) // 2, y + 18))
yy = y + 40 + b.height
d = ImageDraw.Draw(img); d.rectangle((210, yy, W - 210, yy + 150), fill=(20, 14, 34), outline=(150, 120, 200), width=3)
text(img, '見られる条件（どちらか）', W // 2, yy + 16, 24, GOLD, 'ma')
text(img, '・所持縁銭が、表示できる最大までたどりつく', 250, yy + 62, 22, INK, stroke=2)
text(img, '・家賃を、千回払いきる', 250, yy + 100, 22, INK, stroke=2)
center(img, '8人全員登場・新しい挿絵7枚・背景2枚', yy + 176, 11)
footer(img); img.convert('RGB').save(os.path.join(OUT, 'kanst_1_ending.png'), optimize=True)

# ---- 2枚目：エンドレス(?)と、数の表示 ----
img = base(); y = header(img, 'エンドレス(?) と 数の表示', None)
d = ImageDraw.Draw(img)
d.rectangle((70, y + 10, W - 70, y + 150), fill=(24, 18, 40), outline=(120, 96, 160), width=3)
text(img, 'エンドレス →「エンドレス(?)」', 96, y + 28, 27, GOLD)
text(img, '終わりがあることがわかったので、名前が変わりました', 96, y + 80, 21, INK, stroke=2)
text(img, '（記録やセーブは、そのまま引きつぎ）', 96, y + 114, 19, MUTE, stroke=2)
yy = y + 175
d.rectangle((70, yy, W - 70, yy + 215), fill=(24, 18, 40), outline=(120, 96, 160), width=3)
text(img, '大きい数は 和式の単位で', 96, yy + 18, 27, GOLD)
rows = [('12,345', '1.23万'), ('340,773,119', '3.41億'), ('7,300,000,000,000', '7.3兆'), ('1.5×10の68乗', '1.5無量大数')]
for k, (a, b2) in enumerate(rows):
    x0 = 110 + (k % 2) * 520; yr = yy + 76 + (k // 2) * 64
    text(img, a, x0, yr, 21, MUTE, stroke=2); text(img, '→', x0 + 250, yr - 2, 24, GOLD); text(img, b2, x0 + 290, yr - 2, 25, INK)
footer(img); img.convert('RGB').save(os.path.join(OUT, 'kanst_2_other.png'), optimize=True)
print('art/promo/ に kanst を2枚')
