#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2004-5 先拉預力梁・開裂彎矩與設計彎矩強度 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2004-5.md §1 給定的原始資料；β1、S_b、e、f_ce、M_cr、f_ps、
     a、c、ε_t、M_n 一律現算，檔尾對 §4 公佈值 assert。
  2. 改 §1 任一數字（A_ps、f_pu、f'_c、d_p）重跑，三張圖全部跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

FIGURES
  fig-1-mcr       M_cr 的底纖維應力歷程  攔：只把預壓應力歸零就當開裂，忘了再加 f_r
  fig-2-section   斷面／應變／應力三聯   攔：β1 不折減、a 與 c 互相代錯
  fig-3-strength  四個彎矩的相對位置     攔：漏做 φM_n ≥ 1.2M_cr（本題餘裕只有 9%）
"""
import sys, os, math

sys.path.insert(0, os.environ.get(
    "STRUCTDRAW_DIR", "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose                       # noqa: E402
from recipes import bar_compare                                  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2004-5"

# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
B    = 40.0        # 斷面寬 (cm)
H    = 90.0        # 斷面高 (cm)
DP   = 80.0        # 鋼腱有效深度 (cm)  = 90 − 10
APS  = 6.16        # 鋼腱面積 (cm^2)
FPU  = 16_500.0    # 極限強度 (kgf/cm^2)
FPY  = 0.85 * FPU  # 降伏強度
FE   = 0.6 * FPU   # 有效預力應力
FC   = 350.0
GP   = 0.4         # γ_p（題目給定）
EPS_CU = 0.003
PHI  = 0.90

# ── 材料與幾何（現算） ──────────────────────────────────
B1 = 0.85 if FC <= 280 else max(0.65, 0.85 - 0.05 * (FC - 280) / 70)
FR = 2.0 * math.sqrt(FC)
A  = B * H
I  = B * H**3 / 12
SB = I / (H / 2)
ECC = DP - H / 2

# ── ② 開裂彎矩 ──────────────────────────────────────────
PE  = APS * FE
FCE_AXI = PE / A
FCE_ECC = PE * ECC / SB
FCE = FCE_AXI + FCE_ECC
MCR = SB * (FCE + FR)

# ── ③④⑤ 極限強度 ───────────────────────────────────────
RHO_P = APS / (B * DP)
FPS = FPU * (1 - GP / B1 * RHO_P * FPU / FC)
T_PS = APS * FPS
A_BLK = T_PS / (0.85 * FC * B)
CU = round(A_BLK / B1, 2)          # §4⑤ 公佈值 10.19（a 取三位後再除 β1）
ET = EPS_CU * (DP - CU) / CU
MN = T_PS * (DP - A_BLK / 2)
PHI_MN = PHI * MN
OMEGA_P = T_PS / (B * DP * FC)
OMEGA_LIM = 0.36 * B1
MCR_12 = 1.2 * MCR
# 誤用 β1 = 0.85（§5 ②）
FPS_085 = FPU * (1 - GP / 0.85 * RHO_P * FPU / FC)
A_085 = APS * FPS_085 / (0.85 * FC * B)
PHIMN_085 = PHI * APS * FPS_085 * (DP - A_085 / 2)

TFM = 1e5      # kgf·cm → tf·m

# ══════════════════════════════════════════════════════════
# 圖 1　M_cr 的底纖維應力歷程
# ══════════════════════════════════════════════════════════
PW, PH = 430, 620
SMAX = 130.0
sc = (PH - 360) / H
SS = (110.0 / SMAX) / sc
SEC_W = 26.0 / sc


def stress_shape(cv, h, ftop, fbot, ss, x0=0.0, w=2.2):
    ys = [0.0, h]
    if ftop * fbot < 0:
        ys = [0.0, -fbot / (ftop - fbot) * h, h]
    for i in range(len(ys) - 1):
        ya, yb = ys[i], ys[i + 1]
        fa = fbot + (ftop - fbot) * ya / h
        fb = fbot + (ftop - fbot) * yb / h
        comp = (fa + fb) > 0
        cv.polygon([(x0, ya), (x0 + fa * ss, ya), (x0 + fb * ss, yb), (x0, yb)],
                   C["fill_c"] if comp else C["fill_t"],
                   C["compr"] if comp else C["tension"], w)
    cv.line((x0, 0), (x0, h), C["member"], 2.6)


def step_panel(tag, sub, ftop, fbot, lines, foot, col):
    cv = Canvas(PW, PH, sx=sc, ox=PW * 0.44, oy=PH - 178 - H * sc)
    cv.panel(tag, sub)
    cv.polygon([(-SEC_W, 0), (0, 0), (0, H), (-SEC_W, H)], "#EDF1F6", C["member"], 2.2)
    cv.dot((-SEC_W / 2, H - DP), 5.4, fill=C["tension"], stroke="#FFFFFF", w=1.5)
    stress_shape(cv, H, ftop, fbot, SS)
    for v, y, dy in ((ftop, H, -2), (fbot, 0.0, 2)):
        cv.math_px(cv.X(v * SS) + (8 if v > 0 else -8), cv.Y(y) + dy, f"{v:+.2f}", 13,
                   C["compr"] if v > 0 else (C["tension"] if v < 0 else C["muted"]),
                   "start" if v > 0 else "end", weight="700")
    cv.text_px(cv.X(0) + 4, cv.Y(H) - 22, "上緣", 11.5, C["muted"], "start")
    cv.text_px(cv.X(0) + 4, cv.Y(0.0) + 22, "底緣", 11.5, C["muted"], "start")
    for i, t in enumerate(lines):
        cv.text_px(PW / 2, PH - 132 + i * 22, t, 12, C["muted"])
    cv.text_px(PW / 2, PH - 34, foot, 13, col, weight="700")
    return cv


# 三個狀態的上下緣應力（壓為正）
S0_TOP = FCE_AXI - FCE_ECC          # 只有預力
S0_BOT = FCE
M_ZERO = SB * FCE                   # 底緣去壓所需彎矩
S1_TOP = S0_TOP + M_ZERO / SB
S1_BOT = 0.0
S2_TOP = S0_TOP + MCR / SB
S2_BOT = -FR

compose([
    step_panel("① 只有有效預力", f"P_{{e}} = A_{{ps}}·f_{{e}} = {PE:,.0f} kgf",
               S0_TOP, S0_BOT,
               [f"軸壓 P_{{e}}/A = {FCE_AXI:.2f}",
                f"偏心 P_{{e}}·e/S_{{b}} = {FCE_ECC:.2f}（e = {ECC:.0f} cm）",
                f"底緣預壓 f_{{ce}} = {FCE:.2f} kgf/cm²"],
               f"底緣預壓 {FCE:.2f}（壓）", C["compr"]),
    step_panel("② 外加彎矩把底緣壓到零", f"M = S_{{b}}·f_{{ce}} = {M_ZERO/TFM:.1f} tf·m",
               S1_TOP, S1_BOT,
               ["這裡還沒有裂 —— 只是預壓被抵銷完",
                f"若停在這裡會少算 S_{{b}}·f_{{r}} = {SB*FR/TFM:.1f} tf·m",
                "（這是最常見的失分點）"],
               "底緣 0.00（尚未開裂）", C["accent"]),
    step_panel("③ 再拉到開裂模數才開裂", "M_{cr} = S_{b}(f_{ce} + f_{r})",
               S2_TOP, S2_BOT,
               [f"f_{{r}} = 2.0√f'c = {FR:.2f} kgf/cm²（原卷給定）",
                f"f_{{ce}} + f_{{r}} = {FCE:.2f} + {FR:.2f} = {FCE+FR:.2f}",
                f"M_{{cr}} = {SB:,.0f} × {FCE+FR:.2f}"],
               f"M_{{cr}} = {MCR/TFM:.1f} tf·m", C["load"])],
    title=f"{TAG}　開裂彎矩＝「把預壓歸零」＋「再拉到 fr」兩段，不是只有第一段",
    sub=(f"矩形斷面 {B:.0f}×{H:.0f} cm，Sb = {SB:,.0f} cm³；壓為正、拉為負"),
    note=(f"只算到第②格會得 {M_ZERO/TFM:.1f} tf·m，比正解少 "
          f"{100*(MCR-M_ZERO)/MCR:.0f}% —— fr 那一段就佔了 Mcr 的 "
          f"{100*FR/(FCE+FR):.0f}%"),
    path=f"{OUT}/{TAG}-fig-1-mcr.svg")

# ══════════════════════════════════════════════════════════
# 圖 2　斷面／應變／等值應力塊
# ══════════════════════════════════════════════════════════
PW, PH = 420, 540
sc2 = min((PH - 200) / H, (PW - 150) / B)
MW = 92 / sc2

r1 = Canvas(PW, PH, sx=sc2, ox=PW / 2 - B * sc2 / 2, oy=100)
r1.panel("斷面", f"b × h = {B:.0f} × {H:.0f} cm")
r1.polygon([(0, 0), (B, 0), (B, H), (0, H)], "#EDF1F6", C["member"], 2.6)
for i in range(3):
    r1.dot((B * (0.22 + 0.28 * i), H - DP), 6.0, fill=C["tension"], stroke="#FFFFFF", w=1.6)
r1.line((0, H / 2), (B, H / 2), C["accent"], 1.8, dash="6 4")
r1.text_px(r1.X(B) + 6, r1.Y(H / 2), "形心", 11.5, C["accent"], "start", weight="700")
r1.dim((0, H), (0, H - DP), f"d_{{p}}={DP:.0f}", off=40, label_off=13)
r1.dim((B, H / 2), (B, H - DP), f"e={ECC:.0f}", off=-36, label_off=-12, color=C["tension"])
r1.dim((0, 0), (B, 0), f"b={B:.0f}", off=26, label_off=13)
r1.text_px(PW / 2, PH - 24, f"A_{{ps}} = {APS:.2f} cm^{{2}}（先拉、有黏結）",
           12.5, C["muted"])

r2 = Canvas(PW, PH, sx=sc2, ox=PW * 0.50, oy=100)
r2.panel("應變分佈", "平面保持平面")
r2.line((0, 0), (0, H), C["ghost"], 2, dash="5 4")
wc = MW * CU / (DP - CU)
r2.polygon([(0, H), (wc, H), (0, H - CU)], C["fill_c"], C["compr"], 2.4)
r2.polygon([(0, H - CU), (-MW, H - DP), (0, H - DP)], C["fill_t"], C["tension"], 2.4)
r2.line((-MW * 1.2, H - CU), (MW * 1.2, H - CU), C["accent"], 1.8, dash="6 4")
r2.text_px(r2.X(MW * 1.2) + 4, r2.Y(H - CU), "N.A.", 12, C["accent"], "start", weight="700")
r2.math_px(r2.X(wc) + 6, r2.Y(H) - 13, "ε_{cu}=0.003", 12.5, C["compr"], "start",
           weight="700")
r2.math_px(r2.X(-MW) - 6, r2.Y(H - DP), f"ε_{{t}}={ET:.4f}", 12.5, C["tension"], "end",
           weight="700")
r2.dim((0, H), (0, H - CU), f"c={CU:.2f}", off=34, label_off=12)
r2.text_px(PW / 2, PH - 66, f"ε_{{t}} = {ET:.4f} 遠大於 0.005", 12.5, C["bmd"],
           weight="700")
r2.text_px(PW / 2, PH - 44, f"→ 拉力控制，φ = {PHI:.2f}", 12.5, C["bmd"], weight="700")

r3 = Canvas(PW, PH, sx=sc2, ox=PW * 0.44, oy=100)
r3.panel("等值應力塊", f"a = β1 × c = {B1:.2f} × {CU:.2f}")
r3.line((0, 0), (0, H), C["ghost"], 2, dash="5 4")
r3.polygon([(0, H), (MW, H), (MW, H - A_BLK), (0, H - A_BLK)], C["fill_c"], C["compr"], 2.4)
r3.math_px(r3.X(0) - 8, r3.Y(H) - 13, f"0.85f'_{{c}}={0.85*FC:.1f}", 12.5, C["compr"],
           "end", weight="700")
r3.arrow((MW * 0.45, H - A_BLK / 2), (MW * 1.40, H - A_BLK / 2), C["compr"], 3.2, 10)
r3.arrow((0.0, H - DP), (-MW * 0.95, H - DP), C["tension"], 3.2, 10)
r3.dim((0, H), (0, H - A_BLK), f"a={A_BLK:.2f}", off=30, label_off=11)
r3.text_px(PW / 2, PH - 110, f"C_{{c}} = T = {T_PS:,.0f} kgf", 12.5, C["compr"],
           weight="700")
r3.text_px(PW / 2, PH - 88, f"f_{{ps}} = {FPS:,.0f} kgf/cm^{{2}}", 12.5, C["tension"],
           weight="700")
r3.text_px(PW / 2, PH - 62, f"力臂 d_{{p}} − a/2 = {DP - A_BLK/2:.2f} cm", 12, C["muted"])
r3.text_px(PW / 2, PH - 38, f"M_{{n}} = {MN/TFM:.2f} tf·m", 13.5, C["text"], weight="700")

compose([r1, r2, r3],
        title=f"{TAG}　β1 折減後 a 與 c 才對得上",
        sub=(f"f'c = {FC:.0f} 大於 280 → β1 = {B1:.2f}（不是 0.85）；"
             f"β1 在 γp/β1 是分母、在 c = a/β1 也是分母，兩處都會受影響"),
        note=(f"若誤用 β1 = 0.85：fps = {FPS_085:,.0f}（差 "
              f"{100*(FPS_085-FPS)/FPS:+.2f}%）、φMn = {PHIMN_085/TFM:.2f} tf·m；"
              f"本題影響小，但 f'c 更高、ρp 更大時會迅速放大"),
        path=f"{OUT}/{TAG}-fig-2-section.svg")

# ══════════════════════════════════════════════════════════
# 圖 3　四個彎矩的相對位置
# ══════════════════════════════════════════════════════════
bar_compare(
    [("M_{cr}　開裂彎矩", f"S_{{b}}(f_{{ce}}+f_{{r}}) = {SB:,.0f}×{FCE+FR:.2f}",
      MCR / TFM, f"{MCR/TFM:.2f} tf·m", C["accent"]),
     ("1.2M_{cr}　最小強度門檻", "土木401-112 §9.6.2.1",
      MCR_12 / TFM, f"{MCR_12/TFM:.2f} tf·m", C["load"]),
     ("φM_{n}　設計彎矩強度", f"φ = {PHI:.2f}（拉力控制）",
      PHI_MN / TFM, f"{PHI_MN/TFM:.2f} tf·m", C["bmd"]),
     ("M_{n}　標稱彎矩強度", "A_{ps}·f_{ps}(d_{p}−a/2)",
      MN / TFM, f"{MN/TFM:.2f} tf·m", C["muted"])],
    title=f"{TAG}　φM_{{n}} ≥ 1.2M_{{cr}} 這一關，餘裕只有 {100*(PHI_MN/MCR_12-1):.0f}%",
    sub=(f"長度即彎矩大小（最大者 M_{{n}} = {MN/TFM:.2f} tf·m 為 100%）；"
         f"φM_{{n}}/1.2M_{{cr}} = {PHI_MN/MCR_12:.2f}"),
    note=("這條規定防的是「一開裂就立刻破壞」：A_{ps} 再小一點，M_{n} 會掉而 "
          "M_{cr} 幾乎不動（由 f_{ce} 撐著），就會翻過門檻"),
    path=f"{OUT}/{TAG}-fig-3-strength.svg")

# ══════════════════════════════════════════════════════════
# 對 .md §4 公佈值 assert（含本次訂正後的 P_e、ω_p）
# ══════════════════════════════════════════════════════════
assert abs(B1 - 0.80) < 1e-9,            B1
assert abs(FR - 37.4) < 0.03,            FR
assert (A, I, SB, ECC) == (3600.0, 2_430_000.0, 54_000.0, 35.0)
assert abs(PE - 60_984) < 1,             PE      # ← 訂正：舊寫 61,024
assert abs(FCE_AXI - 16.94) < 0.01,      FCE_AXI
assert abs(FCE_ECC - 39.53) < 0.01,      FCE_ECC
assert abs(FCE - 56.47) < 0.01,          FCE     # ← 訂正：舊寫 56.50
assert abs(MCR / TFM - 50.7) < 0.05,     MCR / TFM
assert abs(RHO_P - 0.001925) < 5e-7,     RHO_P
assert abs(FPS - 15_751) < 2,            FPS
assert abs(A_BLK - 8.15) < 0.01,         A_BLK
assert abs(CU - 10.19) < 0.01,           CU
assert abs(ET - 0.02055) < 5e-5,         ET
assert abs(MN / TFM - 73.67) < 0.02,     MN / TFM
assert abs(PHI_MN / TFM - 66.3) < 0.02,  PHI_MN / TFM
assert abs(OMEGA_P - 0.0866) < 5e-5,     OMEGA_P  # ← 訂正：舊寫 0.0867
assert abs(OMEGA_LIM - 0.288) < 1e-9,    OMEGA_LIM
assert abs(MCR_12 / TFM - 60.84) < 0.05, MCR_12 / TFM
assert PHI_MN >= MCR_12,                 (PHI_MN, MCR_12)
assert abs(FPS_085 - 15_795) < 2,        FPS_085
assert abs(PHIMN_085 / TFM - 66.48) < 0.02, PHIMN_085 / TFM  # ← 訂正：舊寫 66.44
assert FE < FPS < FPU,                   (FE, FPS, FPU)
print(f"{TAG}: 3 圖 OK　Pe={PE:,.0f} f_ce={FCE:.2f} Mcr={MCR/TFM:.2f} "
      f"f_ps={FPS:,.0f} a={A_BLK:.2f} c={CU:.2f} εt={ET:.4f} "
      f"Mn={MN/TFM:.2f} φMn={PHI_MN/TFM:.2f} 1.2Mcr={MCR_12/TFM:.2f} "
      f"ωp={OMEGA_P:.4f} β1=0.85誤用→{PHIMN_085/TFM:.2f}")
