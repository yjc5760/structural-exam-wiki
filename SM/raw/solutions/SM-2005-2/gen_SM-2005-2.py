# -*- coding: utf-8 -*-
"""SM-2005-2 圖解。所有數值取自 SM-2005-2.md §4（Step 1–4）。
用法：python gen_SM-2005-2.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 由 SM-2005-2 §4 解得（題目正本 #1：粗顆粒體積 = 乾重/(G·ρw)）──
VT = 315.0
COARSE = [("1/2″", 18.0, 0.023, 2.41), ("3/8″", 26.0, 0.041, 2.32), ("#4", 40.0, 0.072, 2.35)]
rows = [(n, w / (1 + m), w / (1 + m) / g) for n, w, m, g in COARSE]   # (篩, 乾重 g, 實體積 cm³)
VC = sum(r[2] for r in rows)        # 33.945
WSC = sum(r[1] for r in rows)       # 79.884
WSF = 650.0 / 1.112                 # 584.53
VF = VT - VC                        # 281.06
RD = WSF / VF                       # 2.0798
WRONG_V = WSF / VT                  # 1.856 只扣重量不扣體積
WRONG_ALL = (WSF + WSC) / VT        # 2.109 全試樣（非所求）

W_, H_ = 980, 800
cv = Canvas(W_, H_, bg="#FFFFFF")
BASE, SCALE, BW, CX = 600, 1.45, 230, 330
cols = ["rgba(180,83,9,0.40)", "rgba(180,83,9,0.28)", "rgba(180,83,9,0.18)"]
parts = [(VF, "rgba(46,125,111,0.20)", C["bmd"], "細料（土粒＋孔隙）{:.2f} cm³".format(VF))]
top = vbar(cv, CX, BASE, BW, parts, SCALE)
# 粗顆粒堆在上方，逐格以引線標註（格太薄放不下字）
y = top
LY = [top + 70, top + 22, top - 26]     # 標籤錯開的列位置（由下層到上層）
for (n, ws, vc), fc, ly in zip(rows, cols, LY):
    hp = vc * SCALE
    cv.rect_px(CX - BW / 2, y - hp, BW, hp, fc, 0, C["accent"], 1.6)
    ym = y - hp / 2
    seg(cv, (CX + BW / 2, ym), (CX + BW / 2 + 40, ly), C["accent"], 1.1, "3 3")
    tag_px(cv, CX + BW / 2 + 46, ly, "{} 粗粒實體積 {:.3f} cm³（乾 {:.3f} g ÷ {:.2f}）".format(
        n, vc, ws, dict((c[0], c[3]) for c in COARSE)[n]), 12, C["accent"], anchor="start", weight="400")
    y -= hp
# 總體積括號
xb = CX - BW / 2 - 26
seg(cv, (xb, BASE), (xb, y), C["dim"], 1.4)
for yy in (BASE, y):
    seg(cv, (xb - 6, yy), (xb + 6, yy), C["dim"], 1.4)
tag_px(cv, xb - 10, (BASE + y) / 2, "挖洞 V = 315 cm³", 12.5, C["muted"], anchor="end")
seg(cv, (CX - BW / 2 - 8, top), (CX + BW / 2 + 8, top), C["accent"], 1.6, "6 4")
tag_px(cv, CX, top - 4 - VC * SCALE - 18, "粗顆粒合計 {:.3f} cm³（乾 {:.2f} g）".format(VC, WSC),
       12.5, C["accent"])
cv.text_px(CX, BASE + 26, "細料乾重 650 ÷ 1.112 = {:.2f} g".format(WSF), 13, C["bmd"], weight="700")

# 右側：三種算法對照
X0 = 600
cv.text_px(X0 + 150, 300, "通過 #4 試樣乾密度", 14, C["text"], weight="700")
L = [("正解：細料乾重 ÷ 細料體積", "{:.2f} / {:.2f} = {:.3f} g/cm³".format(WSF, VF, RD), C["bmd"]),
     ("錯：只扣重量、不扣體積", "{:.2f} / 315 = {:.3f}".format(WSF, WRONG_V), C["load"]),
     ("錯：全試樣乾密度（非所求）", "{:.2f} / 315 = {:.3f}".format(WSF + WSC, WRONG_ALL), C["load"])]
for i, (a, b, c) in enumerate(L):
    yy = 340 + i * 58
    cv.text_px(X0 + 150, yy, a, 13, c, weight="700")
    cv.text_px(X0 + 150, yy + 22, b, 12.5, c)

cv.text_px(W_ / 2, 34, "圖 1　工地密度試驗的過大顆粒修正：從洞體積扣掉粗顆粒「實體積」", 17.5, C["text"], weight="700")
cv.text_px(W_ / 2, 60, "高度依實際體積等比繪製（1 cm³ = 1.45 px）；粗顆粒視為無孔隙實體，體積 = 乾重 ÷ (G·ρ_w)",
           12.5, C["muted"])
cv.text_px(W_ / 2, H_ - 96,
           "攔錯用：所求是「通過 #4 試樣」的乾密度，分子分母都只能留細料——", 13, C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 72,
           "扣了粗粒重量卻沒扣它佔的 33.9 cm³，會低估 11%（1.856）；整包一起算則是另一個量（2.109）。", 13,
           C["accent"], weight="700")
cv.text_px(W_ / 2, H_ - 40,
           "驗算：粗粒體積 7.301 + 10.766 + 15.878 = {:.3f} cm³；315 − {:.3f} = {:.3f} cm³ ✓".format(VC, VC, VF),
           12.5, C["muted"])
cv.save(os.path.join(OUT, "SM-2005-2-fig-1-oversize-correction.svg"))
print("VC", VC, "WSC", WSC, "WSF", WSF, "VF", VF, "RD", RD, WRONG_V, WRONG_ALL)
