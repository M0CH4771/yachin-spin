# X などで URL を貼ったときに出る画像（1200x630）と、タブのアイコンを作る
# 使い方：python3 tools/ogp.py   → ogp.png と favicon.png をリポジトリの直下に書き出す
import json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
p = lambda *a: os.path.join(ROOT, *a)
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'   # ない環境では好きな日本語フォントに変える
W, H = 1200, 630
INK, RED, EDGE, RIM, GOLD, MUTE = (255, 226, 168), (163, 47, 40), (11, 8, 18), (65, 52, 94), (242, 193, 78), (214, 204, 232)

def pixel_text(text, size, scale, color, shadow=None):
    """小さく描いてから拡大して、ドット文字にする"""
    f = ImageFont.truetype(FONT, size, index=0)
    l, t, r, b = f.getbbox(text)
    small = Image.new('L', (r - l + 2, b - t + 2), 0)
    ImageDraw.Draw(small).text((1 - l, 1 - t), text, font=f, fill=255)
    small = small.point(lambda v: 255 if v > 110 else 0)
    mask = small.resize((small.width * scale, small.height * scale), Image.NEAREST)
    out = Image.new('RGBA', (mask.width + scale * 4, mask.height + scale * 4), (0, 0, 0, 0))
    if shadow:
        for (dx, dy, c) in shadow:
            out.paste(Image.new('RGBA', mask.size, c + (255,)), (dx, dy), mask)
    out.paste(Image.new('RGBA', mask.size, color + (255,)), (0, 0), mask)
    return out

def frame(img, pad=6):
    """ゲームの枠と同じ：黒い縁＋内側の線"""
    w, h = img.size
    f = Image.new('RGBA', (w + pad * 2, h + pad * 2), EDGE + (255,))
    ImageDraw.Draw(f).rectangle([3, 3, w + pad * 2 - 4, h + pad * 2 - 4], outline=RIM, width=3)
    f.paste(img, (pad, pad))
    return f

# 背景：なつまつりの通りを横長に切って、ぼかして暗くする
bg = Image.open(p('bg', 'festival.jpg')).convert('RGB')
bg = bg.resize((W, round(bg.height * W / bg.width)), Image.LANCZOS).crop((0, 330, W, 330 + H)).filter(ImageFilter.GaussianBlur(3))
shade = Image.new('L', (W, H))
for x in range(W): shade.paste(int(215 - 120 * min(1, x / 900)), (x, 0, x + 1, H))
canvas = Image.composite(Image.new('RGB', (W, H), (16, 11, 28)), bg, shade).convert('RGBA')

# 右：はじめての横丁の挿絵をカードにする
cg = Image.open(p('cg', 'yokocho.jpg')).convert('RGB')
card = cg.resize((300, round(cg.height * 300 / cg.width)), Image.LANCZOS).crop((0, 0, 300, 520))
card = frame(card.convert('RGBA'))
sh = Image.new('RGBA', card.size, (0, 0, 0, 150)).filter(ImageFilter.GaussianBlur(8))
canvas.alpha_composite(sh, (W - card.width - 46, 66))
canvas.alpha_composite(card, (W - card.width - 54, 54))

# 左：タイトル（ドット文字）
sd = lambda s: [(s * 2, s * 2, RED), (s * 4, s * 4, EDGE)]
y = 58
for line in ('ヤチン', 'スピン'):
    t = pixel_text(line, 22, 6, INK, sd(2)); canvas.alpha_composite(t, (64, y)); y += t.height - 10
sub = pixel_text('縁日スロットで家賃を払え', 13, 3, GOLD, [(3, 3, EDGE)]); canvas.alpha_composite(sub, (70, y + 14))
tag = pixel_text('ばあちゃんのスロット台と、ツケの残った長屋の話。', 12, 2, MUTE, [(2, 2, EDGE)]); canvas.alpha_composite(tag, (72, y + 14 + sub.height + 12))

# 下：タイトル画面と同じシンボルの並び
sheet = Image.open(p('art', 'sheet.png')).convert('RGBA'); idx = json.load(open(p('art', 'sheet.json')))['idx']
cell = lambda k: sheet.crop(((idx[k] % 16) * 32, (idx[k] // 16) * 32, (idx[k] % 16) * 32 + 32, (idx[k] // 16) * 32 + 32))
x = 72
for k in ('lantern', 'fox', 'dango', 'dragon', 'firework'):
    box = Image.new('RGBA', (76, 76), (44, 35, 66, 255))
    box.alpha_composite(cell(k).resize((64, 64), Image.NEAREST), (6, 6))
    b = frame(box, 5); canvas.alpha_composite(b, (x, H - b.height - 40)); x += b.width + 12
canvas.convert('RGB').save(p('ogp.png'), optimize=True)

# タブのアイコン：提灯のドット絵
ic = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); ic.alpha_composite(cell('lantern').resize((64, 64), Image.NEAREST))
ic.save(p('favicon.png'))
print('ogp.png', os.path.getsize(p('ogp.png')) // 1024, 'KB / favicon.png')
