"""lecture-SM-U3-3 figures. All geometry/numbers from calcs.py (題解對帳).
Usage: python3 gen_figs.py <lecture.html>"""
import sys, os, re, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'U1-1'))
from svglib import *
from calcs import N, fs14
d = math.radians
FIG = {}
BRN, BLU, RED, GRN, ORG, PUR = "#6d4c41", "#1565c0", "#c62828", "#2e7d32", "#ef6c00", "#6a1b9a"
SOIL = "#efe3d3"; WATC = "#b3e5fc"
def arr(x1, y1, x2, y2, c, mk, sw=2.2, dash=None):
    return L(x1, y1, x2, y2, c, sw, dash, f' marker-end="url(#{mk})"')
def axes(b, px0, py0, px1, py1, xt, yt, X, Y, xl, yl, xfmt="{}", yfmt="{}"):
    for v in xt:
        b.append(L(X(v), py0, X(v), py0 + 4, "#455a64", 1)); b.append(T(X(v), py0 + 18, xfmt.format(v), 11, MUT))
    for v in yt:
        b.append(L(px0 - 4, Y(v), px0, Y(v), "#455a64", 1)); b.append(T(px0 - 8, Y(v) + 4, yfmt.format(v), 11, MUT, "end"))
        b.append(L(px0, Y(v), px1, Y(v), "#eceff1", 1))
    b.append(L(px0, py0, px1, py0, "#455a64", 1.6)); b.append(L(px0, py0, px0, py1, "#455a64", 1.6))
    b.append(T((px0 + px1)/2, py0 + 38, xl, 12, MUT)); b.append(T(px0 - 4, py1 - 12, yl, 12, MUT, "start"))

# ===================================== g0: three slip-surface geometries
def g0():
    b = [arrow_defs((("g0a", RED), ("g0b", BLU)))]
    titles = ["① 無限邊坡（淺層、平行坡面）", "② 平面楔體（有限、一條直線）", "③ 圓弧切片（深層、繞圓心轉）"]
    subs = ["取一個切片：τ_{f} / τ_{d}", "整塊楔體：ΣR / ΣT", "力矩：ΣM_{R} / ΣM_{D}"]
    for k in range(3):
        ox = 20 + k*260
        b.append(T(ox + 120, 30, titles[k], 13.5, "#0d47a1", weight=700))
        b.append(T(ox + 120, 300, subs[k], 12.5, INK))
    # 1 infinite slope beta 25
    ox, oy = 20, 250; be = d(25)
    P = lambda s, n: (ox + 10 + s*math.cos(be) + n*math.sin(be), oy - s*math.sin(be) + n*math.cos(be))
    b.append(PG([P(0, 0), P(230, 0), P(230, 40), P(0, 40)], SOIL, BRN, 1))
    b.append(L(*P(0, 0), *P(230, 0), BRN, 2))
    b.append(L(*P(0, 30), *P(230, 30), RED, 2, "7,4"))
    b.append(PG([P(100, 0), P(130, 0), P(130, 30), P(100, 30)], "#ffe0b2", ORG, 1.4))
    x1, y1 = P(115, 30); x2, y2 = P(85, 30)
    b.append(arr(x1, y1, x2, y2, RED, "g0a", 2))
    b.append(T(P(60, 64)[0], P(60, 64)[1], "滑動面深 z ≪ 坡長", 11, RED))
    # 2 planar wedge (2023-2 geometry H=8, 60/45) scale
    U = 22; ox2, oy2 = 300, 250
    X = lambda x: ox2 + x*U; Y = lambda y: oy2 - y*U
    xc = 8/math.tan(d(60)); xb = 8/math.tan(d(45))
    b.append(PG([(X(-1), Y(0)), (X(0), Y(0)), (X(xc), Y(8)), (X(xb + 1.5), Y(8)), (X(xb + 1.5), Y(-1)), (X(-1), Y(-1))], SOIL))
    b.append(PG([(X(0), Y(0)), (X(xc), Y(8)), (X(xb), Y(8))], "#ffe0b2", ORG, 1.4))
    b.append(L(X(0), Y(0), X(xb), Y(8), RED, 2.2, "7,4"))
    b.append(arr(X(xb*0.62), Y(8*0.62) + 4, X(xb*0.38), Y(8*0.38) + 4, RED, "g0a", 2))
    b.append(T(X(xb) + 4, Y(4), "破壞面 45°", 11, RED, "start"))
    b.append(T(X(xc) - 6, Y(8) - 6, "坡面 60°", 11, BRN, "end"))
    # 3 circle with slices
    ox3, oy3 = 540, 250; R_ = 150; cx, cy = ox3 + 70, oy3 - 190
    # slope: toe at (ox3+10, oy3) to crest
    toe = (ox3 + 30, oy3); crest = (ox3 + 130, oy3 - 100)
    b.append(PG([(ox3, oy3), toe, crest, (ox3 + 240, oy3 - 100), (ox3 + 240, oy3 + 20), (ox3, oy3 + 20)], SOIL))
    # circle through toe: radius from center to toe
    R_ = math.hypot(toe[0] - cx, toe[1] - cy)
    # find intersection with crest line y = oy3-100 on right
    yy = oy3 - 100; xx = cx + math.sqrt(R_**2 - (yy - cy)**2)
    a0 = math.atan2(toe[1] - cy, toe[0] - cx); a1 = math.atan2(yy - cy, xx - cx)
    pts = [(cx + R_*math.cos(a0 + (a1 - a0)*i/60), cy + R_*math.sin(a0 + (a1 - a0)*i/60)) for i in range(61)]
    surf = lambda x: oy3 if x < toe[0] else (oy3 - (x - toe[0]) if x < crest[0] else oy3 - 100)
    b.append(PG(pts + [(xx, yy), crest, toe], "#ffe0b2", ORG, 1))
    b.append(PL(pts, RED, 2.2, "7,4"))
    xs = [toe[0] + (xx - toe[0])*j/5 for j in range(1, 5)]
    for xv in xs:
        ybot = cy + math.sqrt(R_**2 - (xv - cx)**2)
        b.append(L(xv, surf(xv), xv, ybot, ORG, 1.2))
    b.append(C(cx, cy, 4, RED)); b.append(T(cx + 6, cy - 4, "O", 12, RED, "start", 700))
    b.append(L(cx, cy, *pts[30], RED, 1, "3,3"))
    b.append(T(400, 330, "三種幾何的差別只在「滑動面長什麼樣」；FS 的定義相同：沿滑動面可發揮的抗剪強度 ÷ 維持平衡所需的剪力", 11.5, MUT))
    return svg(800, 342, b)

# ===================================== g1: infinite slope c=0, FS vs beta
def g1():
    phi = 35; gs, gw = 20.0, 9.81
    px0, py0, px1, py1 = 80, 300, 540, 50
    X = lambda v: px0 + (v - 15)/(50 - 15)*(px1 - px0); Y = lambda f: py0 - f/2.6*(py0 - py1)
    b = [T(400, 26, "c = 0 無限邊坡（φ = 35°）：浸水不改變 FS，滲流才會", 14, "#0d47a1", weight=700)]
    axes(b, px0, py0, px1, py1, range(15, 51, 5), [0, 0.5, 1.0, 1.5, 2.0, 2.5], X, Y, "坡角 β（°）", "FS", "{}°", "{:.1f}")
    bs = [15 + i*35/140 for i in range(141)]
    f1 = [(X(v), Y(math.tan(d(phi))/math.tan(d(v)))) for v in bs if math.tan(d(phi))/math.tan(d(v)) <= 2.6]
    f2 = [(X(v), Y((gs - gw)/gs*math.tan(d(phi))/math.tan(d(v)))) for v in bs if (gs-gw)/gs*math.tan(d(phi))/math.tan(d(v)) <= 2.6]
    b.append(PL(f1, BRN, 3)); b.append(PL(f2, BLU, 2.6, "7,4"))
    b.append(L(px0, Y(1), px1, Y(1), RED, 1.3, "4,3"))
    b.append(L(X(phi), py0, X(phi), py1 + 10, "#90a4ae", 1, "3,3")); b.append(T(X(phi) + 4, py1 + 20, "β = φ：FS = 1（休止角）", 11, "#455a64", "start"))
    f24 = N['24']['FS']
    b.append(C(X(42), Y(f24), 5, RED, "#fff", 1.5)); b.append(T(X(42) - 6, Y(f24) + 24, f"SM-2024-2：β = 42° → {f24:.2f}", 12, RED, "end", 700))
    b.append(T(X(20), Y(math.tan(d(phi))/math.tan(d(20))) - 10, "乾坡＝完全浸水：tanφ / tanβ", 12, BRN, "start", 700))
    b.append(T(X(29), Y(0.24), "滲流至地表：(γ′/γ_{sat})·tanφ/tanβ", 12, BLU, "start", 700))
    b.append(T(X(29), Y(0.06), "（示意取 γ_{sat} = 20 → γ′/γ_{sat} ≈ 0.51）", 11, BLU, "start"))
    b.append(R(570, 70, 210, 210, "#fff3e0", "#ffcc80", 1))
    for i, (s, c, w) in enumerate([("為什麼浸水不變？", "#e65100", 700), ("浮力同時減少", INK, None), ("正向力（抗力）與", INK, None), ("下滑力，比例相同 → 約掉", INK, None), ("", INK, None),
                                   ("為什麼滲流會變？", "#e65100", 700), ("滲流力順坡向下，", INK, None), ("只加在驅動側：", INK, None), ("驅動用 γ_{sat}、抗力用 γ′", INK, None)]):
        b.append(T(584, 94 + i*21, s, 12.5, c, "start", w))
    return svg(800, 352, b)

# ===================================== g2: SM-2014-1 seepage geometry + FS vs water depth
def g2():
    b = [arrow_defs((("g2a", BLU), ("g2k", "#455a64")))]
    b.append(T(200, 26, "平行坡面滲流：等勢線垂直坡面", 14, "#0d47a1", weight=700))
    be = d(15); U = 34
    ox, oy = 90, 300
    P = lambda s, n: (ox + s*U*math.cos(be) - n*U*math.sin(be), oy - s*U*math.sin(be) - n*U*math.cos(be))  # s along slope, n along upward normal (perpendicular)
    Hn = 6*math.cos(be); hwn = 4.5*math.cos(be)  # normal thickness of whole layer / water part
    b.append(PG([P(0, 0), P(10, 0), P(10, Hn), P(0, Hn)], SOIL))
    b.append(PG([P(0, 0), P(10, 0), P(10, hwn), P(0, hwn)], WATC, "none", 1, ' opacity="0.6"'))
    b.append(L(*P(0, Hn), *P(10, Hn), BRN, 2)); b.append(L(*P(0, hwn), *P(10, hwn), BLU, 1.8))
    b.append(L(*P(0, 0), *P(10, 0), RED, 2.4, "7,4"))
    b.append(T(P(1.2, 0)[0], P(1.2, 0)[1] + 20, "滑動面（岩層介面）", 11, RED, "start"))
    for k in (0.3, 0.6):
        x1, y1 = P(10, hwn*k); x2, y2 = P(8.3, hwn*k)
        b.append(arr(x1, y1, x2, y2, BLU, "g2a", 1.6))
    b.append(T(*P(9.0, hwn*0.12), "流線 ∥ 坡面", 11, BLU))
    # point A on slip surface at s=4; equipotential normal to slope up to water table
    sA = 4.0; A = P(sA, 0); Bq = P(sA, hwn)
    b.append(L(*A, *Bq, PUR, 2)); b.append(C(*A, 4, PUR)); b.append(T(A[0] + 6, A[1] + 14, "A", 12, PUR, "start", 700))
    # horizontal from B to vertical above A: vertical drop = hw cos^2
    hp = 4.5*math.cos(be)**2
    b.append(L(Bq[0], Bq[1], A[0], Bq[1], "#9e9e9e", 1, "3,3"))
    b.append(L(A[0], A[1], A[0], A[1] - hp*U, PUR, 1.4, "3,3"))
    b.append(L(A[0], A[1] - hp*U, A[0], P(sA, 0)[1] - 4.5*U, "#9e9e9e", 1, "3,3"))
    b.append(T(A[0] + 8, A[1] - hp*U/2, "h_{p} = h_{w}cos²β", 11.5, PUR, "start", 700))
    b.append(T(A[0] + 8, A[1] - hp*U/2 + 16, f"= {hp:.2f} m", 11.5, PUR, "start", 700))
    b.append(T(A[0] + 8, P(sA, 0)[1] - 4.5*U - 24, "h_{w} = 4.5 m（鉛直到水面）", 11, "#757575", "start"))
    b.append(T(Bq[0] - 6, Bq[1] + 40, "等勢線 ⊥ 坡面", 11, PUR, "end"))
    b.append(T(Bq[0] - 4, Bq[1] - 6, "B", 12, PUR, "end", 700))
    b.append(T(200, 338, f"u = γ_{{w}}h_{{w}}cos²β = 9.81×4.5×cos²15° = {N['14']['u']:.2f} kPa（不是 {N['14']['u_wrong']:.2f}）", 11.5, INK))
    b.append(T(200, 356, "沿等勢線總水頭相同；B 點在水面上 u = 0，所以 A 的壓力水頭 = B、A 的高程差", 11, MUT))
    # right: FS vs water depth
    px0, py0, px1, py1 = 470, 300, 770, 60
    X = lambda v: px0 + v/6*(px1 - px0); Y = lambda f: py0 - (f - 1.0)/1.1*(py0 - py1)
    b.append(T(620, 26, "SM-2014-1：水位越淺，FS 越低", 14, "#0d47a1", weight=700))
    axes(b, px0, py0, px1, py1, range(0, 7), [1.0, 1.2, 1.4, 1.6, 1.8, 2.0], X, Y, "地下水位深度 d_{w}（地表下 m）", "FS", "{}", "{:.1f}")
    ds = [i*6/120 for i in range(121)]
    b.append(PL([(X(v), Y(fs14(v)[0])) for v in ds], GRN, 2.8))
    r = N['14']
    b.append(C(X(1.5), Y(r['FS']), 5, RED, "#fff", 1.5)); b.append(T(X(2.2), Y(1.25), f"題目 d_{{w}} = 1.5：{r['FS']:.2f}", 12, RED, "start", 700))
    b.append(C(X(1.5), Y(r['FS_uwrong']), 4, "#9e9e9e", "#fff", 1.5)); b.append(T(X(2.2), Y(1.18), f"誤用 u = γ_{{w}}h_{{w}}：{r['FS_uwrong']:.2f}", 11, "#757575", "start"))
    b.append(T(X(6) - 2, Y(r['FS_dry']) + 18, f"無水 {r['FS_dry']:.2f}", 11.5, GRN, "end", 700))
    b.append(T(X(0) + 4, Y(1.08), f"水到地表 {r['FS_full']:.2f}", 11.5, GRN, "start", 700))
    return svg(800, 370, b)

# ===================================== g3: SM-2023-2 cohesion
def g3():
    r = N['23']
    b = [T(400, 26, "SM-2023-2：淺層楔體的抗力大半來自 c —— 雨水入滲把 c 砍掉，FS 從 3.68 掉到 1.02", 14, "#0d47a1", weight=700)]
    # left bars
    px0, py0 = 80, 300; sc = 0.32
    for k, (c, lab) in enumerate([(50, "㈠ c = 50"), (5, "㈡ c = 5")]):
        x = px0 + k*120
        cL = c*r['L']; nt = r['Ntan']
        b.append(R(x, py0 - nt*sc, 60, nt*sc, "#a1887f", BRN, 1))
        b.append(R(x, py0 - (nt + cL)*sc, 60, cL*sc, "#90caf9", BLU, 1))
        b.append(T(x + 30, py0 - (nt + cL)*sc - 8, f"FS = {(cL+nt)/r['Td']:.2f}", 12, RED, "middle", 700))
        b.append(T(x + 30, py0 + 18, lab, 12, INK))
        if cL*sc > 18: b.append(T(x + 30, py0 - nt*sc - cL*sc/2 + 4, f"cL {cL:.0f}", 11, BLU))
        b.append(T(x + 30, py0 - nt*sc/2 + 4, f"{nt:.0f}", 11, "#fff"))
    b.append(L(px0 - 10, py0 - r['Td']*sc, px0 + 190, py0 - r['Td']*sc, RED, 1.6, "5,4"))
    b.append(T(px0 + 192, py0 - r['Td']*sc + 4, f"驅動 W sin45° = {r['Td']:.1f}", 11.5, RED, "start"))
    b.append(L(px0 - 10, py0, px0 + 190, py0, "#455a64", 1.4))
    b.append(T(px0 + 90, py0 + 40, "抗力組成（kN/m）：藍 cL、褐 N tanφ", 11.5, MUT))
    # right: FS vs c
    qx0, qy0, qx1, qy1 = 480, 300, 760, 70
    X = lambda v: qx0 + v/50*(qx1 - qx0); Y = lambda f: qy0 - f/4*(qy0 - qy1)
    axes(b, qx0, qy0, qx1, qy1, range(0, 51, 10), [0, 1, 2, 3, 4], X, Y, "破壞面凝聚力 c（kPa）", "FS", "{}", "{}")
    b.append(PL([(X(v), Y((v*r['L'] + r['Ntan'])/r['Td'])) for v in [0, 50]], BLU, 2.8))
    b.append(L(qx0, Y(1), qx1, Y(1), RED, 1.2, "4,3"))
    for v, f in [(50, r['FS1']), (5, r['FS2']), (0, r['FS0'])]:
        b.append(C(X(v), Y(f), 4.5, RED, "#fff", 1.5))
    b.append(T(X(50) - 10, Y(r['FS1']) - 6, f"{r['FS1']:.2f}", 12, RED, "end", 700))
    b.append(T(X(5) + 8, Y(r['FS2']) + 18, f"c = 5：{r['FS2']:.2f}", 12, RED, "start", 700))
    b.append(T(X(0) + 8, Y(r['FS0']) + 18, f"c = 0：{r['FS0']:.2f}", 11, RED, "start"))
    b.append(T(X(20), Y(0.4), f"FS = 1 只需 c = {r['c_for_1']:.2f} kPa", 11.5, MUT, "start"))
    return svg(800, 350, b)

# ===================================== g4: SM-2008-4 wedge + seismic + anchor
def g4():
    r = N['08']; U = 20
    b = [arrow_defs((("g4a", RED), ("g4b", "#455a64"), ("g4c", GRN), ("g4d", ORG)))]
    ox, oy = 60, 300
    X = lambda x: ox + x*U; Y = lambda y: oy - y*U
    LAB = 7.5/math.sin(d(70))
    A = (0, 0); Bp = (LAB*math.cos(d(70)), 7.5); Cp = (r['LAC']*math.cos(d(40)), r['LAC']*math.sin(d(40)))
    b.append(T(200, 26, "SM-2008-4：塊體 ABC（依標註角度按比例）", 14, "#0d47a1", weight=700))
    b.append(PG([(X(-1.5), Y(0)), (X(0), Y(0)), (X(Bp[0]), Y(Bp[1])), (X(Cp[0]), Y(Cp[1])), (X(Cp[0] + 3), Y(Cp[1] + 3*math.tan(d(5)))), (X(Cp[0] + 3), Y(-1.5)), (X(-1.5), Y(-1.5))], "#e0e0e0"))
    b.append(PG([(X(0), Y(0)), (X(Bp[0]), Y(Bp[1])), (X(Cp[0]), Y(Cp[1]))], "#ffe0b2", ORG, 1.4))
    b.append(L(X(0), Y(0), X(Cp[0] + 2), Y((Cp[0] + 2)*math.tan(d(40))), RED, 2.4, "7,4"))
    for p, n, dx, dy in [(A, "A", -12, 14), (Bp, "B", -14, -6), (Cp, "C", 6, -8)]:
        b.append(T(X(p[0]) + dx, Y(p[1]) + dy, n, 13, INK, "middle", 700))
    g = ((A[0] + Bp[0] + Cp[0])/3, (A[1] + Bp[1] + Cp[1])/3)
    gx, gy = X(g[0]), Y(g[1])
    b.append(arr(gx, gy, gx, gy + 70, "#455a64", "g4b", 2.4)); b.append(T(gx + 6, gy + 64, f"W = {r['W']:.1f}", 11.5, INK, "start"))
    b.append(arr(gx, gy, gx - 52, gy, RED, "g4a", 2.4)); b.append(T(gx - 56, gy - 8, f"k_{{h}}W = {0.2*r['W']:.1f}", 11.5, RED, "end"))
    # anchor normal to AC, pushing into slope (compression on surface)
    mx, my = Cp[0]*0.55, Cp[1]*0.55
    nx, ny = -math.sin(d(40)), math.cos(d(40))
    b.append(arr(X(mx + nx*2.2), Y(my + ny*2.2), X(mx + nx*0.2), Y(my + ny*0.2), GRN, "g4c", 2.6))
    b.append(T(X(mx + nx*2.2) + 4, Y(my + ny*2.2) - 6, "地錨 ⊥ AC", 11.5, GRN, "start", 700))
    b.append(T(X(Cp[0]*0.75) + 10, Y(Cp[1]*0.75) + 22, "AC 40°（泥岩夾層）", 11, RED, "start"))
    b.append(T(200, 350, f"FS = (cL + N tanφ)/T_{{d}} = {r['FS']:.2f}；無地震 {r['FS_static']:.2f}", 11.5, INK))
    # right curves
    px0, py0, px1, py1 = 470, 300, 760, 70
    Xk = lambda v: px0 + v/0.3*(px1 - px0); Yf = lambda f: py0 - (f - 0.4)/0.8*(py0 - py1)
    b.append(T(615, 26, "k_{h} 兩邊夾擊：驅動↑、正向力↓", 14, "#0d47a1", weight=700))
    from calcs import fs08
    axes(b, px0, py0, px1, py1, [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3], [0.4, 0.6, 0.8, 1.0, 1.2], Xk, Yf, "水平地震係數 k_{h}", "FS", "{:.2f}", "{:.1f}")
    ks = [i*0.3/120 for i in range(121)]
    b.append(PL([(Xk(k), Yf(fs08(k)[0])) for k in ks], RED, 2.8))
    b.append(PL([(Xk(k), Yf((10*r['LAC'] + (r['W']*math.cos(d(40)))*math.tan(d(28)))/(r['W']*math.sin(d(40)) + k*r['W']*math.cos(d(40))))) for k in ks], ORG, 1.8, "6,4"))
    b.append(L(px0, Yf(1.2), px1, Yf(1.2), GRN, 1.3, "4,3")); b.append(T(px1, Yf(1.2) - 6, "要求 1.2", 11, GRN, "end"))
    b.append(C(Xk(0.2), Yf(r['FS']), 5, RED, "#fff", 1.5)); b.append(T(Xk(0.2) + 8, Yf(r['FS']) + 18, f"{r['FS']:.2f}", 12, RED, "start", 700))
    b.append(T(Xk(0.02), Yf(0.55), "實線：正確（兩個分量都算）", 11, RED, "start"))
    b.append(T(Xk(0.02), Yf(0.48), "虛線：只加在驅動側（高估）", 11, ORG, "start"))
    b.append(T(615, 366, f"地錨 ⊥ AC：每公尺 {r['P']:.1f} kN → 間距 2 m 每支 {r['T']:.0f} kN", 11.5, GRN))
    return svg(800, 378, b)

# ===================================== g5: SM-2006-3 three-block bars
def g5():
    b = [arrow_defs((("g5a", RED), ("g5b", BLU)))]
    b.append(T(400, 26, "SM-2006-3 三塊法：中間塊沿軟弱夾層被主動側推、被被動側與夾層 s_{u}L 擋", 14, "#0d47a1", weight=700))
    # schematic geometry (to scale: 1:2 slope, H=10, clay at 12 m below original ground, 2 m below excavation)
    U = 11; ox, oy = 40, 220
    X = lambda x: ox + x*U; Y = lambda y: oy - y*U    # y=0 at clay layer
    b.append(PG([(X(0), Y(2)), (X(8), Y(2)), (X(28), Y(12)), (X(36), Y(12)), (X(36), Y(-3)), (X(0), Y(-3))], SOIL, BRN, 1))
    b.append(R(X(0), Y(0) - 2, 36*U, 4, "#8d6e63"))
    b.append(L(X(8), Y(2), X(8), Y(0), BLU, 2, "5,3")); b.append(L(X(28), Y(12), X(28), Y(0), RED, 2, "5,3"))
    b.append(arr(X(31.5), Y(4), X(28.3), Y(4), RED, "g5a", 2.4)); b.append(T(X(32), Y(4) + 4, "P_{A}", 12, RED, "start", 700))
    b.append(arr(X(4.5), Y(0.8), X(7.7), Y(0.8), BLU, "g5b", 2.4)); b.append(T(X(4.3), Y(0.8) + 4, "P_{P}", 12, BLU, "end", 700))
    b.append(arr(X(14), Y(0) + 10, X(22), Y(0) + 10, GRN, "g5b", 2) if False else "")
    b.append(T(X(18), Y(0) + 18, "夾層 s_{u} = 12 kPa × L = 20 m → T = 240", 11, BRN))
    b.append(T(X(28) + 4, Y(12) - 6, "H_{1} = 12", 11, RED, "start")); b.append(T(X(8) - 4, Y(2) - 6, "H_{2} = 2", 11, BLU, "end"))
    # bars
    bx0, by0 = 470, 210; sc = 0.15
    for k, (key, lab) in enumerate([('n', "常時（水在夾層）"), ('r', "豪雨（水沿地表）")]):
        r = N['06'][key]; y = 70 + k*80
        b.append(T(bx0, y - 8, lab + f"　FS = {r['FS']:.2f}", 12.5, RED if r['FS'] < 1 else GRN, "start", 700))
        # driving
        b.append(R(bx0, y, r['PA']*sc, 18, "#ef9a9a", RED, 1))
        if r['PwA']: b.append(R(bx0 + r['PA']*sc, y, r['PwA']*sc, 18, WATC, BLU, 1))
        b.append(T(bx0 + (r['PA'] + r['PwA'])*sc + 4, y + 14, f"驅動 {r['PA'] + r['PwA']:.0f}", 11, INK, "start"))
        # resisting
        b.append(R(bx0, y + 22, r['T']*sc, 18, "#bcaaa4", BRN, 1))
        b.append(R(bx0 + r['T']*sc, y + 22, r['PP']*sc, 18, "#90caf9", BLU, 1))
        if r['PwP']: b.append(R(bx0 + (r['T'] + r['PP'])*sc, y + 22, r['PwP']*sc, 18, WATC, BLU, 1))
        b.append(T(bx0 + (r['T'] + r['PP'] + r['PwP'])*sc + 4, y + 36, f"抵抗 {r['T'] + r['PP'] + r['PwP']:.0f}", 11, INK, "start"))
    rr = N['06']['r']
    b.append(T(bx0, 252, f"豪雨時主動側靜水壓 {rr['PwA']:.0f} 佔驅動 {rr['PwA']/(rr['PwA']+rr['PA']):.0%}", 11.5, BLU, "start", 700))
    b.append(T(bx0, 270, "紅：有效土壓　淺藍：水壓　褐：夾層 s_{u}L　藍：被動土壓", 11, MUT, "start"))
    return svg(800, 290, b)

# ===================================== g6: SM-2021-4 per-slice
def g6():
    r = N['21']; rows = r['rows']
    b = [T(400, 26, "SM-2021-4 普通切片法：每一片的驅動 vs 抵抗（題解量測切片表）", 14, "#0d47a1", weight=700)]
    px0, py0 = 80, 290; sc = 0.38; w = 34
    b.append(L(px0 - 10, py0, px0 + 5*110, py0, "#455a64", 1.4))
    for i, rw in enumerate(rows):
        x = px0 + i*110
        b.append(R(x, py0 - rw['drv']*sc, w, rw['drv']*sc, "#ef9a9a", RED, 1))
        b.append(R(x + w + 4, py0 - rw['res']*sc, w, rw['res']*sc, "#a5d6a7", GRN, 1))
        b.append(T(x + w/2, py0 - rw['drv']*sc - 6, f"{rw['drv']:.0f}", 11, RED))
        b.append(T(x + w*1.5 + 4, py0 - rw['res']*sc - 6, f"{rw['res']:.0f}", 11, GRN))
        b.append(T(x + w + 2, py0 + 18, f"切片 {i+1}", 11.5, INK))
        b.append(T(x + w + 2, py0 + 34, f"α = {rw['a']}°", 11, MUT))
    b.append(R(px0, 54, 14, 12, "#ef9a9a", RED, 1)); b.append(T(px0 + 20, 64, "驅動 W sinα", 11.5, INK, "start"))
    b.append(R(px0 + 130, 54, 14, 12, "#a5d6a7", GRN, 1)); b.append(T(px0 + 150, 64, "抵抗 c′ΔL + (W cosα − uΔL)tanφ′", 11.5, INK, "start"))
    b.append(R(620, 80, 170, 190, "#fff", "#dfe6ea", 1))
    for i, (s, c, wt) in enumerate([("Σ驅動", INK, None), (f"{r['sum_drv']:.1f}", RED, 700), ("Σ抵抗", INK, None), (f"{r['sum_res']:.1f}", GRN, 700),
                                    ("Fellenius", INK, None), (f"FS = {r['FS']:.3f}", RED, 700), ("Bishop 簡化（同表試算）", MUT, None), (f"FS ≈ {r['FS_bishop']:.2f}", PUR, 700)]):
        b.append(T(705, 102 + i*21, s, 12.5, c, "middle", wt))
    b.append(T(400, 344, "切片 1（α = 60°）驅動最大、抵抗最小；切片 5（α = 0°）只出抵抗。α 越大的切片越「推」，越平的切片越「擋」", 11.5, MUT))
    return svg(800, 356, b)

# ===================================== g7 flowchart
def box(x, y, w, h, lines, fill="#e3f2fd", stroke=BLU):
    s = [R(x - w/2, y - h/2, w, h, fill, stroke, 1.4, ' rx="8"')]
    for i, t_ in enumerate(lines):
        s.append(T(x, y - (len(lines)-1)*8 + i*16 + 4, t_, 12.5))
    return "".join(s)
def dia(x, y, w, h, lines):
    s = [PG([(x, y - h/2), (x + w/2, y), (x, y + h/2), (x - w/2, y)], "#fff3e0", ORG, 1.4)]
    for i, t_ in enumerate(lines):
        s.append(T(x, y - (len(lines)-1)*8 + i*16 + 4, t_, 12))
    return "".join(s)
def g7():
    b = [arrow_defs((("g7k", "#455a64"),))]
    k = lambda x1, y1, x2, y2: arr(x1, y1, x2, y2, "#455a64", "g7k", 1.6)
    ln = lambda pts: PL(pts, "#455a64", 1.6)
    cx = 380
    b.append(box(cx, 36, 420, 40, ["① 讀圖：深度是鉛直還是垂直坡面？角度標在哪？比例尺？"]))
    b.append(k(cx, 56, cx, 80))
    b.append(dia(cx, 118, 240, 72, ["滑動面形狀？"]))
    b.append(k(cx - 120, 118, 175, 118)); b.append(T(218, 108, "平行坡面", 11, MUT))
    b.append(box(100, 118, 150, 50, ["無限邊坡", "取一個切片"], "#e8f5e9", GRN))
    b.append(k(cx, 154, cx, 190)); b.append(T(cx + 8, 176, "一條直線", 11, MUT, "start"))
    b.append(k(cx + 120, 118, 585, 118)); b.append(T(542, 108, "圓弧", 11, MUT))
    b.append(box(660, 118, 150, 50, ["切片法", "（題目多會給式）"], "#ede7f6", PUR))
    b.append(box(cx, 212, 300, 48, ["平面楔體：幾何（正弦定理）→ W、L", "軟弱夾層 → 三塊法"], "#fff8e1", ORG))
    # left branch
    b.append(k(100, 143, 100, 186))
    b.append(box(100, 216, 170, 56, ["分清水的狀態：", "乾／浸水／平行滲流"], "#e8f5e9", GRN))
    b.append(box(100, 310, 170, 72, ["乾／浸水：tanφ/tanβ", "平行滲流：", "u = γ_{w}h_{w}cos²β"], "#e8f5e9", GRN))
    b.append(k(100, 244, 100, 274))
    # wedge branch
    b.append(k(cx, 234, cx, 258))
    b.append(box(cx, 280, 300, 44, ["分解：T_{d} = W sinθ (+k_{h}W cosθ)", ] , "#fff8e1", ORG))
    b.append(k(cx, 302, cx, 326))
    b.append(box(cx, 348, 300, 44, ["N = W cosθ (− k_{h}W sinθ) (− U) (+ 地錨)"], "#fff8e1", ORG))
    # slice branch
    b.append(k(660, 143, 660, 186))
    b.append(box(660, 216, 170, 60, ["量 b、h、α（列表）", "W、ΔL、u 每片算"], "#ede7f6", PUR))
    b.append(k(660, 246, 660, 270))
    b.append(box(660, 300, 170, 60, ["Fellenius 直接算", "Bishop 迭代 m_{α}"], "#ede7f6", PUR))
    # merge
    b.append(ln([(100, 346), (100, 430)])); b.append(k(100, 430, cx - 170, 430))
    b.append(k(cx, 370, cx, 410))
    b.append(ln([(660, 330), (660, 430)])); b.append(k(660, 430, cx + 170, 430))
    b.append(box(cx, 430, 340, 40, ["FS = Σ(c′L + N′tanφ′) / Σ驅動"], "#e3f2fd", BLU))
    b.append(k(cx, 450, cx, 476))
    b.append(dia(cx, 510, 240, 64, ["FS ≥ 門檻？"]))
    b.append(k(cx + 120, 510, 560, 510)); b.append(T(cx + 136, 502, "否", 11.5, RED, "start", 700))
    b.append(box(650, 510, 180, 56, ["對策：排水、減重、", "坡趾加載、地錨／樁"], "#fce4ec", RED))
    b.append(k(cx, 542, cx, 566)); b.append(T(cx + 8, 558, "是", 11.5, GRN, "start", 700))
    b.append(box(cx, 586, 420, 40, ["收尾：寫明門檻依據（常時／地震／豪雨）與量測或假設"], "#ede7f6", PUR))
    b.append(ln([(650, 538), (650, 586)])); b.append(k(650, 586, cx + 210, 586))
    return svg(760, 612, b)

FIG.update(g0=g0(), g1=g1(), g2=g2(), g3=g3(), g4=g4(), g5=g5(), g6=g6(), g7=g7())

def inject(path):
    s = open(path, encoding='utf-8').read()
    for k_, v in FIG.items():
        tag = f'<!--FIG:{k_}-->'
        if s.count(tag) != 1: raise SystemExit(f'marker {tag} count = {s.count(tag)}')
        s = re.sub(re.escape(tag) + r'\s*<svg\b.*?</svg>', lambda m: tag + '\n' + v, s, flags=re.S)
    open(path, 'w', encoding='utf-8').write(s); print('injected', len(FIG))

if __name__ == '__main__':
    if len(sys.argv) > 1: inject(sys.argv[1])
    else:
        os.makedirs('/tmp/u33figs', exist_ok=True)
        for k_, v in FIG.items(): open(f'/tmp/u33figs/{k_}.svg', 'w').write(v)
        print('ok')
