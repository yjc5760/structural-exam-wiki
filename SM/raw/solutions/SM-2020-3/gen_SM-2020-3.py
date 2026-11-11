# -*- coding: utf-8 -*-
"""SM-2020-3 圖解。數值取自 SM-2020-3.md §4（方法一與方法二）。"""
import sys, math, os
sys.path.insert(0, "/tmp/sd")
from geo import *
from geo import tag_px, seg, curve, dot, vbar

OUT = "/tmp/sd/out/SM-2020-3"
os.makedirs(OUT, exist_ok=True)

# ── 由 SM-2020-3 §4 解得 ────────────────────────────────
GW    = 9.81
V     = 500.0; W = 900.0; WS = 850.0
VMIN  = 440.0; VMAX = 640.0; S = 0.27
WW    = W - WS                       # 50 g
VW    = WW / 1.0                     # 50 ml
VV    = VW / S                       # 185.185
VS    = V - VV                       # 314.815
VA    = VV - VW                      # 135.185
GS    = WS / VS                      # 2.700
E     = (V - VS) / VS                # 0.58824
EMAX  = (VMAX - VS) / VS             # 1.03294
EMIN  = (VMIN - VS) / VS             # 0.39765
DR    = (EMAX - E) / (EMAX - EMIN)   # 0.70000
DR_V  = (VMAX - V) / (VMAX - VMIN)   # 0.70000
GD    = WS / V * GW                  # 16.677 kN/m³
GDMAX = WS / VMIN * GW               # 18.951
GDMIN = WS / VMAX * GW               # 13.029
DR_G  = (GD - GDMIN) / (GDMAX - GDMIN) * (GDMAX / GD)

# ══════ fig-1：三狀態體積柱 ＋ D_r 標尺 ══════
W_, H_ = 1120, 700
cv = Canvas(W_, H_, bg="#FFFFFF")
BASE, SCALE, BW = 430, 0.42, 118      # 每 1 ml = 0.42 px
CXS = [290, 530, 770]
COLS = [C["member2"], C["deform"], C["load"]]
DATA = [("最疏鬆", VMAX, EMAX, GDMIN, "夯實模內鬆填"),
        ("現地取樣", V, E, GD, "取樣器 500 ml"),
        ("最緊密", VMIN, EMIN, GDMAX, "夯實模內夯緊")]
tops = []
for cx, col, (t, vol, e, gd, sub) in zip(CXS, COLS, DATA):
    top = vbar(cv, cx, BASE, BW,
               [(VS, "rgba(63,74,90,0.30)", C["member"], "土粒 V_s"),
                (vol - VS, "rgba(0,0,0,0.05)", col, "孔隙 V_v")],
               SCALE, t, sub, col)
    tops.append(top)
    cv.text_px(cx, top - 20, "V = %.0f ml" % vol, 14, col, weight="700")
    cv.text_px(cx, top - 42, "e = %.4f" % e, 13, col, weight="700")
    cv.text_px(cx, BASE + 70, "γ_d = %.2f kN/m³" % gd, 12.5, C["muted"])
seg(cv, (CXS[0] - BW / 2 - 150, BASE - VS * SCALE), (CXS[2] + BW / 2 + 12, BASE - VS * SCALE),
    C["member"], 1.8, "6 4")
tag_px(cv, CXS[0] - BW / 2 - 18, BASE - VS * SCALE,
       "V_s = %.1f ml 固定" % VS, 12.5, C["member"], anchor="end")

# D_r 標尺：0% 對齊最疏鬆的柱頂，100% 對齊最緊密的柱頂
XR = CXS[2] + BW / 2 + 160
y0, y100 = tops[0], tops[2]
seg(cv, (XR, y0), (XR, y100), C["accent"], 3.0)
for pct in range(0, 101, 10):
    yy = y0 + (y100 - y0) * pct / 100.0
    seg(cv, (XR - 7, yy), (XR + 7, yy), C["accent"], 1.6)
    if pct % 50 == 0:
        cv.text_px(XR + 14, yy, "%d%%" % pct, 12.5, C["accent"], anchor="start")
cv.text_px(XR, y0 - 26, "D_r 標尺", 13, C["accent"], weight="700")
y_now = y0 + (y100 - y0) * DR
seg(cv, (tops and CXS[1], tops[1]), (XR, y_now), C["accent"], 1.4, "4 4")
dot(cv, XR, y_now, 7.0, C["accent"])
tag_px(cv, XR + 46, y_now, "D_r = 70%", 13.5, C["accent"], anchor="start")
for i, yy in enumerate(tops):
    seg(cv, (CXS[i] + BW / 2 + 4, yy), (XR - 10, yy), C["muted"], 1.0, "3 4")

cv.text_px(W_ / 2, 34, "圖 1　三個狀態的土粒體積完全相同，只有孔隙在變", 17.5,
           C["text"], weight="700")
cv.text_px(W_ / 2, 60, "柱高即題目給的總體積（640 / 500 / 440 ml），灰色底座是同一塊 %.1f ml 的土粒" % VS,
           12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 122,
           "因為 V_s 固定，e = (V − V_s)/V_s 對 V 是線性的，兩種算法必然給同一個答案：",
           13, C["text"])
cv.text_px(W_ / 2, H_ - 96,
           "體積法　D_r = (V_max − V)/(V_max − V_min) = (640 − 500)/(640 − 440) = %.3f" % DR_V,
           14, C["bmd"], weight="700")
cv.text_px(W_ / 2, H_ - 70,
           "孔隙比法　D_r = (e_max − e)/(e_max − e_min) = (%.4f − %.4f)/(%.4f − %.4f) = %.3f"
           % (EMAX, E, EMAX, EMIN, DR), 14, C["load"], weight="700")
cv.text_px(W_ / 2, H_ - 42,
           "攔錯用：體積最大＝最疏鬆＝D_r 0%，體積最小＝最緊密＝D_r 100%——鬆緊一旦搞反，答案變 30%。",
           13, C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 18,
           "注意標尺是等距的（D_r 對 V 線性），但 γ_d 那一列的間距並不等距（13.03 → 16.68 → 18.95）。",
           12.5, C["muted"])
cv.save(OUT + "/SM-2020-3-fig-1-three-volumes.svg")

# ══════ fig-2：現地 500 ml 的三相圖（驗證 G_s = 2.70）══════
W_, H_ = 900, 620
cv = Canvas(W_, H_, bg="#FFFFFF")
BASE, SCALE, BW = 430, 0.60, 210
CX = 300
top = vbar(cv, CX, BASE, BW,
           [(VS, "rgba(63,74,90,0.30)", C["member"], None),
            (VW, "rgba(29,78,216,0.24)", C["deform"], None),
            (VA, "rgba(0,0,0,0.05)", C["muted"], None)],
           SCALE, None, None)
ys = BASE - VS * SCALE
yw = ys - VW * SCALE
ya = yw - VA * SCALE
LX = CX + BW / 2 + 24
for y_lo, y_hi, lab, val, wt, col in [
        (BASE, ys, "土粒 V_s", "%.1f ml" % VS, "W_s = 850 g", C["member"]),
        (ys, yw, "水 V_w", "%.0f ml" % VW, "W_w = 50 g", C["deform"]),
        (yw, ya, "空氣 V_a", "%.1f ml" % VA, "重量 = 0", C["muted"])]:
    ym = (y_lo + y_hi) / 2
    seg(cv, (CX + BW / 2 + 4, ym), (LX - 8, ym), col, 1.0, "3 4")
    cv.text_px(LX, ym - 12, "%s = %s" % (lab, val), 13.5, col, anchor="start", weight="700")
    cv.text_px(LX, ym + 10, wt, 12.5, C["muted"], anchor="start")
# 孔隙括號
BX = CX - BW / 2 - 20
seg(cv, (BX, ys), (BX, ya), C["accent"], 2.2)
seg(cv, (BX, ys), (BX + 10, ys), C["accent"], 2.2)
seg(cv, (BX, ya), (BX + 10, ya), C["accent"], 2.2)
cv.text_px(BX - 12, (ys + ya) / 2 - 12, "孔隙 V_v", 13.5, C["accent"], anchor="end", weight="700")
cv.text_px(BX - 12, (ys + ya) / 2 + 10, "= %.2f ml" % VV, 13, C["accent"], anchor="end")
cv.text_px(CX, BASE + 26, "現地取樣 500 ml", 14, C["text"], weight="700")

cv.text_px(W_ / 2, 34, "圖 2　由飽和度倒推土粒體積，順手驗出 G_s = 2.70", 17.5,
           C["text"], weight="700")
cv.text_px(W_ / 2, 60, "三段高度依實際體積等比繪製（1 ml = 0.6 px）", 12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 142,
           "V_w = W_w/γ_w = 50 ml　→　V_v = V_w/S = 50/0.27 = %.2f ml　→　V_s = 500 − V_v = %.2f ml"
           % (VV, VS), 13.5, C["text"], weight="700")
cv.text_px(W_ / 2, H_ - 114,
           "G_s = W_s/(V_s·γ_w) = 850/%.2f = %.3f" % (VS, GS), 15, C["bmd"], weight="700")
cv.text_px(W_ / 2, H_ - 86,
           "這個 2.70 是資料自洽性的檢核：若算出 2.2 或 3.1，代表題目數據或計算有問題。",
           13, C["bmd"], weight="700")
cv.text_px(W_ / 2, H_ - 58,
           "攔錯用：V_v = V_w / S，不是 V_w × S。S = 27% 代表孔隙只有 27% 裝水，",
           13, C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 34,
           "所以孔隙比水多得多（%.2f ml vs 50 ml）；乘除顛倒會得 V_v = 13.5 ml，V_s 變成 486.5 ml、G_s = 1.75。"
           % VV, 12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 12,
           "本題給的 S、W、W_s 對「體積法」是冗餘資訊，但正是它們讓這張驗證圖成立。",
           12.5, C["muted"])
cv.save(OUT + "/SM-2020-3-fig-2-phase-check.svg")

print("Vv=%.4f Vs=%.4f Va=%.4f Gs=%.4f" % (VV, VS, VA, GS))
print("e=%.5f emax=%.5f emin=%.5f Dr=%.5f (體積法 %.5f, 乾單位重法 %.5f)"
      % (E, EMAX, EMIN, DR, DR_V, DR_G))
print("gd=%.3f gdmax=%.3f gdmin=%.3f" % (GD, GDMAX, GDMIN))
print("乘除顛倒: Vv=%.2f Vs=%.2f Gs=%.3f" % (50*0.27, 500-50*0.27, 850/(500-50*0.27)))
