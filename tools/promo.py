# アップデート告知用の画像（1200x675、Xに4枚組で載せる）を作る
# 使い方：python3 tools/promo.py   → art/promo/ に書き出す
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ogp import pixel_text, p

W, H = 1200, 675
INK, GOLD, MUTE, EDGE, RED = (255, 226, 168), (242, 193, 78), (214, 204, 232), (11, 8, 18), (163, 47, 40)
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
font = lambda size: ImageFont.truetype(FONT, size, index=0)
sheet = Image.open(p('art', 'sheet.png')).convert('RGBA'); idx = json.load(open(p('art', 'sheet.json')))['idx']
cell = lambda k: sheet.crop(((idx[k] % 16) * 32, (idx[k] // 16) * 32, (idx[k] % 16) * 32 + 32, (idx[k] // 16) * 32 + 32))
OUT = p('art', 'promo')

def base():
    bg = Image.open(p('bg', 'festival.jpg')).convert('RGB')
    bg = bg.resize((W, round(bg.height * W / bg.width)), Image.LANCZOS)
    top = max(0, (bg.height - H) // 2)
    bg = bg.crop((0, top, W, top + H)).filter(ImageFilter.GaussianBlur(4))
    dark = Image.new('RGB', (W, H), (16, 11, 28))
    img = Image.blend(bg, dark, 0.72).convert('RGBA')
    for k in range(13):                                           # 上の提灯
        t = cell('lantern').resize((36, 36), Image.NEAREST); img.alpha_composite(t, (14 + k * 92, 10))
    return img

def header(img, title, sub=None, series=True):
    y = 58
    if series:
        s = pixel_text('― よいまつり横丁　ヤチンスピン ―', 10, 2, (255, 214, 150), [(2, 2, EDGE)]); img.alpha_composite(s, ((W - s.width) // 2, y)); y += s.height + 6
    t = pixel_text(title, 16, 3, INK, [(3, 3, RED), (6, 6, EDGE)]); img.alpha_composite(t, ((W - t.width) // 2, y)); y += t.height + 4
    if sub:
        u = pixel_text(sub, 10, 2, GOLD, [(2, 2, EDGE)]); img.alpha_composite(u, ((W - u.width) // 2, y)); y += u.height
    return y + 10

def tile(img, k, x, y, size, frame=True):
    if frame:
        d = ImageDraw.Draw(img)
        d.rectangle((x - 6, y - 6, x + size + 5, y + size + 5), fill=EDGE)
        d.rectangle((x - 3, y - 3, x + size + 2, y + size + 2), fill=(65, 52, 94))
        d.rectangle((x, y, x + size - 1, y + size - 1), fill=(35, 27, 54))
    t = cell(k).resize((size, size), Image.NEAREST); img.alpha_composite(t, (x, y))

def text(img, s, x, y, size, color, anchor='la', stroke=3):
    ImageDraw.Draw(img).text((x, y), s, font=font(size), fill=color, anchor=anchor, stroke_width=stroke, stroke_fill=EDGE)

def grid(img, items, top, cols, cw, ch, size, desc_w, nsize=24, dsize=19):
    x0 = (W - cols * cw) // 2
    for n, (k, name, desc) in enumerate(items):
        x, y = x0 + (n % cols) * cw, top + (n // cols) * ch
        tile(img, k, x, y, size)
        ns = nsize                                                   # 長い名前は枠に収まるまで縮める
        while ns > 14 and font(ns).getlength(name) > desc_w: ns -= 1
        text(img, name, x + size + 14, y, ns, INK)
        lines = []
        for part in desc.split('\n'):                               # \n で区切った所で改行（なければ幅で折り返す）
            cur = ''
            for ch_ in part:
                if font(dsize).getlength(cur + ch_) > desc_w: lines.append(cur); cur = ch_
                else: cur += ch_
            if cur: lines.append(cur)
        for i, ln in enumerate(lines[:3]): text(img, ln, x + size + 14, y + nsize + 10 + i * (dsize + 5), dsize, MUTE, stroke=2)

def footer(img):
    text(img, '#ヤチンスピン #よいまつり横丁　m0ch4771.github.io/yachin-spin', W - 24, H - 18, 18, (226, 216, 242), 'rs', 2)

# ---- 1枚目：表紙 ----
img = base()
y = header(img, 'アップデート Ver.1.3', None)
for i, (big, small) in enumerate((('100', 'シンボル'), ('60', 'お守り'))):
    cx = W // 2 + (-200 if i == 0 else 200)
    b = pixel_text(big, 22, 5, GOLD, [(4, 4, RED), (8, 8, EDGE)]); img.alpha_composite(b, (cx - b.width // 2, y + 20))
    s = pixel_text(small + 'に', 12, 3, INK, [(3, 3, EDGE)]); img.alpha_composite(s, (cx - s.width // 2, y + 30 + b.height))
row = ['yatai', 'kappa', 'daruma', 'shishi', 'kitsunebi', 'karakasa', 'kotatsu', 'bonodori', 'i_omikoshi', 'i_tamatebako', 'i_kumade']
size = 72; gap = 26; tot = len(row) * size + (len(row) - 1) * gap; x = (W - tot) // 2
for k in row: tile(img, k, x, 470, size); x += size + gap
c = pixel_text('コンボが育つ！　新しいシンボル14種・お守り15種', 11, 2, MUTE, [(2, 2, EDGE)]); img.alpha_composite(c, ((W - c.width) // 2, 580))
footer(img); img.convert('RGB').save(os.path.join(OUT, 'v13_1_cover.png'), optimize=True)

# ---- 2枚目：新しいシンボル ----
SYMS = [('yatai', 'やたい', 'となりの食べ物\n稼ぎ ×2'), ('kingyosukui', '金魚すくい', 'となりに金魚がいると\n手持ちに金魚をふやす'),
        ('bonodori', 'ぼんおどり', 'いちばん多い種類に\nその数だけ＋'), ('kappa', 'かっぱ', 'きゅうりを食べて\nずっと育つ'),
        ('kyuri', 'きゅうり', 'かっぱの大好物'), ('susuki', 'すすき', 'おつきさまがいると\nずっと育つ'),
        ('daruma', 'だるま', '縁起物の数だけ\nずっと育つ'), ('tamaya', 'たまや', 'はなびの数だけ\nずっと育つ'),
        ('mikan', 'みかん', 'こたつの相方'), ('kotatsu', 'こたつ', 'みかんとねこで\nずっと育つ'),
        ('shishi', 'ししまい', 'となりの縁起物\n稼ぎ ×3'), ('inari', 'いなりずし', 'きつねの大好物'),
        ('kitsunebi', 'きつねび', 'となりのきつね\n稼ぎ ×3'), ('karakasa', 'からかさおばけ', 'ようかいの数だけ\nずっと育つ')]
img = base(); y = header(img, 'あたらしいシンボル 14種', None)
grid(img, SYMS, y + 6, 4, 292, 124, 72, 190, 26, 19); footer(img)
img.convert('RGB').save(os.path.join(OUT, 'v13_2_symbols.png'), optimize=True)

# ---- 3枚目：新しいお守り ----
ITEMS = [('i_keito', 'けいと', 'ねこ・こたつ +3'), ('i_hyotan', 'ひょうたん', 'かっぱ +4'), ('i_aburaage', 'あぶらあげ', 'きつね・いなり\n+3'),
         ('i_hachimaki', 'はちまき', '縁起物 +2'), ('i_nukadoko', 'ぬかどこ', 'きゅうり・みかん\n+3'), ('i_chawan', 'ちゃわん', 'おにぎり・いなり\n・いなほ +2'),
         ('i_noren', 'のれん', 'やたいが ×3 に'), ('i_kingyobachi', 'きんぎょばち', '金魚 ×2'), ('i_bachi', 'たいこのばち', 'ぼんおどりが2倍'),
         ('i_emaki', 'ひゃっきやこう絵巻', 'ようかい +3'), ('i_kintsugi', 'きんつぎ', '消えた数だけ\nつぼが育つ'), ('i_fude', 'ふで', 'だるま ×2'),
         ('i_omikoshi', 'おみこし', 'いちばん多い\n種類 ×2'), ('i_tamatebako', 'たまてばこ', '育つシンボル\n全部 ×2'), ('i_kumade', 'くまで', '縁起物の数だけ\n稼ぎ ×')]
img = base(); y = header(img, 'あたらしいお守り 15種', None)
grid(img, ITEMS, y + 10, 5, 234, 128, 68, 146, 23, 18); footer(img)
img.convert('RGB').save(os.path.join(OUT, 'v13_3_items.png'), optimize=True)

# ---- 4枚目：コンボが育つ ----
img = base(); y = header(img, 'コンボが決まるたびに 育つ', None)
COMBOS = [(['tea', 'dango'], 'お茶 × だんご', 'だんごが育つ'), (['cat', 'goldfish'], 'ねこ × 金魚', '食べるたびに育つ'),
          (['kappa', 'kyuri'], 'かっぱ × きゅうり', '食べるたびに育つ'), (['kotatsu', 'mikan'], 'こたつ × みかん', 'こたつが育つ'),
          (['daruma', 'shishi'], 'だるま × ししまい', '縁起物の数だけ育つ'), (['susuki', 'moon'], 'すすき × おつきさま', '月夜に育つ')]
cols, cw, ch = 3, 390, 190; x0 = (W - cols * cw) // 2
for n, (ks, name, desc) in enumerate(COMBOS):
    x, yy = x0 + (n % cols) * cw + 10, y + 10 + (n // cols) * ch
    tile(img, ks[0], x + 40, yy, 88); text(img, '×', x + 158, yy + 44, 44, GOLD, 'mm'); tile(img, ks[1], x + 190, yy, 88)
    text(img, name, x + 164, yy + 112, 26, INK, 'ma'); text(img, desc, x + 164, yy + 146, 19, MUTE, 'ma', 2)
n1 = pixel_text('かたつむり・かざんだけじゃない。どのコンボでも後半まで戦える', 10, 2, GOLD, [(2, 2, EDGE)])
img.alpha_composite(n1, ((W - n1.width) // 2, 588)); footer(img)
img.convert('RGB').save(os.path.join(OUT, 'v13_4_combo.png'), optimize=True)
print('art/promo/ に4枚')
