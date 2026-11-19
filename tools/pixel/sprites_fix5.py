# Ver.1.3 で増えたお守りのドット絵（32x32 で直接描く）
import math
from pixel import S, N
from sprites import SP
from sprites_fix3 import rell, clear_if, paint_if, ering

def sp(name):
    def deco(fn): SP[name] = fn; return fn
    return deco

# けいと：ピンクの毛糸玉＋ほどけた糸
@sp('i_keito')
def _():
    s = S(True)
    s.disc(14, 15, 11, '#f07aa0')
    s.line(23, 22, 28, 26, '#f07aa0', 2); s.line(28, 26, 24, 30, '#f07aa0', 2); s.line(24, 30, 30, 31, '#f07aa0', 1)
    s.finish(ol='#5a1a30')
    for k in range(-2, 3): s.line(5 + k * 4, 6, 14 + k * 4, 25, '#c84a78')       # 巻いた糸
    s.line(4, 12, 22, 9, '#ffb0c8'); s.line(5, 19, 24, 15, '#ffb0c8')
    s.px(9, 9, '#ffd8e4'); s.px(10, 8, '#ffd8e4')
    return s

# ひょうたん：2つのふくらみ＋赤いひも
@sp('i_hyotan')
def _():
    s = S(True)
    s.disc(16, 10, 6, '#e0b04a'); s.disc(16, 22, 9, '#e0b04a')
    s.rect(15, 1, 17, 4, '#8a5a2a')
    s.finish(ol='#4a2a08')
    s.rect(11, 14, 21, 16, '#d8302a'); s.line(20, 16, 24, 21, '#d8302a'); s.px(24, 22, '#f0c040')
    s.px(13, 7, '#fff0c0'); s.px(12, 19, '#fff0c0'); s.px(11, 20, '#fff0c0')
    return s

# あぶらあげ：きつね色の四角い油あげ
@sp('i_aburaage')
def _():
    s = S(True)
    s.poly([(3, 12), (22, 5), (29, 20), (10, 27)], '#d8962e')
    s.finish(ol='#3a1a04')
    s.poly([(6, 13), (21, 8), (26, 19), (11, 24)], '#e8aa40')
    for (x, y) in ((9, 14), (14, 12), (19, 10), (12, 19), (17, 17), (22, 15), (15, 22), (20, 20)): s.px(x, y, '#b8701e')
    s.line(7, 12, 18, 8, '#f8d080')
    return s

# はちまき：日の丸のはちまき＋結び目
@sp('i_hachimaki')
def _():
    s = S(True)
    s.poly([(2, 12), (24, 9), (25, 17), (3, 20)], '#f8f6f0')
    s.poly([(24, 10), (31, 5), (30, 11), (26, 13)], '#f8f6f0'); s.poly([(25, 16), (31, 22), (27, 23), (24, 18)], '#f8f6f0')
    s.finish(ol='#3a3448')
    s.disc(13, 14.5, 3.6, '#e0303a')
    s.line(3, 18, 24, 15, '#d8d4e0')
    return s

# ぬかどこ：木のたる＋ぬか＋きゅうり
@sp('i_nukadoko')
def _():
    s = S(True)
    rell(s, 21, 8, 7, 2, -60, '#3e8e3a')                                         # きゅうり
    s.poly([(4, 13), (28, 13), (26, 30), (6, 30)], '#b8844a')                    # たる
    s.finish(ol='#3a2008')
    s.ell(16, 13, 12, 3, '#c8a868'); s.ell(16, 13, 10, 2, '#a8884a')            # ぬか
    for y in (18, 25): s.line(5, y, 27, y, '#5a5a6a', 2)                        # たが
    for x in (10, 16, 22): s.line(x, 15, x, 29, '#a07038')
    s.px(19, 6, '#7ac860'); s.px(22, 10, '#7ac860')
    return s

# ちゃわん：藍もようのごはん茶わん＋白いごはん
@sp('i_chawan')
def _():
    s = S(True)
    s.ell(16, 13, 12, 6, '#fbf8f0')                                              # ごはん
    s.poly([(3, 15), (29, 15), (25, 26), (7, 26)], '#f4f0e8')                   # 茶わん
    s.rect(11, 26, 21, 29, '#f4f0e8')
    s.finish(ol='#2a2a3a')
    s.line(4, 16, 28, 16, '#2c4f9a'); s.line(10, 27, 22, 27, '#2c4f9a')
    for x in (9, 15, 21): s.ring(x, 21, 2, 1, '#2c4f9a')
    for (x, y) in ((9, 11), (14, 9), (19, 10), (23, 12), (12, 13)): s.px(x, y, '#e0dccc')
    return s

# のれん：竿にかかった紺ののれん＋白い紋
@sp('i_noren')
def _():
    s = S(True)
    s.rect(2, 4, 29, 6, '#8a5a2a')                                               # 竿
    s.rect(4, 7, 27, 28, '#2c3f7a')
    s.finish(ol='#0e1430')
    for x in (11, 19): s.rect(x, 14, x, 28, '#16244a')                          # 切れ目
    s.ring(15.5, 11.5, 3.2, 1.2, '#f2ecd8'); s.px(15, 11, '#f2ecd8')
    s.line(5, 27, 26, 27, '#3c56a0')
    return s

# きんぎょばち：ふちが波打つガラスの鉢＋水＋金魚
@sp('i_kingyobachi')
def _():
    s = S(True)
    s.disc(16, 18, 12.5, '#d8f0ff')
    s.finish(ol='#1e3a60')
    clear_if(s, lambda x, y: y < 8.5)
    for x in range(5, 28, 4): s.disc(x + 1.5, 8.5, 1.8, '#d8f0ff')              # 波のふち
    paint_if(s, lambda x, y: y > 12, '#7ab8f0')                                  # 水
    rell(s, 14, 19, 4, 2.4, -10, '#ff5a2a'); s.poly([(18, 18), (21, 16), (21, 21)], '#ff5a2a'); s.px(12, 18, '#1a1418')
    s.line(8, 13, 24, 13, '#bfe4ff'); s.px(9, 22, '#ffffff'); s.px(10, 21, '#ffffff')
    s.rect(11, 27, 21, 29, '#3a6a3a'); s.px(13, 26, '#5aa050'); s.px(19, 26, '#5aa050')   # 水草
    return s

# たいこのばち：太い2本が交差
@sp('i_bachi')
def _():
    s = S(True)
    s.line(5, 27, 25, 5, '#d8b070', 4); s.line(7, 5, 27, 27, '#c8a060', 4)
    s.disc(25.5, 4.5, 3, '#d8b070'); s.disc(6.5, 4.5, 3, '#c8a060')
    s.finish(ol='#3a2408')
    s.line(5, 27, 9, 23, '#e0303a', 3); s.line(27, 27, 23, 23, '#e0303a', 3)    # にぎりの赤
    s.line(10, 21, 22, 9, '#f0d098'); s.px(24, 4, '#fff0c0'); s.px(5, 4, '#fff0c0')
    return s

# ひゃっきやこう絵巻：ひらいた巻物＋ようかいのかげ
@sp('i_emaki')
def _():
    s = S(True)
    s.rect(4, 8, 27, 24, '#efe2c0')
    s.rect(1, 6, 4, 26, '#8a3a2a'); s.rect(27, 6, 30, 26, '#8a3a2a')            # 軸
    s.finish(ol='#2a1408')
    s.rect(5, 18, 26, 23, '#3a2a48')                                             # 夜の行列
    s.poly([(7, 18), (9, 13), (11, 18)], '#3a2a48'); s.disc(15, 16, 2.4, '#3a2a48'); s.poly([(19, 18), (21, 12), (23, 18)], '#3a2a48')
    s.px(15, 16, '#ffd040'); s.px(9, 16, '#ff5a3a'); s.px(21, 15, '#ffd040')
    s.disc(22, 11, 1.8, '#f6e08a')                                               # 月
    s.line(2, 9, 2, 23, '#c86a4a'); s.line(29, 9, 29, 23, '#c86a4a')
    return s

# きんつぎ：金色のひびが走るお椀
@sp('i_kintsugi')
def _():
    s = S(True)
    s.poly([(3, 10), (29, 10), (24, 24), (8, 24)], '#3a3040')
    s.rect(11, 24, 21, 27, '#3a3040')
    s.finish(ol='#120e18')
    s.line(4, 11, 28, 11, '#6a5a78')
    s.line(9, 11, 12, 16, '#f2c03a'); s.line(12, 16, 10, 20, '#f2c03a'); s.line(12, 16, 17, 19, '#f2c03a')
    s.line(22, 11, 20, 15, '#f2c03a'); s.line(20, 15, 23, 21, '#f2c03a'); s.px(13, 25, '#f2c03a'); s.px(14, 26, '#f2c03a')
    s.px(7, 12, '#ffffff')
    return s

# ふで：書道の筆＋墨のしずく
@sp('i_fude')
def _():
    s = S(True)
    s.line(27, 4, 12, 19, '#c8944a', 3)                                          # 軸
    s.poly([(12, 16), (16, 20), (8, 28), (5, 27)], '#2a2228')                    # 穂
    s.disc(25, 26, 2.6, '#2a2228')                                               # 墨
    s.finish(ol='#120e10')
    s.line(26, 4, 13, 17, '#e0b070'); s.rect(11, 17, 14, 18, '#a8302a')
    s.px(24, 25, '#6a6a7a')
    return s

# おみこし：金の屋根＋鳳凰＋赤い胴＋かつぐ棒
@sp('i_omikoshi')
def _():
    s = S(True)
    s.rect(1, 23, 30, 25, '#b88a4a')                                             # かつぐ棒
    s.rect(8, 14, 23, 23, '#c8302a')                                             # 胴
    s.poly([(3, 15), (28, 15), (22, 8), (9, 8)], '#2a2228')                      # 屋根
    s.poly([(13, 8), (16, 3), (19, 8)], '#f0c040')                               # 鳳凰
    s.finish(ol='#1a0a08')
    s.line(3, 15, 28, 15, '#f0c040'); s.line(9, 8, 22, 8, '#f0c040')
    s.rect(10, 17, 21, 21, '#a02020'); s.rect(14, 17, 17, 21, '#f0c040')        # とびら
    s.px(16, 2, '#fff0a0'); s.px(5, 16, '#f0c040'); s.px(26, 16, '#f0c040')
    s.rect(8, 26, 9, 28, '#f0c040'); s.rect(22, 26, 23, 28, '#f0c040')          # 房
    return s

# たまてばこ：黒い漆の箱＋赤いひも＋立ちのぼるけむり
@sp('i_tamatebako')
def _():
    s = S(True)
    s.rect(4, 16, 27, 29, '#2a2228'); s.rect(3, 12, 28, 16, '#2a2228')
    for (cx, cy, r) in ((12, 8, 3.5), (17, 6, 4), (22, 9, 3), (15, 3, 2.4)): s.disc(cx, cy, r, '#f4f6ff')   # けむり
    s.finish(ol='#0e0a10')
    s.rect(15, 12, 16, 29, '#e0303a'); s.rect(4, 21, 27, 22, '#e0303a')         # ひも
    s.ring(13.5, 11, 2, 1, '#e0303a'); s.ring(18, 11, 2, 1, '#e0303a')
    for (x, y) in ((7, 18), (24, 26), (8, 26), (23, 17)): s.px(x, y, '#f0c040')  # 金のもよう
    s.line(4, 13, 27, 13, '#5a4a58')
    return s

# くまで：竹の熊手＋おかめ・小判・赤い飾り
@sp('i_kumade')
def _():
    s = S(True)
    s.line(16, 31, 16, 14, '#c8a060', 2)                                         # 柄
    for k in range(7):                                                            # 爪
        x = 4 + k * 4; s.line(16, 15, x, 4, '#d8b070', 1); s.rect(x - 1, 2, x, 4, '#d8b070')
    s.disc(16, 13, 5, '#fbe8d8')                                                  # おかめ
    s.finish(ol='#3a2408')
    s.px(14, 12, '#1a1418'); s.px(18, 12, '#1a1418'); s.px(16, 15, '#e0303a'); s.ell(13, 14, 1.2, .8, '#ff9aa0'); s.ell(19, 14, 1.2, .8, '#ff9aa0')
    s.ell(8, 10, 2, 2.8, '#f2c03a'); s.ell(24, 10, 2, 2.8, '#f2c03a')            # 小判
    s.rect(10, 18, 12, 21, '#e0303a'); s.rect(20, 18, 22, 21, '#e0303a')        # 飾り
    return s
