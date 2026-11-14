#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2006-4 組合預力梁・兩階段應力疊加 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2006-4.md §1 給定的原始資料；斷面性質、n、形心、I_c、S、
     各階段應力一律現算，檔尾對 §4／§5 公佈值 assert。
  2. 改 §1 任一數字（P_e、版厚、f'_c2、w_LL…）重跑，三張圖全部跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

FIGURES
  fig-1-composite  兩階段斷面對照      攔：版寬不折換（n=1）、形心位置抓錯
  fig-2-stress     載重歸屬與應力疊加  攔：把版 DL 放到組合斷面（Stage1 梁底就差 56.25）
  fig-3-allow      容許應力利用率      攔：用查無出處的 0.4f'c／3√f'c 當容許值；梁距讀成 200
"""
import sys, os, math

sys.path.insert(0, os.environ.get(
    "STRUCTDRAW_DIR", "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose                       # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2006-4"

# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
L     = 2000.0     # 跨度 (cm)
BW    = 30.0       # 梁寬 (cm)
HB    = 80.0       # 梁全深 (cm)
FC1   = 350.0      # 梁 f'c
BS    = 100.0      # 版寬＝梁中心距 (cm)（題目正本判讀 #2；2026-11-14 勘誤，原誤讀 200）
TS    = 15.0       # 版厚 (cm)
FC2   = 280.0      # 版 f'c
PE    = 210_000.0  # 有效預力 (kgf)
CGS   = 15.0       # c.g.s. 距梁底 (cm)
WLL_A = 1.0        # 活載 tf/m^2
GAMMA = 2400.0     # 混凝土單位重 kgf/m^3（原卷未給，§5 已說明）

# ── Step 1：非組合梁斷面性質 ─────────────────────────────
A1 = BW * HB
I1 = BW * HB**3 / 12
S1 = I1 / (HB / 2)
ECC = HB / 2 - CGS

# ── Step 2：Stage 1（P_e + 梁 SW + 版 DL 都在梁斷面上） ──
R2 = lambda x: round(x, 2)
PS_AXI = R2(PE / A1)
PS_ECC = R2(PE * ECC / S1)
PS_TOP = R2(PS_AXI - PS_ECC)
PS_BOT = R2(PS_AXI + PS_ECC)
W_BEAM = GAMMA * (BW * HB / 1e4)          # kgf/m
W_SLAB = GAMMA * (TS / 100) * (BS / 100)  # kgf/m
W_S1 = (W_BEAM + W_SLAB) / 100            # kgf/cm
M_S1 = W_S1 * L**2 / 8
DL_S = R2(M_S1 / S1)
S1_TOP = R2(PS_TOP + DL_S)
S1_BOT = R2(PS_BOT - DL_S)

# ── Step 3：組合轉換斷面 ─────────────────────────────────
NR = math.sqrt(FC2 / FC1)
BS_T = BS * NR
A_SLAB = BS_T * TS
Y_BEAM, Y_SLAB = HB / 2, HB + TS / 2
YBAR = (A1 * Y_BEAM + A_SLAB * Y_SLAB) / (A1 + A_SLAB)
IC = (I1 + A1 * (YBAR - Y_BEAM)**2
      + BS_T * TS**3 / 12 + A_SLAB * (Y_SLAB - YBAR)**2)
SC_TOP = IC / (HB - YBAR)                 # 量到梁頂
SC_BOT = IC / YBAR
SC_DECK = IC / (HB + TS - YBAR)

# ── Step 4：Stage 2（w_LL 作用於組合斷面） ───────────────
W_LL = WLL_A * (BS / 100) * 1000 / 100    # kgf/cm
M_LL = W_LL * L**2 / 8
LL_TOP = R2(M_LL / SC_TOP)
LL_BOT = R2(-M_LL / SC_BOT)
F_TOP = round(S1_TOP + LL_TOP, 1)
F_BOT = round(S1_BOT + LL_BOT, 1)
F_DECK = R2(M_LL / SC_DECK * NR)

# ── 錯誤對照：版 DL 誤放到組合斷面 ──────────────────────
M_BEAM = (W_BEAM / 100) * L**2 / 8
M_SLAB = (W_SLAB / 100) * L**2 / 8
E_S1_TOP = R2(PS_TOP + M_BEAM / S1)
E_S1_BOT = R2(PS_BOT - M_BEAM / S1)
E_TOP = round(E_S1_TOP + (M_SLAB + M_LL) / SC_TOP, 1)
E_BOT = round(E_S1_BOT - (M_SLAB + M_LL) / SC_BOT, 1)

# ── 容許值（土木 401-110／112 §18.4；ACI 318-19 §24.5） ──
ALW_D  = 0.45 * FC1                        # 預力＋持續載重（壓）
ALW_L  = 0.60 * FC1                        # 預力＋全部載重（壓）
CLS_U  = 2.0 * math.sqrt(FC1)              # Class U 拉應力上限
CLS_T  = 3.2 * math.sqrt(FC1)              # Class T 上限
ALW_DK = 0.60 * FC2                        # 版頂壓


# ══════════════════════════════════════════════════════════
# 共用：線性應力分佈（壓為正 → 右側藍；拉為負 → 左側紅）
# ══════════════════════════════════════════════════════════
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


# ══════════════════════════════════════════════════════════
# 圖 1　Stage 1 梁斷面 vs Stage 2 組合轉換斷面
# ══════════════════════════════════════════════════════════
PW, PH = 520, 560
HTOT = HB + TS
sc = min((PW - 200) / max(BS, 200.0), (PH - 250) / HTOT)   # 版寬 100 時維持與 200 相同比例，避免標註互相壓疊


def beam_body(cv):
    cv.polygon([(-BW / 2, 0), (BW / 2, 0), (BW / 2, HB), (-BW / 2, HB)],
               "#EDF1F6", C["member"], 2.6)
    cv.dot((0, CGS), 6.4, fill=C["tension"], stroke="#FFFFFF", w=1.8)


g1 = Canvas(PW, PH, sx=sc, ox=PW / 2, oy=PH - 132 - HTOT * sc - 70)
g1.panel("Stage 1：非組合梁斷面", "版尚未硬化，版重由梁獨自承受")
beam_body(g1)
g1.polygon([(-BS / 2, HB), (BS / 2, HB), (BS / 2, HB + TS), (-BS / 2, HB + TS)],
           "none", C["ghost"], 1.8)
g1.text_px(g1.X(0), g1.Y(HB + TS / 2), "濕混凝土（尚無強度）", 11, C["muted"])
g1.line((-BW / 2, HB / 2), (BW / 2, HB / 2), C["accent"], 2.0, dash="7 4")
g1.dim((BW / 2 + 2, HB / 2), (BW / 2 + 2, CGS), f"e={ECC:.0f}", off=-46, label_off=-13,
       color=C["tension"])
g1.dim((-BW / 2 - 2, HB), (-BW / 2 - 2, 0), f"h={HB:.0f}", off=40, label_off=13)
g1.dim((-BW / 2, 0), (BW / 2, 0), f"b={BW:.0f}", off=32, label_off=14)
g1.text_px(PW / 2, PH - 96,
           f"A_{{1}} = {A1:,.0f} cm^{{2}}　I_{{1}} = {I1/1e6:.2f}×10^{{6}} cm^{{4}}",
           12.5, C["muted"])
g1.text_px(PW / 2, PH - 72,
           f"S_{{t1}} = S_{{b1}} = {S1:,.0f} cm^{{3}}（上下對稱）", 12.5, C["muted"])
g1.text_px(PW / 2, PH - 44,
           f"承受：P_{{e}} ＋ 梁自重 ＋ 版 DL", 13.5, C["bmd"], weight="700")

g2 = Canvas(PW, PH, sx=sc, ox=PW / 2, oy=PH - 132 - HTOT * sc - 70)
g2.panel("Stage 2：組合轉換斷面", f"版寬折換 n = √(f'c2/f'c1) = {NR:.4f}")
beam_body(g2)
g2.polygon([(-BS / 2, HB), (BS / 2, HB), (BS / 2, HB + TS), (-BS / 2, HB + TS)],
           "none", C["ghost"], 1.6, op=0.9)
g2.polygon([(-BS_T / 2, HB), (BS_T / 2, HB), (BS_T / 2, HB + TS), (-BS_T / 2, HB + TS)],
           "#E3E9F2", C["member"], 2.4)
g2.dim((-BS / 2, HB + TS), (BS / 2, HB + TS), f"原寬 {BS:.0f}", off=-78, label_off=-13)
g2.dim((-BS_T / 2, HB + TS), (BS_T / 2, HB + TS), f"折換後 {BS_T:.1f}", off=-38,
       label_off=-13, color=C["compr"])
g2.line((-BS_T / 2, YBAR), (BS_T / 2, YBAR), C["accent"], 2.2, dash="7 4")
g2.text_px(g2.X(BS_T / 2) + 6, g2.Y(YBAR), "組合形心", 11.5, C["accent"], "start",
           weight="700")
g2.dim((-BS_T / 2 - 2, YBAR), (-BS_T / 2 - 2, 0), f"{YBAR:.2f}", off=40, label_off=13)
g2.text_px(PW / 2, PH - 96,
           f"I_{{c}} = {IC:,.0f} cm^{{4}}　形心距梁底 {YBAR:.2f} cm", 12.5, C["muted"])
g2.text_px(PW / 2, PH - 72,
           f"S_{{top}} = {SC_TOP:,.0f}　S_{{bot}} = {SC_BOT:,.0f} cm^{{3}}"
           f"　→　比值 {SC_TOP/SC_BOT:.2f}", 12.5, C["muted"])
g2.text_px(PW / 2, PH - 44, "承受：w_{LL} 活載重", 13.5, C["bmd"], weight="700")

compose([g1, g2],
        title=f"{TAG}　「利用梁作為支撐」＝版重歸給非組合梁",
        sub=(f"組合形心被樓版拉高到距梁底 {YBAR:.2f} cm（梁全深才 {HB:.0f} cm），"
             f"故 Stop／Sbot = {SC_TOP/SC_BOT:.2f}"),
        note=(f"同一個 MLL 在梁底造成的應力是梁頂的 {SC_TOP/SC_BOT:.1f} 倍；"
              f"版寬取梁中心距 {BS:.0f} cm（圖四兩段 100 cm 皆為相鄰梁中心距），讀成 200 會使版重與活載重加倍"),
        path=f"{OUT}/{TAG}-fig-1-composite.svg")

# ══════════════════════════════════════════════════════════
# 圖 2　載重歸屬與應力疊加（含錯誤對照）
# ══════════════════════════════════════════════════════════
PW, PH = 470, 620
SMAX = 270.0
sc2 = (PH - 372) / HB
SS = (128.0 / SMAX) / sc2
SEC_W = 26.0 / sc2


def stress_panel(tag, sub, ftop, fbot, rows, foot, foot_col):
    cv = Canvas(PW, PH, sx=sc2, ox=PW * 0.42, oy=PH - 178 - HB * sc2)
    cv.panel(tag, sub)
    cv.polygon([(-SEC_W, 0), (0, 0), (0, HB), (-SEC_W, HB)], "#EDF1F6", C["member"], 2.2)
    stress_shape(cv, HB, ftop, fbot, SS)
    for v, y, dy in ((ftop, HB, -2), (fbot, 0.0, 2)):
        cv.math_px(cv.X(v * SS) + (8 if v > 0 else -8), cv.Y(y) + dy, f"{v:+.2f}", 13,
                   C["compr"] if v > 0 else C["tension"], "start" if v > 0 else "end",
                   weight="700")
    cv.text_px(cv.X(0) + 4, cv.Y(HB) - 22, "梁頂", 11.5, C["muted"], "start")
    cv.text_px(cv.X(0) + 4, cv.Y(0.0) + 22, "梁底", 11.5, C["muted"], "start")
    y0 = PH - 130
    cv.text_px(34, y0 - 22, "分量（梁頂／梁底）", 11.5, C["muted"], "start", weight="700")
    for i, (lab, vt, vb) in enumerate(rows):
        cv.text_px(34, y0 + i * 21, lab, 11.5, C["muted"], "start")
        cv.text_px(PW - 116, y0 + i * 21, vt, 11.5, C["text"], "end")
        cv.text_px(PW - 22, y0 + i * 21, vb, 11.5, C["text"], "end")
    cv.text_px(PW / 2, PH - 26, foot, 12.5, foot_col, weight="700")
    return cv


q1 = stress_panel(
    "Stage 1 結束", "P_e ＋ 梁自重 ＋ 版 DL（都在梁斷面）", S1_TOP, S1_BOT,
    [("預力軸壓 P_e/A_1", f"+{PS_AXI:.2f}", f"+{PS_AXI:.2f}"),
     ("預力偏心 P_e·e/S_1", f"−{PS_ECC:.2f}", f"+{PS_ECC:.2f}"),
     ("Stage1 DL M_S1/S_1", f"+{DL_S:.2f}", f"−{DL_S:.2f}")],
    f"梁頂 {S1_TOP:+.2f}　梁底 {S1_BOT:+.2f}（均壓）", C["bmd"])

q2 = stress_panel(
    "施加 LL 後（正解）", "w_{LL} 作用於組合斷面", F_TOP, F_BOT,
    [("Stage 1 小計", f"+{S1_TOP:.2f}", f"+{S1_BOT:.2f}"),
     ("活載 M_{LL}/S_{comp}", f"+{LL_TOP:.2f}", f"{LL_BOT:.2f}"),
     ("合計", f"+{F_TOP:.1f}", f"{F_BOT:.1f}")],
    f"梁頂 {F_TOP:+.1f}（壓）　梁底 {F_BOT:+.1f}（{'壓' if F_BOT > 0 else '拉'}）", C["bmd"])

q3 = stress_panel(
    "若把版 DL 誤放到組合斷面", "常見失分：版重當成組合後才施加", E_TOP, E_BOT,
    [("Stage 1（只有梁自重）", f"+{E_S1_TOP:.2f}", f"+{E_S1_BOT:.2f}"),
     ("版 DL＋LL 於組合斷面（錯）", f"+{(M_SLAB+M_LL)/SC_TOP:.2f}",
      f"−{(M_SLAB+M_LL)/SC_BOT:.2f}"),
     ("合計（錯誤）", f"+{E_TOP:.1f}", f"{E_BOT:.1f}")],
    f"梁底變成 {E_BOT:+.1f} —— 與正解差 {abs(F_BOT-E_BOT):.1f}", C["load"])

compose([q1, q2, q3],
        title=f"{TAG}　載重放在哪一個斷面上，決定梁底是 {F_BOT:+.1f} 還是 {E_BOT:+.1f}",
        sub=("原卷「澆置樓版時利用梁作為支撐」就是把版 DL 指定給非組合梁的關鍵字；"
             "壓為正、拉為負"),
        note=(f"錯放版 DL 的代價：Stage 1 梁底就差 {abs(E_S1_BOT-S1_BOT):.1f}"
              f"（{S1_BOT:.2f} 對 {E_S1_BOT:.2f}），最終梁底差 {abs(F_BOT-E_BOT):.1f} "
              f"kgf/cm²（本題另一個大失分點是把梁距讀成 200 cm）"),
        path=f"{OUT}/{TAG}-fig-2-stress.svg")

# ══════════════════════════════════════════════════════════
# 圖 3　容許應力利用率（各列以自己的容許值為 100%）
# ══════════════════════════════════════════════════════════
CHECKS = [
    ("梁頂壓（預力＋持續載重 D）", f"{S1_TOP:.1f} 對 0.45f'c = {ALW_D:.1f}",
     S1_TOP, ALW_D, C["bmd"]),
    ("梁頂壓（預力＋全部載重）", f"{F_TOP:.1f} 對 0.60f'c = {ALW_L:.1f}",
     F_TOP, ALW_L, C["bmd"]),
    ("版頂壓（換回版材料）", f"{F_DECK:.1f} 對 0.60f'c2 = {ALW_DK:.1f}",
     F_DECK, ALW_DK, C["bmd"]),
    ("梁底壓（預力＋持續載重 D）", f"{S1_BOT:.1f} 對 0.45f'c = {ALW_D:.1f}",
     S1_BOT, ALW_D, C["bmd"]),
    ("梁底拉 對 Class U 上限", f"梁底仍受壓 {F_BOT:+.1f}，拉應力 0 對 2.0√f'c = {CLS_U:.1f}",
     max(0.0, -F_BOT), CLS_U, C["load"]),
]
W3 = 1040
ROW_H = 82
H3 = 132 + ROW_H * len(CHECKS) + 96
cv = Canvas(W3, H3, sx=1, bg="#FFFFFF")
cv.text_px(W3 / 2, 34, f"{TAG}　五項檢核的利用率（各列以自己的容許值為 100%）",
           17.5, C["text"], weight="700")
cv.text_px(W3 / 2, 60,
           "土木401-110/112 §18.4；ACI 318-19 §24.5（kgf/cm² 制）", 13, C["muted"])
X0, BAR_W, FULL = 470, 380, 3.2
xl = X0 + BAR_W / FULL
for i, (name, desc, val, lim, col) in enumerate(CHECKS):
    y = 132 + i * ROW_H
    r = val / lim
    ok = r <= 1.0
    cv.text_px(40, y - 11, name, 14, C["text"], "start", weight="700")
    cv.text_px(40, y + 13, desc, 12, C["muted"], "start")
    cv.rect_px(X0, y - 17, BAR_W, 34, "#EDF1F6", 8)
    cv.rect_px(X0, y - 17, min(BAR_W, BAR_W * r / FULL), 34,
               C["bmd"] if ok else C["load"], 8)
    bw_px = BAR_W * min(r, FULL) / FULL
    if bw_px >= 64:
        cv.text_px(X0 + bw_px - 12, y, f"{100*r:.0f}%", 14, "#FFFFFF", "end", weight="700")
    else:
        cv.text_px(X0 + bw_px + 10, y, f"{100*r:.0f}%", 14, C["text"], "start", weight="700")
    cv.text_px(X0 + BAR_W + 18, y, "✓ 通過" if ok else "× 超限", 14,
               C["bmd"] if ok else C["load"], "start", weight="700")
cv.parts.append(f'<line x1="{xl}" y1="{132-28}" x2="{xl}" y2="{132+ROW_H*len(CHECKS)-40}" '
                f'stroke="{C["accent"]}" stroke-width="2.4" stroke-dasharray="7 5"/>')
cv.text_px(xl, 132 - 44, "容許值 100%", 13, C["accent"], weight="700")
cv.text_px(W3 / 2, H3 - 62,
           f"施加活載重後梁底仍有 {F_BOT:.1f} 的壓應力 → 全斷面未開裂，屬 Class U，彈性疊加有效",
           13.5, C["bmd"], weight="700")
cv.text_px(W3 / 2, H3 - 36,
           "舊版把梁距讀成 200 cm，梁底算成 −106.3（拉、Class C）；版重與活載重都多算一倍",
           12.5, C["muted"])
cv.save(f"{OUT}/{TAG}-fig-3-allow.svg")

# ══════════════════════════════════════════════════════════
# 對 .md §4／§5 公佈值 assert
# ══════════════════════════════════════════════════════════
assert (A1, I1, S1, ECC) == (2400.0, 1_280_000.0, 32_000.0, 25.0)
assert (PS_AXI, PS_ECC) == (87.5, 164.06), (PS_AXI, PS_ECC)
assert PS_TOP == -76.56 and PS_BOT == 251.56, (PS_TOP, PS_BOT)
assert (W_BEAM, W_SLAB, W_S1) == (576.0, 360.0, 9.36), (W_BEAM, W_SLAB, W_S1)
assert M_S1 == 4_680_000.0 and DL_S == 146.25, (M_S1, DL_S)
assert S1_TOP == 69.69 and S1_BOT == 105.31, (S1_TOP, S1_BOT)
assert abs(NR - 0.8944) < 5e-5 and abs(BS_T - 89.44) < 0.01, (NR, BS_T)
assert abs(YBAR - 57.03) < 0.01, YBAR
assert abs(IC - 3_246_813) < 3, IC
assert abs(SC_TOP - 141_363) < 3 and abs(SC_BOT - 56_930) < 3, (SC_TOP, SC_BOT)
assert abs(SC_TOP / SC_BOT - 2.48) < 0.01, SC_TOP / SC_BOT
assert (W_LL, M_LL) == (10.0, 5_000_000.0), (W_LL, M_LL)
assert abs(LL_TOP - 35.37) < 0.01 and abs(LL_BOT + 87.83) < 0.01, (LL_TOP, LL_BOT)
assert F_TOP == 105.1 and F_BOT == 17.5, (F_TOP, F_BOT)
assert abs(F_DECK - 52.3) < 0.05, F_DECK
assert abs(E_S1_BOT - 161.56) < 0.02 and abs(E_BOT - 42.1) < 0.05, (E_S1_BOT, E_BOT)
assert abs(ALW_D - 157.5) < 1e-9 and abs(ALW_L - 210.0) < 1e-9
assert abs(CLS_U - 37.4) < 0.05 and abs(CLS_T - 59.9) < 0.05, (CLS_U, CLS_T)
assert abs(ALW_DK - 168.0) < 1e-9
print(f"{TAG}: 3 圖 OK　Stage1 {S1_TOP}/{S1_BOT}　最終 {F_TOP}/{F_BOT}　"
      f"n={NR:.4f} b'={BS_T:.1f} ȳ={YBAR:.2f} Ic={IC:,.0f} "
      f"S={SC_TOP:,.0f}/{SC_BOT:,.0f}（比 {SC_TOP/SC_BOT:.2f}）　"
      f"版頂 {F_DECK:.1f}　誤放版DL 梁底 {E_BOT:+.1f}")


# ══════════════════════════════════════════════════════════
# 題目附圖重繪（2026-11-14，RC-U4-1 批 1；依題目正本 RC-2006-4-problem.md §4，已確認）
# 只畫考卷給的東西：15 cm 連續版、三支 30×80 梁（中心距 100）、c.g.s. 距梁底 15
# 攔：兩段 100 cm 讀成「梁中心向兩側各 100」→ 梁距 200
# ══════════════════════════════════════════════════════════
def fig_problem():
    W, Hc = 960, 520
    s = 2.6
    cv = Canvas(W, Hc, sx=s, ox=W / 2, oy=110)
    cv.panel("圖四 跨中梁與樓版斷面（重繪）", "依題目正本判讀清單 #1–#4；80 cm 量自版底，不含版")
    xe = 150.0
    cv.polygon([(-xe, HB), (xe, HB), (xe, HB + TS), (-xe, HB + TS)], "#E3E9F2", C["member"], 2.2)
    for sg in (-1, 1):                                  # 版端折斷線
        x = sg * xe
        cv.poly([(x, HB - 2), (x - sg * 3, HB + 5), (x + sg * 3, HB + 10), (x, HB + TS + 2)], C["member"], 1.6)
    for x in (-BS, 0.0, BS):
        cv.polygon([(x - BW / 2, 0), (x + BW / 2, 0), (x + BW / 2, HB), (x - BW / 2, HB)], "#EDF1F6", C["member"], 2.4)
        cv.circle((x, CGS), 2.0, "#FFFFFF", C["member"], 1.6)
        cv.line((x, HB + TS + 4), (x, HB + TS + 22), C["dim"], 1, dash="3 3")
    cv.dim((-BS, HB + TS + 18), (0, HB + TS + 18), "100 cm", off=0, label_off=-13)
    cv.dim((0, HB + TS + 18), (BS, HB + TS + 18), "100 cm", off=0, label_off=-13)
    cv.dim((xe, HB + TS), (xe, HB), "15 cm", off=-20, label_off=-24)
    cv.dim((BW / 2 + 14, HB), (BW / 2 + 14, 0), "80 cm", off=0, label_off=-24)
    cv.line((-BW / 2 - 30, CGS), (-2.2, CGS), C["muted"], 1)
    cv.text((-BW / 2 - 31, CGS + 4), "c.g.s.", 13, C["text"], "end")
    cv.dim((-BW / 2 - 8, CGS), (-BW / 2 - 8, 0), "15 cm", off=0, label_off=24)
    cv.dim((-BW / 2, 0), (BW / 2, 0), "30 cm", off=24, label_off=14)
    return compose([cv], title=f"{TAG} 題目附圖（重繪）",
                   sub="樓版厚 15 cm（f'c＝280）；預力梁 30×80 cm（f'c＝350），梁中心距 100 cm；c.g.s. 距梁底 15 cm",
                   note="兩段 100 cm 都是相鄰梁中心距（梁距 100 cm），不是梁中心到版緣",
                   path=os.path.join(OUT, f"{TAG}-fig-1-problem.svg"))


fig_problem()
