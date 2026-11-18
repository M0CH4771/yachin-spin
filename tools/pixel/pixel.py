# 32x32 ドット絵の描画ツール（自動の輪郭と陰影つき）
# 既存の絵は 24 マス基準の座標で描かれているので、S() は座標を 4/3 倍して 32 マスに描く。
# 新しく 32 マスで直接描くときは S(native=True)。
import math
N = 32

def hx(c): c = c.lstrip('#'); return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
def tohex(t): return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(v)))) for v in t)
def dark(c, f=0.25): r, g, b = hx(c); return tohex((r * (1 - f), g * (1 - f), b * (1 - f) * 0.95 + 8 * f))
def light(c, f=0.2): r, g, b = hx(c); return tohex((r + (255 - r) * f, g + (255 - g) * f, b + (255 - b) * f * 0.9))

class S:
    def __init__(s, native=False):
        s.K = 1.0 if native else N / 24
        s.g = [[None] * N for _ in range(N)]
        s.fix = [[False] * N for _ in range(N)]
    def _set(s, X, Y, c, fix):
        if 0 <= X < N and 0 <= Y < N:
            s.g[Y][X] = c
            if fix: s.fix[Y][X] = True
    def _cells(s, a, b):
        # 論理座標 a..b（両端ふくむ）に当たるマス。四捨五入で割り当てるので左右対称がくずれない
        lo = int(round(a * s.K)); hi = int(round((b + 1) * s.K)) - 1
        return range(lo, max(hi, lo) + 1)
    def px(s, x, y, c, fix=False):
        x, y = int(x), int(y)
        for Y in s._cells(y, y):
            for X in s._cells(x, x): s._set(X, Y, c, fix)
    def rect(s, x0, y0, x1, y1, c, fix=False):
        for Y in s._cells(int(y0), int(y1)):
            for X in s._cells(int(x0), int(x1)): s._set(X, Y, c, fix)
    def _each(s):
        for Y in range(N):
            for X in range(N): yield X, Y, (X + .5) / s.K, (Y + .5) / s.K
    def ell(s, cx, cy, rx, ry, c, fix=False):
        for X, Y, x, y in s._each():
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1: s._set(X, Y, c, fix)
    def disc(s, cx, cy, r, c, fix=False): s.ell(cx, cy, r, r, c, fix)
    def ring(s, cx, cy, r, w, c, fix=False):
        for X, Y, x, y in s._each():
            if r - w <= math.hypot(x - cx, y - cy) <= r: s._set(X, Y, c, fix)
    def poly(s, pts, c, fix=False):
        for X, Y, px, py in s._each():
            inside = False; j = len(pts) - 1
            for i in range(len(pts)):
                xi, yi = pts[i]; xj, yj = pts[j]
                if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi + 1e-9) + xi: inside = not inside
                j = i
            if inside: s._set(X, Y, c, fix)
    def line(s, x0, y0, x1, y1, c, w=1, fix=True):
        K = s.K
        # 論理座標のピクセル中心どうしを結ぶ
        X0, Y0, X1, Y1 = (x0 + .5) * K - .5, (y0 + .5) * K - .5, (x1 + .5) * K - .5, (y1 + .5) * K - .5
        W = max(1, int(round(w * K)))
        n = int(max(abs(X1 - X0), abs(Y1 - Y0)) * 2) + 1
        for k in range(n + 1):
            t = k / n
            x, y = X0 + (X1 - X0) * t, Y0 + (Y1 - Y0) * t
            bx, by = int(round(x - .01)) - (W - 1) // 2, int(round(y - .01)) - (W - 1) // 2
            for dy in range(W):
                for dx in range(W): s._set(bx + dx, by + dy, c, fix)
    def finish(s, shade=True, outline=True, ol=None):
        g = s.g
        out = [row[:] for row in g]
        filled = lambda x, y: 0 <= x < N and 0 <= y < N and g[y][x] is not None
        if shade:
            for y in range(N):
                for x in range(N):
                    c = g[y][x]
                    if c is None or s.fix[y][x]: continue
                    if not filled(x + 1, y) or not filled(x, y + 1) or not filled(x + 1, y + 1): out[y][x] = dark(c, 0.22)
                    elif not filled(x - 1, y) or not filled(x, y - 1): out[y][x] = light(c, 0.28)
        if outline:
            for y in range(N):
                for x in range(N):
                    if g[y][x] is not None: continue
                    nb = [g[yy][xx] for xx, yy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)) if 0 <= xx < N and 0 <= yy < N and g[yy][xx] is not None]
                    if nb: out[y][x] = ol or dark(nb[0], 0.68)
        s.g = out
        s.fix = [[False] * N for _ in range(N)]
        return s
