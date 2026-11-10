#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2015-2 雙筋梁・最大設計彎矩與最大韌性 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2015-2.md §1 給定的原始資料；掃描表、c_u、k_y、φ_u、φ_y、μ
     一律由 state() / part2() 現算，檔尾對 §4 公佈值 assert。
  2. 改 §1 任一數字（b、d、d'、A's、f'_c）重跑，三張圖全部跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

FIGURES
  fig-1-scan       φMn 掃描與折點極大值   攔：把「最大鋼筋量」當成「最大設計彎矩」
  fig-2-part2      cu < d' 壓筋落拉力區    攔：Part(二) 沿用「壓力鋼筋」平衡式
  fig-3-tradeoff   強度－韌性抵換圖         攔：以為兩個小題可以同時最佳化
"""
import sys, os, math

sys.path.insert(0, os.environ.get(
    "STRUCTDRAW_DIR", "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose                       # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2015-2"

# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
B      = 35.0      # 斷面寬 cm
HH     = 70.0      # 斷面總深 cm
D      = 63.0      # 拉力鋼筋有效深度 cm
DP     = 7.0       # 壓力鋼筋有效深度 cm
FC     = 350.0
FY     = 4200.0
NRAT   = 7.0       # 題目給定彈性模數比
ASP    = 2 * 5.067  # 2-#8 壓力鋼筋 cm^2
ES     = 2.04e6
EPS_CU = 0.003

B1   = 0.85 if FC <= 280 else max(0.65, 0.85 - 0.05 * (FC - 280) / 70)
EPSY = FY / ES


def phi_of(et):
    if et >= 0.005: return 0.90
    if et <= EPSY:  return 0.65
    return 0.65 + 0.25 * (et - EPSY) / (0.005 - EPSY)


def state(c):
    """以中性軸深 c 為唯一參數，回傳整個斷面（Part 一的掃描用）。"""
    a = B1 * c
    esp = EPS_CU * (c - DP) / c
    fsp = min(ES * esp, FY)
    Cc = 0.85 * FC * a * B
    Cs = ASP * (fsp - 0.85 * FC)
    As = (Cc + Cs) / FY
    Mn = Cc * (D - a / 2) + Cs * (D - DP)
    et = EPS_CU * (D - c) / c
    return dict(c=c, a=a, esp=esp, fsp=fsp, As=As, Mn=Mn, et=et,
                phi=phi_of(et), phiMn=phi_of(et) * Mn)


def c_of_et(et): return EPS_CU / (EPS_CU + et) * D


def sig3(x):
    """取三位有效數字（§4 Part(二) 公佈曲率時使用的位數）。"""
    return 0.0 if x == 0 else round(x, -int(math.floor(math.log10(abs(x)))) + 2)


def ky_d(As):
    """彈性轉換斷面中性軸（A's 在壓力區）。"""
    qa = B / 2
    qb = (NRAT - 1) * ASP + NRAT * As
    qc = -((NRAT - 1) * ASP * DP + NRAT * As * D)
    return (-qb + math.sqrt(qb * qb - 4 * qa * qc)) / (2 * qa)


# ── Part 一：兩個端點與峰值 ──────────────────────────────
S004 = state(c_of_et(0.004))
S005 = state(c_of_et(0.005))
SCAN_ET = [0.0040, 0.0045, 0.0050, 0.0060, 0.0080, 0.0100]
SCAN = [state(c_of_et(e)) for e in SCAN_ET]
PEAK = max(SCAN, key=lambda s: s["phiMn"])

# ── Part 二：最小鋼筋量 → 最大韌性 ───────────────────────
RHO_MIN = 0.8 * math.sqrt(FC) / FY
# §4 Part(二) 逐步公佈的位數：As,min = 7.86、cu = 5.69、kyd = 11.97、εy = 0.00206。
# 圖上要與解題檔逐位相同，故此處沿用同一條四捨五入鏈。
AS_MIN  = round(RHO_MIN * B * D, 2)
EPSY_PUB = round(EPSY, 5)
# c_u < d'：A's 落在拉力區
qa = 0.85 * FC * B1 * B
qb = ASP * ES * EPS_CU - AS_MIN * FY
qc = -ASP * ES * EPS_CU * DP
CU2 = round((-qb + math.sqrt(qb * qb - 4 * qa * qc)) / (2 * qa), 2)
A2  = B1 * CU2
EPS_SP2 = EPS_CU * (DP - CU2) / CU2               # A's 的「拉」應變
TP2 = ASP * ES * EPS_SP2
T2  = AS_MIN * FY
MN2 = T2 * (D - A2 / 2) + TP2 * (DP - A2 / 2)
ET2 = EPS_CU * (D - CU2) / CU2
PHI2 = phi_of(ET2)
KYD2 = round(ky_d(AS_MIN), 2)
PHU2 = sig3(EPS_CU / CU2)
PHY2 = sig3(EPSY_PUB / (D - KYD2))
MU2  = PHU2 / PHY2

# ── 三種設計的抵換資料 ───────────────────────────────────
def design(As, c, Mn, phi):
    k = ky_d(As)
    return dict(As=As, cu=c, phiMn=phi * Mn / 1e5,
                phu=EPS_CU / c, phy=EPSY / (D - k), ky_d=k,
                mu=(EPS_CU / c) / (EPSY / (D - k)))


D_MAX_M = design(S005["As"], S005["c"], S005["Mn"], S005["phi"])   # 最大彎矩
D_004   = design(S004["As"], S004["c"], S004["Mn"], S004["phi"])   # 延性下限
D_MAX_U = dict(As=AS_MIN, cu=CU2, phiMn=PHI2 * MN2 / 1e5,
               phu=PHU2, phy=PHY2, ky_d=KYD2, mu=MU2)              # 最大韌性

# ══════════════════════════════════════════════════════════
# 共用繪圖框
# ══════════════════════════════════════════════════════════
class Frame:
    def __init__(self, W, H, xlim, ylim, L=100, R=160, T=96, Bm=96):
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

    def frame(self, yticks, xticks, yfmt="{:.0f}", xfmt="{:.3f}", xlabel=None, ylabel=None):
        cv = self.cv
        for v in yticks:
            cv.line(self.p(self.x0, v), self.p(self.x1, v), C["border"], 1.0)
            cv.math_px(cv.X(self.p(self.x0, v)[0]) - 10, cv.Y(self.p(self.x0, v)[1]),
                       yfmt.format(v), 12.5, C["muted"], "end")
        for v in xticks:
            cv.line(self.p(v, self.y0),
                    (self.p(v, self.y0)[0], self.p(v, self.y0)[1] - 7 / self.pw),
                    C["muted"], 1.4)
            cv.math_px(cv.X(self.p(v, self.y0)[0]), cv.Y(self.p(v, self.y0)[1]) + 22,
                       xfmt.format(v), 12, C["muted"])
        cv.line(self.p(self.x0, self.y0), self.p(self.x1, self.y0), C["muted"], 1.8)
        cv.line(self.p(self.x0, self.y0), self.p(self.x0, self.y1), C["muted"], 1.8)
        if xlabel:
            cv.text_px(cv.X(self.p(self.x1, self.y0)[0]) + 12,
                       cv.Y(self.p(self.x1, self.y0)[1]), xlabel, 13, C["muted"], "start")
        if ylabel:
            cv.text_px(cv.X(self.p(self.x0, self.y1)[0]) - 10,
                       cv.Y(self.p(self.x0, self.y1)[1]) - 24, ylabel, 13, C["muted"], "end")


# ══════════════════════════════════════════════════════════
# 圖 1　φMn 掃描：折點極大值
# ══════════════════════════════════════════════════════════
X0, X1 = 0.0038, 0.0105
F = Frame(880, 540, (X0, X1), (70.0, 145.0), L=104, R=176, T=100, Bm=110)
cv, P = F.cv, F.p
cv.panel("φM_n 的極大值落在「折點」，不是導數為零的地方", None)
cv.text_px(F.W / 2, 62, "縱軸單位 tf·m；A_s 可自由調整，故以中性軸深 c 為唯一參數掃描",
           12.5, C["muted"])

cv.polygon([P(X0, 70), P(0.004, 70), P(0.004, 145), P(X0, 145)], "rgba(192,57,43,0.10)")
F.frame([70, 85, 100, 115, 130, 145],
        [0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.010], xlabel="ε_t")

n = 240
ets = [0.004 + (X1 - 0.004) * i / n for i in range(n + 1)]
cv.poly([P(e, state(c_of_et(e))["Mn"] / 1e5) for e in ets], C["muted"], 2.4, dash="7 5")
cv.poly([P(e, state(c_of_et(e))["phiMn"] / 1e5) for e in ets], C["bmd"], 3.6)

# 規範可行區左界
cv.line(P(0.004, 70), P(0.004, 143), C["load"], 2.0, dash="4 5")
cv.text_px(cv.X(P(0.004, 0)[0]) + 8, F.T + 40, "梁 ε_t ≥ 0.004", 12.5, C["load"], "start",
           weight="700")
cv.text_px(cv.X(P(0.004, 0)[0]) + 8, F.T + 60, "（配筋上限）", 11.5, C["load"], "start")

# 拉力控制界限
cv.line(P(0.005, 70), P(0.005, 143), C["accent"], 2.0, dash="6 4")
cv.text_px(cv.X(P(0.005, 0)[0]) + 8, F.T + 96, "ε_t = 0.005：φ 觸頂 0.90", 12.5,
           C["accent"], "start", weight="700")

for s, lab, col in ((S004, "延性下限", C["muted"]), (S005, "峰值", C["accent"])):
    cv.dot(P(s["et"], s["phiMn"] / 1e5), 6.6 if s is S005 else 5.2,
           fill=col, stroke="#FFFFFF", w=2.0)
    cv.text_px(cv.X(P(s["et"], 0)[0]) + (12 if s is S005 else -10),
               cv.Y(P(0, s["phiMn"] / 1e5)[1]) + (-18 if s is S005 else 26),
               f"{lab} {s['phiMn']/1e5:.1f}", 13.5, col,
               "start" if s is S005 else "end", weight="700")
    cv.dot(P(s["et"], s["Mn"] / 1e5), 4.6, fill=C["muted"], stroke="#FFFFFF", w=1.6)

cv.text_px(cv.X(P(0.0088, 0)[0]), cv.Y(P(0, state(c_of_et(0.0088))["Mn"] / 1e5)[1]) - 16,
           "M_n（標稱）", 12.5, C["muted"])
cv.text_px(cv.X(P(0.0088, 0)[0]), cv.Y(P(0, state(c_of_et(0.0088))["phiMn"] / 1e5)[1]) + 20,
           "φM_n（設計）", 12.5, C["bmd"], weight="700")

cv.text_px(F.W / 2, F.H - 62,
           f"在 0.004→0.005 之間：φ 漲 "
           f"{100*(S005['phi']-S004['phi'])/S004['phi']:.1f}%，"
           f"M_n 只掉 {100*(S004['Mn']-S005['Mn'])/S004['Mn']:.1f}% → 乘積上升；"
           f"過了 0.005 之後 φ 被截平，乘積轉為下降",
           13, C["text"])
cv.text_px(F.W / 2, F.H - 36,
           f"max(φM_n) = {S005['phiMn']/1e5:.1f} tf·m（A_s = {S005['As']:.2f} cm²）"
           f"　不是 φ × max(M_n) = {S004['phiMn']/1e5:.1f}", 13.5, C["accent"], weight="700")
cv.save(f"{OUT}/{TAG}-fig-1-scan.svg")

# ══════════════════════════════════════════════════════════
# 圖 2　Part(二)：cu < d'，壓力鋼筋落在拉力區
# ══════════════════════════════════════════════════════════
PW, PH = 460, 560
sc = min((PW - 175) / B, (PH - 235) / HH)
MW = 84 / sc


def sect(cv, na, bars=4):
    cv.polygon([(0, 0), (B, 0), (B, HH), (0, HH)], "#EDF1F6", C["member"], 2.6)
    for i in range(bars):
        cv.dot((B * (0.18 + 0.64 * i / (bars - 1)), HH - D), 5.4,
               fill=C["tension"], stroke="#FFFFFF", w=1.5)
    for i in range(2):
        cv.dot((B * (0.24 + 0.52 * i), HH - DP), 5.4,
               fill=C["tension"], stroke="#FFFFFF", w=1.5)


g1 = Canvas(PW, PH, sx=sc, ox=PW / 2 - B * sc / 2, oy=PH - 128 - HH * sc)
g1.panel("最小拉力鋼筋時的斷面", f"b × h = {B:.0f} × {HH:.0f} cm，As,min = {AS_MIN:.2f} cm²".format(AS_MIN=AS_MIN))
sect(g1, CU2)
g1.line((0, HH - CU2), (B, HH - CU2), C["accent"], 2.2, dash="7 4")
g1.math_px(g1.X(B) + 8, g1.Y(HH - CU2), f"c_{{u}}={CU2:.2f}", 12.5, C["accent"], "start",
           weight="700")
g1.line((0, HH - DP), (B, HH - DP), C["muted"], 1.4, dash="4 4")
g1.math_px(g1.X(0) - 8, g1.Y(HH - DP), f"d'={DP:.0f}", 12.5, C["muted"], "end", weight="700")
g1.dim((B, HH), (B, HH - D), f"d={D:.0f}", off=-40, label_off=-13)
g1.text_px(PW / 2, PH - 96, f"c_{{u}} = {CU2:.2f} cm  小於  d' = {DP:.0f} cm",
           14, C["load"], weight="700")
g1.text_px(PW / 2, PH - 72, "→ A's 落在中性軸「下方」＝拉力區", 12.5, C["load"], weight="700")
g1.text_px(PW / 2, PH - 46, "兩排鋼筋同為紅色（都受拉），這不是筆誤", 12, C["muted"])

g2 = Canvas(PW, PH, sx=sc, ox=PW * 0.44, oy=PH - 128 - HH * sc)
g2.panel("應變與三個力", "壓力只剩混凝土提供")
g2.line((0, 0), (0, HH), C["ghost"], 2, dash="5 4")
wc = MW * CU2 / (D - CU2)
g2.polygon([(0, HH), (wc, HH), (0, HH - CU2)], C["fill_c"], C["compr"], 2.4)
g2.polygon([(0, HH - CU2), (-MW, HH - D), (0, HH - D)], C["fill_t"], C["tension"], 2.4)
g2.line((-MW * 1.2, HH - CU2), (MW * 1.2, HH - CU2), C["accent"], 1.8, dash="6 4")
g2.text_px(g2.X(MW * 1.2) + 4, g2.Y(HH - CU2), "N.A.", 12, C["accent"], "start", weight="700")
g2.math_px(g2.X(wc) + 6, g2.Y(HH) - 13, "ε_{cu}=0.003", 12, C["compr"], "start", weight="700")
g2.math_px(g2.X(-MW) - 6, g2.Y(HH - D), f"ε_{{t}}={ET2:.4f}", 12, C["tension"], "end",
           weight="700")
wsp = MW * (DP - CU2) / (D - CU2)
g2.arrow((0, HH - DP), (-wsp - MW * 0.30, HH - DP), C["tension"], 2.6, 9)
g2.math_px(g2.X(-wsp - MW * 0.30) - 5, g2.Y(HH - DP) - 14,
           f"T'={TP2/1000:.1f}k", 12, C["tension"], "end", weight="700")
g2.arrow((0, HH - D), (-MW * 1.05, HH - D), C["tension"], 3.2, 10)
g2.math_px(g2.X(-MW * 0.52), g2.Y(HH - D) - 15, f"T={T2/1000:.1f}k", 12.5, C["tension"],
           weight="700")
g2.arrow((MW * 0.20, HH - A2 / 2), (MW * 1.15, HH - A2 / 2), C["compr"], 3.0, 10)
g2.math_px(g2.X(MW * 1.15) + 5, g2.Y(HH - A2 / 2), f"C_{{c}}={0.85*FC*A2*B/1000:.1f}k",
           12, C["compr"], "start", weight="700")
g2.text_px(PW / 2, PH - 96, f"ε'_{{s}}（拉）= {EPS_SP2:.6f}  小於  ε_{{y}}",
           12.5, C["muted"])
g2.text_px(PW / 2, PH - 72, "對 C_c 作用線取矩：兩個拉力都要算", 12.5, C["text"], weight="700")
g2.text_px(PW / 2, PH - 46, f"M_{{n}} = {MN2/1e5:.1f} tf·m　φM_{{n}} = {PHI2*MN2/1e5:.1f} tf·m",
           13.5, C["bmd"], weight="700")

compose([g1, g2],
        title=f"{TAG}　Part(二)：鋼筋一少，「壓力鋼筋」就變成拉力鋼筋",
        sub=(f"ρmin = 0.8√f'c/fy = {RHO_MIN:.6f}　→　As,min = {AS_MIN:.2f} cm²"
             f"（A's = {ASP:.3f} cm² 固定不變）"),
        note=(f"只算 As,min 那一項會少掉約 {100*TP2*(DP-A2/2)/MN2:.0f}% 的彎矩；"
              f"φu = εcu/cu = {PHU2*1e4:.2f}e-4、φy = {PHY2*1e5:.2f}e-5 rad/cm "
              f"→ μ = {MU2:.1f}"),
        path=f"{OUT}/{TAG}-fig-2-part2.svg")

# ══════════════════════════════════════════════════════════
# 圖 3　強度－韌性抵換
# ══════════════════════════════════════════════════════════
F = Frame(860, 520, (0.0, 15.0), (0.0, 130.0), L=104, R=170, T=100, Bm=110)
cv, P = F.cv, F.p
cv.panel("強度與韌性是同一條曲線的兩端", "橫軸：曲率韌性 μ = φu/φy　縱軸：φM_n（tf·m）")

F.frame([0, 25, 50, 75, 100, 125], [0, 3, 6, 9, 12, 15],
        yfmt="{:.0f}", xfmt="{:.0f}", xlabel="μ")

# 由 c 掃出的完整抵換曲線（規範可行範圍 εt ≥ 0.004）
pts = []
for i in range(200):
    et = 0.004 + (0.060 - 0.004) * i / 199
    c = c_of_et(et)
    s = state(c)
    As = s["As"]
    if As < AS_MIN: break
    k = ky_d(As)
    pts.append(P((EPS_CU / c) / (EPSY / (D - k)), s["phiMn"] / 1e5))
cv.poly(pts, C["muted"], 2.6, dash="7 5")

def fmt_mu(v): return f"{v:.2f}" if v < 10 else f"{v:.1f}"


LBL = ((D_MAX_M, "(一) 最大設計彎矩", C["accent"], 4.2, 124.0),
       (D_004,   "延性下限 ε_t = 0.004", C["muted"], 4.2, 100.0),
       (D_MAX_U, "(二) 最大韌性", C["bmd"], 6.6, 56.0))
for d_, lab, col, lx, ly in LBL:
    cv.dot(P(d_["mu"], d_["phiMn"]), 6.8, fill=col, stroke="#FFFFFF", w=2.2)
    cv.line(P(d_["mu"], d_["phiMn"]), P(lx - 0.15, ly - 3.0), col, 1.2, dash="3 3")
    cv.text_px(cv.X(P(lx, 0)[0]), cv.Y(P(0, ly)[1]), lab, 13.5, col, "start", weight="700")
    cv.text_px(cv.X(P(lx, 0)[0]), cv.Y(P(0, ly)[1]) + 20,
               f"A_s = {d_['As']:.2f} cm^{{2}}　μ = {fmt_mu(d_['mu'])}　"
               f"φM_n = {d_['phiMn']:.1f} tf·m", 12, col, "start")

cv.text_px(F.W / 2, F.H - 58,
           f"從 (一) 走到 (二)：A_s 由 {D_MAX_M['As']:.1f} 降到 {D_MAX_U['As']:.1f} cm²，"
           f"韌性漲 {D_MAX_U['mu']/D_MAX_M['mu']:.1f} 倍，強度只剩 "
           f"{100*D_MAX_U['phiMn']/D_MAX_M['phiMn']:.0f}%", 13.5, C["text"], weight="700")
cv.text_px(F.W / 2, F.H - 32,
           "兩個小題問的是同一條曲線的兩個端點，不可能同時達成", 12.5, C["muted"])
cv.save(f"{OUT}/{TAG}-fig-3-tradeoff.svg")

# ══════════════════════════════════════════════════════════
# 對 .md §4 公佈值 assert
# ══════════════════════════════════════════════════════════
assert abs(B1 - 0.80) < 1e-9,                B1
assert abs(S004["c"] - 27.00) < 0.01,        S004["c"]
assert abs(S004["a"] - 21.60) < 0.01,        S004["a"]
assert abs(S004["As"] - 62.97) < 0.02,       S004["As"]
assert abs(S004["Mn"] / 1e5 - 139.55) < 0.05, S004["Mn"] / 1e5
assert abs(S004["phi"] - 0.815) < 5e-4,      S004["phi"]
assert abs(S004["phiMn"] / 1e5 - 113.7) < 0.1, S004["phiMn"] / 1e5
assert abs(S005["c"] - 23.625) < 0.005,      S005["c"]
assert abs(S005["a"] - 18.90) < 0.01,        S005["a"]
assert abs(S005["esp"] - 0.002111) < 5e-6,   S005["esp"]
assert abs(S005["As"] - 56.27) < 0.02,       S005["As"]
assert abs(S005["Mn"] / 1e5 - 127.53) < 0.05, S005["Mn"] / 1e5
assert abs(S005["phiMn"] / 1e5 - 114.8) < 0.05, S005["phiMn"] / 1e5
assert PEAK is S005 or abs(PEAK["et"] - 0.005) < 1e-9
for s, want in zip(SCAN, (113.7, 114.3, 114.8, 105.3, 89.3, 77.0)):
    assert abs(s["phiMn"] / 1e5 - want) < 0.06, (s["et"], s["phiMn"] / 1e5, want)
assert abs(RHO_MIN - 0.003564) < 1e-6,       RHO_MIN
assert abs(AS_MIN - 7.86) < 1e-9,            AS_MIN
assert abs(CU2 - 5.69) < 1e-9,               CU2
assert abs(EPS_SP2 - 0.000691) < 5e-6,       EPS_SP2
assert abs(KYD2 - 11.97) < 1e-9,             KYD2
assert abs(PHU2 - 5.27e-4) < 5e-7,           PHU2
assert abs(PHY2 - 4.04e-5) < 5e-8,           PHY2
assert abs(MU2 - 13.0) < 0.05,               MU2
assert abs(MN2 / 1e5 - 20.7) < 0.1,          MN2 / 1e5
assert abs(PHI2 * MN2 / 1e5 - 18.6) < 0.1,   PHI2 * MN2 / 1e5
assert abs(D_MAX_M["ky_d"] - 27.15) < 0.05,  D_MAX_M["ky_d"]
assert abs(D_004["ky_d"] - 28.29) < 0.05,    D_004["ky_d"]
assert abs(D_MAX_M["mu"] - 2.21) < 0.02,     D_MAX_M["mu"]
assert abs(D_004["mu"] - 1.87) < 0.02,       D_004["mu"]
print(f"{TAG}: 3 圖 OK　峰值 φMn={S005['phiMn']/1e5:.1f}（εt=0.005, As={S005['As']:.2f}）"
      f"　0.004 端 {S004['phiMn']/1e5:.1f}　|| cu={CU2:.2f} kyd={KYD2:.2f} μ={MU2:.1f} "
      f"φMn2={PHI2*MN2/1e5:.1f}")
