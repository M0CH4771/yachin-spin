# 共有用の画像（ogp.png）を、元の絵（art/ogp/ogp_original.png）から作り直して、
# タイトルの上にシリーズ名「よいまつり横丁」を入れる
# 使い方：python3 tools/ogp_series.py
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ogp import pixel_text, p, W, H

SERIES = 'よいまつり横丁'
im = Image.open(p('art', 'ogp', 'ogp_original.png')).convert('RGB')
w, h = im.size; tw = round(h * W / H); x0 = (w - tw) // 2
im = im.crop((x0, 0, x0 + tw, h)).resize((W, H), Image.LANCZOS).convert('RGBA')
# 左右に小さな線をつけた「― よいまつり横丁 ―」
t = pixel_text(SERIES, 14, 3, (255, 214, 150), shadow=[(3, 3, (120, 30, 30)), (5, 5, (11, 8, 18))])
cx, top = 283, 82                       # タイトル「ヤチンスピン」の中央の上（夜空の部分）
x = cx - t.width // 2
im.alpha_composite(t, (x, top))
line_y = top + t.height // 2 - 4
for (a, b) in ((x - 46, x - 12), (x + t.width + 6, x + t.width + 40)):
    for dy, c in ((0, (255, 214, 150, 255)), (3, (120, 30, 30, 255))):
        im.alpha_composite(Image.new('RGBA', (b - a, 3), c), (a + (dy and 2), line_y + dy))
im.convert('RGB').save(p('ogp.png'), optimize=True)
print('ogp.png', os.path.getsize(p('ogp.png')) // 1024, 'KB')
