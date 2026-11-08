"""SS-U2-1 講義圖解：全部由 calcs.py 的數值算出座標。

用法：python3 gen_figs.py <lecture.html>
  HTML 內每張圖以 <!--FIG:id--><svg …>…</svg> 標記；本腳本只替換標記後的那一個 <svg>。
  找不到或重複標記時直接報錯。重跑結果逐位元相同。
"""
import math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "lecture-SS-U2-3"))  # 共用 figlib（同科沿用一份）
try:
    from figlib import Fig, axes, esc, INK, MUT, BLUE, RED, GREEN, ORANGE, PURPLE, STEEL, STEEL_D, GRID
except ImportError:  # 雲端暫存區只放了一份副本
    sys.path.insert(0, HERE)
    from figlib import Fig, axes, esc, INK, MUT, BLUE, RED, GREEN, ORANGE, PURPLE, STEEL, STEEL_D, GRID
import calcs as C

C.check()
SERIF = "'Times New Roman','Noto Serif',serif"


# ------------------------------------------------------------ 文字：_{下標} ^{上標}
def mk(s):
    out, i = [], 0
    while i < len(s):
        if s[i] in "_^" and i + 1 < len(s) and s[i + 1] == "{":
            j = s.index("}", i)
            dy = 4 if s[i] == "_" else -6
            out.append(f'<tspan dy="{dy}" font-size="72%">{esc(s[i + 2:j])}</tspan><tspan dy="{-dy}">​</tspan>')
            i = j + 1
        else:
            out.append(esc(s[i]))
            i += 1
    return "".join(out)


def T(f, x, y, s, size=13, fill=INK, anchor="start", weight=None, italic=False):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    w = f' font-weight="{weight}"' if weight else ""
    it = ' font-style="italic"' if italic else ""
    f.raw(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}"{a}{w}{it}>{mk(s)}</text>')


def polyline(f, pts, stroke, sw=2, dash=None):
    f.poly(pts, stroke=stroke, sw=sw, close=False, dash=dash)


def fmt(v, n=0):
    s = f"{v:,.{n}f}"
    return s


# ============================================================ F0 全景：兩段儲備
def fig_s0():
    f = Fig(900, 430, "f0")
    s, L = C.S2005, C.L05
    EI = C.E * s.I
    x = C.xc05
    # 載重–撓度（塑性鉸模型）
    d1 = C.propped_elastic_defl(x, C.w1_05, L, EI)
    du = d1 + C.ss_defl(x, C.wu05 - C.w1_05, L, EI)
    de = C.propped_elastic_defl(x, C.we_05, L, EI)
    X, Y = axes(f, 90, 50, 560, 360, 0, du * 1.45, 0, 6.2)
    # grid
    for wv in range(0, 7):
        f.line(90, Y(wv), 560, Y(wv), GRID, 1)
        T(f, 82, Y(wv) + 4, str(wv), 11, MUT, "end")
    step = 0.5 if du * 1.45 < 4 else 1.0
    k = 0.0
    while k <= du * 1.45 + 1e-9:
        T(f, X(k), 378, f"{k:g}", 11, MUT, "middle")
        k += step
    f.line(90, 360, 560, 360, INK, 1.3)
    f.line(90, 360, 90, 44, INK, 1.3)
    T(f, 325, 404, "跨間鉸位置（距固定端 351.5 cm）的撓度 Δ (cm)", 12, MUT, "middle")
    T(f, 30, 205, "w (tf/m)", 12, MUT, "middle")
    # 曲線（tf/m = 100 × tf/cm）
    pts = [(X(0), Y(0)), (X(d1), Y(C.w1_05 * 100)), (X(du), Y(C.wu05 * 100)), (X(du * 1.42), Y(C.wu05 * 100))]
    polyline(f, pts[:3], BLUE, 2.6)
    polyline(f, pts[2:], BLUE, 2.6, "7 5")
    # 標記點
    for (dd, ww, col, lab, dx, anc) in [
        (de, C.we_05 * 100, ORANGE, f"① 固定端最外纖維 F_{{y}}：w_{{e}} = {C.we_05*100:.2f}", 10, "start"),
        (d1, C.w1_05 * 100, RED, f"② 固定端成塑性鉸：w_{{1}} = {C.w1_05*100:.2f}", 10, "start"),
        (du, C.wu05 * 100, PURPLE, f"③ 跨間第二鉸 → 機構：w_{{u}} = {C.wu05*100:.2f}", 0, "middle"),
    ]:
        f.circle(X(dd), Y(ww), 5.5, "#fff" if col == ORANGE else col, col, 2)
        if anc == "middle":
            T(f, X(dd), Y(ww) - 14, lab, 12.5, col, "middle", "600")
        else:
            T(f, X(dd) + dx, Y(ww) + 4, lab, 12.5, col, anc, "600")
    T(f, X(du * 1.25), Y(C.wu05 * 100) + 20, "撓度無限增加", 11.5, MUT, "middle")
    # 右側：儲備階梯
    bx = 640
    T(f, 760, 40, "同一根梁的三個載重門檻", 13.5, INK, "middle", "700")
    yy = {k: Y(v) for k, v in (("e", C.we_05 * 100), ("1", C.w1_05 * 100), ("u", C.wu05 * 100))}
    for k, col in (("e", ORANGE), ("1", RED), ("u", PURPLE)):
        f.line(bx, yy[k], bx + 34, yy[k], col, 2.4)
    f.line(bx + 17, yy["e"] - 3, bx + 17, yy["1"] + 6, MUT, 1.3, arrow=MUT)
    f.line(bx + 17, yy["1"] - 3, bx + 17, yy["u"] + 6, MUT, 1.3, arrow=MUT)
    r1, r2, r3 = C.w1_05 / C.we_05, C.wu05 / C.w1_05, C.wu05 / C.we_05
    my1 = (yy["e"] + yy["1"]) / 2
    my2 = (yy["1"] + yy["u"]) / 2
    T(f, bx + 44, my1 - 4, f"× {r1:.2f}　斷面儲備", 13, RED, "start", "700")
    T(f, bx + 44, my1 + 14, "M_{p}/M_{y} ＝ 形狀因子", 11.5, MUT)
    T(f, bx + 44, my2 - 4, f"× {r2:.2f}　結構儲備", 13, PURPLE, "start", "700")
    T(f, bx + 44, my2 + 14, "彎矩重分配 11.657 / 8", 11.5, MUT)
    T(f, bx + 44, yy["u"] - 30, f"合計 × {r3:.2f}", 13.5, INK, "start", "700")
    T(f, bx + 44, yy["e"] + 26, "彈性設計停在這裡", 11.5, ORANGE)
    # 底註
    T(f, 450, 422, f"SS-2005-4：T 型梁一端固定一端簡支，L = 6 m，M_{{y}} = {s.My:.0f}、M_{{p}} = {s.Mp:.1f} tf·cm；"
      "塑性鉸模型（集中塑性），E = 2040 tf/cm²", 11, MUT, "middle")
    return f.svg()


# ============================================================ F1 應力狀態序列（SS-2010-1）
def fig_s1a():
    s = C.S2010
    f = Fig(900, 360, "f1")
    sc = 26.0
    top = 70
    base = top + s.H * sc         # y=0 的 px
    Yp = lambda y: base - y * sc
    # 斷面（左）
    x0 = 40
    for b, h, y in s.b:
        f.rect(x0 + (6 - b) / 2 * sc, Yp(y + h), b * sc, h * sc, STEEL, STEEL_D, 1.2)
    T(f, x0 + 3 * sc, top - 22, "SS-2010-1 斷面", 13, INK, "middle", "700")
    T(f, x0 + 3 * sc, top - 6, "（依比例，1 cm = 26 px）", 11, MUT, "middle")
    for yv, col, lab in ((s.ena, BLUE, "ENA 3.5"), (s.pna, RED, "PNA 4.0")):
        f.line(x0 - 8, Yp(yv), x0 + 6 * sc + 8, Yp(yv), col, 1.4, "5 3")
    T(f, x0 + 6 * sc + 10, Yp(s.ena) + 13, "ENA 3.5", 11, BLUE)
    T(f, x0 + 6 * sc + 10, Yp(s.pna) - 4, "PNA 4.0", 11, RED)
    T(f, x0 + 3 * sc, base + 20, "↑ 由底量起 (cm)", 10.5, MUT, "middle")
    # 三個應力圖
    fb = s._fibers(800)
    py = s.phi_y()
    panels = [
        ("① M = M_{y}", py, ORANGE),
        ("② 部分塑性", 3 * py, RED),
        ("③ M = M_{p}", None, PURPLE),
    ]
    sx = 17  # px per tf/cm²
    for i, (title, phi, col) in enumerate(panels):
        cx = 380 + i * 200
        f.line(cx, top - 6, cx, base + 6, MUT, 1)
        T(f, cx, top - 22, title, 13.5, col, "middle", "700")
        if phi is None:
            yna, M = s.pna, s.Mp
            ys = [0, yna, yna, s.H]
            sig = [-s.Fy, -s.Fy, s.Fy, s.Fy]
        else:
            yna, M = s.moment_at(phi, fb)
            ys = [s.H * k / 300 for k in range(301)]
            sig = [max(-s.Fy, min(s.Fy, C.E * phi * (y - yna))) for y in ys]
        pts = [(cx, Yp(0))] + [(cx + sg * sx, Yp(y)) for y, sg in zip(ys, sig)] + [(cx, Yp(s.H))]
        # 分上下著色
        up = [(cx, Yp(yna))] + [(cx + sg * sx, Yp(y)) for y, sg in zip(ys, sig) if y >= yna - 1e-9] + [(cx, Yp(s.H))]
        dn = [(cx, Yp(0))] + [(cx + sg * sx, Yp(y)) for y, sg in zip(ys, sig) if y <= yna + 1e-9] + [(cx, Yp(yna))]
        f.poly(up, "#ffcdd2", RED, 1.4)
        f.poly(dn, "#c8e6c9", GREEN, 1.4)
        f.line(cx - 76, Yp(yna), cx + 76, Yp(yna), INK, 1.2, "4 3")
        T(f, cx, top - 6, f"中性軸距底 {yna:.2f} cm", 11, INK, "middle")
        for yv in (0, s.H):
            pass
        f.line(cx - s.Fy * sx, top - 2, cx - s.Fy * sx, base + 2, GRID, 1, "2 3")
        f.line(cx + s.Fy * sx, top - 2, cx + s.Fy * sx, base + 2, GRID, 1, "2 3")
        T(f, cx + s.Fy * sx, base + 18, "+F_{y}", 10.5, RED, "middle")
        T(f, cx - s.Fy * sx, base + 18, "−F_{y}", 10.5, GREEN, "middle")
        T(f, cx, base + 40, f"M = {M:.1f} tf·cm", 12.5, INK, "middle", "600")
        T(f, cx, base + 58, f"M / M_{{y}} = {M / s.My:.2f}", 12, col, "middle", "700")
    T(f, 580, 18, "壓（紅，頂部）／拉（綠，底部）；橫軸為應力，F_{y} = 4.0 tf/cm²", 11.5, MUT, "middle")
    return f.svg()


# ============================================================ F2 M–φ 與中性軸遷移
def fig_s1b():
    f = Fig(900, 380, "f2")
    X, Y = axes(f, 70, 40, 480, 320, 0, 8, 0, 1.95)
    for v in [0, 0.5, 1.0, 1.5]:
        f.line(70, Y(v), 480, Y(v), GRID, 1)
        T(f, 62, Y(v) + 4, f"{v:.1f}", 11, MUT, "end")
    for k in range(0, 9, 2):
        T(f, X(k), 338, str(k), 11, MUT, "middle")
    f.line(70, 320, 480, 320, INK, 1.3); f.line(70, 320, 70, 34, INK, 1.3)
    T(f, 275, 362, "φ / φ_{y}（各斷面以自己的 φ_{y} 正規化）", 12, MUT, "middle")
    T(f, 22, 180, "M / M_{y}", 12, MUT, "middle")
    sets = [(C.S2009, BLUE, "H500×304（SS-2009-3）"), (C.RECT, GREEN, "矩形"), (C.S2005, RED, "T 型（SS-2005-4）")]
    ks = [0.02 * i for i in range(0, 401)]
    for s, col, name in sets:
        fb = s._fibers(500); py = s.phi_y()
        pts = []
        for k in ks:
            if k == 0:
                pts.append((X(0), Y(0))); continue
            _, M = s.moment_at(k * py, fb)
            pts.append((X(k), Y(M / s.My)))
        polyline(f, pts, col, 2.4)
        f.line(X(0), Y(s.f), X(8), Y(s.f), col, 1, "6 4")
        T(f, X(8) - 4, Y(s.f) - 6, f"{name}　f = {s.f:.3f}", 11.5, col, "end", "600")
    f.circle(X(1), Y(1), 4.5, "#fff", ORANGE, 2)
    T(f, X(1) + 8, Y(1) + 16, "M_{y}：最外纖維剛到 F_{y}", 11, ORANGE)
    T(f, 275, 22, "① 彎矩–曲率：曲線只會「逼近」M_{p}，不會越過", 13, INK, "middle", "700")
    # 右：T 型中性軸距頂
    s = C.S2005
    X2, Y2 = axes(f, 590, 40, 860, 320, 0, 8, 0, 6.0)   # y：距頂（cm），向下為正→ 用反向
    Yd = lambda d: 40 + d / 6.0 * 280
    for d in range(0, 7):
        f.line(590, Yd(d), 860, Yd(d), GRID, 1)
        T(f, 582, Yd(d) + 4, str(d), 11, MUT, "end")
    for k in range(0, 9, 2):
        T(f, X2(k), 338, str(k), 11, MUT, "middle")
    f.line(590, 320, 860, 320, INK, 1.3); f.line(590, 320, 590, 34, INK, 1.3)
    T(f, 725, 362, "φ / φ_{y}", 12, MUT, "middle")
    T(f, 528, 180, "距翼板頂 (cm)", 11.5, MUT, "middle")
    fb = s._fibers(600); py = s.phi_y()
    pts = []
    for k in ks:
        if k == 0:
            yna = s.ena
        else:
            yna, _ = s.moment_at(k * py, fb)
        pts.append((X2(k), Yd(s.H - yna)))
    polyline(f, pts, RED, 2.4)
    dE, dP = s.H - s.ena, s.H - s.pna
    f.line(590, Yd(dE), 860, Yd(dE), BLUE, 1.2, "6 4")
    f.line(590, Yd(dP), 860, Yd(dP), PURPLE, 1.2, "6 4")
    T(f, 856, Yd(dE) + 15, f"ENA {dE:.2f}", 11.5, BLUE, "end", "600")
    T(f, 856, Yd(dP) - 6, f"PNA {dP:.3f}", 11.5, PURPLE, "end", "600")
    f.line(590, Yd(2.6), 860, Yd(2.6), STEEL_D, 1, "2 3")
    T(f, 600, Yd(2.6) + 14, "翼板底 2.6", 10.5, STEEL_D)
    T(f, 725, 22, "② T 型梁的中性軸一路往翼板走", 13, INK, "middle", "700")
    return f.svg()


# ============================================================ F3 Z 的拆塊（SS-2020-2 與 SS-2005-4）
def _section_panel(f, s, x_c, top, sc, title, sub, flip_label_side=False):
    Yp = lambda y: top + (s.H - y) * sc
    W = max(b for b, _, _ in s.b)
    p = s.pna
    T(f, x_c, top - 26, title, 13.5, INK, "middle", "700")
    T(f, x_c, top - 10, sub, 11, MUT, "middle")
    pieces = []
    for b, h, y in s.b:
        lo, hi = y, y + h
        segs = [(lo, hi)] if (hi <= p or lo >= p) else [(lo, p), (p, hi)]
        for a, c in segs:
            comp = (a + c) / 2 > p
            f.rect(x_c - b / 2 * sc, Yp(c), b * sc, (c - a) * sc,
                   "#ffcdd2" if comp else "#c8e6c9", RED if comp else GREEN, 1.1)
            pieces.append((b * (c - a), abs((a + c) / 2 - p), (a + c) / 2, comp, b))
    f.line(x_c - W / 2 * sc - 30, Yp(p), x_c + W / 2 * sc + 30, Yp(p), PURPLE, 1.8, "6 3")
    f.line(x_c - W / 2 * sc - 30, Yp(s.ena), x_c + W / 2 * sc + 30, Yp(s.ena), BLUE, 1.4, "3 3")
    return Yp, pieces


def fig_s2a():
    f = Fig(900, 470, "f3")
    # 左：SS-2020-2
    s = C.S2020
    sc = 5.4
    Yp, pcs = _section_panel(f, s, 125, 70, sc, "SS-2020-2 非對稱 H", "1 cm = 5.4 px；PNA 落在腹板")
    dtop = lambda y: s.H - y
    T(f, 125 + 15 * sc + 34, Yp(s.pna) + 4, f"PNA（距頂 {dtop(s.pna):.2f}）", 11.5, PURPLE, "start", "600")
    T(f, 125 + 15 * sc + 34, Yp(s.ena) + 4, f"ENA（距頂 {dtop(s.ena):.2f}）", 11.5, BLUE, "start", "600")
    rows = []
    names = {0: "下翼板", 1: "腹板下段", 2: "腹板上段", 3: "上翼板"}
    for i, (A, d, yc, comp, b) in enumerate(pcs):
        rows.append((names[i], A, d, A * d, comp))
    tx = 232
    T(f, tx, 300, "塊", 11.5, MUT); T(f, tx + 95, 300, "A (cm²)", 11.5, MUT, "end")
    T(f, tx + 165, 300, "d (cm)", 11.5, MUT, "end"); T(f, tx + 240, 300, "A·d (cm³)", 11.5, MUT, "end")
    for j, (n, A, d, Ad, comp) in enumerate(reversed(rows)):
        yy = 320 + j * 20
        col = RED if comp else GREEN
        T(f, tx, yy, n, 12, col, "start", "600")
        T(f, tx + 95, yy, f"{A:.2f}", 12, INK, "end")
        T(f, tx + 165, yy, f"{d:.2f}", 12, INK, "end")
        T(f, tx + 240, yy, fmt(Ad, 1), 12, INK, "end")
    f.line(tx, 323 + 3 * 20 + 4, tx + 240, 323 + 3 * 20 + 4, MUT, 1)
    T(f, tx, 323 + 4 * 20 + 6, f"Z = {fmt(s.Z, 1)} cm³", 12.5, PURPLE, "start", "700")
    up = math.fsum(r[1] for r in rows if r[4]); dn = math.fsum(r[1] for r in rows if not r[4])
    T(f, tx, 323 + 5 * 20 + 6, f"壓 {up:.2f} = 拉 {dn:.2f} cm²", 11.5, MUT)
    # 右：SS-2005-4 T
    s2 = C.S2005
    sc2 = 6.0
    Yq, pcs2 = _section_panel(f, s2, 710, 70, sc2, "SS-2005-4 T 型", "1 cm = 6 px；PNA 落在翼板內")
    T(f, 710 - 20 * sc2 - 36, Yq(s2.pna) + 4, f"PNA 距頂 {s2.H - s2.pna:.3f}", 11.5, PURPLE, "end", "600")
    T(f, 710 - 20 * sc2 - 36, Yq(s2.ena) + 4, f"ENA 距頂 {s2.H - s2.ena:.2f}", 11.5, BLUE, "end", "600")
    names2 = {0: "腹板（肢）", 1: "翼板 PNA 以下", 2: "翼板 PNA 以上"}
    tx = 568
    T(f, tx, 300, "塊", 11.5, MUT); T(f, tx + 140, 300, "A", 11.5, MUT, "end")
    T(f, tx + 200, 300, "d", 11.5, MUT, "end"); T(f, tx + 270, 300, "A·d", 11.5, MUT, "end")
    for j, (A, d, yc, comp, b) in enumerate(reversed(pcs2)):
        yy = 320 + j * 20
        col = RED if comp else GREEN
        T(f, tx, yy, names2[len(pcs2) - 1 - j], 12, col, "start", "600")
        T(f, tx + 140, yy, f"{A:.2f}", 12, INK, "end")
        T(f, tx + 200, yy, f"{d:.3f}", 12, INK, "end")
        T(f, tx + 270, yy, f"{A * d:.2f}", 12, INK, "end")
    f.line(tx, 323 + 2 * 20 + 4, tx + 270, 323 + 2 * 20 + 4, MUT, 1)
    T(f, tx, 323 + 3 * 20 + 6, f"Z = {s2.Z:.2f} cm³", 12.5, PURPLE, "start", "700")
    T(f, tx, 323 + 4 * 20 + 6, "翼板 104 cm² > A/2 = 77.68 → PNA 在翼板", 11.5, MUT)
    f.line(520, 40, 520, 450, GRID, 1.2)
    return f.svg()


# ============================================================ F4 形狀因子比較
def fig_s2b():
    data = [
        ("H600×300×12×20（SS-2006-3）", C.S2006.f, BLUE),
        ("H500×304×15×24（SS-2009-3）", C.S2009.f, BLUE),
        ("非對稱 H（SS-2020-2）", C.S2020.f, ORANGE),
        ("非對稱 I（SS-2023-3）", C.S2023.f, ORANGE),
        ("矩形", C.RECT.f, PURPLE),
        ("空心圓 d = 0.6D（SS-2013-1）", C.f_tube, PURPLE),
        ("實心圓", C.f_circ, PURPLE),
        ("上下不對稱堆疊（SS-2010-1）", C.S2010.f, ORANGE),
        ("T 型（SS-2005-4）", C.S2005.f, RED),
    ]
    f = Fig(900, 410, "f4")
    X = lambda v: 300 + (v - 1.0) / 0.9 * 540
    T(f, 450, 22, "形狀因子 f = Z / S_{min}：面積離中性軸越遠，f 越小", 13.5, INK, "middle", "700")
    for v in (1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9):
        f.line(X(v), 40, X(v), 360, GRID, 1)
        T(f, X(v), 376, f"{v:.1f}", 11, MUT, "middle")
    for i, (n, v, col) in enumerate(data):
        y = 50 + i * 34
        f.rect(X(1.0), y, X(v) - X(1.0), 22, col, col, 1, op=0.85)
        T(f, X(1.0) - 8, y + 16, n, 12, INK, "end")
        T(f, X(v) + 6, y + 16, f"{v:.3f}", 12, col, "start", "700")
    f.line(X(1.0), 40, X(1.0), 360, INK, 1.3)
    T(f, 450, 400, "藍＝雙對稱 H（面積集中在翼板）　紫＝實心／圓形　橙＝非對稱　紅＝T 型（S 取肢端較小者）", 11, MUT, "middle")
    return f.svg()


# ============================================================ F5 鉸 vs 塑性鉸
def fig_s3():
    f = Fig(900, 330, "f5")
    for i, (title, col) in enumerate((("一般鉸（pin）", BLUE), ("塑性鉸（剛塑性理想化）", RED))):
        ox = 80 + i * 450
        X, Y = axes(f, ox, 60, ox + 300, 260, -1, 1, -1.4, 1.4)
        f.line(X(-1), Y(0), X(1), Y(0), INK, 1.2, arrow=INK)
        f.line(X(0), Y(-1.4), X(0), Y(1.4), INK, 1.2, arrow=INK)
        T(f, X(1) + 4, Y(0) + 16, "θ（相對轉角）", 11.5, MUT, "end")
        T(f, X(0) + 6, Y(1.4) + 4, "M", 12, MUT)
        T(f, X(0), 36, title, 14, col, "middle", "700")
        if i == 0:
            f.line(X(-0.95), Y(0), X(0.95), Y(0), col, 4)
            T(f, X(0.5), Y(0) - 12, "M ≡ 0，轉多少都行", 12, col, "middle", "600")
            T(f, X(0), 300, "不傳彎矩、不耗能：虛功法裡這一點的內功 = 0", 12, INK, "middle")
        else:
            f.line(X(0), Y(-1), X(0), Y(1), col, 4)
            f.line(X(0), Y(1), X(0.86), Y(1), col, 4)
            f.line(X(0), Y(-1), X(-0.86), Y(-1), col, 4)
            f.line(X(0.80), Y(1), X(0.95), Y(1), col, 1.6, arrow=col)
            f.line(X(-0.80), Y(-1), X(-0.95), Y(-1), col, 1.6, arrow=col)
            f.line(X(0.6), Y(1), X(0.6), Y(0.35), ORANGE, 1.8, "5 3", arrow=ORANGE)
            T(f, X(0.6) + 8, Y(0.6), "卸載：轉角留下", 11, ORANGE)
            T(f, X(0.5), Y(1) - 10, "+M_{p}：可持續轉動", 12, col, "middle", "600")
            T(f, X(-0.5), Y(-1) + 22, "−M_{p}", 12, col, "middle", "600")
            T(f, X(0) - 8, Y(0.5), "|M| < M_{p}", 11.5, MUT, "end")
            T(f, X(0) - 8, Y(0.5) + 15, "不轉（剛性）", 11.5, MUT, "end")
            T(f, X(0), 300, "轉動時仍傳 M_{p}、耗能 M_{p}·θ；每多一個就少一個贅餘約束", 12, INK, "middle")
    f.line(450, 30, 450, 310, GRID, 1.2)
    return f.svg()


# ============================================================ F6 機構幾何 + w(x)
def fig_s4():
    f = Fig(900, 600, "f6")
    L = C.L05; xc = C.xc05
    x0, x1 = 110, 790
    px = lambda x: x0 + x / L * (x1 - x0)
    yb = 150
    dmax = 70   # 虛位移放大（示意比例）
    T(f, 450, 24, "① 崩塌機構的虛位移（固定端 A、跨間鉸 C、簡支端 B；SS-2005-4 尺寸）", 13.5, INK, "middle", "700")
    # 原梁
    f.line(px(0), yb, px(L), yb, STEEL_D, 6, op=0.25)
    # 固定端牆
    f.rect(px(0) - 22, yb - 46, 22, 92, f.hatch(), STEEL_D, 1.2)
    # 簡支
    f.poly([(px(L), yb + 3), (px(L) - 12, yb + 22), (px(L) + 12, yb + 22)], "#fff", INK, 1.4)
    f.line(px(L) - 18, yb + 26, px(L) + 18, yb + 26, INK, 1.4)
    # 均布載重
    for k in range(0, 21):
        xx = px(L * k / 20)
        f.line(xx, yb - 52, xx, yb - 12, BLUE, 1.2, arrow=BLUE)
    f.line(px(0), yb - 52, px(L), yb - 52, BLUE, 1.4)
    T(f, px(L / 2), yb - 60, "w_{u}", 13, BLUE, "middle", "700")
    # 機構形狀
    f.poly([(px(0), yb), (px(xc), yb + dmax), (px(L), yb)], stroke=RED, sw=3, close=False)
    for xx in (0, xc):
        f.circle(px(xx), yb + (dmax if xx else 0), 7, RED, "#fff", 2)
    T(f, px(0) + 10, yb - 4, "A", 13, INK, "start", "700")
    T(f, px(xc), yb + dmax + 26, "C", 13, INK, "middle", "700")
    T(f, px(L) + 18, yb - 4, "B", 13, INK, "start", "700")
    f.line(px(xc), yb, px(xc), yb + dmax, MUT, 1, "3 3")
    T(f, px(xc) + 6, yb + dmax / 2 + 4, "δ = x·θ", 12, MUT)
    # 角度弧
    ang = math.atan(dmax / (px(xc) - px(0)))
    R = 130
    f.path(f"M{px(0)+R:.1f},{yb:.1f} A{R},{R} 0 0,1 {px(0)+R*math.cos(ang):.1f},{yb+R*math.sin(ang):.1f}", stroke=ORANGE, sw=1.8)
    T(f, px(0) + R + 6, yb + R * math.sin(ang) / 2 + 5, "θ", 13, ORANGE, "start", "700")
    T(f, px(L) - 60, yb + 44, "θ·x/(L−x)", 12, ORANGE, "end")
    # 尺寸
    f.dim(px(0), yb + 110, px(xc), yb + 110, f"x = (2−√2)L = {xc:.1f} cm", BLUE)
    f.dim(px(xc), yb + 110, px(L), yb + 110, f"L − x = {L - xc:.1f} cm", MUT)
    T(f, 450, yb + 140, "內功：A 轉 θ、C 的相對轉角 θ + θx/(L−x) = θL/(L−x)；B 是真鉸，M = 0 不耗能。外功：w·(三角形面積) = w·Lδ/2", 11.5, INK, "middle")
    # 下：w(x) 曲線
    X, Y = axes(f, 110, 340, 790, 540, 0.2, 0.95, 11.0, 16.0)
    for v in (11, 12, 13, 14, 15, 16):
        f.line(110, Y(v), 790, Y(v), GRID, 1)
        T(f, 102, Y(v) + 4, str(v), 11, MUT, "end")
    for v in (0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9):
        T(f, X(v), 558, f"{v:.1f}", 11, MUT, "middle")
    f.line(110, 540, 790, 540, INK, 1.3); f.line(110, 540, 110, 334, INK, 1.3)
    T(f, 450, 582, "x / L（跨間鉸距固定端）", 12, MUT, "middle")
    T(f, 50, 440, "w·L²/M_{p}", 12, MUT, "middle")
    T(f, 450, 322, "② 每一個 x 都給一個「看起來合理」的 w；真正的崩塌載重是其中最小的那個", 13.5, INK, "middle", "700")
    pts = []
    for i in range(0, 301):
        xr = 0.2 + 0.75 * i / 300
        wv = C.w_propped(xr * L, L, 1.0) * L * L
        if wv <= 16.0:
            pts.append((X(xr), Y(wv)))
    polyline(f, pts, BLUE, 2.5)
    xo = C.X_OPT
    wo = C.w_propped(xo * L, L, 1.0) * L * L
    wm = C.w_propped(0.5 * L, L, 1.0) * L * L
    f.circle(X(xo), Y(wo), 6, PURPLE, "#fff", 2)
    f.circle(X(0.5), Y(wm), 5.5, "#fff", ORANGE, 2)
    T(f, X(xo) + 10, Y(wo) + 18, f"最小：x = {xo:.4f}L → w_{{u}} = {wo:.3f} M_{{p}}/L²（距簡支端 {1 - xo:.4f}L）", 12, PURPLE, "start", "700")
    T(f, X(0.5) - 12, Y(wm) + 24, f"猜跨中：{wm:.3f}（偏高 {(wm / wo - 1) * 100:.1f}%，不安全）", 12, ORANGE, "end", "600")
    return f.svg()


# ============================================================ F7 彎矩重分配（BMD 疊圖）
def fig_s5():
    f = Fig(900, 400, "f7")
    L = C.L05; Mp = C.S2005.Mp
    X, Y = axes(f, 90, 50, 820, 330, 0, 1, -1.25, 1.25)
    for v in (-1, -0.5, 0, 0.5, 1):
        f.line(90, Y(v), 820, Y(v), GRID if v not in (-1, 1) else "#b0bec5", 1, None if v in (0,) else ("6 4" if v in (-1, 1) else None))
        T(f, 82, Y(v) + 4, f"{v:+.1f}" if v else "0", 11, MUT, "end")
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        T(f, X(v), Y(-1.25) + 18, f"{v:.2f}", 11, MUT, "middle")
    f.line(90, Y(0), 820, Y(0), INK, 1.3)
    f.line(90, 50, 90, 330, INK, 1.3)
    T(f, 455, 372, "x / L（自固定端 A 起算）", 12, MUT, "middle")
    T(f, 36, 190, "M / M_{p}", 12, MUT, "middle")
    T(f, 816, Y(1) - 6, "+M_{p}", 12, RED, "end", "700")
    T(f, 816, Y(-1) + 16, "−M_{p}", 12, RED, "end", "700")
    xs = [L * i / 400 for i in range(401)]
    # 第一鉸瞬間：彈性解，固定端 = wL²/8 = Mp
    M1 = C.propped_M(xs, C.w1_05, L, C.w1_05 * L * L / 8)
    Mu = C.propped_M(xs, C.wu05, L, Mp)
    polyline(f, [(X(x / L), Y(m / Mp)) for x, m in zip(xs, M1)], ORANGE, 2.4)
    polyline(f, [(X(x / L), Y(m / Mp)) for x, m in zip(xs, Mu)], PURPLE, 2.6)
    i1 = M1.index(max(M1))
    xc = C.xc05
    Mxc = C.propped_M([xc], C.wu05, L, Mp)[0]
    assert abs(Mxc - Mp) < 1e-6 * Mp and max(Mu) <= Mp * (1 + 1e-9)
    f.circle(X(xs[i1] / L), Y(M1[i1] / Mp), 5, "#fff", ORANGE, 2)
    f.circle(X(xc / L), Y(1.0), 6, PURPLE, "#fff", 2)
    f.circle(X(0), Y(-1), 6, RED, "#fff", 2)
    f.line(X(xs[i1] / L), Y(M1[i1] / Mp) + 6, X(0.80), Y(-0.10), ORANGE, 1, "3 3")
    T(f, X(0.80), Y(-0.10) + 16, f"w_{{1}}：跨間最大 {M1[i1] / Mp:.4f} M_{{p}}（x = {xs[i1] / L:.3f}L）", 12, ORANGE, "middle", "600")
    T(f, X(xc / L), Y(1.0) - 12, f"w_{{u}}：跨間 x = {C.X_OPT:.4f}L 處達 +M_{{p}}，全跨無一處超過", 12, PURPLE, "middle", "700")
    T(f, X(0) + 14, Y(-1) + 24, "A：w_{1} 時已達 −M_{p}，之後被鎖在 −M_{p}", 12, RED, "start", "600")
    T(f, 455, 30, "從 w_{1} 到 w_{u}，多出來的載重全部由「跨間」扛——這就是彎矩重分配", 13.5, INK, "middle", "700")
    return f.svg()


# ============================================================ F8 解題決策流程
def fig_s7():
    f = Fig(900, 820, "f8")

    def box(cx, cy, w, h, rows, col=BLUE, fill="#e3f2fd", size=12.5):
        f.rect(cx - w / 2, cy - h / 2, w, h, fill, col, 1.6, rx=8)
        n = len(rows); lh = size * 1.45
        for i, r in enumerate(rows):
            T(f, cx, cy - (n - 1) * lh / 2 + i * lh + size * 0.35, r, size, INK, "middle")

    def dia(cx, cy, w, h, rows, size=12.5):
        f.poly([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)], "#fff3e0", ORANGE, 1.6)
        n = len(rows); lh = size * 1.4
        for i, r in enumerate(rows):
            T(f, cx, cy - (n - 1) * lh / 2 + i * lh + size * 0.35, r, size, INK, "middle", "600")

    def arr(pts, lab=None, lp=None, col=MUT):
        f.poly(pts, stroke=col, sw=1.6, close=False, arrow=col)
        if lab:
            T(f, lp[0], lp[1], lab, 12, col, "middle", "700")

    box(450, 40, 300, 44, ["讀題：問的是什麼？"], INK, "#eceff1", 13.5)
    dia(450, 125, 300, 90, ["斷面性質（M_{y}／M_{p}／Z／f）", "還是崩塌載重？"])
    arr([(450, 62), (450, 80)])
    # 左支：斷面
    LX, RX = 210, 690
    arr([(300, 125), (LX, 125), (LX, 165)], "斷面", (255, 117))
    box(LX, 195, 300, 56, ["分塊 → 一次矩求 ENA", "→ 平行軸求 I"])
    arr([(LX, 223), (LX, 243)])
    box(LX, 271, 300, 56, ["c 取離 ENA 較遠側 → S_{min}", "M_{y} = F_{y}·S_{min}"])
    arr([(LX, 299), (LX, 317)])
    dia(LX, 360, 250, 84, ["上下對稱？"])
    arr([(LX + 125, 360), (LX + 175, 360), (LX + 175, 533), (LX + 150, 533)], "是", (LX + 150, 352))
    arr([(LX, 402), (LX, 425)], "否", (LX - 14, 418))
    box(LX, 455, 300, 56, ["半面積法：累加到 A/2", "先判斷 PNA 落在哪一塊"])
    T(f, LX + 181, 450, "PNA = ENA", 11.5, MUT, "start")
    arr([(LX, 483), (LX, 503)])
    box(LX, 533, 300, 60, ["Z = Σ A_{i}·d_{i}（跨 PNA 的板切開）", "M_{p} = F_{y}·Z，f = Z / S_{min}"])
    # 右支：結構
    arr([(600, 125), (RX, 125), (RX, 165)], "崩塌載重", (648, 117))
    box(RX, 195, 300, 56, ["先求 M_{p}（走左支）", "靜不定度 n → 完整機構需 n+1 鉸"])
    arr([(RX, 223), (RX, 243)])
    box(RX, 271, 300, 56, ["列候選鉸位：固定端、集中力點、", "斷面變化處、均布的最大正彎矩點"])
    arr([(RX, 299), (RX, 317)])
    dia(RX, 360, 250, 84, ["跨間鉸位置", "已知？"])
    arr([(RX, 402), (RX, 425)], "否（均布）", (RX - 44, 418))
    arr([(RX + 125, 360), (RX + 170, 360), (RX + 170, 535), (RX + 150, 535)], "是", (RX + 150, 352))
    box(RX, 455, 300, 56, ["設距離 x，W_{ext} = W_{int}", "dw/dx = 0 求最小 w"])
    arr([(RX, 483), (RX, 505)])
    box(RX, 535, 300, 56, ["每個候選機構都算一次", "取最小者（上限定理）"])
    arr([(RX, 563), (RX, 585)])
    dia(RX, 630, 260, 90, ["畫崩塌時彎矩圖：", "全跨 |M| ≤ M_{p}？"])
    arr([(RX + 130, 630), (RX + 200, 630), (RX + 200, 271), (RX + 150, 271)], "否：換機構", (RX + 158, 618))
    arr([(RX, 675), (RX, 700), (450, 700), (450, 718)], "是", (RX - 14, 692))
    f.poly([(LX, 563), (LX, 700), (450, 700)], stroke=MUT, sw=1.6, close=False)
    box(450, 752, 420, 64, ["前提檢核：寬厚比 λ ≤ λ_{pd}、側向支撐、", "題目指定版本（AISC 360 的 T 型限制等）→ 作答"], PURPLE, "#f3e5f5")
    return f.svg()


FIGS = {
    "s0": fig_s0, "s1a": fig_s1a, "s1b": fig_s1b, "s2a": fig_s2a, "s2b": fig_s2b,
    "s3": fig_s3, "s4": fig_s4, "s5": fig_s5, "s7": fig_s7,
}


def apply(path):
    h = open(path, encoding="utf-8").read()
    for k, fn in FIGS.items():
        pat = re.compile(r"(<!--FIG:" + re.escape(k) + r"-->)\s*<svg\b.*?</svg>", re.S)
        n = len(pat.findall(h))
        if n != 1:
            raise SystemExit(f"FIG:{k} 標記數 {n}（應為 1）")
        svg = fn()
        h = pat.sub(lambda m: m.group(1) + svg, h)
    open(path, "w", encoding="utf-8").write(h)
    print("figs ->", path, len(FIGS))


if __name__ == "__main__":
    apply(sys.argv[1])
