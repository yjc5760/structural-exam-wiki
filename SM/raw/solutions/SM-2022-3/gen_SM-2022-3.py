# -*- coding: utf-8 -*-
"""SM-2022-3 圖解。
fig-1-problem：題目附圖重繪（立體圖改畫成正視剖面），幾何只取自題目正本 SM-2022-3-problem.md §4 判讀清單（#2–#7），不含任何解題結果。
fig-2-head：解題圖解（2026-11-15 階段 E），總水頭沿土柱分布，數值取自解析 §4。
用法：python gen_SM-2022-3.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *                                      # Canvas, C, compose, fit, wt_symbol
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單（mm）──────────────────────────
HA, HB, HC = 50.0, 100.0, 50.0       # #5
H_DIFF = 600.0                       # #6 上、下水位面差
Y_D = 0.0; Y_C = HC; Y_B = HC + HB; Y_A = HC + HB + HA     # #4 點位
Y_LOW = 0.5 * HC                     # #2 下水位面在 c、d 之間（考卷未標高差，示意取中間）
Y_UP = Y_LOW + H_DIFF                # #6
BW = 50.0                            # #8 斷面寬（正視）
KS = {"A": "10^{-2}", "B": "10^{-1}", "C": "10^{-3}"}

def fig_problem():
    W, H = 760, 980
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-165, 330), (-110, Y_UP + 40), 20, 20, 20, 20))
    # 土柱
    cv.polygon([(0, Y_A), (BW, Y_A), (BW, Y_UP + 15), (0, Y_UP + 15)], "rgba(29,78,216,0.12)")
    for y0, y1, col, lab in ((Y_B, Y_A, "rgba(180,83,9,0.12)", "A"), (Y_C, Y_B, "rgba(180,83,9,0.26)", "B"),
                             (Y_D, Y_C, "rgba(63,74,90,0.30)", "C")):
        cv.polygon([(0, y0), (BW, y0), (BW, y1), (0, y1)], col, C["member"], 1.4)
        cv.text((BW / 2, (y0 + y1) / 2), "土壤 " + lab, 12.5, C["text"], weight="700")
    cv.line((0, Y_D - 15), (0, Y_UP + 15), C["member"], 2.4)
    cv.line((BW, Y_D - 15), (BW, Y_UP + 15), C["member"], 2.4)
    cv.text((BW / 2, (Y_A + Y_UP) / 2), "水", 14, C["deform"], weight="700")
    cv.line((0, Y_UP), (BW, Y_UP), C["deform"], 2.0)
    wt_symbol(cv, BW / 2, Y_UP + 3.0 * 2.4, C["deform"], 3.0)
    cv.text((-8, Y_UP + 6), "上水位面", 13, C["text"], anchor="end", weight="700")
    # 點位
    for y, lab in ((Y_A, "a"), (Y_B, "b"), (Y_C, "c"), (Y_D, "d")):
        cv.dot((BW, y), 5, fill=C["text"])
        cv.text((BW + 9, y + 7), lab, 14, C["text"], anchor="start", weight="700")
    # 連通管與下水位面水槽
    cv.poly([(15, Y_D), (15, -60), (215, -60), (215, Y_LOW - 20)], C["member2"], 6)
    cv.polygon([(185, Y_LOW - 20), (245, Y_LOW - 20), (245, Y_LOW + 22), (185, Y_LOW + 22)], "none", C["member"], 1.8)
    cv.polygon([(185, Y_LOW - 20), (245, Y_LOW - 20), (245, Y_LOW), (185, Y_LOW)], "rgba(29,78,216,0.18)")
    cv.line((185, Y_LOW), (245, Y_LOW), C["deform"], 2.0)
    wt_symbol(cv, 215, Y_LOW + 3.0 * 2.4, C["deform"], 3.0)
    cv.text((252, Y_LOW + 2), "下水位面", 13, C["text"], anchor="start", weight="700")
    cv.text((252, Y_LOW - 22), "（與 d 的高差考卷未標，示意）", 11, C["muted"], anchor="start")
    cv.line((BW + 2, Y_LOW), (183, Y_LOW), C["dim"], 0.9, dash="3 3")
    # 尺寸線
    xl = -22
    for y0, y1, lab, k in ((Y_B, Y_A, "H_{A} = 50 mm", "A"), (Y_C, Y_B, "H_{B} = 100 mm", "B"), (Y_D, Y_C, "H_{C} = 50 mm", "C")):
        cv.dim((xl, y0), (xl, y1), "", 0, C["dim"], 12)
        cv.math((xl - 14, (y0 + y1) / 2 + 9), lab, 12.5, C["text"], anchor="end")
        cv.math((xl - 14, (y0 + y1) / 2 - 10), "k_{%s} = %s cm/sec" % (k, KS[k]), 12, C["text"], anchor="end")
    xr = 120
    cv.dim((xr, Y_LOW), (xr, Y_UP), "h = 600 mm", 0, C["dim"], 13, label_off=48)
    cv.line((BW + 2, Y_UP), (xr + 6, Y_UP), C["dim"], 0.9, dash="3 3")
    cv.text((90, -88), "斷面 50 mm × 50 mm", 12.5, C["muted"])
    return cv

compose([fig_problem()],
        title="SM-2022-3 題目附圖重繪",
        sub="依題目正本判讀清單；以正視剖面表示原立體圖",
        note="攔錯用：下水位面在土壤 C 範圍內、不與 d 切齊；h = 600 mm 是上、下水位面之差。",
        path=os.path.join(OUT, "SM-2022-3-fig-1-problem.svg"))


# ══════ fig-2：總水頭沿土柱分布（解題圖解，2026-11-15 階段 E）══════
# ── 由 SM-2022-3 §4 Step 1–3 解得（總水頭以下水位面為 0）──
K = {"A": 1e-2, "B": 1e-1, "C": 1e-3}                 # cm/s
LAY = [("A", HA), ("B", HB), ("C", HC)]               # 水流 a→d 依序經過
RS = {k: h / K[k] for k, h in LAY}; RT = sum(RS.values())
DHL = {k: H_DIFF * RS[k] / RT for k in RS}            # 53.57、10.71、535.71 mm

def fig_head():
    W, H = 900, 560
    XF = 3.0                                          # 橫軸放大（mm → 圖面），縱軸 1:1
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-40 * XF / 3, 200 * XF + 280), (-90, 680), 80, 30, 30, 40))
    X = lambda x: x * XF
    xs = [0.0]; hs = [H_DIFF]
    for k, h in LAY:
        xs.append(xs[-1] + h); hs.append(hs[-1] - DHL[k])
    cols = {"A": "rgba(180,83,9,0.12)", "B": "rgba(180,83,9,0.24)", "C": "rgba(63,74,90,0.22)"}
    x0 = 0.0
    for k, h in LAY:
        cv.polygon([(X(x0), 0), (X(x0 + h), 0), (X(x0 + h), 640), (X(x0), 640)], cols[k])
        cv.text((X(x0 + h / 2), 655), "土壤 %s" % k, 12.5, C["text"], weight="700")
        x0 += h
    for v in range(0, 700, 100):
        cv.line((0, v), (X(200), v), C["border"], 1.0)
        cv.text_px(cv.X(0) - 8, cv.Y(v), "%d" % v, 12, C["muted"], anchor="end")
    for v in range(0, 250, 50):
        cv.text_px(cv.X(X(v)), cv.Y(0) + 36, "%d" % v, 11.5, C["muted"])
    cv.line((0, 0), (X(205), 0), C["muted"], 1.8); cv.line((0, 0), (0, 640), C["muted"], 1.8)
    cv.text_px(cv.X(0) - 44, cv.Y(320), "h（mm）", 13, C["text"], anchor="end")
    cv.text_px(cv.X(X(100)), cv.Y(0) + 60, "沿水流方向距 a 點（mm）", 12.5, C["text"])
    cv.poly([(X(x), h) for x, h in zip(xs, hs)], C["deform"], 3.0)
    for x, h, lab, dy in zip(xs, hs, "abcd", (-14, -16, 18, -14)):
        cv.dot((X(x), h), 5.5, fill=C["deform"])
        cv.text_px(cv.X(X(x)), cv.Y(0) + 16, lab, 13.5, C["text"], weight="700")
        tag_px(cv, cv.X(X(x)) + 10, cv.Y(h) + dy, "h%s = %.2f" % (lab, h) if 1e-6 < h < H_DIFF - 1e-6 else "h%s = %g" % (lab, round(h, 2)), 12, C["deform"], anchor="start")
    tx = X(200) + 30
    cv.text((tx, 470), "水頭損失 ∝ H/k", 12.5, C["text"], anchor="start", weight="700")
    for row, k in enumerate(("A", "B", "C")):
        y = 430 - row * 40
        cv.text((tx, y), "%s：%.2f mm" % (k, DHL[k]), 12, C["load"] if k == "C" else C["text"], anchor="start", weight="700" if k == "C" else "400")
        cv.math_px(cv.X(tx) + 120, cv.Y(y), "k = %s cm/s" % KS[k], 11.5, C["muted"], anchor="start")
    cv.text((tx, 300), "C 層占 %.0f%%" % (100 * DHL["C"] / H_DIFF), 12.5, C["load"], anchor="start", weight="700")
    return cv

compose([fig_head()],
        title="圖 2　總水頭沿土柱：k 最小的 C 層吃掉 89% 的水頭",
        sub="串聯滲流各層流速相同，水頭損失與 H/k 成正比；斜率越陡代表透水性越差",
        note="攔錯用：水頭損失不是依厚度平均分配；h 是總水頭（以下水位面為 0），不是壓力水頭。",
        path=os.path.join(OUT, "SM-2022-3-fig-2-head.svg"))
