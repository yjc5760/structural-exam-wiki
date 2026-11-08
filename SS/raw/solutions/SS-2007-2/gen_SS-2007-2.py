#!/usr/bin/env python3
"""
SS-2007-2 H 型鋼柱受軸壓＋雙軸彎矩（ASD 檢核）— 題目附圖重繪腳本（圖二）

用法：
    python3 gen_SS-2007-2.py [輸出目錄]

重繪依據：題目正本 SS-2007-2-problem.md §4 判讀清單（待確認）。
只畫考卷給的東西（斷面標註、P、M_X 與 M_Y 彎矩圖形狀、L），不含任何解題結果
（Cm、Cb、F_a、F_b、應力比都不畫）。
斷面 H 500×300×15×20 依比例繪製；柱長為示意比例（L = 10 m）；彎矩圖高度為示意，
只表達考卷給的形狀（上端最大、下端為 0）。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2007-2"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2007-2-problem.md §4，待確認）＋題文
# ══════════════════════════════════════════════════════════
D, BF, TW, TF = 50.0, 30.0, 1.5, 2.0   # 題文 H 500×300×15×20（cm）
L_M = 10.0                             # #3、#4 柱長 L = 10 m（兩端鉸接，無中間支撐）
MX_TOP, MX_BOT = 1.0, 0.0              # #1 M_X 三角形：上端最大（20 m-tf）、下端 O
MY_TOP, MY_BOT = 1.0, 0.0              # #1 M_Y 三角形：上端最大（10 m-tf）、下端 O
#                                        #2 X 軸垂直腹板 → M_X 強軸、M_Y 弱軸

PW, PH = 340, 580
COL_H = 330.0     # 柱高（像素，示意）
COL_W = 46.0      # 柱寬（像素，示意）


def _rect(cv, x0, x1, y0, y1, fill=C["fill_c"], w=1.6):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, C["member"], w)


def section_panel():
    sx = 5.0
    cv = Canvas(PW, PH, sx=sx, ox=PW / 2 + 10, oy=PH / 2 - 30)
    cv.panel("斷面", "H 500×300×15×20（依比例）")
    _rect(cv, -BF / 2, BF / 2, D / 2 - TF, D / 2)
    _rect(cv, -BF / 2, BF / 2, -D / 2, -D / 2 + TF)
    _rect(cv, -TW / 2, TW / 2, -D / 2 + TF, D / 2 - TF)
    cv.arrow((0, 0), (0, D / 2 + 9), C["text"], 1.6, 8)
    cv.arrow((0, 0), (BF / 2 + 9, 0), C["text"], 1.6, 8)
    cv.math((0, D / 2 + 9), "Y", 17, C["text"], dy=-12, weight="700")
    cv.math((BF / 2 + 9, 0), "X", 17, C["text"], "start", dx=6, weight="700")
    cv.dim((-BF / 2, -D / 2), (-BF / 2, D / 2), "d", off=-26, label_off=-14, size=16)
    cv.dim((BF / 2, D / 2 - TF), (BF / 2, D / 2), "t_{f}", off=22, label_off=34, size=16)
    cv.dim((-BF / 2, -D / 2), (BF / 2, -D / 2), "b_{f}", off=24, label_off=18, size=16)
    cv.math((TW / 2, -6), "t_{w}", 16, C["dim"], "start", dx=10)
    return cv


def _column_panel(title, sub, mlab, top, bot, inner):
    cv = Canvas(PW, PH, sx=1.0, ox=0, oy=0)
    cv.panel(title, sub)
    cx, y0 = 110.0, 100.0                      # 柱軸 x、柱底（像素，自底起算）
    y1 = y0 + COL_H
    _rect(cv, cx - COL_W / 2, cx + COL_W / 2, y0, y1, "#FFFFFF", 1.4)
    for xx, dash in inner:
        cv.line((cx + xx, y0), (cx + xx, y1), C["member"], 1.1, dash=dash)
    # P 上下端軸壓
    cv.arrow((cx, y1 + 60), (cx, y1), C["load"], 2.6, 10)
    cv.math((cx, y1 + 60), "P", 17, C["load"], "start", dx=10, dy=4, weight="700")
    cv.arrow((cx, y0 - 60), (cx, y0), C["load"], 2.6, 10)
    cv.math((cx, y0 - 60), "P", 17, C["load"], "start", dx=10, dy=-4, weight="700")
    # 彎矩圖：上端最大、下端為 O（#1）
    bx, bw = cx + COL_W / 2 + 34, 58.0
    cv.polygon([(bx, y1), (bx + bw * top, y1), (bx + bw * bot, y0)], C["fill_m"], C["bmd"], 1.6)
    cv.line((bx, y0), (bx, y1), C["bmd"], 1.2, dash="4 3")
    cv.math((bx + bw * top / 2, y1), mlab, 17, C["bmd"], dy=-16, weight="700")
    cv.text((bx, y0), "O", 15, C["bmd"], "start", dx=8, dy=16, weight="700")
    return cv, cx, y0, y1


def fig1_problem():
    p1, cx, y0, y1 = _column_panel("強軸彎曲面", "M_X 彎矩圖", "M_{X}", MX_TOP, MX_BOT,
                                   [(0.0, "4 3")])
    p1.dim((cx + COL_W / 2 + 120, y0), (cx + COL_W / 2 + 120, y1), "L", off=0, label_off=-16, size=17)
    p2, *_ = _column_panel("弱軸彎曲面", "M_Y 彎矩圖", "M_{Y}", MY_TOP, MY_BOT,
                           [(-COL_W / 2 + 6, None), (COL_W / 2 - 6, None)])
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([section_panel(), p1, p2], cols=3,
            title="SS-2007-2 題目附圖（重繪，考卷圖二）",
            sub=f"依題目正本判讀清單 #1–#4；斷面依比例，柱長與彎矩圖高度示意；L = {L_M:.0f} m，"
                "Mx = 20 m-tf、MY = 10 m-tf",
            note="兩個彎矩圖都是上端最大、下端為 O（三角形分布），不是均勻彎矩",
            path=path)
    return path


# ── 解題圖解共用小工具（像素座標；y 由上往下）──
def _hl(cv, PH, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line((x0, PH - y0), (x1, PH - y1), color, w, dash=dash, cap="butt")


def rsum(terms, nd=3):
    """與解析相同的加法：各項先四捨五入到 nd 位再相加"""
    return round(sum(round(t, nd) for t in terms), nd)


def _stack_row(cv, x0, y, scale, terms, colors, name, total_color, h=34, fmt="{:.3f}"):
    """水平堆疊長條：互制比 1.0 對應 scale 像素"""
    cv.text_px(x0 - 14, y, name, 14, C["text"], "end", weight="700")
    xx = x0
    for t, col in zip(terms, colors):
        w = scale * t
        cv.rect_px(xx, y - h/2, w, h, col, 0)
        if w > 44:
            cv.text_px(xx + w/2, y, fmt.format(t), 12.5, "#FFFFFF", weight="700")
        xx += w
    tot = rsum(terms)
    cv.text_px(xx + 12, y, "= " + fmt.format(tot), 15, total_color, "start", weight="700")
    return tot


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2007-2.md §1／§4，由下式即時算出
# ══════════════════════════════════════════════════════════════
import math
P_TF  = 40.0                     # tf                       §1
MX_TC = 2000.0                   # tf·cm（20 m-tf）           §1
MY_TC = 1000.0                   # tf·cm（10 m-tf）           §1
L_CM  = 1000.0                   # cm                       §1
A_G, R_X, R_Y, R_T = 189.0, 20.74, 6.91, 7.94                  # §1
S_X, S_Y = 3253.0, 600.0                                       # §1
F_Y, E_TF = 3.5, 2040.0                                        # §1
AF_FL = (BF / 1) * TF            # A_f = 30 × 2.0 cm^2（取題目斷面尺寸）

M1M2 = 0.0                                                     # §4 Step 1：一端最大、一端為零
CM   = 0.6 - 0.4 * M1M2                                        # = 0.6
CB   = min(1.75 + 1.05 * M1M2 + 0.3 * M1M2**2, 2.3)            # = 1.75
fa, fbx, fby = P_TF / A_G, MX_TC / S_X, MY_TC / S_Y            # Step 2
CC   = math.sqrt(2 * math.pi**2 * E_TF / F_Y)                  # Step 3
EUL  = lambda klr: 12 * math.pi**2 * E_TF / (23 * klr**2)
KLRX, KLRY = L_CM / R_X, L_CM / R_Y
FA   = EUL(KLRY)                                               # KL/ry > Cc → 彈性式
FB1  = (2/3 - F_Y * (L_CM / R_T)**2 / (107600 * CB)) * F_Y     # Step 4
FB2  = 840 * CB / (L_CM * (D / 1) / AF_FL)
FBX  = min(max(FB1, FB2), 0.6 * F_Y)
FBY  = 0.75 * F_Y                                              # Step 5
FEX, FEY = EUL(KLRX), EUL(KLRY)                                # Step 6
AFX, AFY = 1 / (1 - fa / FEX), 1 / (1 - fa / FEY)              # 二階放大
EQ2  = [fa / FA, CM * fbx * AFX / FBX, CM * fby * AFY / FBY]   # Step 7 式 (2)
EQ3  = [fa / (0.6 * F_Y), fbx / FBX, fby / FBY]                # Step 7 式 (3)
NOAMP = [fa / FA, CM * fbx / FBX, CM * fby / FBY]              # 假設漏掉放大


def _equiv_panel(title, m2_tc, af, sc, warn):
    """單一彎曲面：一階三角形彎矩 → 等效均勻 Cm·M2 → 再乘二階放大"""
    W1, H1 = 520, 560
    cv = Canvas(W1, H1, sx=1)
    cv.panel(title, "柱軸（上端最大、下端為零）")
    cx, yt, yb = 96, 132, 412                       # 像素，y 向下
    m2 = m2_tc / 100                               # tf·m
    eq = CM * m2
    amp = eq * af
    X = lambda m: cx + sc * m
    _hl(cv, H1, cx, yt - 12, cx, yb + 12, C["member"], 5.0)
    cv.polygon([(cx, H1 - yt), (X(m2), H1 - yt), (cx, H1 - yb)], C["fill_m"], C["bmd"], 2.2)
    cv.poly([(cx, H1 - yt), (X(eq), H1 - yt), (X(eq), H1 - yb), (cx, H1 - yb)],
            C["bmd"], 2.0, dash="7 5")
    _hl(cv, H1, X(amp), yt - 6, X(amp), yb + 6, C["accent"], 2.6, dash="3 4")
    _hl(cv, H1, X(m2), yt - 6, X(m2), yb + 6, C["muted"], 1.2, dash="2 4")
    cv.text_px(X(m2), yt - 16, f"M2 = {m2:g}", 13, C["bmd"], "middle", weight="700")
    rows = ((C["bmd"], f"一階：三角形，M2 = {m2:g} tf·m，M1 = 0"),
            (C["bmd"], f"等效均勻：Cm·M2 = {CM:.1f} × {m2:g} = {eq:.1f} tf·m（虛框）"),
            (C["accent"], f"二階：× 1/(1 − fa/F'e) = × {af:.3f} → {amp:.2f} tf·m"))
    for i, (col, s) in enumerate(rows):
        cv.text_px(40, yb + 44 + i * 26, s, 13, col, "start", weight="700" if i == 2 else "400")
    cv.text_px(W1 / 2, H1 - 28, warn, 12.5, C["load"] if amp > m2 else C["muted"], weight="700")
    return cv


def fig1_equiv():
    sc = 300 / 20.0                                   # 20 tf·m = 300 px（兩格共用比例）
    p1 = _equiv_panel("① 強軸 Mx", MX_TC, AFX, sc,
                      f"放大後 {CM * MX_TC / 100 * AFX:.2f} 仍小於 M2——強軸二階效應溫和")
    p2 = _equiv_panel("② 弱軸 My", MY_TC, AFY, sc,
                      f"放大後 {CM * MY_TC / 100 * AFY:.2f} 已超過一階最大值 {MY_TC / 100:g}")
    path = os.path.join(OUT, f"{TAG}-fig-1-equiv.svg")
    compose([p1, p2], cols=2,
            title="圖 1　三角形彎矩 → Cm = 0.6 的等效均勻彎矩 → 二階放大",
            sub=f"M1/M2 = 0 ⇒ Cm = {CM:.1f}、Cb = {CB:.2f}；"
                f"KL/rx = {KLRX:.1f}、KL/ry = {KLRY:.1f} > Cc = {CC:.1f}",
            note="兩格同一比例尺：Cm 把三角形換成較小的均勻彎矩，但弱軸的放大係數 1.73 又把它推回並超過原值",
            path=path)
    return path


def fig2_terms():
    W1, H1 = 560, 420
    COLS = [C["compr"], C["bmd"], C["accent"]]
    SC = 230.0
    cv = Canvas(W1, H1, sx=1)
    cv.panel("① 兩式皆須滿足", f"fa/Fa = {EQ2[0]:.3f} > 0.15 ⇒ 用式 (2)、(3)")
    x0 = 110
    _hl(cv, H1, x0 + SC, 96, x0 + SC, 300, C["load"], 2.0, dash="6 4")
    cv.text_px(x0 + SC, 86, "上限 1.0", 12.5, C["load"], weight="700")
    _stack_row(cv, x0, 160, SC, EQ2, COLS, "式 (2) 穩定", C["load"])
    _stack_row(cv, x0, 240, SC, EQ3, COLS, "式 (3) 強度", C["load"])
    cv.legend(x0 - 70, 316, [(COLS[0], "軸壓項"), (COLS[1], "強軸彎矩項"), (COLS[2], "弱軸彎矩項")],
              size=12, gap=19)
    p1 = cv

    cv = Canvas(W1, H1, sx=1)
    cv.panel("② 二階放大的貢獻（式 (2) 的彎矩項）", "淺色＝未放大、深色＝放大後")
    x0, sc2 = 150, 420.0
    rows = (("強軸項", NOAMP[1], EQ2[1], C["bmd"], AFX), ("弱軸項", NOAMP[2], EQ2[2], C["accent"], AFY))
    y = 136
    for nm, a, b, col, af in rows:
        cv.text_px(x0 - 14, y + 18, nm, 14, C["text"], "end", weight="700")
        cv.rect_px(x0, y, sc2 * a, 16, C["ghost"], 3)
        cv.text_px(x0 + sc2 * a + 8, y + 8, f"{a:.3f}", 12, C["muted"], "start")
        cv.rect_px(x0, y + 20, sc2 * b, 16, col, 3)
        cv.text_px(x0 + sc2 * b + 8, y + 28, f"{b:.3f}（× {af:.3f}）", 12, col, "start", weight="700")
        y += 86
    cv.text_px(W1 / 2, H1 - 78, f"若漏乘放大係數：式 (2) = {rsum(NOAMP):.3f}", 13, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 52, f"仍 > 1.0，但把超出量由 {rsum(EQ2) - 1:.0%} 低估成 {rsum(NOAMP) - 1:.0%}", 12.5, C["muted"])
    cv.text_px(W1 / 2, H1 - 28, f"弱軸 F'ey = Fa = {FA:.3f}：同一個歐拉應力同時壓低 Fa 與放大彎矩", 12.5,
               C["accent"], weight="700")
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-2-terms.svg")
    compose([p1, p2], cols=2,
            title=f"圖 2　ASD 互制：式 (2) = {rsum(EQ2):.3f}、式 (3) = {rsum(EQ3):.3f}，皆 N.G.",
            sub=f"Fa = {FA:.3f}　Fbx = {FBX:.3f}　Fby = {FBY:.3f}　F'ex = {FEX:.3f}　F'ey = {FEY:.3f}（tf/cm²）",
            note=f"式 (2) 最大的一項是弱軸彎矩 {EQ2[2]:.3f}，其中 {EQ2[2] - NOAMP[2]:.3f}（{(EQ2[2] - NOAMP[2]) / EQ2[2]:.0%}）來自二階放大",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把三角形彎矩圖讀成均勻彎矩或雙曲率（M1/M2 取錯）；Mx 與 MY 對應的強弱軸對調"),
    (fig1_equiv, "§4 Step 1、6",
     "把三角形彎矩取 Cm = 1.0；以為 Cm·M2 一定小於 M2 而忽略弱軸放大會把它推過原值"),
    (fig2_terms, "§4 Step 7",
     "只驗一式；漏乘 1/(1 − fa/F'e) 而把超出量由 30% 低估成 1%；誤判控制項為軸壓"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
