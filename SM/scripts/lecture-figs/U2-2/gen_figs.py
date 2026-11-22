"""lecture-SM-U2-2 figures (2026-11-22 改版：h1、h2、h3、h5 由程式依題解數值重繪).
Usage: python3 gen_figs.py <lecture.html>"""
import sys, os, re, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'U1-1'))
from svglib import *
from calcs import N, ALPHA, sv_true, sv_design, fsz
FIG = {}
BRN, BLU, RED, GRN, ORG, PUR = "#6d4c41", "#1565c0", "#c62828", "#2e7d32", "#ef6c00", "#6a1b9a"
def axes(b, px0, py0, px1, py1, xt, yt, X, Y, xl, yl, xfmt="{}", yfmt="{}", down=False):
    for v in xt:
        yy = py1 if down else py0
        b.append(L(X(v), yy, X(v), yy + (-4 if down else 4), "#455a64", 1)); b.append(T(X(v), yy - 8 if down else yy + 18, xfmt.format(v), 11, MUT))
    for v in yt:
        b.append(L(px0 - 4, Y(v), px0, Y(v), "#455a64", 1)); b.append(T(px0 - 8, Y(v) + 4, yfmt.format(v), 11, MUT, "end"))
    b.append(L(px0, py0, px1, py0, "#455a64", 1.6)); b.append(L(px0, py0, px0, py1, "#455a64", 1.6))

# ===== h1: fs profiles (sand 2023-3, clay 2012-3) + alpha table (2024-4)
def h1():
    b = []
    # sand panel: depth axis down
    px0, ptop, pbot, px1 = 70, 70, 330, 290
    Z = lambda z: ptop + z/25*(pbot - ptop); F = lambda f: px0 + f/150*(px1 - px0)
    b.append(T(170, 28, "砂土（SM-2023-3）：隨深度增加，過 L_{c} 封頂", 13.5, ORG, weight=700))
    b.append(L(px0, ptop, px1, ptop, "#455a64", 1.4)); b.append(L(px0, ptop, px0, pbot, "#455a64", 1.4))
    for f in (0, 50, 100, 150):
        b.append(T(F(f), ptop - 8, f"{f}", 10.5, MUT))
    b.append(T(px1, ptop - 22, "f_{s} (kPa)", 11, MUT, "end"))
    for z in (0, 5, 10, 15, 20, 25):
        b.append(T(px0 - 6, Z(z) + 4, f"{z}", 10.5, MUT, "end"))
    b.append(T(px0 - 6, pbot + 18, "深度 m", 11, MUT, "end"))
    zs = [i*25/250 for i in range(251)]
    pts = [(F(fsz(z)), Z(z)) for z in zs]
    b.append(PG([(px0, ptop)] + pts + [(px0, pbot)], "#ffe0b2", "none"))
    b.append(PL(pts, ORG, 2.6))
    b.append(L(px0 - 4, Z(10), px1, Z(10), RED, 1.4, "5,4")); b.append(T(px1, Z(10) + 16, "L_{c} = 20D = 10 m", 11.5, RED, "end", 700))
    for z in (5, 15):
        b.append(L(px0, Z(z), F(140), Z(z), "#bcaaa4", 1, "2,3"))
    fsg = N['23']['fs_seg']
    for (z, f) in [(2.5, fsg[0]), (7.5, fsg[1]), (12.5, fsg[2]), (20, fsg[3])]:
        b.append(T(F(fsz(z)) + 6, Z(z) + 4, f"{f:.1f}", 11, ORG, "start", 700))
    b.append(T(170, 372, "段平均：26.6 → 85.8 → 116.4 → 138.0（φ 換層而跳）", 11, INK))
    # clay panel
    qx0, qx1 = 380, 560
    Z2 = lambda z: ptop + z/16*(pbot - ptop); F2 = lambda f: qx0 + f/70*(qx1 - qx0)
    b.append(T(470, 28, "黏土（SM-2012-3）：按層的矩形", 13.5, BLU, weight=700))
    b.append(L(qx0, ptop, qx1, ptop, "#455a64", 1.4)); b.append(L(qx0, ptop, qx0, pbot, "#455a64", 1.4))
    for f in (0, 35, 70):
        b.append(T(F2(f), ptop - 8, f"{f}", 10.5, MUT))
    for z in (0, 4, 8, 12, 16):
        b.append(T(qx0 - 6, Z2(z) + 4, f"{z}", 10.5, MUT, "end"))
    r = N['12']
    b.append(R(qx0, Z2(0), F2(r['f1']) - qx0, Z2(8) - Z2(0), "#bbdefb", BLU, 1.4))
    b.append(R(qx0, Z2(8), F2(r['f2']) - qx0, Z2(r['L']) - Z2(8), "#90caf9", BLU, 1.4))
    b.append(T(F2(r['f1']) + 4, Z2(4), "1.0×45", 11, BLU, "start")); b.append(T(F2(r['f1']) + 4, Z2(4) + 15, "= 45.0", 11, BLU, "start", 700))
    b.append(T(F2(r['f2']) + 4, Z2(11.5), "0.75×70", 11, BLU, "start")); b.append(T(F2(r['f2']) + 4, Z2(11.5) + 15, "= 52.5", 11, BLU, "start", 700))
    b.append(T(qx0 + 4, Z2(r['L']) + 16, f"樁底 L = {r['L']:.2f} m", 11, MUT, "start"))
    b.append(T(470, 372, "α 變小、c_{u} 變大：f_{s} 只升 17%", 11, INK))
    # alpha table panel
    ax0, ay0, ax1, ay1 = 640, 330, 860, 70
    X = lambda v: ax0 + v/2.8*(ax1 - ax0); Y = lambda a: ay0 - (a - 0.2)/0.9*(ay0 - ay1)
    b.append(T(750, 28, "α 表（SM-2024-4 考卷）", 13.5, PUR, weight=700))
    axes(b, ax0, ay0, ax1, ay1, [0, 0.6, 1.4, 2.0, 2.8], [0.2, 0.4, 0.6, 0.8, 1.0], X, Y, "", "", "{}", "{:.1f}")
    pts = [(X(0), Y(1.0))] + [(X(c), Y(a)) for c, a in ALPHA]
    b.append(PL(pts, PUR, 2.4))
    for c, a in ALPHA:
        b.append(C(X(c), Y(a), 2.6, PUR))
    b.append(L(X(0.6), ay0, X(0.6), Y(0.62), RED, 1, "3,3")); b.append(L(ax0, Y(0.62), X(0.6), Y(0.62), RED, 1, "3,3"))
    b.append(C(X(0.6), Y(0.62), 5, RED, "#fff", 1.5)); b.append(T(X(0.6) + 8, Y(0.62) - 8, "c_{u}/p_{a} = 0.6 → α = 0.62", 11.5, RED, "start", 700))
    b.append(T(ax1, ay0 + 34, "c_{u} / p_{a}", 11, MUT, "end")); b.append(T(ax0 - 4, ay1 - 12, "α", 11, MUT, "start"))
    b.append(T(750, 390, "表格點逐點連線（≤ 0.1 時 α = 1）", 11, MUT))
    return svg(880, 402, b)

# ===== h2: SM-2023-3 sigma' true vs design + segmentation
def h2():
    b = [T(190, 26, "SM-2023-3：計算用 σ′_{v} 在 L_{c} 封頂", 13.5, "#0d47a1", weight=700)]
    px0, ptop, pbot, px1 = 70, 70, 330, 330
    Z = lambda z: ptop + z/25*(pbot - ptop); S = lambda s: px0 + s/360*(px1 - px0)
    b.append(L(px0, ptop, px1, ptop, "#455a64", 1.4)); b.append(L(px0, ptop, px0, pbot, "#455a64", 1.4))
    for s in (0, 90, 190, 343):
        b.append(T(S(s), ptop - 8, f"{s}", 10.5, MUT))
    b.append(T(px1 + 10, ptop - 22, "σ′_{v} (kPa)", 11, MUT, "end"))
    for z in (0, 5, 10, 15, 20, 25):
        b.append(T(px0 - 6, Z(z) + 4, f"{z}", 10.5, MUT, "end"))
    b.append(T(px0 - 6, pbot + 18, "深度 m", 11, MUT, "end"))
    zs = [i*25/250 for i in range(251)]
    b.append(PL([(S(sv_true(z)), Z(z)) for z in zs], "#90a4ae", 2, "7,4"))
    b.append(PL([(S(sv_design(z)), Z(z)) for z in zs], RED, 3))
    b.append(L(px0 - 4, Z(10), px1, Z(10), ORG, 1.4, "5,4"))
    b.append(T(S(200) + 4, Z(10) - 6, "L_{c} = 20D = 10 m（也是水位）", 11.5, ORG, "start", 700))
    b.append(T(S(300), Z(22), "實際（續增至 343）", 11, "#78909c", "end"))
    b.append(T(S(190) - 6, Z(18), "計算用 190", 11.5, RED, "end", 700))
    b.append(T(190, 356, "忘記封頂 → 側摩擦與端承同時高估", 11.5, RED))
    # right segmentation
    ox = 440; Zr = lambda z: 70 + z/25*260
    b.append(T(640, 26, "跨 L_{c} 的土層要拆段", 13.5, "#0d47a1", weight=700))
    fsg = N['23']['fs_seg']
    segs = [(0, 5, "#ffe0b2", "層 1（SM）", "σ′ 0 → 90，平均 45", fsg[0], INK),
            (5, 10, "#ffcc80", "層 2 上段（ML）", "σ′ 90 → 190，平均 140", fsg[1], INK),
            (10, 15, "#ffcc80", "層 2 下段（ML）", "σ′ = 190（封頂）", fsg[2], RED),
            (15, 25, "#ffb74d", "層 3（SW）", "σ′ = 190（封頂）", fsg[3], RED)]
    for a, bb, col, nm, txt, f, c in segs:
        b.append(R(ox + 20, Zr(a), 60, Zr(bb) - Zr(a), col, ORG, 1.2))
        ym = (Zr(a) + Zr(bb))/2
        b.append(T(ox + 92, ym - 4, f"{nm}　{txt}", 11.5, c, "start"))
        b.append(T(ox + 92, ym + 12, f"f_{{s}} = {f:.1f} kPa", 11, MUT, "start"))
    for z in (0, 5, 10, 15, 25):
        b.append(T(ox + 14, Zr(z) + 4, f"{z}", 10.5, MUT, "end"))
    b.append(L(ox + 20, Zr(10), ox + 420, Zr(10), RED, 1.8, "6,4"))
    b.append(T(640, 356, f"Q_{{s}} = 209.0 + 673.8 + 914.4 + 2168.3 = {N['23']['Qs']:.1f} kN（題解 3965.5）", 11.5, INK))
    return svg(880, 370, b)

# ===== h3: tip resistance: sand (2024-4) and clay Nc*
def h3():
    r = N['24']
    b = [T(200, 26, "砂土（SM-2024-4）：q_{p} 取兩個上限的較小者", 13.5, ORG, weight=700)]
    px0, ptop, pbot, px1 = 70, 70, 330, 360
    Z = lambda z: ptop + z/20*(pbot - ptop); Q = lambda q: px0 + q/3200*(px1 - px0)
    b.append(L(px0, ptop, px1, ptop, "#455a64", 1.4)); b.append(L(px0, ptop, px0, pbot, "#455a64", 1.4))
    for q in (0, 781, 2895):
        b.append(T(Q(q), ptop - 8, f"{q}", 10.5, MUT))
    b.append(T(px1, ptop - 24, "q_{p} (kPa)", 11, MUT, "end"))
    for z in (0, 5, 10, 15, 20):
        b.append(T(px0 - 6, Z(z) + 4, f"{z}", 10.5, MUT, "end"))
    b.append(T(px0 - 6, pbot + 18, "樁底深 m", 11, MUT, "end"))
    zs = [i*20/200 for i in range(201)]
    qn = lambda z: min(z, r['Lc'])*r['gp']*20
    b.append(PL([(Q(qn(z)), Z(z)) for z in zs], "#90a4ae", 2, "7,4"))
    b.append(PL([(Q(min(qn(z), r['ql'])), Z(z)) for z in zs], BLU, 3))
    b.append(L(px0 - 4, Z(15), px1, Z(15), ORG, 1.3, "5,4")); b.append(T(Q(r['ql']) + 10, Z(15) - 6, "L_{c} = 15D = 15 m", 11.5, ORG, "start", 700))
    b.append(L(Q(r['ql']), ptop, Q(r['ql']), pbot, RED, 1.2, "3,3"))
    b.append(T(Q(r['ql']) + 6, Z(1.6), f"q_{{l}} = 0.5p_{{a}}N_{{q}}*tanφ = {r['ql']:.1f}", 11.5, RED, "start", 700))
    b.append(T(Q(r['ql']) + 16, Z(r['z_ql']) + 18, f"約 {r['z_ql']:.1f} m 深就被 q_{{l}} 封頂", 11, BLU, "start"))
    b.append(T(Q(2895) - 4, Z(15) + 18, f"σ′_{{0}}N_{{q}}* = 144.75×20 = {r['qLc']:.0f}", 11, "#78909c", "end"))
    b.append(T(Q(r['ql']) - 6, Z(10), "採用", 12, BLU, "end", 700))
    b.append(T(200, 372, "本題樁底 50.28 m：q_{p} = 781.3 kPa（不是 2895）", 11.5, INK))
    # clay Nc*
    ax0, ay0, ax1, ay1 = 520, 320, 850, 80
    X = lambda v: ax0 + v/5*(ax1 - ax0); Y = lambda n: ay0 - (n - 5)/5*(ay0 - ay1)
    b.append(T(690, 26, "黏土：N_{c}* = 9 是深基礎的上限值", 13.5, BLU, weight=700))
    axes(b, ax0, ay0, ax1, ay1, [0, 1, 2, 2.5, 3, 4, 5], [5, 6, 7, 8, 9, 10], X, Y, "", "", "{}", "{}")
    vs = [i*5/100 for i in range(101)]
    b.append(PL([(X(v), Y(min(6*(1 + 0.2*v), 9))) for v in vs], BLU, 2.8))
    b.append(L(X(2.5), ay0, X(2.5), Y(9), "#9e9e9e", 1, "3,3"))
    b.append(C(X(2.5), Y(9), 5, RED, "#fff", 1.5))
    b.append(T(X(2.6), Y(9) + 22, "D_{f}/B ≥ 2.5 後恆為 9", 11.5, RED, "start", 700))
    b.append(T(X(2.8), Y(7.0), "Skempton（圓／方形）", 11, MUT, "start"))
    b.append(T(X(2.8), Y(7.0) + 18, "N_{c} = 6(1 + 0.2D_{f}/B) ≤ 9", 11, BLU, "start"))
    b.append(T(ax1, ay0 + 34, "埋深比 D_{f} / B", 11, MUT, "end")); b.append(T(ax0 - 4, ay1 - 12, "N_{c}", 11, MUT, "start"))
    b.append(T(690, 372, "樁的 L/D 動輒 20–50，永遠在平段 → 直接取 9", 11.5, INK))
    return svg(880, 386, b)

# ===== h5: mobilization SM-2005-4
def h5():
    r = N['05']
    b = []
    px0, py0, px1, py1 = 80, 300, 600, 70
    X = lambda dl: px0 + dl/9*(px1 - px0); Y = lambda p: py0 - p/100*(py0 - py1)
    b.append(T(340, 28, "SM-2005-4 剛性墩：同一個沉陷，兩條路徑動員的比例不同", 14, "#0d47a1", weight=700))
    axes(b, px0, py0, px1, py1, [0, 1, 1.5, 2, 4, 6, 8], [0, 25, 50, 75, 100], X, Y, "", "", "{}", "{}%")
    b.append(T(px1, py0 + 36, "墩頂沉陷 Δ (cm)", 11.5, MUT, "end")); b.append(T(px0 - 4, py1 - 14, "動員比例", 11.5, MUT, "start"))
    ds = [i*9/180 for i in range(181)]
    b.append(PL([(X(v), Y(min(v/2, 1)*100)) for v in ds], GRN, 2.8))
    b.append(PL([(X(v), Y(min(v/8, 1)*100)) for v in ds], BLU, 2.8))
    b.append(T(X(2.3), Y(100) - 8, "側摩擦：2 cm 達 τ_{s,max} = 10 kPa", 11.5, GRN, "start", 700))
    b.append(T(X(5.2), Y(5.2/8*100) + 24, "端承：8 cm 達 q_{p,max} = 400 kPa", 11.5, BLU, "start", 700))
    for dl, c in [(1, RED), (1.5, ORG)]:
        b.append(L(X(dl), py0, X(dl), py1, c, 1.2, "4,3"))
        for p, cc in [(dl/2*100, GRN), (dl/8*100, BLU)]:
            b.append(C(X(dl), Y(p), 4.5, cc, "#fff", 1.5))
    b.append(T(X(1) - 6, Y(50) + 4, "50%", 11, GRN, "end")); b.append(T(X(1.5) + 6, Y(75) + 4, "75%", 11, GRN, "start"))
    b.append(T(X(1) - 6, Y(12.5) - 6, "12.5%", 11, BLU, "end")); b.append(T(X(1.5) + 6, Y(18.75) + 14, "18.75%", 11, BLU, "start"))
    b.append(R(620, 100, 230, 150, "#fff3e0", "#ffcc80", 1))
    for i, (s, c, w) in enumerate([("位移限制下的工作荷重", "#e65100", 700),
                                   (f"Δ = 1 cm：{r['Q1']:.1f} kN", INK, None), (f"　其中摩擦佔 {r['share1']:.0%}", INK, None),
                                   (f"Δ = 1.5 cm：{r['Q15']:.1f} kN", INK, None), ("", INK, None),
                                   (f"極限法（自取 FS = 3）：{r['Qa']:.1f} kN", RED, None)]):
        b.append(T(632, 124 + i*21, s, 12, c, "start", w))
    return svg(880, 340, b)

FIG.update(h1=h1(), h2=h2(), h3=h3(), h5=h5())

def inject(path):
    s = open(path, encoding='utf-8').read()
    for k, v in FIG.items():
        tag = f'<!--FIG:{k}-->'
        if s.count(tag) != 1: raise SystemExit(f'marker {tag} count = {s.count(tag)}')
        s = re.sub(re.escape(tag) + r'\s*<svg\b.*?</svg>', lambda m: tag + '\n' + v, s, flags=re.S)
    open(path, 'w', encoding='utf-8').write(s); print('injected', len(FIG))

if __name__ == '__main__':
    if len(sys.argv) > 1: inject(sys.argv[1])
    else:
        os.makedirs('/tmp/u22figs', exist_ok=True)
        for k, v in FIG.items(): open(f'/tmp/u22figs/{k}.svg', 'w').write(v)
        print('ok')
