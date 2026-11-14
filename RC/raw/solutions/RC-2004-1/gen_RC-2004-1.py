#!/usr/bin/env python3
"""
RC-2004-1 耐震梁受撓鋼筋搭接 — 解題圖解

用法：python3 gen_RC-2004-1.py [輸出目錄]（預設 figs/）
依據：RC-2004-1.md §4 乙（建築物混凝土結構設計規範 112 年版 §18.3.3.3）。本題無附圖、無數值，
圖中尺度以梁深 h 為單位（示意）；禁區長度 2h 與箍筋間距上限 min(d/4, 10 cm) 取自規範條文。
FIGURES
  fig-1-beam-lap  梁立面搭接禁區  攔：把柱的「中段 1/2」套到梁、漏掉預期降伏斷面的 2h 禁區
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2004-1"

# ── 規範 §18.3.3.3（以梁深 h 為單位的示意尺度）──
H = 1.0              # 梁深
LN = 16.0            # 梁淨跨（示意：16h）
BC = 1.4             # 柱寬（示意）
NO_SPLICE = 2 * H    # 距接頭面 2h 不得搭接
X_YIELD = 10.0       # 示意：跨內另有一處預期撓曲降伏斷面（例如梁中有集中載重）
LAP = 2.4            # 示意搭接長度


def fig1_beam_lap():
    W, Hc = 1000, 470
    s = 50.0
    cv = Canvas(W, Hc, sx=s, ox=(W - (LN + 2 * BC) * s) / 2 + BC * s, oy=150)
    cv.panel("特殊抗彎矩構架梁：受撓鋼筋搭接位置（立面）", "規範 §18.3.3.3；尺度以梁深 h 計（示意）")
    for x0 in (-BC, LN):
        cv.polygon([(x0, -1.3), (x0 + BC, -1.3), (x0 + BC, H + 1.3), (x0, H + 1.3)], "#DCE3EC", C["member"], 2.2)
        cv.polygon([(x0, 0), (x0 + BC, 0), (x0 + BC, H), (x0, H)], C["fill_t"], C["tension"], 1.6)
    cv.polygon([(0, 0), (LN, 0), (LN, H), (0, H)], "#EDF1F6", C["member"], 2.2)
    bad = [(0, NO_SPLICE), (LN - NO_SPLICE, LN), (X_YIELD - NO_SPLICE, X_YIELD + NO_SPLICE)]
    for a, b in bad:
        cv.polygon([(a, 0), (b, 0), (b, H), (a, H)], C["fill_t"], C["tension"], 1.4)
    cv.line((X_YIELD, -0.25), (X_YIELD, H + 0.25), C["tension"], 1.8, dash="5 4")
    # 允許搭接的兩段之一，畫出搭接筋與密箍
    xa = NO_SPLICE + 0.5 * ((X_YIELD - NO_SPLICE) - NO_SPLICE - LAP)
    xb = xa + LAP
    cv.polygon([(xa, 0), (xb, 0), (xb, H), (xa, H)], C["fill_m"], C["bmd"], 1.8)
    cv.line((-BC + 0.2, 0.15), (xb, 0.15), C["member"], 2.6)
    cv.line((xa, 0.27), (LN + BC - 0.2, 0.27), C["member"], 2.6)
    n = 9
    for i in range(n):
        x = xa + LAP * i / (n - 1)
        cv.line((x, 0.06), (x, H - 0.06), C["deform"], 1.4)
    cv.text(((xa + xb) / 2, H + 0.32), "搭接段：全長閉合箍筋 s ≤ min(d/4, 10 cm)", 13, C["bmd"], weight="700")
    cv.text((NO_SPLICE / 2, -0.45), "2h 禁區", 13, C["tension"], weight="700")
    cv.text((LN - NO_SPLICE / 2, -0.45), "2h 禁區", 13, C["tension"], weight="700")
    cv.text((X_YIELD, -0.45), "預期降伏斷面兩側各 2h", 13, C["tension"], weight="700")
    cv.text((-BC / 2, H + 1.6), "接頭內", 13, C["tension"], weight="700")
    cv.text((LN + BC / 2, H + 1.6), "接頭內", 13, C["tension"], weight="700")
    cv.dim((0, H + 1.0), (NO_SPLICE, H + 1.0), "2h", off=0, label_off=-12, size=13)
    # 錯誤觀念：中段 1/2（柱的規定）
    cv.line((LN / 4, -1.0), (3 * LN / 4, -1.0), C["muted"], 1.6, dash="6 5")
    cv.text((LN / 2, -1.3), "「跨中 l_n/2 才能搭接」是柱的規定，不適用於梁", 13, C["muted"])
    cv.text_px(W / 2, Hc - 34, "紅色：不得搭接（接頭內、距接頭面 2h、預期降伏斷面兩側 2h）　綠色：可搭接，但須全長密箍", 13, C["text"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-beam-lap.svg")
    compose([cv], title=f"{TAG} 圖 1　耐震梁受撓鋼筋搭接：三個禁區＋搭接段密箍",
            sub="搭接位置限制是「禁區」，不是「中央一半」；搭接比例只影響甲／乙級，沒有「每次只搭接一半」的規定",
            note="尺度為示意（以梁深 h 為單位）；跨內降伏斷面位置依結構分析而定",
            path=path)
    return path


FIGURES = [(fig1_beam_lap, "§4 乙", "把柱的「中段 1/2」套到梁、漏掉預期降伏斷面的 2h 禁區")]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, where, catches in FIGURES:
        print(os.path.basename(fn()), "→", where, "攔：", catches)
