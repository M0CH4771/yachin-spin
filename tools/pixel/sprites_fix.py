# 32x32 で直接描き直したスプライト（見分けにくかったもの）
from pixel import S, dark, light
from sprites import SP, R, DR, OR, YE, GO, CR, WH, PK, LP, GR, DG, LG, BL, LB, NV, PU, BR, DB, TN, GY, DY, BK, SK, TE, EYE

RIM = '#cfc6e8'   # 暗い絵に使う明るい縁

def sp(name):
    def deco(fn): SP[name] = fn; return fn
    return deco

def steam(s, xs, y0=10, h=7):
    for x in xs:
        s.line(x, y0, x - 1, y0 - 3, '#eef2f6', 1, True); s.line(x - 1, y0 - 3, x + 1, y0 - h, '#eef2f6', 1, True)

# ---------- 食べもの ----------
@sp('tea')
def _():
    s = S(True)
    s.ell(16, 27, 13, 3.2, '#8a5232')                                         # 茶托
    s.poly([(6, 13), (26, 13), (24, 25), (8, 25)], '#efe6cf')                  # 湯のみ
    s.ell(16, 13, 10, 2.6, '#7cc04a')                                          # お茶の面
    s.finish()
    s.rect(8, 18, 24, 19, '#4f8f3a'); s.ell(16, 13, 7, 1.4, '#a6e070')
    steam(s, (12, 20), 9, 7)
    return s

@sp('rice')
def _():
    s = S(True)
    stalks = [(16, 1, 16, 30), (6, 4, 14, 30), (26, 4, 18, 30)]
    for (x0, y0, x1, y1) in stalks: s.line(x0, y0, x1, y1, '#8aa040', 1)
    s.line(13, 22, 5, 26, '#5f8a2e', 2); s.line(19, 22, 27, 26, '#5f8a2e', 2)
    for (x0, y0, x1, y1) in stalks:
        for k in range(5):
            y = y0 + 1.5 + k * 2.3; x = x0 + (x1 - x0) * (y - y0) / (y1 - y0)
            s.ell(x - 1.4, y, 1.25, 1.05, '#f2c040'); s.ell(x + 1.4, y + 1.1, 1.25, 1.05, '#f2c040')
        s.ell(x0, y0 + .5, 1.0, 1.3, '#f2c040')
    s.finish()
    s.rect(12, 21, 20, 22, '#c8302a')
    for (x0, y0, x1, y1) in stalks: s.px(x0 - 1, y0 + 1, '#fff0a8')
    return s

@sp('oden')
def _():
    s = S(True)
    s.line(16, 1, 16, 31, TN, 2)
    s.poly([(16, 3), (24, 12), (8, 12)], '#7a6a72')                            # こんにゃく
    s.disc(16, 18, 5.5, '#d49a52')                                              # がんも
    s.rect(10, 24, 22, 29, '#f3e2b0')                                           # だいこん
    s.finish()
    for (x, y) in [(13, 9), (17, 8), (19, 10), (15, 6)]: s.px(x, y, '#5a5666')
    s.px(14, 16, '#f0c080'); s.px(18, 19, '#a86a30'); s.rect(11, 24, 21, 24, '#fff6d8')
    return s

@sp('ika')
def _():
    s = S(True)
    s.line(16, 18, 16, 31, TN, 2)
    s.poly([(16, 1), (25, 11), (22, 19), (10, 19), (7, 11)], '#e07a3a')         # 胴
    s.poly([(7, 11), (2, 8), (9, 6)], '#e07a3a'); s.poly([(25, 11), (30, 8), (23, 6)], '#e07a3a')
    for x0 in (10, 13, 16, 19, 22):
        s.line(x0, 19, x0 + (1 if x0 % 2 else -1), 24, '#d0602a', 2, False)
    s.finish()
    for y in (9, 13): s.line(11, y, 21, y, '#a8401a', 1, True)
    s.line(13, 5, 12, 15, '#f8b070', 1, True)
    return s

@sp('yakiimo')
def _():
    s = S(True)
    s.poly([(1, 18), (6, 12), (14, 10), (22, 10), (28, 12), (31, 17), (27, 23), (18, 25), (9, 24), (3, 22)], '#8a3a86')
    s.finish()
    s.poly([(10, 14), (20, 13), (21, 20), (11, 21)], '#f6c445'); s.poly([(12, 15), (18, 15), (19, 18), (13, 19)], '#ffe08a')
    s.px(5, 18, '#b860b0'); s.px(26, 15, '#b860b0'); s.px(24, 20, '#b860b0')
    steam(s, (13, 19), 9, 7)
    return s

@sp('mame')
def _():
    s = S(True)
    s.poly([(4, 16), (28, 16), (26, 29), (6, 29)], '#c8975a')                  # 枡
    s.finish()
    s.rect(6, 21, 26, 21, '#8a6234'); s.line(6, 17, 6, 28, '#e8c08a', 1, True)
    beans = [(8, 13), (14, 13), (20, 13), (25, 13), (11, 8), (17, 8), (22, 8), (14, 4), (27, 27)]
    for (x, y) in beans:
        s.ell(x, y, 3.3, 2.9, '#5a3a1a'); s.ell(x, y, 2.5, 2.1, '#dba65a'); s.px(x - 1, y - 1, '#ffe0a8'); s.px(x, y - 1, '#f2c47a')
    return s

@sp('senbei')
def _():
    s = S(True)
    s.disc(16, 15, 13, '#e0a050')
    s.finish()
    s.ring(16, 15, 12.2, 1.2, '#b8742e')
    for (x, y) in [(10, 8), (19, 6), (23, 11), (11, 14), (17, 11), (8, 19), (24, 18), (15, 18)]: s.px(x, y, '#a8642a'); s.px(x + 1, y, '#c47e38')
    s.line(8, 9, 12, 5, '#f8cf90', 1, True)
    for y in range(19, 30):                                                     # 下の方にのりを巻く
        for x in range(32):
            if s.g[y][x] is not None and (x - 15.5) ** 2 + (y - 14.5) ** 2 <= 12.9 ** 2: s.g[y][x] = '#1f3a2a'
    s.rect(5, 19, 26, 19, '#3f7a52')
    return s

# ---------- 行事・道具 ----------
@sp('tanzaku')
def _():
    s = S(True)
    s.line(15, 31, 15, 2, '#4a9a3a', 3)
    for y in (9, 17, 25): s.rect(14, y, 16, y, '#2f6a2a')
    s.line(16, 6, 27, 2, '#4a9a3a', 1, False); s.line(14, 12, 4, 7, '#4a9a3a', 1, False)
    s.poly([(24, 2), (31, 2), (27, 6)], LG); s.poly([(7, 7), (1, 5), (5, 10)], LG); s.poly([(17, 20), (24, 17), (21, 22)], LG)
    s.rect(20, 7, 24, 18, '#f59ab8'); s.rect(5, 11, 9, 22, '#f6d045'); s.rect(19, 20, 23, 29, '#6ab0f0')
    s.finish()
    s.line(22, 4, 22, 7, WH, 1, True); s.line(7, 8, 7, 11, WH, 1, True); s.line(21, 17, 21, 20, WH, 1, True)
    return s

@sp('kadomatsu')
def _():
    s = S(True)
    for x0, top in ((9, 5), (14, 2), (19, 7)):
        s.poly([(x0, top + 4), (x0 + 5, top), (x0 + 5, 22), (x0, 22)], '#4fa648')
    s.ell(6, 18, 4, 3, '#2f6a3a'); s.ell(26, 18, 4, 3, '#2f6a3a')
    s.rect(6, 20, 26, 30, '#d8b070')
    s.finish()
    for x0, top in ((9, 5), (14, 2), (19, 7)):
        s.line(x0 + 1, top + 3, x0 + 4, top + 1, '#e8e0a0', 1, True)
        s.rect(x0, 14, x0 + 4, 14, '#2f7a30')
    for y in (23, 27): s.rect(7, y, 25, y + 1, '#8a2a2a')
    return s

@sp('hina')
def _():
    s = S(True)
    s.rect(1, 27, 30, 30, '#d8433b')                                            # ひな段
    s.poly([(3, 26), (15, 26), (13, 14), (5, 14)], '#2a2a4a')                   # お内裏さま
    s.poly([(17, 26), (30, 26), (27, 14), (20, 14)], '#d8433b')                 # おひなさま
    s.disc(9, 10, 4, '#fbeee0'); s.disc(23.5, 10, 4, '#fbeee0')
    s.finish(ol='#1a1420')
    s.rect(7, 1, 10, 6, '#1a1a1a')                                              # 烏帽子
    s.rect(5, 6, 12, 7, '#1a1a1a'); s.rect(19, 6, 28, 8, '#1a1a1a')             # 髪
    s.rect(21, 4, 26, 5, '#f2c14e')                                             # 冠
    s.poly([(18, 20), (30, 20), (30, 26), (18, 26)], '#f2c14e'); s.rect(18, 22, 30, 23, '#2a7a6a')
    s.rect(7, 16, 11, 18, WH); s.rect(4, 22, 14, 23, '#4a5aa0')
    for x in (8, 10, 22, 25): s.px(x, 10, EYE)
    return s

@sp('mallet')
def _():
    s = S(True)
    s.line(17, 16, 27, 30, '#8a5232', 3)
    s.rect(3, 4, 21, 16, '#f2c14e')
    s.ell(3, 10, 2, 6, '#e0a82e'); s.ell(21, 10, 2, 6, '#e0a82e')
    s.finish()
    s.rect(4, 8, 20, 11, '#d8433b')
    s.disc(12, 10, 3, '#fff2c0'); s.disc(12, 10, 1.4, '#d8433b')
    s.line(5, 5, 19, 5, '#fff2a8', 1, True)
    s.rect(26, 28, 28, 31, '#d8433b')
    return s

@sp('nobori')
def _():
    s = S(True)
    s.line(5, 1, 5, 31, '#8a5232', 2); s.line(5, 3, 26, 3, '#8a5232', 2)
    s.poly([(7, 4), (26, 4), (24, 10), (26, 16), (24, 22), (26, 28), (7, 28)], WH)
    s.finish()
    s.rect(7, 5, 25, 8, '#d8433b'); s.rect(7, 24, 25, 27, '#d8433b')
    s.disc(16, 16, 4.5, '#d8433b')
    for y in (7, 13, 19, 25): s.rect(6, y, 7, y + 1, '#c8c0b0')
    return s

@sp('mirror')
def _():
    s = S(True)
    s.rect(14, 22, 18, 31, '#8a2a2a')                                           # 柄
    s.disc(16, 12, 11, '#d8433b')                                                # 漆の枠
    s.finish()
    s.disc(16, 12, 8.5, '#bfe6ff'); s.disc(16, 12, 7, '#e4f6ff')
    s.line(11, 15, 18, 8, WH, 2, True); s.line(15, 17, 20, 12, WH, 1, True)
    s.px(22, 5, '#fff2a8'); s.px(23, 4, '#fff2a8'); s.px(21, 4, '#fff2a8'); s.px(22, 3, '#fff2a8'); s.px(22, 6, '#fff2a8')
    for y in (24, 27, 30): s.rect(14, y, 18, y, '#f2c14e')
    return s

@sp('tsubo')
def _():
    s = S(True)
    s.poly([(11, 3), (21, 3), (19, 7), (26, 13), (27, 21), (22, 29), (10, 29), (5, 21), (6, 13), (13, 7)], '#c8784a')
    s.finish()
    s.rect(9, 3, 23, 4, '#e8a070')
    s.rect(7, 15, 25, 18, '#f3e2b0')
    for x in (9, 13, 17, 21): s.px(x + 1, 16, '#3a6ac8'); s.px(x + 2, 17, '#3a6ac8'); s.px(x, 17, '#3a6ac8')
    s.line(9, 12, 11, 20, '#f0a878', 1, True)
    return s

@sp('japan')
def _():
    s = S(True)
    s.disc(16, 16, 14.5, '#3f78c8')
    s.ell(23, 7, 5, 3.4, '#5aae4a')                                             # 北海道
    s.poly([(20, 11), (23, 12), (21, 17), (17, 21), (12, 23), (8, 23), (8, 20), (13, 19), (17, 16)], '#5aae4a')   # 本州
    s.ell(13, 26, 2.6, 1.4, '#5aae4a')                                          # 四国
    s.ell(6, 26, 2.4, 3, '#5aae4a')                                             # 九州
    s.finish()
    s.ring(16, 16, 14.5, 1, '#7ab0ee')
    s.px(25, 27, '#9ad86a')                                                      # 沖縄
    return s

@sp('ninja')
def _():
    s = S(True)
    s.disc(16, 17, 12, '#3c4a7a')
    s.finish(ol=RIM)
    s.rect(6, 13, 26, 19, '#f6cfaa')
    s.rect(9, 15, 12, 17, EYE); s.rect(20, 15, 23, 17, EYE); s.px(10, 15, WH); s.px(21, 15, WH)
    s.line(9, 13, 13, 14, '#2a2430', 1, True); s.line(23, 13, 19, 14, '#2a2430', 1, True)
    s.rect(5, 9, 27, 11, '#d8433b')
    s.poly([(26, 9), (31, 6), (30, 10)], '#d8433b'); s.poly([(26, 11), (31, 13), (29, 9)], '#b8302a')
    return s

@sp('tengu')
def _():
    s = S(True)
    s.ell(13, 17, 10, 11, '#d8433b')
    s.poly([(15, 15), (31, 24), (29, 27), (15, 21)], '#e85a4a')                 # 長い鼻
    s.finish()
    s.poly([(8, 3), (14, 1), (18, 3), (16, 7), (10, 7)], '#1a1a1a')              # 頭襟
    s.line(4, 11, 11, 14, WH, 2, True); s.line(21, 11, 15, 14, WH, 2, True)      # まゆ
    s.rect(7, 15, 9, 17, '#fff2a8'); s.rect(15, 15, 17, 17, '#fff2a8'); s.px(8, 16, EYE); s.px(16, 16, EYE)
    s.line(7, 24, 13, 23, '#7a1a1a', 1, True)
    s.line(17, 18, 28, 24, '#ff8a70', 1, True)
    return s

@sp('suzumushi')
def _():
    s = S(True)
    s.ell(15, 19, 10, 5, '#6a5a2a')
    s.disc(5, 18, 3.5, '#6a5a2a')
    s.line(22, 18, 29, 12, '#6a5a2a', 2, False); s.line(29, 12, 30, 24, '#6a5a2a', 2, False)   # うしろ足
    s.line(8, 22, 6, 28, '#6a5a2a', 2, False); s.line(14, 23, 13, 29, '#6a5a2a', 2, False)
    s.finish(ol=RIM)
    s.ell(16, 17, 7, 3, '#b8a46a')
    for x in (12, 16, 20): s.line(x, 15, x - 1, 19, '#8a7840', 1, True)
    s.line(3, 16, 0, 4, '#b8a46a', 1, True); s.line(4, 15, 9, 2, '#b8a46a', 1, True)  # 触角
    s.px(4, 17, '#fff2a8')
    s.disc(25, 5, 3, '#f2c14e'); s.px(25, 7, '#8a6a20'); s.line(24, 3, 26, 3, '#fff2a8', 1, True)   # 鈴
    return s

# ---------- お守り ----------
@sp('i_kinchaku')
def _():
    s = S(True)
    s.poly([(9, 9), (23, 9), (28, 20), (24, 29), (8, 29), (4, 20)], '#d0507a')
    s.poly([(10, 4), (14, 9), (18, 9), (22, 4), (20, 9), (12, 9)], '#d0507a')
    s.finish()
    s.rect(7, 9, 25, 10, '#f2c14e')
    s.line(16, 10, 13, 16, '#f2c14e', 1, True); s.line(16, 10, 19, 16, '#f2c14e', 1, True)
    s.disc(13, 17, 1.4, '#f2c14e'); s.disc(19, 17, 1.4, '#f2c14e')
    for (x, y) in [(9, 21), (14, 24), (20, 22), (23, 26), (11, 27), (18, 27)]: s.px(x, y, '#ffd0e0')
    return s

@sp('i_horagai')
def _():
    s = S(True)
    s.poly([(2, 18), (14, 8), (26, 7), (30, 14), (27, 23), (16, 26), (5, 22)], '#f2d6a8')
    s.finish()
    s.ell(22, 16, 6, 6, '#f59ab8'); s.ell(22, 16, 3.5, 3.5, '#d86a8a')
    for x in (8, 12, 16): s.line(x, 12 + (16 - x) // 4, x + 2, 23, '#c8a070', 1, True)
    s.rect(1, 17, 3, 20, '#8a5232')
    s.line(4, 21, 2, 30, '#d8433b', 1, True); s.disc(2, 30, 1.2, '#d8433b')
    return s

@sp('i_tebukuro')
def _():
    s = S(True)
    for x in (9, 13, 17, 21): s.rect(x, 4 + (0 if x in (13, 17) else 2), x + 3, 16, WH)
    s.ell(6, 16, 3, 5, WH)
    s.rect(8, 13, 24, 25, WH)
    s.rect(8, 25, 24, 30, '#4a82d8')
    s.finish()
    for x in (12, 16, 20): s.line(x, 6, x, 15, '#c8c0b0', 1, True)
    s.rect(8, 27, 24, 27, '#8cc8f0')
    for (x, y) in [(11, 18), (15, 20), (19, 18), (13, 22), (18, 23)]: s.px(x, y, '#d8433b')
    return s

@sp('i_telescope')
def _():
    s = S(True)
    s.line(16, 18, 8, 30, '#5a3a22', 2); s.line(16, 18, 24, 30, '#5a3a22', 2); s.line(16, 18, 16, 30, '#5a3a22', 2)
    s.poly([(3, 17), (11, 12), (13, 16), (5, 21)], '#e0a82e')
    s.poly([(11, 12), (20, 7), (22, 12), (13, 16)], '#f2c14e')
    s.poly([(20, 6), (28, 2), (31, 8), (22, 13)], '#e0a82e')
    s.finish()
    s.line(11, 12, 13, 16, '#8a5a1a', 1, True); s.line(20, 7, 22, 12, '#8a5a1a', 1, True)
    s.line(28, 2, 31, 8, '#bfe6ff', 1, True); s.px(29, 4, WH)
    s.line(13, 10, 19, 7, '#fff2a8', 1, True)
    return s

@sp('i_ofuda')
def _():
    s = S(True)
    s.poly([(9, 2), (23, 2), (24, 29), (8, 30)], '#f3e8cc')
    s.finish()
    s.disc(16, 8, 3.5, '#d8433b'); s.disc(16, 8, 1.6, '#f3e8cc')
    s.line(16, 13, 16, 26, '#2a2430', 2, True); s.line(12, 16, 20, 16, '#2a2430', 1, True); s.line(12, 21, 20, 21, '#2a2430', 1, True)
    s.rect(9, 27, 23, 28, '#d8433b')
    s.line(9, 1, 23, 1, '#c8b88a', 1, True)
    return s

# ---------- 挿絵（額縁の絵） ----------
@sp('u_picture')
def _():
    s = S(True)
    s.rect(3, 5, 28, 26, '#b07a3a')                                            # 額縁
    s.rect(6, 8, 25, 23, '#2c3a6e')                                            # 夜空
    s.finish()
    s.rect(6, 8, 25, 23, '#2c3a6e')
    s.disc(20, 12, 2.2, '#ffe9a0')                                             # 月
    s.poly([(6, 23), (12, 15), (17, 21), (20, 18), (25, 23)], '#3f7a4a')        # 山
    s.poly([(8, 23), (12, 17), (15, 21)], '#5aa060')
    s.rect(4, 6, 27, 6, '#e0a860'); s.rect(4, 6, 4, 25, '#e0a860')             # 額のハイライト
    return s
