# -*- coding: utf-8 -*-
"""lecture-RC-U3-2 圖解產生器：所有座標由 calcs.py 的數值換算，注入 study/lecture-RC-U3-2.html。
用法（在 RC/ 下）：python3 scripts/lecture-figs/RC-U3-2/gen_figs.py study/lecture-RC-U3-2.html"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from svglib import *          # noqa
import calcs as c             # noqa

F07, F25, F17 = c.F07, c.F25, c.F17


def plan_footing(b, ox, oy, s, F, title):
    """回傳畫布座標換算：基腳中心在 (ox, oy)，s=px/cm。"""
    B = F.B
    b.append(R(ox - B / 2 * s, oy - B / 2 * s, B * s, B * s, "#fafafa", AX, 1.5))
    b.append(R(ox - F.c / 2 * s, oy - F.c / 2 * s, F.c * s, F.c * s, "#90a4ae", INK, 1.4))
    b.append(T(ox, oy - B / 2 * s - 12, title, 13, "middle", INK, True))


def g0():
    """2007-3：單向剪力 vs 穿孔剪力（平面＋斷面）。"""
    W, H = 900, 430
    s = 0.8
    b = [L(450, 20, 450, 420, "#cfd8dc", 2, "6 5")]
    for side in (0, 1):
        ox, oy = 225 + side * 450, 165
        plan_footing(b, ox, oy, s, F07, "單向剪力（梁式）" if side == 0 else "穿孔剪力（雙向）")
        B, cc, d = F07.B, F07.c, F07.d
        if side == 0:
            xcs = ox + (cc / 2 + d) * s
            b.append(R(xcs, oy - B / 2 * s, (B / 2 - cc / 2 - d) * s, B * s, BLUEL, BLUE, 1.2, op=0.9))
            b.append(L(xcs, oy - B / 2 * s - 4, xcs, oy + B / 2 * s + 4, RED, 2.2))
            b.append(T(xcs + 4, oy + B / 2 * s + 18, "距柱面 d＝50", 11.5, "middle", RED, True))
        else:
            hw = (cc + d) / 2 * s
            b.append(R(ox - B / 2 * s, oy - B / 2 * s, B * s, B * s, BLUEL, "none", 0, op=0.9))
            b.append(R(ox - hw, oy - hw, 2 * hw, 2 * hw, "#fafafa", RED, 2.2))
            b.append(R(ox - cc / 2 * s, oy - cc / 2 * s, cc * s, cc * s, "#90a4ae", INK, 1.4))
            b.append(T(ox, oy + hw + 16, "距柱面 d/2，bo＝4(c+d)＝380", 11.5, "middle", RED, True))
        # 斷面
        ys, hh = 318, 60 * s  # 斷面頂、全厚（假設 60 cm，與平面同比例）
        x0, x1 = ox - B / 2 * s, ox + B / 2 * s
        b.append(R(x0, ys, B * s, hh * 1.0, GREY2, GREY, 1.3))
        b.append(R(ox - cc / 2 * s, ys - 26, cc * s, 26, "#90a4ae", INK, 1.2))
        ydb = ys + d * s      # 有效深度處（45° 破壞面水平投影＝d）
        if side == 0:
            xa = ox + cc / 2 * s
            b.append(L(xa, ys, xa + d * s, ydb, RED, 2.4))
        else:
            for sg in (-1, 1):
                xa = ox + sg * cc / 2 * s
                b.append(L(xa + sg * 2, ys, xa + sg * (d * s + 2), ydb, RED, 2.4))
        b.append(T(ox, ys + hh + 14, "斷面（紅線＝45° 破壞面，同比例）", 11, "middle", MUT))
        if side == 0:
            line = f"Vu＝{F07.Vu1 / c.TF:.2f} tf　vs　φVc＝{F07.phiVc1 / c.TF:.2f} tf（現行式）"
        else:
            line = f"Vu＝{F07.Vu2 / c.TF:.2f} tf　vs　φVc＝{F07.phiVc2 / c.TF:.2f} tf（λs＝1）"
        b.append(T(ox, 397, line, 12.5, "middle", INK, True))
        b.append(T(ox, 418, "不足" if side == 0 else "足夠", 13, "middle", RED if side == 0 else GRN, True))
    return svg(W, H, b, "RC-2007-3 單向剪力與穿孔剪力的臨界斷面")


def g1():
    """2025-1 兩種土壓。"""
    W, H = 900, 410
    b = [L(450, 20, 450, 400, "#cfd8dc", 2, "6 5"), defs(("g1-up", BLUE), ("g1-dn", INK))]
    s = 0.9                       # px per cm（水平）
    vs = 1.0                      # px per cm（垂直）
    for side in (0, 1):
        ox = 225 + side * 450
        x0, x1 = ox - 150 * s, ox + 150 * s
        yg = 120                   # 地表
        ybot = yg + 150 * vs      # 基腳底
        ytop = ybot - 60 * vs
        title = "承載力檢核：服務載重＋自重" if side == 0 else "強度設計：因數化淨土壓"
        b.append(T(ox, 34, title, 14, "middle", BLUE2, True))
        b.append(L(x0 - 40, yg, x1 + 40, yg, BROWN, 1.6))
        b.append(T(x1 + 40, yg - 6, "地表", 11, "end", BROWN))
        if side == 0:
            b.append(R(x0, yg, x1 - x0, ytop - yg, BROWN2, "#a1887f", 1, op=0.9))
            b.append(T(x0 + 6, yg + 20, "覆土 0.9 m", 11, "start", BROWN))
        b.append(R(x0, ytop, x1 - x0, ybot - ytop, GREY2, GREY, 1.4))
        b.append(R(ox - 20 * s, yg - 40, 40 * s, ytop - yg + 40, "#90a4ae", INK, 1.2))
        b.append(L(ox, yg - 60, ox, yg - 42, INK, 2, marker="g1-dn"))
        b.append(T(ox + 14, yg - 48, "PD＋PL＝155 tf" if side == 0 else "Pu＝1.2PD＋1.6PL＝216 tf", 12, "start", INK, True))
        b.append(T(x1 + 4, (ytop + ybot) / 2 + 4, "60", 11, "start", MUT))
        q = F25.q_serv * 10 if side == 0 else F25.qu * 10
        kq = 3.0                   # px per tf/m²
        yq = ybot + q * kq
        b.append(R(x0, ybot, x1 - x0, q * kq, BLUEL, BLUE, 1.2, op=0.9))
        for i in range(9):
            xx = x0 + 15 + i * (x1 - x0 - 30) / 8
            b.append(L(xx, yq - 2, xx, ybot + 4, BLUE, 1.3, marker="g1-up"))
        b.append(T(ox, yq + 18, (f"q＝(155＋12.96＋16.20)/9＝{q:.2f} tf/m²" if side == 0 else f"qu＝216/9＝{q:.2f} tf/m²"), 12.5, "middle", BLUE, True))
        b.append(T(ox, yq + 38, ("≤ qa＝25 tf/m²，合格（驗土壤）" if side == 0 else "只用來算彎矩、剪力（驗混凝土）"), 12.5, "middle", GRN if side == 0 else RED, True))
        if side == 1:
            b.append(T(ox, ytop + 34, "基腳與覆土自重＝其土壓反力，互相抵銷", 11.5, "middle", MUT))
    return svg(W, H, b, "RC-2025-1 承載力土壓與因數化淨土壓")


def g2():
    """2007-3 三個臨界斷面平面。"""
    W, H = 900, 360
    s = 0.8
    b = [defs(("g2-ar", AX))]
    B, cc, d = F07.B, F07.c, F07.d
    titles = ["彎矩：柱面", "單向剪力：距柱面 d", "穿孔：距柱面 d/2"]
    for k in range(3):
        ox, oy = 150 + k * 300, 170
        x0, y0 = ox - B / 2 * s, oy - B / 2 * s
        b.append(R(x0, y0, B * s, B * s, "#fafafa", AX, 1.5))
        if k == 0:
            xs = ox + cc / 2 * s
            b.append(R(xs, y0, (B / 2 - cc / 2) * s, B * s, BLUEL, "none", 0, op=0.95))
            b.append(L(xs, y0 - 4, xs, y0 + B * s + 4, RED, 2.2))
            b.append(L(xs, oy + 70, ox + B / 2 * s, oy + 70, AX, 1, marker="g2-ar", mstart="g2-ar"))
            b.append(T((xs + ox + B / 2 * s) / 2, oy + 64, f"L＝{F07.Lc:.1f}", 11.5, "middle", AX, True))
            lab = f"Mu＝qu·B·L²/2＝{F07.Mu / c.TFM:.2f} tf·m"
        elif k == 1:
            xs = ox + (cc / 2 + d) * s
            b.append(R(xs, y0, (B / 2 - cc / 2 - d) * s, B * s, BLUEL, "none", 0, op=0.95))
            b.append(L(xs, y0 - 4, xs, y0 + B * s + 4, RED, 2.2))
            b.append(L(xs, oy + 70, ox + B / 2 * s, oy + 70, AX, 1, marker="g2-ar", mstart="g2-ar"))
            b.append(T((xs + ox + B / 2 * s) / 2, oy + 64, f"{F07.Lc - d:.1f}", 11.5, "middle", AX, True))
            lab = f"Vu＝qu·B·(L−d)＝{F07.Vu1 / c.TF:.2f} tf"
        else:
            hw = (cc + d) / 2 * s
            b.append(R(x0, y0, B * s, B * s, BLUEL, "none", 0, op=0.95))
            b.append(R(ox - hw, oy - hw, 2 * hw, 2 * hw, "#fafafa", RED, 2.2))
            b.append(T(ox, oy + hw + 14, f"{cc + d:.0f}×{cc + d:.0f}", 11.5, "middle", RED, True))
            lab = f"Vu＝Pu−qu(c+d)²＝{F07.Vu2 / c.TF:.2f} tf"
        b.append(R(ox - cc / 2 * s, oy - cc / 2 * s, cc * s, cc * s, "#90a4ae", INK, 1.4))
        b.append(T(ox, y0 - 12, titles[k], 13, "middle", INK, True))
        b.append(T(ox, y0 + B * s + 22, lab, 12, "middle", BLUE2, True))
    b.append(T(450, 348, f"qu＝{F07.qu * 10:.2f} tf/m²；藍色＝造成該需求的土壓面積；基腳 300×300、柱 45×45、d＝50 cm", 12, "middle", AX))
    return svg(W, H, b, "RC-2007-3 三個臨界斷面")


def g3():
    """單向剪力 vc 與 ρw。"""
    W, H = 900, 380
    x0, x1, y0, y1 = 90, 620, 330, 40
    rmax = 2.0      # %
    X = lambda r: x0 + r / rmax * (x1 - x0)
    Y = lambda v: y0 - v / 0.7 * (y0 - y1)
    b = [defs()]
    b.append(L(x0, y0, x1, y0, AX, 1.3)); b.append(L(x0, y0, x0, y1, AX, 1.3))
    for r in [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]:
        b.append(L(X(r), y0, X(r), y0 + 5, AX)); b.append(T(X(r), y0 + 19, f"{r:g}", 11, "middle", AX))
    for v in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
        b.append(L(x0 - 5, Y(v), x0, Y(v), AX)); b.append(T(x0 - 8, Y(v) + 4, f"{v:.1f}", 11, "end", AX))
    b.append(T((x0 + x1) / 2, y0 + 38, "縱向鋼筋比 ρw（%）", 12.5, "middle", INK))
    b.append(T(40, (y0 + y1) / 2 - 10, "vc", 13, "middle", INK, True))
    b.append(T(40, (y0 + y1) / 2 + 8, "＝Vc/(√f'c·bw·d)", 10.5, "middle", MUT))
    b.append(L(X(0), Y(0.53), X(rmax), Y(0.53), GREY, 2.2, "8 4"))
    pts = [(X(r), Y(2.12 * (r / 100) ** (1 / 3))) for r in [rmax * i / 200 for i in range(1, 201)]]
    b.append(P(pts, "none", BLUE, 2.6, close=False))
    rc = 0.25 ** 3 * 100
    b.append(C(X(rc), Y(0.53), 4, INK)); b.append(T(X(rc), Y(0.53) - 10, f"交點 ρw＝{rc:.2f}%", 11.5, "middle", INK))
    for F, nm, col, dy in ((F07, "2007-3", RED, -1), (F17, "2017-3", ORG, 1)):
        r = F.rho_w * 100
        vcap = 2.12 * F.rho_w ** (1 / 3)
        vneed = F.Vu1 / (0.75 * math.sqrt(F.fc) * F.B * F.d)
        b.append(L(X(r), Y(vcap), X(r), Y(0.53), col, 1, "3 3"))
        b.append(C(X(r), Y(vcap), 4.5, col))
        b.append(P([(X(r) - 5, Y(vneed) - 5), (X(r) + 5, Y(vneed) + 5)], "none", col, 2.2, close=False))
        b.append(P([(X(r) - 5, Y(vneed) + 5), (X(r) + 5, Y(vneed) - 5)], "none", col, 2.2, close=False))
        lx, ly = X(0.62), (Y(0.43) if dy < 0 else Y(0.17))
        b.append(L(X(r) + 6, Y(vneed), lx - 4, ly - 4, col, 0.9, "2 2"))
        b.append(T(lx, ly, f"{nm}（ρw＝{r:.2f}%）", 12, "start", col, True))
        b.append(T(lx, ly + 17, f"需求 {vneed:.3f} ＞ 強度 {vcap:.3f}（舊式 0.53）", 11.5, "start", col))
    b.append(L(650, 70, 680, 70, GREY, 2.2, "8 4")); b.append(T(686, 74, "舊式 0.53", 12.5, "start", GREY, True))
    b.append(L(650, 96, 680, 96, BLUE, 2.6)); b.append(T(686, 100, "現行 2.12·ρw^(1/3)", 12.5, "start", BLUE, True))
    b.append(C(665, 126, 4.5, INK)); b.append(T(686, 130, "強度（現行式）", 12, "start", INK))
    b.append(P([(660, 147), (670, 157)], "none", INK, 2, close=False)); b.append(P([(660, 157), (670, 147)], "none", INK, 2, close=False))
    b.append(T(686, 157, "需求 Vu/(φ√f'c·bw·d)", 12, "start", INK))
    b += [T(650, 200, "兩題需求都在兩線之間：", 12.5, "start", INK, True),
          T(650, 222, "舊式判「足夠」", 12.5, "start", GREY),
          T(650, 244, "現行式判「不足」", 12.5, "start", RED, True),
          T(650, 280, "基腳 λs＝1、λ＝1", 12, "start", MUT)]
    return svg(W, H, b, "單向剪力強度係數與縱向鋼筋比")


def g4():
    """(a) 穿孔三式 vs bo/d；(b) λs vs d。"""
    W, H = 900, 380
    b = [defs(), L(470, 20, 470, 370, "#cfd8dc", 2, "6 5")]
    # (a)
    x0, x1, y0, y1 = 70, 440, 320, 60
    rmax = 30
    X = lambda r: x0 + r / rmax * (x1 - x0)
    Y = lambda v: y0 - (v - 0.6) / (1.8 - 0.6) * (y0 - y1)
    b.append(T(30, 36, "(a) 方柱 β＝1 的係數 κ 與 bo/d", 13.5, "start", INK, True))
    b.append(L(x0, y0, x1, y0, AX, 1.3)); b.append(L(x0, y0, x0, y1, AX, 1.3))
    for r in range(0, 31, 5):
        b.append(L(X(r), y0, X(r), y0 + 5, AX)); b.append(T(X(r), y0 + 19, str(r), 11, "middle", AX))
    for v in (0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8):
        b.append(L(x0 - 5, Y(v), x0, Y(v), AX)); b.append(T(x0 - 8, Y(v) + 4, f"{v:.1f}", 11, "end", AX))
    b.append(T((x0 + x1) / 2, y0 + 38, "bo/d", 12.5, "middle", INK))
    b.append(L(X(0), Y(1.59), X(rmax), Y(1.59), GREY, 1.6, "6 4")); b.append(T(X(20), Y(1.59) + 15, "0.53(1+2/β)＝1.59", 11, "start", GREY))
    b.append(L(X(0), Y(1.06), X(rmax), Y(1.06), INK, 2)); b.append(T(X(rmax), Y(1.06) - 6, "1.06", 11.5, "end", INK, True))
    for a_s, col in ((40, BLUE), (20, PUR)):
        pts = [(X(r), Y(0.265 * (2 + a_s / r))) for r in [2 + (rmax - 2) * i / 200 for i in range(201)]
               if 0.6 <= 0.265 * (2 + a_s / r) <= 1.8]
        b.append(P(pts, "none", col, 2.2, close=False))
        rr = a_s / 2
        b.append(C(X(rr), Y(1.06), 3.5, col)); b.append(T(X(rr), Y(1.06) + 16, f"αs＝{a_s}：{rr:.0f}", 11, "middle", col, True))
    pts_q = [("07", F07.bo / F07.d), ("17", F17.bo / F17.d), ("20", c.bo20 / c.d20), ("21柱", c.bo_col21 / c.d21),
             ("21角樁", c.bo_pile21 / c.d21), ("25", F25.bo / F25.d)]
    for i, (nm, r) in enumerate(pts_q):
        b.append(C(X(r), Y(1.06), 4, RED))
    b.append(T(x0 + 150, y1 + 4, "紅點：本單元檢核點，全落在 1.06", 11, "start", RED, True))
    lst = "、".join(f"{nm} {r:.1f}" for nm, r in sorted(pts_q, key=lambda t: t[1]))
    b.append(T(x0 + 150, y1 + 20, "bo/d：" + lst.replace("21角樁", "21角樁").split("、")[0] + "、" + "、".join(lst.split("、")[1:3]), 10.5, "start", RED))
    b.append(T(x0 + 150, y1 + 35, "、".join(lst.split("、")[3:]), 10.5, "start", RED))
    # (b)
    x0, x1, y0, y1 = 530, 870, 320, 60
    X2 = lambda d: x0 + d / 100 * (x1 - x0)
    Y2 = lambda v: y0 - (v - 0.5) / 0.55 * (y0 - y1)
    b.append(T(500, 36, "(b) 尺寸效應 λs＝√(2/(1+0.04d))，d 以 cm 計", 13.5, "start", INK, True))
    b.append(L(x0, y0, x1, y0, AX, 1.3)); b.append(L(x0, y0, x0, y1, AX, 1.3))
    for d in range(0, 101, 20):
        b.append(L(X2(d), y0, X2(d), y0 + 5, AX)); b.append(T(X2(d), y0 + 19, str(d), 11, "middle", AX))
    for v in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
        b.append(L(x0 - 5, Y2(v), x0, Y2(v), AX)); b.append(T(x0 - 8, Y2(v) + 4, f"{v:.1f}", 11, "end", AX))
    b.append(T((x0 + x1) / 2, y0 + 38, "有效深度 d（cm）", 12.5, "middle", INK))
    b.append(R(x0, Y2(1.0) - 4, x1 - x0, 8, GRN2, "none", 0, op=0.9))
    b.append(T(x1 - 4, Y2(1.0) - 8, "獨立基腳可取 1（13.2.6.2）", 11, "end", GRN, True))
    pts = [(X2(d), Y2(c.lam_s(d))) for d in [100 * i / 200 for i in range(201)]]
    b.append(P(pts, "none", BLUE, 2.4, close=False))
    for d, nm in ((35, "2020-3 樓版"), (45, "2021-3 樁帽"), (50, "2007/2025 基腳")):
        v = c.lam_s(d)
        # 標籤放在曲線左下方（曲線往右下降，右側標籤會壓到曲線）（2026-11-22）
        b.append(C(X2(d), Y2(v), 4, RED)); b.append(T(X2(d) - 8, Y2(v) + (34 if d == 50 else 16), f"{nm} {v:.3f}", 11, "end", RED, True))
    b.append(T(X2(23), Y2(1.0) + 22, "d ≤ 25：λs＝1", 11, "end", MUT))   # 放在折點左側，避開下降段
    return svg(W, H, b, "穿孔三式係數與尺寸效應")


def g5():
    """2020-3 平面＋長條。"""
    W, H = 900, 400
    b = [defs()]
    s = 0.33                       # px per cm
    ox, oy = 210, 205
    Lx, Ly = 800, 900
    b.append(R(ox - Lx / 2 * s, oy - Ly / 2 * s, Lx * s, Ly * s, BLUEL, BLUE, 1.2, dash="5 4", op=0.9))
    b.append(T(ox, oy - Ly / 2 * s - 8, "從屬面積 8 m × 9 m", 12, "middle", BLUE, True))
    hw = (c.c20 + c.d20) / 2 * s
    b.append(R(ox - hw, oy - hw, 2 * hw, 2 * hw, "#fafafa", RED, 2))
    b.append(R(ox - c.c20 / 2 * s, oy - c.c20 / 2 * s, c.c20 * s, c.c20 * s, "#90a4ae", INK, 1.3))
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        for k in range(1, 9):
            r = (c.c20 / 2 + 5 * k) * s
            px, py = ox + dx * r, oy + dy * r
            if dx:
                b.append(L(px, py - 12, px, py + 12, ORG, 1.6))
            else:
                b.append(L(px - 12, py, px + 12, py, ORG, 1.6))
    b.append(T(ox + hw + 6, oy - hw - 6, "bo＝4×135＝540", 11.5, "start", RED, True))
    b.append(T(ox, oy + Ly / 2 * s + 18, "柱 100×100；橘線＝剪力筋（四條、每條雙肢、s＝5）", 11.5, "middle", AX))
    # 長條
    bx0, by = 520, 80
    k = 0.85
    rows = [("Vu", c.Vu20 / c.TF, INK), ("φVc（無剪力筋）", c.phiVc20 / c.TF, RED),
            ("φ(Vc′＋Vs)，s＝5.37", c.Vu20 / c.TF, GRN), ("φVn,max＝0.75×1.59√f'c·bo·d", c.phiVnmax20 / c.TF, GREY)]
    b.append(T(bx0 - 120, 50, "需求與強度（tf）", 13, "start", INK, True))
    for i, (nm, v, col) in enumerate(rows):
        y = by + i * 62
        b.append(T(bx0 - 120, y + 12, nm, 12, "start", col, True))
        b.append(R(bx0 - 120, y + 20, v * k, 22, col, col, 1, op=0.8))
        b.append(T(bx0 - 120 + v * k + 6, y + 36, f"{v:.2f}", 12.5, "start", col, True))
    b.append(T(bx0 - 120, by + 4 * 62 + 14, "Vc′＝0.53·λs·√f'c·bo·d＝153.01；Vs＝277.41 tf", 12, "start", AX))
    b.append(T(bx0 - 120, by + 4 * 62 + 36, "λs＝√(2/2.4)＝0.9129（樓版要乘）", 12, "start", AX))
    return svg(W, H, b, "RC-2020-3 無梁版內柱穿孔與剪力筋")


def g6():
    """2021-3 樁帽平面＋樁力 vs e。"""
    W, H = 900, 400
    b = [defs()]
    s = 1.05
    ox, oy = 200, 205
    Bc = 260
    b.append(R(ox - Bc / 2 * s, oy - Bc / 2 * s, Bc * s, Bc * s, "#fafafa", AX, 1.5))
    b.append(T(ox, oy - Bc / 2 * s - 10, "樁帽 260×260、D＝55、d＝45 cm", 12, "middle", INK, True))
    hw = (50 + c.d21) / 2 * s
    b.append(R(ox - hw, oy - hw, 2 * hw, 2 * hw, "none", RED, 2))
    b.append(R(ox - 25 * s, oy - 25 * s, 50 * s, 50 * s, "#90a4ae", INK, 1.3))
    for sx in (-1, 1):
        for sy in (-1, 1):
            b.append(C(ox + sx * 90 * s, oy + sy * 90 * s, 15 * s, "#cfd8dc", INK, 1.2))
    # 角隅樁臨界周長（右上樁：兩段直線到帽緣 + 四分之一圓弧，半徑 15+22.5）
    rr = (15 + c.d21 / 2) * s
    px, py = ox + 90 * s, oy - 90 * s
    edgeX, edgeY = ox + Bc / 2 * s, oy - Bc / 2 * s
    b.append(PATH(f"M {px - rr:.1f},{edgeY:.1f} L {px - rr:.1f},{py:.1f} A {rr:.1f} {rr:.1f} 0 0 0 {px:.1f},{py + rr:.1f} L {edgeX:.1f},{py + rr:.1f}",
                  "none", PUR, 2.2))
    b.append(T(ox + hw + 4, oy + 4, "柱周 bo＝380", 11.5, "start", RED, True))
    b.append(T(px - rr - 6, edgeY + 16, "角隅樁 bo＝138.9", 11.5, "end", PUR, True))
    b.append(T(px - rr - 6, edgeY + 31, "（2×40＋π×37.5/2）", 10.5, "end", PUR))
    b.append(T(ox, oy + Bc / 2 * s + 20, "樁徑 30、樁心 ±90 cm（距帽緣 40）", 11.5, "middle", AX))
    # 右：樁力
    x0, x1, y0, y1 = 470, 860, 330, 60
    emax = 140
    X = lambda e: x0 + e / emax * (x1 - x0)
    Y = lambda p: y0 - (p + 20) / 70 * (y0 - y1)
    b.append(L(x0, y0, x1, y0, AX, 1.3)); b.append(L(x0, y0, x0, y1, AX, 1.3))
    for e in range(0, 141, 20):
        b.append(L(X(e), y0, X(e), y0 + 5, AX)); b.append(T(X(e), y0 + 19, str(e), 11, "middle", AX))
    for p in range(-20, 51, 10):
        b.append(L(x0 - 5, Y(p), x0, Y(p), AX)); b.append(T(x0 - 8, Y(p) + 4, str(p), 11, "end", AX))
    b.append(T((x0 + x1) / 2, y0 + 38, "偏心距 ex（cm）", 12.5, "middle", INK))
    b.append(T(x0, y1 - 14, "樁力（tf，壓為正）", 12, "start", INK, True))
    b.append(L(x0, Y(0), x1, Y(0), MUT, 1, "3 3"))
    b.append(L(X(0), Y(25), X(90), Y(50), BLUE, 2.4))
    b.append(L(X(0), Y(25), X(emax), Y(25 - emax / 3.6), ORG, 2.4))
    b.append(L(x0, Y(40), x1, Y(40), RED, 1.4, "6 4")); b.append(T(x1, Y(40) - 6, "承壓 40", 11.5, "end", RED, True))
    b.append(L(x0, Y(-10), x1, Y(-10), RED, 1.4, "6 4")); b.append(T(X(100), Y(-10) + 16, "承拉 −10", 11.5, "end", RED, True))
    b.append(C(X(c.e_Pc21), Y(40), 5, RED)); b.append(T(X(c.e_Pc21) - 6, Y(40) - 10, f"ex＝{c.e_Pc21:.0f}（控制）", 12, "end", RED, True))
    b.append(C(X(c.e_Pt21), Y(-10), 4, ORG)); b.append(T(X(c.e_Pt21), Y(-10) - 10, f"{c.e_Pt21:.0f}", 11.5, "middle", ORG, True))
    b.append(T(X(80) + 8, Y(25 + 80 / 3.6) + 8, "Pmax＝25＋ex/3.6", 12, "start", BLUE, True))
    b.append(T(X(40), Y(25 - 40 / 3.6) + 26, "Pmin＝25−ex/3.6", 12, "middle", ORG, True))
    return svg(W, H, b, "RC-2021-3 樁帽臨界周長與樁力")


def g7():
    """單向版彎矩係數。"""
    W, H = 900, 330
    b = [defs()]
    x0, Ls = 60, 260          # 每跨 px
    ybase = 170
    k = 1400                  # px per 係數
    sup = [x0 + i * Ls for i in range(4)]
    b.append(L(sup[0], ybase, sup[3] + 20, ybase, AX, 3))
    b.append(T(sup[3] + 26, ybase + 4, "…", 14, "start", AX))
    for i, xs in enumerate(sup):
        b.append(R(xs - 10, ybase + 2, 20, 50, "#cfd8dc", GREY, 1))
    b.append(T(sup[0], ybase + 70, "外支承（邊梁）", 11.5, "middle", AX))
    b.append(T(sup[1], ybase + 70, "第一內支承", 11.5, "middle", AX))
    b.append(T(sup[2], ybase + 70, "內支承", 11.5, "middle", AX))
    b.append(T((sup[0] + sup[1]) / 2, ybase + 90, "外跨", 12, "middle", INK, True))
    b.append(T((sup[1] + sup[2]) / 2, ybase + 90, "內跨", 12, "middle", INK, True))
    b.append(T((sup[2] + sup[3]) / 2, ybase + 90, "內跨", 12, "middle", INK, True))
    items = [(sup[0] + 18, -1 / 24, "−1/24"), ((sup[0] + sup[1]) / 2, 1 / 14, "+1/14"), (sup[1] - 18, -1 / 10, "−1/10"),
             (sup[1] + 18, -1 / 11, "−1/11"), ((sup[1] + sup[2]) / 2, 1 / 16, "+1/16"), (sup[2] - 18, -1 / 11, "−1/11"),
             (sup[2] + 18, -1 / 11, "−1/11"), ((sup[2] + sup[3]) / 2, 1 / 16, "+1/16")]
    for x, v, s in items:
        hgt = abs(v) * k
        col = RED if v < 0 else BLUE
        if v < 0:
            b.append(R(x - 9, ybase - hgt, 18, hgt, RED2, RED, 1.2))
            b.append(T(x, ybase - hgt - 8, s, 12, "middle", RED, True))
        else:
            b.append(R(x - 9, ybase - hgt, 18, hgt, BLUEL, BLUE, 1.2))
            b.append(T(x, ybase - hgt - 8, s, 12, "middle", BLUE, True))
    b.append(R(sup[0] + 4, ybase - 1 / 24 * k - 30, 36, 1 / 24 * k + 32, "none", ORG, 1.6, dash="4 3"))
    b.append(T(sup[0] + 46, ybase - 1 / 24 * k - 18, "2013-1 問這裡 → 最少鋼筋控制", 12, "start", ORG, True))
    b.append(T(450, 310, "Mu＝Cm·wu·ℓn²；紅＝負彎矩（版頂受拉）、藍＝正彎矩；支承為柱時外支承改 −1/16", 12, "middle", AX))
    return svg(W, H, b, "多跨連續單向版彎矩係數")


def g8():
    """雙向版外角隅配筋：版頂、版底。"""
    W, H = 900, 380
    b = [defs(("g8-ar", AX))]
    for side in (0, 1):
        ox = 60 + side * 450
        oy = 60
        S = 290              # 版格示意（長跨 ℓ → 290 px）
        b.append(R(ox, oy, S, S * 0.8, "#fafafa", "#b0bec5", 1, dash="5 4"))
        b.append(L(ox, oy, ox + S, oy, INK, 6)); b.append(L(ox, oy, ox, oy + S * 0.8, INK, 6))
        z = S / 5
        b.append(R(ox, oy, z * 1.0 + 0, z, ORG2, ORG, 1.2, op=0.9))
        b.append(R(ox, oy, z, z, ORG2, ORG, 1.6))
        # 對角線
        b.append(L(ox, oy, ox + z * 1.6, oy + z * 1.6, MUT, 1, "4 3"))
        # 用參數化直線畫鋼筋：頂層方向 (1,1)，底層方向 (1,-1)，裁切在 z×z 方塊內
        def clip_lines(dx, dy, col):
            for j in range(-6, 7):
                off = j * z / 7
                # 直線：通過 (cx+off·n) 方向 (dx,dy)，n 為法向
                nx, ny = -dy / math.hypot(dx, dy), dx / math.hypot(dx, dy)
                cx, cy = ox + z / 2 + nx * off, oy + z / 2 + ny * off
                ts = []
                for (px, py, qx, qy) in ((ox, oy, ox + z, oy), (ox + z, oy, ox + z, oy + z),
                                          (ox + z, oy + z, ox, oy + z), (ox, oy + z, ox, oy)):
                    # 與邊求交
                    ex, ey = qx - px, qy - py
                    den = dx * ey - dy * ex
                    if abs(den) < 1e-9:
                        continue
                    tt = ((px - cx) * ey - (py - cy) * ex) / den
                    uu = ((px - cx) * dy - (py - cy) * dx) / den
                    if -1e-9 <= uu <= 1 + 1e-9:
                        ts.append(tt)
                if len(ts) >= 2:
                    t1, t2 = min(ts), max(ts)
                    if t2 - t1 > 2:
                        b.append(L(cx + dx * t1, cy + dy * t1, cx + dx * t2, cy + dy * t2, col, 2))
        def cracks(dx, dy, col):
            for j in (-2, -1, 0, 1, 2):
                nx, ny = -dy / math.hypot(dx, dy), dx / math.hypot(dx, dy)
                cx, cy = ox + z * 0.5 + 1.0 * z * 0.5 + nx * j * 14, oy + z * 1.0 + ny * j * 14
                b.append(L(cx - dx * 16, cy - dy * 16, cx + dx * 16, cy + dy * 16, col, 1.4, "3 2"))
        if side == 0:
            clip_lines(1, 1, BLUE)
            ttl = "版頂：沿對角線受拉"
            note1, note2 = "裂縫垂直對角線（紅虛線）", "鋼筋平行對角線（藍）"
            cracks(-1, 1, RED)
        else:
            clip_lines(1, -1, BLUE)
            ttl = "版底：垂直對角線受拉"
            note1, note2 = "裂縫平行對角線（紅虛線）", "鋼筋垂直對角線（藍）"
            cracks(1, 1, RED)
        b.append(T(ox + S / 2, 36, ttl, 14, "middle", BLUE2, True))
        b.append(L(ox, oy + z + 14, ox + z, oy + z + 14, AX, 1, marker="g8-ar", mstart="g8-ar"))
        b.append(T(ox + z / 2, oy + z + 30, "ℓ/5", 12, "middle", AX, True))
        b.append(T(ox + z + 8, oy + z / 2 + 4, "ℓ＝長跨", 11.5, "start", AX))
        b.append(T(ox + S / 2 + 40, oy + S * 0.8 - 40, note1, 12, "middle", RED, True))
        b.append(T(ox + S / 2 + 40, oy + S * 0.8 - 18, note2, 12, "middle", BLUE, True))
        b.append(T(ox - 4, oy - 8, "邊梁", 11, "start", INK))
    b.append(T(450, 366, "外角隅（邊牆或 αf＞1.0 邊梁支承）；頂、底層鋼筋量＝最大正彎矩鋼筋；亦可頂底各配兩層平行版邊鋼筋", 12, "middle", AX))
    return svg(W, H, b, "雙向版外角隅特殊配筋")


def g9():
    """解題決策流程。"""
    W, H = 900, 690
    b = [defs(("g9-ar", AX))]
    def arrow(x1, y1, x2, y2, lab=None, lx=0, ly=-8):
        b.append(L(x1, y1, x2, y2, AX, 1.5, marker="g9-ar"))
        if lab:
            b.append(T((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, lab, 12, "middle", RED, True))
    b += box(320, 12, 260, 44, ["讀題：構件型式、尺寸、載重", "（是否已因數化）、問什麼"], BLUEL, BLUE, 12)
    arrow(450, 56, 450, 80)
    b += diamond(450, 118, 220, 76, ["構件？"])
    # 左：獨立基腳（欄中心 x=150）
    b.append(L(340, 118, 150, 118, AX, 1.5)); arrow(150, 118, 150, 140)
    b.append(T(245, 110, "獨立基腳", 12, "middle", RED, True))
    b += box(40, 140, 220, 46, ["補假設：全厚、保護層、", "fy、單位重"], GREY2, GREY, 12)
    arrow(150, 186, 150, 206)
    b += box(40, 206, 220, 46, ["承載力（服務載重＋自重）", "q ≤ qa"], GREY2, GREY, 12)
    arrow(150, 252, 150, 272)
    b += box(40, 272, 220, 46, ["qu＝Pu/A（不含自重）", "柱面 Mu、0.0018Ag"], GREY2, GREY, 12)
    arrow(150, 318, 150, 338)
    b += box(30, 338, 240, 56, ["單向剪力：距柱面 d", "Vc＝2.12λsλρw^(1/3)√f'c·bw·d", "（考卷印舊式也要換）"], GREY2, GREY, 11.5)
    arrow(150, 394, 150, 414)
    b += box(40, 414, 220, 46, ["穿孔：bo＝4(c+d)", "Vu＝Pu−qu(c+d)²"], GREY2, GREY, 12)
    arrow(150, 460, 150, 500)
    # 中：版柱／樁帽（欄中心 x=450）
    arrow(450, 156, 450, 186, "版柱／樁帽", 46, 0)
    b += box(340, 186, 220, 46, ["樁帽：Pi＝P/n ± P·e·x/Σx²", "版：Vu＝wu[ℓxℓy−(c+d)²]"], GREY2, GREY, 11.5)
    arrow(450, 232, 450, 256)
    b += box(340, 256, 220, 46, ["柱周 αs＝40", "邊柱 30、角柱／角隅樁 20"], GREY2, GREY, 12)
    arrow(450, 302, 450, 500)
    # 穿孔三式（左右兩支分別進左右頂點）
    b += diamond(300, 500, 300, 76, ["三式取小 κ；λs 取多少？", "基腳可取 1；版、樁帽要乘"], ORG2, ORG, 11.5)
    arrow(300, 538, 300, 556)
    b += diamond(300, 584, 200, 56, ["φVc ≥ Vu？"], ORG2, ORG, 12)
    arrow(400, 584, 470, 584, "否", 0, -8)
    b += box(470, 560, 150, 48, ["配剪力筋：Vc′ 減半", "Vs＝Av·fyt·d/s"], GREY2, GREY, 11.5)
    arrow(300, 612, 300, 630, "是", 14, 4)
    arrow(545, 608, 545, 630)
    # 右：樓版
    b.append(L(560, 118, 765, 118, AX, 1.5)); arrow(765, 118, 765, 140)
    b.append(T(660, 110, "樓版", 12, "middle", RED, True))
    b += box(650, 140, 230, 52, ["單向版：版厚表（ℓ/24 等）", "係數 Cm·wu·ℓn²、0.0018Ag"], GREY2, GREY, 11.5)
    arrow(765, 192, 765, 214)
    b += box(650, 214, 230, 46, ["雙向版角隅：長跨 1/5", "頂底兩層、量＝最大正彎矩筋"], GREY2, GREY, 11.5)
    arrow(765, 260, 765, 282)
    b += box(650, 282, 230, 46, ["橫膈版：Vn＝(0.53√f'c＋ρt·fy)Acv", "撓曲筋＋抗剪筋合計"], GREY2, GREY, 11.5)
    arrow(765, 328, 765, 630)
    b += box(40, 630, 840, 48, ["收尾：每一項寫「需求 vs 強度 → 合格／不合格」，列出所有假設與 λs 取值；", "考卷印舊式時附舊式對照值"], GRN2, GRN, 12)
    return svg(W, H, b, "RC-U3-2 解題決策流程")


FIGS = dict(g0=g0, g1=g1, g2=g2, g3=g3, g4=g4, g5=g5, g6=g6, g7=g7, g8=g8, g9=g9)

if __name__ == "__main__":
    path = sys.argv[1]
    html = open(path, encoding="utf-8").read()
    html = inject(html, {k: fn() for k, fn in FIGS.items()})
    open(path, "w", encoding="utf-8").write(html)
    print("injected", list(FIGS))
