# 日本人がぱっと見てわかるように描き直したスプライト（第3弾）。32x32 で直接描く
import math
from pixel import S, N, dark, light
from sprites import SP

def sp(name):
    def deco(fn): SP[name] = fn; return fn
    return deco

def rell(s, cx, cy, rx, ry, ang, c):
    """回転した楕円（ang は度）"""
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    for X, Y, x, y in s._each():
        dx, dy = x - cx, y - cy
        u = dx * ca + dy * sa; v = -dx * sa + dy * ca
        if (u / rx) ** 2 + (v / ry) ** 2 <= 1: s._set(X, Y, c, False)

def clear_if(s, fn):
    for Y in range(N):
        for X in range(N):
            if fn(X + .5, Y + .5): s.g[Y][X] = None

def paint_if(s, fn, c):
    for Y in range(N):
        for X in range(N):
            if s.g[Y][X] is not None and fn(X + .5, Y + .5): s.g[Y][X] = c

# ================= 第1束 =================

# すいか：三角に切った大きいひと切れ
@sp('suika')
def _():
    s = S(True)
    yb = lambda x: 20 + 8 * math.sqrt(max(0, 1 - ((x - 16) / 14) ** 2))
    inside = lambda x, y: y <= yb(x) and y >= 2 + abs(x - 16) * 18 / 14 and abs(x - 16) <= 14
    for X, Y, x, y in s._each():
        if inside(x, y): s._set(X, Y, '#ec3a4c', False)
    s.finish(shade=False)
    paint_if(s, lambda x, y: inside(x, y) and y > yb(x) - 2.2, '#2f8a3a')
    paint_if(s, lambda x, y: inside(x, y) and yb(x) - 3.4 < y <= yb(x) - 2.2, '#cfeec0')
    paint_if(s, lambda x, y: inside(x, y) and y > yb(x) - 1.1 and int(x) % 4 == 0, '#1f6a2a')   # しま
    for x, y in ((16, 9), (13, 14), (19, 14), (10, 19), (16, 19), (22, 19)):  # たね
        s.px(x, y, '#1a1418'); s.px(x, y + 1, '#1a1418')
    s.px(15, 6, '#ff8a96'); s.px(14, 8, '#ff8a96')
    return s

# だんご：大きめの三色だんご（上からピンク・白・緑）
@sp('dango')
def _():
    s = S(True)
    s.line(27, 2, 5, 30, '#c8a070', 2)
    for (cx, cy, c) in ((21, 9, '#f6a6bf'), (16, 16, '#f7f2e6'), (11, 23, '#8cc86a')):
        s.disc(cx, cy, 5.6, c)
    s.finish()
    s.line(7, 27, 5, 30, '#c8a070', 2)
    for (cx, cy) in ((21, 9), (16, 16), (11, 23)):
        s.px(cx - 2, cy - 3, '#ffffff'); s.px(cx - 3, cy - 2, '#ffffff')
    return s

# はなび：丸く開いた打ち上げ花火（太めの点で）
@sp('firework')
def _():
    s = S(True)
    for k in range(12):
        a = math.radians(k * 30 + 15)
        for r, c in ((5, '#ffe27a'), (8.5, '#ffb03a'), (12, '#ff5a8a'), (14.6, '#ff9ad0')):
            x, y = 16 + r * math.cos(a), 16 + r * math.sin(a)
            sz = 1 if r < 6 or r > 14 else 2
            s.rect(round(x - sz / 2), round(y - sz / 2), round(x - sz / 2) + sz - 1, round(y - sz / 2) + sz - 1, c)
    s.disc(16, 16, 2.2, '#fff6c8')
    return s

# サイコロ：立体で、上の面に赤い「一」
@sp('dice')
def _():
    s = S(True)
    s.poly([(16, 2), (30, 9), (16, 16), (2, 9)], '#ffffff')
    s.poly([(2, 9), (16, 16), (16, 30), (2, 23)], '#e4dfec')
    s.poly([(16, 16), (30, 9), (30, 23), (16, 30)], '#c2bad2')
    s.finish(shade=False, ol='#2a2236')
    s.ell(16, 9, 4, 2.2, '#e0283a'); s.px(14, 8, '#ff8a90')
    for (x, y) in ((6, 15), (12, 24)): s.ell(x, y, 1.3, 1.7, '#2a2236')
    for (x, y) in ((20, 25), (23, 19.5), (26, 14)): s.ell(x, y, 1.3, 1.7, '#2a2236')
    return s

# さくら：花びらの先に切れこみのある五弁
@sp('sakura')
def _():
    s = S(True)
    for k in range(5):
        a = -90 + 72 * k; r = math.radians(a)
        rell(s, 16 + 7.4 * math.cos(r), 16.5 + 7.4 * math.sin(r), 6.6, 5.0, a, '#f9b8cc')
    for k in range(5):                                                         # 切れこみ
        r = math.radians(-90 + 72 * k); ux, uy = math.cos(r), math.sin(r)
        tip = (16 + 14.4 * ux, 16.5 + 14.4 * uy)
        clear_if(s, lambda x, y, ux=ux, uy=uy, tip=tip: (lambda d, p: d > 10.8 and abs(p) < (d - 10.8) * 0.75)(
            (x - 16) * ux + (y - 16.5) * uy, -(x - 16) * uy + (y - 16.5) * ux))
    s.finish(ol='#8a2a4a')
    s.disc(16, 16.5, 3.4, '#f47a9a'); s.disc(16, 16.5, 1.6, '#ffe070')
    for k in range(5):
        r = math.radians(-54 + 72 * k); s.px(round(16 + 4.6 * math.cos(r)), round(16.5 + 4.6 * math.sin(r)), '#e85a84')
    return s

# おさけ：とっくり＋おちょこ
@sp('sake')
def _():
    s = S(True)
    s.ell(12, 21, 8, 8.5, '#f4eee2'); s.rect(9, 5, 14, 14, '#f4eee2'); s.ell(11.5, 5, 3.6, 1.6, '#f4eee2')
    s.poly([(19, 21), (30, 21), (28, 29), (21, 29)], '#f4eee2')
    s.finish(ol='#2a2236')
    s.rect(5, 15, 19, 17, '#2c4f9a'); s.rect(4, 18, 20, 18, '#2c4f9a')        # 藍の帯
    s.px(7, 22, '#ffffff'); s.px(7, 23, '#ffffff'); s.px(10, 7, '#ffffff')
    s.ell(11.5, 5, 2.2, .8, '#8a7a6a')                                          # 口
    s.rect(20, 21, 29, 22, '#2c4f9a'); s.rect(21, 23, 28, 23, '#f2e4b0')        # おちょこの縁と酒
    return s

# ひよこ：まるい体＋くちばし＋足
@sp('chick')
def _():
    s = S(True)
    s.ell(16, 17, 11.5, 11, '#ffd83a')
    s.poly([(14, 6), (16, 2), (17, 6)], '#ffd83a'); s.poly([(17, 6), (20, 3), (19, 7)], '#ffd83a')   # 頭の毛
    s.rect(11, 28, 12, 30, '#f08a2a'); s.rect(20, 28, 21, 30, '#f08a2a'); s.rect(9, 30, 13, 30, '#f08a2a'); s.rect(19, 30, 23, 30, '#f08a2a')
    s.finish(ol='#5a3a10')
    s.ell(5.5, 19, 2, 4, '#f2b820'); s.ell(26.5, 19, 2, 4, '#f2b820')           # 羽
    s.rect(11, 14, 12, 16, '#1a1418'); s.rect(20, 14, 21, 16, '#1a1418')       # 目
    s.px(11, 14, '#ffffff'); s.px(20, 14, '#ffffff')
    s.poly([(14, 18), (18, 18), (16, 21)], '#f07a20')                           # くちばし
    s.ell(9, 19, 1.6, 1, '#ff9a8a'); s.ell(23, 19, 1.6, 1, '#ff9a8a')
    return s

# おばけ：三角の頭巾＋足のかわりにしっぽ＋だらんとした手
@sp('ghost')
def _():
    s = S(True)
    s.disc(15, 12, 10, '#f2f4ff')
    s.poly([(5, 12), (25, 12), (25, 19), (21, 25), (27, 30), (15, 28), (8, 22)], '#f2f4ff')
    s.poly([(2, 18), (7, 16), (8, 19), (4, 21)], '#f2f4ff')                     # 手
    s.finish(ol='#3a3460')
    s.poly([(9.5, 2.5), (20.5, 2.5), (15, 10)], '#ffffff')                     # 三角の頭巾
    s.line(10, 2, 15, 9, '#6a6698'); s.line(20, 2, 15, 9, '#6a6698'); s.line(10, 2, 20, 2, '#6a6698')
    s.line(9, 12, 12, 13, '#2a2448'); s.line(18, 13, 21, 12, '#2a2448')         # うらめしそうな目
    s.ell(15, 17.5, 1.6, 2, '#2a2448')
    s.px(23, 9, '#c8ccf0'); s.px(23, 14, '#c8ccf0'); s.px(22, 21, '#c8ccf0')
    return s

# ================= 第2束 =================

# おしろ：石垣＋白壁＋三段の屋根＋金のしゃちほこ
@sp('castle')
def _():
    s = S(True)
    s.poly([(3, 30.5), (29, 30.5), (25.5, 22.5), (6.5, 22.5)], '#8c8a98')       # 石垣
    s.rect(8, 18, 24, 22, '#f6f4ee'); s.poly([(3, 18.5), (29, 18.5), (25, 14.5), (7, 14.5)], '#3e4a62')
    s.rect(10, 11, 22, 14, '#f6f4ee'); s.poly([(6, 12), (26, 12), (22, 8.5), (10, 8.5)], '#3e4a62')
    s.rect(12, 6, 20, 8, '#f6f4ee'); s.poly([(9, 7), (23, 7), (16, 2)], '#3e4a62')
    s.finish(ol='#1e2230')
    for y in (25, 28): s.line(7, y, 25, y, '#6a6878')                           # 石垣の目地
    for x in (10, 15, 20): s.px(x, 24, '#6a6878'); s.px(x + 2, 27, '#6a6878'); s.px(x - 1, 30, '#6a6878')
    for x in (10, 14, 18, 22): s.rect(x, 19, x + 1, 20, '#2a2a3a')             # 窓
    for x in (13, 18): s.rect(x, 12, x + 1, 13, '#2a2a3a')
    s.rect(15, 18, 17, 22, '#5a3a2a')                                          # 門
    s.rect(4, 17, 5, 17, '#f0c040'); s.rect(27, 17, 28, 17, '#f0c040')
    s.px(9, 6, '#f0c040'); s.px(23, 6, '#f0c040'); s.px(16, 1, '#f0c040')       # しゃちほこ
    return s

# りゅう：横顔＋角＋長いひげ＋くねった胴
@sp('dragon')
def _():
    s = S(True)
    path = [(19, 10), (23, 12), (26, 15), (25, 19), (21, 21), (16, 22), (12, 24), (11, 27), (14, 29), (19, 29), (23, 28)]
    for i, (x, y) in enumerate(path):
        s.disc(x, y, 3.6 - i * 0.15, '#3aa860')
    s.ell(11, 9, 6, 4.4, '#3aa860'); s.rect(3, 8, 9, 12, '#3aa860')            # 頭と鼻先
    s.finish(ol='#123a20')
    for (x, y) in ((21, 8), (26, 11), (28, 16), (26, 21), (20, 24), (14, 26), (9, 26)):   # 背びれ
        s.px(x, y, '#f08a2a')
    for (x, y) in ((22, 14), (17, 20), (13, 23), (15, 27), (20, 27)):          # 腹のうろこ
        s.px(x, y, '#c8e890')
    s.rect(4, 11, 8, 11, '#123a20')                                            # 口
    s.rect(11, 7, 12, 8, '#ffd040'); s.px(12, 8, '#1a1418')                    # 目
    s.line(14, 5, 18, 1, '#e8d6a0'); s.line(12, 5, 13, 1, '#e8d6a0'); s.px(17, 3, '#e8d6a0')   # 角
    s.line(3, 12, 1, 17, '#f6e4a0'); s.line(1, 17, 3, 21, '#f6e4a0')           # ひげ
    s.line(4, 8, 2, 4, '#f6e4a0'); s.line(2, 4, 4, 1, '#f6e4a0')
    s.rect(15, 6, 16, 11, '#f08a2a'); s.px(17, 7, '#f08a2a')                   # たてがみ
    return s

# やきいも：細長いいもを割って、黄色い中身を見せる
@sp('yakiimo')
def _():
    s = S(True)
    rell(s, 9.5, 21.5, 8.5, 5.2, -40, '#9a2e5a')
    rell(s, 22.5, 11, 8.5, 5.2, -40, '#9a2e5a')
    s.finish(ol='#3a1024')
    rell(s, 13.6, 17.4, 2.2, 4.4, -40, '#ffd24a'); rell(s, 18.4, 14.6, 2.2, 4.4, -40, '#ffd24a')   # 割れ目の中身
    s.px(6, 20, '#c85a88'); s.px(19, 9, '#c85a88'); s.px(8, 18, '#c85a88')
    s.line(25, 4, 24, 1, '#eef2f6'); s.line(28, 6, 29, 2, '#eef2f6')           # 湯気
    return s

# たいこ：胴の長い和太鼓（上の面に三つ巴、上下に鋲）＋右にばち
@sp('taiko')
def _():
    s = S(True)
    s.ell(14, 25, 11, 4.5, '#a8402a'); s.rect(3, 10, 25, 25, '#a8402a'); s.ell(14, 18, 12, 5, '#a8402a')
    s.ell(14, 10, 11, 4.5, '#f3e7c8')
    s.line(22, 2, 30, 26, '#e6c890', 2); s.line(27, 1, 30, 22, '#e6c890', 2)     # ばち
    s.finish(ol='#3a140c')
    s.ell(14, 10, 10, 3.6, '#f6ecd2')
    s.disc(14, 10, 2.4, '#c8302a'); s.px(11, 9, '#c8302a'); s.px(17, 11, '#c8302a'); s.px(14, 8, '#c8302a')   # 巴もよう
    for x in range(4, 25, 3): s.px(x, 14 if 7 < x < 21 else 13, '#2a1810'); s.px(x, 25 if 7 < x < 21 else 24, '#2a1810')   # 鋲
    s.line(5, 19, 23, 19, '#c8603a'); s.line(6, 20, 22, 20, '#8a2e18')           # 胴のふくらみ
    return s

# ちょきんばこ：ぶたの貯金箱＋背中の口＋入っていく小銭
@sp('piggy')
def _():
    s = S(True)
    s.ell(15, 19, 12, 8.5, '#f7a8bb')
    s.ell(27, 19, 3.2, 3.6, '#f28aa4')
    s.poly([(19, 13), (21, 7), (24, 13)], '#f7a8bb'); s.poly([(9, 13), (11, 8), (14, 12)], '#f7a8bb')
    for x in (7, 12, 18, 23): s.rect(x, 26, x + 2, 29, '#f7a8bb')
    s.finish(ol='#6a2a40')
    s.px(26, 18, '#8a3050'); s.px(28, 18, '#8a3050')                           # 鼻の穴
    s.rect(22, 15, 22, 16, '#1a1418')                                          # 目
    s.line(2, 17, 1, 14, '#e888a0'); s.px(2, 13, '#e888a0')                     # しっぽ
    s.rect(11, 11, 16, 11, '#5a1a30')                                          # 貯金の口
    s.ell(13.5, 5, 1.8, 3.4, '#f2c03a'); s.line(13, 3, 13, 6, '#fff0a0')        # 小銭
    s.px(19, 21, '#ffd0dc'); s.px(10, 16, '#ffd0dc')
    return s

# いぬ：柴犬（立った三角耳・白いほお・まろ眉）
@sp('dog')
def _():
    s = S(True)
    s.poly([(5, 3), (13, 9), (5, 13)], '#e0943a'); s.poly([(27, 3), (19, 9), (27, 13)], '#e0943a')
    s.ell(16, 18, 11.5, 10, '#e0943a')
    s.finish(ol='#4a2a10')
    s.poly([(7, 6), (11, 9), (7, 11)], '#f6d6b0'); s.poly([(25, 6), (21, 9), (25, 11)], '#f6d6b0')
    s.ell(16, 23, 8, 5.2, '#fbf1e0'); s.ell(8, 21, 3, 3, '#fbf1e0'); s.ell(24, 21, 3, 3, '#fbf1e0')
    s.ell(11, 13.2, 1.6, 1, '#fbf1e0'); s.ell(21, 13.2, 1.6, 1, '#fbf1e0')        # まろ眉
    s.rect(10, 16, 11, 17, '#1a1418'); s.rect(21, 16, 22, 17, '#1a1418')
    s.ell(16, 20.5, 2, 1.4, '#1a1418')
    s.line(16, 22, 16, 23, '#7a4a2a'); s.line(14, 24, 16, 23, '#7a4a2a'); s.line(18, 24, 16, 23, '#7a4a2a')
    return s

# ふじさん：右上の赤い点（ずれて見えた）を消す
_fuji_old = SP['fuji']
@sp('fuji')
def _():
    s = _fuji_old()
    for Y in range(0, 11):
        for X in range(23, 32): s.g[Y][X] = None
    return s

# まめ：木の枡に、まるい大豆を山もりに
@sp('mame')
def _():
    s = S(True)
    s.poly([(3, 15), (29, 15), (27, 30), (5, 30)], '#d8b27a')
    s.finish(ol='#4a3418')
    s.rect(4, 15, 28, 17, '#b88c50'); s.line(6, 23, 26, 23, '#c49a60')
    for (x, y) in ((7, 13), (13, 13), (19, 13), (25, 13), (10, 8), (16, 8), (22, 8), (13, 3.5), (19, 3.5)):
        s.disc(x, y, 3.3, '#7a5424'); s.disc(x, y, 2.6, '#f0d08a'); s.px(int(x) - 1, int(y) - 1, '#fff4d0'); s.px(int(x) + 1, int(y) + 1, '#d8b060')
    return s

# ================= 第3束 =================

# こりゅう：たまごの殻から顔を出した子どもの竜（殻のかけらを帽子に）
@sp('koryu')
def _():
    s = S(True)
    s.disc(16, 13, 8.5, '#5ec0e6')
    s.ell(16, 23, 10.5, 8, '#f6f2e6')
    s.finish(ol='#1a3a50')
    s.ell(16, 23, 10.5, 8, '#f6f2e6')
    for k, x in enumerate(range(6, 27, 3)):                                    # 割れた殻のギザギザ
        s.poly([(x, 18), (x + 1.5, 15.5 if k % 2 == 0 else 16.5), (x + 3, 18)], '#f6f2e6')
    s.line(6, 18, 26, 18, '#c8c0b0'); s.px(9, 24, '#e0d8c8'); s.px(22, 27, '#e0d8c8'); s.px(14, 28, '#e0d8c8')
    s.poly([(10, 6), (16, 2), (22, 6), (19, 7), (16, 5), (13, 7)], '#f6f2e6')  # 頭にのった殻
    s.line(10, 6, 13, 7, '#8a8070'); s.line(22, 6, 19, 7, '#8a8070')
    s.px(9, 7, '#f0c040'); s.px(23, 7, '#f0c040'); s.px(8, 6, '#f0c040'); s.px(24, 6, '#f0c040')   # 角
    s.rect(11, 11, 13, 13, '#1a1418'); s.rect(19, 11, 21, 13, '#1a1418'); s.px(11, 11, '#ffffff'); s.px(19, 11, '#ffffff')
    s.px(14, 15, '#2a6a90'); s.px(18, 15, '#2a6a90'); s.line(14, 16, 18, 16, '#2a6a90')
    s.rect(6, 17, 8, 18, '#5ec0e6'); s.rect(24, 17, 26, 18, '#5ec0e6')         # 殻にかけた手
    return s

# はなまる：答案用紙に赤ペンで書いた「花丸」
@sp('hanamaru')
def _():
    s = S(True)
    s.rect(3, 2, 28, 29, '#fbf8ee')
    s.finish(ol='#3a3448')
    s.poly([(22, 2), (28, 2), (28, 8)], '#e4dccc')                              # 紙の角
    for y in (24, 27): s.line(6, y, 25, y, '#c8d4e8')                          # 罫線
    R = '#e02a36'
    for k in range(8):
        a = math.radians(k * 45 + 22.5)
        s.ring(15.5 + 8.2 * math.cos(a), 14 + 8.2 * math.sin(a), 3.3, 1.2, R)
    clear_tmp = [(X, Y) for Y in range(N) for X in range(N) if s.g[Y][X] == R and math.hypot(X + .5 - 15.5, Y + .5 - 14) < 6.6]
    for X, Y in clear_tmp: s.g[Y][X] = '#fbf8ee'
    s.ring(15.5, 14, 6.4, 1.2, R); s.ring(15.5, 14, 3.4, 1.2, R); s.disc(15.5, 14, .9, R)
    return s

# にほんれっとう：海の丸の中に日本の島々
@sp('japan')
def _():
    s = S(True)
    s.disc(16, 16, 14.5, '#3a7ad0')
    s.finish(ol='#16305a')
    s.disc(16, 16, 13.5, '#3a7ad0'); s.px(7, 8, '#7aaaf0'); s.px(8, 7, '#7aaaf0')
    g = '#7ad850'
    s.poly([(19, 3), (24, 3), (27, 6), (25, 9), (21, 9), (19, 6)], g)           # 北海道
    for (x0, y0, x1, y1) in ((21, 11, 22, 15), (22, 15, 20, 19), (20, 19, 16, 21), (16, 21, 12, 22), (12, 22, 9, 24)):
        s.line(x0, y0, x1, y1, g, 3)                                           # 本州
    s.ell(13.5, 25.5, 2.4, 1.2, g)                                             # 四国
    s.ell(7, 27, 2.2, 2.8, g)                                                  # 九州
    s.px(3, 29, g)
    paint_if(s, lambda x, y: False, g)
    return s

# たこ：赤いたこ＋ねじりはちまき＋とがった口
@sp('octopus')
def _():
    s = S(True)
    s.ell(15, 11, 9.5, 9, '#e8443a')
    for x0, x1, x2 in ((8, 5, 3), (11, 9, 8), (14, 14, 12), (17, 18, 20), (20, 23, 25), (22, 26, 29)):
        s.line(x0, 18, x1, 25, '#e8443a', 2); s.line(x1, 25, x2, 28, '#e8443a', 2)
    s.ell(25, 14, 2.6, 2.2, '#e8443a')
    s.finish(ol='#5a1410')
    s.ell(25, 14, 1.2, 1, '#8a1a14')                                           # 口
    s.rect(6, 5, 24, 7, '#ffffff'); s.line(6, 6, 24, 6, '#d8d8e0')            # はちまき
    s.poly([(24, 4), (29, 2), (28, 6), (25, 7)], '#ffffff'); s.poly([(24, 7), (29, 9), (27, 10)], '#ffffff')
    s.rect(10, 11, 11, 13, '#1a1418'); s.rect(17, 11, 18, 13, '#1a1418')       # 目
    s.px(10, 11, '#ffffff'); s.px(17, 11, '#ffffff')
    s.px(9, 15, '#ff8a80'); s.px(19, 15, '#ff8a80')
    for (x, y) in ((5, 23), (9, 22), (13, 23), (19, 23), (23, 23), (27, 25)): s.px(x, y, '#ffb0a0')   # 吸盤
    return s

# おおなみ：北斎ふうの巻きこむ大波＋白いしぶき
@sp('wave')
def _():
    s = S(True)
    s.disc(17, 14, 12, '#2a5ab0')
    clear_if(s, lambda x, y: math.hypot(x - 13.5, y - 17) < 6.4)
    clear_if(s, lambda x, y: x < 13.5 and y > 17)
    s.rect(2, 23, 30, 30, '#2a5ab0')
    s.finish(ol='#0e2050')
    def crest(x, y):
        a = math.degrees(math.atan2(y - 14, x - 17)) % 360; r = math.hypot(x - 17, y - 14)
        return 10 <= r <= 12.2 and (a >= 170 or a <= 10)
    paint_if(s, crest, '#f4f8ff')
    for (x, y) in ((5, 12), (4, 15), (6, 16), (7, 19), (9, 18)): s.px(x, y, '#f4f8ff')   # しぶきの指
    paint_if(s, lambda x, y: 7.2 < math.hypot(x - 13.5, y - 17) < 8.3 and y < 17, '#6a9ae0')
    paint_if(s, lambda x, y: 16 < math.hypot(x - 17, y - 14) < 99 and False, '#fff')
    for y, x0, x1 in ((26, 4, 12), (28, 16, 26), (25, 20, 28)): s.line(x0, y, x1, y, '#6a9ae0')
    s.px(3, 23, '#f4f8ff'); s.px(29, 23, '#f4f8ff')
    return s

# くすだま：パカッと割れた玉＋たれ幕＋紙ふぶき
@sp('kusudama')
def _():
    s = S(True)
    s.rect(15, 0, 16, 3, '#c8b8a0')
    s.ell(9.5, 8, 6.5, 5.5, '#f0b830'); s.ell(22.5, 8, 6.5, 5.5, '#f0b830')
    clear_if(s, lambda x, y: (x < 16 and x > 9.5 + 0) and y < 6 and False)
    s.rect(11, 12, 21, 28, '#ffffff')                                          # たれ幕
    s.finish(ol='#5a3a10')
    s.rect(11, 12, 21, 13, '#e0303a'); s.rect(11, 27, 21, 28, '#e0303a')
    for y in (16, 19, 22): s.line(14, y, 18, y, '#e0303a')                     # 字のかわり
    s.line(16, 15, 16, 24, '#e0303a')
    s.line(4, 8, 15, 8, '#e0303a'); s.line(17, 8, 28, 8, '#e0303a')            # 玉の帯
    for (x, y, c) in ((3, 16, '#ff5a8a'), (6, 21, '#5ab0ff'), (25, 17, '#7ad070'), (28, 22, '#ff5a8a'), (4, 27, '#ffd040'), (27, 28, '#5ab0ff'), (8, 14, '#ffd040'), (24, 13, '#ff8a3a')):
        s.rect(x, y, x + 1, y + 1, c)
    return s

# すずむし：竹の虫かご＋中の鈴虫＋鳴いている音符
@sp('suzumushi')
def _():
    s = S(True)
    s.rect(4, 8, 24, 29, '#e8d29a')                                            # かご
    s.finish(ol='#4a3418')
    s.rect(5, 9, 23, 28, '#2e3a2a')                                            # 中（暗い）
    rell(s, 14.5, 22, 6.5, 2.6, -10, '#6e6650'); s.disc(8.5, 23, 2, '#2a2420')  # 鈴虫
    s.line(12, 21, 20, 20, '#a8a080'); s.line(7, 22, 6, 17, '#a8a080'); s.line(7, 22, 10, 16, '#a8a080')
    s.rect(6, 26, 22, 27, '#5a8a3a')                                           # 草
    for x in range(6, 24, 3): s.rect(x, 9, x, 28, '#d8be80')                   # 竹ひご
    s.rect(4, 8, 24, 9, '#c8a060'); s.rect(4, 28, 24, 29, '#c8a060')
    s.line(9, 7, 14, 3, '#c8a060'); s.line(19, 7, 14, 3, '#c8a060')            # 持ち手
    s.disc(26, 10, 1.6, '#ffd040'); s.line(27, 10, 27, 4, '#ffd040'); s.line(27, 4, 29, 5, '#ffd040')   # 音符
    s.disc(29, 17, 1.3, '#ffd040'); s.line(30, 17, 30, 12, '#ffd040')
    return s

# やぶさめ：太い和弓＋矢＋的
@sp('yabusame')
def _():
    s = S(True)
    for (x0, y0, x1, y1) in ((9, 1, 5, 8), (5, 8, 4, 18), (4, 18, 5, 25), (5, 25, 8, 31)):
        s.line(x0, y0, x1, y1, '#3a2418', 2)
    s.rect(23, 9, 30, 22, '#f4eee0')                                           # 的
    s.finish(ol='#1a1010')
    s.line(9, 1, 8, 31, '#e8e0d0')                                             # 弦
    s.rect(3, 19, 5, 21, '#f4f4f4')                                            # にぎり
    s.ring(26.5, 15.5, 3.4, 1.2, '#1a1418'); s.disc(26.5, 15.5, 1.2, '#e0303a')
    s.line(8, 15, 24, 15, '#d8b070', 2)                                        # 矢
    s.poly([(24, 13), (27, 15.5), (24, 17)], '#9aa0b0')
    s.poly([(8, 12), (12, 15), (8, 15)], '#f4f4f4'); s.poly([(8, 18), (12, 16), (8, 16)], '#1a1418')
    return s

# へび：太くうねった体＋舌
@sp('snake')
def _():
    s = S(True)
    path = [(6, 28), (11, 29), (17, 28), (21, 24), (18, 20), (12, 18.5), (9, 14.5), (12, 10), (18, 9), (22, 7.5)]
    for i, (x, y) in enumerate(path): s.disc(x, y, 2.4 + i * 0.12, '#4ab04a')
    s.ell(24.5, 6.5, 4.2, 3.2, '#4ab04a')
    s.line(28, 7, 30, 8, '#e0303a'); s.px(31, 7, '#e0303a'); s.px(31, 9, '#e0303a')
    s.finish(ol='#123a14')
    for i, (x, y) in enumerate(path[::2]): s.px(int(x), int(y), '#c8ec90')     # もよう
    for (x, y) in ((14, 28), (19, 22), (10, 12), (15, 9)): s.px(x, y, '#2e7a30')
    s.rect(25, 5, 26, 5, '#1a1418'); s.px(25, 4, '#ffe060')
    return s

# 小銭：四角い穴の古いお金（寛永通宝ふう）
@sp('coin')
def _():
    s = S(True)
    s.disc(16, 16, 13.5, '#f2c03a')
    clear_if(s, lambda x, y: 13 < x < 19 and 13 < y < 19)
    s.finish(ol='#5a3a08')
    s.ring(16, 16, 11.5, 1, '#c8901a')
    s.rect(12, 12, 19, 12, '#c8901a'); s.rect(12, 19, 19, 19, '#c8901a'); s.rect(12, 12, 12, 19, '#c8901a'); s.rect(19, 12, 19, 19, '#c8901a')
    for (x, y) in ((15, 6), (16, 6), (15, 25), (16, 25), (6, 15), (6, 16), (25, 15), (25, 16), (16, 8), (8, 16), (23, 16), (16, 23)):
        s.px(x, y, '#b07a12')                                                  # 文字のかわり
    s.px(8, 9, '#fff2a0'); s.px(9, 8, '#fff2a0'); s.px(10, 7, '#fff2a0')
    return s

# なると：ふちがギザギザの白い丸＋ピンクのうずまき
@sp('i_naruto')
def _():
    s = S(True)
    s.disc(16, 16, 13.5, '#fbf8f2')
    clear_if(s, lambda x, y: math.hypot(x - 16, y - 16) > 12.2 and math.sin(8 * math.atan2(y - 16, x - 16)) < 0)
    s.finish(ol='#6a5a68')
    s.ring(16, 16, 9.5, 2, '#f06a96'); s.ring(16, 16, 5.5, 2, '#f06a96'); s.disc(16, 16, 1.6, '#f06a96')
    clear_if(s, lambda x, y: 16 < x < 18.5 and 6 < y < 10.5)
    s.line(17, 10, 17, 6, '#f06a96', 2)
    return s

# ================= 第4束（お守り） =================

def ering(s, cx, cy, rx, ry, w, c):
    for X, Y, x, y in s._each():
        d = math.hypot((x - cx) / rx, (y - cy) / ry)
        if 1 - w / min(rx, ry) <= d <= 1: s._set(X, Y, c, False)

# きゅうす：常滑ふうの赤茶色＋横に出た持ち手＋注ぎ口
@sp('i_teapot')
def _():
    s = S(True)
    s.ell(15, 20, 10.5, 8.5, '#b8603a')
    s.poly([(6, 19), (1, 12), (3, 11), (8, 16)], '#b8603a')                     # 注ぎ口
    s.line(24, 16, 30, 10, '#9a4a2a', 3)                                       # 横の持ち手
    s.ell(15, 12, 6.5, 2.4, '#b8603a'); s.disc(15, 9.5, 1.8, '#b8603a')
    s.finish(ol='#3a1408')
    s.line(9, 13, 21, 13, '#7a3018'); s.line(8, 16, 22, 16, '#d88a5a')
    s.px(9, 18, '#e8a070'); s.px(10, 17, '#e8a070'); s.px(14, 8, '#e8a070')
    return s

# ヨーヨー：縁日の水ヨーヨー（しまもようの風船＋ゴムひも）
@sp('i_yoyo')
def _():
    s = S(True)
    s.disc(15, 19, 10, '#f8f2fa')
    s.finish(ol='#3a2a48')
    for k, c in enumerate(('#e8405a', '#3a8ae0', '#f0c030', '#40b060')):
        y0 = 13 + k * 3.6
        for X, Y, x, y in s._each():
            if s.g[Y][X] not in (None,) and abs(y - (y0 + 2 * math.sin((x - 5) / 3.2))) < .7 and math.hypot(x - 15, y - 19) < 9.3:
                s.g[Y][X] = c
    s.disc(10, 14, 1.8, '#ffffff')                                             # 水のつや
    s.rect(14, 8, 16, 9, '#e8405a')                                            # 結び目
    s.line(15, 8, 22, 1, '#f0e6c8'); s.ring(24, 2, 2.2, 1, '#f0e6c8')          # ゴムひもと指輪
    return s

# たこあげ：四角い和凧＋竹の骨＋しっぽ＋糸
@sp('i_kite')
def _():
    s = S(True)
    s.rect(4, 2, 24, 22, '#f6eedc')
    s.finish(ol='#3a2418')
    s.line(4, 2, 24, 22, '#d8c8a8'); s.line(24, 2, 4, 22, '#d8c8a8')           # 竹の骨
    s.disc(14, 12, 6.4, '#e0303a')                                             # 絵柄
    s.line(11, 9, 17, 9, '#1a1418', 2); s.line(14, 9, 14, 16, '#1a1418', 2); s.line(10, 14, 18, 14, '#1a1418')
    s.rect(4, 2, 24, 3, '#e0303a')
    for x0 in (6, 22):                                                         # しっぽ
        s.line(x0, 23, x0 - 2, 27, '#e0303a'); s.line(x0 - 2, 27, x0 + 1, 31, '#e0303a')
    s.line(14, 12, 30, 29, '#e8e0f0')                                          # 糸
    return s

# おつきみ：三方にのった月見だんご＋すすき＋満月
@sp('i_tsukimi')
def _():
    s = S(True)
    s.disc(26, 6, 4.6, '#ffe48a')
    s.line(5, 30, 6, 8, '#b8a060'); s.line(9, 30, 11, 11, '#b8a060')            # すすき
    for (x, y) in ((6, 8), (11, 11)):
        s.line(x, y, x - 3, y + 5, '#efe2b8', 2); s.line(x, y, x + 2, y + 5, '#efe2b8')
    s.rect(10, 22, 29, 23, '#d8b27a'); s.poly([(13, 24), (26, 24), (25, 30), (14, 30)], '#c89a5a')   # 三方
    for (cx, cy) in ((13, 19.5), (17, 19.5), (21, 19.5), (25, 19.5), (15, 15.8), (19, 15.8), (23, 15.8), (17, 12.1), (21, 12.1), (19, 8.4)):
        s.disc(cx, cy, 2.1, '#fbf8f0')
    s.finish(ol='#3a2a18')
    s.disc(19.5, 27, 1.8, '#5a3a18')                                           # 三方の穴
    s.px(25, 4, '#fff6d0'); s.px(24, 5, '#fff6d0')
    return s

# まよけ：破魔矢（白い矢＋絵馬＋鈴）
@sp('i_mayoke')
def _():
    s = S(True)
    s.line(4, 28, 25, 7, '#f6f2ea', 2)
    s.poly([(25, 4), (29, 3), (28, 7), (26, 8)], '#e8c040')                     # 矢じり
    rell(s, 6.5, 24.5, 4.2, 1.6, 45, '#ffffff'); rell(s, 4.5, 26.5, 4.2, 1.6, 45, '#ffffff')   # 羽
    s.poly([(13, 22), (19, 22), (19, 29), (13, 29), (13, 22)], '#e2b878')       # 絵馬
    s.poly([(13, 22), (16, 19.5), (19, 22)], '#e2b878')
    s.finish(ol='#3a2418')
    s.line(16, 16, 16, 20, '#e0303a')                                          # 赤いひも
    s.rect(14, 24, 18, 25, '#e0303a'); s.rect(15, 27, 17, 27, '#a8702a')
    s.disc(21.5, 17, 1.8, '#f0c030'); s.px(21, 16, '#fff2a0')                  # 鈴
    s.line(4, 26, 7, 23, '#e0303a'); s.line(3, 28, 6, 25, '#1a1418')
    return s

# おんせん：太い♨マーク
@sp('i_onsen')
def _():
    s = S(True)
    ering(s, 16, 23, 12, 6.5, 2.2, '#e0303a')
    for x0 in (10, 16, 22):
        for k in range(17):
            y = 21 - k; x = x0 + 1.6 * math.sin(k / 2.6)
            s.rect(round(x - 1), y, round(x), y, '#e0303a')
    s.finish(shade=False, ol='#fff0e8')
    return s

# つづら：編んだ箱＋ふた＋赤いひも
@sp('i_tsuzura')
def _():
    s = S(True)
    s.rect(4, 13, 28, 29, '#8a5a2a'); s.rect(3, 8, 29, 13, '#7a4a24')
    s.finish(ol='#2a1408')
    for k in range(-30, 40, 4):                                                # 編み目
        s.line(4 + k, 29, 4 + k + 16, 13, '#a8743a'); s.line(4 + k, 13, 4 + k + 16, 29, '#6a4020')
    for X in range(32):
        for Y in range(32):
            if not (4 <= X <= 28 and 13 <= Y <= 29) and s.g[Y][X] in ('#a8743a', '#6a4020'): s.g[Y][X] = None
    s.rect(3, 12, 29, 13, '#2a1a10'); s.rect(3, 8, 29, 8, '#9a6a34')
    s.rect(15, 8, 16, 29, '#d8303a'); s.rect(4, 20, 28, 21, '#d8303a')         # ひも
    s.ring(13, 6, 2.2, 1, '#d8303a'); s.ring(18.5, 6, 2.2, 1, '#d8303a')
    return s

# はなかざり：つまみ細工のかんざし（花＋さがり）
@sp('i_hanakazari')
def _():
    s = S(True)
    s.line(14, 13, 29, 30, '#d8a830', 2)                                       # かんざしの棒
    for k in range(6):
        a = k * 60 - 90; r = math.radians(a)
        rell(s, 11 + 4.4 * math.cos(r), 10 + 4.4 * math.sin(r), 3.6, 1.9, a, '#e8405a')
    for k in range(5):
        a = k * 72 - 54; r = math.radians(a)
        rell(s, 21 + 2.8 * math.cos(r), 6 + 2.8 * math.sin(r), 2.4, 1.3, a, '#f6a6c0')
    s.finish(ol='#4a1020')
    s.disc(11, 10, 1.6, '#ffe060'); s.disc(21, 6, 1, '#ffffff')
    for x in (6, 10, 14):                                                      # さがり
        s.line(x, 16, x, 26, '#d8a830')
        for y in (19, 23): s.rect(x - 1, y, x, y + 1, '#f6a6c0')
        s.rect(x - 1, 27, x, 28, '#e8405a')
    return s

# つりざお：太い竹ざお＋糸＋赤白のうき
@sp('i_rod')
def _():
    s = S(True)
    s.line(3, 30, 15, 14, '#b8843a', 3); s.line(15, 14, 26, 3, '#c8944a', 2)
    s.ell(27, 22, 2.4, 3.6, '#e0303a')
    s.finish(ol='#3a2410')
    for (x, y) in ((7, 25), (11, 20), (18, 11)): s.px(x, y, '#6a4a1a')         # 竹の節
    s.line(26, 3, 27, 18, '#e8e4f0')                                           # 糸
    s.ell(27, 22, 2.4, 3.6, '#e0303a'); s.rect(25, 22, 29, 25, '#ffffff'); s.rect(27, 26, 27, 28, '#e8e4f0')
    s.line(23, 28, 31, 28, '#6a9ae0')                                          # 水面
    return s

# 線香花火：たれ下がった紙こより＋赤い火の玉＋松葉の火花
@sp('i_sparkler')
def _():
    s = S(True)
    s.line(15, 1, 16, 9, '#c86ab0', 2); s.line(16, 9, 16, 15, '#e89ad0', 1)
    for k in range(10):                                                         # 松葉
        a = math.radians(k * 36 + 10); r1 = 9 + (k % 3) * 2
        x1, y1 = 16 + r1 * math.cos(a), 19 + r1 * math.sin(a) * .9
        s.line(16 + 3.5 * math.cos(a), 19 + 3.5 * math.sin(a), x1, y1, '#ffcf4a')
        s.line(x1, y1, x1 + 2 * math.cos(a + .8), y1 + 2 * math.sin(a + .8), '#ff9a3a')
        s.line(x1, y1, x1 + 2 * math.cos(a - .8), y1 + 2 * math.sin(a - .8), '#ff9a3a')
    s.disc(16, 18, 2.8, '#ff6a2a'); s.disc(16, 18, 1.6, '#ffd24a')
    return s

# ほらがい：巻きの段がわかるとがった先＋まだらもよう＋金の吹き口＋房
@sp('i_horagai')
def _():
    s = S(True)
    for (cx, cy, r) in ((8, 8, 3.2), (11, 11, 4.6), (16, 16, 7.4), (19, 20, 8.6)):   # 先から胴へ太くなる巻き
        s.disc(cx, cy, r, '#f2e2c4')
    s.rect(3, 2, 6, 5, '#d8a830')                                              # 吹き口
    s.finish(ol='#3a2418')
    for (x0, y0, x1, y1) in ((6, 11, 11, 6), (8, 15, 15, 8), (11, 21, 21, 11)):      # 巻きの段
        s.line(x0, y0, x1, y1, '#b8885a')
    for (x, y) in ((14, 18), (18, 15), (20, 22), (24, 18), (16, 24), (22, 26), (13, 13), (10, 9)):   # まだら
        s.rect(x, y, x + 1, y, '#a8642a')
    rell(s, 23, 22, 3.2, 5.8, -45, '#f0a85a'); s.px(22, 21, '#ffe0b0')         # 口
    s.px(4, 3, '#fff0a0')
    s.line(7, 6, 3, 14, '#f4f4f4'); s.line(3, 14, 3, 22, '#f4f4f4')            # 房
    s.rect(2, 22, 4, 25, '#e0303a'); s.rect(2, 26, 2, 29, '#e0303a'); s.rect(4, 26, 4, 29, '#e0303a')
    return s
