#!/usr/bin/env python3
"""
SS-2008-4 偏心軸壓＋跨中橫力之梁柱構件（ASD 求最大容許 P）— 題目附圖重繪腳本（圖 3）

用法：
    python3 gen_SS-2008-4.py [輸出目錄]

重繪依據：題目正本 SS-2008-4-problem.md §4 判讀清單（待確認）。
只畫考卷給的東西（支承、P 與偏心 d、H、L/2、側撐、斷面軸向），不含任何解題結果
（彎矩圖、F_a、F_b、所求 P 值都不畫）。
構件長度依 L 比例；偏心臂高度 d 為示意（25 cm 相對 12 m 放大）；斷面依 W 型鋼題給
d、b_f、t_f、t_w 比例繪製。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2008-4"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2008-4-problem.md §4，待確認）＋題文
# ══════════════════════════════════════════════════════════
L_M = 12.0                     # 題文 L = 12 m；A–B、B–C 各 L/2
XB = L_M / 2                   # #4 H 作用於跨中 B
ECC_PX = 58.0                  # #1、#2 A 端偏心臂高 d（自臂頂 P 作用點量到形心軸；25 cm，示意放大）
#                                #1 只有 A 端偏心；C 端 P 作用於軸線上
#                                #3 y-z 面：A 滾支、C 鉸支；x-z 面：A、B、C 皆側撐
#                                #4 H 沿 +y（向下）
SEC_D, SEC_BF, SEC_TF, SEC_TW = 30.3, 20.3, 1.31, 0.749   # 題文 W 型鋼（cm）

PW, PH = 1000, 330


def _rect(cv, x0, x1, y0, y1):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], C["fill_c"], C["member"], 1.4)


def _section(cv, cx, cy, s=3.0):
    """斷面小圖（cx, cy 為像素，cy 自底起算）：腹板沿 y（鉛直）、x 軸向左、y 軸向下"""
    def M(u, v):                       # 斷面 cm 座標 → 畫布模型座標
        return ((cx + u * s - cv.ox) / cv.sx, (cy + v * s - cv.oy) / cv.sx)

    def R(x0, x1, y0, y1):
        cv.polygon([M(x0, y0), M(x1, y0), M(x1, y1), M(x0, y1)], C["fill_c"], C["member"], 1.4)
    d, bf, tf, tw = SEC_D, SEC_BF, SEC_TF, SEC_TW
    R(-bf / 2, bf / 2, d / 2 - tf, d / 2)
    R(-bf / 2, bf / 2, -d / 2, -d / 2 + tf)
    R(-tw / 2, tw / 2, -d / 2 + tf, d / 2 - tf)
    cv.arrow(M(0, 0), M(-(bf / 2 + 12), 0), C["text"], 1.6, 8)
    cv.arrow(M(0, 0), M(0, -(d / 2 + 8)), C["text"], 1.6, 8)
    cv.math(M(-(bf / 2 + 12), 0), "x", 16, C["text"], "end", dx=-6, weight="700")
    cv.math(M(0, -(d / 2 + 8)), "y", 16, C["text"], dy=14, weight="700")
    cv.text(M(0, d / 2), "斷面", 12.5, C["muted"], dy=-16)


def yz_panel():
    sx = 560 / L_M
    cv = Canvas(PW, PH, sx=sx, ox=150, oy=170)
    cv.panel("y-z 面", None)
    A, B, Cc = (0, 0), (XB, 0), (L_M, 0)
    cv.line(A, Cc, C["member"], 4, cap="butt")
    cv.support(A, "roller", 0, size=13)
    cv.support(Cc, "pin", 0, size=13)
    for p, lab, dx in ((A, "A", 14), (Cc, "C", -14)):
        cv.text(p, lab, 15, C["text"], "start" if dx > 0 else "end", dx=dx, dy=-14, weight="700")
    # A 端偏心臂（−y 側＝圖上方）與 P（+z）
    e = ECC_PX / sx
    cv.line(A, (0, e), C["member"], 3.2, cap="butt")
    cv.arrow((-58 / sx, e), (0, e), C["load"], 2.8, 10)
    cv.math((-58 / sx, e), "P", 17, C["load"], "end", dx=-6, weight="700")
    cv.line((-70 / sx, 0), (-12 / sx, 0), C["dim"], 1, dash="3 3")
    cv.dim((-26 / sx, 0), (-26 / sx, e), "d", off=0, label_off=-14, size=16)
    # C 端 P（−z）沿軸線
    cv.arrow((L_M + 62 / sx, 0), (L_M + 2 / sx, 0), C["load"], 2.8, 10)
    cv.math((L_M + 62 / sx, 0), "P", 17, C["load"], "start", dx=6, weight="700")
    # H 於 B 向下（+y）
    cv.arrow((XB, 62 / sx), (XB, 2 / sx), C["load"], 2.8, 10)
    cv.math((XB, 62 / sx), "H", 17, C["load"], "start", dx=8, dy=4, weight="700")
    cv.text(B, "B", 15, C["text"], "start", dx=8, dy=34, weight="700")
    # L/2 尺寸
    cv.dim(A, B, "L/2", off=74, label_off=14, size=16)
    cv.dim(B, Cc, "L/2", off=74, label_off=14, size=16)
    # 座標軸：z 向右、y 向下
    ax = (L_M + 88 / sx, 0)
    cv.arrow(ax, (ax[0] + 40 / sx, 0), C["muted"], 1.6, 8)
    cv.math((ax[0] + 40 / sx, 0), "z", 15, C["muted"], "start", dx=6)
    cv.arrow((-110 / sx, -10 / sx), (-110 / sx, -58 / sx), C["muted"], 1.6, 8)
    cv.math((-110 / sx, -58 / sx), "y", 15, C["muted"], dy=12)
    _section(cv, PW - 80, PH - 118)
    return cv


def xz_panel():
    sx = 560 / L_M
    cv = Canvas(PW, PH, sx=sx, ox=150, oy=150)
    cv.panel("x-z 面", "A、B、C 三點側撐補強；H 沿 y 向（垂直此面）")
    A, B, Cc = (0, 0), (XB, 0), (L_M, 0)
    cv.line(A, Cc, C["member"], 4, cap="butt")
    for p, lab in ((A, "A"), (B, "B"), (Cc, "C")):
        cv.support(p, "roller", 0, size=12)
        cv.support(p, "roller", 180, size=12)
        cv.text(p, lab, 15, C["text"], dy=-56, weight="700")
    cv.text(B, "H", 15, C["load"], "start", dx=22, dy=-14, weight="700")
    cv.arrow((-62 / sx, 0), (-2 / sx, 0), C["load"], 2.8, 10)
    cv.math((-62 / sx, 0), "P", 17, C["load"], "end", dx=-6, weight="700")
    cv.arrow((L_M + 62 / sx, 0), (L_M + 2 / sx, 0), C["load"], 2.8, 10)
    cv.math((L_M + 62 / sx, 0), "P", 17, C["load"], "start", dx=6, weight="700")
    cv.text((L_M, 0), "（側撐補強）", 13, C["muted"], dy=62)
    ax = (L_M + 120 / sx, 0)
    cv.arrow(ax, (ax[0] + 48 / sx, 0), C["muted"], 1.6, 8)
    cv.math((ax[0] + 48 / sx, 0), "z", 15, C["muted"], "start", dx=6)
    cv.arrow((-110 / sx, -14 / sx), (-110 / sx, -62 / sx), C["muted"], 1.6, 8)
    cv.math((-110 / sx, -62 / sx), "x", 15, C["muted"], dy=12)
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([yz_panel(), xz_panel()], cols=1,
            title="SS-2008-4 題目附圖（重繪，考卷圖 3）",
            sub="依題目正本判讀清單 #1–#4、#6；L = 12 m、偏心 d = 25 cm、H = 2.5 t；偏心臂高度為示意放大",
            note="只有 A 端經剛臂偏心 d；C 端 P 直接作用在軸線上",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2008-4.md §1／§4，由下式即時算出
# ══════════════════════════════════════════════════════════════
import math
H_T, D_ECC, L_CM = 2.5, 25.0, 1200.0                 # t、cm、cm             §1
A_G, S_X, R_X, R_Y = 76.0, 851.0, 13.0, 4.91         # §1
F_Y, E_T = 2.5, 2040.0                               # §1
LX, LY = 1.0 * L_CM, 1.0 * L_CM / 2                  # K=1；B 點只束制弱軸   §4 Step 1
P_MD = 11.1                                          # 解析驗算代入值         §4 Step 6

CC  = math.sqrt(2 * math.pi**2 * E_T / F_Y)          # Step 2
KLRX, KLRY = LX / R_X, LY / R_Y
_k = KLRY / CC
FA  = (1 - KLRY**2 / (2 * CC**2)) * F_Y / (5/3 + 3*_k/8 - _k**3/8)   # 非彈性（KL/ry < Cc）
FBX = 0.6 * F_Y                                      # Step 3：兩式取大後蓋頂 0.6Fy
FEX = 12 * math.pi**2 * E_T / (23 * KLRX**2)         # Step 4


def m_ecc(x, P):   return P * D_ECC * (1 - x / L_CM)               # A 端偏心矩，線性至 C 為零
def m_h(x):        return H_T * L_CM / 4 * (x / (L_CM / 2) if x <= L_CM / 2 else (L_CM - x) / (L_CM / 2))
def m_tot(x, P):   return m_ecc(x, P) + m_h(x)                     # 兩者同向（皆使上緣受壓）
def eq1(P):        # 穩定式
    fa = P / A_G
    return fa / FA + 1.0 * (m_tot(L_CM / 2, P) / S_X) / ((1 - fa / FEX) * FBX)
def eq2(P):        # 強度式
    return P / A_G / (0.6 * F_Y) + (m_tot(L_CM / 2, P) / S_X) / FBX


def _root(f, lo, hi):
    for _ in range(200):
        mid = (lo + hi) / 2
        if (f(lo) - 1) * (f(mid) - 1) <= 0: hi = mid
        else: lo = mid
    return (lo + hi) / 2


P1 = _root(eq1, 0.0, 60.0)          # 小根（物理解）
P2 = _root(eq2, 0.0, 60.0)
P015 = 0.15 * FA * A_G              # fa/Fa = 0.15 之門檻
P1B  = _root(eq1, FEX * A_G + 1e-6, 400.0)   # 二次式的另一根（越過 F'ex·A 之後，無物理意義）


def fig1_bmd():
    W1, H1 = 1000, 420
    # ── 格 1：彎矩疊加（以 P = 11.1 t 代入）──
    cv = Canvas(W1, H1, sx=1)
    cv.panel("① 強軸彎矩疊加（y-z 面，P = 11.1 t 代入）", "A 端偏心矩（線性）＋ B 點 H（三角形），兩者同號")
    X0, X1, YB = 110, 830, 300                     # 像素；基線 YB，彎矩向上畫（受壓側在上）
    xs = [L_CM * i / 120 for i in range(121)]
    mmax = m_tot(L_CM / 2, P_MD)
    sc = 170 / mmax
    PX = lambda x: X0 + (X1 - X0) * x / L_CM
    cv.polygon([(X0, H1 - YB)] + [(PX(x), H1 - (YB - sc * m_tot(x, P_MD))) for x in xs] + [(X1, H1 - YB)],
               C["fill_m"], C["bmd"], 2.4)
    cv.poly([(PX(x), H1 - (YB - sc * m_ecc(x, P_MD))) for x in xs], C["accent"], 2.0, dash="7 5")
    cv.poly([(PX(x), H1 - (YB - sc * m_h(x))) for x in xs], C["sfd"], 2.0, dash="3 4")
    _hl(cv, H1, X0 - 10, YB, X1 + 10, YB, C["member"], 4.0)
    for x, nm in ((0, "A"), (L_CM / 2, "B"), (L_CM, "C")):
        cv.text_px(PX(x), YB + 22, nm, 15, C["text"], weight="700")
    ma, mb = m_tot(0, P_MD), m_tot(L_CM / 2, P_MD)
    cv.dot((PX(0), H1 - (YB - sc * ma)), 5, fill=C["bmd"])
    cv.dot((PX(L_CM / 2), H1 - (YB - sc * mb)), 5, fill=C["bmd"])
    cv.text_px(PX(0) - 4, YB - sc * ma - 40, f"MA = 25P = {ma:.1f}", 13, C["bmd"], "start", weight="700")
    cv.text_px(PX(L_CM / 2), YB - sc * mb - 16, f"MB = 12.5P + 750 = {mb:.1f} t·cm（最大）", 13.5,
               C["bmd"], weight="700")
    cv.legend(860 - 2, 150, [(C["accent"], "偏心矩 P·d"), (C["sfd"], "H 引起"), (C["bmd"], "合計")],
              size=12, gap=20)
    cv.text_px(W1 / 2, H1 - 34, f"MB > MA 的條件：12.5P + 750 > 25P ⇔ P 小於 {750 / 12.5:.0f} t；"
               f"本題 P ≈ {P_MD:g} t，最大彎矩在 B", 13, C["muted"])
    p1 = cv

    # ── 格 2：兩軸挫屈長度 ──
    cv = Canvas(W1, H1, sx=1)
    cv.panel("② 兩個方向的挫屈長度不同", "x-z 面 B 點側撐只擋弱軸；y-z 面 B 點無支承")
    for k, (yy, nm, nwave, klr, col) in enumerate(((150, "強軸（y-z 面）", 1, KLRX, C["muted"]),
                                                    (290, "弱軸（x-z 面）", 2, KLRY, C["load"]))):
        _hl(cv, H1, X0, yy, X1, yy, C["ghost"], 1.6, dash="6 5")
        amp = 46
        pts = [(X0 + (X1 - X0) * i / 200,
                H1 - (yy - amp * math.sin(math.pi * nwave * i / 200))) for i in range(201)]
        cv.poly(pts, col if k else C["deform"], 3.2)
        for j in range(nwave + 1):
            xx = X0 + (X1 - X0) * j / nwave
            cv.dot((xx, H1 - yy), 5.5, fill="#FFFFFF", stroke=C["member"], w=2.2)
        if nwave == 1:
            cv.dot(((X0 + X1) / 2, H1 - yy), 4, fill=C["ghost"])
        cv.text_px(X0 - 16, yy, nm, 13.5, C["text"], "end", weight="700")
        lab = (f"KL = {LX:.0f} cm，KL/rx = {KLRX:.1f}" if nwave == 1
               else f"KL = {LY:.0f} cm，KL/ry = {KLRY:.1f}（控制 Fa）")
        cv.text_px(X1, yy - 30 if k else yy + 30, lab, 13, col if k else C["deform"], "end", weight="700")
    cv.text_px(W1 / 2, H1 - 34, f"Fa 由弱軸 {KLRY:.1f} 控制 ⇒ Fa = {FA:.3f}；F'ex 用強軸 {KLRX:.1f} ⇒ F'ex = {FEX:.3f}（t/cm²）",
               13, C["muted"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-1-bmd.svg")
    compose([p1, p2], cols=1,
            title="圖 1　彎矩分佈與兩軸有效長度",
            sub=f"Lx = {LX:.0f} cm、Ly = {LY:.0f} cm；Cm = 1.0（題給）",
            note="同一根構材：Fa 看弱軸（B 點有側撐），F'ex 看強軸（彎曲平面、B 點沒有支承）",
            path=path)
    return path


def fig2_pmax():
    W1, H1 = 1000, 560
    cv = Canvas(W1, H1, sx=1)
    cv.panel("互制比隨 P 的變化", "兩式各自等於 1.0 時的 P；取較小者")
    X0, X1, YB, YT = 110, 900, 470, 110
    PM, RM = 30.0, 1.6
    PX = lambda p: X0 + (X1 - X0) * p / PM
    PY = lambda r: YB - (YB - YT) * r / RM
    cv.rect_px(X0, YT, PX(P015) - X0, YB - YT, "#EDF1F6", 0)
    cv.text_px((X0 + PX(P015)) / 2, YT + 18, "fa/Fa ≤ 0.15", 12, C["muted"])
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.6)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.6)
    for p in range(0, 31, 5):
        cv.text_px(PX(p), YB + 20, f"{p}", 12, C["muted"])
    for r in (0.0, 0.5, 1.0, 1.5):
        cv.text_px(X0 - 10, PY(r), f"{r:.1f}", 12, C["muted"], "end")
    cv.text_px((X0 + X1) / 2, YB + 46, "軸壓力 P（t）", 13, C["text"], weight="700")
    _hl(cv, H1, X0, PY(1.0), X1, PY(1.0), C["load"], 2.0, dash="6 4")
    ps = [PM * i / 300 for i in range(301)]
    cv.poly([(PX(p), H1 - PY(eq1(p))) for p in ps if eq1(p) < RM + 0.05], C["bmd"], 3.0)
    cv.poly([(PX(p), H1 - PY(eq2(p))) for p in ps], C["compr"], 3.0, dash="8 5")
    for p, col, lab, dx, anc, dy in ((P1, C["bmd"], f"穩定式 = 1 ⇒ P = {P1:.1f} t（控制）", -12, "end", -20),
                                     (P2, C["compr"], f"強度式 = 1 ⇒ P = {P2:.1f} t", 10, "start", 26)):
        cv.dot((PX(p), H1 - PY(1.0)), 6, fill=col)
        _hl(cv, H1, PX(p), PY(1.0), PX(p), YB, col, 1.4, dash="3 4")
        cv.text_px(PX(p) + dx, PY(1.0) + dy, lab, 13.5, col, anc, weight="700")
    cv.text_px(X0 + 10, PY(eq1(0)) + 30, f"P = 0 時已用掉 {eq1(0):.3f}（H 的彎矩）", 12.5, C["muted"], "start")
    cv.text_px(X1, PY(1.48), "穩定式（實線）", 12.5, C["bmd"], "end", weight="700")
    cv.text_px(X1, PY(0.62) , "強度式（虛線）", 12.5, C["compr"], "end", weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-2-pmax.svg")
    compose([cv], cols=1,
            title=f"圖 2　P 的上限由穩定式控制：Pmax ≈ {P1:.1f} t",
            sub=f"Fa = {FA:.3f}、Fbx = {FBX:.1f}、F'ex = {FEX:.3f}（t/cm²）；"
                f"fa/Fa = 0.15 對應 P = {P015:.2f} t",
            note=f"穩定式整理成二次式時另一根約 {P1B:.0f} t（已超過 F'ex·A = {FEX * A_G:.0f} t，放大係數變號），沒有物理意義",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把兩端都當偏心（變成均勻彎矩）；A 滾支／C 鉸支對調；x-z 面 B 點側撐漏看而弱軸用 12 m"),
    (fig1_bmd, "§4 Step 1–4",
     "最大彎矩取在 A（25P）而非 B；偏心矩與 H 彎矩相減；Fa 與 F'ex 用錯方向的有效長度"),
    (fig2_pmax, "§4 Step 5–6",
     "二次式取到大根；以強度式 22.2 t 為答案；P 小於門檻時仍套完整互制式"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
