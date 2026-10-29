# -*- coding: utf-8 -*-
"""lecture-SS-U1-3 觀念講義圖解產生器。
所有曲線、座標、標註數值都由公式或 calcs.py 算出；改輸入重跑，圖會跟著變。
用法：python3 gen_figs.py [輸出資料夾，預設為本資料夾]   → 產生 fig-*.svg；再跑 refresh_figs.py 內嵌回講義
"""
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import SVG, Axes, COL
from calcs import R, B1_aisc, B1_tw
import frame2d

OUT = sys.argv[1] if (__name__ == "__main__" and len(sys.argv) > 1) else os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)
FIGS = {}


def f2(v, n=2):
    return f"{v:.{n}f}"


# ════════════════════════════════════════════════════════════════
# 圖 0-1　P 與 δ 互餵：幾何級數收斂
# ════════════════════════════════════════════════════════════════
def fig_0_1():
    sv = SVG(900, 370)
    sv.line(330, 12, 330, 355, COL["lgray"], 2, "7,5")
    # 左：柱
    sv.text(165, 30, "柱 或 梁（U1-1／U1-2）", 16, COL["ten"], weight="700")
    top, bot, xc = 100, 228, 80
    sv.pin(xc, bot)
    sv.line(xc, top, xc, bot, COL["ten"], 7, cap="butt")
    sv.arrow(xc, top - 34, xc, top - 2, COL["dk"], 3)
    sv.text(xc, top - 40, "$P$", 14, COL["dk"], weight="700")
    ys = np.linspace(top, bot, 41)
    sv.poly([(xc + 22 * math.sin(math.pi * (y - top) / (bot - top)), y) for y in ys], COL["comp"], 2, "4,3")
    sv.text(xc + 30, (top + bot) / 2 + 4, "挫屈模態", 11.5, COL["comp"], "start")
    sv.text(xc, bot + 38, "$P$ 小於 $P_{cr}$ 時 $δ$ = 0", 12.5, COL["ink"])
    sv.text(xc, bot + 56, "沒有外加彎矩", 12.5, COL["ink"])
    # 左：梁（簡支 UDL 精確撓曲 x(L^3-2Lx^2+x^3)）
    x0, x1, yb = 195, 305, 140
    sv.line(x0, yb, x1, yb, COL["ten"], 7, cap="butt")
    sv.pin(x0, yb + 4, s=8); sv.roller(x1, yb + 4, s=8)
    for i in range(6):
        xx = x0 + 8 + (x1 - x0 - 16) * i / 5
        sv.arrow(xx, yb - 34, xx, yb - 5, COL["dk"], 1.6, 7)
    sv.line(x0 + 8, yb - 34, x1 - 8, yb - 34, COL["dk"], 1.6)
    sv.text((x0 + x1) / 2, yb - 42, "$w$", 14, COL["dk"], weight="700")
    xs = np.linspace(0, 1, 41)
    defl = xs * (1 - 2 * xs ** 2 + xs ** 3) / (5 / 16 * 0.5)  # 正規化至跨中=1
    sv.poly([(x0 + (x1 - x0) * x, yb + 22 * d) for x, d in zip(xs, defl / defl.max())], COL["comp"], 2, "4,3")
    sv.text((x0 + x1) / 2, yb + 52, "$δ$", 13, COL["comp"], weight="700")
    sv.text((x0 + x1) / 2, bot + 38, "有 $δ$，但沒有 $P$", 12.5, COL["ink"])
    sv.text((x0 + x1) / 2, bot + 56, "$P·δ$ = 0", 12.5, COL["ink"])
    sv.text(165, 318, "內力算一次就定案", 15, COL["ten_d"], weight="700")
    sv.text(165, 340, "一階分析 = 最終答案", 12.5, COL["sub"])

    # 右：梁柱，δ_n = δ_1 (1-α^n)/(1-α)
    alpha = 0.4
    sv.text(615, 30, "梁柱（U1-3）＝ $P$ 與 $δ$ 同時存在", 16, COL["comp"], weight="700")
    top, bot, xc = 72, 252, 410
    sv.pin(xc, bot)
    sv.arrow(xc, top - 34, xc, top - 2, COL["dk"], 3)
    sv.text(xc, top - 40, "$P$", 14, COL["dk"], weight="700")
    sv.moment(xc - 26, top + 14, 13, True, COL["warn"]); sv.text(xc - 44, top + 18, "$M$", 13, COL["warn"], "end", "700")
    d1 = 34.0
    seq = [d1 * (1 - alpha ** n) / (1 - alpha) for n in (1, 2, 3)]
    dinf = d1 / (1 - alpha)
    cols = [COL["warn"], COL["comp"], "#d84315"]
    ys = np.linspace(top, bot, 61)
    sv.line(xc, top, xc, bot, COL["gray"], 1.3, "4,3")
    for dn, c in zip(seq, cols):
        sv.poly([(xc + dn * math.sin(math.pi * (y - top) / (bot - top)), y) for y in ys], c, 1.8, "4,3")
    sv.poly([(xc + dinf * math.sin(math.pi * (y - top) / (bot - top)), y) for y in ys], COL["comp_d"], 4)
    ym = (top + bot) / 2
    sv.text(xc + dinf + 8, ym - 30, "$δ_{∞}$", 13, COL["comp_d"], "start", "700")
    sv.text(xc, bot + 40, "$P$ 與 $δ$ 互餵", 12.5, COL["ink"])
    # 收斂長條
    ax_x, ax_y, bw = 545, 70, 230
    sv.text(ax_x + bw / 2 + 20, ax_y - 6, f"以 $α$ = $P/P_{{cr}}$ = {alpha} 為例（長度按比例）", 12, COL["dk"])
    labels = ["$δ_1$（$M$ 造成）", "$δ_2$ = $δ_1$(1+$α$)", "$δ_3$ = $δ_1$(1+$α$+$α^2$)", "$δ_{∞}$ = $δ_1$/(1−$α$)"]
    vals = seq + [dinf]
    for k, (lab, v) in enumerate(zip(labels, vals)):
        y = ax_y + 12 + k * 34
        c = (cols + [COL["comp_d"]])[k]
        sv.rect(ax_x, y, bw * v / dinf, 16, c, "none", 0, 3, op=0.85)
        sv.text(ax_x + bw + 8, y + 13, f"{v / d1:.3f}", 12, c, "start", "700")
        sv.text(ax_x + 2, y + 30, lab, 11.5, COL["ink"], "start")
    sv.line(ax_x + bw, ax_y + 8, ax_x + bw, ax_y + 152, COL["comp_d"], 1.2, "3,3")
    sv.text(615, 318, "內力自己長大，要放大後才能用", 15, COL["comp_d"], weight="700")
    sv.text(615, 340, "一階分析只是起點 → 乘 $B_1$／$B_2$（或 ASD 的 $C_m$／$F'_e$）", 12.5, COL["sub"])
    return sv.svg("圖0-1 P與δ互餵的幾何級數")


# ════════════════════════════════════════════════════════════════
# 圖 1-1　P-δ 與 P-Δ：形狀與附加彎矩分佈
# ════════════════════════════════════════════════════════════════
def fig_1_1():
    sv = SVG(900, 430)
    sv.line(450, 12, 450, 420, COL["lgray"], 2, "7,5")
    top, bot = 112, 300
    H = bot - top
    xi = np.linspace(0, 1, 61)
    # 左：簡支柱，正弦撓曲，附加彎矩 P·y 同形（跨中最大）
    sv.text(225, 30, "P-δ 效應（構件自己彎）", 16, COL["warn"], weight="700")
    xc, amp = 130, 42
    sv.pin(xc, bot)
    sv.line(xc, top, xc, bot, COL["gray"], 1.3, "4,3")
    sv.poly([(xc + amp * math.sin(math.pi * t), bot - H * t) for t in xi], COL["warn"], 6)
    sv.circle(xc, top, 5, "#fff", COL["dk"], 2)
    sv.line(xc - 14, top - 6, xc + 14, top - 6, COL["dk"], 2)
    sv.arrow(xc, top - 46, xc, top - 8, COL["comp"], 3)
    sv.text(xc, top - 52, "$P$", 14, COL["comp"], weight="700")
    sv.darrow(xc, (top + bot) / 2, xc + amp, (top + bot) / 2)
    sv.text(xc + amp + 8, (top + bot) / 2 + 5, "$δ$", 14, COL["key"], "start", "700")
    sv.text(xc - 52, top + 4, "柱頂", 11.5, COL["sub"], "end")
    sv.text(xc - 52, top + 20, "不側移", 11.5, COL["sub"], "end")
    # 附加彎矩圖
    bx = 270
    sv.line(bx, top, bx, bot, COL["dk"], 1.6)
    pts = [(bx + 52 * math.sin(math.pi * t), bot - H * t) for t in xi]
    sv.area([(bx, bot)] + pts + [(bx, top)], COL["warn"], 0.22)
    sv.poly(pts, COL["warn"], 2.4)
    sv.text(bx + 58, (top + bot) / 2 + 4, "$P·δ$", 13, COL["warn_d"], "start", "700")
    sv.text(bx + 26, top - 14, "附加彎矩 $P·y(x)$", 12, COL["warn_d"])
    sv.text(bx + 26, bot + 18, "兩端 = 0", 11.5, COL["sub"])
    sv.text(225, 360, "兩端不相對位移，中間鼓出去", 13, COL["ink"])
    sv.text(225, 382, "附加彎矩與撓曲同形 → 跨中最大", 13.5, COL["warn_d"], weight="700")
    sv.text(225, 404, "→ 用 $B_1$ 放大 $M_{nt}$", 13, COL["warn_d"], weight="700")

    # 右：兩端固接、側移 Δ 的柱：u = Δ(3ξ²−2ξ³)；P-Δ 等效層剪 PΔ/L → 端彎矩 ±PΔ/2
    sv.text(675, 30, "P-Δ 效應（整層一起歪）", 16, COL["comp"], weight="700")
    xc, D = 560, 54
    sv.fixed(xc, bot, half=24)
    sv.line(xc, top, xc, bot, COL["gray"], 1.3, "4,3")
    sv.poly([(xc + D * (3 * t * t - 2 * t ** 3), bot - H * t) for t in xi], COL["comp"], 6)
    sv.line(xc + D - 24, top, xc + D + 24, top, COL["dk"], 3)   # 柱頂受梁束制（不轉）
    sv.line(xc + D - 24, top - 2, xc + D + 24, top - 2, COL["dk"], 1)
    sv.arrow(xc + D, top - 46, xc + D, top - 6, COL["comp"], 3)
    sv.text(xc + D, top - 52, "$ΣP$", 14, COL["comp"], weight="700")
    sv.darrow(xc, top + 14, xc + D, top + 14)
    sv.text(xc + D / 2, top + 30, "$Δ$", 14, COL["key"], weight="700")
    sv.line(xc, bot, xc + D, top, COL["key"], 1.3, "2,4")
    sv.text(xc + D / 2 + 6, (top + bot) / 2 + 30, "弦線", 11, COL["key"], "start")
    # 附加彎矩（線性，端部 ±PΔ/2）
    bx = 760
    sv.line(bx, top, bx, bot, COL["dk"], 1.6)
    m = 46
    p_top, p_bot = (bx - m, top), (bx + m, bot)
    sv.area([(bx, top), p_top, (bx, (top + bot) / 2)], COL["comp"], 0.22)
    sv.area([(bx, bot), p_bot, (bx, (top + bot) / 2)], COL["comp"], 0.22)
    sv.poly([p_top, p_bot], COL["comp"], 2.4)
    sv.text(bx - m - 4, top + 4, "$PΔ$/2", 12, COL["comp_d"], "end", "700")
    sv.text(bx + m + 4, bot + 4, "$PΔ$/2", 12, COL["comp_d"], "start", "700")
    sv.text(bx, top - 14, "附加彎矩（線性）", 12, COL["comp_d"])
    sv.text(bx + 10, (top + bot) / 2 + 4, "中點 = 0", 11, COL["sub"], "start")
    sv.text(675, 360, "柱可以是直的，但兩端相對位移了", 13, COL["ink"])
    sv.text(675, 382, "附加彎矩 $ΣP·Δ$ 由柱端分攤 → 柱端最大", 13.5, COL["comp_d"], weight="700")
    sv.text(675, 404, "→ 用 $B_2$ 放大 $M_{lt}$", 13, COL["comp_d"], weight="700")
    return sv.svg("圖1-1 P-δ 與 P-Δ")


# ════════════════════════════════════════════════════════════════
# 圖 2-1　D_m = 1/(1−P/P_cr)
# ════════════════════════════════════════════════════════════════
def fig_2_1():
    sv = SVG(840, 380)
    ax = Axes(sv, 90, 40, 620, 270, (0, 1.0), (0, 6))
    ax.frame([0, .2, .4, .6, .8, 1.0], [0, 1, 2, 3, 4, 5, 6], xfmt="{:.1f}",
             xlabel="軸力比 $P/P_{cr}$（＝離挫屈有多近）", ylabel="$D_m$", ylabel_x=60)
    xs = np.linspace(0, 0.835, 300)
    ax.curve(xs, 1 / (1 - xs), COL["ac"], 3.4)
    sv.line(ax.X(1), ax.Y(6), ax.X(1), ax.Y(0), COL["comp"], 2, "7,5")
    sv.text(ax.X(1) - 8, ax.Y(0.45), "$P$ = $P_{cr}$ → $D_m$ = ∞（挫屈）", 12.5, COL["comp"], "end", "700")
    # AISC 360-10 起 ELM 適用限：Δ2nd/Δ1st ≤ 1.5
    sv.line(ax.X(0), ax.Y(1.5), ax.X(1), ax.Y(1.5), COL["key"], 1.4, "5,4")
    sv.text(ax.X(0.995), ax.Y(1.5) - 6, "1.5：AISC 360-10 起有效長度法的適用上限（$Δ_{2nd}$/$Δ_{1st}$）", 11.5, COL["key"], "end")
    pts = [(0.2, COL["ten"], "0.2 → 1.25（+25%）", 12, 22),
           (1 / 3, COL["key"], "1/3 → 1.50", 12, 22),
           (0.5, COL["warn"], "0.5 → 2.00（翻倍）", -150, -10),
           (0.6, COL["comp"], "0.6 → 2.50", -100, -12)]
    for r, c, lab, dx, dy in pts:
        x, y = ax.P(r, 1 / (1 - r))
        sv.circle(x, y, 5.5, c, "#fff", 1.6)
        sv.text(x + dx, y + dy, lab, 12.5, c, "start", "700")
    # 邊界檢查框
    sv.rect(110, 52, 290, 92, COL["key2"], "#ce93d8", 1.5, 7)
    sv.text(124, 75, "邊界檢查（忘記公式時自救）", 12.5, COL["key"], "start", "700")
    sv.text(124, 97, "$P$ = 0 → $D_m$ = 1（沒有軸力，不放大）✓", 12, "#4a148c", "start")
    sv.text(124, 116, "$P$ = $P_{cr}$ → $D_m$ = ∞（挫屈）✓", 12, "#4a148c", "start")
    sv.text(124, 135, "$P$ 增加 → $D_m$ 單調增加且越來越陡 ✓", 12, "#4a148c", "start")
    return sv.svg("圖2-1 放大係數曲線")


# ════════════════════════════════════════════════════════════════
# 圖 3-1　單曲率 vs 雙曲率：彈性二階精確解
#   EI y'' + P y = −M0(x)，M_total(x) = M_A cos kx + (M_B − M_A cos kL)/sin kL · sin kx
# ════════════════════════════════════════════════════════════════
P_RATIO = 0.30


def exact_moment(r, p=P_RATIO, n=201):
    """端彎矩 M_A = 1（柱頂）、M_B = −r（柱底；r = M1/M2，單曲率 r<0 → M_B 同號）。"""
    kL = math.pi * math.sqrt(p)
    MA, MB = 1.0, -r
    x = np.linspace(0, 1, n)
    M0 = MA * (1 - x) + MB * x
    Mt = MA * np.cos(kL * x) + (MB - MA * math.cos(kL)) / math.sin(kL) * np.sin(kL * x)
    y = (Mt - M0) / (p * math.pi ** 2)        # 以 M L^2/EI 為單位
    return x, M0, Mt, y


def amp_exact(r, p):
    x, M0, Mt, y = exact_moment(r, p)
    return np.abs(Mt).max()


def fig_3_1():
    sv = SVG(900, 420)
    sv.line(450, 12, 450, 410, COL["lgray"], 2, "7,5")
    top, bot = 84, 300
    H = bot - top
    for side, r in ((0, -1.0), (1, 1.0)):
        ox = side * 450
        x, M0, Mt, y = exact_moment(r)
        single = r < 0
        c = COL["comp"] if single else COL["ten"]
        title = "單曲率（C 形）— 危險" if single else "雙曲率（S 形）— 安全"
        sv.text(ox + 225, 28, title, 16, c, weight="700")
        sv.text(ox + 225, 50, f"$M_1/M_2$ = {r:+.0f}，$P/P_e$ = {P_RATIO}", 12.5, COL["dk"])
        # 柱（x 由頂而下）
        xc = ox + 120
        scale = 90 / max(1e-9, np.abs(exact_moment(-1.0)[3]).max())  # 兩側共用尺度
        sv.line(xc, top, xc, bot, COL["gray"], 1.3, "4,3")
        sv.poly([(xc + scale * yy, top + H * xx) for xx, yy in zip(x, y)], c, 6)
        sv.circle(xc, top, 5, "#fff", COL["dk"], 2); sv.pin(xc, bot)
        sv.arrow(xc, top - 34, xc, top - 7, COL["dk"], 3)
        sv.text(xc - 14, top - 26, "$P$", 14, COL["dk"], "end", "700")
        # 端彎矩箭頭：柱向右鼓 ⇔ 柱頂逆時針；單曲率柱底順時針、雙曲率柱底同為逆時針
        sv.moment(xc - 32, top + 6, 14, True, COL["warn"], start=330, span=230)
        sv.text(xc - 52, top + 10, "$M_2$", 12.5, COL["warn"], "end", "700")
        sv.moment(xc - 32, bot - 6, 14, not single, COL["warn"], start=210 if single else 330, span=230)
        sv.text(xc - 52, bot - 2, "$M_1$", 12.5, COL["warn"], "end", "700")
        k = int(np.argmax(np.abs(y)))
        sv.darrow(xc, top + H * x[k], xc + scale * y[k], top + H * x[k])
        sv.text(xc + scale * y[k] + 6, top + H * x[k] - 8, f"{abs(y[k]):.3f}", 11.5, COL["key"], "start", "700")
        if not single:
            km = int(np.argmin(np.abs(y[20:-20]))) + 20
            sv.circle(xc + scale * y[km], top + H * x[km], 5, COL["ac"], "#fff", 1.5)
            sv.text(xc + 12, top + H * x[km] + 4, "反曲點", 11.5, COL["ac"], "start")
        # 彎矩圖
        bx = ox + 300
        ms = 50
        sv.line(bx, top, bx, bot, COL["dk"], 1.6)
        pts = [(bx + ms * m, top + H * xx) for xx, m in zip(x, Mt)]
        sv.area([(bx, top)] + pts + [(bx, bot)], c, 0.2)
        sv.poly(pts, c, 2.6)
        sv.poly([(bx + ms * m, top + H * xx) for xx, m in zip(x, M0)], COL["dk"], 1.6, "5,4")
        km = int(np.argmax(np.abs(Mt)))
        sv.circle(bx + ms * Mt[km], top + H * x[km], 4.5, c, "#fff", 1.4)
        sv.text(bx + ms * Mt[km] + (8 if Mt[km] > 0 else -8), top + H * x[km] + (4 if single else 18),
                f"{abs(Mt[km]):.3f}$M_2$", 12, c, "start" if Mt[km] > 0 else "end", "700")
        sv.text(bx, top - 14, "彎矩：虛線一階／實線二階", 11.5, COL["dk"])
        sv.text(ox + 225, 346, "撓曲以 $M_2L^2/EI$ 為單位（兩側同比例）", 11.5, COL["sub"])
        if single:
            sv.text(ox + 225, 370, "變形同側累積，二階最大彎矩在跨中", 13, COL["comp_d"], weight="700")
            sv.text(ox + 225, 392, f"放大 {amp_exact(-1, P_RATIO):.3f} 倍 → $C_m$ 大（= 1.0）", 13.5, COL["comp_d"], weight="700")
        else:
            sv.text(ox + 225, 370, "上下抵消，二階彎矩仍以柱端為最大", 13, COL["ten_d"], weight="700")
            sv.text(ox + 225, 392, f"最大值 {amp_exact(1, P_RATIO):.3f}$M_2$（未放大）→ $C_m$ 小（= 0.2）", 13.5, COL["ten_d"], weight="700")
    return sv.svg("圖3-1 單曲率與雙曲率")


# ════════════════════════════════════════════════════════════════
# 圖 3-2　B1 曲線：台灣 (8.2-3) vs AISC，對照彈性精確解
# ════════════════════════════════════════════════════════════════
def fig_3_2():
    sv = SVG(880, 470)
    ax = Axes(sv, 80, 40, 500, 340, (0, 0.6), (0, 2.6))
    ax.frame([0, .1, .2, .3, .4, .5, .6], [0, .5, 1, 1.5, 2, 2.5], xfmt="{:.1f}", yfmt="{:.1f}",
             xlabel="$P_u/P_{e1}$", ylabel="$B_1$", ylabel_x=56)
    sv.area([ax.P(0, 0), ax.P(0.6, 0), ax.P(0.6, 1), ax.P(0, 1)], COL["lgray"], 0.28)
    sv.line(ax.X(0), ax.Y(1), ax.X(0.6), ax.Y(1), COL["dk"], 2.2)
    sv.text(ax.X(0.59), ax.Y(1) + 16, "灰區：算出小於 1.0 一律取 1.0", 11.5, COL["dk"], "end")
    ps = np.linspace(0, 0.6, 121)
    sets = [(-1.0, COL["comp"]), (-0.5, COL["warn"]), (0.0, COL["key"]), (1.0, COL["ten"])]
    for r, c in sets:
        ax.curve(ps, [B1_tw(p, r) for p in ps], c, 2.8)
        ax.curve(ps, [B1_aisc(p, r) for p in ps], c, 2.0, "7,5")
    # 精確解（單曲率等值端彎矩：sec 式）
    pe = np.linspace(0.001, 0.6, 121)
    ax.curve(pe, [amp_exact(-1.0, p) for p in pe], COL["ink"], 1.6, "2,3")
    # 曲線端標籤
    for r, c in sets:
        v = B1_tw(0.6, r)
        rs = "0" if r == 0 else f"{r:+.1f}"
        sv.text(ax.X(0.6) + 6, ax.Y(min(v, 2.55)) + 4, f"$M_1/M_2$ = {rs}", 12, c, "start", "700")
    # 範例 A 兩點（標籤只放代號，數值列在右側框）
    for p, tag in ((R['px'], "A強"), (R['py'], "A弱")):
        v = B1_tw(p, -1)
        x, y = ax.P(p, v)
        sv.circle(x, y, 5.5, COL["comp_d"], "#fff", 1.6)
        sv.text(x - 8, y - 10, tag, 11.5, COL["comp_d"], "end", "700")
    # 圖例（放在左上空白區）
    lx, ly = 104, 66
    sv.rect(lx - 12, ly - 20, 232, 84, "#fff", "#dfe6ea", 1.2, 6)
    sv.line(lx, ly, lx + 34, ly, COL["dk"], 2.8); sv.text(lx + 42, ly + 4, "台灣 (8.2-3)", 12, COL["ink"], "start")
    sv.line(lx, ly + 22, lx + 34, ly + 22, COL["dk"], 2, "7,5"); sv.text(lx + 42, ly + 26, "AISC $C_m$/(1−$P_u/P_{e1}$)", 12, COL["ink"], "start")
    sv.line(lx, ly + 44, lx + 34, ly + 44, COL["ink"], 1.6, "2,3"); sv.text(lx + 42, ly + 48, "彈性精確解 sec(π√$p$/2)", 12, COL["ink"], "start")
    return sv.svg("圖3-2 B1 曲線")


# ════════════════════════════════════════════════════════════════
# 圖 4-1　M_nt / M_lt 拆解：門型剛架勁度法實算
# ════════════════════════════════════════════════════════════════
FR = dict(h=4.0, b=6.0, w=3.0, H=6.0)   # m, m, tf/m, tf


def portal(braced, w, Hx):
    h, b = FR['h'], FR['b']
    nodes = [(0, 0), (0, h), (b, h), (b, 0)]
    members = [(0, 1, 1.0), (1, 2, 1.0), (3, 2, 1.0)]
    fixed = {(0, 0), (0, 1), (0, 2), (3, 0), (3, 1), (3, 2)}
    if braced:
        fixed |= {(2, 0)}
    loads = {(1, 0): Hx} if Hx else {}
    udl = {1: -w} if w else {}
    return frame2d.solve(nodes, members, fixed, loads, udl), nodes, members, udl


def draw_portal(sv, P, res, nodes, members, udl, mscale, color):
    """P: 模型→像素；mscale: 像素 / (tf·m)。彎矩圖畫在受拉側，端值與跨中值標註。"""
    d, ends, Rx = res
    for (i, j, EI) in members:
        sv.line(*P(nodes[i]), *P(nodes[j]), COL["dk"], 4, cap="butt")
    sv.fixed(*P(nodes[0])); sv.fixed(*P(nodes[3]))
    for mi, (i, j, EI) in enumerate(members):
        (x1, y1), (x2, y2) = nodes[i], nodes[j]
        Lm = math.hypot(x2 - x1, y2 - y1); c, s = (x2 - x1) / Lm, (y2 - y1) / Lm
        q = udl.get(mi, 0.0)
        ss = np.linspace(0, Lm, 61)
        Ms = frame2d.moment_along(ends[mi], q, Lm, ss)
        nx, ny = s, -c                      # 局部 −y 方向（正彎矩之受拉側），整體座標
        snx, sny = nx, -ny                  # 換成螢幕座標方向
        base = [P((x1 + c * t, y1 + s * t)) for t in ss]
        pts = [(bx_ + snx * m * mscale, by_ + sny * m * mscale) for (bx_, by_), m in zip(base, Ms)]
        sv.area(base + pts[::-1], color, 0.2)
        sv.poly(pts, color, 2.2)
        vertical = abs(c) < 0.5
        marks = ([0, len(ss) - 1] if vertical else []) + ([len(ss) // 2] if q else [])
        for k in marks:
            m = Ms[k]
            if abs(m) < 0.05:
                continue
            sgn = 1 if m >= 0 else -1
            ux, uy = snx * sgn, sny * sgn          # 指向圖形外側的螢幕單位向量
            X, Y = pts[k][0] + ux * 9, pts[k][1] + uy * 9
            if abs(ux) > 0.5:
                anchor = "start" if ux > 0 else "end"; Y += 4
                if k == 0: Y -= 8
                if k == len(ss) - 1: Y += 18
            else:
                anchor = "middle"; Y += 12 if uy > 0 else -3
                if k == 0: X += 10
                if k == len(ss) - 1: X -= 10
            sv.text(X, Y, f"{abs(m) + 1e-6:.2f}", 11.5, color, anchor, "700")


def fig_4_1():
    W = 930
    sv = SVG(W, 340)
    h, b, w, Hx = FR['h'], FR['b'], FR['w'], FR['H']
    sc = 27
    full = portal(False, w, Hx)
    nt = portal(True, w, Hx)
    nodes = [(0, 0), (0, h), (b, h), (b, 0)]
    members = [(0, 1, 1.0), (1, 2, 1.0), (3, 2, 1.0)]
    fixed = {(0, 0), (0, 1), (0, 2), (3, 0), (3, 1), (3, 2)}
    R_val = nt[0][2][2 * 3 + 0]          # 假想支撐對結構的反力（x 向）
    lt = (frame2d.solve(nodes, members, fixed, {(2, 0): -R_val}), nodes, members, {})
    mscale = 3.0                          # px / tf·m（三格共用）
    oxs = [62, 377, 692]
    oy = 262
    titles = [("① 真實狀態（一階）", COL["ac_d"]), ("② 加假想支撐（阻止側移）", COL["ten"]), ("③ 反向施加反力 $R$", COL["comp"])]
    for k, ox in enumerate(oxs):
        sv.text(ox + b * sc / 2, 24, titles[k][0], 14, titles[k][1], weight="700")
    for k, (res, nodes_, members_, udl_) in enumerate([full, nt, lt]):
        ox = oxs[k]
        P = lambda p, ox=ox: (ox + p[0] * sc, oy - p[1] * sc)
        col = [COL["ac"], COL["ten"], COL["comp"]][k]
        draw_portal(sv, P, res, nodes_, members_, udl_, mscale, col)
        x0, y0 = P((0, h)); x1, y1 = P((b, h))
        if k in (0, 1):
            for i in range(7):
                xx = x0 + (x1 - x0) * i / 6
                sv.arrow(xx, y0 - 58, xx, y0 - 34, COL["dk"], 1.3, 6)
            sv.line(x0, y0 - 58, x1, y0 - 58, COL["dk"], 1.3)
            sv.text((x0 + x1) / 2, y0 - 64, f"$w$ = {w:g} tf/m", 11.5, COL["dk"])
            sv.arrow(x0 - 46, y0, x0 - 4, y0, COL["warn"], 2.6)
            sv.text(x0 - 30, y0 - 10, f"$H$ = {Hx:g}", 11.5, COL["warn"], "middle", "700")
        if k == 1:
            sv.line(x1, y0, x1 + 30, y0, COL["key"], 3)
            sv.line(x1 + 30, y0 - 14, x1 + 30, y0 + 14, COL["key"], 3)
            for t in (-12, 0, 12):
                sv.line(x1 + 30, y0 + t, x1 + 38, y0 + t - 7, COL["key"], 1.4)
            sv.text(x1 + 34, y0 - 22, f"$R$ = {abs(R_val):.2f}", 11.5, COL["key"], "middle", "700")
        if k == 2:
            sgn = -1 if R_val > 0 else 1      # 反向施加
            sv.arrow(x1 + 4 if sgn > 0 else x1 + 46, y0, x1 + 46 if sgn > 0 else x1 + 4, y0, COL["key"], 2.6)
            sv.text(x1 + 26, y0 - 10, f"{abs(R_val):.2f}", 11.5, COL["key"], "middle", "700")
    sv.text((oxs[0] + b * sc + oxs[1]) / 2 - 6, 200, "=", 28, COL["dk"], weight="700")
    sv.text((oxs[1] + b * sc + oxs[2]) / 2 + 6, 200, "+", 28, COL["dk"], weight="700")
    sv.text(W / 2, 46, "柱端數字即節點彎矩（梁端與柱端相等）", 11.5, COL["sub"])
    cap_y = 306
    sv.text(oxs[0] + b * sc / 2, cap_y, "一階總彎矩", 12.5, COL["ac_d"], weight="700")
    sv.text(oxs[1] + b * sc / 2, cap_y, "$M_{nt}$ → 乘 $B_1$", 13, COL["ten_d"], weight="700")
    sv.text(oxs[2] + b * sc / 2, cap_y, "$M_{lt}$ → 乘 $B_2$", 13, COL["comp_d"], weight="700")
    sv.text(W / 2, 330, f"門型剛架：$h$ = {h:g} m、$b$ = {b:g} m、柱底固接、各構材 $EI$ 相同；彎矩圖畫在受拉側，單位 tf·m（勁度法實算，①＝②＋③ 已驗證）", 11.5, COL["sub"])
    for mi in range(3):   # 自我驗算：①＝②＋③
        for e in (2, 5):
            a_ = full[0][1][mi][e]; s2 = nt[0][1][mi][e] + lt[0][1][mi][e]
            assert abs(a_ - s2) < 1e-6, (mi, a_, s2)
    FIGS_DATA['portal'] = dict(R=abs(R_val))
    return sv.svg("圖4-1 Mnt 與 Mlt 拆解")


FIGS_DATA = {}


# ════════════════════════════════════════════════════════════════
# 圖 4-2　靠桿：側移形狀＋範例 B 的帳
# ════════════════════════════════════════════════════════════════
def fig_4_2():
    sv = SVG(880, 340)
    top, bot, D = 100, 240, 36
    H = bot - top
    sv.ground(60, 820, bot + 8, 40)
    xi = np.linspace(0, 1, 41)
    xs_rigid, xs_lean = [150, 330], [530, 690]
    # 原位虛線
    for x in xs_rigid + xs_lean:
        sv.line(x, top, x, bot, COL["lgray"], 1.6, "5,4")
    sv.line(110, top, 760, top, COL["lgray"], 1.6, "5,4")
    # 側移後梁
    sv.line(110 + D, top, 760 + D, top, COL["dk"], 5, cap="butt")
    for x in xs_rigid:   # 柱底固接、柱頂受梁束制 → 雙曲率
        sv.poly([(x + D * (3 * t * t - 2 * t ** 3), bot - H * t) for t in xi], COL["ac"], 8)
        sv.fixed(x, bot + 2, half=16)
    for x in xs_lean:
        sv.line(x, bot, x + D, top, COL["comp"], 4)
        sv.hinge(x, bot); sv.hinge(x + D, top)
    for x in xs_rigid + xs_lean:
        sv.arrow(x + D, top - 44, x + D, top - 6, COL["dk"], 2.4, 9)
    sv.text(xs_rigid[0] + D, top - 50, "250", 12, COL["ac_d"], weight="700")
    sv.text(xs_rigid[1] + D, top - 50, "250", 12, COL["ac_d"], weight="700")
    sv.text(xs_lean[0] + D, top - 50, "300", 12, COL["comp_d"], weight="700")
    sv.text(xs_lean[1] + D, top - 50, "300", 12, COL["comp_d"], weight="700")
    sv.text(xs_rigid[0] - 30, top - 50, "各柱 $P_u$（tf）", 12, COL["dk"], "end")
    sv.darrow(xs_lean[1], top + 18, xs_lean[1] + D, top + 18)
    sv.text(xs_lean[1] + D + 8, top + 23, "$Δ$", 13, COL["key"], "start", "700")
    sv.text(440, 26, "靠桿把自己的 P-Δ 負擔「轉嫁」給抗側力構架", 15.5, COL["dk"], weight="700")
    sv.text(240, 278, f"抗側力柱（剛接）：$P_{{e2}}$ = {R['Pe2']:.1f} tf 各", 13, COL["ac_d"], weight="700")
    sv.text(240, 298, "進 $ΣP_u$，也進 $ΣP_{e2}$", 12.5, COL["ac_d"])
    sv.text(610, 278, "靠桿（兩端鉸接）：勁度 0", 13, COL["comp_d"], weight="700")
    sv.text(610, 298, "進 $ΣP_u$，但不進 $ΣP_{e2}$！", 12.5, COL["comp_d"], weight="700")
    sv.text(440, 326, f"$ΣP_u$ = 1100、$ΣP_{{e2}}$ = {R['sPe2_B']:.0f} → 比值 {R['ratio_B']:.3f}、$B_2$ = {R['B2_B']:.2f}"
            f"（漏算靠桿得 {R['B2_B_wrong']:.2f}）", 12.5, COL["warn_d"], weight="700")
    return sv.svg("圖4-2 靠桿")


# ════════════════════════════════════════════════════════════════
# 圖 6-1　P-M 互制：H1 雙折線 vs 斷面全塑性精確互制
# ════════════════════════════════════════════════════════════════
def section_pm(d=400, bf=400, tw=13, tf=21, n=400):
    """H 型斷面強軸全塑性互制（不計圓角），回傳 (M/Mp, P/Py)。"""
    hw = d - 2 * tf
    A = 2 * bf * tf + hw * tw

    def width(y):            # y 自中心起算（mm）
        return bf if abs(y) > hw / 2 else tw
    ys = np.linspace(-d / 2, d / 2, 4001)
    dy = ys[1] - ys[0]
    b = np.array([width(y) for y in ys])
    Mp = np.sum(b * np.abs(ys)) * dy
    out = []
    for yn in np.linspace(-d / 2, d / 2, n):
        sig = np.where(ys > yn, 1.0, -1.0)
        Pp = np.sum(sig * b) * dy / A
        Mm = np.sum(sig * b * ys) * dy / Mp
        out.append((abs(Mm), Pp))
    pts = sorted([(m, p) for m, p in out if p >= 0], key=lambda t: -t[1])
    return pts


def fig_6_1():
    sv = SVG(860, 430)
    ax = Axes(sv, 110, 40, 520, 320, (0, 1.05), (0, 1.05))
    ax.frame([0, .2, .4, .6, .8, .9, 1.0], [0, .2, .4, .6, .8, 1.0], xfmt="{:.1f}", yfmt="{:.1f}",
             xlabel="彎矩利用率 $M_u/φ_bM_n$", ylabel="軸力利用率 $P_u/φ_cP_n$", ylabel_x=110)
    pm = section_pm()
    sv.poly([ax.P(m, p) for m, p in pm], COL["gray"], 2.2, "6,5")
    # 量測最大間距（以 P 軸方向）
    def h1(m):
        return 1 - 8 / 9 * m if m <= 0.9 else 2 * (1 - m)
    gap = max(p - h1(m) for m, p in pm if m <= 1)
    A_, B_, C_ = ax.P(0, 1), ax.P(0.9, 0.2), ax.P(1, 0)
    sv.area([ax.P(0, 0), A_, B_, C_], COL["ten"], 0.10)
    sv.line(*A_, *B_, COL["ac"], 4); sv.line(*B_, *C_, COL["comp"], 4)
    sv.line(B_[0], B_[1], B_[0], ax.Y(0), COL["key"], 1.4, "4,3")
    sv.line(ax.X(0), B_[1], B_[0], B_[1], COL["key"], 1.4, "4,3")
    sv.circle(*A_, 6, COL["ac"], "#fff", 1.5); sv.circle(*B_, 6.5, COL["key"], "#fff", 1.5); sv.circle(*C_, 6, COL["comp"], "#fff", 1.5)
    sv.text(A_[0] + 12, A_[1] - 6, "(0, 1.0) 純壓", 12.5, COL["ac"], "start", "700")
    sv.text(B_[0] - 14, B_[1] + 20, "折點 (0.9, 0.2)", 12.5, COL["key"], "end", "700")
    sv.text(C_[0] + 10, C_[1] - 8, "(1.0, 0) 純彎", 12.5, COL["comp"], "start", "700")
    mid = ax.P(0.45, 0.6)
    ang = math.degrees(math.atan2(B_[1] - A_[1], B_[0] - A_[0]))
    sv.text(mid[0] + 8, mid[1] - 12, "H1-1a：斜率 −8/9（較平）", 13, COL["ac_d"], "middle", "700", rot=round(ang, 1))
    sv.text(C_[0] + 10, ax.Y(0.12), "H1-1b：斜率 −2（較陡）", 12.5, COL["comp_d"], "start", "700")
    # 範例 C 設計點
    mu, pr = R['Mu_C'] / R['phiMnx_C'], R['Pr_C']
    x, y = ax.P(mu, pr)
    sv.circle(x, y, 6, COL["ten"], "#fff", 1.5)
    sv.text(x - 10, y + 22, f"範例 C：({mu:.3f}, {pr:.3f}) → {R['H1_C']:.3f}", 12.5, COL["ten_d"], "end", "700")
    sv.text(ax.X(0.98), ax.Y(0.93), "灰虛線：H400×400×13×21 斷面全塑性互制（精確，短柱）", 11.5, COL["sub"], "end")
    sv.text(ax.X(0.98), ax.Y(0.88), f"雙折線全程在內側；最大差距 {gap:.3f}（軸力比）", 11.5, COL["sub"], "end")
    sv.text(ax.X(0.2), ax.Y(0.1), "折線內側：安全", 12.5, COL["ten_d"], "middle", "700")
    FIGS_DATA['pm_gap'] = gap
    return sv.svg("圖6-1 P-M 互制")


# ════════════════════════════════════════════════════════════════
# 圖 7-1　ASD ↔ LRFD 逐項對應
# ════════════════════════════════════════════════════════════════
def fig_7_1():
    sv = SVG(880, 350)
    sv.text(220, 28, "ASD（台灣容許應力法 8.2 節）", 15, COL["comp"], weight="700")
    sv.text(660, 28, "LRFD（台灣極限設計法 8.2 節）", 15, COL["ac"], weight="700")
    sv.line(440, 14, 440, 340, COL["lgray"], 2, "7,5")
    rows = [
        ("$f_a/F_a$　（軸力利用率）", None, "$P_u/φ_cP_n$　（軸力利用率）", None),
        ("$C_m$/(1 − $f_a/F'_e$)　（二階放大）", "$C_m$ = 0.6 − 0.4$M_1/M_2$，無 0.4 下限",
         "$B_1$：台灣 (8.2-3) 0.64／0.32 式", "AISC：$C_m$/(1 − $P_u/P_{e1}$)"),
        ("$F'_e$ = 12$π^2E$ / [23($KL/r$)$^2$]", "用彎矩對應軸的 $KL/r$", "$P_{e1}$ = $π^2EI$/($KL$)$^2$", "$K$ 取 1.0（不側移模式）"),
        ("$f_{bx}/F_{bx}$　（$F_{bx}$ 含 LTB 分段）", None, "$M_{ux}/φ_bM_{nx}$　（含 LTB）", None),
    ]
    y = 46
    for a, a2, b, b2 in rows:
        hgt = 52 if (a2 or b2) else 40
        sv.rect(40, y, 360, hgt, COL["comp2"], COL["comp"], 1.6, 6)
        sv.rect(482, y, 360, hgt, COL["ac2"], COL["ac"], 1.6, 6)
        sv.text(56, y + 25 if hgt == 40 else y + 22, a, 13, COL["comp_d"], "start")
        sv.text(498, y + 25 if hgt == 40 else y + 22, b, 13, COL["ac_d"], "start")
        if a2:
            sv.text(56, y + 42, a2, 11.5, COL["comp_d"], "start")
        if b2:
            sv.text(498, y + 42, b2, 11.5, COL["ac_d"], "start")
        sv.line(402, y + hgt / 2, 478, y + hgt / 2, COL["dk"], 1.6, "4,3")
        y += hgt + 10
    sv.rect(40, y, 360, 52, COL["warn2"], COL["warn"], 1.8, 6)
    sv.text(56, y + 22, "另需「強度式」：$f_a$/0.6$F_y$ + $f_b/F_b$ ≤ 1", 13, COL["warn_d"], "start")
    sv.text(56, y + 42, "（檢查端部斷面降伏，SS-2003-4 即由它控制）", 11.5, COL["warn_d"], "start")
    sv.rect(482, y, 360, 52, COL["ten2"], COL["ten"], 1.8, 6)
    sv.text(498, y + 22, "只要一條 H1-1（8.2-1a／b）", 13, COL["ten_d"], "start")
    sv.text(498, y + 42, "（$φ_cP_n$／$φ_bM_n$ 已含挫屈折減）", 11.5, COL["ten_d"], "start")
    return sv.svg("圖7-1 ASD 與 LRFD 對應")


# ════════════════════════════════════════════════════════════════
# 圖 8-1　K 的敏感度（新增）
# ════════════════════════════════════════════════════════════════
def fig_8_1():
    sv = SVG(900, 380)
    # 左：P_e / P_e(K=1) = 1/K^2
    ax = Axes(sv, 70, 44, 330, 250, (0.5, 2.5), (0, 4))
    ax.frame([0.5, 1, 1.5, 2, 2.5], [0, 1, 2, 3, 4], xfmt="{:.1f}", xlabel="有效長度係數 $K$", ylabel="$P_e$ / $P_e$($K$=1)", ylabel_x=90)
    ks = np.linspace(0.5, 2.5, 200)
    ax.curve(ks, 1 / ks ** 2, COL["ac"], 3)
    for k, c, dx, dy, an in ((0.7, COL["ten"], 10, -6, "start"), (1.0, COL["dk"], 10, -8, "start"),
                             (1.5, COL["warn"], -10, -16, "end"), (1.8, COL["comp"], 2, -30, "start"),
                             (2.0, COL["comp"], 6, 24, "start")):
        x, y = ax.P(k, 1 / k ** 2)
        sv.circle(x, y, 5, c, "#fff", 1.4)
        sv.text(x + dx, y + dy, f"{k:g} → {1 / k ** 2:.2f}", 11.5, c, an, "700")
    sv.text(235, 24, "(a) 挫屈載重 ∝ 1/$K^2$", 14, COL["ac_d"], weight="700")
    # 右：範例 C 的 B2 隨 K
    ax2 = Axes(sv, 540, 44, 320, 250, (1.0, 2.6), (1.0, 3.0))
    ax2.frame([1.0, 1.4, 1.8, 2.2, 2.6], [1.0, 1.5, 2.0, 2.5, 3.0], xfmt="{:.1f}", yfmt="{:.1f}",
              xlabel="$ΣP_{e2}$ 所用的 $K$", ylabel="範例 C 的 $B_2$", ylabel_x=560)
    a1 = 750 / (3 * R['Pe1x'])
    kk = np.linspace(1.0, 2.6, 200)
    ax2.curve(kk, 1 / (1 - a1 * kk ** 2), COL["comp"], 3)
    sv.line(ax2.X(1.0), ax2.Y(1.5), ax2.X(2.6), ax2.Y(1.5), COL["key"], 1.4, "5,4")
    kc = math.sqrt((1 - 1 / 1.5) / a1)
    sv.text(ax2.X(1.02), ax2.Y(1.5) - 7, f"1.5：AISC 有效長度法上限（$K$ = {kc:.2f}）", 11, COL["key"], "start")
    for k, lab in ((1.0, "誤用 $K$=1"), (1.8, "正確 $K$=1.8")):
        v = 1 / (1 - a1 * k * k)
        x, y = ax2.P(k, v)
        sv.circle(x, y, 5.5, COL["comp_d"], "#fff", 1.5)
        sv.text(x + 10, y + (20 if k > 1.5 else -20), f"{lab}：{v:.3f}", 12, COL["comp_d"], "start", "700")
    sv.text(700, 24, "(b) 範例 C：$K$ 決定 $B_2$", 14, COL["comp_d"], weight="700")
    sv.text(450, 360, f"把 $K$ = 1.8 誤用成 1.0：$P_e$ 高估 {1.8 ** 2:.2f} 倍，$B_2$ 由 {R['B2_C']:.3f} 掉到 {R['B2_C_K1']:.3f}"
            f"（側移放大量 {R['B2_C'] - 1:.3f} → {R['B2_C_K1'] - 1:.3f}，少掉 {(1 - (R['B2_C_K1'] - 1) / (R['B2_C'] - 1)) * 100:.0f}%）",
            12.5, COL["warn_d"], weight="700")
    return sv.svg("圖8-1 K 的敏感度")


# ════════════════════════════════════════════════════════════════
# 圖 8-2　三代穩定處理法
# ════════════════════════════════════════════════════════════════
def fig_8_2():
    sv = SVG(900, 340)
    boxes = [(20, COL["ten2"], COL["ten"], COL["ten_d"], "第一代：有效長度法 ELM"),
             (315, COL["warn2"], COL["warn"], COL["warn_d"], "第二代：$B_1$／$B_2$ 放大法"),
             (610, COL["ac2"], COL["ac"], COL["ac_d"], "第三代：直接分析法 DAM")]
    for x, f, s, t, title in boxes:
        sv.rect(x, 48, 270, 196, f, s, 2, 10)
        sv.text(x + 135, 34, title, 14.5, t, weight="700")
    sv.arrow(292, 146, 312, 146, COL["dk"], 2.5, 9); sv.arrow(587, 146, 607, 146, COL["dk"], 2.5, 9)
    L = [
        (36, [("做法：穩定效應全部塞進 $K$", COL["ten_d"], "400"), ("一階分析 ＋ 對位圖 $K$", COL["ten_d"], "400"),
              ("問題：", COL["comp_d"], "700"), ("・$K$ 只反映彈性挫屈模態", COL["ink"], "400"),
              ("・不反映實際載重分佈", COL["ink"], "400"), ("・靠桿、非均勻載重算不準", COL["ink"], "400"),
              ("・對位圖假設多（等 $EI$、等載重）", COL["sub"], "400")]),
        (331, [("做法：一階分析 ＋ 兩個放大係數", COL["warn_d"], "400"), ("$M_u$ = $B_1M_{nt}$ + $B_2M_{lt}$", COL["warn_d"], "400"),
               ("進步：", COL["ten"], "700"), ("・二階效應顯式計算", COL["ink"], "400"), ("・整層 $ΣP_u$ 抓到靠桿", COL["ink"], "400"),
               ("仍需：", COL["comp_d"], "700"), ("・$B_2$ 仍要側移 $K$（對位圖）", COL["ink"], "400")]),
        (626, [("做法：直接做二階分析，", COL["ac_d"], "400"), ("$K$ 一律取 1.0", COL["ac_d"], "700"),
               ("代價（四件事）：", COL["ten"], "700"), ("① 二階分析（P-Δ ＋ P-δ）", COL["ink"], "400"),
               ("② 初始不完美（假想水平力）", COL["ink"], "400"), ("③ 勁度折減 0.8$τ_b$", COL["ink"], "400"),
               ("④ ASD 載重先乘 $α$ = 1.6", COL["ink"], "400")]),
    ]
    for x, items in L:
        for i, (s, c, wgt) in enumerate(items):
            sv.text(x, 74 + i * 23, s, 12.5, c, "start", wgt)
    sv.text(450, 270, "三代方法解的是同一個問題：「這個構架離側移失穩有多遠？」", 13, COL["sub"])
    sv.text(450, 294, "演化方向：把藏在 $K$ 裡的假設一項項搬到分析裡明說", 13.5, COL["dk"], weight="700")
    sv.text(450, 318, "台灣現行鋼構規範（99 年版）停在第二代：沒有 DAM 條文；DAM 只在概念題以 AISC 360 出現（SS-2011-1）", 12, "#78909c")
    return sv.svg("圖8-2 三代穩定處理法")


# ════════════════════════════════════════════════════════════════
# 圖 9-1　梁機構 vs 層機構（同屋頂側移）
# ════════════════════════════════════════════════════════════════
def fig_9_1():
    sv = SVG(900, 380)
    sv.line(450, 12, 450, 370, COL["lgray"], 2, "7,5")
    h, b, n = 62, 210, 3
    base = 270
    Droof = 54
    for side in (0, 1):
        ox = 120 + side * 450
        good = side == 0
        c = COL["ten"] if good else COL["comp"]
        sv.text(ox + b / 2, 30, "梁先降伏（強柱弱梁）— 好" if good else "柱先降伏（弱柱強梁）— 災難", 15.5, c, weight="700")
        sv.ground(ox - 30, ox + b + 70, base, 18)
        # 原位
        for x in (ox, ox + b):
            sv.line(x, base, x, base - n * h, COL["lgray"], 1.6, "5,4")
        for k in range(1, n + 1):
            sv.line(ox, base - k * h, ox + b, base - k * h, COL["lgray"], 1.6, "5,4")
        u = (lambda k: Droof * k / n) if good else (lambda k: Droof if k >= 1 else 0)
        for k in range(n):
            col_c = COL["dk"] if (good or k > 0) else COL["comp"]
            for x in (ox, ox + b):
                sv.line(x + u(k), base - k * h, x + u(k + 1), base - (k + 1) * h, col_c, 4)
        for k in range(1, n + 1):
            sv.line(ox + u(k), base - k * h, ox + b + u(k), base - k * h, COL["dk"], 4)
        hinges = []
        if good:
            for k in range(1, n + 1):
                hinges += [(ox + u(k) + 16, base - k * h), (ox + b + u(k) - 16, base - k * h)]
            hinges += [(ox, base), (ox + b, base)]
        else:
            hinges = [(ox, base), (ox + b, base), (ox + u(1), base - h), (ox + b + u(1), base - h)]
        for x, y in hinges:
            sv.circle(x, y, 6.5, c, "#fff", 1.6)
        sv.darrow(ox + b, base - n * h - 16, ox + b + Droof, base - n * h - 16)
        sv.text(ox + b + Droof + 6, base - n * h - 12, "$Δ$", 13, COL["key"], "start", "700")
        th = Droof / (n * h) if good else Droof / h
        if good:
            sv.text(ox + b / 2, 302, f"塑鉸 {len(hinges)} 個，分散在每層梁端＋柱底", 13, COL["ink"])
            sv.text(ox + b / 2, 324, "塑鉸轉角 $θ$ = $Δ$/(3$h$)", 13.5, COL["ten_d"], weight="700")
            sv.text(ox + b / 2, 346, "梁壞了只失去一根梁，重力仍有柱撐著", 12.5, COL["sub"])
        else:
            sv.text(ox + b / 2 + 40, base - h / 2 + 4, "軟層", 13, COL["comp_d"], "start", "700")
            sv.text(ox + b / 2, 302, f"塑鉸 {len(hinges)} 個，全部集中在第一層柱端", 13, COL["ink"])
            sv.text(ox + b / 2, 324, "塑鉸轉角 $θ$ = $Δ$/$h$ ＝ 左邊的 3 倍", 13.5, COL["comp_d"], weight="700")
            sv.text(ox + b / 2, 346, "柱一壞，上方所有樓層的重量無處可去 → 倒塌", 12.5, COL["sub"])
    sv.text(450, 372, "兩邊屋頂側移 $Δ$ 相同（按比例繪製）", 11.5, "#78909c")
    return sv.svg("圖9-1 梁機構與層機構")


for fn in [fig_0_1, fig_1_1, fig_2_1, fig_3_1, fig_3_2, fig_4_1, fig_4_2, fig_6_1, fig_7_1, fig_8_1, fig_8_2, fig_9_1]:
    key = fn.__name__.replace("fig_", "fig-").replace("_", "-")
    FIGS[key] = fn()
    open(os.path.join(OUT, key + ".svg"), "w", encoding="utf-8").write(FIGS[key])

if __name__ == "__main__":
    import json
    print("figs:", list(FIGS))
    print(json.dumps(FIGS_DATA, ensure_ascii=False, default=float, indent=1))
    for r in (-1, 1):
        print("exact amp", r, amp_exact(r, P_RATIO), "tw", B1_tw(P_RATIO, r), "aisc", B1_aisc(P_RATIO, r))
