# -*- coding: utf-8 -*-
"""SM-2018-3 圖解。
本題附圖是流網（題目資料），不重繪。
fig-2-uplift：解題圖解（2026-11-15 階段 E，勘誤後），壩底 a–e 上揚壓力分解（靜水部分＋滲流水頭部分），數值取自解析 §4。
用法：python gen_SM-2018-3.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 由 SM-2018-3 §4 解得（題目正本 #1–#4）──
GW = 9.81
DH, ND, NF = 6.3, 10, 3          # 上下游水位差、等勢降數、流槽數
EMB = 1.6                        # 壩底在下游水面（地表）下
DHN = DH / ND                    # 0.63
NS = [("a", 4.5), ("b", 5), ("c", 6), ("d", 7), ("e", 8)]
XS = {"a": 0.0, "b": 1.0, "c": 2.0, "d": 3.0, "e": 4.0}   # 點位等距示意（考卷水平未依比例）

def fig_uplift():
    W, H = 960, 600
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-1.6, 6.6), (-7.2, 1.6), 40, 40, 30, 30))
    sc = 0.1                                            # 1 kPa → 0.1 單位（向下畫）
    cv.polygon([(-0.4, 0), (4.4, 0), (4.4, 1.2), (-0.4, 1.2)], "rgba(138,148,166,0.45)")
    cv.text((2.0, 0.6), "壩底（下游水面下 1.6 m）", 13, C["text"], weight="700")
    cv.line((-0.4, 0), (-0.4, -1.6), C["text"], 5, cap="butt")
    cv.text((-0.55, -1.0), "截水牆", 12, C["muted"], anchor="end")
    u_s = GW * EMB
    for lab, n in NS:
        x = XS[lab]; h = DH - n * DHN; u = GW * (h + EMB)
        bw = 0.42
        cv.polygon([(x - bw/2, 0), (x + bw/2, 0), (x + bw/2, -u_s * sc), (x - bw/2, -u_s * sc)], "rgba(138,148,166,0.55)")
        cv.polygon([(x - bw/2, -u_s * sc), (x + bw/2, -u_s * sc), (x + bw/2, -u * sc), (x - bw/2, -u * sc)], "rgba(29,78,216,0.55)")
        cv.dot((x, 0), 5, fill=C["text"]); cv.text((x, 0.25), lab, 13.5, C["text"], weight="700")
        cv.text((x, -u * sc - 0.35), "%.1f" % u, 12.5, C["deform"], weight="700")
        cv.text((x, -u * sc - 0.75), "n = %g" % n, 11, C["muted"])
    cv.line((-0.4, -u_s * sc), (4.4, -u_s * sc), C["member2"], 1.0, dash="4 3")
    cv.text((4.55, -u_s * sc / 2), "靜水部分 1.6γw = %.1f kPa" % u_s, 12, C["muted"], anchor="start")
    cv.text((4.55, -3.4), "滲流水頭部分 (6.3 − 0.63n)γw", 12, C["deform"], anchor="start", weight="700")
    cv.text((4.55, -4.0), "相鄰點差 0.63γw = %.2f kPa" % (DHN * GW), 12, C["text"], anchor="start")
    cv.math_px(cv.X(4.55), cv.Y(-4.6), "q = k ΔH N_{f}/N_{d} = 6.62×10^{-6} m^{3}/s/m", 12.5, C["text"], anchor="start")
    cv.text((-1.5, -6.8), "u（kPa，向下畫）＝ (h + 1.6)γw；a 在牆與壩底交角，取 4.5 降", 12, C["muted"], anchor="start")
    return cv

compose([fig_uplift()],
        title="圖 2　壩底上揚壓力：ΔH = 6.3 m、Nd = 10，每點都含 1.6γw 的靜水部分",
        sub="以下游水面為基準，h = 6.3 − 0.63n；壩底低於下游水面 1.6 m，壓力水頭 = h + 1.6",
        note="攔錯用：e 點上揚壓力不是 0（之後還有 2 降、且壩底在水面下）；1.6 m 是埋深，不加進 ΔH。",
        path=os.path.join(OUT, "SM-2018-3-fig-2-uplift.svg"))
