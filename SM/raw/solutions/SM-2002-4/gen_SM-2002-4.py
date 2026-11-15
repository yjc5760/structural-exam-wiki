# -*- coding: utf-8 -*-
"""SM-2002-4 圖解。數值由本檔依 SM-2002-4.md §3.5 L1 與 §4 重算；NC 包絡線為示意（題目未給）。
用法：STRUCTDRAW=<struct-diagram/scripts> python gen_SM-2002-4.py"""
# -*- coding: utf-8 -*-
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
D, Rad = math.degrees, math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
# ── L1 ──
GSAT, GW, Z = 19.8, 9.81, 20.0
SC = (49.0, 73.5, 147.0)              # 試驗壓密壓力
CP, PHIP = 15.0, 25.0                 # 試驗擬合結果
# ── §4 ──
SV0 = (GSAT-GW)*Z                     # 199.8
OCR = [SV0/s for s in SC]             # 4.08、2.72、1.36
REDO = (SV0, SV0+100, SV0+200)        # §4 Step 4 建議約 200／300／400（示例）

W, H = 1000, 600
xr, yr = (-15, 470), (-75, 230)
L, R, T, B = 60, 40, 80, 40
sx = min((W-L-R)/(xr[1]-xr[0]), (H-T-B)/(yr[1]-yr[0]))
cv = Canvas(W, H, sx=sx, ox=L-xr[0]*sx, oy=B-yr[0]*sx, bg="#FFFFFF")
cv.panel(title="試驗壓密壓力全落在現地 σ'_{v0} 左側（過壓密段）",
         sub="c' = 15 是把 OC 段數據擬合成直線的截距，不是 NC 黏土的性質")
cv.polygon([(0, 0), (SV0, 0), (SV0, yr[1]-10), (0, yr[1]-10)], "rgba(192,57,43,0.07)")
cv.polygon([(SV0, 0), (xr[1]-5, 0), (xr[1]-5, yr[1]-10), (SV0, yr[1]-10)], "rgba(46,125,111,0.08)")
cv.line((xr[0], 0), (xr[1], 0), C["muted"], 1.6); cv.line((0, 0), (0, yr[1]), C["muted"], 1.6)
cv.text_px(cv.X(xr[1])-4, cv.Y(0)-12, "σ' (kPa)", 12.5, C["muted"], anchor="end")
cv.text_px(cv.X(0)+8, cv.Y(yr[1])+4, "τ (kPa)", 12.5, C["muted"], anchor="start")
t = math.tan(Rad(PHIP))
cv.line((0, CP), (SC[-1], CP+SC[-1]*t), C["load"], 3.0)
cv.line((SC[-1], CP+SC[-1]*t), (440, CP+440*t), C["load"], 2.2, dash="7 5")
cv.text_px(cv.X(70), cv.Y(CP+70*t)-36, "試驗擬合 c' = 15、φ' = 25°", 13, C["load"], weight="700")
cv.text_px(cv.X(212), cv.Y(CP+300*t)-30, "外插到設計應力範圍（無試驗依據）", 12, C["load"], anchor="start")
cv.line((0, 0), (440, 440*t), C["member2"], 2.0, dash="3 4")
cv.text_px(cv.X(440), cv.Y(440*t)+44, "NC 段包絡線應過原點（c' ≈ 0，示意）", 12, C["member2"], anchor="end")
cv.text_px(cv.X(CP*0+4), cv.Y(CP)+2, "c' = 15", 12, C["load"], anchor="start", weight="700")
cv.line((SV0, -60), (SV0, yr[1]-10), C["deform"], 2.4)
cv.text_px(cv.X(SV0)+6, cv.Y(yr[1]-24), "現地 σ'_{v0} = %.1f" % SV0, 13, C["deform"], anchor="start", weight="700")
for i, (s, o) in enumerate(zip(SC, OCR)):
    cv.dot((s, 0), 5.5, fill=C["load"])
    cv.text_px(cv.X(s), cv.Y(0)+20+18*(i % 2), "%g" % s, 12.5, C["load"], weight="700")
    cv.text_px(cv.X(s), cv.Y(0)+56+18*(i % 2), "OCR %.2f" % o, 11.5, C["muted"])
for s in REDO:
    cv.dot((s, 0), 5.5, fill=C["bmd"])
cv.text_px(cv.X(REDO[1]), cv.Y(0)+22, "重做：≥ σ'_{v0}（約 200／300／400）", 12.5, C["bmd"], weight="700")
cv.text_px(cv.X(SV0/2), cv.Y(yr[1]-24), "OC 段（試驗範圍）", 12.5, C["load"])
cv.save(os.path.join(OUT, "SM-2002-4-fig-1-pressure-vs-sv0.svg"))
print("sv0=%.2f ocr=%s" % (SV0, ["%.2f" % o for o in OCR]))
