"""lecture-SM-U3-2 figures. Geometry and every number come from calcs.py (solution-verified).
Usage: python3 gen_figs.py <lecture.html>   (replaces the <svg> right after each <!--FIG:id--> marker)"""
import sys, os, re, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'U1-1'))
from svglib import *
from calcs import N, ka_rankine, w09
d = math.radians
FIG = {}
BRN, BLU, RED, GRN, ORG, PUR = "#6d4c41", "#1565c0", "#c62828", "#2e7d32", "#ef6c00", "#6a1b9a"
CON, CON_S = "#cfd8dc", "#546e7a"
SOIL = "#efe3d3"

def arr(x1, y1, x2, y2, c, mk, sw=2.2, dash=None):
    return L(x1, y1, x2, y2, c, sw, dash, f' marker-end="url(#{mk})"')

def hatch_ground(x1, x2, y, step=10):
    s = [L(x1, y, x2, y, "#5d4037", 1.6)]
    x = x1
    while x < x2 - 1:
        s.append(L(x, y, x - 6, y + 7, "#8d6e63", 1)); x += step
    return "".join(s)

# ======================================================= f0: three ways to fail
def f0():
    r = N['09']; B, H, t = 2.49, 6.0, 0.6
    U = 26
    b = [arrow_defs((("f0a", RED), ("f0b", BLU), ("f0g", "#455a64")))]
    titles = ["① 滑動：整面牆平移", "② 傾倒：繞牆趾轉動", "③ 承載：牆趾壓陷"]
    checks = ["ΣH：底面抗剪 ≥ 1.5 × 推力", "ΣM（對牆趾）：M_{R} ≥ 2.0 × M_{O}", "底壓：q_{u} ≥ 3.0 × 接觸壓力"]
    for k in range(3):
        ox, oy = 40 + k*250, 250       # toe at (ox+30, oy)
        tx = ox + 40
        poly = [(0, 0), (B, 0), (B, H), (B - t, H)]
        P = [(tx + x*U, oy - y*U) for x, y in poly]
        b.append(R(ox, oy, 220, 26, SOIL)); b.append(hatch_ground(ox, ox + 220, oy))
        # backfill
        b.append(PG([(tx + B*U, oy), (ox + 220, oy), (ox + 220, oy - H*U - 22), (tx + B*U, oy - H*U)], SOIL))
        if k == 0:
            G = [(x + 16, y) for x, y in P]
        elif k == 1:
            ang = d(-7); cx, cy = P[0]
            G = [(cx + (x-cx)*math.cos(ang) - (y-cy)*math.sin(ang), cy + (x-cx)*math.sin(ang) + (y-cy)*math.cos(ang)) for x, y in P]
        else:
            ang = d(-4); cx, cy = P[1]
            G = [(cx + (x-cx)*math.cos(ang) - (y-cy)*math.sin(ang), cy + (x-cx)*math.sin(ang) + (y-cy)*math.cos(ang) + 6) for x, y in P]
        b.append(PG(P, CON, CON_S, 1.2, ' opacity="0.45" stroke-dasharray="4,3"'))
        b.append(PG(G, CON, CON_S, 1.8))
        # thrust arrow at H/3 on back
        yb = oy - H/3*U
        b.append(arr(tx + B*U + 58, yb, tx + B*U + 6, yb, RED, "f0a"))
        b.append(T(tx + B*U + 34, yb - 8, "P_{ah}", 12, RED))
        if k == 0:
            b.append(arr(tx + 10, oy + 14, tx + B*U - 4, oy + 14, BLU, "f0b"))
            b.append(T(tx + B*U/2, oy + 40, "底面摩擦／黏著", 11.5, BLU))
            b.append(arr(G[0][0] - 2, oy - 60, G[0][0] - 2 - 28, oy - 60, "#455a64", "f0g", 1.6))
        elif k == 1:
            b.append(C(P[0][0], P[0][1], 5, RED))
            b.append(T(P[0][0] - 6, oy + 40, "轉動中心＝牆趾", 11.5, RED, "start"))
            b.append(f'<path d="M{P[0][0]+44:.1f} {oy-104:.1f} A 112 112 0 0 0 {P[0][0]+4:.1f} {oy-112:.1f}" fill="none" stroke="#455a64" stroke-width="1.6" marker-end="url(#f0g)"/>')
        else:
            q = r['qtoe']; sc = 0.25
            b.append(PG([(tx, oy + 4), (tx, oy + 4 + q*sc*0.25), (tx + B*U, oy + 4)], "#bbdefb", BLU, 1.2))
            b.append(T(tx + 4, oy + 40, "牆趾底壓最大", 11.5, BLU, "start"))
        b.append(T(ox + 110, 40, titles[k], 15, "#0d47a1", weight=700))
        b.append(T(ox + 110, 310, checks[k], 12, INK))
    b.append(T(400, 336, "三種死法用同一張自由體圖：力平衡管滑動、力矩平衡管傾倒、底壓分布管承載（牆形取 SM-2009-4，B = 2.49 m、H = 6 m，位移放大示意）", 11.5, MUT))
    return svg(800, 350, b)

# ======================================================= f1: water level (SM-2004-3)
def f1():
    r = N['04']; Ka = r['Ka']
    px0, py0, px1, py1 = 90, 290, 560, 50
    X = lambda x: px0 + x/6*(px1-px0); Y = lambda p: py0 - p/240*(py0-py1)
    b = [T(380, 26, "SM-2004-3：水位每升高一點，總推力只會變大", 15, "#0d47a1", weight=700)]
    xs = [i*6/150 for i in range(151)]
    pa = [0.5*Ka*19.2*36 - 0.5*Ka*9.81*x*x for x in xs]
    pw = [0.5*9.81*x*x for x in xs]
    for gx in range(7):
        b.append(L(X(gx), py0, X(gx), py0 + 4, "#455a64", 1)); b.append(T(X(gx), py0 + 18, f"{gx}", 11, MUT))
    for gp in range(0, 241, 40):
        b.append(L(px0 - 4, Y(gp), px0, Y(gp), "#455a64", 1)); b.append(T(px0 - 8, Y(gp) + 4, f"{gp}", 11, MUT, "end"))
        b.append(L(px0, Y(gp), px1, Y(gp), "#eceff1", 1))
    b.append(L(px0, py0, px1, py0, "#455a64", 1.6)); b.append(L(px0, py0, px0, py1, "#455a64", 1.6))
    b.append(T((px0+px1)/2, py0 + 38, "水位距牆底高度 x (m)", 12, MUT))
    b.append(T(px0 - 6, py1 - 12, "推力 (kN/m)", 12, MUT, "start"))
    b.append(PL([(X(x), Y(p)) for x, p in zip(xs, pa)], ORG, 2, "6,4"))
    b.append(PL([(X(x), Y(p)) for x, p in zip(xs, pw)], BLU, 2, "6,4"))
    b.append(PL([(X(x), Y(a+w)) for x, a, w in zip(xs, pa, pw)], RED, 3))
    b.append(L(px0, Y(146), px1, Y(146), GRN, 1.6, "3,3"))
    b.append(T(px1 - 4, Y(146) - 8, "抵抗力 146 kN/m", 12, GRN, "end", 700))
    xc = r['x']
    b.append(C(X(xc), Y(146), 5.5, RED, "#fff", 1.5)); b.append(L(X(xc), Y(146), X(xc), py0, RED, 1, "3,3"))
    b.append(T(X(xc) + 8, py0 - 8, f"x = {xc:.3f} m 開始滑動", 12, RED, "start", 700))
    b.append(T(X(6) - 4, Y(r['Ph6']) + 16, f"總推力 {r['Ph6']:.1f}", 12, RED, "end", 700))
    b.append(T(X(0) + 6, Y(r['Ph0']) - 10, f"無水 {r['Ph0']:.2f}", 12, RED, "start"))
    b.append(T(X(5.9), Y(pa[-1]) + 18, "有效土壓（K_{a}γ′，遞減）", 11.5, ORG, "end"))
    b.append(T(X(4.3), Y(0.5*9.81*4.3**2) + 18, "水壓（K = 1，遞增）", 11.5, BLU, "start"))
    # side note
    b.append(R(590, 70, 170, 190, "#fff3e0", "#ffcc80", 1))
    for i, s in enumerate(["每升 1 m 水的淨增量", "½γ_{w}(1 − K_{a})x²", f"K_{{a}} = {Ka:.3f}", "→ 水的側壓是土的",  f"1/K_{{a}} = {r['ratio']:.1f} 倍", "", "排水是成本最低的", "穩定對策"]):
        b.append(T(675, 96 + i*21, s, 12.5, "#e65100" if i in (1, 4, 6, 7) else INK, weight=700 if i in (4,) else None))
    return svg(780, 340, b)

# ======================================================= f2: real back vs virtual back
def f2():
    b = [arrow_defs((("f2r", RED), ("f2k", "#455a64")))]
    b.append(L(400, 30, 400, 420, "#b0bec5", 1.2, "5,4"))
    # ---- left: SM-2009-4, scale U px/m
    r = N['09']; B, H, t = 2.49, 6.0, 0.6; U = 44
    tx, oy = 60, 360
    X = lambda x: tx + x*U; Y = lambda y: oy - y*U
    b.append(T(200, 26, "重力式（SM-2009-4）：牆背就是真牆背", 14, "#0d47a1", weight=700))
    ext = 3.2
    b.append(PG([(X(B), Y(H)), (X(B+ext), Y(H + ext*math.tan(d(20)))), (X(B+ext), Y(0)), (X(B), Y(0))], SOIL))
    b.append(L(X(B), Y(H), X(B+ext), Y(H + ext*math.tan(d(20))), "#8d6e63", 1.6))
    b.append(T(X(B+1.6), Y(H + 1.6*math.tan(d(20))) - 8, "α = 20°", 12, BRN))
    b.append(PG([(X(0), Y(0)), (X(B), Y(0)), (X(B), Y(H)), (X(B-t), Y(H))], CON, CON_S, 1.6))
    b.append(hatch_ground(X(-0.6), X(B+ext), Y(0)))
    # pressure triangle normal to back (horizontal width proportional), drawn behind back
    pmax = r['Ka']*18*6; sc = 1.6
    b.append(PG([(X(B), Y(H)), (X(B) + pmax*sc, Y(0)), (X(B), Y(0))], "#ffcdd2", RED, 1, ' opacity="0.7"'))
    b.append(T(X(B) + pmax*sc + 4, Y(0) - 6, f"{pmax:.1f} kPa", 11, RED, "start"))
    # Pa arrow at H/3 parallel to slope, pointing into wall (down-left)
    L_ = 110; ya = Y(H/3); xe = X(B)
    xs_, ys_ = xe + L_*math.cos(d(20)), ya - L_*math.sin(d(20))
    b.append(arr(xs_, ys_, xe + 3, ya - 1, RED, "f2r", 3))
    b.append(T(xs_ + 4, ys_ - 24, f"P_{{a}} = {r['Pa']:.1f}", 12, RED, "end", 700))
    b.append(T(xs_ + 4, ys_ - 8, "∥地表，與水平夾 20°", 11, RED, "end"))
    b.append(T(X(B) + 8, ya + 22, "作用在 H/3、力臂 B", 11, MUT, "start"))
    b.append(T(X(B*0.55), Y(H*0.45), "W", 13, "#37474f", weight=700))
    b.append(hdim(oy + 22, X(0), X(B), "#455a64")); b.append(T(X(B/2), oy + 40, f"B = {B:.2f} m", 12))
    b.append(T(200, 428, f"V = W + P_{{av}} = {r['V']:.1f}；FS_{{OT}} = {r['FSOT']:.2f}、FS_{{SL}} = {r['FSSL']:.2f}", 12, INK))
    # ---- right: SM-2018-4 cantilever, virtual back
    r = N['18']; U = 30; tx, oy = 450, 372
    X = lambda x: tx + x*U; Y = lambda y: oy - y*U
    b.append(T(600, 26, "懸臂式（SM-2018-4）：牆背改取過踵端的虛擬牆背", 14, "#0d47a1", weight=700))
    Bt, toe, heel, tb, Hs = 5.6, 1.5, 3.5, 0.96, 7.5
    hx = toe + 0.6                      # stem back x
    a = math.tan(d(12))
    # backfill above heel (soil block, is part of free body)
    top_back = (hx, tb + Hs); top_heel = (Bt, tb + Hs + heel*a)
    b.append(PG([(X(hx), Y(tb)), (X(Bt), Y(tb)), (X(Bt), Y(top_heel[1])), (X(hx), Y(top_back[1]))], "#d7ccc8", BRN, 1.2))
    b.append(PG([(X(Bt), Y(0)), (X(Bt+2.0), Y(0)), (X(Bt+2.0), Y(top_heel[1] + 2*a)), (X(Bt), Y(top_heel[1]))], SOIL))
    b.append(L(X(hx), Y(top_back[1]), X(Bt + 2.0), Y(top_heel[1] + 2*a), "#8d6e63", 1.6))
    b.append(PG([(X(0), Y(0)), (X(Bt), Y(0)), (X(Bt), Y(tb)), (X(0), Y(tb))], CON, CON_S, 1.4))
    b.append(PG([(X(toe), Y(tb)), (X(hx), Y(tb)), (X(hx), Y(tb+Hs)), (X(toe+0.2), Y(tb+Hs))], CON, CON_S, 1.4))
    b.append(PG([(X(0), Y(tb)), (X(toe), Y(tb)), (X(toe), Y(1.75)), (X(0), Y(1.75))], SOIL, "#bcaaa4", 1))
    b.append(hatch_ground(X(-0.4), X(Bt+2.0), Y(0)))
    b.append(L(X(Bt), Y(0), X(Bt), Y(top_heel[1]), RED, 2.2, "7,4"))
    b.append(T(X(Bt) - 4, Y(top_heel[1]) - 10, "虛擬牆背", 12, RED, "end", 700))
    b.append(T(X((hx+Bt)/2), Y(tb + Hs/2), "踵上土", 12, BRN, weight=700))
    b.append(T(X((hx+Bt)/2), Y(tb + Hs/2) + 16, "＝牆的一部分", 11, BRN))
    ya = Y(r['Hp']/3); xe = X(Bt); L_ = 90
    xs_, ys_ = xe + L_*math.cos(d(12)), ya - L_*math.sin(d(12))
    b.append(arr(xs_, ys_, xe + 3, ya, RED, "f2r", 3))
    b.append(T(xs_ - 6, ys_ + 22, f"P_{{a}} = {r['Pa']:.1f}", 12, RED, "end", 700))
    b.append(vdim(X(Bt+2.4), Y(0), Y(top_heel[1]), "#455a64"))
    b.append(T(X(Bt+2.25), Y(top_heel[1]*0.62), f"H′ = {r['Hp']:.3f} m", 12, INK, "end", 700))
    b.append(T(X(Bt+2.25), Y(top_heel[1]*0.62) + 16, "7.5 + 0.96", 10.5, MUT, "end"))
    b.append(T(X(Bt+2.25), Y(top_heel[1]*0.62) + 30, "+ 3.5tan12°", 10.5, MUT, "end"))
    b.append(T(600, 428, f"踵上土重 {r['Wsoil']:.0f} kN/m 進 ΣV；FS_{{OT}} = {r['FSOT']:.2f}、FS_{{SL}} = {r['FSSL']:.2f}", 12, INK))
    return svg(800, 440, b)

# ======================================================= f3: friction base vs phi=0 base (SM-2025-3)
def f3():
    r = N['25']; PA = r['PA']
    px0, py0, px1, py1 = 80, 300, 520, 60
    Wmax = 1200
    X = lambda w: px0 + w/Wmax*(px1-px0); Y = lambda f: py0 - f/3.0*(py0-py1)
    b = [T(400, 26, "SM-2025-3 同一面牆、同一個推力：底面是砂還是 φ = 0 黏土，加重牆體的效果完全不同", 14, "#0d47a1", weight=700)]
    for gw in range(0, 1201, 200):
        b.append(L(X(gw), py0, X(gw), py0 + 4, "#455a64", 1)); b.append(T(X(gw), py0 + 18, f"{gw}", 11, MUT))
    for gf in [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
        b.append(L(px0 - 4, Y(gf), px0, Y(gf), "#455a64", 1)); b.append(T(px0 - 8, Y(gf) + 4, f"{gf:.1f}", 11, MUT, "end"))
    b.append(L(px0, py0, px1, py0, "#455a64", 1.6)); b.append(L(px0, py0, px0, py1, "#455a64", 1.6))
    b.append(T((px0+px1)/2, py0 + 38, "牆重 W (kN/m)", 12, MUT)); b.append(T(px0 - 4, py1 - 14, "FS_{SL}", 12, MUT, "start"))
    ws = [i*Wmax/120 for i in range(121)]
    fsa = [w*math.tan(d(20))/PA for w in ws]
    pts = [(X(w), Y(f)) for w, f in zip(ws, fsa) if f <= 3.0]
    b.append(PL(pts, BRN, 3))
    b.append(L(X(0), Y(r['FS']), X(Wmax), Y(r['FS']), BLU, 3))
    b.append(L(px0, Y(1.5), px1, Y(1.5), RED, 1.4, "5,4")); b.append(T(px1 - 2, Y(1.5) - 7, "要求 1.5", 12, RED, "end"))
    b.append(L(X(r['W']), py0, X(r['W']), py1 + 10, "#90a4ae", 1, "3,3"))
    b.append(T(X(r['W']) + 4, py1 + 20, f"本題 W = {r['W']:.1f}", 11.5, "#455a64", "start"))
    b.append(C(X(r['W']), Y(r['FS_sand']), 5, BRN, "#fff", 1.5)); b.append(C(X(r['W']), Y(r['FS']), 5, BLU, "#fff", 1.5))
    b.append(T(X(r['W']) - 8, Y(r['FS_sand']) - 8, f"砂底 δ = 20°：{r['FS_sand']:.2f}", 12, BRN, "end", 700))
    b.append(T(X(r['W']) + 8, Y(r['FS']) + 18, f"φ = 0 黏土：{r['FS']:.2f}（水平線）", 12, BLU, "start", 700))
    b.append(T(X(900), Y(900*math.tan(d(20))/PA) + 22, "FS = W·tanδ / P_{A}", 12, BRN, "start"))
    b.append(T(X(150), Y(r['FS']) + 20, "FS = S_{u}B / P_{A}", 12, BLU, "middle"))
    # right panel text
    b.append(R(560, 70, 220, 220, "#fff", "#dfe6ea", 1))
    lines = [("摩擦型底面（c = 0）", BRN, 700), ("抗力 ∝ 正向力 ΣV", INK, None), ("→ 加重、P_{av}、踵上土", INK, None),
             ("   都會提高 FS", INK, None), ("", INK, None), ("黏著型底面（φ = 0）", BLU, 700), ("抗力 = S_{u}·B，與 ΣV 無關", INK, None),
             ("→ 只有加寬 B、剪力榫", INK, None), ("   或降推力有用", INK, None), (f"（B 加到 7 m：FS = {30*7/PA:.2f}）", MUT, None)]
    for i, (s, c, w) in enumerate(lines):
        b.append(T(572, 96 + i*20, s, 12.5, c, "start", w))
    return svg(800, 350, b)

# ======================================================= f4: 2009-4 resultant vs B, and base pressure states
def f4():
    b = [arrow_defs((("f4k", "#455a64"),))]
    # left: FS and xbar/B vs B
    px0, py0, px1, py1 = 70, 300, 400, 60
    B0, B1 = 1.8, 3.2
    X = lambda v: px0 + (v-B0)/(B1-B0)*(px1-px0); Y = lambda f: py0 - f/2.5*(py0-py1)
    b.append(T(235, 26, "SM-2009-4：底寬 B 怎麼決定三個數字", 14, "#0d47a1", weight=700))
    for gb in [1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2]:
        b.append(L(X(gb), py0, X(gb), py0 + 4, "#455a64", 1)); b.append(T(X(gb), py0 + 18, f"{gb:.1f}", 11, MUT))
    for gf in [0, 0.5, 1.0, 1.5, 2.0, 2.5]:
        b.append(L(px0 - 4, Y(gf), px0, Y(gf), "#455a64", 1)); b.append(T(px0 - 8, Y(gf) + 4, f"{gf:.1f}", 11, MUT, "end"))
        b.append(L(px0, Y(gf), px1, Y(gf), "#eceff1", 1))
    b.append(L(px0, py0, px1, py0, "#455a64", 1.6)); b.append(L(px0, py0, px0, py1, "#455a64", 1.6))
    b.append(T((px0+px1)/2, py0 + 38, "牆底寬 B (m)", 12, MUT))
    Bs = [B0 + i*(B1-B0)/140 for i in range(141)]
    R_ = [w09(x) for x in Bs]
    b.append(PL([(X(x), Y(r['FSOT'])) for x, r in zip(Bs, R_)], RED, 2.6))
    b.append(PL([(X(x), Y(r['FSSL'])) for x, r in zip(Bs, R_)], BLU, 2.6))
    b.append(PL([(X(x), Y(3*r['xbar']/x)) for x, r in zip(Bs, R_)], PUR, 2.2, "6,4"))
    b.append(T(X(3.0) + 6, Y(w09(3.0)['FSOT']) + 16, "FS_{OT}", 12, RED, "start", 700))
    b.append(T(X(3.15), Y(w09(3.15)['FSSL']) + 18, "FS_{SL}", 12, BLU, "end", 700))
    b.append(T(X(1.85), Y(3*w09(1.85)['xbar']/1.85) - 8, "3x̄/B（=1 即 e = B/6）", 11.5, PUR, "start"))
    for v, c in [(2.0, RED), (1.5, BLU), (1.0, PUR)]:
        b.append(L(px0, Y(v), px1, Y(v), c, 1, "2,3"))
    r = N['09']
    for bx, lab, c, yy in [(r['B'], f"B = {r['B']:.2f}（e = B/6）", PUR, 1.0), (r['B_OT2'], f"{r['B_OT2']:.2f}", RED, 2.0), (r['B_SL15'], f"{r['B_SL15']:.2f}", BLU, 1.5)]:
        b.append(C(X(bx), Y(yy), 4.5, c, "#fff", 1.5))
        b.append(L(X(bx), Y(yy), X(bx), py0, c, 1, "3,3"))
    b.append(T(X(r['B']) - 4, py0 - 6, f"{r['B']:.2f}", 11, PUR, "end", 700))
    b.append(T(X(r['B_OT2']) + 3, py0 - 20, f"{r['B_OT2']:.2f}", 11, RED, "start", 700))
    b.append(T(X(r['B_SL15']) + 3, py0 - 6, f"{r['B_SL15']:.2f}", 11, BLU, "start", 700))
    b.append(T(235, 356, f"e = B/6 只保證牆踵不受拉；要 FS_{{OT}} ≥ 2 需 B ≥ {r['B_OT2']:.2f}、FS_{{SL}} ≥ 1.5 需 B ≥ {r['B_SL15']:.2f}", 11.5, INK))
    # right: three base pressure states, same V, B=1 unit
    ox = 440; Wd = 300
    b.append(T(610, 26, "合力位置 → 底壓形狀", 14, "#0d47a1", weight=700))
    V, B = 1.0, 1.0
    for k, (e, lab, c) in enumerate([(B/12, "e < B/6：梯形，全斷面受壓", GRN), (B/6, "e = B/6：三角形，牆踵剛好 0", ORG), (B/4, "e > B/6：牆踵脫開，壓力集中", RED)]):
        y0 = 96 + k*134
        b.append(R(ox + 20, y0, Wd - 40, 14, CON, CON_S, 1))
        x0, x1 = ox + 20, ox + Wd - 20; s = 22   # px per (V/B)
        if e <= B/6 + 1e-9:
            qt, qh = V/B*(1 + 6*e/B), V/B*(1 - 6*e/B)
            poly = [(x0, y0 + 14), (x0, y0 + 14 + qt*s), (x1, y0 + 14 + qh*s), (x1, y0 + 14)]
            txt = f"q_{{toe}} = {qt:.2f}、q_{{heel}} = {qh:.2f}"
        else:
            Lc = 3*(B/2 - e); qt = 2*V/(3*(B/2 - e))
            poly = [(x0, y0 + 14), (x0, y0 + 14 + qt*s), (x0 + Lc*(x1-x0), y0 + 14)]
            txt = f"接觸長 3(B/2 − e) = {Lc:.2f}B、q_{{toe}} = {qt:.2f}"
        b.append(PG(poly, "#bbdefb", BLU, 1.2))
        xr = x0 + (B/2 - e)*(x1-x0)
        b.append(arr(xr, y0 - 22, xr, y0 - 2, "#455a64", "f4k", 2))
        b.append(T(x0 - 4, y0 + 10, "趾", 11, MUT, "end")); b.append(T(x1 + 4, y0 + 10, "踵", 11, MUT, "start"))
        b.append(T(ox + Wd/2, y0 - 26, lab, 12, c, weight=700))
        b.append(T(x1, y0 + 14 + 22*2.67 + 16, txt + "（×V/B）", 11, INK, "end"))
    return svg(780, 490, b)

# ======================================================= f5: inclination factors + q_max vs V/B'
def f5():
    b = [arrow_defs((("f5k", "#455a64"),))]
    px0, py0, px1, py1 = 70, 290, 400, 60
    X = lambda t: px0 + t/30*(px1-px0); Y = lambda f: py0 - f*(py0-py1)
    b.append(T(235, 26, "傾斜因數：θ 只有 14°，N_{γ} 項就剩三成", 14, "#0d47a1", weight=700))
    for gt in range(0, 31, 5):
        b.append(L(X(gt), py0, X(gt), py0 + 4, "#455a64", 1)); b.append(T(X(gt), py0 + 18, f"{gt}°", 11, MUT))
    for gf in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        b.append(L(px0 - 4, Y(gf), px0, Y(gf), "#455a64", 1)); b.append(T(px0 - 8, Y(gf) + 4, f"{gf:.1f}", 11, MUT, "end"))
        b.append(L(px0, Y(gf), px1, Y(gf), "#eceff1", 1))
    b.append(L(px0, py0, px1, py0, "#455a64", 1.6)); b.append(L(px0, py0, px0, py1, "#455a64", 1.6))
    b.append(T((px0+px1)/2, py0 + 38, "合力傾角 θ = tan⁻¹(ΣH/ΣV)", 12, MUT))
    ts = [i*30/150 for i in range(151)]
    b.append(PL([(X(t), Y((1-t/90)**2)) for t in ts], GRN, 2.6))
    b.append(PL([(X(t), Y((1-t/32)**2)) for t in ts if t <= 32], BLU, 2.6))
    b.append(PL([(X(t), Y((1-t/30)**2)) for t in ts], BLU, 1.6, "6,4"))
    b.append(T(X(29), Y(0.38), "i_{c} = (1 − θ/90°)²", 12, GRN, "end", 700))
    b.append(T(X(21), Y(0.20), "i_{γ} = (1 − θ/φ′)²", 12, BLU, "start", 700))
    b.append(T(X(17), Y(0.90), "i_{γ}：實線 φ′ = 32°、虛線 30°", 11, BLU, "start"))
    for j, (key, phi, lab) in enumerate([('16_3', 32, "2016-3"), ('16_4', 30, "2016-4")]):
        th = N[key]['th']; g = (1-th/phi)**2
        b.append(C(X(th), Y(g), 4.5, RED, "#fff", 1.5)); b.append(C(X(th), Y((1-th/90)**2), 4.5, RED, "#fff", 1.5))
        b.append(T(X(0.6), Y(0.085 - 0.06*j), f"{lab}：θ = {th:.2f}° → i_{{γ}} = {g:.3f}", 11, RED, "start", 700))
    b.append(T(235, 345, f"2016-3 不做傾斜修正：FS_{{BC}} = {N['16_3']['FSBC_noincl']:.2f}；做了：{N['16_3']['FSBC']:.2f}（低於 3.0）", 11.5, INK))
    # right: q_max (trapezoid) vs V/B' uniform, SM-2016-4
    r = N['16_4']; ox = 450; B = 5.0; U = 56; y0 = 90
    X2 = lambda x: ox + 20 + x*U
    b.append(T(610, 26, "SM-2016-4：q_{u} 用 B′，分母也要用 B′", 14, "#0d47a1", weight=700))
    s = 0.33
    b.append(R(X2(0), y0, B*U, 16, CON, CON_S, 1))
    b.append(PG([(X2(0), y0 + 16), (X2(0), y0 + 16 + r['qmax']*s), (X2(B), y0 + 16 + r['qmin']*s), (X2(B), y0 + 16)], "#e3f2fd", BLU, 1.2, ' stroke-dasharray="5,3"'))
    b.append(PG([(X2(0), y0 + 16), (X2(0), y0 + 16 + r['qeff']*s), (X2(r['Bp']), y0 + 16 + r['qeff']*s), (X2(r['Bp']), y0 + 16)], "#ffe0b2", ORG, 1.6, ' opacity="0.85"'))
    b.append(T(X2(0) + 2, y0 + 16 + r['qmax']*s + 16, f"梯形 q_{{max}} = {r['qmax']:.1f}、q_{{min}} = {r['qmin']:.1f}", 11.5, BLU, "start", 700))
    b.append(T(X2(r['Bp']/2), y0 + 16 + r['qeff']*s/2, f"V/B′ = {r['qeff']:.1f}", 12, ORG, "middle", 700))
    b.append(T(X2(r['Bp']/2), y0 + 16 + r['qeff']*s/2 + 18, f"均布在 B′ = {r['Bp']:.3f}", 11.5, ORG, "middle"))
    xr = X2(r['xbar'])
    b.append(arr(xr, y0 - 30, xr, y0 - 2, "#455a64", "f5k", 2)); b.append(T(xr + 4, y0 - 18, f"x̄ = {r['xbar']:.3f}", 11, INK, "start"))
    b.append(T(X2(0), y0 - 6, "趾", 11, MUT, "end")); b.append(T(X2(B) + 4, y0 + 12, "踵", 11, MUT, "start"))
    yt = 268
    lines = [("q_{u}（B′、傾斜修正）= 642.2 kPa（題解）", INK), ("FS = q_{u} / (V/B′) = 642.2 / 254.4 = 2.52 < 3.0", ORG),
             ("錯：q_{u} / q_{max} = 1.89（寬度不一致）", BLU), ("（題解 2026-11-22 勘誤；要用 q_{max} 就以全寬 B 算 q_{u}）", MUT)]
    for i, (s_, c) in enumerate(lines):
        b.append(T(610, yt + i*20, s_, 12, c))
    return svg(800, 360, b)

# ======================================================= f6: M-O decomposition (SM-2016-4)
def f6():
    r = N['16_4']; H = 8.0; U = 32
    b = [arrow_defs((("f6a", RED), ("f6b", PUR), ("f6c", "#212121")))]
    b.append(T(400, 26, "SM-2016-4 ㈢：P_{ae} 拆成靜態 + 動態增量，各自有作用點", 14, "#0d47a1", weight=700))
    def panel(ox, title, kind):
        oy = 330; wx = ox + 30
        b.append(L(wx, oy, wx, oy - H*U, "#455a64", 3))
        b.append(hatch_ground(wx - 30, wx + 170, oy))
        b.append(T(ox + 95, 56, title, 13, INK, weight=700))
        return wx, oy
    # static
    wx, oy = panel(40, "靜態 P_{a}", 's')
    pm = 2*r['Pa']/H; s = 1.4
    b.append(PG([(wx, oy - H*U), (wx + pm*s, oy), (wx, oy)], "#ffcdd2", RED, 1.2))
    b.append(arr(wx + 110, oy - H/3*U, wx + 4, oy - H/3*U, RED, "f6a", 2.6))
    b.append(T(wx + 112, oy - H/3*U - 8, f"{r['Pa']:.1f} @ H/3 = 2.67", 11.5, RED, "start", 700))
    # dynamic increment: trapezoid with top = 4 x bottom -> centroid 0.6H
    wx, oy = panel(290, "動態增量 ΔP_{ae}", 'd')
    a = 2*r['dP']/(H*5); bt = 4*a; s2 = 6
    b.append(PG([(wx, oy - H*U), (wx + bt*s2, oy - H*U), (wx + a*s2, oy), (wx, oy)], "#e1bee7", PUR, 1.2))
    b.append(arr(wx + 120, oy - 0.6*H*U, wx + 4, oy - 0.6*H*U, PUR, "f6b", 2.6))
    b.append(T(wx + 122, oy - 0.6*H*U - 8, f"{r['dP']:.2f} @ 0.6H = 4.8", 11.5, PUR, "start", 700))
    b.append(T(wx + 4, oy + 26, "等效分布：頂 = 4×底 ⇒ 形心在 0.6H", 10.5, MUT, "start"))
    # total
    wx, oy = panel(540, "合力 P_{ae}", 't')
    b.append(arr(wx + 130, oy - r['zbar']*U, wx + 4, oy - r['zbar']*U, "#212121", "f6c", 3))
    b.append(T(wx + 132, oy - r['zbar']*U - 8, f"{r['Pae']:.2f} @ {r['zbar']:.2f} m", 11.5, "#212121", "start", 700))
    for hh, c in [(H/3, RED), (0.6*H, PUR)]:
        b.append(L(wx, oy - hh*U, wx + 60, oy - hh*U, c, 1, "3,3"))
    b.append(T(400, 378, f"z̄ = [P_{{a}}(H/3) + ΔP_{{ae}}(0.6H)] / P_{{ae}} = ({r['Pa']:.1f}×2.667 + {r['dP']:.2f}×4.8) / {r['Pae']:.2f} = {r['zbar']:.2f} m（不是 H/3，也不是 H/2）", 11.5, INK))
    b.append(T(400, 398, f"K_{{ae}} = {r['Kae']:.4f}（θ′ = {r['thp']:.2f}°），P_{{ae}} = ½γH²(1 − K_{{v}})K_{{ae}}；方向同靜態：與牆背法線夾 δ = 15°", 11.5, MUT))
    return svg(800, 410, b)

# ======================================================= f7: MSE wall internal vs external
def f7():
    r = N['16_3']; H, Lr = 6.0, 4.5; U = 46
    b = [arrow_defs((("f7a", RED), ("f7b", GRN), ("f7c", BLU)))]
    tx, oy = 70, 340
    X = lambda x: tx + x*U; Y = lambda y: oy - y*U
    b.append(T(400, 24, "加勁擋土牆：外穩定把加勁區當一塊重力牆；內穩定看每一層筋（幾何取 SM-2016-3：H = 6 m、L = 4.5 m、φ′ = 32°）", 13, "#0d47a1", weight=700))
    b.append(PG([(X(0), Y(0)), (X(Lr), Y(0)), (X(Lr), Y(H)), (X(0), Y(H))], "#e8f5e9", GRN, 1.4))
    b.append(PG([(X(Lr), Y(0)), (X(Lr + 3), Y(0)), (X(Lr + 3), Y(H)), (X(Lr), Y(H))], SOIL))
    b.append(R(X(-0.25), Y(H), 0.25*U, H*U, CON, CON_S, 1.4))
    b.append(hatch_ground(X(-1.2), X(Lr + 3), Y(0)))
    # Rankine plane from toe at 45+phi/2 to horizontal
    ang = d(r['plane']); xt = H/math.tan(ang)
    b.append(L(X(0), Y(0), X(xt), Y(H), RED, 2.2, "7,4"))
    b.append(T(X(xt) + 6, Y(H) - 8, f"潛在破壞面 45° + φ′/2 = {r['plane']:.0f}°", 11.5, RED, "start", 700))
    sv = 0.75; nlay = 8
    for i in range(nlay):
        z = H - sv/2 - i*sv     # height above base
        b.append(L(X(0), Y(z), X(Lr), Y(z), "#1b5e20", 2))
        xa = z/math.tan(ang)
        if i in (1, 5):
            b.append(L(X(xa), Y(z) - 5, X(xa), Y(z) + 5, RED, 2))
    z = H - sv/2 - 5*sv; xa = z/math.tan(ang)
    b.append(hdim(Y(z) + 14, X(xa), X(Lr), GRN, 4)); b.append(T(X((xa + Lr)/2), Y(z) + 30, f"L_{{e}} = {Lr - xa:.2f} m（抗拔區）", 11, GRN))
    b.append(hdim(Y(z) + 14, X(0), X(xa), RED, 4)); b.append(T(X(xa/2), Y(z) + 30, "主動區", 11, RED))
    z1 = H - sv/2 - 1*sv; xa1 = z1/math.tan(ang)
    b.append(T(X(xa1 + 0.15), Y(z1) - 6, f"L_{{e}} = {Lr - xa1:.2f}", 11, GRN, "start"))
    # external arrows
    b.append(arr(X(Lr + 2.6), Y(H/3), X(Lr) + 4, Y(H/3), BLU, "f7c", 2.6))
    b.append(T(X(Lr + 1.8), Y(H/3) - 10, "外推力", 11.5, BLU))
    # mode list
    ox = 560
    b.append(R(ox - 10, 52, 250, 300, "#fff", "#dfe6ea", 1))
    items = [("內穩定（看每一層筋）", RED, 700), ("① 拉斷：T_{max} > 筋的長期強度", INK, None), ("② 拔出：抗拔區 L_{e} 太短", INK, None),
             ("③ 面板連接破壞", INK, None), ("④ 面板局部鼓出（S_{v} 太大）", INK, None), ("⑤ 沿某一層筋水平滑動", INK, None), ("", INK, None),
             ("外穩定（整塊當重力牆）", BLU, 700), ("滑動、傾倒、承載", INK, None), ("＋整體圓弧滑動（U3-3）", INK, None), ("", INK, None),
             ("拔出 FS = 2L_{e}tanφ / (K_{a}S_{v})", GRN, 700), ("σ′_{v} 約掉 → L_{e} 最短的上層最危險", GRN, None)]
    for i, (s, c, w) in enumerate(items):
        b.append(T(ox, 76 + i*21, s, 12, c, "start", w))
    return svg(820, 380, b)

# ======================================================= f8: decision flowchart
def box(x, y, w, h, lines, fill="#e3f2fd", stroke=BLU, size=12.5):
    s = [R(x - w/2, y - h/2, w, h, fill, stroke, 1.4, ' rx="8"')]
    n = len(lines)
    for i, t in enumerate(lines):
        s.append(T(x, y - (n-1)*8 + i*16 + 4, t, size))
    return "".join(s)
def dia(x, y, w, h, lines):
    s = [PG([(x, y - h/2), (x + w/2, y), (x, y + h/2), (x - w/2, y)], "#fff3e0", ORG, 1.4)]
    n = len(lines)
    for i, t in enumerate(lines):
        s.append(T(x, y - (n-1)*8 + i*16 + 4, t, 12))
    return "".join(s)
def f8():
    b = [arrow_defs((("f8k", "#455a64"),))]
    k = lambda x1, y1, x2, y2: arr(x1, y1, x2, y2, "#455a64", "f8k", 1.6)
    ln = lambda pts: PL(pts, "#455a64", 1.6)
    cx = 320
    b.append(box(cx, 40, 380, 44, ["① 讀圖：H 量到哪、B 含不含趾、地表傾角、牆前有無覆土"]))
    b.append(k(cx, 62, cx, 86))
    b.append(dia(cx, 124, 220, 72, ["牆型？"]))
    b.append(k(cx - 110, 124, 140, 124)); b.append(T(175, 116, "加勁", 11.5, MUT))
    b.append(box(76, 124, 124, 56, ["說明題：", "外 4 項＋內 5 種"], "#e8f5e9", GRN))
    b.append(k(cx + 110, 124, 520, 124)); b.append(T(475, 116, "懸臂式", 11.5, MUT))
    b.append(box(610, 124, 176, 56, ["虛擬牆背過踵端", "踵上土併入牆體"]))
    b.append(k(cx, 160, cx, 190)); b.append(T(cx + 8, 180, "重力式", 11.5, MUT, "start"))
    b.append(ln([(610, 152), (610, 210)])); b.append(k(610, 210, cx + 190, 210))
    b.append(box(cx, 210, 380, 40, ["② 推力：K_{a}（Rankine／Coulomb）→ 有水？水壓另算 K = 1"]))
    b.append(k(cx, 230, cx, 256))
    b.append(box(cx, 276, 380, 40, ["③ 自由體圖：分塊 W、P_{av} 放 M_{R}、對牆趾取矩"]))
    b.append(k(cx, 296, cx, 320))
    b.append(dia(cx, 356, 220, 68, ["底面土？"]))
    b.append(k(cx - 110, 356, 145, 356)); b.append(T(178, 346, "φ = 0 黏土", 11, MUT))
    b.append(box(88, 356, 112, 50, ["抗滑 = c_{a}B", "ΣV 不幫忙"], "#fce4ec", RED))
    b.append(k(cx + 110, 356, 488, 356)); b.append(T(458, 346, "砂／c-φ", 11, MUT))
    b.append(box(565, 356, 150, 50, ["ΣV tanδ + c_{a}B", "δ、c_{a} 寫明假設"], "#fce4ec", RED))
    b.append(k(cx, 390, cx, 420))
    b.append(ln([(88, 381), (88, 440)])); b.append(k(88, 440, cx - 190, 440))
    b.append(ln([(565, 381), (565, 440)])); b.append(k(565, 440, cx + 190, 440))
    b.append(box(cx, 440, 380, 40, ["④ x̄ → e ≤ B/6？→ 底壓／B′ = B − 2e"]))
    b.append(k(cx, 460, cx, 484))
    b.append(box(cx, 504, 380, 40, ["⑤ 承載：B′ 上算 q_{u}，乘傾斜因數（θ = tan⁻¹ΣH/ΣV）"]))
    b.append(k(cx, 524, cx, 550))
    b.append(dia(cx, 584, 220, 64, ["FS 都過門檻？"]))
    b.append(k(cx + 110, 584, 478, 584)); b.append(T(cx + 128, 576, "否", 11.5, RED, "start", 700))
    b.append(box(565, 584, 170, 56, ["對症補救（§8 表）", "降推力 → 增抵抗"], "#fce4ec", RED))
    b.append(ln([(650, 584), (690, 584), (690, 276)])); b.append(k(690, 276, cx + 190, 276))
    b.append(T(696, 430, "改了重算", 11, RED, "start"))
    b.append(k(cx, 616, cx, 640)); b.append(T(cx + 8, 632, "是", 11.5, GRN, "start", 700))
    b.append(ln([(22, 152), (22, 660)])); b.append(k(22, 660, cx - 190, 660))
    b.append(box(cx, 660, 380, 40, ["收尾：列出 FS 與門檻、寫明假設（δ、c_{a}、P_{p}、q_{s}）"], "#ede7f6", PUR))
    return svg(760, 690, b)

FIG.update(f0=f0(), f1=f1(), f2=f2(), f3=f3(), f4=f4(), f5=f5(), f6=f6(), f7=f7(), f8=f8())

def inject(path):
    s = open(path, encoding='utf-8').read()
    for k, v in FIG.items():
        tag = f'<!--FIG:{k}-->'
        c = s.count(tag)
        if c != 1:
            raise SystemExit(f'marker {tag} count = {c}')
        s = re.sub(re.escape(tag) + r'\s*<svg\b.*?</svg>', lambda m: tag + '\n' + v, s, flags=re.S)
    open(path, 'w', encoding='utf-8').write(s)
    print('injected', len(FIG))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        inject(sys.argv[1])
    else:
        os.makedirs('/tmp/u32figs', exist_ok=True)
        for k, v in FIG.items():
            open(f'/tmp/u32figs/{k}.svg', 'w').write(v)
        print('ok')
