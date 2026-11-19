import sys, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, '..', '..', 'art')
sys.path.insert(0, HERE)
from PIL import Image, ImageDraw
from pixel import hx, N
from sprites import SP
import sprites_fix
import sprites_fix2
import sprites_fix3
import sprites_fix4
import sprites_fix5
names = list(SP.keys())
cols = 16
rows = (len(names) + cols - 1) // cols
sheet = Image.new('RGBA', (cols * N, rows * N), (0, 0, 0, 0))
idx = {}
def center(s):
    # 描いた部分の外枠を求めて、32マスのまん中に寄せる
    pts = [(x, y) for y in range(N) for x in range(N) if s.g[y][x]]
    if not pts: return s
    x0 = min(p[0] for p in pts); x1 = max(p[0] for p in pts); y0 = min(p[1] for p in pts); y1 = max(p[1] for p in pts)
    dx = (N - 1 - x1 - x0) // 2; dy = (N - 1 - y1 - y0) // 2
    g = [[None] * N for _ in range(N)]
    for x, y in pts: g[y + dy][x + dx] = s.g[y][x]
    s.g = g; return s
for i, n in enumerate(names):
    s = center(SP[n]())
    x0, y0 = (i % cols) * N, (i // cols) * N
    for y in range(N):
        for x in range(N):
            c = s.g[y][x]
            if c: sheet.putpixel((x0 + x, y0 + y), hx(c) + (255,))
    idx[n] = i
sheet.save(os.path.join(ART, 'sheet.png'))
json.dump({'cols': cols, 'idx': idx}, open(os.path.join(ART, 'sheet.json'), 'w'))
# 確認用プレビュー（3倍＋名前）
sc = 3
pv = Image.new('RGB', (cols * (N * sc + 8), rows * (N * sc + 20)), (40, 32, 56))
d = ImageDraw.Draw(pv)
big = sheet.resize((sheet.width * sc, sheet.height * sc), Image.NEAREST)
for i, n in enumerate(names):
    cx, cy = (i % cols), (i // cols)
    tile = big.crop((cx * N * sc, cy * N * sc, (cx + 1) * N * sc, (cy + 1) * N * sc))
    px, py = cx * (N * sc + 8) + 4, cy * (N * sc + 20) + 2
    pv.paste(tile, (px, py), tile)
    d.text((px, py + N * sc + 2), n[:11], fill=(220, 210, 240))
pv.save(os.path.join(ART, 'preview.png'))
print(len(names), 'sprites', sheet.size)
