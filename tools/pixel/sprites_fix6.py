# Ver.1.4 で増えたドット絵（おちゃだんご・はんげつ・えんむすび）
import math
from pixel import S, N
from sprites import SP

def sp(name):
    def deco(fn): SP[name] = fn; return fn
    return deco

# おちゃだんご：お盆の上に湯のみと三色だんご
@sp('chadango')
def _():
    s = S(True)
    s.ell(16, 27, 15, 3.6, '#8a5232')                                          # お盆
    s.poly([(4, 7), (16, 7), (15, 19), (5, 19)], '#efe6cf')                     # 湯のみ（奥）
    s.ell(10, 7, 6, 1.8, '#7cc04a')                                             # お茶の面
    s.line(6, 23, 31, 23, '#c8a070', 1)                                         # 串（手前で横向き）
    for (cx, c) in ((12, '#f6a6bf'), (19, '#f7f2e6'), (26, '#8cc86a')):
        s.disc(cx, 22, 3.8, c)
    s.finish()
    s.rect(5, 12, 15, 13, '#4f8f3a'); s.ell(10, 7, 4, 1, '#a6e070')
    for cx in (12, 19, 26): s.px(cx - 2, 20, '#ffffff')
    s.px(8, 3, '#e8e8f0'); s.px(9, 1, '#e8e8f0'); s.px(12, 3, '#e8e8f0')          # ゆげ
    return s

# はんげつ：右半分が光る月
@sp('hangetsu')
def _():
    s = S(True)
    s.disc(16, 16, 12, '#ffe8a0')
    s.rect(0, 0, 15, 31, None)
    s.finish()
    s.disc(21, 11, 1.8, '#f0cf78'); s.disc(23, 19, 2.4, '#f0cf78'); s.disc(18, 24, 1.4, '#f0cf78')
    s.px(18, 7, '#ffffff'); s.px(19, 6, '#ffffff')
    return s

# えんむすび：ピンクのお守り袋＋紅白の水引
@sp('i_enmusubi')
def _():
    s = S(True)
    s.poly([(8, 9), (24, 9), (25, 29), (7, 29)], '#f07aa0')                    # 袋
    s.poly([(10, 9), (16, 3), (22, 9)], '#f07aa0')
    s.finish(ol='#5a1a30')
    s.rect(11, 14, 21, 25, '#fff0f4')                                           # 白い札
    s.disc(14, 18, 2, '#e0304a'); s.disc(18, 18, 2, '#e0304a')                 # ハート
    s.poly([(12, 19), (20, 19), (16, 24)], '#e0304a')
    s.rect(7, 9, 25, 10, '#e0303a'); s.rect(7, 11, 25, 11, '#ffffff')          # 紅白の水引
    s.ring(12, 6, 2.6, 1, '#e0303a'); s.ring(20, 6, 2.6, 1, '#ffffff'); s.px(16, 8, '#f0c040')
    return s

# かぎや：花火屋の目じるしの鍵と、ぱっと開いた花火
@sp('kagiya')
def _():
    s = S(True)
    for k in range(12):                                                         # 花火（うしろ）
        a = k * math.pi / 6
        s.line(20, 11, 20 + math.cos(a) * 9, 11 + math.sin(a) * 9, '#ff8fb0' if k % 2 else '#ffd36a', 1)
    s.ring(10, 22, 5.5, 2.2, '#e0b040')                                         # 鍵の輪
    s.line(14, 18, 24, 8, '#e0b040', 2)                                         # 鍵の軸
    s.rect(19, 9, 21, 12, '#e0b040'); s.rect(22, 6, 24, 9, '#e0b040')           # 鍵の歯
    s.finish()
    s.px(8, 20, '#fff4c0'); s.px(20, 11, '#ffffff')
    return s
