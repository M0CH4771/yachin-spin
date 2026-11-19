# Ver.1.2 で増えたシンボルのドット絵（32x32 で直接描く）
import math
from pixel import S, N
from sprites import SP
from sprites_fix3 import rell, clear_if, paint_if, ering

def sp(name):
    def deco(fn): SP[name] = fn; return fn
    return deco

# やたい：紅白しまの屋根＋のれん＋木のカウンター
@sp('yatai')
def _():
    s = S(True)
    s.rect(4, 10, 6, 29, '#8a5a2a'); s.rect(25, 10, 27, 29, '#8a5a2a')          # 柱
    s.rect(3, 21, 28, 29, '#c08a4a')                                            # カウンター
    s.poly([(1, 10), (31, 10), (28, 3), (4, 3)], '#ffffff')                      # 屋根
    s.finish(ol='#2a1a10')
    for x in range(2, 31, 4): s.poly([(x, 10), (x + 2, 10), (x + 2 - (x - 16) * 0.12, 3), (x - (x - 16) * 0.12, 3)], '#e0303a')
    for x in range(2, 31, 4): s.disc(x + 1.5, 10.5, 1.5, '#e0303a' if (x // 4) % 2 == 0 else '#ffffff')
    s.rect(8, 12, 23, 17, '#2c4a8a')                                            # のれん
    for x in (11, 15, 19): s.rect(x, 14, x, 17, '#1a2a50')
    s.rect(14, 13, 16, 13, '#f2e8d0')
    s.rect(3, 21, 28, 22, '#e0b070'); s.line(4, 25, 27, 25, '#a87038')
    s.disc(10, 19.5, 1.8, '#f6a6bf'); s.disc(13, 19.5, 1.8, '#f7f2e6'); s.disc(16, 19.5, 1.8, '#8cc86a')   # だんご
    s.ell(22, 20, 3, 1.4, '#f4f4f4')                                             # 皿
    return s

# 金魚すくい：ポイ（紙を張った輪）にのった赤い金魚＋水
@sp('kingyosukui')
def _():
    s = S(True)
    s.ell(16, 24, 14, 6.5, '#3a7ad0')                                           # 水
    s.line(17, 15, 29, 4, '#d8c8a8', 3)                                         # 持ち手
    s.disc(11, 17, 8.5, '#f4f6ff')                                              # ポイ
    s.finish(ol='#16305a')
    s.ell(16, 24, 13, 5.5, '#3a7ad0'); s.line(4, 22, 9, 22, '#7aaaf0'); s.line(22, 27, 27, 27, '#7aaaf0')
    s.ring(11, 17, 8.5, 1.4, '#e0303a')                                         # ポイの枠
    s.disc(11, 17, 7, '#eef2ff')
    rell(s, 10.5, 17, 3.6, 2.2, -20, '#ff5a2a'); s.poly([(14, 15), (17, 13), (16.5, 18)], '#ff5a2a')   # 金魚
    s.px(9, 16, '#1a1418'); s.px(11, 16, '#ffd0a0')
    rell(s, 22, 25, 2.6, 1.5, 10, '#ff5a2a'); s.poly([(24, 25), (26.5, 23.5), (26.5, 26.5)], '#ff5a2a')
    return s

# ぼんおどり：紅白のやぐら＋屋根＋提灯のひも
@sp('bonodori')
def _():
    s = S(True)
    s.poly([(7, 30), (25, 30), (23, 17), (9, 17)], '#ffffff')                   # やぐら
    s.rect(6, 15, 26, 17, '#a8703a')                                            # 舞台
    s.rect(10, 9, 11, 15, '#a8703a'); s.rect(21, 9, 22, 15, '#a8703a')
    s.poly([(5, 10), (27, 10), (16, 3)], '#3e4a62')                             # 屋根
    s.finish(ol='#1e1420')
    for y in range(18, 30, 4): s.poly([(8.4 + (30 - y) * .13, y), (23.6 - (30 - y) * .13, y), (23.6 - (30 - y - 2) * .13, y + 2), (8.4 + (30 - y - 2) * .13, y + 2)], '#e0303a')
    s.rect(14, 11, 17, 14, '#c8302a'); s.rect(14, 11, 17, 11, '#f0c040')       # 太鼓
    for k in range(5):                                                         # 提灯のひも
        x = 1 + k * 1.2; y = 5 + k * 2.4; s.px(round(x + 2), round(y), '#c8b8a0')
    for (x, y) in ((2, 10), (4, 14), (28, 10), (30, 14)): s.rect(x - 1, y - 1, x, y + 1, '#ff5a3a'); s.px(x - 1, y - 1, '#ffd060')
    s.line(4, 8, 2, 10, '#c8b8a0'); s.line(28, 8, 30, 10, '#c8b8a0'); s.line(2, 11, 4, 13, '#c8b8a0'); s.line(30, 11, 28, 13, '#c8b8a0')
    return s

# きゅうり：ななめの緑のきゅうり＋いぼ＋黄色い花
@sp('kyuri')
def _():
    s = S(True)
    rell(s, 15, 17, 13.5, 4.4, -40, '#3e8e3a')
    s.finish(ol='#123a14')
    for (x, y) in ((8, 23), (12, 18), (16, 15), (20, 11), (11, 21), (18, 13), (14, 19), (22, 10)): s.px(x, y, '#7ac860')
    s.line(7, 21, 20, 9, '#5aac4a')
    s.rect(24, 5, 26, 6, '#2e6a24'); s.disc(27.5, 4, 2, '#ffd83a'); s.px(27, 4, '#ff9a20')   # へたと花
    return s

# かっぱ：緑の顔＋頭の白い皿＋黄色いくちばし
@sp('kappa')
def _():
    s = S(True)
    s.disc(16, 18, 11.5, '#5ab04a')
    s.finish(ol='#123a14')
    s.ell(16, 9.5, 11, 4.5, '#2e6a3a')                                          # 髪
    for x in range(6, 27, 3): s.poly([(x, 11), (x + 1.5, 15), (x + 3, 11)], '#2e6a3a')
    s.ell(16, 8, 7, 3, '#f6f8ff'); s.ell(16, 8, 5, 1.8, '#c8e0ff')               # 皿
    s.rect(10, 17, 12, 19, '#1a1418'); s.rect(20, 17, 22, 19, '#1a1418'); s.px(10, 17, '#ffffff'); s.px(20, 17, '#ffffff')
    s.ell(16, 23.5, 4.5, 2.6, '#ffd040'); s.line(12, 23.5, 20, 23.5, '#c08a10')   # くちばし
    s.ell(8.5, 21, 1.6, 1, '#7ad070'); s.ell(23.5, 21, 1.6, 1, '#7ad070')
    return s

# すすき：銀色の穂が垂れたすすきの束
@sp('susuki')
def _():
    s = S(True)
    for (x1, y1, a) in ((7, 5, -55), (15, 2, -80), (24, 4, -115)):
        s.line(16, 30, x1 + 2, y1 + 6, '#8a9a5a', 2)
        rell(s, x1, y1 + 5, 6, 2.6, a + 180 if a < -90 else a, '#efe2b8')
    s.line(16, 30, 4, 18, '#6a7a40'); s.line(16, 30, 28, 17, '#6a7a40')        # 葉
    s.finish(ol='#3a3418')
    for (x, y) in ((6, 7), (15, 5), (24, 7), (8, 9), (14, 9), (22, 9)): s.px(x, y, '#ffffff')
    return s

# だるま：赤い体＋白い顔＋太いまゆ＋片目だけ
@sp('daruma')
def _():
    s = S(True)
    s.ell(16, 17, 12.5, 13.5, '#d8283a')
    s.finish(ol='#3a0a10')
    s.ell(16, 13.5, 8, 6.5, '#fbf6ee')                                          # 顔
    s.line(9, 9, 13, 10, '#1a1418', 2); s.line(19, 10, 23, 9, '#1a1418', 2)     # まゆ
    s.disc(12, 13.5, 2.4, '#ffffff'); s.ring(12, 13.5, 2.4, 1, '#1a1418'); s.disc(12, 13.5, 1.1, '#1a1418')   # 入った目
    s.disc(20, 13.5, 2.4, '#ffffff'); s.ring(20, 13.5, 2.4, 1, '#1a1418')      # まだ白い目
    s.line(13, 18, 15, 17, '#1a1418'); s.line(17, 17, 19, 18, '#1a1418')       # ひげ
    s.ell(16, 25, 5.5, 3, '#f0c040'); s.line(14, 25, 18, 25, '#c8302a')        # おなかの金
    s.px(8, 8, '#ff8a90'); s.px(7, 9, '#ff8a90')
    return s

# たまや：花火の絵のうちわ
@sp('tamaya')
def _():
    s = S(True)
    s.line(16, 20, 16, 31, '#c8a070', 3)                                        # 持ち手
    s.disc(16, 12, 11.5, '#1e2a5a')
    s.finish(ol='#0e1430')
    for k in range(10):
        a = math.radians(k * 36); s.line(16 + 2 * math.cos(a), 12 + 2 * math.sin(a), 16 + 8 * math.cos(a), 12 + 8 * math.sin(a), '#ff9ad0' if k % 2 else '#ffd24a')
        s.px(round(16 + 9 * math.cos(a)), round(12 + 9 * math.sin(a)), '#ffffff')
    s.disc(16, 12, 1.6, '#fff6c8')
    s.ring(16, 12, 11.5, 1, '#e8e0f0')
    return s

# みかん：オレンジの丸＋葉っぱ
@sp('mikan')
def _():
    s = S(True)
    s.ell(16, 18, 12.5, 11, '#ff9a20')
    rell(s, 21, 5, 4.5, 2, -25, '#4aa040')
    s.finish(ol='#5a2a08')
    s.rect(15, 7, 17, 8, '#4a6a20')
    for (x, y) in ((9, 15), (12, 22), (20, 24), (24, 17), (18, 12), (14, 18)): s.px(x, y, '#e07a10')
    s.px(9, 12, '#ffd080'); s.px(10, 11, '#ffd080'); s.px(8, 13, '#ffd080')
    s.line(19, 4, 24, 6, '#2e7a2a')
    return s

# こたつ：天板＋もようのふとん＋上のみかん
@sp('kotatsu')
def _():
    s = S(True)
    s.poly([(2, 30), (30, 30), (28, 15), (4, 15)], '#d84a3a')                   # ふとん
    s.poly([(3, 15), (29, 15), (26, 9), (6, 9)], '#a86a3a')                     # 天板
    s.disc(16, 7, 3.6, '#ff9a20'); s.disc(10.5, 9, 2.6, '#ff9a20')              # みかん
    s.finish(ol='#2a1008')
    for (x, y) in ((7, 20), (13, 19), (19, 20), (25, 19), (10, 25), (16, 25), (22, 25)):   # ふとんのもよう
        s.disc(x, y, 1.6, '#f6c050'); s.px(x, y, '#ffffff')
    s.line(5, 15, 27, 15, '#6a3a1a'); s.line(7, 11, 25, 11, '#c88a50')
    s.px(16, 3, '#4aa040'); s.px(15, 5, '#ffd080')
    return s

# ししまい：赤い獅子の頭（大きな口と歯）＋緑の唐草の布
@sp('shishi')
def _():
    s = S(True)
    s.poly([(4, 18), (28, 18), (31, 31), (1, 31)], '#2e8a4a')                   # 唐草の布
    s.ell(16, 13, 12, 10, '#d8283a')                                            # 頭
    s.finish(ol='#2a0a0a')
    for (x, y) in ((5, 24), (11, 27), (20, 25), (26, 28), (15, 30)): s.ring(x, y, 1.6, 1, '#f4f4f4')
    s.ell(16, 13, 12, 10, '#d8283a')
    s.line(6, 6, 12, 8, '#1a1418', 2); s.line(20, 8, 26, 6, '#1a1418', 2)       # まゆ
    s.disc(11, 10.5, 2.4, '#ffd040'); s.disc(21, 10.5, 2.4, '#ffd040'); s.px(11, 10, '#1a1418'); s.px(21, 10, '#1a1418')
    s.ell(16, 18, 7.5, 4, '#5a0a10')                                            # 口
    for x in range(10, 23, 3): s.rect(x, 15, x + 1, 16, '#ffffff'); s.rect(x, 20, x + 1, 21, '#ffffff')
    s.rect(14, 5, 18, 7, '#f0c040')                                             # 金の飾り
    return s

# いなりずし：きつね色の油あげ2つ
@sp('inari')
def _():
    s = S(True)
    for (cx, cy, a) in ((11, 19, -12), (21, 15, 10)):
        rell(s, cx, cy, 9, 6.2, a, '#d8963a')
    s.finish(ol='#4a2408')
    for (cx, cy, a) in ((21, 15, 10),):
        rell(s, cx, cy, 8, 5.2, a, '#e0a24a')
    for (x, y) in ((7, 18), (10, 22), (14, 20), (18, 13), (22, 17), (25, 14), (12, 17)): s.px(x, y, '#b0702a')
    s.line(8, 15, 13, 14, '#f6c87a'); s.line(18, 11, 23, 11, '#f6c87a')
    return s

# きつねび：青白い炎が3つ
@sp('kitsunebi')
def _():
    s = S(True)
    def flame(cx, cy, r):
        s.disc(cx, cy, r, '#5ab8ff'); s.poly([(cx - r * .9, cy - r * .3), (cx + r * .1, cy - r * 2.6), (cx + r * .9, cy - r * .3)], '#5ab8ff')
    flame(16, 20, 6.5); flame(7, 12, 4); flame(25, 11, 4)
    s.finish(ol='#0e2a50')
    for (cx, cy, r) in ((16, 21, 3.4), (7, 12.6, 2), (25, 11.6, 2)):
        s.disc(cx, cy, r, '#d8f4ff'); s.disc(cx, cy + r * .3, r * .5, '#ffffff')
    return s

# からかさおばけ：一つ目＋長い舌＋一本足のげた
@sp('karakasa')
def _():
    s = S(True)
    s.poly([(2, 17), (16, 2), (30, 17)], '#8a4ab8')                             # かさ
    s.line(16, 17, 16, 27, '#c8a070', 2)                                        # 足
    s.rect(11, 28, 21, 29, '#8a5a2a'); s.rect(12, 30, 13, 31, '#5a3a1a'); s.rect(19, 30, 20, 31, '#5a3a1a')   # げた
    s.finish(ol='#1e0e30')
    for x in (6, 11, 21, 26): s.line(16, 3, x, 16, '#6a3098')                   # 骨
    s.ell(16, 10.5, 4, 3.2, '#ffffff'); s.disc(16, 10.5, 1.8, '#1a1418'); s.px(15, 10, '#ffffff')   # 一つ目
    s.poly([(14, 15), (18, 15), (19, 22), (16, 24), (14, 21)], '#e8405a'); s.line(16, 16, 16, 22, '#b02a40')   # 舌
    return s

# ---- 描き直し（上の定義より後ろが優先される） ----
# いなりずし：ふっくらした油あげ（口からごはんとごま）を2つ
@sp('inari')
def _():
    s = S(True)
    for (x0, y0, x1, y1) in ((3, 13, 17, 28), (15, 8, 29, 23)):
        s.poly([(x0, y0 + 3), (x1 - 3, y0), (x1, y1 - 3), (x0 + 3, y1)], '#c8802a')
    s.finish(ol='#3a1a04')
    s.poly([(15, 11), (26, 8), (29, 20), (18, 23)], '#d8963a')
    for (x, y) in ((6, 18), (9, 24), (13, 21), (19, 14), (23, 19), (25, 13), (20, 18), (11, 16)): s.px(x, y, '#a0601a')
    s.ell(22, 9.5, 5, 2.2, '#fbf8f0'); s.px(20, 9, '#1a1418'); s.px(23, 10, '#1a1418'); s.px(25, 9, '#1a1418')   # ごはんとごま
    s.line(5, 15, 11, 14, '#f0b866'); s.line(17, 12, 23, 12, '#f0b866')
    return s

# きつねび：しっぽがゆらぐ青白い火の玉が3つ
@sp('kitsunebi')
def _():
    s = S(True)
    def onibi(cx, cy, r, side):
        s.disc(cx, cy, r, '#4aa8ff')
        for k in range(8):                                                      # 上にのびて横にゆらぐしっぽ
            t = k / 7; x = cx + side * (math.sin(t * 3.0) * r * .9); y = cy - r * .4 - t * r * 2.4
            s.disc(x, y, r * (0.75 - t * 0.6), '#4aa8ff')
    onibi(15, 22, 6.2, 1); onibi(6, 13, 3.6, -1); onibi(26, 12, 3.6, 1)
    s.finish(ol='#0e2050')
    for (cx, cy, r) in ((15, 22.6, 3.6), (6, 13.4, 2), (26, 12.4, 2)):
        s.disc(cx, cy, r, '#cdeeff'); s.disc(cx - r * .3, cy + r * .2, r * .45, '#ffffff')
    return s

# いなりずし（もう一度）：皿の上に、つやのある丸い油あげの袋が2つ
@sp('inari')
def _():
    s = S(True)
    s.ell(16, 25, 15, 5, '#f4f4f8')                                             # 皿
    rell(s, 10, 18, 8, 5.6, -8, '#b8701e'); rell(s, 22, 16, 8, 5.6, 8, '#b8701e')
    s.finish(ol='#2a1204')
    s.ell(16, 26, 13, 3, '#dde4f0'); s.line(4, 25, 7, 27, '#6a8ae0'); s.line(25, 27, 28, 25, '#6a8ae0')   # 皿のもよう
    rell(s, 10, 18, 8, 5.6, -8, '#b8701e'); rell(s, 22, 16, 8, 5.6, 8, '#c88028')
    for (x, y) in ((6, 18), (9, 21), (13, 17), (18, 15), (22, 19), (26, 16), (21, 13), (11, 15)): s.px(x, y, '#8a4a10')
    s.line(5, 15, 10, 13, '#f0b060'); s.line(18, 12, 24, 11, '#f0b060')           # つや
    s.rect(28, 11, 29, 12, '#f6b8c8'); s.rect(29, 13, 30, 14, '#f6b8c8')           # ガリ
    return s

# いなりずし（三角）：皿の上に三角いなり2つ
@sp('inari')
def _():
    s = S(True)
    s.ell(16, 26, 15, 4.5, '#f4f4f8')                                           # 皿
    s.poly([(2, 24), (11, 7), (19, 24)], '#c07a22'); s.poly([(13, 24), (21, 7), (30, 24)], '#c88428')
    s.finish(ol='#2a1204')
    s.ell(16, 27, 13, 2.6, '#dde4f0'); s.line(4, 26, 7, 28, '#6a8ae0'); s.line(25, 28, 28, 26, '#6a8ae0')
    s.poly([(13, 24), (21, 7), (30, 24)], '#d08c2c')
    for (x, y) in ((7, 19), (10, 14), (13, 20), (19, 15), (22, 20), (25, 18), (9, 22), (21, 11)): s.px(x, y, '#8a4a10')
    s.line(8, 15, 10, 11, '#f6c070'); s.line(19, 14, 20, 11, '#f6c070')
    s.line(4, 22, 17, 22, '#a0601a'); s.line(15, 22, 28, 22, '#a8681e')        # 油あげのしわ
    return s
