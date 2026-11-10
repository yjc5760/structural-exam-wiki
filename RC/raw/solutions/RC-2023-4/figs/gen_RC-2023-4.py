#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2023-4 無握裹後拉腱單向版・撓曲強度 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2023-4.md §1 給定的原始資料；ℓ/h、ρ_p、f_ps、上限、β1、
     A_s,min、a、c、ε_t、M_n 一律現算，檔尾對 §4 公佈值 assert。
  2. 改 §1 任一數字（L、h、d_p、間距、f'_c、f_se）重跑，三張圖全部跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

FIGURES
  fig-1-branch   跨深比分支與上限配套   攔：用 300 的公式配 4200 的上限（兩分支混用）
  fig-2-section  20 cm 條帶斷面三聯     攔：漏掉規範強制的最小握裹鋼筋
  fig-3-mn       三種 M_n 的差距        攔：只算鋼絞線就交卷（少 22%）
"""
import sys, os, math

sys.path.insert(0, os.environ.get(
    "STRUCTDRAW_DIR", "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose                       # noqa: E402
from recipes import bar_compare                                  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2023-4"

# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
L    = 1000.0      # 短向跨度 (cm)
H    = 25.0        # 版厚 (cm)
DP   = 22.0        # 有效深度 (cm)
AP   = 1.47        # 每根鋼絞線面積 (cm^2)
SP   = 20.0        # 間距 (cm) —— 同時是分析條帶寬 b
FPU  = 19_000.0
FSE  = 11_000.0
FPY  = 0.85 * FPU
FC   = 420.0
FY   = 4_200.0
EPS_CU = 0.003
AS_D13 = 1.27      # 實務常見 D13@20 的面積（§5-2 參考列）

B = SP                                    # 分析單元：20 cm 條帶
B1 = 0.85 if FC <= 280 else max(0.65, 0.85 - 0.05 * (FC - 280) / 70)
RHO_P = AP / (B * DP)
SLEND_H = L / H
SLEND_D = L / DP


def fps_of(coef):
    """無握裹腱經驗式；coef 為分母係數（100 或 300）。"""
    return FSE + 700 + FC / (coef * RHO_P)


COEF = 300 if SLEND_H > 35 else 100
CAP_INC = 2100 if SLEND_H > 35 else 4200
FPS_RAW = fps_of(COEF)
FPS = min(FPS_RAW, FPY, FSE + CAP_INC)
# 另一分支（對照用）
COEF_ALT = 100 if COEF == 300 else 300
CAP_ALT = 4200 if CAP_INC == 2100 else 2100
FPS_ALT = fps_of(COEF_ALT)

# ── §7.6.2.3 強制最小握裹鋼筋 ───────────────────────────
ACT = B * H / 2
AS_MIN = 0.004 * ACT


def sect(As):
    T = AP * FPS + As * FY
    a = T / (0.85 * FC * B)
    c = a / B1
    return dict(T=T, a=a, c=c, et=EPS_CU * (DP - c) / c,
                Mn=T * (DP - a / 2))


S_PS   = sect(0.0)        # 只算鋼絞線
S_MAIN = sect(AS_MIN)     # 主線：含 A_s,min
S_D13  = sect(AS_D13)     # 參考：實配 D13@20
NSTRIP = 100.0 / SP       # 每米寬的條帶數
TFM = 1e5


# ══════════════════════════════════════════════════════════
# 圖 1　跨深比分支與上限配套
# ══════════════════════════════════════════════════════════
W1, H1 = 900, 540
L_, R_, T_, B_ = 116, 188, 100, 132
pw, ph = W1 - L_ - R_, H1 - T_ - B_
asp = ph / pw
X0, X1 = 0.0015, 0.0075          # ρ_p 範圍
Y0, Y1 = 11_000.0, 16_500.0      # f_ps 範圍
cv = Canvas(W1, H1, sx=pw, ox=L_, oy=B_)


def P(x, y): return ((x - X0) / (X1 - X0), (y - Y0) / (Y1 - Y0) * asp)


cv.panel("兩個分支是「配套」的：公式與上限不能拆開用", None)
cv.text_px(W1 / 2, 60,
           f"本題 ℓ/h = {SLEND_H:.1f} 大於 35（ℓ/d_p = {SLEND_D:.2f} 亦然）→ 走 300 分支",
           12.5, C["muted"])

for v in (11_000, 12_000, 13_000, 14_000, 15_000, 16_000):
    cv.line(P(X0, v), P(X1, v), C["border"], 1.0)
    cv.math_px(cv.X(P(X0, v)[0]) - 10, cv.Y(P(X0, v)[1]), f"{v:,}", 12.5, C["muted"], "end")
for v in (0.002, 0.003, 0.004, 0.005, 0.006, 0.007):
    cv.line(P(v, Y0), (P(v, Y0)[0], P(v, Y0)[1] - 7 / pw), C["muted"], 1.4)
    cv.math_px(cv.X(P(v, Y0)[0]), cv.Y(P(v, Y0)[1]) + 22, f"{v:.3f}", 12, C["muted"])
cv.line(P(X0, Y0), P(X1, Y0), C["muted"], 1.8)
cv.line(P(X0, Y0), P(X0, Y1), C["muted"], 1.8)
cv.text_px(cv.X(P(X1, Y0)[0]) + 12, cv.Y(P(X1, Y0)[1]), "ρ_p", 14, C["muted"], "start")
cv.text_px(cv.X(P(X0, Y1)[0]) - 10, cv.Y(P(X0, Y1)[1]) - 24, "f_{ps}", 13.5, C["muted"], "end")

n = 200
xs = [X0 + (X1 - X0) * i / n for i in range(n + 1)]


def curve(coef, cap, col, dash, lab, laby, ldy=-16):
    pts = [P(x, min(FSE + 700 + FC / (coef * x), FPY, FSE + cap)) for x in xs]
    cv.poly(pts, col, 3.2, dash=dash)
    cv.line(P(X0, FSE + cap), P(X1, FSE + cap), col, 1.8, dash="4 5")
    cv.math_px(cv.X(P(X1, 0)[0]) + 8, cv.Y(P(0, FSE + cap)[1]),
               f"f_{{se}}+{cap} = {FSE+cap:,.0f}", 12, col, "start", weight="700")
    cv.text_px(cv.X(P(laby, 0)[0]), cv.Y(P(0, FSE + 700 + FC / (coef * laby))[1]) + ldy,
               lab, 12.5, col, weight="700")


curve(100, 4200, C["muted"], "7 5", "ℓ/h ≤ 35：分母 100ρ_p", 0.0052, -18)
curve(300, 2100, C["bmd"], None, "ℓ/h > 35：分母 300ρ_p（本題）", 0.0058, +24)

cv.line(P(RHO_P, Y0), P(RHO_P, Y1 - 200), C["accent"], 1.8, dash="4 5")
cv.dot(P(RHO_P, FPS), 7.0, fill=C["accent"], stroke="#FFFFFF", w=2.2)
cv.math_px(cv.X(P(RHO_P, 0)[0]) + 12, cv.Y(P(0, FPS)[1]) - 8,
           f"本題 f_{{ps}} = {FPS:,.0f}", 13.5, C["accent"], "start", weight="700")
cv.text_px(cv.X(P(RHO_P, 0)[0]) + 12, cv.Y(P(0, FPS)[1]) + 14,
           f"ρ_p = {RHO_P:.6f}", 12, C["accent"], "start")

cv.line(P(X0, FPY), P(X1, FPY), C["load"], 1.8, dash="6 4")
cv.math_px(cv.X(P(X1, 0)[0]) + 8, cv.Y(P(0, FPY)[1]),
           f"f_{{py}} = {FPY:,.0f}", 12, C["load"], "start", weight="700")

cv.text_px(W1 / 2, H1 - 72,
           f"若把 300 的公式配 4200 的上限：本題 {FPS:,.0f} 仍過關，"
           f"但依據是錯的（正確上限是 {FSE+CAP_INC:,.0f}，餘裕只有 "
           f"{100*(FSE+CAP_INC-FPS)/FPS:.1f}%）", 13, C["load"], weight="700")
cv.text_px(W1 / 2, H1 - 46,
           f"若誤用 100 分母：f_{{ps}} = {FPS_ALT:,.0f}，"
           f"比正解高 {100*(FPS_ALT-FPS)/FPS:.1f}%", 12.5, C["muted"])
cv.text_px(W1 / 2, H1 - 22,
           "長跨的腱伸長被稀釋 → 公式壓低（分母 100→300），上限也跟著壓低（4200→2100）",
           12.5, C["muted"])
cv.save(f"{OUT}/{TAG}-fig-1-branch.svg")

# ══════════════════════════════════════════════════════════
# 圖 2　20 cm 條帶的斷面／應變／應力
# ══════════════════════════════════════════════════════════
PW, PH = 430, 500
sc = min((PH - 210) / H, (PW - 170) / B)
MW = 88 / sc

k1 = Canvas(PW, PH, sx=sc, ox=PW / 2 - B * sc / 2, oy=112)
k1.panel("分析單元：20 cm 條帶", f"版厚 h = {H:.0f}，d_p = {DP:.0f} cm")
k1.polygon([(0, 0), (B, 0), (B, H), (0, H)], "#EDF1F6", C["member"], 2.6)
k1.dot((B / 2, H - DP), 7.0, fill=C["tension"], stroke="#FFFFFF", w=1.8)
k1.dot((B * 0.28, H - DP), 5.0, fill=C["accent"], stroke="#FFFFFF", w=1.6)
k1.dot((B * 0.72, H - DP), 5.0, fill=C["accent"], stroke="#FFFFFF", w=1.6)
k1.line((0, H / 2), (B, H / 2), C["muted"], 1.4, dash="5 4")
k1.text_px(k1.X(B) + 6, k1.Y(H * 0.25), "A_{ct}", 12, C["accent"], "start", weight="700")
k1.polygon([(0, 0), (B, 0), (B, H / 2), (0, H / 2)], "rgba(180,83,9,0.10)")
k1.dim((0, H), (0, H - DP), f"d_{{p}}={DP:.0f}", off=38, label_off=13)
k1.dim((B, H), (B, 0), f"h={H:.0f}", off=-34, label_off=-12)
k1.text_px(PW / 2, PH - 96, f"紅＝無握裹鋼絞線 A_{{p}} = {AP:.2f} cm^{{2}}", 12,
           C["tension"], weight="700")
k1.text_px(PW / 2, PH - 74, f"橘＝§7.6.2.3 強制握裹鋼筋", 12, C["accent"], weight="700")
k1.text_px(PW / 2, PH - 50,
           f"A_{{ct}} = b·h/2 = {ACT:.0f} cm^{{2}}　→　"
           f"A_{{s,min}} = 0.004A_{{ct}} = {AS_MIN:.2f} cm^{{2}}", 12, C["muted"])
k1.text_px(PW / 2, PH - 28, f"（每米寬 {AS_MIN*NSTRIP:.1f} cm²）", 11.5, C["muted"])

k2 = Canvas(PW, PH, sx=sc, ox=PW * 0.52, oy=112)
k2.panel("應變分佈", f"c = {S_MAIN['c']:.3f} cm 遠小於 d_p")
k2.line((0, 0), (0, H), C["ghost"], 2, dash="5 4")
cc = S_MAIN["c"]
wc = MW * cc / (DP - cc)
k2.polygon([(0, H), (wc, H), (0, H - cc)], C["fill_c"], C["compr"], 2.4)
k2.polygon([(0, H - cc), (-MW, H - DP), (0, H - DP)], C["fill_t"], C["tension"], 2.4)
k2.line((-MW * 1.2, H - cc), (MW * 1.2, H - cc), C["accent"], 1.8, dash="6 4")
k2.text_px(k2.X(MW * 1.2) + 4, k2.Y(H - cc), "N.A.", 12, C["accent"], "start", weight="700")
k2.math_px(k2.X(wc) + 6, k2.Y(H) - 13, "ε_{cu}=0.003", 12, C["compr"], "start", weight="700")
k2.math_px(k2.X(-MW) - 6, k2.Y(H - DP), f"ε_{{t}}={S_MAIN['et']:.4f}", 12, C["tension"],
           "end", weight="700")
k2.text_px(PW / 2, PH - 74, f"ε_{{t}} = {S_MAIN['et']:.4f} 遠大於 0.005", 12.5, C["bmd"],
           weight="700")
k2.text_px(PW / 2, PH - 50, "→ 拉力控制（本題只問 M_{n}，不乘 φ）", 12, C["muted"])
k2.text_px(PW / 2, PH - 26, "無握裹腱不能用應變相容求 f_{ps}", 12, C["load"], weight="700")

k3 = Canvas(PW, PH, sx=sc, ox=PW * 0.42, oy=112)
k3.panel("等值應力塊與拉力", f"a = {S_MAIN['a']:.3f} cm（β1 = {B1:.2f}）")
k3.line((0, 0), (0, H), C["ghost"], 2, dash="5 4")
k3.polygon([(0, H), (MW, H), (MW, H - S_MAIN["a"]), (0, H - S_MAIN["a"])],
           C["fill_c"], C["compr"], 2.4)
k3.math_px(k3.X(0) - 8, k3.Y(H) - 13, f"0.85f'_{{c}}={0.85*FC:.0f}", 12, C["compr"], "end",
           weight="700")
k3.arrow((MW * 0.45, H - S_MAIN["a"] / 2), (MW * 1.35, H - S_MAIN["a"] / 2),
         C["compr"], 3.0, 10)
k3.arrow((0.0, H - DP), (-MW * 0.95, H - DP), C["tension"], 3.2, 10)
k3.dim((0, H), (0, H - S_MAIN["a"]), f"a={S_MAIN['a']:.2f}", off=28, label_off=11)
k3.text_px(PW / 2, PH - 104, f"A_{{p}}f_{{ps}} = {AP*FPS:,.0f} kgf", 12, C["tension"],
           weight="700")
k3.text_px(PW / 2, PH - 82, f"A_{{s,min}}f_{{y}} = {AS_MIN*FY:,.0f} kgf", 12, C["accent"],
           weight="700")
k3.text_px(PW / 2, PH - 58, f"T = {S_MAIN['T']:,.0f} kgf　力臂 {DP - S_MAIN['a']/2:.3f} cm",
           12, C["muted"])
k3.text_px(PW / 2, PH - 30,
           f"M_{{n}} = {S_MAIN['Mn']/TFM:.2f} tf·m／條帶 → {S_MAIN['Mn']*NSTRIP/TFM:.1f} tf·m/m",
           13, C["bmd"], weight="700")

compose([k1, k2, k3],
        title=f"{TAG}　題目給了 fy，就是要你把握裹鋼筋算進去",
        sub=(f"因 dp = d = {DP:.0f} cm，兩項拉力可共用同一個力臂；"
             f"若鋼筋比腱更靠外側就必須分開寫"),
        note=(f"§7.6.2.3 對「使用無握裹腱之單向版」訂 As,min = 0.004Act 為強制最小量；"
              f"卷首又明訂未依土木401-110 作答不予計分 —— 這一項不是選配"),
        path=f"{OUT}/{TAG}-fig-2-section.svg")

# ══════════════════════════════════════════════════════════
# 圖 3　三種 M_n
# ══════════════════════════════════════════════════════════
bar_compare(
    [("只算鋼絞線（舊主線）", f"a = {S_PS['a']:.3f} cm，T = {S_PS['T']:,.0f} kgf",
      S_PS["Mn"] * NSTRIP / TFM, f"{S_PS['Mn']*NSTRIP/TFM:.1f} tf·m/m", C["muted"]),
     ("含 A_{s,min}=0.004A_{ct}（主線）",
      f"a = {S_MAIN['a']:.3f} cm，A_{{s}} = {AS_MIN:.2f} cm²",
      S_MAIN["Mn"] * NSTRIP / TFM, f"{S_MAIN['Mn']*NSTRIP/TFM:.1f} tf·m/m", C["bmd"]),
     ("若實配 D13@20", f"A_{{s}} = {AS_D13:.2f} cm²（實務常見）",
      S_D13["Mn"] * NSTRIP / TFM, f"{S_D13['Mn']*NSTRIP/TFM:.1f} tf·m/m", C["accent"])],
    title=f"{TAG}　握裹鋼筋算不算，差 {100*(S_MAIN['Mn']/S_PS['Mn']-1):.0f}%",
    sub=(f"每 20 cm 條帶算完再乘 {NSTRIP:.0f} 換成每米寬；"
         f"f_{{ps}} = {FPS:,.0f} kgf/cm² 三者相同"),
    note=("考場最安全的寫法是兩者都寫：先算絞線得 "
          f"{S_PS['Mn']*NSTRIP/TFM:.1f}，再補「依 §7.6.2.3 尚須配 A_{{s,min}}」得 "
          f"{S_MAIN['Mn']*NSTRIP/TFM:.1f} tf·m/m"),
    path=f"{OUT}/{TAG}-fig-3-mn.svg")

# ══════════════════════════════════════════════════════════
# 對 .md §4 公佈值 assert
# ══════════════════════════════════════════════════════════
assert SLEND_H == 40.0 and abs(SLEND_D - 45.45) < 0.01
assert COEF == 300 and CAP_INC == 2100
assert abs(RHO_P - 3.341e-3) < 5e-7,      RHO_P
assert abs(FC / (COEF * RHO_P) - 419.0) < 0.5
assert abs(FPS - 12_119) < 2,             FPS
assert FPS < FPY and FPS < FSE + CAP_INC
assert abs(B1 - 0.75) < 1e-9,             B1
assert abs(ACT - 250.0) < 1e-9 and abs(AS_MIN - 1.00) < 1e-9
assert abs(S_PS["a"] - 2.495) < 0.002,    S_PS["a"]
assert abs(S_PS["c"] - 3.327) < 0.003,    S_PS["c"]
assert abs(S_PS["T"] - 17_815) < 3,       S_PS["T"]
assert abs(S_PS["Mn"] * NSTRIP / TFM - 18.5) < 0.05
assert abs(S_MAIN["T"] - 22_015) < 3,     S_MAIN["T"]
assert abs(S_MAIN["a"] - 3.083) < 0.002,  S_MAIN["a"]
assert abs(S_MAIN["c"] - 4.111) < 0.003,  S_MAIN["c"]
assert abs(S_MAIN["et"] - 0.0131) < 5e-5, S_MAIN["et"]
assert abs(S_MAIN["Mn"] - 450_390) < 60,  S_MAIN["Mn"]
assert abs(S_MAIN["Mn"] * NSTRIP / TFM - 22.5) < 0.05
assert abs(S_D13["a"] - 3.242) < 0.002,   S_D13["a"]
assert abs(S_D13["Mn"] * NSTRIP / TFM - 23.6) < 0.05
assert abs(100 * (S_MAIN["Mn"] / S_PS["Mn"] - 1) - 21.8) < 0.3
print(f"{TAG}: 3 圖 OK　ℓ/h={SLEND_H:.1f} ρp={RHO_P:.6f} fps={FPS:,.0f}"
      f"（上限 {FPY:,.0f} / {FSE+CAP_INC:,.0f}）β1={B1:.2f} As,min={AS_MIN:.2f}　"
      f"Mn/m：只絞線 {S_PS['Mn']*NSTRIP/TFM:.1f}／主線 {S_MAIN['Mn']*NSTRIP/TFM:.1f}／"
      f"D13@20 {S_D13['Mn']*NSTRIP/TFM:.1f}")
