# 24x24 ドット絵スプライト定義
from pixel import S, dark, light
R, DR, OR, YE, GO, CR, WH = '#d8433b', '#9a2a2a', '#f0913a', '#f6c445', '#e0a82e', '#f4e6c4', '#f7f3ea'
PK, LP, GR, DG, LG, BL, LB = '#f59ab8', '#ffd0e0', '#5aae4a', '#2f7a3a', '#9ad86a', '#4a82d8', '#8cc8f0'
NV, PU, BR, DB, TN, GY, DY, BK, SK, TE = '#2a3a6a', '#7a5ac8', '#9a6438', '#5a3a22', '#d8a868', '#a6a2b4', '#5e5a6c', '#2a2430', '#f6cfaa', '#3aa89a'
EYE = '#1c1420'
SP = {}
def sp(name):
    def deco(fn): SP[name] = fn; return fn
    return deco

def eyes(s, x1, x2, y, c=EYE, h=2):
    s.rect(x1, y, x1, y + h - 1, c); s.rect(x2, y, x2, y + h - 1, c)

# ===================== シンボル =====================
@sp('coin')
def _():
    s = S(); s.ell(12, 12.5, 8.5, 8.5, YE); s.finish()
    s.ring(12, 12.5, 6.5, 1, GO); s.rect(10, 10, 13, 15, None); s.rect(10, 10, 13, 10, GO); s.rect(10, 15, 13, 15, GO); s.rect(10, 11, 10, 14, GO); s.rect(13, 11, 13, 14, GO)
    s.px(7, 9, WH); s.px(8, 8, WH); return s
@sp('tea')
def _():
    s = S(); s.poly([(5, 8), (19, 8), (17, 20), (7, 20)], '#7ab89a'); s.ell(12, 8.5, 7, 2, '#a8d880'); s.finish()
    s.rect(8, 13, 16, 14, '#5a9a7a'); s.line(10, 6, 9, 3, '#e6eef0', fix=True); s.line(14, 6, 15, 2, '#e6eef0', fix=True); return s
@sp('dango')
def _():
    s = S(); s.line(5, 21, 19, 3, TN, 2); s.disc(16, 7, 4.2, '#f7a6c0'); s.disc(12, 12, 4.2, WH); s.disc(8, 17, 4.2, '#8ec76a'); s.finish()
    s.px(15, 5, WH); s.px(11, 10, '#ffffff'); s.px(7, 15, '#c8f0a8'); return s
@sp('goldfish')
def _():
    s = S(); s.ell(11, 12, 7, 5, '#f06a3a'); s.poly([(16, 12), (22, 6), (21, 12), (22, 18)], '#f69a5a'); s.poly([(9, 7), (13, 4), (14, 8)], '#f69a5a'); s.finish()
    s.px(7, 11, EYE); s.px(6, 10, WH); s.rect(10, 12, 12, 12, '#ffb07a'); return s
@sp('rice')
def _():
    s = S(); s.line(12, 22, 12, 6, '#8aa040', 1); s.line(12, 14, 6, 8, '#8aa040', 1)
    for (x, y) in [(13, 4), (14, 6), (11, 6), (14, 9), (10, 9), (14, 12), (6, 7), (8, 6), (5, 10)]: s.ell(x, y, 1.6, 1.3, YE)
    s.finish(); return s
@sp('onigiri')
def _():
    s = S(); s.poly([(12, 3), (21, 19), (3, 19)], WH); s.finish(); s.rect(8, 13, 15, 19, '#2a3a2a'); s.rect(9, 14, 14, 18, '#3a5a3a'); s.px(10, 7, '#ffffff'); return s
@sp('seed')
def _():
    s = S(); s.ell(12, 18, 7, 4, '#8a5a32'); s.line(12, 16, 12, 10, GR, 2); s.ell(8, 9, 3.5, 2.2, LG); s.ell(16, 8, 3.5, 2.2, LG); s.finish(); return s
@sp('egg')
def _():
    s = S(); s.ell(12, 13, 6.5, 8.5, CR); s.finish(); s.px(9, 8, WH); s.px(9, 9, WH); s.px(8, 10, WH); return s
@sp('mouse')
def _():
    s = S(); s.ell(12, 15, 7, 5, GY); s.disc(7, 9, 3, GY); s.disc(15, 9, 3, GY); s.line(19, 17, 22, 14, '#e0a0b0', fix=False); s.finish()
    s.disc(7, 9, 1.3, '#f2b8c8'); s.disc(15, 9, 1.3, '#f2b8c8'); s.px(9, 14, EYE); s.px(14, 14, EYE); s.px(11, 16, '#f28aa0'); s.px(12, 16, '#f28aa0'); return s
@sp('dice')
def _():
    s = S(); s.rect(5, 5, 18, 18, WH); s.finish()
    s.rect(7, 7, 8, 8, R); s.rect(15, 15, 16, 16, BK); s.rect(11, 11, 12, 12, BK); s.rect(15, 7, 16, 8, BK); s.rect(7, 15, 8, 16, BK); return s
@sp('rabbit')
def _():
    s = S(); s.ell(9, 6, 2, 5, WH); s.ell(15, 6, 2, 5, WH); s.ell(12, 15, 7, 6.5, WH); s.finish()
    s.rect(9, 3, 9, 7, LP); s.rect(15, 3, 15, 7, LP); s.px(9, 14, '#d0303a'); s.px(15, 14, '#d0303a'); s.px(12, 17, '#f28aa0'); s.ell(8, 17, 1.4, 0.8, LP); s.ell(16, 17, 1.4, 0.8, LP); return s
@sp('frog')
def _():
    s = S(); s.ell(12, 15, 9, 6, GR); s.disc(7, 9, 3.4, GR); s.disc(17, 9, 3.4, GR); s.finish()
    s.disc(7, 9, 2, WH); s.disc(17, 9, 2, WH); s.px(7, 9, EYE); s.px(17, 9, EYE); s.line(8, 16, 16, 16, DG); s.px(7, 15, DG); s.px(17, 15, DG); s.ell(12, 19, 4, 1.4, LG); return s
@sp('furin')
def _():
    s = S(); s.ell(12, 9, 6, 6, '#bfe6ff'); s.rect(6, 9, 18, 11, '#bfe6ff'); s.finish(); s.line(12, 12, 12, 16, BK, fix=True); s.rect(9, 16, 15, 21, '#f6e0a0'); s.rect(9, 16, 15, 21, None); s.rect(10, 16, 14, 21, CR)
    s.px(12, 2, BK); s.px(9, 7, R); s.px(14, 6, BL); s.px(11, 9, GR); s.px(8, 5, WH); return s
@sp('cat')
def _():
    s = S(); s.poly([(5, 10), (7, 3), (11, 8)], WH); s.poly([(19, 10), (17, 3), (13, 8)], OR); s.ell(12, 13, 8, 7, WH); s.finish()
    s.rect(14, 7, 18, 9, OR); s.rect(15, 10, 18, 11, OR); s.rect(6, 8, 8, 9, BK); s.rect(8, 12, 8, 14, EYE); s.rect(15, 12, 15, 14, EYE); s.px(11, 16, '#f28aa0'); s.px(12, 16, '#f28aa0')
    s.line(2, 15, 6, 16, BK); s.line(17, 16, 21, 15, BK); return s
@sp('fox')
def _():
    s = S(); s.poly([(4, 11), (6, 3), (11, 8)], OR); s.poly([(20, 11), (18, 3), (13, 8)], OR); s.poly([(4, 10), (20, 10), (12, 21)], OR); s.ell(12, 12, 8, 4, OR); s.finish()
    s.poly([(6, 12), (12, 20), (12, 14)], WH); s.poly([(18, 12), (12, 20), (12, 14)], WH); s.rect(11, 18, 12, 19, BK); s.line(7, 12, 9, 13, EYE); s.line(17, 12, 15, 13, EYE); s.px(7, 6, BK); s.px(17, 6, BK); return s
@sp('lantern')
def _():
    s = S(); s.ell(12, 12.5, 7, 8, R); s.finish(); s.rect(8, 2, 15, 4, BK); s.rect(8, 21, 15, 22, BK)
    for y in (7, 10, 13, 16, 19): s.line(6 if y in (10, 13, 16) else 7, y, 18 if y in (10, 13, 16) else 17, y, DR)
    s.rect(11, 9, 13, 16, '#ffd060'); s.px(8, 8, '#ff9a80'); return s
@sp('koi')
def _():
    s = S(); s.line(4, 2, 4, 22, DB, 2); s.ell(13, 8, 8, 3.6, R); s.poly([(20, 8), (23, 4), (23, 12)], R); s.ell(13, 16, 7, 3.2, BL); s.poly([(19, 16), (22, 13), (22, 19)], BL); s.finish()
    s.px(8, 7, WH); s.px(8, 8, EYE); s.px(9, 15, WH); s.px(9, 16, EYE); s.rect(12, 8, 16, 8, '#ffb0a0'); s.rect(12, 16, 15, 16, LB); return s
@sp('chick')
def _():
    s = S(); s.ell(12, 14, 7, 7, YE); s.poly([(5, 15), (19, 15), (17, 21), (7, 21)], CR); s.finish()
    s.line(5, 15, 19, 15, '#b8a888'); s.px(6, 16, '#b8a888'); s.px(18, 16, '#b8a888'); s.px(10, 11, EYE); s.px(14, 11, EYE); s.rect(11, 13, 13, 13, OR); s.px(12, 6, YE); s.px(11, 5, YE); return s
@sp('chicken')
def _():
    s = S(); s.ell(13, 15, 7.5, 6.5, WH); s.disc(9, 8, 4.2, WH); s.poly([(20, 12), (23, 8), (22, 15)], WH); s.finish()
    s.rect(7, 2, 10, 4, R); s.px(8, 1, R); s.rect(4, 8, 5, 9, OR); s.px(3, 9, OR); s.rect(5, 10, 6, 12, R); s.px(9, 7, EYE); s.rect(9, 21, 9, 22, OR); s.rect(14, 21, 14, 22, OR); s.line(11, 15, 17, 17, '#d8d0c8'); return s
@sp('firework')
def _():
    s = S(); s.finish(shade=False, outline=False)
    import math
    for k in range(12):
        a = k * math.pi / 6; c = [R, YE, '#8cc8f0', PK][k % 4]
        s.line(12 + math.cos(a) * 3, 12 + math.sin(a) * 3, 12 + math.cos(a) * 9, 12 + math.sin(a) * 9, c)
        s.px(round(12 + math.cos(a) * 10), round(12 + math.sin(a) * 10), WH)
    s.rect(11, 11, 12, 12, '#ffffff'); return s
@sp('sake')
def _():
    s = S(); s.rect(10, 2, 14, 6, CR); s.ell(12, 15, 7, 7.5, CR); s.rect(6, 19, 18, 21, CR); s.finish()
    s.rect(9, 11, 15, 17, '#2a3a6a'); s.rect(11, 12, 13, 16, WH); s.px(12, 13, '#2a3a6a'); s.px(12, 15, '#2a3a6a'); s.rect(9, 1, 15, 1, R); return s
@sp('shooting')
def _():
    s = S(); s.disc(12, 12, 9.5, WH); s.finish(); s.ring(12, 12, 8, 2, R); s.ring(12, 12, 4.5, 2, R); s.rect(11, 11, 12, 12, R); s.line(14, 10, 22, 2, BK); s.rect(20, 2, 22, 3, R); return s
@sp('purse')
def _():
    s = S(); s.ell(12, 14, 9, 7, PK); s.finish(); s.rect(5, 7, 18, 8, GO); s.disc(9, 5, 1.6, GO); s.disc(14, 5, 1.6, GO); s.rect(5, 7, 18, 7, '#ffd870'); s.rect(9, 12, 14, 14, '#ffb8d0'); return s
@sp('sakura')
def _():
    s = S()
    import math
    for k in range(5):
        a = math.radians(k * 72 - 90); s.ell(12 + math.cos(a) * 5.5, 12 + math.sin(a) * 5.5, 3.8, 3.8, '#ffc4d8')
    s.disc(12, 12, 3.5, '#ffc4d8'); s.finish(); s.disc(12, 12, 1.8, '#e85a8a'); s.px(12, 12, YE)
    for k in range(5):
        a = math.radians(k * 72 - 90); s.px(round(12 + math.cos(a) * 8.4 - .5), round(12 + math.sin(a) * 8.4 - .5), '#e88aaa')
    return s
@sp('torii')
def _():
    s = S(); s.rect(3, 4, 20, 6, R); s.rect(1, 3, 22, 4, R); s.rect(5, 9, 18, 10, R); s.rect(6, 6, 8, 21, R); s.rect(15, 6, 17, 21, R); s.finish(); s.rect(1, 2, 22, 2, BK); s.rect(11, 6, 12, 9, DR); return s
@sp('moon')
def _():
    s = S(); s.disc(12, 12, 9, '#ffe8a0'); s.finish(); s.disc(8, 10, 1.8, '#f0cf78'); s.disc(14, 15, 2.4, '#f0cf78'); s.disc(15, 7, 1.2, '#f0cf78'); s.px(7, 7, WH); return s
@sp('hanafuda')
def _():
    s = S(); s.rect(6, 2, 17, 21, '#2a2a3a'); s.finish(); s.rect(7, 3, 16, 20, '#d8433b'); s.rect(7, 13, 16, 20, '#2a2a3a'); s.disc(14, 9, 3, '#ffe0a0'); s.ell(10, 15, 4, 1.4, '#f7f3ea'); s.ell(14, 17, 3, 1, '#f7f3ea'); return s
@sp('clover')
def _():
    s = S(); s.disc(8, 8, 4, GR); s.disc(16, 8, 4, GR); s.disc(8, 15, 4, GR); s.disc(16, 15, 4, GR); s.line(13, 15, 16, 22, DG, 2); s.finish(); s.px(7, 7, LG); s.px(15, 7, LG); s.px(7, 14, LG); s.px(15, 14, LG); return s
@sp('castle')
def _():
    s = S(); s.rect(6, 15, 17, 21, WH); s.poly([(3, 15), (21, 15), (17, 11), (7, 11)], NV); s.rect(8, 8, 15, 11, WH); s.poly([(5, 8), (19, 8), (15, 4), (9, 4)], NV); s.rect(3, 21, 20, 22, GY); s.finish()
    s.rect(10, 17, 13, 21, DB); s.px(11, 9, BK); s.px(13, 9, BK); s.rect(11, 2, 12, 3, GO); s.px(7, 13, GO); s.px(16, 13, GO); return s
@sp('dragon')
def _():
    s = S(); s.ell(12, 13, 6, 7, GR); s.poly([(6, 10), (2, 6), (5, 13)], LG); s.poly([(18, 10), (22, 6), (19, 13)], LG); s.poly([(9, 7), (8, 2), (11, 6)], YE); s.poly([(15, 7), (16, 2), (13, 6)], YE); s.ell(12, 17, 4, 3, LG); s.finish()
    s.px(9, 11, R); s.px(15, 11, R); s.px(10, 17, DG); s.px(14, 17, DG); s.line(8, 18, 4, 21, '#f6e0a0'); s.line(16, 18, 20, 21, '#f6e0a0'); return s
@sp('oni')
def _():
    s = S(); s.ell(12, 14, 8, 8, R); s.poly([(7, 8), (6, 2), (10, 7)], CR); s.poly([(17, 8), (18, 2), (14, 7)], CR); s.finish()
    s.rect(6, 7, 17, 8, BK); s.line(7, 10, 10, 12, BK); s.line(17, 10, 14, 12, BK); s.px(9, 12, YE); s.px(15, 12, YE); s.rect(8, 17, 16, 18, BK); s.px(9, 16, WH); s.px(15, 16, WH); return s
@sp('rainbow')
def _():
    s = S()
    for k, c in enumerate([R, OR, YE, GR, BL, PU]): s.ring(12, 19, 10 - k * 1.4, 1.5, c)
    s.rect(0, 19, 23, 23, None); s.finish(); s.ell(4, 19, 3, 1.6, WH); s.ell(20, 19, 3, 1.6, WH); return s
@sp('oden')
def _():
    s = S(); s.line(12, 22, 12, 2, TN, 1); s.poly([(12, 3), (17, 9), (7, 9)], '#b8a070'); s.disc(12, 13, 3.6, '#e8d8a8'); s.rect(9, 17, 15, 20, '#a07040'); s.finish(); s.line(12, 22, 12, 21, TN); return s
@sp('yakiimo')
def _():
    s = S(); s.ell(12, 12, 9, 5, '#9a3a6a'); s.finish(); s.ell(14, 10, 4, 2.5, '#f6c445'); s.px(7, 11, '#c86a9a'); s.px(17, 14, '#6a2a4a'); s.line(10, 4, 11, 2, '#e6e6f0'); s.line(14, 4, 13, 1, '#e6e6f0'); return s
@sp('kakigori')
def _():
    s = S(); s.poly([(6, 14), (18, 14), (15, 21), (9, 21)], '#c8e8ff'); s.ell(12, 11, 7, 5.5, WH); s.ell(12, 9, 5, 3, '#f06a8a'); s.finish(); s.rect(10, 16, 14, 18, '#8cc8f0'); s.px(9, 8, '#ffb0c0'); s.line(16, 6, 20, 2, '#f6c445'); return s
@sp('ika')
def _():
    s = S(); s.line(12, 22, 12, 14, TN, 1); s.poly([(12, 2), (17, 9), (16, 15), (8, 15), (7, 9)], '#e0904a'); s.finish()
    for x in (8, 10, 12, 14, 16): s.line(x, 15, x, 18, '#c8703a')
    s.px(10, 10, EYE); s.px(14, 10, EYE); s.rect(9, 5, 15, 5, '#b05a2a'); return s
@sp('turtle')
def _():
    s = S(); s.disc(19, 13, 3, '#8ec76a'); s.ell(6, 18, 2, 1.5, '#8ec76a'); s.ell(17, 18, 2, 1.5, '#8ec76a'); s.ell(11, 13, 8, 6, '#5a8a3a'); s.finish()
    s.px(20, 12, EYE); s.line(7, 11, 15, 11, '#3a6a2a'); s.line(11, 8, 11, 17, '#3a6a2a'); s.px(8, 9, '#8ec76a'); return s
@sp('crab')
def _():
    s = S(); s.ell(12, 14, 7, 5, R); s.disc(4, 8, 3, R); s.disc(20, 8, 3, R); s.finish()
    s.rect(3, 6, 4, 7, '#2a2430'); s.rect(20, 6, 21, 7, '#2a2430'); s.px(10, 11, WH); s.px(14, 11, WH); s.px(10, 12, EYE); s.px(14, 12, EYE)
    for x in (6, 8, 16, 18): s.line(x, 18, x - (1 if x < 12 else -1), 21, DR)
    return s
@sp('pochi')
def _():
    s = S(); s.rect(6, 3, 17, 21, R); s.finish(); s.poly([(6, 3), (17, 3), (12, 9)], DR); s.rect(9, 12, 14, 17, GO); s.px(11, 14, R); s.px(12, 14, R); s.rect(10, 15, 13, 15, R); return s
@sp('bomb')
def _():
    s = S(); s.disc(11, 14, 7.5, BK); s.rect(15, 5, 17, 8, GY); s.finish(); s.px(8, 11, '#6a6478'); s.px(9, 10, '#6a6478'); s.line(17, 5, 19, 2, TN); s.px(20, 1, YE); s.px(21, 2, OR); s.px(19, 0, R); return s
@sp('bee')
def _():
    s = S(); s.ell(8, 7, 4, 3, '#dff2ff'); s.ell(16, 7, 4, 3, '#dff2ff'); s.ell(12, 14, 8, 6, YE); s.finish()
    s.rect(9, 9, 10, 19, BK); s.rect(14, 9, 15, 19, BK); s.px(19, 13, EYE); s.px(19, 15, EYE); s.line(4, 13, 1, 14, BK); return s
@sp('ghost')
def _():
    s = S(); s.ell(12, 10, 7, 7, WH); s.rect(5, 10, 18, 18, WH); s.poly([(5, 18), (8, 22), (10, 18), (13, 22), (15, 18), (18, 22), (18, 18)], WH); s.finish()
    s.rect(9, 9, 9, 11, EYE); s.rect(14, 9, 14, 11, EYE); s.ell(11.5, 15, 2, 1.5, '#5a4a6a'); s.px(7, 6, '#ffffff'); return s
@sp('tanzaku')
def _():
    s = S(); s.line(18, 22, 12, 1, DG, 1); s.line(15, 8, 21, 6, GR); s.line(14, 13, 20, 12, GR); s.rect(5, 6, 9, 18, PK); s.rect(10, 9, 13, 20, LB); s.finish(); s.line(7, 5, 15, 3, DG); s.line(11, 8, 14, 7, DG); return s
@sp('nobori')
def _():
    s = S(); s.line(5, 2, 5, 22, DB, 2); s.rect(7, 4, 17, 21, '#f7f3ea'); s.finish(); s.rect(7, 4, 17, 6, R); s.rect(10, 9, 14, 17, R); s.rect(11, 10, 13, 16, '#f7f3ea'); s.rect(7, 21, 17, 21, R); return s
@sp('taiko')
def _():
    s = S(); s.ell(12, 13, 9, 7, '#c8402a'); s.finish(); s.ell(12, 9, 7.5, 3, CR); s.rect(4, 12, 20, 12, GO)
    for x in (5, 9, 15, 19): s.px(x, 14, GO)
    s.line(3, 2, 8, 7, TN); s.line(21, 2, 16, 7, TN); return s
@sp('piggy')
def _():
    s = S(); s.ell(12, 14, 9, 7, '#f6a8c0'); s.poly([(6, 9), (7, 5), (10, 8)], '#f6a8c0'); s.poly([(18, 9), (17, 5), (14, 8)], '#f6a8c0'); s.ell(5, 19, 2, 2, '#f6a8c0'); s.ell(19, 19, 2, 2, '#f6a8c0'); s.finish()
    s.rect(10, 7, 14, 7, BK); s.ell(16, 15, 2.5, 2, '#f28aa8'); s.px(15, 15, DR); s.px(17, 15, DR); s.px(13, 12, EYE); return s
@sp('tanuki')
def _():
    s = S(); s.disc(6, 7, 3, BR); s.disc(18, 7, 3, BR); s.ell(12, 13, 8.5, 7.5, BR); s.finish()
    s.ell(8, 12, 3, 2.2, DB); s.ell(16, 12, 3, 2.2, DB); s.px(8, 12, WH); s.px(16, 12, WH); s.ell(12, 16, 3.5, 2.5, CR); s.px(12, 15, BK); s.disc(6, 7, 1.2, DB); s.disc(18, 7, 1.2, DB)
    s.poly([(10, 4), (15, 1), (14, 6)], LG); return s
@sp('soroban')
def _():
    s = S(); s.rect(2, 5, 21, 18, DB); s.finish(); s.rect(3, 6, 20, 17, '#e6d6b0'); s.rect(3, 9, 20, 9, DB)
    for x in range(4, 21, 3):
        s.line(x, 6, x, 17, '#8a6a4a'); s.rect(x - 1, 7, x, 7, BR)
        for y in (11, 13, 15): s.rect(x - 1, y, x, y, BR)
    return s
@sp('honey')
def _():
    s = S(); s.ell(12, 14, 7.5, 7, '#e8a830'); s.rect(7, 4, 17, 7, '#c88a3a'); s.finish(); s.rect(6, 6, 18, 7, '#9a6a2a'); s.ell(10, 14, 3, 2, '#ffd068'); s.line(14, 7, 15, 11, '#ffc848', fix=True); s.px(15, 12, '#ffc848'); return s
@sp('misemono')
def _():
    s = S(); s.poly([(12, 2), (22, 10), (2, 10)], R); s.rect(4, 10, 19, 21, '#f7f3ea'); s.finish()
    s.poly([(12, 3), (15, 9), (9, 9)], '#f7f3ea'); s.rect(9, 13, 14, 21, BK); s.rect(4, 10, 19, 11, YE); s.px(12, 1, YE); return s
@sp('dog')
def _():
    s = S(); s.ell(5, 11, 2.5, 5, DB); s.ell(19, 11, 2.5, 5, DB); s.ell(12, 12, 7.5, 7.5, TN); s.finish()
    s.ell(12, 16, 4, 3, CR); s.rect(11, 14, 13, 15, BK); s.px(9, 11, EYE); s.px(15, 11, EYE); s.px(12, 18, '#f28aa0'); return s
@sp('ramen')
def _():
    s = S(); s.ell(12, 13, 10, 3, '#f6e0a0'); s.poly([(2, 13), (22, 13), (18, 21), (6, 21)], R); s.finish()
    s.ell(12, 12.5, 9, 2, '#f0c060'); s.disc(8, 12, 1.8, WH); s.px(8, 12, '#f0a020'); s.rect(13, 11, 16, 12, '#c8806a'); s.rect(5, 16, 19, 16, WH); s.line(14, 9, 21, 1, TN); s.line(16, 9, 22, 2, TN); return s
@sp('bear')
def _():
    s = S(); s.disc(5, 6, 3.5, BR); s.disc(19, 6, 3.5, BR); s.disc(12, 13, 9, BR); s.finish()
    s.disc(5, 6, 1.5, DB); s.disc(19, 6, 1.5, DB); s.ell(12, 16, 4.5, 3.4, TN); s.rect(11, 14, 13, 15, BK); s.px(8, 11, EYE); s.px(16, 11, EYE); return s
@sp('fuji')
def _():
    s = S(); s.poly([(1, 21), (9, 5), (15, 5), (23, 21)], '#4a6aa8'); s.finish(); s.poly([(9, 5), (15, 5), (17, 9), (14, 8), (12, 10), (10, 8), (7, 9)], WH); s.rect(0, 21, 23, 22, '#3a5a8a'); s.disc(20, 4, 2, R); return s
@sp('sun')
def _():
    s = S(); s.disc(12, 12, 6.5, '#f6b030')
    import math
    for k in range(8):
        a = k * math.pi / 4; s.disc(12 + math.cos(a) * 9.5, 12 + math.sin(a) * 9.5, 1.6, '#f68a30')
    s.finish(); s.px(9, 9, '#ffe080'); s.px(10, 9, '#ffe080'); return s
@sp('crystal')
def _():
    s = S(); s.rect(6, 19, 17, 22, DB); s.disc(12, 11, 8, '#a888f0'); s.finish(); s.ell(9, 8, 2.5, 3, '#e8dcff'); s.disc(14, 13, 2, '#7a5ac8'); s.px(15, 12, '#ffffff'); return s
@sp('kadomatsu')
def _():
    s = S()
    for x, h in ((7, 4), (12, 2), (17, 5)): s.poly([(x - 2, 14), (x + 2, 14), (x + 2, h + 3), (x - 2, h)], GR)
    s.poly([(4, 14), (20, 14), (18, 22), (6, 22)], TN); s.finish(); s.line(4, 17, 20, 17, DB); s.line(5, 19, 19, 19, DB); s.disc(6, 13, 1.6, R); s.disc(18, 13, 1.6, R); return s
@sp('hina')
def _():
    s = S(); s.poly([(3, 22), (5, 12), (10, 12), (11, 22)], NV); s.disc(7.5, 9, 3.2, WH); s.poly([(13, 22), (14, 12), (19, 12), (21, 22)], R); s.disc(16.5, 9, 3.2, WH); s.finish()
    s.rect(5, 5, 10, 7, BK); s.rect(14, 5, 19, 7, BK); s.rect(15, 4, 18, 4, GO); s.px(6, 9, EYE); s.px(9, 9, EYE); s.px(15, 9, EYE); s.px(18, 9, EYE); s.rect(7, 13, 8, 21, '#f7f3ea'); s.rect(16, 13, 17, 21, '#f7f3ea'); return s
@sp('mallet')
def _():
    s = S(); s.line(14, 13, 21, 21, TN, 2); s.poly([(3, 7), (12, 2), (17, 11), (8, 16)], GO); s.finish(); s.line(5, 8, 13, 4, '#ffd870'); s.disc(10, 9, 1.4, R); return s
@sp('mirror')
def _():
    s = S(); s.rect(10, 16, 13, 22, DB); s.disc(12, 10, 8, GO); s.finish(); s.disc(12, 10, 6, '#bfe6ff'); s.line(8, 7, 11, 4, '#ffffff'); s.px(14, 12, '#ffffff'); return s
@sp('mame')
def _():
    s = S(); s.poly([(3, 12), (12, 6), (21, 12), (12, 21)], '#c89a5a'); s.finish()
    for (x, y) in [(8, 12), (12, 10), (15, 14), (11, 15), (13, 17)]: s.disc(x, y, 2, '#f0d8a0'); s.px(x - 1, y - 1, WH)
    return s
@sp('senbei')
def _():
    s = S(); s.disc(12, 12, 9, '#d8a050'); s.finish(); s.rect(8, 6, 16, 18, '#2a3a2a'); s.rect(9, 7, 15, 17, '#3a4a3a'); s.px(5, 12, '#8a5a2a'); s.px(18, 9, '#8a5a2a'); s.px(17, 16, '#8a5a2a'); return s
@sp('shika')
def _():
    s = S(); s.line(7, 7, 4, 1, DB, 1); s.line(5, 4, 2, 4, DB); s.line(17, 7, 20, 1, DB); s.line(19, 4, 22, 4, DB); s.ell(12, 13, 6, 7, TN); s.ell(5, 11, 3, 1.6, TN); s.ell(19, 11, 3, 1.6, TN); s.finish()
    s.px(9, 12, EYE); s.px(15, 12, EYE); s.ell(12, 18, 2.4, 1.6, BK); s.px(10, 9, CR); s.px(14, 9, CR); return s
@sp('suzumushi')
def _():
    s = S(); s.ell(13, 14, 7, 4.5, '#6a5232'); s.ell(8, 12, 3.2, 3, '#4a3a22'); s.ell(14, 12, 5, 2.4, '#c8b07a'); s.finish()
    s.line(7, 10, 2, 2, '#3a2a1a'); s.line(8, 10, 6, 1, '#3a2a1a'); s.line(18, 16, 22, 21, '#3a2a1a'); s.line(12, 17, 10, 21, '#3a2a1a'); s.line(16, 17, 17, 21, '#3a2a1a'); s.px(7, 11, '#ffe8a0'); return s
@sp('tentou')
def _():
    s = S(); s.ell(12, 14, 8, 7, R); s.ell(12, 7, 4, 3, BK); s.finish(); s.line(12, 8, 12, 21, BK)
    for (x, y) in [(8, 12), (16, 12), (8, 17), (16, 17), (10, 15), (14, 15)]: s.px(x, y, BK)
    s.px(10, 7, WH); s.px(14, 7, WH); return s
@sp('mikazuki')
def _():
    s = S(); s.disc(12, 12, 9, '#ffe8a0'); s.disc(16, 9, 8, None); s.finish(); s.px(5, 11, WH); s.px(18, 4, YE); s.px(20, 16, WH); return s
@sp('tsubo')
def _():
    s = S(); s.rect(9, 2, 15, 5, '#6a4a8a'); s.ell(12, 13, 8, 8, '#8a6aa8'); s.rect(9, 19, 15, 22, '#6a4a8a'); s.finish(); s.line(5, 12, 19, 12, '#c8b0e8'); s.line(6, 14, 18, 14, '#5a3a7a'); s.px(8, 9, '#d8c8f0'); return s
@sp('fukurou')
def _():
    s = S(); s.poly([(4, 4), (8, 7), (5, 9)], '#8a6a4a'); s.poly([(20, 4), (16, 7), (19, 9)], '#8a6a4a'); s.ell(12, 13, 8, 9, '#8a6a4a'); s.finish()
    s.disc(8, 10, 3, CR); s.disc(16, 10, 3, CR); s.disc(8, 10, 1.6, YE); s.disc(16, 10, 1.6, YE); s.px(8, 10, EYE); s.px(16, 10, EYE); s.poly([(11, 12), (13, 12), (12, 15)], OR); s.ell(12, 18, 4, 3, CR)
    for x in (10, 12, 14): s.px(x, 18, '#b89a7a')
    return s
@sp('koryu')
def _():
    s = S(); s.ell(12, 14, 6, 6, '#6ac8e8'); s.poly([(8, 9), (7, 4), (10, 8)], YE); s.poly([(16, 9), (17, 4), (14, 8)], YE); s.ell(12, 18, 3, 2, '#a8e8ff'); s.finish()
    s.disc(9, 13, 1.6, WH); s.disc(15, 13, 1.6, WH); s.px(9, 13, EYE); s.px(15, 13, EYE); s.px(11, 18, BL); s.px(13, 18, BL); return s
@sp('suika')
def _():
    s = S(); s.ell(12, 13, 10, 6, GR); s.rect(1, 6, 23, 12, None); s.finish(); s.ell(12, 13, 8.5, 4.5, R); s.rect(2, 8, 22, 12, None); s.line(3, 12, 21, 12, '#f0f0d0')
    for x in (7, 10, 13, 16): s.px(x, 14, BK)
    return s
@sp('yabusame')
def _():
    s = S(); s.ring(10, 12, 9, 1.5, BR); s.rect(10, 0, 23, 23, None); s.line(10, 3, 10, 21, '#e8e0d0', fix=True); s.finish(); s.line(4, 12, 21, 12, TN); s.poly([(20, 10), (23, 12), (20, 14)], GY); s.rect(3, 11, 5, 13, R); return s
@sp('kujaku')
def _():
    s = S(); s.ell(12, 10, 10, 8, '#2aa89a'); s.ell(12, 16, 3, 5, '#3a6ad8'); s.disc(12, 9, 2.6, '#3a6ad8'); s.finish()
    for (x, y) in [(5, 8), (8, 4), (12, 3), (16, 4), (19, 8), (6, 13), (18, 13)]: s.disc(x, y, 1.4, YE); s.px(x, y, '#3a3ad8')
    s.px(12, 8, WH); s.poly([(11, 6), (12, 4), (13, 6)], YE); return s
@sp('hanamaru')
def _():
    s = S()
    import math
    for k in range(8):
        a = k * math.pi / 4; s.disc(12 + math.cos(a) * 7, 12 + math.sin(a) * 7, 3.2, '#ff8aa8')
    s.disc(12, 12, 6, '#ff8aa8'); s.finish(); s.ring(12, 12, 5, 1.4, R); s.ring(12, 12, 2.6, 1.2, R); return s
@sp('kazan')
def _():
    s = S(); s.poly([(1, 22), (8, 9), (16, 9), (23, 22)], '#7a5a4a'); s.finish(); s.poly([(8, 9), (16, 9), (14, 12), (10, 12)], R); s.line(12, 8, 12, 2, OR, 2); s.line(9, 7, 6, 2, R); s.line(15, 7, 18, 2, R); s.px(12, 1, YE); s.line(10, 13, 8, 18, OR); s.line(14, 13, 16, 17, OR); return s
@sp('whale')
def _():
    s = S(); s.ell(11, 14, 9, 6, '#3a6ab0'); s.poly([(18, 13), (23, 8), (22, 14), (23, 19)], '#3a6ab0'); s.finish(); s.ell(10, 17, 7, 2, '#a8c8f0'); s.px(6, 12, EYE); s.line(9, 7, 9, 4, LB); s.line(9, 5, 6, 3, LB); s.line(9, 5, 12, 3, LB); return s
@sp('tengu')
def _():
    s = S(); s.ell(12, 13, 8, 8, R); s.poly([(13, 13), (22, 9), (14, 16)], R); s.rect(5, 3, 18, 6, BK); s.finish()
    s.line(6, 9, 10, 11, WH); s.line(18, 9, 14, 11, WH); s.px(9, 12, EYE); s.px(15, 12, EYE); s.ell(12, 19, 5, 2, WH); s.rect(10, 1, 13, 3, BK); return s
@sp('japan')
def _():
    s = S(); s.poly([(16, 2), (20, 4), (17, 9), (13, 13), (9, 17), (4, 21), (2, 19), (7, 14), (11, 10), (14, 6)], '#5aae4a'); s.ell(19, 3, 2.5, 1.6, '#5aae4a'); s.finish(); s.disc(9, 7, 3, R); s.px(8, 6, '#ff8a80'); return s
@sp('butterfly')
def _():
    s = S(); s.ell(7, 8, 5, 5, '#f0a0d0'); s.ell(17, 8, 5, 5, '#f0a0d0'); s.ell(8, 16, 4, 3.5, '#a0c8f0'); s.ell(16, 16, 4, 3.5, '#a0c8f0'); s.finish()
    s.line(12, 5, 12, 19, BK); s.line(11, 4, 9, 1, BK); s.line(13, 4, 15, 1, BK); s.disc(7, 8, 1.6, WH); s.disc(17, 8, 1.6, WH); return s
@sp('sparrow')
def _():
    s = S(); s.ell(12, 13, 8, 6.5, '#a0703a'); s.disc(8, 9, 4, '#7a4a2a'); s.poly([(18, 12), (23, 9), (22, 15)], '#7a4a2a'); s.finish()
    s.ell(10, 15, 4, 2.5, CR); s.px(7, 9, EYE); s.poly([(3, 10), (5, 9), (5, 11)], '#e0a040'); s.ell(8, 12, 1.4, 1, BK); s.line(9, 20, 9, 22, OR); s.line(13, 20, 13, 22, OR); return s
@sp('snail')
def _():
    s = S(); s.ell(10, 18, 9, 3, '#e0c8a0'); s.disc(13, 12, 6.5, '#c8784a'); s.line(4, 16, 3, 10, '#e0c8a0', fix=False); s.finish(); s.ring(13, 12, 4.5, 1.2, '#8a4a2a'); s.ring(13, 12, 2, 1, '#8a4a2a'); s.px(3, 9, EYE); s.px(5, 9, EYE); return s
@sp('octopus')
def _():
    s = S(); s.ell(12, 10, 7, 7, '#e85a6a')
    for x in (6, 9, 12, 15, 18): s.ell(x, 18, 1.6, 4, '#e85a6a')
    s.finish(); s.disc(9, 10, 1.8, WH); s.disc(15, 10, 1.8, WH); s.px(9, 10, EYE); s.px(15, 10, EYE); s.ell(12, 14, 2, 1.4, '#a83040'); s.px(8, 6, '#ffb0b8'); return s
@sp('snake')
def _():
    s = S(); s.line(4, 20, 8, 16, '#5aae4a', 3); s.line(8, 16, 15, 17, '#5aae4a', 3); s.line(15, 17, 18, 11, '#5aae4a', 3); s.line(18, 11, 12, 7, '#5aae4a', 3); s.disc(11, 6, 3.4, '#5aae4a'); s.finish()
    s.px(10, 5, EYE); s.px(12, 5, EYE); s.line(8, 7, 5, 8, R); s.px(9, 17, YE); s.px(15, 15, YE); s.px(17, 11, YE); return s
@sp('sushi')
def _():
    s = S(); s.ell(12, 15, 9, 4.5, WH); s.ell(12, 11, 10, 4, '#f07a5a'); s.finish(); s.line(5, 10, 9, 12, '#ffd0c0'); s.line(10, 9, 14, 11, '#ffd0c0'); s.line(15, 9, 19, 11, '#ffd0c0'); s.rect(10, 9, 13, 18, '#2a3a2a'); return s
@sp('fugu')
def _():
    s = S(); s.disc(12, 12, 8.5, '#f6d070')
    import math
    for k in range(10):
        a = k * math.pi / 5; s.px(round(12 + math.cos(a) * 10 - .5), round(12 + math.sin(a) * 10 - .5), '#c8a040')
    s.finish(); s.ell(12, 16, 6, 3, CR); s.disc(8, 10, 2, WH); s.disc(15, 10, 2, WH); s.px(8, 10, EYE); s.px(15, 10, EYE); s.ell(12, 14, 1.6, 1.2, '#c86040')
    for (x, y) in [(10, 6), (14, 6), (6, 13), (18, 13)]: s.px(x, y, '#8a6a2a')
    return s
@sp('kaminari')
def _():
    s = S(); s.poly([(14, 1), (5, 13), (11, 13), (8, 23), (19, 9), (13, 9), (17, 1)], YE); s.finish(); s.line(13, 3, 8, 11, '#fff6c0'); return s
@sp('eagle')
def _():
    s = S(); s.poly([(1, 9), (12, 12), (23, 9), (18, 15), (12, 18), (6, 15)], '#7a5a3a'); s.disc(12, 9, 3.6, WH); s.finish()
    s.poly([(12, 10), (15, 11), (13, 13)], YE); s.px(11, 8, EYE); s.rect(10, 18, 14, 20, '#7a5a3a'); s.line(10, 21, 9, 23, YE); s.line(14, 21, 15, 23, YE); return s
@sp('wave')
def _():
    s = S(); s.ell(12, 17, 11, 6, '#3a7ad8'); s.disc(9, 10, 7, '#3a7ad8'); s.rect(0, 22, 23, 23, None); s.finish(); s.ring(9, 10, 5.5, 1.6, WH); s.disc(11, 11, 3.2, '#3a7ad8'); s.px(4, 6, WH); s.px(15, 6, WH); s.line(14, 17, 21, 17, LB); return s
@sp('ninja')
def _():
    s = S(); s.disc(12, 12, 9, '#2a2a40'); s.poly([(19, 8), (23, 5), (22, 11)], R); s.finish(); s.rect(5, 10, 19, 13, SK); s.px(9, 11, EYE); s.px(15, 11, EYE); s.line(8, 10, 10, 10, '#1c1420'); s.line(14, 10, 16, 10, '#1c1420'); s.rect(5, 9, 19, 9, R); return s
@sp('kusudama')
def _():
    s = S(); s.disc(12, 11, 8, GO); s.finish(); s.line(12, 3, 12, 19, R); s.line(4, 11, 20, 11, R)
    for (x, y, c) in [(6, 20, R), (9, 22, PK), (15, 21, YE), (18, 19, LB), (3, 17, GR), (21, 15, PK)]: s.rect(x, y, x + 1, y, c)
    s.line(12, 19, 12, 23, R); s.px(8, 7, '#ffe8a0'); return s

# ===================== アイテム =====================
@sp('i_kinchaku')
def _():
    s = S(); s.ell(12, 15, 8, 7, '#8a4aa8'); s.poly([(7, 9), (17, 9), (15, 5), (9, 5)], '#8a4aa8'); s.finish(); s.line(6, 9, 18, 9, GO); s.disc(18, 11, 1.4, GO); s.px(9, 14, '#c88ae0'); return s
@sp('i_bell')
def _():
    s = S(); s.disc(12, 13, 8, GO); s.finish(); s.line(5, 12, 19, 12, '#9a6a1a'); s.rect(11, 15, 12, 19, '#6a4a1a'); s.disc(12, 18, 1.3, '#6a4a1a'); s.rect(10, 3, 13, 5, R); s.px(8, 8, '#fff0a0'); return s
@sp('i_hashi')
def _():
    s = S(); s.line(5, 21, 19, 2, '#c8403a', 2); s.line(9, 22, 22, 5, '#c8403a', 2); s.finish(); s.line(16, 6, 18, 3, GO); s.line(19, 9, 21, 6, GO); return s
@sp('i_paw')
def _():
    s = S(); s.ell(12, 15, 6, 5, '#f6a8c0'); s.disc(5, 9, 2.4, '#f6a8c0'); s.disc(10, 6, 2.4, '#f6a8c0'); s.disc(15, 6, 2.4, '#f6a8c0'); s.disc(20, 9, 2.4, '#f6a8c0'); s.finish(); return s
@sp('i_rod')
def _():
    s = S(); s.line(3, 21, 18, 3, BR, 2); s.finish(); s.line(18, 3, 21, 12, '#e8e8e8'); s.disc(21, 14, 1.6, R); s.disc(6, 18, 2.5, GY); return s
@sp('i_teapot')
def _():
    s = S(); s.ell(12, 14, 8, 6.5, '#5a8a6a'); s.poly([(19, 12), (23, 8), (21, 14)], '#5a8a6a'); s.disc(12, 7, 2, '#5a8a6a'); s.finish(); s.ring(5, 13, 3, 1.2, '#3a5a4a'); s.line(7, 12, 17, 12, '#8ab89a'); return s
@sp('i_basket')
def _():
    s = S(); s.poly([(3, 11), (21, 11), (18, 21), (6, 21)], TN); s.finish(); s.ring(12, 11, 8, 1.5, DB); s.rect(2, 11, 22, 23, None); s.poly([(3, 11), (21, 11), (18, 21), (6, 21)], TN)
    for y in (13, 16, 19): s.line(5, y, 19, y, BR)
    s.ell(9, 10, 2.5, 3, CR); s.ell(14, 10, 2.5, 3, CR); return s
@sp('i_magnet')
def _():
    s = S(); s.ring(12, 10, 8, 4, R); s.rect(3, 10, 21, 23, None); s.rect(4, 10, 7, 18, R); s.rect(17, 10, 20, 18, R); s.finish(); s.rect(4, 16, 7, 18, '#e8e8f0'); s.rect(17, 16, 20, 18, '#e8e8f0'); return s
@sp('i_broom')
def _():
    s = S(); s.line(17, 2, 9, 14, BR, 2); s.poly([(5, 13), (12, 13), (13, 22), (2, 22)], '#e0c070'); s.finish(); s.line(4, 15, 11, 15, R)
    for x in (4, 6, 8, 10, 12): s.line(x, 17, x - 1, 21, '#b89040')
    return s
@sp('i_yoyo')
def _():
    s = S(); s.disc(13, 15, 7.5, '#3ab0e8'); s.finish(); s.line(5, 15, 21, 15, WH); s.disc(13, 15, 2, R); s.line(13, 8, 9, 1, '#f7f3ea'); return s
@sp('i_scroll')
def _():
    s = S(); s.rect(5, 5, 18, 18, CR); s.disc(5, 11.5, 3, R); s.disc(18, 11.5, 3, R); s.finish()
    for y in (8, 11, 14): s.line(8, y, 15, y, '#8a7a5a')
    return s
@sp('i_kite')
def _():
    s = S(); s.poly([(12, 1), (21, 9), (12, 18), (3, 9)], R); s.finish(); s.line(12, 2, 12, 17, '#9a2a2a'); s.line(4, 9, 20, 9, '#9a2a2a'); s.line(12, 18, 8, 23, BK); s.rect(9, 20, 10, 21, YE); return s
@sp('i_tsukimi')
def _():
    s = S(); s.disc(17, 6, 4.5, '#ffe8a0'); s.poly([(4, 19), (20, 19), (18, 22), (6, 22)], TN); s.disc(9, 16, 3, WH); s.disc(15, 16, 3, WH); s.disc(12, 12, 3, WH); s.finish(); return s
@sp('i_box')
def _():
    s = S(); s.poly([(3, 9), (12, 5), (21, 9), (21, 19), (12, 23), (3, 19)], '#c8985a'); s.finish(); s.line(3, 9, 12, 13, '#8a6a3a'); s.line(12, 13, 21, 9, '#8a6a3a'); s.line(12, 13, 12, 22, '#8a6a3a'); s.line(7, 7, 16, 11, '#e8c88a'); return s
@sp('i_candle')
def _():
    s = S(); s.rect(9, 9, 15, 21, WH); s.ell(12, 5, 2.5, 4, OR); s.finish(); s.ell(12, 6, 1.2, 2, YE); s.rect(7, 21, 17, 22, GO); s.line(11, 9, 11, 13, '#e8e0d0'); return s
@sp('i_hourglass')
def _():
    s = S(); s.rect(5, 2, 18, 4, BR); s.rect(5, 19, 18, 21, BR); s.poly([(7, 5), (16, 5), (12, 12), (16, 18), (7, 18), (11, 12)], '#d8ecff'); s.finish(); s.poly([(9, 15), (14, 15), (16, 18), (7, 18)], YE); s.line(12, 12, 12, 15, YE); return s
@sp('i_key')
def _():
    s = S(); s.ring(7, 8, 5, 2.4, GO); s.line(10, 11, 20, 21, GO, 2); s.rect(17, 18, 19, 20, GO); s.rect(14, 15, 16, 17, GO); s.finish(); return s
@sp('i_omamori')
def _():
    s = S(); s.poly([(6, 6), (18, 6), (18, 21), (6, 21)], R); s.poly([(6, 6), (12, 2), (18, 6)], R); s.finish(); s.rect(8, 9, 15, 17, GO); s.rect(9, 10, 14, 16, R); s.rect(11, 11, 12, 15, GO); s.line(12, 0, 12, 3, WH); return s
@sp('i_bento')
def _():
    s = S(); s.rect(2, 6, 21, 19, '#2a2a3a'); s.finish(); s.rect(3, 7, 11, 18, WH); s.rect(12, 7, 20, 12, '#f0c060'); s.rect(12, 13, 20, 18, GR); s.disc(7, 12, 1.6, R); s.rect(12, 13, 20, 13, '#2a2a3a'); return s
@sp('i_sparkler')
def _():
    s = S(); s.line(4, 21, 14, 9, '#8a6a9a', 1); s.finish(shade=False)
    for (x, y) in [(16, 4), (20, 7), (19, 11), (13, 4), (17, 13)]: s.line(15, 8, x, y, YE)
    s.disc(15, 8, 1.6, WH); return s
@sp('i_mayoke')
def _():
    s = S(); s.disc(12, 12, 9, '#2a5ad8'); s.finish(); s.disc(12, 12, 6.5, WH); s.disc(12, 12, 4, '#5ab0f0'); s.disc(12, 12, 2, BK); s.px(10, 10, WH); return s
@sp('i_pot')
def _():
    s = S(); s.poly([(5, 13), (19, 13), (17, 22), (7, 22)], '#c86a3a'); s.ell(8, 8, 4, 2.5, GR); s.ell(16, 7, 4, 2.5, GR); s.line(12, 13, 12, 5, DG, 1); s.finish(); s.rect(4, 13, 20, 14, '#e08a5a'); return s
@sp('i_onsen')
def _():
    s = S(); s.ell(12, 18, 10, 4, '#7ac8e8'); s.finish()
    for x in (6, 12, 18): s.line(x, 13, x - 2, 9, R); s.line(x - 2, 9, x + 1, 5, R); s.line(x + 1, 5, x - 1, 1, R)
    return s
@sp('i_yukata')
def _():
    s = S(); s.poly([(2, 7), (8, 3), (12, 7), (16, 3), (22, 7), (20, 12), (17, 11), (17, 22), (7, 22), (7, 11), (4, 12)], '#4a6ad8'); s.finish(); s.line(8, 4, 12, 12, WH); s.line(16, 4, 12, 12, WH); s.rect(7, 13, 17, 15, YE)
    for (x, y) in [(9, 18), (15, 19), (5, 9)]: s.px(x, y, WH)
    return s
@sp('i_teddy')
def _():
    s = S(); s.disc(6, 6, 2.6, BR); s.disc(18, 6, 2.6, BR); s.disc(12, 10, 6, BR); s.ell(12, 18, 6, 5, BR); s.finish(); s.ell(12, 12, 2.5, 1.8, TN); s.px(12, 11, BK); s.px(10, 9, EYE); s.px(14, 9, EYE); s.rect(9, 14, 15, 15, R); return s
@sp('i_bucket')
def _():
    s = S(); s.poly([(4, 8), (20, 8), (18, 21), (6, 21)], '#6a8ad8'); s.finish(); s.ring(12, 9, 8, 1.2, GY); s.rect(3, 9, 21, 23, None); s.poly([(4, 8), (20, 8), (18, 21), (6, 21)], '#6a8ad8'); s.ell(12, 9, 7, 1.4, '#a8d8ff'); s.rect(6, 13, 18, 14, '#4a6ab8'); return s
@sp('i_slot')
def _():
    s = S(); s.rect(3, 3, 19, 21, R); s.finish(); s.rect(5, 7, 17, 13, WH); s.rect(6, 8, 8, 12, YE); s.rect(10, 8, 12, 12, YE); s.rect(14, 8, 16, 12, YE); s.line(20, 6, 21, 13, GY); s.disc(21, 5, 1.5, R); s.rect(6, 16, 16, 18, GO); return s
@sp('i_tsuzura')
def _():
    s = S(); s.rect(3, 7, 20, 20, '#3a4a6a'); s.rect(2, 5, 21, 8, '#4a5a7a'); s.finish()
    for x in range(5, 20, 3): s.line(x, 9, x, 19, '#5a6a8a')
    s.rect(10, 12, 13, 14, GO); return s
@sp('i_kawaraban')
def _():
    s = S(); s.rect(4, 3, 19, 21, CR); s.finish(); s.rect(6, 5, 17, 7, BK)
    for y in (10, 13, 16, 19): s.line(6, y, 17, y, '#8a7a6a')
    s.rect(13, 9, 17, 14, R); return s
@sp('i_hanakazari')
def _():
    s = SP['sakura']()
    s.rect(0, 0, 23, 23, None); s2 = S(); s2.ell(12, 12, 9, 9, '#ff9ccf')
    import math
    for k in range(6):
        a = k * math.pi / 3; s2.disc(12 + math.cos(a) * 7, 12 + math.sin(a) * 7, 3.6, '#ffc4dd')
    s2.finish(); s2.disc(12, 12, 3, YE); s2.disc(12, 12, 1.5, OR); return s2
@sp('i_hone')
def _():
    s = S(); s.line(6, 18, 18, 6, WH, 3); s.disc(4, 17, 2.2, WH); s.disc(7, 20, 2.2, WH); s.disc(17, 4, 2.2, WH); s.disc(20, 7, 2.2, WH); s.finish(); return s
@sp('i_tebukuro')
def _():
    s = S(); s.ell(12, 13, 6, 7, '#e8d8b0'); s.ell(5, 12, 2, 3, '#e8d8b0'); s.rect(7, 18, 17, 22, '#c8403a'); s.finish(); s.line(9, 6, 9, 11, '#b8a880'); s.line(12, 6, 12, 11, '#b8a880'); s.line(15, 6, 15, 11, '#b8a880'); return s
@sp('i_horagai')
def _():
    s = S(); s.poly([(3, 18), (8, 6), (16, 3), (21, 10), (14, 20)], '#f0d8b0'); s.finish(); s.line(8, 7, 15, 18, '#c8a070'); s.line(12, 5, 18, 14, '#c8a070'); s.rect(2, 18, 5, 21, R); return s
@sp('i_telescope')
def _():
    s = S(); s.line(3, 16, 19, 6, '#c8a050', 4); s.finish(); s.line(4, 17, 6, 15, BK); s.line(9, 13, 9, 23, BR); s.line(9, 18, 4, 23, BR); s.line(9, 18, 14, 23, BR); s.px(21, 4, YE); return s
@sp('i_naruto')
def _():
    s = S(); s.ell(12, 12, 9, 8, WH); s.finish(); s.ring(12, 12, 6, 1.4, '#f06a9a'); s.ring(12, 12, 3, 1.2, '#f06a9a'); s.px(12, 12, '#f06a9a'); return s
@sp('i_ofuda')
def _():
    s = S(); s.rect(7, 2, 16, 22, '#f6ecd0'); s.finish(); s.rect(8, 3, 15, 4, R); s.line(11, 6, 11, 20, R); s.line(12, 8, 14, 8, R); s.line(9, 13, 14, 13, R); s.line(10, 17, 13, 17, R); return s
@sp('i_andon')
def _():
    s = S(); s.rect(6, 4, 17, 20, '#f6e0a0'); s.finish(); s.rect(5, 3, 18, 4, DB); s.rect(5, 20, 18, 21, DB); s.line(6, 4, 6, 20, DB); s.line(17, 4, 17, 20, DB); s.line(11, 4, 11, 20, '#c8a060'); s.disc(12, 12, 3, '#ffd060'); s.rect(7, 22, 8, 23, DB); s.rect(15, 22, 16, 23, DB); return s
@sp('i_ticket')
def _():
    s = S(); s.rect(2, 6, 21, 17, '#f6c445'); s.finish(); s.disc(2, 11.5, 2, None); s.disc(21, 11.5, 2, None); s.line(15, 7, 15, 16, '#c89020'); s.rect(5, 9, 12, 10, R); s.rect(5, 13, 10, 14, R); return s
@sp('i_gem')
def _():
    s = S(); s.poly([(6, 4), (18, 4), (22, 9), (12, 21), (2, 9)], '#4ad8e8'); s.finish(); s.line(2, 9, 22, 9, '#2aa8c8'); s.line(9, 4, 12, 21, '#8af0ff'); s.line(15, 4, 12, 21, '#2aa8c8'); s.px(7, 6, WH); return s
@sp('i_trophy')
def _():
    s = S(); s.poly([(6, 3), (18, 3), (17, 12), (12, 15), (7, 12)], GO); s.ring(5, 7, 3, 1.4, GO); s.ring(19, 7, 3, 1.4, GO); s.rect(10, 15, 13, 18, GO); s.rect(7, 18, 16, 21, BR); s.finish(); s.line(9, 5, 9, 10, '#ffe8a0'); return s
@sp('i_yobirin')
def _():
    s = S(); s.ell(12, 14, 8, 6, GO); s.rect(3, 15, 21, 18, GO); s.rect(11, 5, 12, 8, GO); s.finish(); s.rect(2, 18, 22, 20, BR); s.px(8, 11, '#ffe8a0'); return s
@sp('i_hinode')
def _():
    s = S(); s.disc(12, 15, 7, R); s.rect(0, 15, 23, 23, None); s.finish(); s.rect(0, 16, 23, 17, '#3a6ab0'); s.rect(2, 19, 21, 19, '#3a6ab0'); s.line(12, 4, 12, 6, OR); s.line(4, 8, 6, 10, OR); s.line(20, 8, 18, 10, OR); return s
@sp('i_crown')
def _():
    s = S(); s.poly([(3, 18), (3, 7), (8, 12), (12, 4), (16, 12), (21, 7), (21, 18)], GO); s.finish(); s.disc(12, 14, 1.6, R); s.disc(7, 15, 1.2, BL); s.disc(17, 15, 1.2, GR); s.rect(3, 18, 21, 19, '#c88a1a'); return s
@sp('i_compass')
def _():
    s = S(); s.disc(12, 12, 9, GO); s.finish(); s.disc(12, 12, 7, CR); s.poly([(12, 5), (14, 12), (10, 12)], R); s.poly([(12, 19), (14, 12), (10, 12)], '#5a5a6a'); s.px(12, 12, GO); return s
@sp('i_wand')
def _():
    s = S(); s.line(4, 21, 15, 10, '#7a5ac8', 2); s.finish(); s.poly([(17, 3), (18.5, 7), (22.5, 7.5), (19.5, 10), (20.5, 14), (17, 12), (13.5, 14), (14.5, 10), (11.5, 7.5), (15.5, 7)], YE); return s

# ===================== 大家の気まぐれ =====================
@sp('c_raise')
def _():
    s = S(); s.rect(2, 2, 21, 21, WH); s.finish(); s.line(4, 18, 9, 13, R, 2); s.line(9, 13, 12, 15, R, 2); s.line(12, 15, 19, 6, R, 2); s.poly([(15, 5), (20, 5), (20, 10)], R); return s
@sp('c_hurry')
def _():
    s = S(); s.disc(12, 13, 8.5, WH); s.rect(10, 1, 13, 3, GY); s.finish(); s.ring(12, 13, 8.5, 1.4, R); s.line(12, 13, 12, 7, BK); s.line(12, 13, 16, 15, BK); return s
@sp('c_soldout')
def _():
    s = S(); s.disc(12, 12, 9.5, R); s.finish(); s.disc(12, 12, 6.5, WH); s.line(7, 7, 17, 17, R, 2); return s
@sp('c_rats')
def _(): return SP['mouse']()
@sp('c_fog')
def _():
    s = S(); s.ell(9, 9, 6, 3, '#d8dce8'); s.ell(15, 14, 7, 3, '#c8ccd8'); s.ell(8, 19, 6, 2.5, '#b8bccc'); s.finish(); return s
@sp('c_tax')
def _():
    s = S(); s.rect(3, 6, 20, 17, '#8ac870'); s.finish(); s.disc(11.5, 11.5, 3, '#5a9a4a'); s.line(16, 3, 21, 0, '#e8e8f0'); s.line(5, 3, 2, 0, '#e8e8f0'); return s
@sp('c_cold')
def _():
    s = S(); s.finish(shade=False, outline=False)
    import math
    for k in range(3):
        a = k * math.pi / 3; s.line(12 - math.cos(a) * 9, 12 - math.sin(a) * 9, 12 + math.cos(a) * 9, 12 + math.sin(a) * 9, '#8cd8ff', 2)
    s.disc(12, 12, 2, WH); return s
@sp('c_seal')
def _():
    s = S(); s.ring(12, 9, 5, 2, GY); s.rect(5, 10, 18, 21, GO); s.finish(); s.rect(11, 13, 12, 17, '#6a4a1a'); s.disc(11.5, 13, 1.5, '#6a4a1a'); return s

# ===================== UI =====================
@sp('u_house')
def _():
    s = S(); s.poly([(2, 11), (12, 3), (22, 11)], R); s.rect(5, 11, 18, 21, CR); s.finish(); s.rect(10, 14, 13, 21, BR); s.rect(15, 13, 17, 15, LB); return s
@sp('u_bag')
def _():
    s = S(); s.rect(4, 8, 19, 21, '#c8403a'); s.finish(); s.ring(12, 8, 4, 1.4, DB); s.rect(7, 8, 17, 23, None); s.rect(4, 8, 19, 21, '#c8403a'); s.rect(4, 12, 19, 13, '#9a2a2a'); s.rect(10, 12, 13, 15, GO); return s
@sp('u_reroll')
def _():
    s = S(); s.ring(12, 12, 8, 2.6, '#5ab0e8'); s.rect(13, 1, 23, 11, None); s.poly([(13, 2), (20, 5), (14, 9)], '#5ab0e8'); s.finish(); return s
@sp('u_cut')
def _():
    s = S(); s.line(5, 4, 17, 18, '#c8ccd8', 2); s.line(19, 4, 7, 18, '#c8ccd8', 2); s.ring(6, 19, 3, 1.4, R); s.ring(18, 19, 3, 1.4, R); s.finish(); return s
@sp('u_quest')
def _(): return SP['i_scroll']()
@sp('u_curse')
def _():
    s = S(); s.disc(12, 13, 8, PU); s.poly([(5, 9), (4, 2), (9, 6)], PU); s.poly([(19, 9), (20, 2), (15, 6)], PU); s.finish(); s.line(8, 11, 10, 12, YE); s.line(16, 11, 14, 12, YE); s.line(8, 16, 16, 16, BK); s.px(9, 17, WH); s.px(15, 17, WH); return s
@sp('u_eat')
def _():
    s = S(); s.line(7, 3, 7, 21, GY, 2); s.line(16, 3, 16, 21, GY, 2); s.finish(); s.line(5, 3, 5, 8, GY); s.line(9, 3, 9, 8, GY); s.ell(16, 7, 2.4, 4, GY); return s
@sp('u_spark')
def _():
    s = S(); s.finish(shade=False, outline=False); s.poly([(12, 1), (14, 10), (23, 12), (14, 14), (12, 23), (10, 14), (1, 12), (10, 10)], YE); s.px(12, 12, WH); return s
@sp('u_puff')
def _():
    s = S(); s.disc(8, 13, 4.5, '#d8dce8'); s.disc(14, 10, 5, '#e8ecf4'); s.disc(16, 16, 4, '#c8ccd8'); s.finish(); return s
@sp('u_gift')
def _():
    s = S(); s.rect(4, 9, 19, 21, R); s.rect(3, 7, 20, 10, '#e85a4a'); s.finish(); s.rect(11, 7, 12, 21, GO); s.line(11, 7, 7, 3, GO); s.line(12, 7, 16, 3, GO); return s
@sp('u_check')
def _():
    s = S(); s.line(4, 12, 9, 17, GR, 3); s.line(9, 17, 19, 6, GR, 3); s.finish(); return s
@sp('u_lock')
def _(): return SP['c_seal']()
@sp('u_book')
def _():
    s = S(); s.rect(3, 4, 11, 19, CR); s.rect(12, 4, 20, 19, CR); s.finish(); s.line(11, 4, 11, 20, BR); s.line(12, 4, 12, 20, BR)
    for y in (8, 11, 14): s.line(5, y, 9, y, GY); s.line(14, y, 18, y, GY)
    return s
@sp('u_sound')
def _():
    s = S(); s.poly([(3, 9), (8, 9), (13, 4), (13, 20), (8, 15), (3, 15)], CR); s.finish(); s.ring(13, 12, 6, 1.2, CR); s.ring(13, 12, 9, 1.2, CR); s.rect(5, 0, 13, 23, None); s.poly([(3, 9), (8, 9), (13, 4), (13, 20), (8, 15), (3, 15)], CR); s.rect(4, 10, 7, 14, '#c8b890'); return s
@sp('u_mute')
def _():
    s = S(); s.poly([(3, 9), (8, 9), (13, 4), (13, 20), (8, 15), (3, 15)], GY); s.finish(); s.line(15, 9, 21, 15, R, 2); s.line(21, 9, 15, 15, R, 2); return s
@sp('u_fast')
def _():
    s = S(); s.poly([(3, 5), (12, 12), (3, 19)], YE); s.poly([(12, 5), (21, 12), (12, 19)], YE); s.finish(); return s
@sp('u_menu')
def _():
    s = S(); s.rect(3, 5, 20, 7, CR); s.rect(3, 11, 20, 13, CR); s.rect(3, 17, 20, 19, CR); s.finish(); return s
@sp('u_daily')
def _():
    s = S(); s.rect(3, 5, 20, 21, WH); s.rect(3, 5, 20, 9, R); s.finish(); s.rect(7, 3, 8, 6, GY); s.rect(15, 3, 16, 6, GY); s.rect(10, 12, 13, 18, R); s.rect(10, 12, 11, 12, R); return s
@sp('u_dice')
def _(): return SP['dice']()
@sp('u_story')
def _(): return SP['u_book']()
@sp('u_trophy')
def _(): return SP['i_trophy']()
@sp('u_crown')
def _(): return SP['i_crown']()
@sp('u_lantern')
def _(): return SP['lantern']()
@sp('u_coin')
def _(): return SP['coin']()
@sp('u_blank')
def _():
    s = S(); s.finish(shade=False, outline=False); return s
