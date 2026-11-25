# -*- coding: utf-8 -*-
"""SD 教科書共用的向量圖元件（種子樹、五步驟、流程圖、SDOF 台車、剪力屋）。
每本教科書的工作資料夾各放一份（與 lib.py、plot.py 相同做法）。所有幾何由參數計算。"""
from plot import *  # noqa
import math

PUR = '#7b1fa2'


def seed_tree(seeds, kids, title_l=None, title_r='長出來的公式（不用背，會推）', sgap=None, kgap=40.5, sw=330, kw=410, sfs=14.5, kfs=13.5):
    """seeds: [(id, text, color)]；kids: [(seed index, 章, text)]"""
    W = 900
    sx, sh = 20, 46
    kx, kh = 900 - 20 - kw, 34
    n = len(kids)
    sgap = sgap or max(56, (n * kgap) / max(1, len(seeds)))
    sy0, ky0 = 66, 62
    H = 60 + max(len(seeds) * sgap, n * kgap) + 30
    o = T(sx + sw / 2, 36, title_l or f'{len(seeds)} 顆種子（要記的）', 17, PUR, 'middle', 'bold')
    o += T(kx + kw / 2, 36, title_r, 17, INK, 'middle', 'bold')
    spos = {}
    for i, (sid, txt, c) in enumerate(seeds):
        y = sy0 + i * sgap
        spos[i] = (sx + sw, y + sh / 2, c)
        o += R(sx, y, sw, sh, '#fff', c, 2.2, 10)
        o += R(sx, y, 48, sh, c, None, 0, 10) + R(sx + 30, y, 18, sh, c, None)
        o += T(sx + 24, y + 29, sid, 15, '#fff', 'middle', 'bold')
        o += T(sx + 58, y + 29, txt, sfs, INK, 'start', 'bold')
    for j, (si, ch, txt) in enumerate(kids):
        y = ky0 + j * kgap
        x1, y1, c = spos[si]
        x2, y2 = kx, y + kh / 2
        mx = (x1 + x2) / 2
        o += f'<path d="M{f(x1)},{f(y1)} C{f(mx)},{f(y1)} {f(mx)},{f(y2)} {f(x2 - 6)},{f(y2)}" fill="none" stroke="{c}" stroke-width="1.8" opacity=".75"/>'
        o += head(x2, y2, 0, c, 8)
        o += R(kx, y, kw, kh, '#fafafa', STEEL, 1.1, 7)
        o += R(kx, y, 62, kh, STEEL2, None, 0, 7)
        o += T(kx + 31, y + 22, f'第{ch}章', 14, MUT, 'middle', 'bold')
        o += T(kx + 70, y + 22.5, txt, kfs, INK, 'start')
    return svg(W, int(H), o, '種子公式家族樹')


def five_steps():
    W, H = 900, 190
    steps = [('①', '看圖', '自由體圖／相量圖', AC),
             ('②', '第一性原理', '牛頓、能量、相容', TEN),
             ('③', '三步推導', '每一步都有圖', COMP),
             ('④', '極限檢查', '代 0、代 ∞、代 1', WARN),
             ('⑤', '30 秒重建卡', '空白紙重畫一次', PUR)]
    bw, gap = 152, 30
    o = ''
    for i, (n, t, s, c) in enumerate(steps):
        x = 14 + i * (bw + gap)
        o += R(x, 40, bw, 110, '#fff', c, 2.2, 12)
        o += R(x, 40, bw, 40, c, None, 0, 12) + R(x, 66, bw, 14, c, None)
        o += T(x + bw / 2, 67, f'{n} {t}', 16, '#fff', 'middle', 'bold')
        o += T(x + bw / 2, 112, s, 14, INK, 'middle')
        if i < 4:
            o += A(x + bw + 3, 95, x + bw + gap - 3, 95, INK, 2.2, 10)
    o += T(W / 2, 180, '全書每一條公式都照這五步走——讀久了，腦袋會自己照這個順序想', 14, MUT, 'middle')
    return svg(W, H, o, '每條公式的五個步驟')


def flow(rows, W=900, bh=54, gap=26, title=None):
    """垂直流程圖。rows: [(標題, 說明, color)]；每列一個方框，方框間箭頭。"""
    y0 = 50 if title else 18
    H = y0 + len(rows) * (bh + gap) + 6
    o = T(W / 2, 30, title, 17, INK, 'middle', 'bold') if title else ''
    for i, (t, s, c) in enumerate(rows):
        y = y0 + i * (bh + gap)
        o += R(60, y, W - 120, bh, '#fff', c, 2, 10)
        o += R(60, y, 190, bh, c, None, 0, 10) + R(230, y, 20, bh, c, None)
        o += T(155, y + bh / 2 + 6, t, 15.5, '#fff', 'middle', 'bold')
        o += T(266, y + bh / 2 + 6, s, 14.5, INK, 'start')
        if i < len(rows) - 1:
            o += A(W / 2, y + bh + 2, W / 2, y + bh + gap - 2, INK, 2, 10)
    return svg(W, int(H), o, '流程圖')


def spring(x1, y1, x2, y2, n=7, amp=9, c=INK, w=1.8):
    """鋸齒彈簧（兩端各留直線段）。"""
    L_ = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L_, (y2 - y1) / L_
    nx, ny = -uy, ux
    lead = 0.18 * L_
    pts = [(x1, y1), (x1 + ux * lead, y1 + uy * lead)]
    seg = (L_ - 2 * lead) / (2 * n)
    for i in range(1, 2 * n):
        s = lead + i * seg
        sgn = 1 if i % 2 else -1
        pts.append((x1 + ux * s + nx * amp * sgn, y1 + uy * s + ny * amp * sgn))
    pts += [(x2 - ux * lead, y2 - uy * lead), (x2, y2)]
    return P(pts, c, w)


def dashpot(x1, y, x2, c=INK, w=1.8):
    """水平阻尼器（x1 < x2）。"""
    m = (x1 + x2) / 2
    o = L(x1, y, m - 6, y, c, w)
    o += P([(m - 18, y - 11), (m + 8, y - 11)], c, w) + P([(m - 18, y + 11), (m + 8, y + 11)], c, w)
    o += L(m - 18, y - 11, m - 18, y + 11, c, w)
    o += L(m - 4, y - 8, m - 4, y + 8, c, w + 1)
    o += L(m - 4, y, x2, y, c, w)
    return o


def cart(x, yg, w=120, h=70, label='*m*', c=AC, fill=AC2, ks=True, cs=True, wall_x=None):
    """SDOF 台車：牆在 wall_x，彈簧（上）阻尼器（下）連到台車左面；地面 yg。回傳 svg 片段。"""
    wall_x = x - 150 if wall_x is None else wall_x
    o = hatch_ground(wall_x - 20, yg, x + w + 120 - wall_x, INK)
    o += L(wall_x, yg, wall_x, yg - h - 30, INK, 3)
    for i in range(6):
        yy = yg - h - 30 + i * (h + 30) / 6
        o += L(wall_x, yy, wall_x - 8, yy + 8, INK, 1)
    o += R(x, yg - h - 12, w, h, fill, c, 2, 6)
    o += C(x + 25, yg - 6, 6, '#fff', INK, 1.5) + C(x + w - 25, yg - 6, 6, '#fff', INK, 1.5)
    o += T(x + w / 2, yg - 12 - h / 2 + 6, label, 20, c, 'middle', 'bold')
    if ks:
        o += spring(wall_x, yg - 12 - h * 0.72, x, yg - 12 - h * 0.72)
        o += T((wall_x + x) / 2, yg - 12 - h * 0.72 - 16, '*k*', 17, INK, 'middle')
    if cs:
        o += dashpot(wall_x, yg - 12 - h * 0.28, x)
        o += T((wall_x + x) / 2, yg - 12 - h * 0.28 + 30, '*c*', 17, INK, 'middle')
    return o


def shear_building(x0, yb, n, bw=170, sh=70, labels=None, col=STEEL, mc=AC, mfill=AC2, disp=None, dc=COMP, klabels=None):
    """n 層剪力屋；disp 給各樓層位移（像素）則畫變形形狀。回傳 (svg, 樓層中心點列表)。"""
    o = hatch_ground(x0 - 30, yb, bw + 60, INK)
    pts = []
    xs_prev = 0
    for i in range(n):
        y_bot = yb - i * sh
        y_top = yb - (i + 1) * sh
        dx_b = disp[i - 1] if (disp and i > 0) else 0
        dx_t = disp[i] if disp else 0
        for cx in (x0, x0 + bw):
            o += L(cx + dx_b, y_bot, cx + dx_t, y_top, col, 5)
        o += R(x0 - 10 + dx_t, y_top - 10, bw + 20, 14, mfill, mc, 1.8, 3)
        if labels:
            o += T(x0 + bw + 22 + dx_t, y_top + 2, labels[i], 15, mc, 'start', 'bold')
        if klabels:
            o += T(x0 - 18 + (dx_b + dx_t) / 2, (y_bot + y_top) / 2 + 5, klabels[i], 15, INK, 'end')
        pts.append((x0 + bw / 2 + dx_t, y_top - 3))
    return o, pts
