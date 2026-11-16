#!/usr/bin/env python3
"""SD-2006-3 圖解產生器 — 現行規範設計譜形（表 2-5(a)）與因素加大後的變化（示意值）。
圖上數字全由頂端的 SDS、SD1 與加大倍數算出；數值與 §4 示意數值表一致（由 scripts/fixes/2026-11-16_verify_SD-2006-3.py 驗算）。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.join(HERE, "../../../../skills/struct-diagram/scripts")))
from structdraw import Canvas, C
OUT = os.path.join(HERE, "figs")

# ── 由 §4「示意數值」：SDS = 0.60、SD1 = 0.35；各係數加大 20% ──
SDS, SD1, UP = 0.60, 0.35, 1.2

def SaD(T, sds, sd1):
    T0 = sd1 / sds
    if T <= 0.2 * T0: return sds * (0.4 + 3 * T / T0)
    if T <= T0: return sds
    if T <= 2.5 * T0: return sd1 / T
    return 0.4 * sds

def fig1():
    W, H = 960, 580
    XR, YR = 3.2, 0.90
    L, R_, T_, B = 92, 250, 96, 96
    sx = (H - T_ - B) / YR
    XSC = (W - L - R_) / (sx * XR)
    cv = Canvas(W, H, sx=sx, ox=L, oy=B)
    XM = lambda x: x * XSC
    cv.text_px(W / 2, 32, "圖 1　現行規範設計譜形 SaD(T) 與因素加大後的變化（示意值）", 17, C["text"], weight="700")
    cv.text_px(W / 2, 56, f"基準 SDS = {SDS:.2f}、SD1 = {SD1:.2f}（T0D = {SD1/SDS:.3f} s）；各加大 {UP-1:.0%}", 13, C["muted"])
    cv.axes((0, 0), XM(XR) * 0.99, YR * 0.99, ("T (s)", "SaD"), C["muted"], 1.8)
    for yv in (0.2, 0.4, 0.6, 0.8):
        cv.line((-0.03 * XSC, yv), (0.03 * XSC, yv), C["muted"], 1.2)
        cv.text_px(cv.X(0) - 10, cv.Y(yv), f"{yv:.1f}", 11.5, C["muted"], "end")
    for xv in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
        cv.line((XM(xv), -0.008), (XM(xv), 0.008), C["muted"], 1.2)
        cv.text_px(cv.X(XM(xv)), cv.Y(0) + 18, f"{xv:.1f}", 11.5, C["muted"])
    ts = [i * XR / 640 for i in range(641)]
    cases = [(SDS * UP, SD1, C["load"], f"S_S^D 加大（SDS = {SDS*UP:.2f}）", "9 6"),
             (SDS, SD1 * UP, C["bmd"], f"S_1^D 加大（SD1 = {SD1*UP:.2f}）", "3 5"),
             (SDS, SD1, C["deform"], "基準", None)]
    for sds, sd1, col, lab, dash in cases:
        cv.poly([(XM(t), SaD(t, sds, sd1)) for t in ts], col, 4.0 if dash is None else 2.8, dash=dash)
    # 基準譜分段點
    T0 = SD1 / SDS
    for xb, lab in ((0.2 * T0, "0.2T0D"), (T0, "T0D"), (2.5 * T0, "2.5T0D")):
        cv.line((XM(xb), 0), (XM(xb), SaD(xb, SDS, SD1)), C["border"], 1.6, dash="6 5")
        cv.dot((XM(xb), SaD(xb, SDS, SD1)), 5.0, C["deform"])
        cv.text_px(cv.X(XM(xb)), cv.Y(0) + 38, lab, 12, C["deform"], weight="700")
    cv.line((XM(2.5 * T0), 0.4 * SDS), (XM(XR) * 0.99, 0.4 * SDS), C["deform"], 1.0, dash="2 4")
    cv.text_px(cv.X(XM(XR) * 0.99) + 8, cv.Y(0.4 * SDS) + 14, f"0.4SDS = {0.4*SDS:.2f}", 12.5, C["deform"], "start", weight="700")
    cv.text_px(cv.X(XM(XR) * 0.99) + 8, cv.Y(0.4 * SDS * UP) - 4, f"{0.4*SDS*UP:.3f}", 12.5, C["load"], "start", weight="700")
    cv.text_px(cv.X(XM(1.15)), cv.Y(0.71), "平台 SDS", 12.5, C["deform"], weight="700")
    cv.text_px(cv.X(XM(1.55)), cv.Y(0.52), "SD1/T 段", 12.5, C["muted"])
    # 極短週期反降之處（T = 0.05 s）
    t5 = 0.05
    cv.dot((XM(t5), SaD(t5, SDS, SD1 * UP)), 4.5, C["bmd"])
    cv.text_px(cv.X(XM(t5)) + 10, cv.Y(0.13), f"T = 0.05 s：{SaD(t5,SDS,SD1):.3f} → {SaD(t5,SDS,SD1*UP):.3f}", 12, C["bmd"], "start", weight="700")
    cv.text_px(cv.X(XM(t5)) + 10, cv.Y(0.08), "（S_1^D 加大使 T0D 變長，上升段變緩）", 11.5, C["bmd"], "start")
    cv.legend(W - R_ + 26, cv.Y(0.74), [(col, lab) for _, _, col, lab, _ in cases[::-1]])
    cv.text_px(W / 2, H - 22, "攔錯：台灣規範沒有 T_L 長週期段，T > 2.5T0D 取 0.4SDS；係數加大不保證各週期都提高", 13, C["muted"])
    cv.save(f"{OUT}/SD-2006-3-fig-1-spectrum.svg")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1()
    print("T0D =", round(SD1/SDS, 4), [round(SaD(t, SDS, SD1), 4) for t in (0.05, 0.3, 0.8, 1.5, 3.0)])
