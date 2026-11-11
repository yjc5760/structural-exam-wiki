# -*- coding: utf-8 -*-
"""SM-2019-3 圖解。數值取自 SM-2019-3.md §4 Step 1~6。"""
import sys, math, os
sys.path.insert(0, "/tmp/sd")
from geo import *
from geo import tag_px

OUT = "/tmp/sd/out/SM-2019-3"
os.makedirs(OUT, exist_ok=True)

# ── 由 SM-2019-3 §4 解得 ────────────────────────────────
EMAX, EMIN, GS, GW = 0.95, 0.55, 2.65, 9.81
DR0, RC, H0 = 0.50, 0.95, 2.0
E0     = EMAX - DR0 * (EMAX - EMIN)          # 0.75
GD0    = GS * GW / (1 + E0)                  # 14.855
GDMAX  = GS * GW / (1 + EMIN)                # 16.772
GDMIN  = GS * GW / (1 + EMAX)                # 13.332
GDF    = RC * GDMAX                          # 15.933
EF     = GS * GW / GDF - 1                   # 0.63158
DRF    = (EMAX - EF) / (EMAX - EMIN)         # 0.7960
RC0    = GD0 / GDMAX                         # 0.8857
DH     = H0 * (E0 - EF) / (1 + E0)           # 0.13534
DH_BAD = H0 * (E0 - EF) / (1 + EF)           # 0.14517（分母誤用 1+e_f）

# ══════ fig-1：同一根孔隙比軸上的兩把尺 ══════
W, H = 1010, 700
ML, MR = 150, 130
AX = lambda e: ML + (EMAX - e) / (EMAX - EMIN) * (W - ML - MR)   # e 大在左、小在右
Y_E, Y_DR, Y_RC = 190, 310, 430
def seg(p0, p1, col, w, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    cv.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%s" '
                    'stroke-linecap="round"%s/>' % (p0[0], p0[1], p1[0], p1[1], col, w, d))
cv = Canvas(W, H, bg="#FFFFFF")

# 主軸：孔隙比 e
seg((AX(EMAX), Y_E), (AX(EMIN), Y_E), C["member"], 3.0)
for e, lab, col in [(EMAX, "e_{max} = 0.95", C["muted"]), (E0, "e_0 = 0.75", C["deform"]),
                    (EF, "e_f = 0.632", C["load"]), (EMIN, "e_{min} = 0.55", C["muted"])]:
    seg((AX(e), Y_E - 11), (AX(e), Y_E + 11), col, 2.4)
    cv.math_px(AX(e), Y_E - 30, lab, 14, col, weight="700")
cv.text_px(ML - 22, Y_E, "孔隙比 e", 13.5, C["text"], anchor="end")
cv.text_px((AX(EMAX) + AX(EMIN)) / 2, Y_E - 62, "最鬆 ←—————————————→ 最緊", 12.5, C["muted"])

# 尺一：相對密度 D_r（線性於 e）
seg((AX(EMAX), Y_DR), (AX(EMIN), Y_DR), C["bmd"], 2.6)
for e in [EMAX - i * (EMAX - EMIN) / 10 for i in range(11)]:
    seg((AX(e), Y_DR - 6), (AX(e), Y_DR + 6), C["bmd"], 1.4)
for e, v in [(EMAX, 0), (EMIN, 100)]:
    cv.text_px(AX(e), Y_DR + 24, "%d%%" % v, 12.5, C["bmd"])
cv.text_px(ML - 22, Y_DR, "相對密度 D_r", 13.5, C["bmd"], anchor="end", weight="700")
cv.text_px(ML - 22, Y_DR + 22, "（以 e 定義）", 11.5, C["muted"], anchor="end")

# 尺二：相對夯實度 R_c（非線性於 e，因 γ_d = G_s γ_w /(1+e)）
seg((AX(EMAX), Y_RC), (AX(EMIN), Y_RC), C["load"], 2.6)
for pct in [80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100]:
    e = GS * GW / (pct / 100.0 * GDMAX) - 1
    if EMIN - 1e-9 <= e <= EMAX + 1e-9:
        seg((AX(e), Y_RC - 6), (AX(e), Y_RC + 6), C["load"], 1.4)
        if pct in (80, 90, 100):
            cv.text_px(AX(e), Y_RC + 24, "%d%%" % pct, 12.5, C["load"])
e80 = GS * GW / (0.80 * GDMAX) - 1
cv.text_px(ML - 22, Y_RC, "相對夯實度 R_c", 13.5, C["load"], anchor="end", weight="700")
cv.text_px(ML - 22, Y_RC + 22, "（以 γ_d 定義）", 11.5, C["muted"], anchor="end")
cv.text_px(AX(EMAX) + 30, Y_RC - 20, "左端 R_c = 79.5%（不是 0）", 11.5, C["muted"], anchor="start")

# 兩個狀態的垂直對照線
for e, col in [(E0, C["deform"]), (EF, C["load"])]:
    seg((AX(e), Y_E + 12), (AX(e), Y_RC + 36), col, 1.6, "5 4")
    for yy in (Y_DR, Y_RC):
        cv.parts.append('<circle cx="%.1f" cy="%.1f" r="5.4" fill="%s" stroke="#FFFFFF" '
                        'stroke-width="2"/>' % (AX(e), yy, col))
tag_px(cv, AX(E0), Y_RC + 58, "夯實前　D_r = 50.0%　R_c = {:.1f}%".format(RC0 * 100),
       13, C["deform"])
tag_px(cv, AX(EF), Y_RC + 96, "夯實後　D_r = {:.1f}%　R_c = 95.0%".format(DRF * 100),
       13, C["load"])

cv.text_px(W / 2, 34, "圖 1　D_r 與 R_c 是同一根 e 軸上的兩把不同的尺", 17.5, C["text"], weight="700")
cv.text_px(W / 2, 60, "D_r 對 e 線性、兩端固定為 0 與 100%；R_c 對 γ_d 線性，故對 e 非線性、"
                      "且左端不是 0", 12.5, C["muted"])
cv.text_px(W / 2, H - 104,
           "同一個夯實後狀態：D_r = {:.1f}%，R_c = 95.0%——兩個數字都對，但意義不同。"
           .format(DRF * 100), 13.5, C["text"], weight="700")
cv.text_px(W / 2, H - 74,
           "攔錯用：題目要的是 R_c = 95%，若誤讀成 D_r = 95%，會得 e_f = 0.95 − 0.95×0.40 = 0.570，",
           13, C["accent"], weight="700")
cv.text_px(W / 2, H - 48,
           "ΔH 變成 {:.3f} m（正解 {:.3f} m），整整多了 {:.0f}%。"
           .format(H0 * (E0 - (EMAX - 0.95 * (EMAX - EMIN))) / (1 + E0), DH,
                   (H0 * (E0 - (EMAX - 0.95 * (EMAX - EMIN))) / (1 + E0) / DH - 1) * 100),
           13, C["accent"], weight="700")
cv.save(OUT + "/SM-2019-3-fig-1-two-rulers.svg")

# ══════ fig-2：三相體積柱狀對照與 ΔH ══════
W, H = 940, 700
cv = Canvas(W, H, bg="#FFFFFF")
BASE_Y, SCALE = 480, 200.0      # 每 1 單位體積 = 200 px
BW = 150
def column(cx, e, title, col, sub):
    hs, hv = 1.0 * SCALE, e * SCALE
    cv.rect_px(cx - BW / 2, BASE_Y - hs, BW, hs, "rgba(63,74,90,0.30)", 0, C["member"], 1.6)
    cv.rect_px(cx - BW / 2, BASE_Y - hs - hv, BW, hv, "rgba(29,78,216,0.16)", 0, col, 2.0)
    cv.text_px(cx, BASE_Y - hs / 2, "土粒 V_s = 1", 13, C["text"])
    cv.text_px(cx, BASE_Y - hs - hv / 2, "孔隙 V_v = e", 13, col)
    cv.math_px(cx, BASE_Y - hs - hv / 2 + 20, "= %.3f" % e, 13, col, weight="700")
    cv.text_px(cx, BASE_Y + 26, title, 14, col, weight="700")
    cv.text_px(cx, BASE_Y + 48, sub, 12.5, C["muted"])
    return BASE_Y - hs - hv

CX1, CX2 = 330, 640
top1 = column(CX1, E0, "夯實前", C["deform"], "D_r = 50%，γ_d = {:.2f} kN/m³".format(GD0))
top2 = column(CX2, EF, "夯實後", C["load"], "R_c = 95%，γ_d = {:.2f} kN/m³".format(GDF))
seg((CX1 - BW / 2 - 10, BASE_Y - SCALE), (CX2 + BW / 2 + 10, BASE_Y - SCALE),
    C["member"], 1.4, "5 4")
cv.text_px(CX2 + BW / 2 + 16, BASE_Y - SCALE, "土粒體積不變", 12.5, C["muted"], anchor="start")
seg((CX1 + BW / 2 + 6, top1), (CX2 + BW / 2 + 90, top1), C["deform"], 1.2, "4 4")
seg((CX2 + BW / 2 + 6, top2), (CX2 + BW / 2 + 90, top2), C["load"], 1.2, "4 4")
cv.arrow_px = None
cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.6"/>'
                % (CX2 + BW / 2 + 70, top1, CX2 + BW / 2 + 70, top2, C["accent"]))
for yy, dy in ((top1, 1), (top2, -1)):
    cv.parts.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                    % (CX2 + BW / 2 + 70, yy, CX2 + BW / 2 + 64, yy + 9 * dy,
                       CX2 + BW / 2 + 76, yy + 9 * dy, C["accent"]))
tag_px(cv, CX2 + BW / 2 + 84, (top1 + top2) / 2 - 11, "Δe = {:.4f}".format(E0 - EF), 13,
       C["accent"], anchor="start")
tag_px(cv, CX2 + BW / 2 + 84, (top1 + top2) / 2 + 13, "ΔH = {:.3f} m".format(DH), 13,
       C["accent"], anchor="start")
# 左側標出實際層厚
for cx, e, lab, col in [(CX1, E0, "H_0 = 2.000 m", C["deform"]),
                        (CX2, EF, "H = {:.3f} m".format(H0 - DH), C["load"])]:
    xx = cx - BW / 2 - 16
    tp = BASE_Y - (1 + e) * SCALE
    cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                    'stroke-width="1.6"/>' % (xx, tp, xx, BASE_Y, col))
    for yy, dy in ((tp, 1), (BASE_Y, -1)):
        cv.parts.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                        % (xx, yy, xx - 5, yy + 9 * dy, xx + 5, yy + 9 * dy, col))
    cv.math_px(xx - 12, (tp + BASE_Y) / 2, lab, 13, col, anchor="end", weight="700")

cv.text_px(W / 2, 34, "圖 2　高度只隨孔隙變，土粒那一格從頭到尾不動", 17.5, C["text"], weight="700")
cv.text_px(W / 2, 60, "故 ΔH / H_0 = Δe / (1 + e_0)——分母是「初始」的 1 + e_0", 12.5, C["muted"])
cv.text_px(W / 2, H - 104,
           "ΔH = H_0 · Δe / (1 + e_0) = 2.0 × {:.4f} / {:.2f} = {:.4f} m ≈ {:.1f} cm"
           .format(E0 - EF, 1 + E0, DH, DH * 100), 15, C["text"], weight="700")
cv.text_px(W / 2, H - 76,
           "攔錯用：分母若誤用 1 + e_f = {:.3f}，得 ΔH = {:.4f} m，高估 {:.1f}%。"
           .format(1 + EF, DH_BAD, (DH_BAD / DH - 1) * 100), 13, C["accent"], weight="700")
cv.text_px(W / 2, H - 50,
           "檢核：夯實後總高 = 2.000 − {:.3f} = {:.3f} m，其中土粒仍佔 2.000/(1+0.75) = 1.143 m。"
           .format(DH, H0 - DH), 12.5, C["muted"])
cv.text_px(W / 2, H - 24,
           "驗算：1.143 × (1 + {:.3f}) = {:.3f} m ✓ 與上式一致。"
           .format(EF, H0 / (1 + E0) * (1 + EF)), 12.5, C["muted"])
cv.save(OUT + "/SM-2019-3-fig-2-phase-columns.svg")

print("e0=%.4f gd0=%.4f gdmax=%.4f gdf=%.4f ef=%.5f Drf=%.4f Rc0=%.4f"
      % (E0, GD0, GDMAX, GDF, EF, DRF, RC0))
print("dH=%.5f  dH_bad=%.5f  Rc@emax=%.4f" % (DH, DH_BAD, GDMIN / GDMAX))
print("誤把 Rc 當 Dr: e=%.4f dH=%.4f" % (EMAX - 0.95*(EMAX-EMIN),
      H0*(E0-(EMAX-0.95*(EMAX-EMIN)))/(1+E0)))
print("H_after=%.4f  Vs_height=%.4f  check=%.4f" % (H0-DH, H0/(1+E0), H0/(1+E0)*(1+EF)))
