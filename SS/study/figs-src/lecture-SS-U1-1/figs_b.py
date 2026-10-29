import math
from lib import *

KL_FP = 4.493409457909064  # tan(kL)=kL, fixed-pinned


def shape_fp(u):
    """fixed-pinned mode, u measured from the PIN (0) to the FIXED end (1). Returns unnormalised y."""
    return math.sin(KL_FP * u) - u * math.sin(KL_FP)


_FPMAX = max(abs(shape_fp(i / 1000)) for i in range(1001))
U_INFL = math.pi / KL_FP     # 0.699


# ---------------------------------------------------------------- 4-1
def fig4_1():
    W, H = 720, 300
    o = []
    st = [('*P* < *P*_{cr}', '穩定平衡', '推一下會滾回來', TEN),
          ('*P* = *P*_{cr}', '中性平衡（臨界）', '推一下就停在那', WARN),
          ('*P* > *P*_{cr}', '不穩定平衡', '推一下就滾走 → 崩塌', COMP)]
    r = 11
    for i, (pp, nm, ds, col) in enumerate(st):
        xc = 75 + i * 135
        o.append(T(xc, 34, pp, 14, INK, 'middle'))
        o.append(T(xc, 54, ds, 12.5, MUT, 'middle'))
        yb = 150
        if i == 0:
            pts = [(xc + dx, yb - 0.012 * dx * dx) for dx in range(-55, 56, 2)]
            ball = (xc, yb - r - 1.5)
            o.append(curve_arrow([(xc + 34, yb - 0.012 * 34 * 34 - r - 8), (xc + 22, yb - 0.012 * 22 * 22 - r - 14), (xc + 8, yb - r - 14)], TEN, 1.6, 8))
        elif i == 1:
            pts = [(xc - 55, yb), (xc + 55, yb)]
            ball = (xc, yb - r - 1.5)
            o.append(C(xc + 30, yb - r - 1.5, r, 'none', col, 1.2))
            o.append(A(xc + 8, yb - 2 * r - 8, xc + 26, yb - 2 * r - 8, col, 1.5, 7))
        else:
            pts = [(xc + dx, yb - 30 + 0.012 * dx * dx) for dx in range(-55, 56, 2)]
            ball = (xc, yb - 30 - r - 1.5)
            o.append(curve_arrow([(xc + 10, yb - 30 - r - 14), (xc + 28, yb - 30 + 0.012 * 28 * 28 - r - 10), (xc + 44, yb - 30 + 0.012 * 44 * 44 - r - 4)], COMP, 1.6, 8))
        o.append(P(pts, col, 3))
        o.append(C(ball[0], ball[1], r, col, None))
        o.append(T(xc, 196, nm, 14, col, 'middle', 'bold'))
    o.append(T(10, 236, '臨界荷載 *P*_{cr}：「筆直」與「微彎」兩種平衡同時成立的那一點。', 13, INK))
    o.append(T(10, 258, '它由 *E*、*I*、*L* 決定，和材料強度 *F*_{y} 無關。', 13, COMP))
    # ---- P-delta diagram
    o.append(L(430, 20, 430, 280, GRID, 1.5))
    X0, Y0 = 478, 250
    Xs, Ys = 210, 190          # δ-axis length, P-axis length (P/Pcr = 1 at 0.8*Ys)
    pc = Y0 - 0.8 * Ys
    o.append(A(X0, Y0, X0 + Xs, Y0, INK, 1.4, 8)); o.append(A(X0, Y0, X0, Y0 - Ys, INK, 1.4, 8))
    o.append(T(X0 + Xs, Y0 + 18, 'δ（中點側向位移）', 12, INK, 'end'))
    o.append(T(X0 - 8, Y0 - Ys + 6, '*P*', 14, INK, 'end'))
    o.append(T(X0 - 8, pc + 4, '*P*_{cr}', 12.5, INK, 'end'))
    o.append(L(X0, pc, X0 + Xs - 10, pc, MUT, 1, '2 3'))
    # perfect column
    o.append(L(X0, Y0, X0, pc, AC, 3.5))
    o.append(L(X0, pc, X0 + 150, pc, AC, 3.5))
    o.append(C(X0, pc, 4.5, '#fff', AC, 2))
    o.append(T(X0 + 10, pc - 10, '分歧點（理想直柱）', 12, AC, weight='bold'))
    # imperfect column delta = d0/(1-P/Pcr)
    d0 = 0.06
    sx = 150 / 1.0
    pts = []
    for i in range(200):
        p = i / 200 * 0.965
        d = d0 / (1 - p)
        if d > 1.25:
            break
        pts.append((X0 + d * sx, Y0 - p * 0.8 * Ys))
    o.append(P(pts, COMP, 2.6))
    o.append(T(X0 + 44, Y0 - 52, '有初始彎曲 δ_{0} 的真實柱：', 12, COMP))
    o.append(T(X0 + 44, Y0 - 34, 'δ = δ_{0} / (1 − *P*/*P*_{cr})', 12.5, COMP, weight='bold'))
    o.append(T(X0 + 44, Y0 - 16, '沒有分歧，彎曲從一開始就在長', 11.5, MUT))
    o.append(T(X0 + Xs / 2 - 6, 30, '荷載–位移的觀點', 13.5, INK, 'middle', 'bold'))
    return svg(W, H, '\n'.join(o), '挫屈的三種平衡狀態與荷載位移曲線')


# ---------------------------------------------------------------- 4-2
def _xf(pts, ang, cx, cy, dx=0, dy=0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + (x - cx) * c - (y - cy) * s + dx, cy + (x - cx) * s + (y - cy) * c + dy) for x, y in pts]


def fig4_2():
    W, H = 720, 320
    o = []
    titles = [('① 彎曲挫屈', COMP), ('② 扭轉挫屈', KEY), ('③ 彎扭挫屈', WARN)]
    for i in (1, 2):
        o.append(L(240 * i, 18, 240 * i, 300, GRID, 1.5))
    for i, (tt, col) in enumerate(titles):
        o.append(T(20 + 240 * i, 30, tt, 15, col, weight='bold'))
    # 1: H section, translate along x (weak-axis buckling)
    cx, cy = 110, 128
    bf, d, tf, tw = 80, 90, 9, 6
    Hs = [(cx - bf / 2, cy - d / 2), (cx + bf / 2, cy - d / 2), (cx + bf / 2, cy - d / 2 + tf), (cx + tw / 2, cy - d / 2 + tf),
          (cx + tw / 2, cy + d / 2 - tf), (cx + bf / 2, cy + d / 2 - tf), (cx + bf / 2, cy + d / 2), (cx - bf / 2, cy + d / 2),
          (cx - bf / 2, cy + d / 2 - tf), (cx - tw / 2, cy + d / 2 - tf), (cx - tw / 2, cy - d / 2 + tf), (cx - bf / 2, cy - d / 2 + tf)]
    o.append(P(Hs, STEEL, 1.2, fill=STEEL2, close=True, dash='4 3'))
    o.append(P(_xf(Hs, 0, cx, cy, 30), COMP, 1.8, fill=COMPM, close=True, op=0.9))
    o.append(A(cx + 2, cy, cx + 28, cy, INK, 1.6, 8))
    o.append(C(cx, cy, 3, INK, None)); o.append(T(cx - 6, cy - 6, 'C=S', 11.5, INK, 'end'))
    o.append(L(cx, cy - 62, cx, cy + 62, MUT, 0.8, '6 3 2 3')); o.append(T(cx + 4, cy - 56, '*y*', 13, MUT))
    # 2: cruciform rotates
    cx, cy = 350, 128
    a, t = 48, 8
    cr = [(cx - t / 2, cy - a), (cx + t / 2, cy - a), (cx + t / 2, cy - t / 2), (cx + a, cy - t / 2), (cx + a, cy + t / 2), (cx + t / 2, cy + t / 2),
          (cx + t / 2, cy + a), (cx - t / 2, cy + a), (cx - t / 2, cy + t / 2), (cx - a, cy + t / 2), (cx - a, cy - t / 2), (cx - t / 2, cy - t / 2)]
    o.append(P(cr, STEEL, 1.2, fill=STEEL2, close=True, dash='4 3'))
    o.append(P(_xf(cr, math.radians(20), cx, cy), KEY, 1.8, fill='#d1c4e9', close=True, op=0.9))
    arc = [(cx + 62 * math.cos(math.radians(a_)), cy + 62 * math.sin(math.radians(a_))) for a_ in range(-80, -38, 3)]
    o.append(curve_arrow(arc, KEY, 1.6, 8))
    o.append(T(cx + 52, cy - 48, 'φ', 14, KEY, weight='bold'))
    o.append(C(cx, cy, 3, INK, None)); o.append(T(cx + 8, cy + 20, 'C=S', 11.5, INK))
    # 3: equal angle, shear centre at heel
    hx, hy = 560, 168   # heel (shear centre S)
    leg, tt = 80, 9
    ang = [(hx, hy), (hx + leg, hy), (hx + leg, hy - tt), (hx + tt, hy - tt), (hx + tt, hy - leg), (hx, hy - leg)]
    o.append(P(ang, STEEL, 1.2, fill=STEEL2, close=True, dash='4 3'))
    xbar = 0.282 * leg  # proportional to L100x100x10
    Cx, Cy = hx + xbar, hy - xbar
    new = _xf(ang, math.radians(-14), hx, hy, 16, -16)
    o.append(P(new, WARN, 1.8, fill=WARNM, close=True, op=0.9))
    o.append(L(hx - 30, hy + 30, hx + 70, hy - 70, MUT, 0.8, '6 3 2 3'))
    o.append(C(hx, hy, 3.5, INK, None)); o.append(T(hx - 6, hy + 16, 'S', 13, INK, 'end', 'bold'))
    o.append(C(Cx, Cy, 3.5, '#fff', INK, 1.5)); o.append(T(Cx + 6, Cy + 14, 'C', 13, INK, weight='bold'))
    o.append(A(hx + 2, hy - 2, hx + 15, hy - 15, INK, 1.5, 7))
    arc = [(hx + 52 * math.cos(math.radians(a_)), hy + 52 * math.sin(math.radians(a_))) for a_ in range(-2, 16, 3)]
    o.append(curve_arrow(arc[::-1], WARN, 1.6, 8))
    o.append(T(hx + 58, hy + 18, '平移＋轉動', 12, WARN))
    # captions
    caps = [('斷面只平移、不轉動', '雙軸對稱：H、箱型、圓管', '→ 一般柱都是這種'),
            ('斷面繞形心轉動、形心不動', '扭轉勁度極低的雙對稱斷面（十字形）', '→ 少見但存在'),
            ('形心 C ≠ 剪力中心 S，彎與扭綁在一起', '單對稱／不對稱：角鋼、T 型、槽鋼', '→ 單角鋼壓桿幾乎都由它控制')]
    for i, (a1, a2, a3) in enumerate(caps):
        x = 20 + 240 * i
        o.append(T(x, 236, a1, 12.5, INK))
        o.append(T(x, 258, a2, 12, MUT))
        o.append(T(x, 282, a3, 13, titles[i][1], weight='bold'))
    o.append(T(20, 60, '虛線：原斷面　實色：挫屈後（柱中央處的斷面）', 11, MUT))
    return svg(W, H, '\n'.join(o), '三種挫屈模式的斷面運動')


# ---------------------------------------------------------------- 5-1
def fig5_1():
    W, H = 720, 420
    o = []
    top, Lp = 60, 160
    bot = top + Lp
    a = 30
    cols = [95, 255, 415, 590]
    names = ['兩端鉸接', '兩端固接（無側移）', '一固一鉸', '一固一自由（懸臂）']
    for xc, nm in zip(cols, names):
        o.append(T(xc, 28, nm, 14, INK, 'middle', 'bold'))
    def draw(xc, fn, col=COMP, t0=0.0, t1=1.0, y0=top, Ln=Lp, dash=None, w=3):
        pts = [(xc + a * fn(t0 + (t1 - t0) * i / 120), y0 + Ln * (t0 + (t1 - t0) * i / 120)) for i in range(121)]
        return P(pts, col, w, dash=dash)
    # 1 pinned-pinned
    xc = cols[0]
    o.append(L(xc, top, xc, bot, STEEL, 1, '4 3'))
    o.append(draw(xc, lambda t: math.sin(math.pi * t)))
    o.append(C(xc, top, 5)); o.append(C(xc, bot, 5))
    o.append(dim(xc - 40, top, xc - 40, bot, '*KL* = *L*', AC, size=12.5, side=1, lab_off=8))
    # 2 fixed-fixed
    xc = cols[1]
    o.append(L(xc, top, xc, bot, STEEL, 1, '4 3'))
    o.append(draw(xc, lambda t: 0.5 * (1 - math.cos(2 * math.pi * t))))
    o.append(fixed_wall(xc, top, 44, INK, top=True)); o.append(fixed_wall(xc, bot, 44, INK))
    for t in (0.25, 0.75):
        o.append(C(xc + a * 0.5, top + Lp * t, 4.5, WARN, None))
    o.append(T(xc + a * 0.5 + 8, top + Lp * 0.25 - 4, '反曲點 *L*/4', 11.5, WARN))
    o.append(T(xc + a * 0.5 + 8, top + Lp * 0.75 + 12, '反曲點 3*L*/4', 11.5, WARN))
    o.append(dim(xc - 22, top + Lp * .25, xc - 22, top + Lp * .75, '*KL* = 0.5*L*', AC, size=12.5, side=1, lab_off=8))
    # 3 fixed top, pinned bottom ; t from top -> u = 1 - t from pin
    xc = cols[2]
    o.append(L(xc, top, xc, bot, STEEL, 1, '4 3'))
    o.append(draw(xc, lambda t: shape_fp(1 - t) / _FPMAX))
    o.append(fixed_wall(xc, top, 44, INK, top=True)); o.append(C(xc, bot, 5))
    ti = 1 - U_INFL
    xi = xc + a * shape_fp(U_INFL) / _FPMAX
    o.append(C(xi, top + Lp * ti, 4.5, WARN, None))
    o.append(T(xi + 8, top + Lp * ti - 4, '反曲點（距固端 0.30*L*）', 11.5, WARN))
    o.append(dim(xc - 22, top + Lp * ti, xc - 22, bot, '*KL* = 0.70*L*', AC, size=12.5, side=1, lab_off=8))
    # 4 cantilever: fixed bottom, free top; mirror below
    xc = cols[3] - 30
    base = bot
    o.append(L(xc, top, xc, base, STEEL, 1, '4 3'))
    # u from base: y = 1-cos(pi u /2) ; t from top: u = 1 - t
    o.append(draw(xc, lambda t: 1 - math.cos(math.pi / 2 * (1 - t))))
    o.append(draw(xc, lambda t: 1 - math.cos(math.pi / 2 * (t - 1)), COMP, 1.0, 2.0, top, Lp, dash='5 4', w=2))
    o.append(fixed_wall(xc, base, 44, INK))
    o.append(L(xc + a, top, xc + a, top + 2 * Lp, MUT, 1, '2 3'))
    o.append(C(xc + a, top, 4.5, '#fff', INK, 1.4)); o.append(C(xc + a, top + 2 * Lp, 4.5, '#fff', INK, 1.4))
    o.append(dim(xc + a + 22, top, xc + a + 22, top + 2 * Lp, '*KL* = 2*L*', AC, size=12.5, side=-1, lab_off=8, anchor='start'))
    o.append(dim(xc - 22, top, xc - 22, base, '*L*', MUT, size=12.5, side=1, lab_off=8))
    o.append(T(xc - 12, base + 60, '鏡射的', 11.5, MUT, 'end'))
    o.append(T(xc - 12, base + 76, '虛擬下半段', 11.5, MUT, 'end'))
    # K labels
    lab = [('*K* = 1.0', '設計 1.0'), ('*K* = 0.5', '設計 0.65'), ('*K* = 0.7', '設計 0.80'), ('*K* = 2.0', '設計 2.1')]
    for i, (k1, k2) in enumerate(lab):
        x = cols[i] if i < 3 else 676
        y = bot + 48 if i < 3 else bot + 48
        o.append(T(x, y, k1, 17, COMP, 'middle', 'bold'))
        o.append(T(x, y + 22, k2, 12.5, MUT, 'middle'))
    o.append(T(20, H - 18, '曲線為各邊界條件的精確挫屈模態（一固一鉸解 tan *kL* = *kL*，*kL* = 4.493），反曲點位置由模態算出、非目測。', 11.5, MUT))
    return svg(W, H, '\n'.join(o), '有效長度係數與挫屈模態')


# ---------------------------------------------------------------- 5-2
def fig5_2():
    W, H = 720, 400
    o = []
    hc = 118
    a = 26
    o.append(L(360, 16, 360, 386, GRID, 1.5))
    for side in (0, 1):
        x0 = 70 + side * 360
        span = 200
        ytop, ybot = 304 - hc, 304
        col = TEN if side == 0 else COMP
        o.append(T(x0 - 50, 30, '無側移（有斜撐）' if side == 0 else '有側移（純剛架）', 15, col, weight='bold'))
        o.append(T(x0 - 50, 50, '柱底鉸接、柱頂與剛性梁剛接', 12, MUT))
        if side == 0:
            o.append(L(x0, ytop, x0 + span, ybot, STEEL, 1.2, '6 4')); o.append(L(x0 + span, ytop, x0, ybot, STEEL, 1.2, '6 4'))
            o.append(T(x0 + span / 2, ytop + hc / 2 + 30, '斜撐', 11.5, MUT, 'middle'))
            D = 0
        else:
            D = 30
        # original columns
        for xc in (x0, x0 + span):
            o.append(L(xc, ytop, xc, ybot, STEEL, 1, '4 3'))
            o.append(pin(xc, ybot + 1, INK, 9))
        o.append(L(x0 - 10, ytop, x0 + span + 10, ytop, STEEL, 6, op=0.35))
        o.append(L(x0 - 10 + D, ytop, x0 + span + 10 + D, ytop, '#455a64', 7, cap='butt'))
        for xc in (x0, x0 + span):
            if side == 0:
                pts = [(xc + a * shape_fp(u) / _FPMAX, ybot - hc * u) for u in [i / 100 for i in range(101)]]
                o.append(P(pts, col, 3))
                yi = ybot - hc * U_INFL
                xi = xc + a * shape_fp(U_INFL) / _FPMAX
                o.append(C(xi, yi, 4.5, WARN, None))
            else:
                pts = [(xc + D * math.sin(math.pi / 2 * u), ybot - hc * u) for u in [i / 100 for i in range(101)]]
                o.append(P(pts, col, 3))
                ext = [(xc + D * math.sin(math.pi / 2 * u), ybot - hc * u) for u in [1 + i / 100 for i in range(101)]]
                o.append(P(ext, col, 1.6, dash='5 4', op=0.75))
        if side == 0:
            o.append(dim(x0 - 24, ybot - hc * U_INFL, x0 - 24, ybot, '0.70*h*', AC, size=12.5, side=1, lab_off=8))
            o.append(T(x0 + span / 2, ytop - 16, '梁不動', 12, MUT, 'middle'))
        else:
            o.append(A(x0 + span + 14, ytop - 18, x0 + span + 14 + D, ytop - 18, COMP, 2, 9))
            o.append(T(x0 + span + 18 + D, ytop - 14, 'Δ', 14, COMP, weight='bold'))
            o.append(dim(x0 - 24, ybot - 2 * hc, x0 - 24, ybot, '2*h*', AC, size=12.5, side=1, lab_off=8))
            o.append(C(x0, ybot - 2 * hc, 4, '#fff', INK, 1.3))
            o.append(T(x0 + 10, ybot - 2 * hc + 4, '虛擬延伸：半波長落在柱外', 11.5, MUT))
        o.append(T(x0 + span + 26, ybot - 6, '*h*', 13, MUT))
        o.append(dim(x0 + span + 20, ytop, x0 + span + 20, ybot, '', MUT))
        o.append(T(x0 - 50, ybot + 44, '半波長 0.7*h* → *K* = 0.7（設計 0.8）' if side == 0 else '半波長 2*h* → *K* = 2.0', 14.5, col, weight='bold'))
        o.append(T(x0 - 50, ybot + 66, '反曲點在柱內' if side == 0 else '柱頂下方沒有反曲點，整層一起倒', 12.5, MUT))
    return svg(W, H, '\n'.join(o), '無側移與有側移構架的挫屈模態')


# ---------------------------------------------------------------- 5-3 (new) leaning column
def fig5_3():
    W, H = 720, 330
    o = []
    s = 0.3            # px/cm, L = 600 cm -> 180 px
    Lpx = 180
    xA, yA = 70, 270
    xD = xA + Lpx
    yB = yA - Lpx
    D = 34             # sway (drawn)
    psi = D / Lpx
    th = 0.181 * psi   # theta_B = psi*Ic/(Ic+Ib), Ic/(Ic+Ib)=0.181
    # original geometry (dashed)
    o.append(P([(xA, yA), (xA, yB), (xD, yB), (xD, yA)], STEEL, 1.2, dash='4 3'))
    # AB: y = a u + b u^3 (pinned base, sway D, top slope th*L)
    aa = (3 * D - th * Lpx) / 2; bb = D - aa
    AB = [(xA + aa * u + bb * u ** 3, yA - Lpx * u) for u in [i / 80 for i in range(81)]]
    o.append(P(AB, COMP, 3.5))
    # beam BC (rotation th at B, hinge at C): f = th*L(v - 1.5 v^2 + 0.5 v^3), clockwise -> downward
    BC = [(xA + D + Lpx * v, yB + th * Lpx * (v - 1.5 * v * v + 0.5 * v ** 3)) for v in [i / 80 for i in range(81)]]
    o.append(P(BC, '#455a64', 4))
    # CD leaner: straight
    o.append(L(xD, yA, xD + D, yB, AC, 3.5))
    for x in (xA, xD):
        o.append(pin(x, yA + 1, INK, 9))
    o.append(C(xD + D, yB, 5, '#fff', INK, 1.6))
    o.append(C(xA + D, yB, 4, INK, None))
    # load w
    for i in range(9):
        x = xA + D + 10 + i * (Lpx - 20) / 8
        o.append(A(x, yB - 40, x, yB - 8, MUT, 1.2, 6))
    o.append(L(xA + D + 10, yB - 40, xA + D + Lpx - 10, yB - 40, MUT, 1.2))
    o.append(T(xA + D + Lpx / 2, yB - 48, '*w*', 14, INK, 'middle'))
    for x, y, t, anc in ((xA - 12, yA + 4, 'A', 'end'), (xA + D - 10, yB - 6, 'B', 'end'), (xD + D + 12, yB - 6, 'C', 'start'), (xD + 14, yA + 4, 'D', 'start')):
        o.append(T(x, y, t, 14, INK, anc, 'bold'))
    o.append(T(xA + D / 2 + 26, yA - Lpx / 2, 'AB', 13, COMP, weight='bold'))
    o.append(T(xA + D / 2 + 26, yA - Lpx / 2 + 16, '彎曲抗側', 11.5, COMP))
    o.append(T(xD + D / 2 + 14, yA - Lpx / 2, 'CD 靠桿', 13, AC, weight='bold'))
    o.append(T(xD + D / 2 + 14, yA - Lpx / 2 + 16, '兩端鉸、只傾斜', 11.5, AC))
    o.append(A(xD + D + 26, yB + 40, xD + D + 26 + 26, yB + 40, COMP, 2, 9)); o.append(T(xD + D + 56, yB + 45, 'Δ', 14, COMP, weight='bold'))
    o.append(T(30, 312, '圖依 SS-2013-2 的 *I*_{c}/*I*_{b} = 0.221 以傾角變位法繪製（θ_{B} = ψ·*I*_{c}/(*I*_{c}+*I*_{b})）', 11.5, MUT))
    # right text
    x, y = 400, 40
    o.append(T(x, y, 'SS-2013-2（102 年）', 14.5, INK, weight='bold'))
    rows = [('① 對位圖（有側移）', INK, True),
            ('*G*_{A} = 10（鉸）、*G*_{B} = *I*_{c}/*I*_{b} = 0.221 → *K* = 1.71', INK, False),
            ('② 靠桿把重量丟給 AB', INK, True),
            ('Σ*P* = *wL*，但只有 AB 提供 Σ*P*_{eK} = 575.6 tf', INK, False),
            ('Σ*P* / *P*_{AB} = 2（純幾何比，與 *w* 無關）', INK, False),
            ('③ LeMessurier 放大', INK, True),
            ('*K*′ = *K*·√(Σ*P*/*P*_{I}) = 1.71 × √2 = 2.42', COMP, False),
            ('*w*_{cr} = Σ*P*_{eK} / *L* = 575.6 / 6 = 96.0 tf/m', COMP, False)]
    y += 30
    for t, c, b in rows:
        o.append(T(x, y, t, 13 if b else 12.5, c, weight='bold' if b else None))
        y += 26 if b else 22
    o.append(T(x, y + 8, '若把 CD 當一般柱：*w*_{cr} 變 192（高估 2 倍）', 12.5, WARN, weight='bold'))
    return svg(W, H, '\n'.join(o), '靠桿效應：重量在、勁度不在')
