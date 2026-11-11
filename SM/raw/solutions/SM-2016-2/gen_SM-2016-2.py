# -*- coding: utf-8 -*-
"""SM-2016-2 圖解。數值取自 SM-2016-2.md §4／§5。"""
import sys, math, os
sys.path.insert(0, "/tmp/sd")
from geo import *
from geo import tag_px, seg, curve, dot, vbar

OUT = "/tmp/sd/out/SM-2016-2"
os.makedirs(OUT, exist_ok=True)

# ── 由 SM-2016-2 §4 解得 ────────────────────────────────
GW      = 9.81
W       = 100.0 / 1620.0                 # 0.061728（實驗室＝現地，因密封）
GS      = 1.62 * 1.70                    # 2.754
E_LAB   = 0.70                           # 實驗室容器內的孔隙比（題目給）
GD_LAB  = GS * GW / (1 + E_LAB)          # 15.892 kN/m³
GT_BOR  = 1800 * GW / 1000.0             # 17.658
GD_BOR  = GT_BOR / (1 + W)               # 16.6314
E_BOR   = GS * GW / GD_BOR - 1           # 0.6244
GD_FILL = 19.50
OMC     = 0.08
E_FILL  = GS * GW / GD_FILL - 1          # 0.3855
V_FILL  = 10000.0
WS_TOT  = GD_FILL * V_FILL               # 195,000 kN
V_BOR   = WS_TOT / GD_BOR                # 11,724.8 m³
DWW     = WS_TOT * (OMC - W)             # 3563.0 kN
VW      = DWW / GW                       # 363.2 m³
SR      = V_FILL / V_BOR                 # 0.8529

# 每單位土粒體積的水／空氣體積（Vw/Vs = w·Gs）
VW_LAB = W * GS;  VA_LAB = E_LAB - VW_LAB
VW_BOR = W * GS;  VA_BOR = E_BOR - VW_BOR
VW_FIL = OMC * GS; VA_FIL = E_FILL - VW_FIL
S_LAB = VW_LAB / E_LAB; S_BOR = VW_BOR / E_BOR; S_FIL = VW_FIL / E_FILL

# ══════ fig-1：三種狀態的三相體積柱（Vs 恆為 1）══════
W_, H_ = 1000, 672
cv = Canvas(W_, H_, bg="#FFFFFF")
BASE, SCALE, BW = 430, 152.0, 132
CXS = [260, 500, 740]
COLS = [C["member2"], C["deform"], C["load"]]
STATES = [("實驗室容器內（題目給 e = 0.70）", E_LAB, VW_LAB, VA_LAB, GD_LAB, S_LAB, "重新填入容器，最鬆"),
          ("現地借土處（挖孔試驗實測）", E_BOR, VW_BOR, VA_BOR, GD_BOR, S_BOR, "由 450 kgf / 0.25 m³ 反算"),
          ("夯實後填方（OMC 夯至 γ_d,max）", E_FILL, VW_FIL, VA_FIL, GD_FILL, S_FIL, "含水量改為 OMC = 8%")]
for cx, col, (t, e, vw, va, gd, s, sub) in zip(CXS, COLS, STATES):
    top = vbar(cv, cx, BASE, BW,
               [(1.0, "rgba(63,74,90,0.30)", C["member"], "土粒 V_s = 1"),
                (vw, "rgba(29,78,216,0.22)", C["deform"], "水"),
                (va, "rgba(0,0,0,0.05)", C["muted"], "空氣")],
               SCALE, t.split("（")[0], sub, col)
    cv.text_px(cx, top - 20, "e = %.4f" % e, 13.5, col, weight="700")
    cv.text_px(cx, top - 42, "γ_d = %.2f kN/m³" % gd, 13, col, weight="700")
    cv.text_px(cx, BASE + 70, "S = %.1f%%　（V_w/V_s = %.3f）" % (s * 100, vw), 12.5, C["muted"])
seg(cv, (CXS[0] - BW / 2 - 14, BASE - SCALE), (CXS[2] + BW / 2 + 14, BASE - SCALE),
    C["member"], 1.6, "6 4")
tag_px(cv, CXS[2] + BW / 2 + 20, BASE - SCALE, "土粒體積永遠不變", 12.5, C["muted"],
       anchor="start", weight="400")
# 兩兩比較的箭頭
for i, (a, b, lab) in enumerate([(0, 1, "容器裡比現地還鬆"), (1, 2, "夯實後才真正變緊")]):
    x0 = CXS[a] + BW / 2 + 6; x1 = CXS[b] - BW / 2 - 6
    y = BASE - 96
    seg(cv, (x0, y), (x1, y), C["accent"], 2.0)
    cv.parts.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                    % (x1, y, x1 - 10, y - 5, x1 - 10, y + 5, C["accent"]))
    tag_px(cv, (x0 + x1) / 2, y - 18, lab, 12.5, C["accent"])

cv.text_px(W_ / 2, 34, "圖 1　三種狀態的三相組成：只有土粒那一格是共通的", 17.5,
           C["text"], weight="700")
cv.text_px(W_ / 2, 60, "柱高 = 1 + e（以土粒體積為 1 正規化）；含水量在前兩格相同（密封送驗），第三格才改為 OMC",
           12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 118,
           "攔錯用：實驗室容器內的 e = 0.70 是「重新填入」造成的狀態，比現地的 e = %.4f 還鬆。" % E_BOR,
           13.5, C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 92,
           "它只能用來反推比重 G_s（材質常數，不隨鬆緊改變），不能拿來當現地孔隙比。", 13,
           C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 64,
           "若誤把 e = 0.70 當現地值，會得 γ_d = %.2f 而非 %.2f，第三小題的借土量會多算 %.0f m³。"
           % (GD_LAB, GD_BOR, WS_TOT / GD_LAB - V_BOR), 12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 36,
           "G_s = ρ_{d,lab} (1+e) / ρ_w = 1.62 × 1.70 = %.3f" % GS, 14, C["text"], weight="700")
cv.save(OUT + "/SM-2016-2-fig-1-three-states.svg")

# ══════ fig-2：借土 → 填方 的體積與加水量 ══════
W_, H_ = 980, 668
cv = Canvas(W_, H_, bg="#FFFFFF")
BASE, BW = 430, 190
VSCALE = 300.0 / V_BOR          # 每 m³ 對應的像素
CX1, CX2 = 280, 690
# 借土（現地）
hb = V_BOR * VSCALE
cv.rect_px(CX1 - BW / 2, BASE - hb, BW, hb, "rgba(180,83,9,0.18)", 0, C["accent"], 2.2)
cv.text_px(CX1, BASE - hb / 2 - 10, "疏濬處借土", 14, C["accent"], weight="700")
cv.text_px(CX1, BASE - hb / 2 + 14, "%.0f m³" % V_BOR, 15, C["accent"], weight="700")
cv.text_px(CX1, BASE + 24, "γ_d = %.2f kN/m³（鬆）" % GD_BOR, 13, C["muted"])
cv.text_px(CX1, BASE + 46, "ω = 6.17%", 12.5, C["muted"])
# 填方（夯實後）
hf = V_FILL * VSCALE
cv.rect_px(CX2 - BW / 2, BASE - hf, BW, hf, "rgba(46,125,111,0.18)", 0, C["bmd"], 2.2)
cv.text_px(CX2, BASE - hf / 2 - 10, "夯實後填方", 14, C["bmd"], weight="700")
cv.text_px(CX2, BASE - hf / 2 + 14, "%.0f m³" % V_FILL, 15, C["bmd"], weight="700")
cv.text_px(CX2, BASE + 24, "γ_d,max = %.2f kN/m³（緊）" % GD_FILL, 13, C["muted"])
cv.text_px(CX2, BASE + 46, "ω = OMC = 8%", 12.5, C["muted"])
# 中間的守恆錨
ax0 = CX1 + BW / 2 + 10; ax1 = CX2 - BW / 2 - 10
seg(cv, (ax0, BASE - 150), (ax1, BASE - 150), C["member"], 3.0)
cv.parts.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                % (ax1, BASE - 150, ax1 - 13, BASE - 157, ax1 - 13, BASE - 143, C["member"]))
tag_px(cv, (ax0 + ax1) / 2, BASE - 176, "乾土重 W_s = 195,000 kN　不變", 13.5, C["member"])
tag_px(cv, (ax0 + ax1) / 2, BASE - 124,
       "體積比 %.0f / %.0f = %.3f（縮 %.1f%%）" % (V_FILL, V_BOR, SR, (1 - SR) * 100),
       12.5, C["muted"], weight="400")
# 加水
wy = BASE - hf - 40
cv.rect_px(CX2 - BW / 2, wy - VW * VSCALE, BW, VW * VSCALE,
           "rgba(29,78,216,0.30)", 0, C["deform"], 2.0)
tag_px(cv, CX2 - BW / 2 - 16, wy - VW * VSCALE / 2,
       "另加水 %.1f m³（%.0f kN）" % (VW, DWW), 13, C["deform"], anchor="end")
cv.text_px(W_ / 2, 34, "圖 2　借土量由「乾土重不變」決定，不是由體積比", 17.5, C["text"], weight="700")
cv.text_px(W_ / 2, 60, "兩個方塊高度依實際體積等比繪製；加水方塊同一比例尺", 12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 118,
           "V_{borrow} = W_s / γ_{d,borrow} = 195,000 / %.4f = %.1f m³" % (GD_BOR, V_BOR),
           14.5, C["text"], weight="700")
cv.text_px(W_ / 2, H_ - 92,
           "ΔW_w = W_s × (OMC − ω) = 195,000 × (0.08 − 0.06173) = %.0f kN → %.1f m³"
           % (DWW, VW), 14.5, C["deform"], weight="700")
cv.text_px(W_ / 2, H_ - 62,
           "攔錯用：加水量的分母是「乾土重」，不是濕土重也不是體積。", 13,
           C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 38,
           "若誤用夯實後濕土重（195,000 × 1.08）當基準，加水量會多算 8%；"
           "若用借土的濕重更會偏離。", 12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 14,
           "另：γ_d 若取到小數第二位（16.63）代入，借土量得 11,725.8 m³，與 %.1f m³ 差 1 m³ 以內。"
           % V_BOR, 12, C["muted"])
cv.save(OUT + "/SM-2016-2-fig-2-borrow-fill.svg")

print("w=%.6f Gs=%.4f gd_lab=%.4f gd_bor=%.4f e_bor=%.4f e_fill=%.4f"
      % (W, GS, GD_LAB, GD_BOR, E_BOR, E_FILL))
print("V_borrow=%.2f  dWw=%.2f kN  Vw=%.2f m3  收縮比=%.4f" % (V_BOR, DWW, VW, SR))
print("誤用 e=0.70 的借土量=%.1f（多 %.0f m3）" % (WS_TOT / GD_LAB, WS_TOT / GD_LAB - V_BOR))
print("S: lab=%.1f%% bor=%.1f%% fill=%.1f%%" % (S_LAB*100, S_BOR*100, S_FIL*100))
