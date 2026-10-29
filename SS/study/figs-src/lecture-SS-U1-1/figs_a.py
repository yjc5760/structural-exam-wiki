import math
from lib import *


# ---------------------------------------------------------------- 0-1
def fig0_1():
    W, H = 720, 300
    o = []
    o.append(L(360, 20, 360, 282, GRID, 1.5))
    for side in (0, 1):
        x0 = 30 + side * 360
        col = TEN if side == 0 else COMP
        o.append(T(x0, 32, '拉力：擾動會被「拉回來」→ 自我穩定' if side == 0 else '壓力：擾動會被「推得更歪」→ 可能失穩', 15, col, weight='bold'))
        y0, a = 112, 30
        xa, xb = x0 + 40, x0 + 260
        # original (straight) position
        o.append(L(xa, y0, xb, y0, STEEL, 1.4, '5 4'))
        pts = [(xa + (xb - xa) * t, y0 + a * math.sin(math.pi * t)) for t in [i / 80 for i in range(81)]]
        o.append(P(pts, col, 6))
        o.append(C(xa, y0, 4, '#fff', INK, 1.5)); o.append(C(xb, y0, 4, '#fff', INK, 1.5))
        # end forces along the axis
        if side == 0:
            o.append(A(xa - 4, y0, xa - 34, y0, INK, 2.4, 11)); o.append(A(xb + 4, y0, xb + 34, y0, INK, 2.4, 11))
            o.append(T(xa - 34, y0 - 10, '*T*', 15, INK)); o.append(T(xb + 26, y0 - 10, '*T*', 15, INK))
        else:
            o.append(A(xa - 36, y0, xa - 6, y0, INK, 2.4, 11)); o.append(A(xb + 36, y0, xb + 6, y0, INK, 2.4, 11))
            o.append(T(xa - 36, y0 - 10, '*P*', 15, INK)); o.append(T(xb + 28, y0 - 10, '*P*', 15, INK))
        xm = (xa + xb) / 2
        o.append(dim(xm - 34, y0, xm - 34, y0 + a, 'δ', MUT, size=13, side=-1, lab_off=6))
        if side == 0:
            o.append(A(xm, y0 + a + 32, xm, y0 + a + 4, TEN, 2.6, 11))
            o.append(T(xm + 10, y0 + a + 26, '彎矩 *T*·δ 使它回直', 13, TEN, weight='bold'))
        else:
            o.append(A(xm, y0 + a + 4, xm, y0 + a + 32, COMP, 2.6, 11))
            o.append(T(xm + 10, y0 + a + 26, '彎矩 *P*·δ 使它更彎', 13, COMP, weight='bold'))
        o.append(T(xa, y0 - 26, '虛線＝原本筆直位置；實線＝受擾動後（放大）', 11.5, MUT))
        lines = (['→ 恢復力矩隨變形增加，平衡是<b>穩定</b>的', '→ 沒有「挫屈」這回事', ]
                 if side == 0 else
                 ['→ 抵抗彎矩 *EI*·*y*″ 一旦追不上 *P*·*y* 就失穩', '→ 應力遠低於 *F*_{y} 時就可能發生'])
        yy = 214
        for s in lines:
            s2 = s.replace('<b>', '').replace('</b>', '')
            o.append(T(x0, yy, s2, 13.5, INK)); yy += 24
        o.append(T(x0, yy + 6, '破壞＝材料被拉斷／拉降伏' if side == 0 else '破壞＝幾何失穩（挫屈）', 14, col, weight='bold'))
        o.append(T(x0 + (190 if side == 0 else 160), yy + 6,
                   '控制：*F*_{y}、*F*_{u}、*A*' if side == 0 else '控制：*E*、*I*、*KL*', 13.5, col))
    return svg(W, H, '\n'.join(o), '拉力與壓力在擾動下的行為比較')


# ---------------------------------------------------------------- 1-1
def fig1_1():
    W, H = 720, 268
    o = []
    sc = 440 / 600.0          # px per cm   (member 600 cm)
    mag = 5                   # elongation magnification
    xL, xR = 90, 90 + 440
    for k, (ttl, col, y) in enumerate((('GSY 全斷面降伏：降伏區＝整根桿身（≈ 600 cm）', TEN, 56),
                                       ('NSF 淨斷面斷裂：降伏區＝螺栓孔那一排（數 cm）', COMP, 168))):
        o.append(T(30, y - 18, ttl, 14.5, col, weight='bold'))
        h = 30
        # gusset plate at right
        o.append(R(xR - 46, y - 10, 70, h + 20, STEEL3, STEEL, 1))
        if k == 0:
            o.append(R(xL, y, xR - xL, h, TENM, TEN, 1.6))
            o.append(T((xL + xR - 46) / 2, y + 20, '整段都在降伏（應變 ≈ 2%）', 12.5, '#1b5e20', 'middle', 'bold'))
            ext = 12 * sc * mag
        else:
            o.append(R(xL, y, xR - xL, h, STEEL2, '#546e7a', 1.6))
            o.append(R(xR - 40, y, 8, h, COMP, COMP, 0.5))
            o.append(T(xR - 40, y - 6, '孔緣局部降伏→斷裂', 12, COMP, 'end'))
            ext = 0.5 * sc * mag
        for i in range(2):
            o.append(C(xR - 36 + i * 22, y + h / 2, 4.5, '#fff', INK, 1.2))
        # ghost elongated end (left end moves left)
        o.append(R(xL - ext, y, ext, h, 'none', col, 1.4, dash='4 3'))
        o.append(A(xL - ext - 2, y + h / 2, xL - ext - 38, y + h / 2, INK, 2.2, 10))
        o.append(T(xL - ext - 40, y + h / 2 - 8, '*T*', 15))
        if k == 0:
            o.append(dim(xL - ext, y + h, xL, y + h, '', col, off=14))
            o.append(T(xL - ext / 2, y + h + 32, '伸長 ≈ 600 × 2% = 12 cm', 12.5, col, 'start'))
        else:
            o.append(T(xL - 6, y + h + 20, '伸長 ≈ 5 cm × 10% ≈ 0.5 cm（同比例下幾乎看不見）', 12.5, col, 'start'))
        # right-hand verdict
        x = 560
        o.append(T(x + 8, y + 6, '延性破壞，看得見' if k == 0 else '脆性破壞，無預警', 14, col, weight='bold'))
        o.append(T(x + 8, y + 28, 'φ_{t} = 0.90' if k == 0 else 'φ_{t} = 0.75', 15, col, weight='bold'))
        o.append(T(x + 8, y + 48, '*F*_{y} × *A*_{g}' if k == 0 else '*F*_{u} × *A*_{e}', 13.5, INK))
    o.append(T(30, 254, '＊ 虛線框為伸長量，兩列同比例放大 5 倍。數字為量級示意：降伏平台末端應變約 1.5–2%，孔周圍局部頸縮可達 10–20%。', 11.5, MUT))
    return svg(W, H, '\n'.join(o), '全斷面降伏與淨斷面斷裂的變形量比較')


# ---------------------------------------------------------------- 1-2 (new)
def fig1_2():
    W, H = 720, 290
    o = []
    s = 10  # px per cm
    x0, y0, bg = 90, 46, 18
    o.append(R(x0, y0, 330, bg * s, STEEL2, '#546e7a', 1.5))
    gl = [y0 + 3 * s, y0 + 9 * s, y0 + 15 * s]           # gauge lines, g = 6 cm
    hx = x0 + 120; sp = 7 * s                              # stagger s = 7 cm
    holes = [(hx, gl[0]), (hx + sp, gl[1]), (hx, gl[2]), (hx + 2 * sp, gl[0]), (hx + 2 * sp, gl[2]), (hx - sp, gl[1])]
    for yy in gl:
        o.append(L(x0 + 4, yy, x0 + 326, yy, STEEL, 0.8, '6 4'))
    # path 1 (straight)
    o.append(L(hx, y0, hx, y0 + bg * s, AC, 3))
    # path 2 (zig-zag)
    o.append(P([(hx, y0), holes[0], holes[1], holes[2], (hx, y0 + bg * s)], COMP, 3, dash='8 4'))
    for (x, y) in holes:
        o.append(C(x, y, 2.3 * s / 2, '#fff', INK, 1.5))
    # dims
    o.append(dim(hx, y0, hx + sp, y0, '*s* = 7', INK, off=-16, side=-1, size=12.5))
    o.append(dim(x0 + 300, gl[0], x0 + 300, gl[1], '*g* = 6', INK, off=0, size=12.5, side=-1, lab_off=8))
    o.append(dim(x0, y0, x0, y0 + bg * s, '*b*_{g} = 18', INK, off=18, side=1, size=12.5))
    o.append(A(x0 + 334, y0 + bg * s / 2 + 60, x0 + 380, y0 + bg * s / 2 + 60, INK, 2.4, 11))
    o.append(T(x0 + 360, y0 + bg * s / 2 + 52, '*T*', 15, INK, 'middle'))
    o.append(T(hx - 8, y0 + bg * s + 22, '①', 15, AC, 'end', 'bold'))
    o.append(T(hx + 8, y0 + bg * s + 22, '②', 15, COMP, 'start', 'bold'))
    o.append(T(x0, y0 + bg * s + 44, '尺寸單位 cm，孔扣除寬 *d* = 2.3 cm，圖依比例繪製', 11.5, MUT))
    # right text
    x = 480; y = 60
    o.append(T(x, y, '① 直線路徑（穿 2 孔）', 14, AC, weight='bold'))
    o.append(T(x, y + 24, '*A*_{n} = (*b*_{g} − 2*d*)·*t* = 13.4*t*', 13.5))
    o.append(T(x, y + 64, '② 鋸齒路徑（穿 3 孔、2 段斜線）', 14, COMP, weight='bold'))
    o.append(T(x, y + 88, '*A*_{n} = (*b*_{g} − 3*d* + 2·*s*^{2}/4*g*)·*t*', 13.5))
    o.append(T(x, y + 110, '= (18 − 6.9 + 4.08)·*t* = 15.2*t*', 13.5))
    o.append(T(x, y + 148, '→ 多扣一孔（2.3），但兩段斜線', 13, INK))
    o.append(T(x, y + 168, '　補回 2 × 49/24 = 4.08 → ② 不控制', 13, INK))
    o.append(T(x, y + 194, '取所有可能路徑中 *A*_{n} 最小者', 13.5, KEY, weight='bold'))
    return svg(W, H, '\n'.join(o), '交錯螺栓的淨斷面破壞路徑')


# ---------------------------------------------------------------- 2-1
def fig2_1():
    W, H = 740, 372
    o = []
    s = 9.0  # px/cm
    xbar, Lc, sp = 2.82, 14.0, 7.0
    y0 = 92            # connection plane (face of connected leg against gusset), plan view
    wl = 10 * s        # outstanding leg width
    xa, xb = 40, 600   # member extent
    x1 = 110           # first bolt (nearest member end)
    bolts = [x1 + i * sp * s for i in range(3)]
    # gusset (edge-on band)
    o.append(R(20, y0 - 12, bolts[-1] + 40 - 20, 12, STEEL3, STEEL, 1))
    o.append(T(24, y0 - 18, '節點板（邊視）', 12, MUT))
    # outstanding leg seen from above
    o.append(R(xa, y0, xb - xa, wl, '#f1f8e9', TEN, 1.6))
    o.append(L(xa, y0 + 1 * s, xb, y0 + 1 * s, TEN, 0.8, '3 3'))  # hidden: connected leg thickness
    # bolts (hidden, through gusset + connected leg)
    for bx in bolts:
        o.append(L(bx, y0 - 16, bx, y0 + 1 * s + 4, INK, 4, cap='butt'))
        o.append(R(bx - 7, y0 - 20, 14, 5, INK, None))
    # flow lines in outstanding leg
    n = 5
    for k in range(n):
        yf = (k + 0.5) / n * 10.0
        pts = []
        for i in range(161):
            x = bolts[0] + (xb - 10 - bolts[0]) * i / 160
            # spreading: from near connection (0.6 cm) to final position over ~ 2.2 L downstream of last bolt
            t = max(0.0, (x - bolts[0] - (k / n) * (bolts[-1] - bolts[0])) / (2.2 * Lc * s))
            g = 1 - math.exp(-3.2 * t)
            yv = 0.6 + (yf - 0.6) * g
            pts.append((x, y0 + yv * s))
        o.append(P(pts, WARN, 1.6, op=0.9))
        o.append(head(pts[-1][0] + 8, pts[-1][1], 0, WARN, 8))
    # centroid line
    yc = y0 + xbar * s
    o.append(L(xa, yc, xb, yc, KEY, 1.3, '10 3 2 3'))
    o.append(T(xb + 6, yc + 4, '形心線', 12, KEY))
    o.append(dim(xa + 30, y0, xa + 30, yc, '', KEY, off=0))
    o.append(T(xa + 40, y0 + 18, '*x̄* = 2.82 cm', 12.5, KEY, 'start', 'bold'))
    o.append(dim(bolts[0], y0 + wl, bolts[-1], y0 + wl, '*L* = 2*s* = 14 cm', TEN, off=16, side=1, size=13, weight='bold'))
    o.append(A(xb + 6, y0 + wl / 2 + 22, xb + 46, y0 + wl / 2 + 22, INK, 2.4, 11))
    o.append(T(xb + 30, y0 + wl / 2 + 44, '*T*', 15, INK, 'middle'))
    o.append(T(xa + 4, y0 + wl - 8, '外伸肢（俯視）', 12, TEN))
    o.append(T(250, y0 - 22, '橘線＝力線：從連接面附近進入，要走一段距離才攤滿整肢', 12, WARN))
    # stress profiles
    def prof(xp, nonuni, lbl):
        oo = [L(xp, y0, xp, y0 + wl, INK, 1)]
        pts = []
        for i in range(21):
            yy = i / 20 * 10.0
            v = (2.2 * math.exp(-yy / 3.0) + 0.15) if nonuni else 1.0
            pts.append((xp + 18 * v, y0 + yy * s))
        oo.append(P([(xp, y0)] + pts + [(xp, y0 + wl)], c=AC, w=1.4, fill=AC2, close=True))
        oo.append(T(xp + 4, y0 + wl + 50, lbl, 11.5, AC))
        return ''.join(oo)
    # section view inset (L100x100x10)
    ox, oy, k = 650, 214, 0.8  # px per mm
    o.append(T(548, 232, '斷面（依比例）', 12.5, INK, weight='bold'))
    o.append(R(ox - 12, oy - 6, 10, 108, STEEL3, STEEL, 1))                        # gusset
    o.append(P([(ox, oy), (ox + 100 * k, oy), (ox + 100 * k, oy + 10 * k), (ox + 10 * k, oy + 10 * k),
                (ox + 10 * k, oy + 100 * k), (ox, oy + 100 * k)], TEN, 1.4, fill=TENM, close=True))
    cx, cy = ox + 28.2 * k, oy + 28.2 * k
    o.append(C(cx, cy, 3.2, KEY, None))
    o.append(L(ox, cy, cx, cy, KEY, 1, '3 2'))
    o.append(dim(ox, oy + 100 * k, cx, oy + 100 * k, '', KEY, off=12))
    o.append(T(ox + 2, oy + 100 * k + 30, '*x̄*', 13, KEY, weight='bold'))
    o.append(L(ox - 18, oy + 55 * k, ox + 16, oy + 55 * k, INK, 4, cap='butt'))
    o.append(T(ox + 18, oy + 55 * k + 4, '螺栓', 11, MUT))
    o.append(T(548, 250, 'L100×100×10', 11.5, MUT))
    # bottom formula line
    yb = 338
    o.append(T(30, yb, '力線的平均「爬坡陡度」≈ *x̄*/*L* = 2.82/14 = 0.20　→　有效淨斷面折減 *U* = 1 − *x̄*/*L* = 0.80', 14, INK, weight='bold'))
    o.append(T(30, yb + 24, '＊ *x̄*：從<連接面>量到構材形心的距離（不是到肢中心）；*L*：第一顆到最後一顆螺栓的距離。比例依 §3.1 範例繪製。'.replace('<', '「').replace('>', '」'), 12, MUT))
    return svg(W, H, '\n'.join(o), '剪力遲滯的幾何：力從連接肢擴散到外伸肢')


# ---------------------------------------------------------------- 2-2 (new)
def fig2_2():
    W, H = 720, 320
    o = []
    X0, Y0, PW, PH = 70, 270, 400, 230
    Lmax, Pmax = 4.0, 10.0
    X = lambda L_: X0 + L_ / Lmax * PW
    Y = lambda P_: Y0 - P_ / Pmax * PH
    # forbidden zone
    o.append(R(X(3), Y(Pmax), X(4) - X(3), PH, '#fafafa', None))
    for i in range(14):
        xx = X(3) + i * 8
        o.append(L(xx, Y0, min(xx + PH, X(4)), Y0 - (min(xx + PH, X(4)) - xx), '#cfd8dc', 0.8))
    o.append(T(X(3.5), Y(9.6), '*l* < *w*', 13, MUT, 'middle', 'bold'))
    o.append(T(X(3.5), Y(9.0), '規範不允許', 12, MUT, 'middle'))
    # grid & axes
    for p in range(0, 11, 2):
        o.append(L(X0, Y(p), X0 + PW, Y(p), GRID, 1)); o.append(T(X0 - 8, Y(p) + 4, str(p), 11.5, MUT, 'end'))
    for l in range(0, 5):
        o.append(T(X(l), Y0 + 18, str(l), 11.5, MUT, 'middle'))
    o.append(L(X0, Y0, X0 + PW, Y0, INK, 1.4)); o.append(L(X0, Y0, X0, Y(Pmax), INK, 1.4))
    o.append(T(X0 + PW, Y0 + 36, '板寬 *L*（cm）', 12.5, INK, 'end'))
    o.append(T(X0 - 44, Y(Pmax) - 10, '容許拉力 *P*（tf）', 12.5, INK))
    # U step regions
    for a, b, u in ((0, 1.5, '1.00'), (1.5, 2.0, '0.87'), (2.0, 3.0, '0.75')):
        o.append(T(X((a + b) / 2), Y0 - 8, f'*U*={u}', 10.5, AC, 'middle'))
        o.append(L(X(b), Y0, X(b), Y(Pmax), '#bbdefb', 1, '3 3'))
    # wrong approach
    wrong = [(X(l), Y(4.1 * l * (1 - l / 6))) for l in [i / 100 * 3 for i in range(101)]]
    o.append(P(wrong, '#9e9e9e', 2, dash='6 4'))
    o.append(T(X(1.0), Y(2.9) + 18, '誤用 *U* = 1 − *x̄*/*l*', 11.5, '#757575'))
    # NSF
    def U(l):
        return 1.0 if l <= 1.5 else (0.87 if l <= 2.0 else 0.75)
    for a, b in ((0, 1.5), (1.5, 2.0), (2.0, 3.0)):
        o.append(P([(X(a), Y(4.1 * U((a + b) / 2) * a)), (X(b), Y(4.1 * U((a + b) / 2) * b))], AC, 2.4))
    o.append(T(X(1.2) - 4, Y(6.0), '*P*_{NSF} = 0.5*F*_{u}·*U*·2*L*', 12, AC, 'end'))
    # GY
    o.append(P([(X(0), Y(0)), (X(3), Y(9.0))], TEN, 3.2))
    o.append(T(X(1.9), Y(4.2) + 26, '*P*_{GY} = 0.6*F*_{y}·2*L* = 3.0*L*', 12, TEN))
    # optimum
    o.append(C(X(3), Y(9.0), 5.5, COMP, '#fff', 1.5))
    o.append(T(X(3) - 10, Y(9.0) - 12, '(3, 9.00)', 12.5, COMP, 'end', 'bold'))
    o.append(C(X(3), Y(6.15), 4, '#9e9e9e', '#fff', 1))
    o.append(T(X(3) + 8, Y(6.15) + 18, '6.15', 11.5, '#757575'))
    # right text
    x = 500; y = 48
    o.append(T(x, y, 'SS-2025-2（114 年，ASD）', 14, INK, weight='bold'))
    o.append(T(x, y + 22, '板寬 *L*、厚 2 cm，三面圍焊', 12, MUT))
    o.append(T(x, y + 38, '縱向銲長 *l* = 3 cm（兩側各一道）', 12, MUT))
    o.append(T(x, y + 64, '① 板類縱向銲：*U* 查 *l*/*w* 階梯值', 13, AC))
    o.append(T(x, y + 86, '② 且規範要求 *l* ≥ *w* → *L* ≤ 3 cm', 13, AC))
    o.append(T(x, y + 108, '③ 每段 *P*_{NSF} > *P*_{GY}，全程 GSY 控制', 13, TEN))
    o.append(T(x, y + 140, '→ *L* 有<b>最大值</b> 3 cm', 14, COMP, weight='bold').replace('&lt;b&gt;', '').replace('&lt;/b&gt;', ''))
    o.append(T(x, y + 162, '→ *P*_{max} = 9.00 tf', 14, COMP, weight='bold'))
    o.append(T(x, y + 186, '灰虛線：把 *x̄* 取成 *L*/2 的錯解。', 12, '#757575'))
    o.append(T(x, y + 204, '頂點也落在 3 cm 只是巧合，', 12, '#757575'))
    o.append(T(x, y + 222, '*P* 卻低估 32%、控制模式也錯', 12, '#757575'))
    return svg(W, H, '\n'.join(o), 'SS-2025-2 容許拉力隨板寬變化')


# ---------------------------------------------------------------- 3-1
def fig3_1():
    W, H = 720, 360
    o = []
    s = 12.0  # px/cm
    # ---- (a) angle leg, flattened view (example §3.1)
    o.append(T(20, 24, '(a) 角鋼單肢、單排螺栓（§3.1 範例，依比例）', 14, INK, weight='bold'))
    xr = 400                  # member end (inside the gusset)
    yh = 70                   # heel
    leg = 10 * s
    yt = yh + leg             # toe
    yb = yh + 5.5 * s         # bolt line (4.5 cm from toe)
    e, sp, dh = 3.5, 7.0, 2.3
    bolts = [xr - e * s - i * sp * s for i in range(3)]
    o.append(R(bolts[-1] - 34, yh - 22, xr + 36 - (bolts[-1] - 34), leg + 44, STEEL3, STEEL, 1))         # gusset behind
    o.append(T(xr + 32, yh - 28, '節點板', 11.5, MUT, 'end'))
    o.append(R(40, yh, xr - 40, leg, STEEL2, '#546e7a', 1.5))               # connected leg face
    o.append(L(40, yh, xr, yh, INK, 4, cap='butt'))
    o.append(T(44, yh - 8, '肢背（外伸肢垂直紙面）', 11.5, MUT))
    o.append(T(44, yt + 16, '肢趾', 11.5, MUT))
    xin = bolts[-1]
    o.append(R(xin, yb, xr - xin, yt - yb, '#ffe0b2', None))
    o.append(L(xin, yb, xr, yb, COMP, 4, cap='butt'))
    o.append(L(xin, yb, xin, yt, AC, 4, cap='butt'))
    for bx in bolts:
        o.append(C(bx, yb, dh * s / 2, '#fff', INK, 1.5))
    o.append(A(36, yh + leg / 2, 4, yh + leg / 2, INK, 2.4, 11)); o.append(T(8, yh + leg / 2 - 10, '*T*', 15))
    o.append(dim(xr, yb, xr, yt, '4.5', INK, off=-14, size=12, side=-1))
    o.append(dim(xin, yt, xr, yt, '剪力面長 *e* + 2*s* = 3.5 + 14 = 17.5 cm', COMP, off=36, side=1, size=12.5, lab_off=6))
    o.append(T(xin + 8, yb - 8, '剪力面：穿過 2.5 個孔', 12, COMP, weight='bold'))
    o.append(T(xin - 8, yt - 10, '拉力面', 12, AC, 'end', 'bold'))
    o.append(T(xin - 8, yt + 6, '半個孔', 11.5, AC, 'end'))
    o.append(T((xin + xr) / 2, yt - 12, '被撕下的塊體', 12.5, '#e65100', 'middle', 'bold'))
    # numbers
    y = 268
    o.append(T(20, y, '*A*_{gv} = 17.5 × 1.0 = 17.5　*A*_{nv} = (17.5 − 2.5 × 2.3) × 1.0 = 11.75', 12.5, COMP))
    o.append(T(20, y + 22, '*A*_{nt} = (4.5 − 0.5 × 2.3) × 1.0 = 3.35 cm²（*U*_{bs} = 1.0）', 12.5, AC))
    o.append(T(20, y + 48, 'φ*R*_{n} = 0.75 × min(42.6, 40.2) = 30.2 tf ← 控制（GSY 43.1、NSF 41.0）', 13, INK, weight='bold'))
    o.append(T(20, y + 72, '尺寸單位 cm；螺栓 M20，孔扣除寬 2.3 cm', 11.5, MUT))
    # ---- (b) gusset with two bolt lines
    xo = 470
    o.append(L(xo - 14, 14, xo - 14, 326, GRID, 1.5))
    o.append(T(xo, 24, '(b) 節點板、兩排螺栓', 14, INK, weight='bold'))
    gx, gy, gw, gh = xo + 20, 64, 150, 170
    o.append(R(gx, gy, gw, gh, STEEL2, '#546e7a', 1.5))            # gusset plate (fixed at left)
    for i in range(6):
        o.append(L(gx - 2, gy + i * gh / 5, gx - 10, gy + i * gh / 5 + 8, INK, 1))
    o.append(L(gx, gy, gx, gy + gh, INK, 2.5))
    lines = [gy + gh / 2 - 30, gy + gh / 2 + 30]
    bx = [gx + gw - 26 - i * 40 for i in range(3)]
    xin = bx[-1]
    o.append(R(xin, lines[0], gx + gw - xin, lines[1] - lines[0], '#ffe0b2', None))
    for yl in lines:
        o.append(L(xin, yl, gx + gw, yl, COMP, 4, cap='butt'))
    o.append(L(xin, lines[0], xin, lines[1], AC, 4, cap='butt'))
    for yl in lines:
        for x in bx:
            o.append(C(x, yl, 9, '#fff', INK, 1.4))
    o.append(R(xin - 18, lines[0] - 16, gx + gw + 40 - (xin - 18), lines[1] - lines[0] + 32, 'none', TEN, 1.4, dash='5 3'))
    o.append(T(gx + gw + 6, lines[0] - 22, '拉力構材', 11.5, TEN))
    o.append(A(gx + gw + 44, gy + gh / 2, gx + gw + 76, gy + gh / 2, INK, 2.4, 11))
    o.append(T(gx + gw + 60, gy + gh / 2 - 10, '*T*', 15, INK, 'middle'))
    o.append(T(xo, gy + gh + 30, '兩條剪力面（紅）＋一條拉力面（藍）', 12.5, INK))
    o.append(T(xo, gy + gh + 50, '＝「ㄇ」字形撕裂路徑', 12.5, INK))
    o.append(T(xo, gy + gh + 76, '先畫塊體、再數孔：剪力面各 2.5 孔、', 12, MUT))
    o.append(T(xo, gy + gh + 94, '拉力面 1 孔（兩個半孔）', 12, MUT))
    return svg(W, H, '\n'.join(o), '塊狀剪力的破壞塊體')
