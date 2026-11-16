#!/usr/bin/env python3
"""SD-2014-3 圖解產生器 — 動力分析總橫力的調整（現行規範 3.3 節）

調整規則（解析 §4 題(一)）：規則性建築物調整至 0.9Vs、不規則性建築物調整至 1.0Vs，
動力分析值已超過目標時採用動力分析值（只調高不調低）。長條長度全部由 adjust() 算出。
用法：python3 gen_SD-2014-3.py   （輸出 figs/SD-2014-3-fig-1-base-shear-scaling.svg；PNG 由 render.py 產生）
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.environ.get("STRUCTDRAW", os.path.join(HERE, "..", "..", "..", "..", "skills", "struct-diagram", "scripts"))
sys.path.insert(0, SKILL)
from structdraw import Canvas, C

OUT = os.path.join(HERE, "figs")
# ── 由 §4 題(一)「規範調整原則」──
RATIO = {"規則性建築物": 0.9, "不規則性建築物": 1.0}
def adjust(Vd, Vs, kind):
    return max(Vd, RATIO[kind] * Vs)
VS = 1.0
CASES = [("規則性建築物", 0.70), ("不規則性建築物", 0.70), ("規則性建築物", 1.20), ("不規則性建築物", 1.20)]

def main():
    W, H = 900, 420
    L, R, T, B = 190, 250, 80, 66
    xmax = 1.35
    pw = W - L - R
    X = lambda v: L + v / xmax * pw
    cv = Canvas(W, H, sx=1.0, ox=0, oy=0)
    cv.text_px(W / 2, 30, "動力分析總橫力 V_{d} 依靜力最小設計水平總橫力 V_{s} 調整", 18, C["text"], weight="700")
    cv.text_px(W / 2, 56, "規則性建築物調至 0.9V_{s}、不規則性建築物調至 1.0V_{s}；已超過者採用動力分析值", 13, C["muted"])
    top = H - T - 6
    rowh = 72
    # 參考線
    for v, lab in [(0.9, "0.9V_{s}"), (1.0, "1.0V_{s}")]:
        cv.line((X(v), B - 6), (X(v), top + 8), C["accent"] if v == 0.9 else C["load"], w=1.4, dash="5 4")
        cv.text((X(v) + (-5 if v == 0.9 else 5), B - 22), lab, 13, C["accent"] if v == 0.9 else C["load"],
                anchor="end" if v == 0.9 else "start")
    cv.line((L, B), (L, top + 8), C["member"], w=1.6)
    for v in [0, 0.25, 0.5, 0.75, 1.0, 1.25]:
        cv.text((X(v), B - 44), f"{v:.2f}", 11.5, C["muted"])
    cv.text((X(1.25) + 40, B - 44), "總橫力 / V_{s}", 13, C["text"], anchor="start")
    for i, (kind, vd) in enumerate(CASES):
        yc = top - 20 - i * rowh
        va = adjust(vd, VS, kind)
        cv.text((L - 12, yc + 10), kind, 13.5, C["text"], anchor="end", weight="700")
        cv.text((L - 12, yc - 10), f"V_{{d}} = {vd:.2f}V_{{s}}", 12.5, C["muted"], anchor="end")
        cv.polygon([(L, yc + 18), (X(vd), yc + 18), (X(vd), yc + 4), (L, yc + 4)], C["ghost"])
        col = C["accent"] if RATIO[kind] < 1 else C["load"]
        cv.polygon([(L, yc - 4), (X(va), yc - 4), (X(va), yc - 18), (L, yc - 18)], col)
        if va > vd + 1e-9:
            cv.text((X(va) + 12, yc - 11), f"調整後 {va:.2f}V_{{s}}（放大 ×{va/vd:.3f}）", 12.5, col, anchor="start")
        else:
            cv.text((X(va) + 8, yc - 11), f"採用動力分析值 {va:.2f}V_{{s}}（不縮小）", 12.5, C["bmd"], anchor="start")
        cv.text((X(vd) + 8, yc + 11), "動力分析值", 11.5, C["muted"], anchor="start")
    os.makedirs(OUT, exist_ok=True)
    cv.save(os.path.join(OUT, "SD-2014-3-fig-1-base-shear-scaling.svg"))

if __name__ == "__main__":
    main()
