# -*- coding: utf-8 -*-
"""SM-2008-1 圖解。數值取自 SM-2008-1.md §4 與 §5 之可行性檢核。"""
import sys, math, os
sys.path.insert(0, "/tmp/sd")
from geo import *
from geo import tag_px, seg, curve, dot, vbar

OUT = "/tmp/sd/out/SM-2008-1"
os.makedirs(OUT, exist_ok=True)

# ── 由 SM-2008-1 §4／§5 解得 ────────────────────────────
GW   = 9.81
WA, GTA, GSA = 0.09, 19.6, 2.65        # 甲
WB, GTB, GSB = 0.11, 20.6, 2.70        # 乙
WC_, GDC, VC = 0.12, 20.0, 1.0         # 夯實目標
GDA = GTA / (1 + WA)                   # 17.9817
GDB = GTB / (1 + WB)                   # 18.5586
WS  = GDC * VC                         # 20 kN
WW  = WS * WC_                         # 2.4 kN
VB  = WS / (4 * GDA + GDB)             # 0.22103
VA_ = 4 * VB                           # 0.88412
WSA, WSB = GDA * VA_, GDB * VB         # 15.898 / 4.102
WTA, WTB = GTA * VA_, GTB * VB         # 17.328 / 4.553
WWA, WWB = WSA * WA, WSB * WB          # 1.431 / 0.451
DWW = WW - WWA - WWB                   # 0.518 kN
VWADD = DWW / GW                       # 0.0528 m³
# ── 可行性檢核（§5）──
VSA, VSB = WSA / (GSA * GW), WSB / (GSB * GW)
VS = VSA + VSB                         # 0.76641
GSMIX = WS / (VS * GW)                 # 2.6601
VW_T = WW / GW                         # 0.24465
OVER = VS + VW_T - VC                  # +0.01106
E_T = GSMIX * GW / GDC - 1             # 0.30478
S_T = WC_ * GSMIX / E_T                # 1.0474
ZAV = lambda gs, w: gs * GW / (1 + w * gs)
GS_NEEDED = GDC / (GW - WC_ * GDC)     # 2.6991
W_MAX = (1 / GDC - 1 / (GSMIX * GW)) * GW   # 0.11457
# 借土區各自的相組成（每 m³ 之外的實際體積）
VwA, VwB = WWA / GW, WWB / GW
VaA = VA_ - VSA - VwA
VaB = VB - VSB - VwB

# ══════ fig-1：配方與「塞不進 1 m³」══════
W_, H_ = 1080, 720
cv = Canvas(W_, H_, bg="#FFFFFF")
BASE, SCALE = 470, 300.0               # 每 1 m³ = 300 px
BW1, BW2, BW3 = 150, 90, 180
CX1, CX2, CX3 = 210, 400, 760
vbar(cv, CX1, BASE, BW1,
     [(VSA, "rgba(63,74,90,0.30)", C["member"], None),
      (VwA, "rgba(29,78,216,0.24)", C["deform"], None),
      (VaA, "rgba(0,0,0,0.06)", C["muted"], None)],
     SCALE, "甲借土區", "V = {:.3f} m³　ω = 9%".format(VA_), C["accent"])
cv.text_px(CX1, BASE + 70, "W_s = {:.3f} kN，W_t = {:.3f} kN".format(WSA, WTA), 12, C["muted"])
vbar(cv, CX2, BASE, BW2,
     [(VSB, "rgba(63,74,90,0.30)", C["member"], None),
      (VwB, "rgba(29,78,216,0.24)", C["deform"], None),
      (VaB, "rgba(0,0,0,0.06)", C["muted"], None)],
     SCALE, "乙借土區", "V = {:.3f} m³　ω = 11%".format(VB), C["accent"])
cv.text_px(CX2, BASE + 70, "W_s = {:.3f}，W_t = {:.3f} kN".format(WSB, WTB), 12, C["muted"])
tag_px(cv, (CX1 + CX2) / 2, BASE - (VA_ + 0.06) * SCALE, "體積比 4 : 1", 13, C["accent"])

# 箭頭
ax0, ax1 = CX2 + BW2 / 2 + 20, CX3 - BW3 / 2 - 30
ay = BASE - 150
seg(cv, (ax0, ay), (ax1, ay), C["member"], 3.0)
cv.parts.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                % (ax1, ay, ax1 - 13, ay - 7, ax1 - 13, ay + 7, C["member"]))
tag_px(cv, (ax0 + ax1) / 2, ay - 26, "混合＋加水＋滾壓", 13, C["member"])
tag_px(cv, (ax0 + ax1) / 2, ay + 26, "乾土重 {:.0f} kN 守恆".format(WS), 12.5, C["muted"], weight="400")

# 目標 1 m³：土粒＋水已經超線
vbar(cv, CX3, BASE, BW3,
     [(VS, "rgba(63,74,90,0.30)", C["member"], "土粒 V_s = {:.3f}".format(VS)),
      (VW_T, "rgba(29,78,216,0.30)", C["deform"], "水 V_w = {:.3f}".format(VW_T))],
     SCALE, "夯實目標 1 m³", "γ_d = 20，ω = 12%", C["load"])
y1 = BASE - VC * SCALE
seg(cv, (CX3 - BW3 / 2 - 60, y1), (CX3 + BW3 / 2 + 60, y1), C["load"], 3.0, "9 5")
tag_px(cv, CX3 + BW3 / 2 + 66, y1, "1 m³ 的天花板", 13, C["load"], anchor="start")
ytop = BASE - (VS + VW_T) * SCALE
seg(cv, (CX3 + BW3 / 2 + 14, y1), (CX3 + BW3 / 2 + 14, ytop), C["load"], 2.4)
for yy, dy in ((y1, -1), (ytop, 1)):
    cv.parts.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                    % (CX3 + BW3 / 2 + 14, yy, CX3 + BW3 / 2 + 9, yy + 9 * dy,
                       CX3 + BW3 / 2 + 19, yy + 9 * dy, C["load"]))
tag_px(cv, CX3 - BW3 / 2 - 16, (y1 + ytop) / 2, "超出 {:.5f} m³".format(OVER), 12.5,
       C["load"], anchor="end")
tag_px(cv, CX3, ytop - 26, "V_s + V_w = {:.5f} m³".format(VS + VW_T), 13.5, C["load"])

cv.text_px(W_ / 2, 34, "圖 1　配方算得出來，但夯實目標塞不進 1 m³", 17.5, C["text"], weight="700")
cv.text_px(W_ / 2, 60, "所有方塊高度依實際體積等比繪製（1 m³ = 300 px）；土粒體積由各區自己的 G_s 換算",
           12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 128,
           "V_s = W_{{sA}}/(G_{{sA}} γ_w) + W_{{sB}}/(G_{{sB}} γ_w) = {:.5f} + {:.5f} = {:.5f} m³".format(VSA, VSB, VS),
           13.5, C["text"], weight="700")
cv.text_px(W_ / 2, H_ - 102,
           "V_w = W_w/γ_w = 2.4/9.81 = {:.5f} m³　⇒　V_s + V_w = {:.5f} m³ ＞ 1 m³"
           .format(VW_T, VS + VW_T), 13.5, C["load"], weight="700")
cv.text_px(W_ / 2, H_ - 74,
           "換算成飽和度 S = ωG_{{s,mix}}/e = {:.1f}%（G_{{s,mix}} = {:.4f}，e = {:.4f}）"
           .format(S_T * 100, GSMIX, E_T), 13, C["load"], weight="700")
cv.text_px(W_ / 2, H_ - 46,
           "攔錯用：三個小題的算術完全用不到 G_s，但沒有 G_s 就看不出目標狀態不可能達成。",
           13, C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 20,
           "考卷卷首寫著「倘若條件不足，請自行合理假設」——把這個矛盾指出來是加分而非扣分。",
           12.5, C["muted"])
cv.save(OUT + "/SM-2008-1-fig-1-recipe-overflow.svg")

# ══════ fig-2：γ_d–ω 圖上的三條 ZAV 線與目標點 ══════
W_, H_ = 1000, 760
ML, MR, MT_, MB = 150, 150, 88, 250
cv = Canvas(W_, H_, bg="#FFFFFF")
XL, XR = 0.06, 0.16
YL, YH = 17.0, 22.0
PX = lambda w: ML + (w - XL) / (XR - XL) * (W_ - ML - MR)
PY = lambda g: H_ - MB - (g - YL) / (YH - YL) * (H_ - MT_ - MB)
for x in [0.06, 0.08, 0.10, 0.12, 0.14, 0.16]:
    seg(cv, (PX(x), PY(YL)), (PX(x), PY(YH)), C["border"], 1.1)
    cv.text_px(PX(x), PY(YL) + 19, "%d" % round(x * 100), 12.5, C["muted"])
for y in [17, 18, 19, 20, 21, 22]:
    seg(cv, (PX(XL), PY(y)), (PX(XR), PY(y)), C["border"], 1.1)
    cv.text_px(PX(XL) - 12, PY(y), "%d" % y, 12.5, C["muted"], anchor="end")
seg(cv, (PX(XL), PY(YL)), (PX(XR), PY(YL)), C["muted"], 1.9)
seg(cv, (PX(XL), PY(YL)), (PX(XL), PY(YH)), C["muted"], 1.9)
cv.text_px((PX(XL) + PX(XR)) / 2, PY(YL) + 44, "含水量 ω（%）", 13.5, C["text"])
cv.text_px(PX(XL) - 84, (PY(YL) + PY(YH)) / 2, "乾單位重 γ_d（kN/m³）", 13.5, C["text"])

ws = [XL + i * (XR - XL) / 300 for i in range(301)]
LEG = []
for gs, col, dash, lab in [(GSB, C["muted"], "3 5", "ZAV（G_s = 2.70，乙）"),
                           (GSMIX, C["load"], None, "ZAV（G_s = {:.4f}，混合後的實際值）".format(GSMIX)),
                           (GSA, C["bmd"], "8 5", "ZAV（G_s = 2.65，甲）")]:
    pts = [(PX(w), PY(ZAV(gs, w))) for w in ws if YL <= ZAV(gs, w) <= YH]
    curve(cv, pts, col, 3.4 if gs == GSMIX else 2.2, dash)
    LEG.append((col, lab, dash))
lx, ly = PX(0.063), PY(19.55)
cv.rect_px(lx - 12, ly - 20, 356, 26 * len(LEG) + 12, "#FFFFFFEE", 8, "rgba(0,0,0,0.10)", 1)
for i, (col, lab, dash) in enumerate(LEG):
    yy = ly + i * 26
    seg(cv, (lx, yy), (lx + 34, yy), col, 3.0, dash)
    cv.text_px(lx + 44, yy, lab, 12.5, col, anchor="start", weight="700")

# 三個點
for w_, gd_, col, lab, ax_, dxp, dyp in [
        (WA, GDA, C["bmd"], "甲 γ_d = {:.2f}（S = 53.5%）".format(GDA), "start", 14, 26),
        (WB, GDB, C["accent"], "乙 γ_d = {:.2f}（S = 69.5%）".format(GDB), "start", 14, -26),
        (WC_, GDC, C["load"], "目標 γ_d = 20.00", "end", -16, -26)]:
    dot(cv, PX(w_), PY(gd_), 7.2, col)
    tag_px(cv, PX(w_) + dxp, PY(gd_) + dyp, lab, 12.8, col, anchor=ax_)
seg(cv, (PX(WC_), PY(ZAV(GSMIX, WC_))), (PX(WC_), PY(GDC)), C["load"], 2.6)
tag_px(cv, PX(WC_) + 16, (PY(ZAV(GSMIX, WC_)) + PY(GDC)) / 2,
       "落在混合 ZAV 線「上方」＝不可能區", 12.8, C["load"], anchor="start")
tag_px(cv, PX(WC_) - 16, PY(ZAV(GSMIX, WC_)) + 22,
       "混合 ZAV 上限 {:.2f}".format(ZAV(GSMIX, WC_)), 12.5, C["load"], anchor="end", weight="400")

cv.text_px(W_ / 2, 32, "圖 2　目標點落在零空氣孔隙線的上方——這個夯實狀態做不出來", 17.5,
           C["text"], weight="700")
cv.text_px(W_ / 2, 58, "三條線皆由 γ_d,ZAV = G_s γ_w /(1 + ωG_s) 算出，只有 G_s 不同", 12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 170,
           "ω = 12% 時：G_s = 2.65 → {:.2f}　｜　G_{{s,mix}} = {:.4f} → {:.2f}　｜　G_s = 2.70 → {:.2f}"
           .format(ZAV(GSA, WC_), GSMIX, ZAV(GSMIX, WC_), ZAV(GSB, WC_)), 13, C["text"], weight="700")
cv.text_px(W_ / 2, H_ - 144,
           "目標 20.00 幾乎正好落在 G_s = 2.70 那條線上——委員很可能是直接取乙的 G_s 來訂目標。",
           13, C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 116,
           "但實際混合後 G_{{s,mix}} = {:.4f}（依乾土重加權的土粒體積算出），目標就越線了。".format(GSMIX),
           13, C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 86,
           "要讓目標剛好可行：G_s 需 ≥ {:.4f}，或把 ω 降到 ≤ {:.2f}%，或把 γ_d 降到 {:.2f}。"
           .format(GS_NEEDED, W_MAX * 100, ZAV(GSMIX, WC_)), 13, C["text"], weight="700")
cv.text_px(W_ / 2, H_ - 58,
           "攔錯用：ZAV 線是每一道夯實題的最後一道防線——算完永遠回頭看一眼點在線的哪一側。",
           13, C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 30,
           "甲、乙兩點都安穩落在線下（S 53.5% 與 69.5%），問題只出在「混合後要求的目標狀態」。",
           12.5, C["muted"])
cv.save(OUT + "/SM-2008-1-fig-2-zav-check.svg")

print("gdA=%.4f gdB=%.4f VB=%.5f VA=%.5f WtA=%.3f WtB=%.3f dWw=%.4f" % (GDA, GDB, VB, VA_, WTA, WTB, DWW))
print("VsA=%.5f VsB=%.5f Vs=%.5f Gsmix=%.4f Vw=%.5f 超出=%.5f S=%.2f%%"
      % (VSA, VSB, VS, GSMIX, VW_T, OVER, S_T * 100))
print("ZAV: 2.65→%.3f  mix→%.3f  2.70→%.3f ; 需 Gs>=%.4f ; wmax=%.4f%%"
      % (ZAV(GSA, WC_), ZAV(GSMIX, WC_), ZAV(GSB, WC_), GS_NEEDED, W_MAX * 100))
print("借土總體積=%.5f m3 ; VaA=%.5f VaB=%.5f" % (VA_ + VB, VaA, VaB))
