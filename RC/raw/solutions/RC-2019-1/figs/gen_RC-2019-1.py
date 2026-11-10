#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2019-1 單筋矩形梁・過渡區 φ 聯立求 As — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2019-1.md §1 給定的原始資料；a、c、εt、φ、As
     一律由下方函式現算，檔尾對 §4 公佈值 assert。
  2. 改 §1 任一數字（b、d、f'c、fy、Mu）重跑，三張圖全部跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

FIGURES
  fig-1-section    斷面／應變／應力三聯   攔：把 c 當 a（或反之）、忘記 T = Cc 才定出 a
  fig-2-phi-et     φ–εt 內插圖            攔：φ 直接取 0.9、εy 用 0.002、內插方向畫反
  fig-3-roots      二次方程雙根取捨        攔：取到大根 90.3 cm² 交卷
"""
import sys, os, math

sys.path.insert(0, os.environ.get(
    "STRUCTDRAW_DIR", "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose                     # noqa: E402
from recipes import rc_flexure                                 # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2019-1"

# ══════════════════════════════════════════════════════════
# §1 原始給定（RC-2019-1.md §1「原始題目重述」）
# ══════════════════════════════════════════════════════════
B      = 50.0        # 梁寬 (cm)
H      = 70.0        # 全斷面深 (cm)
D      = 63.0        # 有效深度 (cm)
FC     = 210.0       # f'c (kgf/cm^2)
FY     = 4200.0      # fy  (kgf/cm^2)
ES     = 2.04e6      # 土木 401-100
EPS_CU = 0.003
MU     = 85.72e5     # 設計彎矩 (kgf·cm)

# ── 由上列推得（不得手打） ────────────────────────────────
B1   = 0.85 if FC <= 280 else max(0.65, 0.85 - 0.05 * (FC - 280) / 70)
EPSY = FY / ES
KA   = FY / (0.85 * FC * B)          # a  = KA · As
KC   = KA / B1                       # c  = KC · As


def phi_of(et):
    """土木 401-100 現行式（箍筋圍束，壓力控制界限 ε_ty = fy/Es）。"""
    if et >= 0.005:  return 0.90
    if et <= EPSY:   return 0.65
    return 0.65 + 0.25 * (et - EPSY) / (0.005 - EPSY)


def state(As):
    a = KA * As
    c = a / B1
    et = EPS_CU * (D - c) / c
    return dict(a=a, c=c, et=et, phi=phi_of(et), Mn=As * FY * (D - a / 2))


def phi_lin(As):
    """把過渡區內插式**不設限**地外推（§4.4 建立二次方程時的假設）。"""
    et = EPS_CU * (D - KC * As) / (KC * As)
    return 0.65 + 0.25 * (et - EPSY) / (0.005 - EPSY)


# ── 解 φMn = Mu（物理解：φ 依 state() 夾在 0.65~0.90） ──
lo, hi = 5.0, 60.0
for _ in range(200):
    m = (lo + hi) / 2
    s = state(m)
    if s["phi"] * s["Mn"] < MU: lo = m
    else:                        hi = m
AS = (lo + hi) / 2
S = state(AS)

# ── §4.4 二次方程的兩根（把內插式外推後的代數解） ──
QA = 0.25 / (0.005 - EPSY) * (EPS_CU * D / KC)      # = 29.017…  (1/As 項係數)
QB = 0.65 - 0.25 / (0.005 - EPSY) * (EPS_CU + EPSY)  # = 0.220…   (常數項)
# (QB·As + QA)·fy·(D − KA·As/2) = MU
qa = -QB * KA / 2
qb = QB * D - QA * KA / 2
qc = QA * D - MU / FY
disc = qb * qb - 4 * qa * qc
ROOT_S = (-qb + math.sqrt(disc)) / (2 * qa)          # 小根（有效）
ROOT_L = (-qb - math.sqrt(disc)) / (2 * qa)          # 大根（εt < εy，無效）
if ROOT_S > ROOT_L: ROOT_S, ROOT_L = ROOT_L, ROOT_S

AS_MIN = max(0.8 * math.sqrt(FC) / FY, 14 / FY) * B * D
RHO_B  = 0.85 * B1 * FC / FY * 6120 / (6120 + FY)

# ══════════════════════════════════════════════════════════
# 圖 1　斷面／應變／應力三聯
# ══════════════════════════════════════════════════════════
rc_flexure(
    B, H, D, S["c"], S["a"],
    labels={
        "eps_cu": f"ε_{{cu}}=0.003",
        "eps_s":  f"ε_{{t}}={S['et']:.5f}",
        "fc":     f"0.85f'_{{c}}={0.85*FC:.0f}",
        "Cc":     f"C_{{c}}={0.85*FC*S['a']*B/1000:.1f}×10^{{3}}kgf",
        "T":      f"T=A_{{s}}f_{{y}}",
        "c":      f"c={S['c']:.2f}",
        "a":      f"a={S['a']:.2f}",
        "b":      f"b={B:.0f}", "h": f"h={H:.0f}", "d": f"d={D:.0f}",
    },
    title=f"{TAG}　單筋矩形梁：斷面／應變／等值應力塊",
    note=(f"a = β1·c = {B1:.2f}×{S['c']:.2f} = {S['a']:.2f} cm；"
          f"a 永遠比 c 淺 —— 圖上若 a 比 c 深，就是 β1 用錯了"),
    path=f"{OUT}/{TAG}-fig-1-section.svg")

# ══════════════════════════════════════════════════════════
# 通用 XY 繪圖框：資料座標 → 正規化模型座標（1 模型單位 = 繪圖區寬）
# ══════════════════════════════════════════════════════════
class Frame:
    def __init__(self, W, H, xlim, ylim, L=96, R=150, T=92, Bm=84):
        self.W, self.H = W, H
        self.x0, self.x1 = xlim
        self.y0, self.y1 = ylim
        self.pw, self.ph = W - L - R, H - T - Bm
        self.asp = self.ph / self.pw
        self.cv = Canvas(W, H, sx=self.pw, ox=L, oy=Bm)
        self.L, self.T, self.Bm = L, T, Bm

    def p(self, x, y):
        return ((x - self.x0) / (self.x1 - self.x0),
                (y - self.y0) / (self.y1 - self.y0) * self.asp)

    def px(self, n):            # n 像素 → 模型單位
        return n / self.pw

    def frame(self, yticks, xticks, yfmt="{:.2f}", xfmt="{:.3f}",
              xlabel=None, ylabel=None, grid=True):
        cv = self.cv
        for v in yticks:
            if grid:
                cv.line(self.p(self.x0, v), self.p(self.x1, v), C["border"], 1.0)
            cv.math_px(cv.X(self.p(self.x0, v)[0]) - 10,
                       cv.Y(self.p(self.x0, v)[1]), yfmt.format(v), 12.5, C["muted"], "end")
        for v in xticks:
            cv.line(self.p(v, self.y0), (self.p(v, self.y0)[0],
                                         self.p(v, self.y0)[1] - self.px(7)), C["muted"], 1.4)
            cv.math_px(cv.X(self.p(v, self.y0)[0]),
                       cv.Y(self.p(v, self.y0)[1]) + 22, xfmt.format(v), 12, C["muted"])
        cv.line(self.p(self.x0, self.y0), self.p(self.x1, self.y0), C["muted"], 1.8)
        cv.line(self.p(self.x0, self.y0), self.p(self.x0, self.y1), C["muted"], 1.8)
        if xlabel:
            cv.text_px(cv.X(self.p(self.x1, self.y0)[0]) + 14,
                       cv.Y(self.p(self.x1, self.y0)[1]), xlabel, 14.5, C["muted"], "start")
        if ylabel:
            cv.math_px(cv.X(self.p(self.x0, self.y1)[0]) - 10,
                       cv.Y(self.p(self.x0, self.y1)[1]) - 22, ylabel, 15, C["muted"], "end")


# ══════════════════════════════════════════════════════════
# 圖 2　φ–εt 內插圖
# ══════════════════════════════════════════════════════════
F = Frame(780, 470, (0.0, 0.0075), (0.62, 0.95))
cv, P = F.cv, F.p
cv.panel("強度折減因數 φ 與淨拉應變 ε_t", None)
cv.text_px(F.W / 2, 60, "土木401-100 現行式（箍筋圍束）", 12.5, C["muted"])

# 三區底色（先畫，才不會蓋住線）
cv.polygon([P(0.0, 0.62), P(EPSY, 0.62), P(EPSY, 0.95), P(0.0, 0.95)], "rgba(29,78,216,0.07)")
cv.polygon([P(0.005, 0.62), P(0.0075, 0.62), P(0.0075, 0.95), P(0.005, 0.95)],
           "rgba(192,57,43,0.07)")
F.frame([0.65, 0.70, 0.75, 0.80, 0.85, 0.90],
        [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007],
        xlabel="ε_t", ylabel="φ")

# 三段折線（壓力控制平台／過渡區／拉力控制平台）
seg = [P(0.0, 0.65), P(EPSY, 0.65)]
seg += [P(EPSY + (0.005 - EPSY) * i / 24,
          phi_of(EPSY + (0.005 - EPSY) * i / 24)) for i in range(25)]
seg += [P(0.0075, 0.90)]
cv.poly(seg, C["bmd"], 3.6)

cv.text_px((cv.X(P(0.0, 0)[0]) + cv.X(P(EPSY, 0)[0])) / 2, F.T + 34,
           "壓力控制", 12.5, C["compr"], weight="700")
cv.text_px((cv.X(P(EPSY, 0)[0]) + cv.X(P(0.005, 0)[0])) / 2, F.T + 34,
           "過渡區", 12.5, C["accent"], weight="700")
cv.text_px((cv.X(P(0.005, 0)[0]) + cv.X(P(0.0075, 0)[0])) / 2, F.T + 34,
           "拉力控制", 12.5, C["tension"], weight="700")

# εty 與 0.005 兩個折點
for et in (EPSY, 0.005):
    cv.line(P(et, 0.62), P(et, 0.928), C["muted"], 1.6, dash="6 4")
    cv.dot(P(et, phi_of(et)), 5.0, fill=C["bmd"], stroke="#FFFFFF", w=1.8)
cv.math_px(cv.X(P(EPSY, 0)[0]) - 10, cv.Y(P(0, 0.690)[1]),
           f"ε_{{ty}}={EPSY:.6f}", 13, C["bmd"], "end", weight="700")
cv.math_px(cv.X(P(0.005, 0)[0]) + 10, cv.Y(P(0, 0.868)[1]),
           "0.005", 13, C["bmd"], "start", weight="700")

# 梁的配筋上限 0.004
cv.line(P(0.004, 0.62), P(0.004, 0.928), C["load"], 1.8, dash="4 5")
cv.math_px(cv.X(P(0.004, 0)[0]) - 10, cv.Y(P(0, 0.730)[1]),
           "0.004", 13, C["load"], "end", weight="700")
cv.text_px(cv.X(P(0.004, 0)[0]) - 10, cv.Y(P(0, 0.703)[1]),
           "梁配筋上限", 12, C["load"], "end")

# 本題解
cv.dot(P(S["et"], S["phi"]), 6.4, fill=C["accent"], stroke="#FFFFFF", w=2.2)
cv.text_px(cv.X(P(0.00512, 0)[0]), cv.Y(P(0, 0.800)[1]),
           f"本題 ε_{{t}}={S['et']:.5f}", 13.5, C["accent"], "start", weight="700")
cv.math_px(cv.X(P(0.00512, 0)[0]), cv.Y(P(0, 0.775)[1]),
           f"→ φ={S['phi']:.4f}", 13.5, C["accent"], "start", weight="700")
cv.line(P(S["et"], S["phi"]), P(0.00505, 0.795), C["accent"], 1.4, dash="3 3")

cv.text_px(F.W / 2, F.H - 34,
           f"ε_{{ty}} = f_{{y}}/E_{{s}} = {EPSY:.6f}（不是 0.002）；"
           f"ε_{{t}} 越大 φ 越大，不是越小",
           13, C["muted"])
cv.save(f"{OUT}/{TAG}-fig-2-phi-et.svg")

# ══════════════════════════════════════════════════════════
# 圖 3　二次方程雙根取捨
# ══════════════════════════════════════════════════════════
A_LO, A_HI = 20.0, 105.0
Y_LO, Y_HI = 76.0, 96.0
F = Frame(830, 500, (A_LO, A_HI), (Y_LO, Y_HI), L=96, R=196, T=92, Bm=92)
cv, P = F.cv, F.p
cv.panel("為什麼二次方程的大根必須捨棄", None)
cv.text_px(F.W / 2, 60, "縱軸：設計彎矩強度 φM_n（tf·m）　橫軸：拉力鋼筋量 A_s（cm²）",
           12.5, C["muted"])

as_ey = EPS_CU * D / (KC * (EPS_CU + EPSY))          # ε_t = ε_ty 的 A_s
cv.polygon([P(as_ey, Y_LO), P(A_HI, Y_LO), P(A_HI, Y_HI), P(as_ey, Y_HI)],
           "rgba(107,118,132,0.10)")
F.frame([78, 82, 86, 90, 94], [20, 40, 60, 80, 100],
        yfmt="{:.0f}", xfmt="{:.0f}", xlabel="A_s")


def clipped(f, n=400):
    """把落在 y 範圍外的點切掉，回傳可畫的分段。"""
    segs, cur = [], []
    for i in range(n + 1):
        x = A_LO + (A_HI - A_LO) * i / n
        y = f(x)
        if Y_LO <= y <= Y_HI:
            cur.append(P(x, y))
        elif cur:
            segs.append(cur); cur = []
    if cur: segs.append(cur)
    return segs


for seg in clipped(lambda x: phi_lin(x) * x * FY * (D - KA * x / 2) / 1e5):
    cv.poly(seg, C["muted"], 2.6, dash="7 5")
for seg in clipped(lambda x: state(x)["phi"] * state(x)["Mn"] / 1e5):
    cv.poly(seg, C["bmd"], 3.6)

cv.line(P(A_LO, MU / 1e5), P(A_HI, MU / 1e5), C["load"], 2.4, dash="8 5")
cv.math_px(cv.X(P(A_LO, 0)[0]) + 8, cv.Y(P(0, MU / 1e5)[1]) - 13,
           f"M_u={MU/1e5:.2f} tf·m", 13.5, C["load"], "start", weight="700")

cv.line(P(as_ey, Y_LO), P(as_ey, Y_HI - 0.6), C["load"], 1.8, dash="4 5")
cv.math_px(cv.X(P(as_ey, 0)[0]) + 8, cv.Y(P(0, Y_HI - 1.2)[1]),
           "ε_{t} = ε_{ty}", 12.5, C["load"], "start", weight="700")
cv.text_px((cv.X(P(as_ey, 0)[0]) + cv.X(P(A_HI, 0)[0])) / 2, cv.Y(P(0, Y_HI - 3.0)[1]),
           "此區鋼筋未降伏，內插式不成立", 12, C["muted"])

cv.dot(P(ROOT_S, MU / 1e5), 6.6, fill=C["accent"], stroke="#FFFFFF", w=2.2)
cv.math_px(cv.X(P(ROOT_S, 0)[0]) - 8, cv.Y(P(0, 82.6)[1]),
           f"A_s={ROOT_S:.1f} cm^{{2}}  ✓", 14, C["accent"], "middle", weight="700")
cv.text_px(cv.X(P(ROOT_S, 0)[0]) - 8, cv.Y(P(0, 81.4)[1]),
           f"ε_t = {state(ROOT_S)['et']:.5f}，落在過渡區", 12, C["accent"])
cv.line(P(ROOT_S, MU / 1e5), P(ROOT_S - 1.2, 83.4), C["accent"], 1.4, dash="3 3")

etL = EPS_CU * (D - KC * ROOT_L) / (KC * ROOT_L)
cv.dot(P(ROOT_L, MU / 1e5), 6.6, fill=C["muted"], stroke="#FFFFFF", w=2.2)
cv.math_px(cv.X(P(ROOT_L, 0)[0]) + 10, cv.Y(P(0, 79.4)[1]),
           f"A_s={ROOT_L:.1f} cm^{{2}}  ×", 14, C["muted"], "start", weight="700")
cv.text_px(cv.X(P(ROOT_L, 0)[0]) + 10, cv.Y(P(0, 78.2)[1]),
           f"ε_t = {etL:.5f}，鋼筋未降伏", 12, C["muted"], "start")
cv.line(P(ROOT_L, MU / 1e5), P(ROOT_L + 1.2, 80.2), C["muted"], 1.4, dash="3 3")

cv.legend(F.L + 14, F.T + 34, [(C["bmd"], "物理解：φ 夾在 0.65～0.90"),
                               (C["muted"], "代數解：內插式外推（二次方程本體）")])
cv.text_px(F.W / 2, F.H - 26,
           "兩條曲線在 φ 觸頂／觸底處分家 —— 大根只存在於外推的灰虛線上",
           13, C["muted"])
cv.save(f"{OUT}/{TAG}-fig-3-roots.svg")

# ══════════════════════════════════════════════════════════
# 對 .md §4 公佈值 assert（圖上任何數字都必須撐得住這一關）
# ══════════════════════════════════════════════════════════
assert abs(B1 - 0.85) < 1e-9
assert abs(EPSY - 0.002059) < 5e-7,          EPSY
assert abs(KA - 0.4706) < 5e-5,              KA
assert abs(KC - 0.5536) < 5e-5,              KC
assert abs(AS - 45.52) < 0.01,               AS
assert abs(S["a"] - 21.42) < 0.01,           S["a"]
assert abs(S["c"] - 25.20) < 0.01,           S["c"]
assert abs(S["et"] - 0.00450) < 5e-6,        S["et"]
assert abs(S["phi"] - 0.8575) < 5e-5,        S["phi"]
assert abs(ROOT_S - 45.5) < 0.1,             ROOT_S
assert abs(ROOT_L - 90.3) < 0.1,             ROOT_L
assert abs(AS_MIN - 10.50) < 0.01,           AS_MIN
assert abs(RHO_B - 0.02143) < 1e-5,          RHO_B
print(f"{TAG}: 3 圖 OK　As={AS:.2f} a={S['a']:.2f} c={S['c']:.2f} "
      f"εt={S['et']:.5f} φ={S['phi']:.4f}　roots=({ROOT_S:.2f}, {ROOT_L:.2f}) "
      f"As,min={AS_MIN:.2f} ρb={RHO_B:.5f}")
