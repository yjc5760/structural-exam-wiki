# -*- coding: utf-8 -*-
"""SM-2007-1 圖解。所有數值取自 SM-2007-1.md §4（Step 1–4）。
用法：python gen_SM-2007-1.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 由 SM-2007-1 §4 解得 ──
GW = 9.81
D, H0, H1, E0, GS = 6.35, 2.5, 1.9, 1.30, 2.72      # 題給
HS = H0 / (1 + E0)                  # 1.0870 cm 土粒「等效高度」，壓縮前後不變
DE = (H0 - H1) / H0 * (1 + E0)      # 0.552
E1 = E0 - DE                        # 0.748
assert abs(E1 - (H1 - HS) / HS) < 1e-12
G0 = (GS + E0) / (1 + E0) * GW      # 17.15
G1 = (GS + E1) / (1 + E1) * GW      # 19.46
W0, W1 = E0 / GS, E1 / GS           # 47.79% / 27.50%
A = 3.141592653589793 * D ** 2 / 4  # 31.67 cm²
VWOUT = (H0 - H1) * A               # 19.0 cm³ 排出水
MS = HS * A * GS                    # 93.6 g 土粒

W_, H_ = 980, 800
cv = Canvas(W_, H_, bg="#FFFFFF")
BASE, SCALE, BW = 560, 170.0, 180   # 1 cm 試體高 = 170 px
CX1, CX2 = 300, 650
tops = []
for cx, (tt, hw, e, g, w, col) in zip(
        (CX1, CX2),
        [("壓縮前  H_0 = 2.50 cm", H0 - HS, E0, G0, W0, C["deform"]),
         ("壓縮後  H_1 = 1.90 cm", H1 - HS, E1, G1, W1, C["load"])]):
    top = vbar(cv, cx, BASE, BW,
               [(HS, "rgba(63,74,90,0.30)", C["member"], "土粒 H_s = {:.4f} cm".format(HS)),
                (hw, "rgba(29,78,216,0.24)", C["deform"], "水（飽和）{:.4f} cm".format(hw))],
               SCALE, tt, "e = {:.3f}　w = {:.2f}%　γ_{{sat}} = {:.2f} kN/m³".format(e, w * 100, g), col)
    tops.append(top)
# 土粒頂共同基準線
y = BASE - HS * SCALE
seg(cv, (CX1 - BW / 2 - 14, y), (CX2 + BW / 2 + 14, y), C["member"], 1.6, "6 4")
tag_px(cv, CX2 + BW / 2 + 20, y, "土粒高 H_s 不變", 12, C["member"], anchor="start", weight="400")
# 頂端高差 = 排出的水
seg(cv, (CX1 + BW / 2 + 6, tops[0]), (CX2 + BW / 2 + 14, tops[0]), C["accent"], 1.4, "4 4")
AX = CX2 + BW / 2 + 40
seg(cv, (AX, tops[0]), (AX, tops[1]), C["accent"], 2.6)
for yy, dy in ((tops[0], 1), (tops[1], -1)):
    cv.parts.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                    % (AX, yy, AX - 5, yy + 9 * dy, AX + 5, yy + 9 * dy, C["accent"]))
tag_px(cv, AX + 10, (tops[0] + tops[1]) / 2 - 12, "ΔH = {:.2f} cm 全是排出的水".format(H0 - H1),
       12.5, C["accent"], anchor="start")
tag_px(cv, AX + 10, (tops[0] + tops[1]) / 2 + 16, "= {:.1f} cm³ = {:.1f} g".format(VWOUT, VWOUT),
       12, C["accent"], anchor="start", weight="400")

cv.text_px(W_ / 2, 34, "圖 1　一維壓縮：土粒高度不變，少掉的厚度全是孔隙水", 17.5, C["text"], weight="700")
cv.text_px(W_ / 2, 60, "高度依實際厚度等比繪製（1 cm = 170 px）；直徑 6.35 cm 不變，故體積比 = 厚度比",
           12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 150,
           "Δe = ΔH/H_s = ΔH(1+e_0)/H_0 = 0.24 × 2.30 = {:.3f}，e_1 = {:.3f}".format(DE, E1),
           13.5, C["text"], weight="700")
cv.text_px(W_ / 2, H_ - 122,
           "含水量 w = e/G_s（飽和）：{:.2f}% → {:.2f}%，減少 {:.2f} 個百分點".format(
               W0 * 100, W1 * 100, (W0 - W1) * 100), 13.5, C["text"], weight="700")
cv.text_px(W_ / 2, H_ - 90,
           "攔錯用：分母是 H_s（或 H_0/(1+e_0)），不是 H_0——寫成 Δe = ΔH/H_0 會得 e_1 = 1.06；", 13,
           C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 66,
           "孔隙裡只有水，沒有空氣跑進來，所以壓縮後仍用 S = 1 的 γ_{sat} 與 w = e/G_s。", 13,
           C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 36,
           "驗算：土粒 {:.1f} g，排水 {:.1f} g → Δw = {:.1f}/{:.1f} = {:.2f}% ✓".format(
               MS, VWOUT, VWOUT, MS, VWOUT / MS * 100), 12.5, C["muted"])
cv.save(os.path.join(OUT, "SM-2007-1-fig-1-compression-phase.svg"))
print("e1", E1, "G0", G0, "G1", G1, "W0", W0, "W1", W1, "Vout", VWOUT, "Ms", MS)
