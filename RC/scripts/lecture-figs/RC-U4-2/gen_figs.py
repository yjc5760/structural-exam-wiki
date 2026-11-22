# -*- coding: utf-8 -*-
"""lecture-RC-U4-2 圖解產生器：所有座標由 calcs.py 的數值換算，注入 study/lecture-RC-U4-2.html。
用法（在 RC/ 下）：python3 scripts/lecture-figs/RC-U4-2/gen_figs.py study/lecture-RC-U4-2.html"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from svglib import *          # noqa
import calcs as c             # noqa  （import 時即跑完全部 assert）


def f0():
    """2010-4 跨中兩種極端配置的應力分布。"""
    W, H = 900, 330
    b = [L(450, 20, 450, 320, "#cfd8dc", 2, "6 5")]
    k = 1.3           # px per kgf/cm²
    yt, yb = 92, 252   # 斷面高 90 cm → 160 px
    for side, (title, sub_, st, lim, note, col) in enumerate([
        ("上限：e = 34.71 cm", "傳遞階段（Pi＝200 tf，只有自重 MG）", c.st10_tr_emax, "頂", "頂纖維 −13.39 ＝ −0.8√f'ci", RED),
        ("下限：e = 12.83 cm", "使用階段（Pe＝170 tf，MG＋ML）", c.st10_sv_emin, "底", "底纖維 −37.42 ＝ −2.0√f'c（U 類）", RED)]):
        x_off = side * 450
        b.append(T(x_off + 225, 30, title, 15, "middle", BLUE2, True))
        b.append(T(x_off + 225, 52, sub_, 12.5, "middle", AX))
        # 斷面
        sx = x_off + 70
        b.append(R(sx, yt, 50, yb - yt, GREY2, GREY, 1.5))
        ecm = c.r10["e1"] if side == 0 else c.r10["e3"]
        ycg = (yt + yb) / 2
        ye = ycg + ecm * (yb - yt) / 90
        b.append(L(sx - 8, ycg, sx + 58, ycg, MUT, 1, "4 3"))
        b.append(C(sx + 25, ye, 5, BLUE))
        b.append(T(sx - 12, ycg + 4, "形心", 11, "end", MUT))
        b.append(L(sx + 62, ycg, sx + 62, ye, BLUE, 1.2, marker=f"f0-a{side}"))
        b.append(T(sx + 66, (ycg + ye) / 2 + 4, f"e={ecm:.2f}", 11.5, "start", BLUE))
        # 應力圖
        x0 = x_off + 230
        part, xt, xb = stress_diag(x0, yt, yb, st[0], st[1], k)
        b += part
        b.append(T(xt + (6 if st[0] >= 0 else -6), yt - 6, f"{st[0]:+.2f}", 12, "start" if st[0] >= 0 else "end",
                   RED if st[0] < 0 else BLUE, True))
        b.append(T(xb + (6 if st[1] >= 0 else -6), yb + 16, f"{st[1]:+.2f}", 12, "start" if st[1] >= 0 else "end",
                   RED if st[1] < 0 else BLUE, True))
        b.append(T(x0, yb + 40, note, 12.5, "middle", col, True))
        b.append(T(x0 + 70, yt + 70, "壓（＋）→", 11, "start", MUT))
    b.insert(0, defs(("f0-a0", BLUE), ("f0-a1", BLUE)))
    b.append(T(450, 318, "kgf/cm²，壓為正（畫向右）；兩格的拉應力都剛好等於容許值——偏心再大或再小就超限", 12, "middle", AX))
    return svg(W, H, b, "RC-2010-4 偏心上限與下限兩種配置的應力分布")


def f1():
    """2010-4 可行區：橫軸 Pi（tf），縱軸 e（cm）。"""
    W, H = 900, 400
    x0, x1, y0, y1 = 90, 640, 350, 40         # 繪圖區
    Pmin, Pmax, emin, emax = 100, 400, -40, 70
    X = lambda P: x0 + (P - Pmin) / (Pmax - Pmin) * (x1 - x0)
    Y = lambda e: y0 - (e - emin) / (emax - emin) * (y0 - y1)
    r, al = c.r10, c.al10
    k, S, MG, MT, eta = r["k"], r["S"], c.MG10, c.MG10 + c.ML10, c.eta10
    fns = {
        "①": lambda Pi: k + (MG + al["fti"] * S) / Pi,
        "②": lambda Pi: -k + (al["fci_c"] * S + MG) / Pi,
        "③": lambda Pi: -k + (MT - al["ftU"] * S) / (eta * Pi),
        "④": lambda Pi: k + (MT - al["fc_all"] * S) / (eta * Pi),
    }
    Ps = [Pmin + (Pmax - Pmin) * i / 200 for i in range(201)]
    b = [defs()]
    # 可行區（上界 = min(①,②,35)，下界 = max(③,④)）
    up = [min(fns["①"](P * 1000), fns["②"](P * 1000), 35.0) for P in Ps]
    lo = [max(fns["③"](P * 1000), fns["④"](P * 1000)) for P in Ps]
    poly = [(X(P), Y(u)) for P, u, l in zip(Ps, up, lo) if u >= l]
    polyl = [(X(P), Y(l)) for P, u, l in zip(Ps, up, lo) if u >= l]
    b.append(P(poly + polyl[::-1], "#cfd8dc", "none", 0, op=0.8))
    # 軸
    b.append(L(x0, y0, x1, y0, AX, 1.3)); b.append(L(x0, y0, x0, y1, AX, 1.3))
    for P_ in range(100, 401, 50):
        b.append(L(X(P_), y0, X(P_), y0 + 5, AX, 1)); b.append(T(X(P_), y0 + 19, str(P_), 11, "middle", AX))
    for e_ in range(-40, 71, 10):
        b.append(L(x0 - 5, Y(e_), x0, Y(e_), AX, 1)); b.append(T(x0 - 8, Y(e_) + 4, str(e_), 11, "end", AX))
    b.append(L(x0, Y(0), x1, Y(0), MUT, 1, "3 3"))
    b.append(T((x0 + x1) / 2, y0 + 38, "初始預力 Pi（tf）", 12.5, "middle", INK))
    b.append(T(28, (y0 + y1) / 2, "e（cm）", 12.5, "middle", INK))
    b.append(L(x0, Y(35), x1, Y(35), GREY, 1.2, "6 4"))
    b.append(T(x1 - 4, Y(35) - 5, "幾何上限 e＝35（h/2−10）", 11, "end", GREY))
    cols = {"①": RED, "②": ORG, "③": BLUE, "④": GRN}
    lab = {"①": "① 傳遞頂拉", "②": "② 傳遞底壓", "③": "③ 使用底拉", "④": "④ 使用頂壓"}
    for kname, fn in fns.items():
        pts = [(X(P), Y(fn(P * 1000))) for P in Ps if emin <= fn(P * 1000) <= emax]
        b.append(P(pts, "none", cols[kname], 2.2, close=False))
    # 標籤放在右側欄
    for i, kname in enumerate(fns):
        yy = 70 + i * 26
        b.append(L(670, yy - 4, 700, yy - 4, cols[kname], 2.4)); b.append(T(708, yy, lab[kname], 12.5, "start", cols[kname], True))
    b.append(T(670, 190, "e ≤ ①、②（上限）", 12, "start", INK))
    b.append(T(670, 210, "e ≥ ③、④（下限）", 12, "start", INK))
    b.append(R(668, 226, 18, 12, "#cfd8dc", "none", 0)); b.append(T(692, 237, "可行區", 12, "start", INK))
    # Pi = 200
    xp = X(200)
    b.append(L(xp, y0, xp, y1, RED, 1.4, "5 3"))
    for e_, s in ((c.r10["e1"], "34.71"), (c.r10["e3"], "12.83")):
        b.append(C(xp, Y(e_), 4.5, RED)); b.append(T(xp + 8, Y(e_) + (-6 if s == "34.71" else 16), f"e = {s}", 12, "start", RED, True))
    b.append(T(xp, y1 - 8, "題目 Pi＝200 tf", 12, "middle", RED, True))
    b.append(T(670, 290, "Pi＝200 tf 時：", 12.5, "start", INK, True))
    b.append(T(670, 312, "12.83 ≤ e ≤ 34.71 cm", 12.5, "start", RED, True))
    b.append(T(670, 336, "② 給 56.89、④ 給 −25.70，", 12, "start", AX))
    b.append(T(670, 356, "都在可行區之外（不控制）", 12, "start", AX))
    return svg(W, H, b, "RC-2010-4 四控制條件可行區")


def f2():
    """2010-4 直線 vs 曲線鋼腱：立面＋活載容量長條。"""
    W, H = 900, 390
    xA, xB, yt, yb = 80, 820, 40, 130            # 梁立面（15 m → 740 px；高 90 cm → 90 px，垂直放大 7.4 倍）
    sc = (yb - yt) / 90
    ycg = (yt + yb) / 2
    b = [defs(("f2-ar", AX))]
    b.append(R(xA, yt, xB - xA, yb - yt, GREY2, GREY, 1.4))
    b.append(L(xA - 10, ycg, xB + 10, ycg, MUT, 1, "5 4"))
    b.append(T(xB + 14, ycg + 4, "形心", 11, "start", MUT))
    # 直線鋼腱
    ys = ycg + c.e_str10 * sc
    b.append(L(xA, ys, xB, ys, ORG, 2.4))
    # 曲線鋼腱（拋物線）
    N = 120
    pts = [(xA + (xB - xA) * i / N, ycg + c.r10["e1"] * 4 * (i / N) * (1 - i / N) * sc) for i in range(N + 1)]
    b.append(P(pts, "none", BLUE, 2.4, close=False))
    b.append(T(xA, yb + 40, f"直線：全長 e＝{c.e_str10:.2f} cm（梁端 M＝0 控制，一般值 0.8√f'ci）", 12, "start", ORG, True))
    b.append(T(xA, yb + 20, f"曲線：梁端 0、跨中 e＝{c.r10['e1']:.2f} cm（跨中 MG 抵銷）", 12, "start", BLUE, True))
    b.append(T(xA, yt - 10, "梁端", 11.5, "middle", AX)); b.append(T(xB, yt - 10, "梁端", 11.5, "middle", AX))
    b.append(T((xA + xB) / 2, yt - 10, "跨中", 11.5, "middle", AX))
    b.append(T(xB, yt - 26, "立面（垂直方向放大，l＝15 m，h＝90 cm）", 11, "end", MUT))
    # 長條：ML 容量
    bx0, by = 260, 230
    kpx = 6.0     # px per tf·m
    rows = [("直線鋼腱", c.MLs10 / c.TFM, ORG), ("曲線鋼腱", c.MLc10 / c.TFM, BLUE)]
    b.append(T(80, by - 14, "使用階段可承受的活載彎矩 ML（tf·m，底纖維 U 類控制）", 13, "start", INK, True))
    for i, (nm, v, col) in enumerate(rows):
        y = by + i * 46
        b.append(T(bx0 - 12, y + 20, nm, 13, "end", col, True))
        b.append(R(bx0, y, v * kpx, 28, col, col, 1, op=0.85))
        b.append(T(bx0 + v * kpx + 8, y + 20, f"{v:.2f}", 13, "start", col, True))
    xs, xc = bx0 + c.MLs10 / c.TFM * kpx, bx0 + c.MLc10 / c.TFM * kpx
    b.append(L(xs, by + 82, xc, by + 82, INK, 1.4, marker="f2-ar", mstart="f2-ar"))
    b.append(T((xs + xc) / 2, by + 100, f"ΔM＝{c.dM10:.1f} tf·m＝ηMG（約 +{100 * c.dM10 / (c.MLs10 / c.TFM):.0f}%）", 12.5, "middle", INK, True))
    b.append(L(bx0, by - 4, bx0, by + 78, AX, 1.2))
    b.append(T(80, by + 132, f"題給活載彎矩 ML＝{c.ML10 / c.TFM:.2f} tf·m，兩者都夠；梁端若字面套放寬值 1.6√f'ci（e＝{c.e_str10_end:.2f}），ΔM 只剩 {c.dM10_end:.1f}，但離端 1.2 m 內超限。", 12, "start", AX))
    xg = bx0 + c.ML10 / c.TFM * kpx
    b.append(L(xg, by - 6, xg, by + 80, RED, 1.3, "4 3"))
    b.append(T(xg, by + 116, "題給 ML", 11, "middle", RED))
    return svg(W, H, b, "RC-2010-4 直線與曲線鋼腱的偏心與活載容量比較")


def f3():
    """2015-4 應力翻轉。"""
    W, H = 900, 300
    k = 1.25
    yt, yb = 80, 220
    b = [L(450, 20, 450, 290, "#cfd8dc", 2, "6 5")]
    for side, (title, st) in enumerate([("傳遞階段（F＋自重 MD）", c.st15_tr), ("使用階段（F＋MD＋ML,max）", c.st15_sv)]):
        xo = side * 450
        b.append(T(xo + 225, 36, title, 14, "middle", BLUE2, True))
        sx = xo + 70
        b.append(R(sx, yt, 42, yb - yt, GREY2, GREY, 1.5))
        ycg = (yt + yb) / 2
        b.append(L(sx - 6, ycg, sx + 48, ycg, MUT, 1, "4 3"))
        b.append(C(sx + 21, ycg + c.ep15 * (yb - yt) / 50, 5, BLUE))
        b.append(T(sx + 21, yb + 18, f"ep＝{c.ep15:.2f}", 11.5, "middle", BLUE))
        x0 = xo + 200
        part, xt, xb = stress_diag(x0, yt, yb, st[0], st[1], k)
        b += part
        b.append(L(x0 + 140 * k, yt - 14, x0 + 140 * k, yb + 10, ORG, 1.2, "4 3"))
        b.append(T(x0 + 140 * k, yt - 18, "fca＝140", 11.5, "middle", ORG, True))
        b.append(T(x0 - 6, yt - 18, "fta＝0", 11.5, "end", ORG, True))
        # 應力為 0 的纖維：標籤放在軸線左側，避免壓到應力斜線（2026-11-22）
        for yy, v, nm in ((yt + 16, st[0], "頂"), (yb - 6, st[1], "底")):
            if abs(v) > 0.5:
                b.append(T((xt if nm == "頂" else xb) + 6, yy, f"{nm} {abs(v):.0f}", 12.5, "start", BLUE, True))
            else:
                b.append(T(x0 - 8, yy, f"{nm} 0", 12.5, "end", RED, True))
    b.append(T(450, 276, f"F＝{c.F15 / c.TF:.0f} tf、ep＝{c.ep15:.2f} cm、ML,max＝(fca−fta)S＝{c.ML15 / c.TFM:.1f} tf·m → wL,max＝{c.wL15:.3f} tf/m", 13, "middle", INK, True))
    return svg(W, H, b, "RC-2015-4 最優設計四根纖維同時達限")


def f4():
    """2020-4 跨 AB 鋼腱與弦線下垂量。"""
    W, H = 900, 270
    xA, xB = 90, 810
    ycg = 120
    sc = 2.4          # px per cm（垂直放大）
    eA, eB, eD = 0.0, c.eB20, c.eD20
    # 單跨拋物線通過 A(0,0)、D(L/2,eD)、B(L,eB)
    def e(u):         # u ∈ [0,1]
        # 二次插值
        return eA * (1 - u) * (1 - 2 * u) + eD * 4 * u * (1 - u) + eB * u * (2 * u - 1)
    b = [defs(("f4-ar", RED), ("f4-ub", GRN))]
    b.append(L(xA - 20, ycg, xB + 30, ycg, MUT, 1, "5 4")); b.append(T(xB + 34, ycg + 4, "形心", 11, "start", MUT))
    pts = [(xA + (xB - xA) * i / 120, ycg + e(i / 120) * sc) for i in range(121)]
    b.append(P(pts, "none", BLUE, 2.6, close=False))
    yA, yB = ycg + eA * sc, ycg + eB * sc
    b.append(L(xA, yA, xB, yB, ORG, 1.6, "7 4"))
    xm = (xA + xB) / 2
    ychord = (yA + yB) / 2
    yD = ycg + eD * sc
    b.append(L(xm, ychord, xm, yD, RED, 1.8, marker="f4-ar", mstart="f4-ar"))
    b.append(T(xm + 10, (ychord + yD) / 2 - 10, f"f＝{c.sag20:.0f} cm（從弦量）", 13, "start", RED, True))
    b.append(L(xm - 40, ycg, xm - 40, yD, MUT, 1.2, marker="f4-ar", mstart="f4-ar"))
    b.append(T(xm - 46, (ycg + yD) / 2 + 4, f"eD＝{eD:.1f}（≠ f）", 12, "end", MUT))
    b.append(T(xB - 8, yB - 8, f"B：形心上方 {abs(eB):.0f} cm", 12, "end", BLUE))
    b.append(T(xA + 8, yA - 8, "A：e＝0", 12, "start", BLUE))
    b.append(T((xA + xB) / 2 - 150, ychord - 30, "弦（A、B 兩端連線）", 12, "middle", ORG))
    for i in range(9):
        xx = xA + 40 + i * 80
        b.append(L(xx, 228, xx, 205, GRN, 1.6, marker="f4-ub"))
    b.append(T((xA + xB) / 2, 252, f"等效上揚力 wp＝8Pe·f/L²＝8×{c.Pe20 / c.TF:.1f}×0.35/15²＝{c.wp20 / 10:.2f} tf/m（＝外載 w）", 13, "middle", GRN, True))
    b.append(C(xA, yA, 4, INK)); b.append(C(xB, yB, 4, INK))
    return svg(W, H, b, "RC-2020-4 拋物線鋼腱的弦線下垂量與等效載重")


def f5():
    """2020-4 外載彎矩圖與鋼腱（同一函式）。"""
    W, H = 900, 420
    xA, xC = 70, 830
    L2 = 2 * c.L20
    X = lambda x: xA + x / L2 * (xC - xA)
    ky = 1.7          # px per tf·m
    y_m = 120         # 彎矩圖零線
    y_e = 325         # 鋼腱圖形心線
    ke = 2.2          # px per cm
    b = [defs()]
    b.append(T(xA, 30, "外載彎矩 M(x)（tf·m，正彎矩畫在下方）", 13, "start", INK, True))
    b.append(L(xA, y_m, xC, y_m, AX, 1.2))
    xs = [L2 * i / 300 for i in range(301)]
    pts = [(X(x), y_m + c.M_twospan(x) / c.TFM * ky) for x in xs]
    b.append(P([(X(0), y_m)] + pts + [(X(L2), y_m)], "#e3f2fd", BLUE, 2, op=0.9))
    for x, s in ((c.L20 / 2, "D：+22.5"), (c.L20, "B：−45.0"), (1.5 * c.L20, "E：+22.5")):
        yy = y_m + c.M_twospan(x) / c.TFM * ky
        b.append(C(X(x), yy, 4, BLUE))
        b.append(T(X(x), yy + (18 if c.M_twospan(x) > 0 else -9), s, 12, "middle", BLUE, True))
    for xx in (0, c.L20, L2):
        b.append(P([(X(xx), y_m), (X(xx) - 7, y_m + 12), (X(xx) + 7, y_m + 12)], "#fff", AX, 1.3))
    b.append(T(xA, 200, "鋼腱 e(x)＝M(x)/Pe（cm，形心下方為正），Pe＝45/0.35＝128.6 tf", 13, "start", INK, True))
    b.append(L(xA, y_e, xC, y_e, MUT, 1, "5 4")); b.append(T(xC + 4, y_e + 4, "形心", 11, "start", MUT))
    pts2 = [(X(x), y_e + c.M_twospan(x) / c.Pe20 * ke) for x in xs]
    b.append(P(pts2, "none", RED, 2.6, close=False))
    for x, s in ((c.L20 / 2, "eD＝17.5"), (c.L20, "eB＝−35（形心上方）"), (1.5 * c.L20, "eE＝17.5")):
        yy = y_e + c.M_twospan(x) / c.Pe20 * ke
        b.append(C(X(x), yy, 4, RED))
        b.append(T(X(x), yy + (18 if c.M_twospan(x) > 0 else -9), s, 12, "middle", RED, True))
    b.append(T(X(c.L20 / 2), 410, "15 m", 11.5, "middle", AX)); b.append(T(X(1.5 * c.L20), 410, "15 m", 11.5, "middle", AX))
    return svg(W, H, b, "RC-2020-4 外載彎矩圖與載重平衡鋼腱")


def f6():
    """2024-4 等效載重、三種彎矩、鋼腱與 C 線。"""
    W, H = 900, 690
    xA, xB = 110, 790
    X = lambda x: xA + x / c.L24 * (xB - xA)
    b = [defs(("f6-dn", RED), ("f6-up", GRN), ("f6-mm", PUR))]
    # (a) 自由體
    ya = 95
    b.append(T(30, 30, "(a) 等效載重（作用在混凝土上，自平衡）", 13.5, "start", INK, True))
    b.append(R(xA, ya - 12, xB - xA, 24, GREY2, GREY, 1.3))
    for i in range(10):            # 第一支避開 A 端力矩弧（弧右緣 xA+54）（2026-11-22）
        xx = xA + 61 + i * 62
        b.append(L(xx, ya + 50, xx, ya + 16, GRN, 1.6, marker="f6-up"))
    b.append(T((xA + xB) / 2, ya + 66, f"w＝−Pe″＝{c.wq24:.4f} tf/m 向上（合力 22.0 tf）", 12.5, "middle", GRN, True))
    b.append(L(xA, ya - 58, xA, ya - 16, RED, 2, marker="f6-dn"))
    b.append(T(xA - 6, ya - 40, f"{c.VA_anchor:.1f} tf", 12.5, "end", RED, True))
    b.append(L(xB, ya - 58, xB, ya - 16, RED, 2, marker="f6-dn"))
    b.append(T(xB + 6, ya - 40, f"{c.VB_anchor:.1f} tf", 12.5, "start", RED, True))
    b.append(PATH(f"M {xA+26},{ya-28} A 26 26 0 1 1 {xA+26},{ya+28}", "none", PUR, 1.8))
    b.append(L(xA + 27, ya + 28, xA + 22, ya + 28, PUR, 1.8, marker="f6-mm"))
    b.append(T(xA + 58, ya - 26, f"{c.MA_anchor:.0f} tf·m", 12.5, "start", PUR, True))
    b.append(T(xA, ya + 88, "A 固定端", 11.5, "middle", AX)); b.append(T(xB, ya + 88, "B 輥支承", 11.5, "middle", AX))
    b.append(T(xB, 30, "ΣFy＝22.0−13.5−8.5＝0；ΣMA＝22×6−8.5×12−30＝0", 12, "end", AX))
    # (b) 彎矩
    yb0 = 300
    km = 2.0      # px per tf·m（正彎矩畫在下方）
    b.append(T(30, 205, "(b) 主彎矩 M1＝−Pe、二次彎矩 M2＝RB(L−x)、淨彎矩 M（tf·m，正彎矩畫在下方）", 13.5, "start", INK, True))
    b.append(L(xA, yb0, xB, yb0, AX, 1.2))
    xs = [c.L24 * i / 240 for i in range(241)]
    M1 = lambda x: -c.P24 * c.e24(x) / 100
    b.append(P([(X(x), yb0 + M1(x) * km) for x in xs], "none", BLUE, 2, close=False))
    b.append(P([(X(x), yb0 + c.M2_24(x) * km) for x in xs], "none", RED, 2.4, close=False))
    b.append(P([(X(x), yb0 + (M1(x) + c.M2_24(x)) * km) for x in xs], "none", INK, 1.6, "6 4", close=False))
    b.append(T(X(0) - 6, yb0 + M1(0) * km - 4, "M1(0)＝+30", 11.5, "end", BLUE))
    b.append(T(X(0) - 6, yb0 + (M1(0) + 3) * km + 10, "M＝+33", 11.5, "end", INK))
    b.append(T(X(6), yb0 + M1(6) * km - 8, "M1(6)＝−18、M(6)＝−16.5", 11.5, "middle", BLUE))
    b.append(T(X(3), yb0 + c.M2_24(3) * km + 18, "M2：A 端 3.0 → B 端 0（直線）", 12, "start", RED, True))
    b.append(L(600, 390, 630, 390, BLUE, 2)); b.append(T(636, 394, "M1", 12, "start", BLUE, True))
    b.append(L(680, 390, 710, 390, RED, 2.4)); b.append(T(716, 394, "M2", 12, "start", RED, True))
    b.append(L(760, 390, 790, 390, INK, 1.6, "6 4")); b.append(T(796, 394, "M", 12, "start", INK, True))
    # (c) 鋼腱與 C 線
    yc = 560
    ke = 3.2      # px per cm（形心下方為正，畫在下方）
    b.append(T(30, 445, "(c) 鋼腱 e(x) 與 C 線 eC(x)＝e−M2/P（cm，形心下方為正）", 13.5, "start", INK, True))
    b.append(R(xA, yc - 30 * ke, xB - xA, 60 * ke, "#fafafa", "#cfd8dc", 1))
    b.append(L(xA - 10, yc, xB + 10, yc, MUT, 1, "5 4")); b.append(T(xB + 14, yc + 4, "形心", 11, "start", MUT))
    b.append(P([(X(x), yc + c.e24(x) * ke) for x in xs], "none", BLUE, 2.4, close=False))
    b.append(P([(X(x), yc + c.eC24(x) * ke) for x in xs], "none", RED, 2.2, "7 4", close=False))
    for x, e_, s, col, dy in ((0, c.e24(0), "e＝−25", BLUE, 14), (0, c.eC24(0), "eC＝−27.5", RED, -4),
                              (6, c.e24(6), "e＝+15", BLUE, -8), (6, c.eC24(6), "eC＝+13.75", RED, 18), (12, 0, "0", INK, -8)):
        b.append(C(X(x), yc + e_ * ke, 3.5, col))
        b.append(T(X(x) - (8 if x == 0 else 0), yc + e_ * ke + dy, s, 12, "end" if x == 0 else "middle", col, True))
    b.append(T(xB, yc + 30 * ke + 20, "梁高 60 cm（上下緣 ±30）；C 線在固定端高出鋼腱 M2/P＝2.5 cm，線性遞減到 B 端 0", 11.5, "end", AX))
    return svg(W, H, b, "RC-2024-4 等效載重、主彎矩與二次彎矩、鋼腱與 C 線")


def f7():
    """擺動摩擦損失 1−e^{−Kx}。"""
    W, H = 900, 330
    x0, x1, y0, y1 = 90, 620, 280, 40
    X = lambda x: x0 + x / 30 * (x1 - x0)
    Y = lambda p: y0 - p / 20 * (y0 - y1)
    b = [defs()]
    b.append(L(x0, y0, x1, y0, AX, 1.3)); b.append(L(x0, y0, x0, y1, AX, 1.3))
    for xx in range(0, 31, 5):
        b.append(L(X(xx), y0, X(xx), y0 + 5, AX)); b.append(T(X(xx), y0 + 19, str(xx), 11, "middle", AX))
    for p in range(0, 21, 5):
        b.append(L(x0 - 5, Y(p), x0, Y(p), AX)); b.append(T(x0 - 8, Y(p) + 4, f"{p}%", 11, "end", AX))
    b.append(T((x0 + x1) / 2, y0 + 38, "距張拉端 x（m）", 12.5, "middle", INK))
    b.append(T(40, (y0 + y1) / 2, "損失", 12.5, "middle", INK))
    for K, col in ((0.0016, BLUE), (0.0066, RED)):
        pts = [(X(x), Y((1 - math.exp(-K * x)) * 100)) for x in [30 * i / 150 for i in range(151)]]
        b.append(P(pts, "none", col, 2.4, close=False))
        v = (1 - math.exp(-K * 30)) * 100
        b.append(C(X(30), Y(v), 4.5, col)); b.append(T(X(30) + 8, Y(v) + 4, f"{v:.1f}%", 12.5, "start", col, True))
        v15 = (1 - math.exp(-K * 15)) * 100
        b.append(C(X(15), Y(v15), 3.5, col)); b.append(T(X(15) + 6, Y(v15) - 8, f"{v15:.1f}%", 11.5, "start", col))
    b.append(L(X(15), y0, X(15), y1 + 20, MUT, 1, "4 3"))
    b.append(T(X(15), y1 + 14, "兩端張拉時最遠點", 11, "middle", MUT))
    b.append(L(700, 80, 730, 80, BLUE, 2.4)); b.append(T(736, 84, "K＝0.0016 /m", 12.5, "start", BLUE, True))
    b.append(L(700, 108, 730, 108, RED, 2.4)); b.append(T(736, 112, "K＝0.0066 /m", 12.5, "start", RED, True))
    b += [T(700, 160, "直線鋼腱：α＝0", 12.5, "start", INK, True),
          T(700, 182, "Px＝Pj·e^(−Kx)", 12.5, "start", INK),
          T(700, 214, "先拉法：無套管 → 0", 12.5, "start", GRN, True),
          T(700, 236, "後拉法：擺動摩擦 Kx", 12.5, "start", RED, True)]
    return svg(W, H, b, "直線後拉鋼腱擺動摩擦損失")


def f8():
    """解題決策流程。"""
    W, H = 900, 640
    b = [defs(("f8-ar", AX))]
    def arrow(x1, y1, x2, y2, lab=None, lx=0, ly=0):
        b.append(L(x1, y1, x2, y2, AX, 1.5, marker="f8-ar"))
        if lab:
            b.append(T((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, lab, 12, "middle", RED, True))
    b += box(330, 14, 240, 44, ["讀題：斷面、跨度、Pi／Pe、f'ci／f'c", "支承條件、問什麼"], BLUEL, BLUE, 12)
    arrow(450, 58, 450, 84)
    b += diamond(450, 124, 230, 80, ["超靜定？", "（連續梁、受撐懸臂）"])
    # 左：簡支
    arrow(335, 124, 230, 124, "否", 0, -8)
    b += box(60, 102, 170, 44, ["補假設：單位重、", "容許應力（kgf 制）"], GREY2, GREY, 12)
    arrow(145, 146, 145, 176)
    b += diamond(145, 216, 210, 80, ["問 e 範圍？", "還是最優 F、e？"])
    arrow(145, 256, 145, 296, "e 範圍", 32, 0)
    b += box(40, 296, 210, 58, ["四條不等式（§1）", "拉應力兩條定窗口", "壓應力兩條列出"], GREY2, GREY, 12)
    arrow(250, 216, 300, 216, "最優", 0, -8)
    b += box(300, 190, 150, 58, ["四條同時取等號", "兩兩相加消去 e", "（§3）"], GREY2, GREY, 12)
    arrow(145, 354, 145, 386)
    b += diamond(145, 426, 210, 76, ["比較直線／曲線？"])
    arrow(250, 426, 300, 426, "是", 0, -8)
    b += box(300, 400, 150, 52, ["直線由梁端控制", "曲線多放 MG/Pi（§4）"], GREY2, GREY, 12)
    arrow(145, 464, 145, 560, "否", 18, 0)
    b.append(L(450, 219, 520, 219, AX, 1.5)); arrow(520, 219, 520, 560)
    arrow(375, 452, 375, 560)
    # 右：超靜定
    arrow(565, 124, 650, 124, "是", 0, -8)
    b += box(650, 100, 220, 48, ["拋物線方程（三點擬合）", "e(x)、e′、e″"], GREY2, GREY, 12)
    arrow(760, 148, 760, 176)
    b += box(650, 176, 220, 52, ["等效載重：w＝−Pe″", "＋錨碇力 Pe′、力矩 Pe"], GREY2, GREY, 12)
    arrow(760, 228, 760, 254)
    b += diamond(760, 292, 220, 76, ["自平衡？"])
    b.append(L(650, 292, 615, 292, AX, 1.5)); b.append(L(615, 292, 615, 202, AX, 1.5))
    b.append(L(615, 202, 648, 202, AX, 1.5, marker="f8-ar"))
    b.append(T(606, 250, "否", 12, "end", RED, True)); b.append(T(606, 266, "補錨碇力", 11, "end", RED))
    arrow(760, 330, 760, 358, "是", 14, 0)
    b += box(650, 358, 220, 52, ["相容法或等效載重法", "求二次反力 → M2（直線）"], GREY2, GREY, 12)
    arrow(760, 410, 760, 436)
    b += box(650, 436, 220, 52, ["C 線 eC＝e−M2/P", "同位鋼腱：M2＝0"], GREY2, GREY, 12)
    arrow(760, 488, 760, 560)
    # 收尾
    b += box(80, 560, 740, 60, ["收尾：寫出假設與單位 → 代回應力式／檢查自平衡 → 檢查偏心放得進斷面",
                                "（窗口題代上下限、最優題代四根纖維、C 線題檢查 M2 為直線）"], GRN2, GRN, 12.5)
    return svg(W, H, b, "RC-U4-2 解題決策流程")


FIGS = dict(f0=f0, f1=f1, f2=f2, f3=f3, f4=f4, f5=f5, f6=f6, f7=f7, f8=f8)

if __name__ == "__main__":
    path = sys.argv[1]
    html = open(path, encoding="utf-8").read()
    html = inject(html, {k: fn() for k, fn in FIGS.items()})
    open(path, "w", encoding="utf-8").write(html)
    print("injected", list(FIGS))
