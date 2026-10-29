import math
from lib import *


def lrfd(l):
    return 0.658 ** (l * l) if l <= 1.5 else 0.877 / l ** 2


def crc(l):
    return 1 - l * l / 4 if l <= math.sqrt(2) else 1 / l ** 2


def asd_fa(l):
    r2 = math.sqrt(2)
    if l <= r2:
        x = l / r2
        FS = 5 / 3 + 3 * x / 8 - x ** 3 / 8
        return (1 - l * l / 4) / FS
    return (12 / 23) / l ** 2


class Plot:
    def __init__(s, x0, y0, w, h, xmax, ymax, xmin=0, ymin=0):
        s.x0, s.y0, s.w, s.h, s.xmax, s.ymax, s.xmin, s.ymin = x0, y0, w, h, xmax, ymax, xmin, ymin

    def X(s, v): return s.x0 + (v - s.xmin) / (s.xmax - s.xmin) * s.w
    def Y(s, v): return s.y0 - (v - s.ymin) / (s.ymax - s.ymin) * s.h

    def axes(s, xt, yt, xl, yl, fmt=lambda v: f'{v:g}'):
        o = []
        for v in yt:
            o.append(L(s.x0, s.Y(v), s.x0 + s.w, s.Y(v), GRID, 1))
            o.append(T(s.x0 - 7, s.Y(v) + 4, fmt(v), 11, MUT, 'end'))
        for v in xt:
            o.append(L(s.X(v), s.y0, s.X(v), s.y0 + 4, INK, 1))
            o.append(T(s.X(v), s.y0 + 17, fmt(v), 11, MUT, 'middle'))
        o.append(L(s.x0, s.y0, s.x0 + s.w, s.y0, INK, 1.4))
        o.append(L(s.x0, s.y0, s.x0, s.y0 - s.h, INK, 1.4))
        o.append(T(s.x0 + s.w, s.y0 + 34, xl, 12.5, INK, 'end'))
        o.append(T(s.x0 - 4, s.y0 - s.h - 10, yl, 12.5, INK))
        return ''.join(o)

    def curve(s, fn, a, b, n=240, clip=None, **kw):
        pts = []
        segs = []
        for i in range(n + 1):
            v = a + (b - a) * i / n
            yv = fn(v)
            if clip is not None and yv > clip:
                if pts:
                    segs.append(pts); pts = []
                continue
            pts.append((s.X(v), s.Y(yv)))
        if pts:
            segs.append(pts)
        return ''.join(P(p, **kw) for p in segs if len(p) > 1)


# ---------------------------------------------------------------- 6-1
def fig6_1():
    W, H = 720, 396
    o = []
    o.append(T(20, 26, '殘留應力分布（熱軋 H 型鋼，Lehigh 模型）', 14.5, INK, weight='bold'))
    cx, bf, d, tf, tw = 150, 200, 150, 14, 9
    yt = 120                    # top of top flange
    yb = yt + d
    # section
    o.append(R(cx - bf / 2, yt, bf, tf, STEEL2, '#546e7a', 1.2))
    o.append(R(cx - bf / 2, yb - tf, bf, tf, STEEL2, '#546e7a', 1.2))
    o.append(R(cx - tw / 2, yt + tf, tw, d - 2 * tf, STEEL2, '#546e7a', 1.2))
    # flange diagram above top flange: compression plotted up (red), tension down (blue)
    base = 78; amp = 30          # 0.3 Fy -> 30 px
    def sig_f(xr):               # xr in [-1,1] across the flange, compression positive
        u = 1 - abs(xr)          # 0 at tip, 1 at centre
        return 0.3 * (1 - 2 * u)
    pts = [(cx + bf / 2 * xr, base - sig_f(xr) / 0.3 * amp) for xr in [-1 + i / 100 for i in range(201)]]
    # fill pos / neg separately
    comp = [(x, min(y, base)) for x, y in pts]; tens = [(x, max(y, base)) for x, y in pts]
    o.append(P([(cx - bf / 2, base)] + comp + [(cx + bf / 2, base)], c=None, fill=COMPM, close=True, op=0.85))
    o.append(P([(cx - bf / 2, base)] + tens + [(cx + bf / 2, base)], c=None, fill=ACM, close=True, op=0.85))
    o.append(P(pts, INK, 1.2)); o.append(L(cx - bf / 2 - 8, base, cx + bf / 2 + 8, base, INK, 1))
    o.append(T(cx - bf / 2, base - amp - 6, '−0.3*F*_{y}（壓）', 12, COMP, 'middle'))
    o.append(T(cx + bf / 2, base - amp - 6, '−0.3*F*_{y}', 12, COMP, 'middle'))
    o.append(T(cx + 8, base + amp + 2, '+0.3*F*_{y}（拉）', 12, AC, 'start'))
    # web diagram right of the web: sigma = -0.15(1-3 eta^2) (compression positive -> plot to the right)
    wx = cx + 72
    es = [-1 + i / 50 for i in range(101)]
    wp = [(wx + 0.15 * (1 - 3 * e * e) / 0.3 * 30, yt + tf + (d - 2 * tf) * (e + 1) / 2) for e in es]
    o.append(P([(wx, wp[0][1])] + [(max(x, wx), y) for x, y in wp] + [(wx, wp[-1][1])], c=None, fill=COMPM, close=True, op=0.85))
    o.append(P([(wx, wp[0][1])] + [(min(x, wx), y) for x, y in wp] + [(wx, wp[-1][1])], c=None, fill=ACM, close=True, op=0.85))
    o.append(P(wp, INK, 1.1)); o.append(L(wx, yt + tf - 6, wx, yb - tf + 6, INK, 1))
    o.append(T(wx + 22, yt + d / 2 + 4, '腹板：兩端拉、中央壓', 11, MUT))
    o.append(T(20, 362, '冷卻順序：翼板端部先冷 → 被後冷的翼腹交界拉住 → 端部殘留<壓>、交界殘留<拉>'.replace('<', '').replace('>', ''), 12.5, INK))
    o.append(T(20, 384, '每片板各自積分為零（自相平衡）：∫σ_{r} *dA* = 0。圖中數值為常用簡化值，銲接組合斷面可達 0.5*F*_{y}。', 11.5, MUT))
    # ---- right: yield progression of the flange
    o.append(L(372, 16, 372, 336, GRID, 1.5))
    x0 = 392
    o.append(T(x0, 26, '外加均勻壓應變後：翼板端部「提早退場」', 14.5, INK, weight='bold'))
    o.append(T(x0, 46, '端部總應力 = *f* + 0.3*F*_{y}，先達 *F*_{y} 者先降伏（*E*_{t} = 0）', 11.5, MUT))
    rows = [0.7, 0.85, 0.95, 1.0]
    fw = 150
    o.append(T(x0 + 78 + 75, 72, '翼板（俯視）', 11.5, MUT, 'middle'))
    o.append(T(x0 + 254, 72, '弱軸 *I*_{e}/*I*', 11.5, MUT, 'middle'))
    o.append(T(x0 + 304, 72, '強軸', 11.5, MUT, 'middle'))
    for i, fr in enumerate(rows):
        y = 92 + i * 46
        u = max(0.0, min(1.0, (fr - 0.7) / 0.6))       # yielded fraction of half flange from tip
        o.append(T(x0, y + 31, f'*f* = {fr:.2f}*F*_{{y}}', 12, INK, 'start'))
        bx = x0 + 78
        o.append(R(bx, y + 20, fw, 12, '#fff', '#546e7a', 1))
        yl = fw / 2 * u
        if yl > 0:
            o.append(R(bx, y + 20, yl, 12, '#37474f', None)); o.append(R(bx + fw - yl, y + 20, yl, 12, '#37474f', None))
        weak = (1 - u) ** 3; strong = 1 - u
        o.append(T(x0 + 274, y + 31, f'{weak:.2f}', 13.5, COMP if weak < 0.99 else INK, 'end', 'bold'))
        o.append(T(x0 + 316, y + 31, f'{strong:.2f}', 13.5, INK, 'end'))
    o.append(T(x0, 286, '黑＝已降伏。*f* ≤ 0.7*F*_{y} 前全斷面彈性（比例限 ≈ 0.7*F*_{y}）。', 11.5, MUT))
    o.append(T(x0, 306, '弱軸 ∝ 寬度³ → 掉得最快；強軸（略去腹板）∝ 寬度。', 12.5, COMP, weight='bold'))
    o.append(T(x0, 328, '降伏寬度 *u* = (*f*/*F*_{y} − 0.7)/0.6（半翼板比例）', 11.5, MUT))
    return svg(W, H, '\n'.join(o), '殘留應力分布與翼板逐步降伏')


# ---------------------------------------------------------------- 6-2 (new)  SS-2024-1
def fig6_2():
    W, H = 720, 330
    o = []
    p = Plot(64, 280, 400, 240, 2.2, 1.1)
    o.append(p.axes([0, 0.5, 1.0, 1.5, 2.0], [0, 0.25, 0.5, 0.75, 1.0], 'λ = (*KL*/π*r*)√(*F*_{y}/*E*)', '*F*_{cr}/*F*_{y}'))
    ideal = lambda l: min(1.0, 1 / l ** 2) if l > 0 else 1.0
    o.append(p.curve(ideal, 0.01, 2.2, c=STEEL, w=2, dash='6 4'))
    o.append(p.curve(lrfd, 0, 2.2, c=COMP, w=1.4, op=0.8))
    l1, l2, l3 = math.sqrt(0.485), math.sqrt(0.485 / 0.5), math.sqrt(2)
    def ss(l):
        if l <= l1: return 1.0
        if l <= l2: return 0.485 / l ** 2
        if l <= l3: return 0.5
        return 1 / l ** 2
    o.append(p.curve(ss, 0, 2.2, n=440, c=AC, w=3.4))
    for (lx, ly, nm, dxl, dyl, anc) in ((l1, 1.0, 'A', 4, -10, 'start'), (l2, 0.5, 'B', -6, -10, 'end'), (l3, 0.5, 'C', 6, -10, 'start')):
        o.append(C(p.X(lx), p.Y(ly), 4.5, '#fff', AC, 2))
        o.append(T(p.X(lx) + dxl, p.Y(ly) + dyl, f'{nm} ({lx:.3f}, {ly:.3f})', 11.5, AC, anc, 'bold'))
    o.append(T(p.X(1.2), p.Y(0.5) + 18, '強度平台', 12, AC, 'middle', 'bold'))
    o.append(T(p.X(0.80) - 6, p.Y(0.72), '0.485/λ²', 11.5, AC, 'end'))
    o.append(T(p.X(1.82), p.Y(1 / 1.82 ** 2) - 10, '1/λ²', 11.5, MUT))
    o.append(T(p.X(1.62), p.Y(0.92), '灰虛線：無殘留應力', 11, MUT))
    o.append(T(p.X(1.62), p.Y(0.84), '紅細線：LRFD 0.658^{λ²}', 11, COMP))
    o.append(L(p.X(1.0), p.Y(1.0), p.X(1.0), p.Y(0.5), WARN, 2))
    o.append(T(p.X(1.0) + 5, p.Y(0.76), '−50%', 12, WARN, weight='bold'))
    # right text
    x, y = 492, 40
    o.append(T(x, y, 'SS-2024-1（113 年）', 14, INK, weight='bold'))
    o.append(T(x, y + 20, 'RH400×400×13×21 強軸、塊狀殘留應力', 11.5, MUT))
    lines = [('翼板外側 4 塊 −0.5*F*_{y}（整塊同時降伏）', INK),
             ('→ 比例限 *F*_{p} = 0.5*F*_{y}', INK),
             ('→ 扣掉 4 塊後 *I*_{e}/*I*_{x} = 0.485', INK),
             ('', INK),
             ('λ ≤ 0.696：壓潰 *F*_{cr} = *F*_{y}', AC),
             ('0.696–0.985：0.485/λ²（*I*_{e} 有效）', AC),
             ('0.985–1.414：平台 0.5（加到 *F*_{p} 即失穩）', AC),
             ('λ ≥ 1.414：1/λ²（全斷面彈性）', AC),
             ('', INK),
             ('三個轉折點連續、全程單調不遞增；', COMP),
             ('不是在 λ = √2 處「跳一下」。', COMP)]
    y += 48
    for t, c in lines:
        if t:
            o.append(T(x, y, t, 12, c))
        y += 21 if t else 8
    return svg(W, H, '\n'.join(o), 'SS-2024-1 含殘留應力之柱強度曲線')


# ---------------------------------------------------------------- 7-1
def fig7_1():
    W, H = 720, 360
    o = []
    p = Plot(70, 300, 560, 260, 3.0, 1.1)
    o.append(p.axes([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0], [0, 0.2, 0.4, 0.6, 0.8, 1.0], 'λ_{c}', '*F*_{cr}/*F*_{y}'))
    o.append(L(p.X(0), p.Y(1), p.X(3), p.Y(1), STEEL, 1.2, '6 4'))
    o.append(T(p.X(2.98), p.Y(1) - 7, '*F*_{cr} = *F*_{y}（材料上限）', 11.5, MUT, 'end'))
    o.append(p.curve(lambda l: 1 / l ** 2, 0.95, 3.0, clip=1.08, c=AC, w=2.2, dash='7 4'))
    # region shading between Euler/plateau and LRFD
    top = [(p.X(l), p.Y(min(1.0, 1 / l ** 2) if l > 0 else 1)) for l in [i / 100 for i in range(0, 301)]]
    bot = [(p.X(l), p.Y(lrfd(l))) for l in [i / 100 for i in range(300, -1, -1)]]
    o.append(P(top + bot, c=None, fill=KEY2, close=True, op=0.7))
    o.append(p.curve(lrfd, 0, 1.5, c=COMP, w=3.4))
    o.append(p.curve(lrfd, 1.5, 3.0, c=COMP, w=3.4))
    o.append(L(p.X(1.5), p.Y(0), p.X(1.5), p.Y(1.08), WARN, 1.3, '4 3'))
    o.append(C(p.X(1.5), p.Y(lrfd(1.5)), 5.5, WARN, '#fff', 1.5))
    o.append(T(p.X(1.5) + 9, p.Y(0.39) - 8, '(1.5, 0.390)', 12.5, WARN, weight='bold'))
    o.append(T(p.X(1.5) + 9, p.Y(0.39) + 9, '兩式在此連續', 11.5, WARN))
    # brackets at λ=1 and λ=2
    o.append(L(p.X(1.0), p.Y(1.0), p.X(1.0), p.Y(lrfd(1.0)), KEY, 2.2))
    o.append(T(p.X(1.0) + 6, p.Y(0.84), '1.000 → 0.658', 11.5, KEY, weight='bold'))
    o.append(T(p.X(1.0) + 6, p.Y(0.84) + 15, '殘留應力＋初始彎曲', 11, KEY))
    o.append(L(p.X(2.2), p.Y(1 / 2.2 ** 2), p.X(2.2), p.Y(lrfd(2.2)), KEY, 2.2))
    o.append(T(p.X(2.2) + 6, p.Y(0.22) - 2, '× 0.877（初始彎曲）', 11.5, KEY, weight='bold'))
    o.append(T(p.X(0.08), p.Y(0.46), '非彈性區', 14, COMP, weight='bold'))
    o.append(T(p.X(0.08), p.Y(0.46) + 20, '*F*_{cr} = 0.658^{λc²}·*F*_{y}', 12.5, COMP))
    o.append(T(p.X(0.08), p.Y(0.46) + 40, 'λ_{c} → 0 時自動回到 *F*_{y}', 11.5, MUT))
    o.append(T(p.X(2.0), p.Y(0.58), '彈性區', 14, COMP, weight='bold'))
    o.append(T(p.X(2.0), p.Y(0.58) + 20, '*F*_{cr} = (0.877/λ_{c}²)·*F*_{y}', 12.5, COMP))
    o.append(T(p.X(1.04), p.Y(1.045), '理想 Euler 1/λ_{c}²', 12, AC))
    o.append(T(p.X(0.55), p.Y(0.06), '紫色區＝真實柱比理想柱少掉的強度', 11.5, KEY))
    return svg(W, H, '\n'.join(o), 'LRFD 柱強度曲線與理想 Euler 曲線')


# ---------------------------------------------------------------- 7-2
def _contour_cell(x0, y0, w, h, c):
    """closed contour sin(pi X) sin(pi Y) = c within a unit cell mapped to (x0,y0,w,h)."""
    xs = []
    lo = math.asin(c) / math.pi
    up, dn = [], []
    n = 40
    for i in range(n + 1):
        X = lo + (1 - 2 * lo) * i / n
        sx = math.sin(math.pi * X)
        r = min(1.0, c / sx) if sx > 0 else 1.0
        Yl = math.asin(r) / math.pi
        up.append((x0 + w * X, y0 + h * Yl)); dn.append((x0 + w * X, y0 + h * (1 - Yl)))
    return up + dn[::-1]


def fig7_2():
    W, H = 720, 360
    o = []
    o.append(L(360, 16, 360, 340, GRID, 1.5))
    for side in (0, 1):
        x0 = 30 + side * 360
        col = AC if side == 0 else WARN
        o.append(T(x0, 28, '加勁肢：兩邊都有支承（*k* ≈ 4.0）' if side == 0 else '非加勁肢：一邊自由（*k* ≈ 0.425）', 14.5, col, weight='bold'))
        px, py, pl, pb = x0 + 10, 56, 270, 80
        o.append(R(px, py, pl, pb, '#fafafa', MUT, 1))
        if side == 0:
            o.append(L(px, py, px + pl, py, INK, 4, cap='butt')); o.append(L(px, py + pb, px + pl, py + pb, INK, 4, cap='butt'))
            nc = round(pl / pb)
            cw = pl / nc
            for j in range(nc):
                fill = COMPM if j % 2 == 0 else ACM
                for c in (0.2, 0.55, 0.85):
                    o.append(P(_contour_cell(px + j * cw, py, cw, pb, c), COMP if j % 2 == 0 else AC, 1.1, fill='none'))
                o.append(T(px + j * cw + cw / 2, py + pb / 2 + 5, '+' if j % 2 == 0 else '−', 14, COMP if j % 2 == 0 else AC, 'middle', 'bold'))
            o.append(dim(px, py + pb + 14, px + cw, py + pb + 14, '半波長 ≈ *b*', col, size=11.5))
            o.append(T(px + pl + 6, py + 6, '支承', 11, INK))
            o.append(T(px + pl + 6, py + pb + 4, '支承', 11, INK))
        else:
            o.append(L(px, py + pb, px + pl, py + pb, INK, 4, cap='butt'))
            o.append(L(px, py, px + pl, py, WARN, 1.2, '5 3'))
            for c in (0.15, 0.35, 0.55, 0.75, 0.92):
                pts = []
                for i in range(201):
                    X = i / 200
                    sx = math.sin(math.pi * X)
                    if sx <= 0: continue
                    Yv = c / sx
                    if Yv > 1: continue
                    pts.append((px + pl * X, py + pb * (1 - Yv)))
                o.append(P(pts, WARN, 1.1))
            o.append(T(px + pl / 2, py + 18, '+', 14, WARN, 'middle', 'bold'))
            o.append(dim(px, py + pb + 14, px + pl, py + pb + 14, '單一長半波', col, size=11.5))
            o.append(T(px + pl + 6, py + 6, '自由', 11, WARN))
            o.append(T(px + pl + 6, py + pb + 4, '支承', 11, INK))
        o.append(T(px, py - 8, '板面俯視：等值線＝面外變位', 11, MUT))
        # cross-section
        cy = 222
        o.append(T(x0, cy - 34, '斷面（放大變位）', 11.5, MUT))
        bw = 150
        sx0 = x0 + 70
        o.append(L(sx0, cy, sx0 + bw, cy, STEEL, 5, op=0.5, cap='butt'))
        if side == 0:
            pts = [(sx0 + bw * t, cy - 26 * math.sin(math.pi * t)) for t in [i / 50 for i in range(51)]]
            o.append(P(pts, COMP, 3))
            for xx in (sx0, sx0 + bw):
                o.append(P([(xx, cy + 2), (xx - 7, cy + 13), (xx + 7, cy + 13)], INK, 1.3, fill='#fff', close=True))
        else:
            # rotation about supported edge (left), free edge right
            pts = [(sx0 + bw * t, cy - 34 * t) for t in [0, 1]]
            o.append(P(pts, WARN, 3))
            o.append(P([(sx0, cy + 2), (sx0 - 7, cy + 13), (sx0 + 7, cy + 13)], INK, 1.3, fill='#fff', close=True))
            o.append(T(sx0 + bw + 6, cy - 30, '自由邊整片翻出', 11.5, WARN))
        o.append(T(x0, 270, '兩端被扶 → 只能起小波浪' if side == 0 else '一邊自由 → 像懸臂，容易翻', 13, col))
        o.append(T(x0, 294, '限值寬鬆：λ_{r} = 1.49√(*E*/*F*_{y})（腹板）' if side == 0 else '限值嚴格：λ_{r} = 0.56√(*E*/*F*_{y})（翼板）', 13, col, weight='bold'))
        o.append(T(x0, 316, 'A36 → 42.4；A572-50 → 35.9' if side == 0 else 'A36 → 15.9；A572-50 → 13.5', 12.5, MUT))
    o.append(T(30, 344, '限值比 1.49/0.56 = 2.7 ≈ √(4.0/0.425) = 3.1：寬厚比限值與 √*k* 成正比。', 11.5, MUT))
    return svg(W, H, '\n'.join(o), '加勁肢與非加勁肢的局部挫屈')


# ---------------------------------------------------------------- 7-3 (new)
def fig7_3():
    W, H = 720, 320
    o = []
    p = Plot(60, 270, 330, 220, 2.5, 1.1)
    o.append(T(20, 24, '(a) 兩條「非彈性」經驗曲線（不含安全係數）', 13.5, INK, weight='bold'))
    o.append(p.axes([0, 0.5, 1.0, 1.5, 2.0, 2.5], [0, 0.25, 0.5, 0.75, 1.0], 'λ_{c}', '*F*_{cr}/*F*_{y}'))
    o.append(p.curve(lambda l: 1 / l ** 2, 0.95, 2.5, clip=1.08, c=STEEL, w=1.6, dash='6 4'))
    o.append(p.curve(crc, 0, 2.5, c=WARN, w=2.6))
    o.append(p.curve(lrfd, 0, 2.5, c=COMP, w=2.6))
    for lx, c, lab in ((math.sqrt(2), WARN, 'ASD 分界 √2（*C*_{c}）'), (1.5, COMP, 'LRFD 分界 1.5')):
        o.append(L(p.X(lx), p.Y(0), p.X(lx), p.Y(1.05), c, 1, '3 3'))
    o.append(T(p.X(1.41) - 4, p.Y(1.02), '√2', 11.5, WARN, 'end', 'bold'))
    o.append(T(p.X(1.5) + 4, p.Y(1.02), '1.5', 11.5, COMP, 'start', 'bold'))
    o.append(T(p.X(0.08), p.Y(0.30), '橘：CRC 拋物線 1 − λ²/4', 11.5, WARN))
    o.append(T(p.X(0.08), p.Y(0.30) + 16, '紅：SSRC 0.658^{λ²}', 11.5, COMP))
    o.append(T(p.X(0.08), p.Y(0.30) + 32, '灰虛：Euler 1/λ²', 11.5, MUT))
    # (b) ratio
    q = Plot(460, 270, 230, 220, 2.5, 1.50, ymin=1.30)
    o.append(T(420, 24, '(b) LRFD φ_{c}*P*_{n} ÷ ASD *P*_{a}', 13.5, INK, weight='bold'))
    o.append(q.axes([0, 0.5, 1.0, 1.5, 2.0, 2.5], [1.30, 1.35, 1.40, 1.45, 1.50], 'λ_{c}', '', fmt=lambda v: f'{v:.2f}' if v > 1 else f'{v:g}'))
    o.append(q.curve(lambda l: 0.85 * lrfd(l) / asd_fa(l), 0, 2.5, n=500, c=KEY, w=2.6))
    mx = max(((l / 1000, 0.85 * lrfd(l / 1000) / asd_fa(l / 1000)) for l in range(0, 2501)), key=lambda t: t[1])
    mn = min(((l / 1000, 0.85 * lrfd(l / 1000) / asd_fa(l / 1000)) for l in range(0, 2501)), key=lambda t: t[1])
    for (lx, rv), dy in ((mx, -10), (mn, 18)):
        o.append(C(q.X(lx), q.Y(rv), 4, KEY, '#fff', 1.2))
        o.append(T(q.X(lx), q.Y(rv) + dy, f'{rv:.2f}', 12, KEY, 'middle', 'bold'))
    for lx, nm in ((0.512, '§7.7'), (1.205, 'SS-2013-3')):
        rv = 0.85 * lrfd(lx) / asd_fa(lx)
        o.append(C(q.X(lx), q.Y(rv), 4.5, '#fff', COMP, 2))
    o.append(T(q.X(0.05), q.Y(1.335), '○ §7.7 範例 1.46　○ SS-2013-3 1.39', 11, COMP))
    o.append(T(q.X(0.05), q.Y(1.315), 'λ_{c} > 1.5：0.85 × 0.877 × 23/12 = 1.43', 11, MUT))
    return svg(W, H, '\n'.join(o), 'LRFD 與 ASD 柱強度曲線對照')
