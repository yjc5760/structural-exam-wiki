# -*- coding: utf-8 -*-
"""SM-2020-4 圖解。
fig-1-fs-methods：解題圖解（2026-11-15 階段 E）——五種承載力式的 FS 對 FS = 3 的位置。
數值全部由本檔依 SM-2020-4.md §4、§5（含 2026-11-15 盲解比對補註）重算。
用法：python gen_SM-2020-4.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *                                      # Canvas, C, compose, esc
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── §4 L1／L2 ──────────────────────────────────────
QU, B, DF, G, GC, QW = 100.0, 1.25, 0.5, 18.8, 24.0, 120.0
CU = QU / 2                                    # 50 kPa
Q_NET = QW / B + (GC - G) * DF                 # 98.6 kPa（§4 Step 4）
FS_REQ = 3.0
METHODS = [("Terzaghi  N_c = 5.7（本解主線）", 5.7),
           ("Meyerhof  5.14 × d_c 1.08", 5.14 * (1 + 0.2 * DF / B)),
           ("Skempton  5(1 + 0.2D_f/B) = 5.4", 5 * (1 + 0.2 * DF / B)),
           ("N_c = 5.14，不計深度因數", 5.14),
           ("Hansen/Vesic  5.14 × d_c 1.16", 5.14 * (1 + 0.4 * DF / B))]
ROWS = [(n, CU * nc / Q_NET) for n, nc in METHODS]


def fig_fs():
    W, H = 900, 470
    cv = Canvas(W, H, sx=1, bg="#FFFFFF")
    cv.panel(title="淨極限承載力 ÷ 淨施加壓力 %.1f kPa" % Q_NET,
             sub="FS 落在 3 附近：公式一換，結論就可能翻轉")
    x0, x1, f0, f1 = 330, 840, 2.4, 3.2
    FX = lambda f: x0 + (x1 - x0) * (f - f0) / (f1 - f0)
    for k, (n, fs) in enumerate(ROWS):
        y = 130 + k * 52
        col = C["member"] if fs >= FS_REQ else C["load"]
        cv.text_px(x0 - 14, y, n, 12.5, C["text"], anchor="end")
        cv.line((x0, H - y), (x1, H - y), C["border"], 1.2)
        cv.dot((FX(fs), H - y), 7, col)
        cv.text_px(FX(fs) + 12, y, "%.2f" % fs, 14, col, anchor="start", weight="700")
    yb = 130 + len(ROWS) * 52 - 20
    for f in (2.4, 2.6, 2.8, 3.0, 3.2):
        cv.text_px(FX(f), yb + 18, "%.1f" % f, 11.5, C["muted"])
    cv.line((FX(FS_REQ), H - 104), (FX(FS_REQ), H - yb), C["load"], 2, dash="7 5")
    cv.text_px(FX(FS_REQ), 104, "FS 要求 = 3（現行規範常時）", 12.5, C["load"], weight="700")
    cv.text_px(W / 2, H - 28, "五法中四法低於 3 → 本解判「不安全」；採 Hansen 深度因數時 FS ≈ 3.0，應寫成「臨界、無餘裕」", 12.5, C["text"], weight="700")
    return cv

compose([fig_fs()],
        title="SM-2020-4 條形基礎短期承載：五種承載力式的 FS",
        note="攔錯用：只用一條公式就下「安全／不安全」結論；FS 在要求值附近時要寫明所採公式與假設（cu = qu/2、基礎超重 (γc − γ)Df）。",
        path=os.path.join(OUT, "SM-2020-4-fig-1-fs-methods.svg"))
if __name__ == "__main__":
    for n, fs in ROWS: print("%-34s FS=%.3f" % (n, fs))
