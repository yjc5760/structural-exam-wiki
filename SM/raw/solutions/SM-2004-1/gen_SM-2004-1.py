# -*- coding: utf-8 -*-
"""SM-2004-1 圖解。數值取自 SM-2004-1.md §4／§5。"""
import sys, math, os
sys.path.insert(0, "/tmp/sd")
from geo import *
from geo import tag_px, seg, curve, dot, vbar

OUT = "/tmp/sd/out/SM-2004-1"
os.makedirs(OUT, exist_ok=True)

# ── 由 SM-2004-1 §4 解得 ────────────────────────────────
GW = 9.81
V0, M0, WC, GS = 944.0, 1955.0, 0.18, 2.70
RT = M0 / V0                      # 2.0710
RD = RT / (1 + WC)                # 1.75506
GT, GD = RT * GW, RD * GW         # 20.316 / 17.217
E0 = GS / RD - 1                  # 0.53841
S0 = WC * GS / E0                 # 0.90266
S1 = 0.95
E1 = WC * GS / S1                 # 0.51158
GD1 = GS * GW / (1 + E1)          # 17.5227
GT1 = GD1 * (1 + WC)              # 20.6768
# 體積分解（以實際 cm³）
WS = M0 / (1 + WC)                # 1656.78 g
VS = WS / GS                      # 613.62 cm³
VW = WS * WC                      # 298.22 cm³
VA0 = V0 - VS - VW                # 32.16
VV1 = E1 * VS                     # 313.92
VA1 = VV1 - VW                    # 15.70
V1 = VS + VV1                     # 927.54
SHRINK = (V0 - V1) / V0
GD_ZAV = GS * GW / (1 + WC * GS)  # 17.824

# ══════ fig-1：夯實前後的三相體積（實際 cm³）══════
W_, H_ = 980, 760
cv = Canvas(W_, H_, bg="#FFFFFF")
BASE, SCALE, BW = 520, 0.40, 176
CX1, CX2 = 300, 660
tops = []
for cx, (tt, va, vv, tot, e, s_, gd, col) in zip(
        (CX1, CX2),
        [("夯實前", VA0, VA0 + VW, V0, E0, S0, GD, C["deform"]),
         ("進一步夯實後", VA1, VV1, V1, E1, S1, GD1, C["load"])]):
    top = vbar(cv, cx, BASE, BW,
               [(VS, "rgba(63,74,90,0.30)", C["member"], "土粒 V_s = {:.1f}".format(VS)),
                (VW, "rgba(29,78,216,0.24)", C["deform"], "水 V_w = {:.1f}".format(VW)),
                (va, "rgba(0,0,0,0.06)", C["muted"], None)],
               SCALE, tt, "V = {:.1f} cm³　γ_d = {:.2f} kN/m³".format(tot, gd), col)
    tops.append(top)
    cv.text_px(cx, BASE + 70, "e = {:.4f}　S = {:.1f}%".format(e, s_ * 100), 13.5, col,
               weight="700")
    # 空氣那一格太薄，拉引線到外側標註
    ya = BASE - (VS + VW) * SCALE
    side = -1 if cx == CX1 else 1
    xe = cx + side * (BW / 2 + 30)
    seg(cv, (cx + side * BW / 2, (ya + top) / 2), (xe, (ya + top) / 2 - 34), C["muted"], 1.1, "3 3")
    tag_px(cv, xe + side * 6, (ya + top) / 2 - 44, "空氣 {:.1f} cm³".format(va), 12.5,
           C["muted"], anchor=("end" if side < 0 else "start"), weight="400")
# 兩條共通基準線
for h, lab, col in [(VS, "土粒體積不變 V_s", C["member"]),
                    (VS + VW, "水體積也不變（含水量固定 18%）", C["deform"])]:
    y = BASE - h * SCALE
    seg(cv, (CX1 - BW / 2 - 12, y), (CX2 + BW / 2 + 14, y), col, 1.6, "6 4")
    tag_px(cv, CX2 + BW / 2 + 20, y, lab, 12, col, anchor="start", weight="400")
# 擠掉的空氣：雙箭頭放兩柱之間，標籤拉到下方空白處
AX = (CX1 + BW / 2 + CX2 - BW / 2) / 2
y0, y1 = tops[0], tops[1]
seg(cv, (AX, y0), (AX, y1), C["accent"], 2.6)
for yy, dy in ((y0, 1), (y1, -1)):
    cv.parts.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                    % (AX, yy, AX - 5, yy + 9 * dy, AX + 5, yy + 9 * dy, C["accent"]))
seg(cv, (AX, (y0 + y1) / 2), (AX, (y0 + y1) / 2 + 120), C["accent"], 1.1, "3 3")
tag_px(cv, AX, (y0 + y1) / 2 + 134, "擠掉的空氣 {:.1f} cm³".format(VA0 - VA1), 13, C["accent"])
tag_px(cv, AX, (y0 + y1) / 2 + 160, "＝ 總體積的 {:.2f}%".format(SHRINK * 100), 12.5,
       C["accent"], weight="400")

cv.text_px(W_ / 2, 34, "圖 1　進一步夯實，被擠掉的只有空氣那一格", 17.5, C["text"], weight="700")
cv.text_px(W_ / 2, 60, "三段高度依實際體積等比繪製（1 cm³ = 0.40 px）；土粒與水兩格前後完全相同",
           12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 122,
           "空氣由 {:.1f} cm³ 減為 {:.1f} cm³（少了一半），飽和度才從 {:.1f}% 升到 95%。"
           .format(VA0, VA1, S0 * 100), 13.5, C["text"], weight="700")
cv.text_px(W_ / 2, H_ - 96,
           "但總體積只縮 {:.2f}%（944 → {:.1f} cm³）——因為原本空氣本來就只佔 {:.1f}%。"
           .format(SHRINK * 100, V1, VA0 / V0 * 100), 13, C["muted"])
cv.text_px(W_ / 2, H_ - 66,
           "攔錯用：「含水量不改變」是題目明講的條件，所以 V_w 那一格不能動；", 13,
           C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 42,
           "e' 要用 S'e' = ωG_s 求，不能用「體積縮多少」去猜，更不能讓水量跟著變。", 13,
           C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 16,
           "驗算：V' = V_s + e'·V_s = {:.1f} × (1 + {:.4f}) = {:.1f} cm³ ✓".format(VS, E1, V1),
           12.5, C["muted"])
cv.save(OUT + "/SM-2004-1-fig-1-phase-before-after.svg")

# ══════ fig-2：γ_d–ω 圖上的零空氣孔隙線與兩個狀態 ══════
W_, H_ = 940, 660
ML, MR, MT_, MB = 150, 130, 88, 196
cv = Canvas(W_, H_, bg="#FFFFFF")
XL, XR = 0.08, 0.30
YL, YH = 15.0, 20.0
PX = lambda w: ML + (w - XL) / (XR - XL) * (W_ - ML - MR)
PY = lambda g: H_ - MB - (g - YL) / (YH - YL) * (H_ - MT_ - MB)
for x in [0.10, 0.14, 0.18, 0.22, 0.26, 0.30]:
    seg(cv, (PX(x), PY(YL)), (PX(x), PY(YH)), C["border"], 1.1)
    cv.text_px(PX(x), PY(YL) + 19, "%d" % round(x * 100), 12.5, C["muted"])
for y in [15, 16, 17, 18, 19, 20]:
    seg(cv, (PX(XL), PY(y)), (PX(XR), PY(y)), C["border"], 1.1)
    cv.text_px(PX(XL) - 12, PY(y), "%d" % y, 12.5, C["muted"], anchor="end")
seg(cv, (PX(XL), PY(YL)), (PX(XR), PY(YL)), C["muted"], 1.9)
seg(cv, (PX(XL), PY(YL)), (PX(XL), PY(YH)), C["muted"], 1.9)
cv.text_px((PX(XL) + PX(XR)) / 2, PY(YL) + 46, "含水量 ω（%）", 13.5, C["text"])
cv.text_px(PX(XL) - 84, (PY(YL) + PY(YH)) / 2, "乾單位重 γ_d（kN/m³）", 13.5, C["text"])

def gd_of(w, S):
    return GS * GW / (1 + w * GS / S)
ws = [XL + i * (XR - XL) / 300 for i in range(301)]
LEG = []
for S, col, dash, lab in [(1.00, C["load"], None, "S = 100%（零空氣孔隙線 ZAV）"),
                          (0.95, C["accent"], "8 5", "S = 95%"),
                          (0.90, C["bmd"], "8 5", "S = 90%"),
                          (0.80, C["muted"], "3 5", "S = 80%")]:
    pts = [(PX(w), PY(gd_of(w, S))) for w in ws if YL <= gd_of(w, S) <= YH]
    curve(cv, pts, col, 3.4 if S == 1.0 else 2.2, dash)
    LEG.append((col, lab, dash))
# 圖例放左下空白區（含水量小、乾單位重低的角落必為空）
lx, ly = PX(0.093), PY(16.35)
cv.rect_px(lx - 12, ly - 20, 292, 26 * len(LEG) + 12, "#FFFFFFEE", 8, "rgba(0,0,0,0.10)", 1)
for i, (col, lab, dash) in enumerate(LEG):
    yy = ly + i * 26
    seg(cv, (lx, yy), (lx + 34, yy), col, 3.0, dash)
    cv.text_px(lx + 44, yy, lab, 12.5, col, anchor="start", weight="700")
seg(cv, (PX(WC), PY(YL)), (PX(WC), PY(GD_ZAV)), C["member"], 1.8, "5 4")
cv.text_px(PX(WC), PY(YL) - 10, "ω = 18%", 12.5, C["member"], weight="700")
for gd_, s_, lab, dyp in [(GD, S0, "夯實前　γ_d = {:.2f}，S = {:.1f}%".format(GD, S0 * 100), 26),
                          (GD1, S1, "夯實後　γ_d = {:.2f}，S = 95.0%".format(GD1), -26)]:
    dot(cv, PX(WC), PY(gd_), 7.0, C["text"])
    tag_px(cv, PX(WC) + 16, PY(gd_) + dyp, lab, 13, C["text"], anchor="start")
dot(cv, PX(WC), PY(GD_ZAV), 6.0, C["load"])
tag_px(cv, PX(WC) - 16, PY(GD_ZAV) - 26, "ZAV 上限 {:.2f}".format(GD_ZAV), 12.5, C["load"], anchor="end")

cv.text_px(W_ / 2, 32, "圖 2　含水量固定時，乾單位重有一個夯不過去的天花板", 17.5,
           C["text"], weight="700")
cv.text_px(W_ / 2, 58, "四條線皆由 γ_d = G_s γ_w / (1 + ωG_s/S) 以 G_s = 2.70 算出", 12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 126,
           "ω = 18% 時的零空氣孔隙上限：γ_{{d,ZAV}} = G_sγ_w/(1+ωG_s) = 26.487/1.486 = {:.2f} kN/m³".format(GD_ZAV),
           14, C["load"], weight="700")
cv.text_px(W_ / 2, H_ - 92,
           "本題兩個狀態（{:.2f} → {:.2f}）都在線下，故題目設定可行；但只剩 {:.2f} kN/m³ 的空間。"
           .format(GD, GD1, GD_ZAV - GD1), 13, C["text"])
cv.text_px(W_ / 2, H_ - 64,
           "攔錯用：不加水也不排水的情況下，γ_d 再怎麼夯都不可能超過這條線。", 13,
           C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 40,
           "若某題算出的 (ω, γ_d) 落在 ZAV 線上方，就是題目數據或計算有問題——"
           "SM-2008-1 正是這種案例。", 12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 16,
           "夯實曲線的「濕側」之所以都貼著 ZAV 線走，原因就在這裡。", 12.5, C["muted"])
cv.save(OUT + "/SM-2004-1-fig-2-zav-ceiling.svg")

print("rt=%.5f rd=%.5f e=%.5f S=%.4f%% e'=%.5f gd'=%.4f gt'=%.4f"
      % (RT, RD, E0, S0 * 100, E1, GD1, GT1))
print("Ws=%.2f Vs=%.2f Vw=%.2f Va0=%.2f Va1=%.2f V1=%.2f 縮 %.3f%%"
      % (WS, VS, VW, VA0, VA1, V1, SHRINK * 100))
print("ZAV(18%%)=%.4f  空氣佔比 %.2f%% → %.2f%%" % (GD_ZAV, VA0/V0*100, VA1/V1*100))
