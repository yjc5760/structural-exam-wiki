#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2012-1 懸臂後拉預力梁・初始階段應力檢核 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2012-1.md §1 給定的原始資料；A、I、S、P_i、M_sw、四個應力、
     容許值、超限段長度、補充鋼筋量一律現算，檔尾對 §4 公佈值 assert。
  2. 改 §1 任一數字（L、e、根數、f'_c、w_c）重跑，三張圖全部跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

FIGURES
  fig-1-eccentricity 懸臂彎矩與偏心方向  攔：套用簡支梁經驗把鋼鍵放到重心下方
  fig-2-stress       固定端／自由端四應力 攔：只檢核固定端，漏掉自由端底纖維
  fig-3-overrun      底纖維應力沿梁長分布 攔：以為只有自由端那一個點超限
"""
import sys, os, math

sys.path.insert(0, os.environ.get(
    "STRUCTDRAW_DIR", "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose                       # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2012-1"

# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
B     = 30.0        # 斷面寬 (cm)
H     = 90.0        # 斷面高 (cm)
L     = 610.0       # 懸臂長 (cm)
ECC   = 30.0        # 偏心距（全長固定，鋼鍵在重心上方）
FC    = 350.0
FPU   = 19_000.0
APS_1 = 0.9871      # 單根 12.7 mm 七線絞 (cm^2)
N_TEN = 3           # 根數
WC    = 2.3         # 混凝土單位重 tf/m^3
FY    = 4_200.0     # §4 Step 7 假設值（原卷未給，已在 md 註明）

# ── 斷面與容許值 ────────────────────────────────────────
A  = B * H
I  = B * H**3 / 12
S  = I / (H / 2)
FCI = 0.7 * FC
ALW_C = 0.60 * FCI                 # 壓應力容許
ALW_T = 0.80 * math.sqrt(FCI)      # 拉應力容許
FR_CI = 2.0 * math.sqrt(FCI)       # 初始階段開裂模數
FR_C  = 2.0 * math.sqrt(FC)

# ── 初始預力與自重 ──────────────────────────────────────
FPI  = 0.75 * FPU
APS  = N_TEN * APS_1
PI_F = FPI * APS
W    = WC * (B / 100) * (H / 100) * 1000 / 100      # kgf/cm
MSW  = W * L**2 / 2

R2 = lambda x: round(x, 2)
PA  = R2(PI_F / A)                 # 軸壓分量
PES = R2(PI_F * ECC / S)           # 偏心分量
MS  = R2(MSW / S)                  # 自重彎矩分量

# 壓為負、拉為正（依 §4 Step 5 的符號規定）
FIX_TOP  = R2(-PA - PES + MS)
FIX_BOT  = R2(-PA + PES - MS)
FREE_TOP = R2(-PA - PES)
FREE_BOT = R2(-PA + PES)

# ── Step 6b：超限區段 ───────────────────────────────────
def f_bot(xi):
    """距自由端 ξ 處的底纖維應力（拉為正）。"""
    return (PES - PA) - MS * (xi / L)**2


XI_LIM  = L * math.sqrt(((PES - PA) - ALW_T) / MS)   # 超出容許拉應力的區段
XI_ZERO = L * math.sqrt((PES - PA) / MS)             # 底纖維應力歸零的位置

# ── Step 7：補充鋼筋 ────────────────────────────────────
Y_NA = H * FREE_BOT / (FREE_BOT + abs(FREE_TOP))
T_FORCE = 0.5 * FREE_BOT * Y_NA * B
FS = min(0.6 * FY, 2100.0)
AS_REQ = T_FORCE / FS

# ── §5⑤ 鋼腱應力上限 ───────────────────────────────────
FPY = 0.9 * FPU
LIM_OLD = min(0.82 * FPY, 0.74 * FPU)      # ACI 318-11 傳遞後通則（已刪除）
LIM_JACK = min(0.80 * FPU, 0.94 * FPY)     # 現行張拉時
LIM_ANCH = 0.70 * FPU                      # 現行後拉法錨定裝置處


# ══════════════════════════════════════════════════════════
# 圖 1　懸臂彎矩與偏心方向（三條帶：載重／彎矩／鋼鍵）
# ══════════════════════════════════════════════════════════
W1, H1 = 960, 570
sx1 = (W1 - 310) / L
p1 = Canvas(W1, H1, sx=sx1, ox=150, oy=380)
p1.panel("懸臂梁的彎矩方向與簡支梁相反 → 鋼鍵必須在重心「上方」", None)

PX = lambda n: n / sx1                       # 像素 → 模型單位
Y_LOAD, Y_BMD, Y_TEN = 0.0, -PX(116), -PX(238)

# ── 條帶 1：梁與自重 ──
p1.line((0, Y_LOAD), (L, Y_LOAD), C["member"], 6, cap="butt")
p1.support((0, Y_LOAD), "fixed", 90, 24)
p1.udl((0, Y_LOAD), (L, Y_LOAD), PX(40), n=11, label=f"w = {W:.2f} kgf/cm")
p1.text_px(p1.X(L) + 10, p1.Y(Y_LOAD), "自由端", 12, C["muted"], "start")
p1.text_px(p1.X(L * 0.76), p1.Y(Y_LOAD) + 22, "① 自重（懸臂長 L = 610 cm）", 12,
           C["muted"])

# ── 條帶 2：自重彎矩圖（畫在受拉側＝梁線上方）──
MSC = PX(76) / MSW
p1.line((0, Y_BMD), (L, Y_BMD), C["member2"], 3, cap="butt")
pts = [(x, Y_BMD + MSW * ((L - x) / L)**2 * MSC) for x in [L * i / 60 for i in range(61)]]
p1.polygon([(0, Y_BMD)] + pts + [(L, Y_BMD)], C["fill_m"], C["bmd"], 2.6)
p1.math_px(p1.X(L * 0.13), p1.Y(Y_BMD + MSW * MSC) - 15,
           f"M_{{sw}} = wL^{{2}}/2 = {MSW/1e5:.2f} tf·m", 13, C["bmd"], "start",
           weight="700")
p1.text_px(p1.X(L) + 10, p1.Y(Y_BMD), "M = 0", 12, C["bmd"], "start", weight="700")
p1.text_px(p1.X(L * 0.42), p1.Y(Y_BMD) + 20,
           "② 彎矩圖畫在受拉側 → 全長頂部受拉", 12, C["bmd"], weight="700")

# ── 條帶 3：鋼鍵位置 ──
p1.line((0, Y_TEN), (L, Y_TEN), C["ghost"], 2.0, dash="7 4")
p1.text_px(p1.X(L) + 10, p1.Y(Y_TEN), "斷面重心", 11.5, C["muted"], "start")
Y_CABLE = Y_TEN + PX(34)
p1.line((0, Y_CABLE), (L, Y_CABLE), C["tension"], 3.4)
for i in range(9):
    p1.dot((L * (0.05 + 0.1125 * i), Y_CABLE), 4.6, fill=C["tension"],
           stroke="#FFFFFF", w=1.4)
p1.arrow((L * 0.5, Y_TEN), (L * 0.5, Y_CABLE), C["tension"], 2.4, 9)
p1.math_px(p1.X(L * 0.5) + 12, (p1.Y(Y_TEN) + p1.Y(Y_CABLE)) / 2,
           f"e = {ECC:.0f} cm", 13, C["tension"], "start", weight="700")
p1.text_px(p1.X(L * 0.5), p1.Y(Y_CABLE) - 20,
           f"③ 鋼鍵在重心上方、全長固定偏心（{N_TEN} 根 12.7 mm 七線絞）",
           12, C["tension"], weight="700")

p1.text_px(W1 / 2, H1 - 82,
           "偏心壓力對頂纖維造成壓應力，正好抵消自重造成的頂部拉力 —— 這是選「上方」的唯一理由",
           13, C["text"])
p1.text_px(W1 / 2, H1 - 56,
           f"代價：自由端 M = 0，上偏心在底纖維留下淨拉力 {FREE_BOT:+.2f} kgf/cm²",
           13, C["load"], weight="700")
p1.text_px(W1 / 2, H1 - 28,
           "簡支梁跨中鋼鍵在下、懸臂梁固定端鋼鍵在上 —— 判準是彎矩方向，不是構材長相",
           12.5, C["muted"])
p1.save(f"{OUT}/{TAG}-fig-1-eccentricity.svg")

# ══════════════════════════════════════════════════════════
# 圖 2　固定端／自由端的四個應力
# ══════════════════════════════════════════════════════════
PW, PH = 470, 590
SMAX = 60.0
sc2 = (PH - 330) / H
SS = (112.0 / SMAX) / sc2
SEC_W = 26.0 / sc2
GAP = 128.0 / sc2                 # 斷面示意帶與應力軸的水平間隔


def stress_shape(cv, h, ftop, fbot, ss, x0=0.0, w=2.2):
    """拉為正 → 畫右側紅；壓為負 → 畫左側藍（與本題符號規定一致）。"""
    ys = [0.0, h]
    if ftop * fbot < 0:
        ys = [0.0, -fbot / (ftop - fbot) * h, h]
    for i in range(len(ys) - 1):
        ya, yb = ys[i], ys[i + 1]
        fa = fbot + (ftop - fbot) * ya / h
        fb = fbot + (ftop - fbot) * yb / h
        ten = (fa + fb) > 0
        cv.polygon([(x0, ya), (x0 + fa * ss, ya), (x0 + fb * ss, yb), (x0, yb)],
                   C["fill_t"] if ten else C["fill_c"],
                   C["tension"] if ten else C["compr"], w)
    cv.line((x0, 0), (x0, h), C["member"], 2.6)


def end_panel(tag, sub, ftop, fbot, rows):
    cv = Canvas(PW, PH, sx=sc2, ox=PW * 0.58, oy=PH - 150 - H * sc2)
    cv.panel(tag, sub)
    cv.polygon([(-GAP - SEC_W, 0), (-GAP, 0), (-GAP, H), (-GAP - SEC_W, H)],
               "#EDF1F6", C["member"], 2.2)
    cv.dot((-GAP - SEC_W / 2, H / 2 + ECC), 5.4, fill=C["tension"], stroke="#FFFFFF", w=1.5)
    cv.text_px(cv.X(-GAP - SEC_W) - 8, cv.Y(H), "頂", 12, C["muted"], "end")
    cv.text_px(cv.X(-GAP - SEC_W) - 8, cv.Y(0.0), "底", 12, C["muted"], "end")
    # 容許拉應力界線
    cv.line((ALW_T * SS, 0), (ALW_T * SS, H), C["load"], 1.8, dash="5 4")
    cv.math_px(cv.X(ALW_T * SS), cv.Y(H) - 30, f"容許拉 {ALW_T:.2f}", 11.5, C["load"],
               weight="700")
    stress_shape(cv, H, ftop, fbot, SS)
    for v, y, dy in ((ftop, H, -4), (fbot, 0.0, 4)):
        cv.math_px(cv.X(v * SS) + (8 if v > 0 else -8), cv.Y(y) + dy, f"{v:+.2f}", 13.5,
                   C["tension"] if v > 0 else C["compr"], "start" if v > 0 else "end",
                   weight="700")
    y0 = PH - 132
    for i, (lab, val, ok) in enumerate(rows):
        cv.text_px(40, y0 + i * 26, lab, 12.5, C["muted"], "start")
        cv.text_px(PW - 116, y0 + i * 26, val, 12.5, C["text"], "end")
        cv.text_px(PW - 34, y0 + i * 26, "✓" if ok else "×", 15,
                   C["bmd"] if ok else C["load"], "end", weight="700")
    return cv


f1 = end_panel("固定端（x = 0）", f"M = M_{{sw}} = {MSW/1e5:.2f} tf·m",
               FIX_TOP, FIX_BOT,
               [(f"頂 −{PA:.2f}−{PES:.2f}+{MS:.2f}", f"{FIX_TOP:+.2f}（壓）", True),
                (f"底 −{PA:.2f}+{PES:.2f}−{MS:.2f}", f"{FIX_BOT:+.2f}（壓）", True),
                ("壓應力容許 0.60f'ci", f"{ALW_C:.0f}", True)])
f2 = end_panel("自由端（x = L）", "M = 0（沒有重力矩來遮蔽）",
               FREE_TOP, FREE_BOT,
               [(f"頂 −{PA:.2f}−{PES:.2f}", f"{FREE_TOP:+.2f}（壓）", True),
                (f"底 −{PA:.2f}+{PES:.2f}", f"{FREE_BOT:+.2f}（拉）", False),
                ("拉應力容許 0.80√f'ci", f"{ALW_T:.2f}", False)])

compose([f1, f2],
        title=f"{TAG}　控制斷面是自由端，不是固定端",
        sub=(f"初始階段：f'ci = 0.7f'c = {FCI:.0f}，壓容許 {ALW_C:.0f}、"
             f"拉容許 {ALW_T:.2f} kgf/cm²（壓為負、拉為正）"),
        note=(f"自由端沒有重力矩去抵銷上偏心造成的底纖維拉力，故 {FREE_BOT:+.2f} 超出 "
              f"{ALW_T:.2f}（超 {100*(FREE_BOT-ALW_T)/ALW_T:.1f}%）；"
              f"只算固定端會四項全過、完全看不出問題"),
        path=f"{OUT}/{TAG}-fig-2-stress.svg")

# ══════════════════════════════════════════════════════════
# 圖 3　底纖維應力沿梁長分布
# ══════════════════════════════════════════════════════════
W3, H3 = 960, 570
L_, R_, T_, B_ = 118, 196, 100, 162
pw, ph = W3 - L_ - R_, H3 - T_ - B_
asp = ph / pw
Y0, Y1 = -16.0, 36.0
cv = Canvas(W3, H3, sx=pw, ox=L_, oy=B_)


def P(x, y): return (x / L, (y - Y0) / (Y1 - Y0) * asp)


cv.panel("底纖維超限的不是一個點，是自由端起算的一整段", None)
cv.text_px(W3 / 2, 60,
           f"橫軸：距自由端 ξ（cm）　縱軸：底纖維應力（拉為正，kgf/cm²）",
           12.5, C["muted"])

# 超限區底色
cv.polygon([P(0, ALW_T), P(XI_LIM, ALW_T), P(XI_LIM, Y1), P(0, Y1)],
           "rgba(192,57,43,0.12)")
for v in (-15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35):
    cv.line(P(0, v), P(L, v), C["border"], 1.0)
    cv.math_px(cv.X(P(0, v)[0]) - 10, cv.Y(P(0, v)[1]), f"{v}", 12.5, C["muted"], "end")
for v in (0, 100, 200, 300, 400, 500, 600):
    cv.line(P(v, Y0), (P(v, Y0)[0], P(v, Y0)[1] - 7 / pw), C["muted"], 1.4)
    cv.math_px(cv.X(P(v, Y0)[0]), cv.Y(P(v, Y0)[1]) + 22, f"{v}", 12, C["muted"])
cv.line(P(0, Y0), P(L, Y0), C["muted"], 1.8)
cv.line(P(0, Y0), P(0, Y1), C["muted"], 1.8)
cv.line(P(0, 0.0), P(L, 0.0), C["muted"], 1.6)
cv.text_px(cv.X(P(L, Y0)[0]) + 12, cv.Y(P(L, Y0)[1]), "ξ", 14, C["muted"], "start")

n = 200
cv.poly([P(L * i / n, f_bot(L * i / n)) for i in range(n + 1)], C["tension"], 3.4)

for lvl, col, lab in ((ALW_T, C["load"], f"容許拉應力 0.80√f'ci = {ALW_T:.2f}"),
                      (FR_CI, C["accent"], f"開裂模數 2.0√f'ci = {FR_CI:.1f}")):
    cv.line(P(0, lvl), P(L, lvl), col, 2.2, dash="7 5")
    cv.math_px(cv.X(P(L, 0)[0]) + 8, cv.Y(P(0, lvl)[1]), lab, 11.5, col, "start",
               weight="700")

for xi, col, lab in ((XI_LIM, C["load"], f"ξ = {XI_LIM:.0f} cm"),
                     (XI_ZERO, C["muted"], f"ξ = {XI_ZERO:.0f} cm")):
    cv.line(P(xi, Y0), P(xi, Y1 - 2.0), col, 1.8, dash="4 5")
    cv.dot(P(xi, f_bot(xi)), 6.0, fill=col, stroke="#FFFFFF", w=2.0)
    cv.math_px(cv.X(P(xi, 0)[0]), cv.Y(P(0, Y0)[1]) + 44, lab, 12.5, col, weight="700")

cv.dot(P(0.0, FREE_BOT), 7.0, fill=C["load"], stroke="#FFFFFF", w=2.2)
cv.math_px(cv.X(P(0, 0)[0]) + 12, cv.Y(P(0, FREE_BOT)[1]) - 6,
           f"自由端 {FREE_BOT:+.2f}", 13, C["load"], "start", weight="700")
cv.dot(P(L, FIX_BOT), 6.4, fill=C["compr"], stroke="#FFFFFF", w=2.0)
cv.math_px(cv.X(P(L, 0)[0]) - 12, cv.Y(P(0, FIX_BOT)[1]) - 20,
           f"固定端 {FIX_BOT:+.2f}", 12.5, C["compr"], "end", weight="700")

cv.text_px((cv.X(P(0, 0)[0]) + cv.X(P(XI_LIM, 0)[0])) / 2, cv.Y(P(0, 22.0)[1]),
           "超出容許拉應力的區段", 12.5, C["load"], weight="700")

cv.text_px(W3 / 2, H3 - 78,
           f"自由端起算 {XI_LIM:.0f} cm（約梁長 1/3）整段都超限 —— "
           f"補救措施必須涵蓋這一整段，不能只在端點補幾根鋼筋",
           13, C["load"], weight="700")
cv.text_px(W3 / 2, H3 - 52,
           f"但 {FREE_BOT:.2f} 仍小於開裂模數 {FR_CI:.1f}：斷面尚未開裂，"
           f"未開裂彈性分析成立，補鋼筋即可（不必重設計斷面）", 12.5, C["bmd"])
cv.text_px(W3 / 2, H3 - 26,
           f"補充鋼筋承擔「全部」拉力 T = {T_FORCE:,.0f} kgf，"
           f"f_s = min(0.6f_y, 2100) = {FS:,.0f} → A_s = {AS_REQ:.2f} cm²",
           12.5, C["muted"])
cv.save(f"{OUT}/{TAG}-fig-3-overrun.svg")

# ══════════════════════════════════════════════════════════
# 對 .md §4 公佈值 assert
# ══════════════════════════════════════════════════════════
assert (A, I, S) == (2700.0, 1_822_500.0, 40_500.0)
assert abs(FCI - 245.0) < 1e-9 and abs(ALW_C - 147.0) < 1e-9
assert abs(ALW_T - 12.52) < 0.005,      ALW_T
assert abs(FPI - 14_250) < 1e-9
assert abs(APS - 2.9613) < 1e-9
assert abs(PI_F - 42_199) < 1,          PI_F
assert abs(W - 6.21) < 1e-9,            W
assert abs(MSW - 1_155_371) < 1,        MSW
assert (PA, PES, MS) == (15.63, 31.26, 28.53), (PA, PES, MS)
assert FIX_TOP == -18.36,   FIX_TOP
assert FIX_BOT == -12.90,   FIX_BOT
assert FREE_TOP == -46.89,  FREE_TOP
assert FREE_BOT == 15.63,   FREE_BOT
assert abs(XI_LIM - 201) < 1,           XI_LIM
assert abs(XI_ZERO - 452) < 1,          XI_ZERO
assert abs(Y_NA - 22.5) < 0.02,         Y_NA
assert abs(T_FORCE - 5275) < 1,         T_FORCE   # ← 訂正：md §4 Step 7 一處誤寫 5,276
assert abs(FS - 2100) < 1e-9
assert abs(AS_REQ - 2.51) < 0.01,       AS_REQ
assert abs(FR_CI - 31.3) < 0.05,        FR_CI
assert FREE_BOT < FR_CI
assert abs(LIM_OLD - 14_022) < 1 and abs(LIM_JACK - 15_200) < 1
assert abs(LIM_ANCH - 13_300) < 1
print(f"{TAG}: 3 圖 OK　Pi={PI_F:,.0f} 分量 {PA}/{PES}/{MS}　"
      f"固定端 {FIX_TOP}/{FIX_BOT}　自由端 {FREE_TOP}/{FREE_BOT}　"
      f"容許拉 {ALW_T:.2f} → 超限段 ξ={XI_LIM:.0f} cm、零應力 ξ={XI_ZERO:.0f} cm　"
      f"T={T_FORCE:,.0f} As={AS_REQ:.2f} cm²　fr(f'ci)={FR_CI:.1f}")
