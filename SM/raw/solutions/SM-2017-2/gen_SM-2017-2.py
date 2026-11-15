# -*- coding: utf-8 -*-
"""SM-2017-2 圖解。
fig-1-compaction-cbr：題目要求的夯實曲線（γd–ω）與 CBR–ω，標出 γdmax、ωOMC 與 CBR = 10 的乾、濕側邊界。
數值只取自題目正本 §2 試驗表與解析 §4（Step 1–3），不另行擬合。
用法：python gen_SM-2017-2.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §2 試驗表 ───────────────────────────────
W_PCT = [8.0, 10.0, 12.0, 16.0, 18.0]
GD    = [17.2, 18.2, 18.6, 18.3, 17.3]
CBR   = [4.0, 9.0, 12.0, 11.0, 7.0]
CBR_REQ = 10.0

# ── 解析 §4 Step 1：過 ω = 10、12、16 的拋物線求峰值 ──
(x1, x2, x3), (y1, y2, y3) = (W_PCT[1], W_PCT[2], W_PCT[3]), (GD[1], GD[2], GD[3])
def para(x):   # Lagrange 拋物線
    return (y1 * (x - x2) * (x - x3) / ((x1 - x2) * (x1 - x3)) +
            y2 * (x - x1) * (x - x3) / ((x2 - x1) * (x2 - x3)) +
            y3 * (x - x1) * (x - x2) / ((x3 - x1) * (x3 - x2)))
def dpara(x, h=1e-6): return (para(x + h) - para(x - h)) / (2 * h)
A_ = (y1 / ((x1 - x2) * (x1 - x3)) + y2 / ((x2 - x1) * (x2 - x3)) + y3 / ((x3 - x1) * (x3 - x2)))
B_ = -(y1 * (x2 + x3) / ((x1 - x2) * (x1 - x3)) + y2 * (x1 + x3) / ((x2 - x1) * (x2 - x3))
       + y3 * (x1 + x2) / ((x3 - x1) * (x3 - x2)))
W_OPT = -B_ / (2 * A_)                     # 13.2 %（§4 Step 1）
GD_MAX = para(W_OPT)                       # 18.66 kN/m³

# ── 解析 §4 Step 2：CBR = 10 邊界，γd 以相鄰試驗點線性內插 ──
def lin(xa, xb, ya, yb, x): return ya + (yb - ya) * (x - xa) / (xb - xa)
f_dry = (CBR_REQ - CBR[1]) / (CBR[2] - CBR[1])             # 1/3
f_wet = (CBR_REQ - CBR[4]) / (CBR[3] - CBR[4])             # 3/4
W_DRY = W_PCT[1] + f_dry * (W_PCT[2] - W_PCT[1])           # 10.67 %
W_WET = W_PCT[4] + f_wet * (W_PCT[3] - W_PCT[4])           # 16.5 %
GD_DRY = GD[1] + f_dry * (GD[2] - GD[1])                   # 18.33
GD_WET = GD[4] + f_wet * (GD[3] - GD[4])                   # 18.05
GD_REQ = max(GD_DRY, GD_WET)
RC = GD_REQ / GD_MAX                                        # 98.2 %（§4 Step 3）
# 反例：取較低的 18.05，乾側同一 γd 的含水量與 CBR（線性內插 ω = 8～10）
W_LOWX = W_PCT[0] + (GD_WET - GD[0]) / (GD[1] - GD[0]) * (W_PCT[1] - W_PCT[0])
CBR_LOWX = lin(W_PCT[0], W_PCT[1], CBR[0], CBR[1], W_LOWX)

def smooth_curve():
    """過 5 點的平滑曲線：ω 10～16 用 §4 的拋物線，兩端用斜率銜接的三次 Hermite。"""
    pts = []
    def herm(xa, ya, ma, xb, yb, mb, n=30):
        h = xb - xa
        for j in range(n + 1):
            t = j / n
            h00 = 2*t**3 - 3*t**2 + 1; h10 = t**3 - 2*t**2 + t
            h01 = -2*t**3 + 3*t**2;    h11 = t**3 - t**2
            pts.append((xa + h*t, h00*ya + h10*h*ma + h01*yb + h11*h*mb))
    m10, m16 = dpara(10.0), dpara(16.0)
    herm(8.0, GD[0], (GD[1] - GD[0]) / 2 * 1.2, 10.0, GD[1], m10)
    for j in range(1, 121):
        x = 10.0 + 6.0 * j / 120
        pts.append((x, para(x)))
    herm(16.0, GD[3], m16, 18.0, GD[4], (GD[4] - GD[3]) / 2 * 1.2)
    return pts

def fig():
    W, H = 900, 760
    cv = Canvas(W, H, bg="#FFFFFF")
    L, R = 150, 250
    XA, XB = 7.0, 19.0
    X = lambda w: L + (w - XA) / (XB - XA) * (W - L - R)
    # 上框 γd
    T1, B1, YA, YB = 30, 400, 17.0, 18.9
    Yg = lambda g: B1 - (g - YA) / (YB - YA) * (B1 - T1)
    # 下框 CBR
    T2, B2, CA, CB = 470, 690, 2.0, 14.0
    Yc = lambda c: B2 - (c - CA) / (CB - CA) * (B2 - T2)
    for (t, b, yt, Yf, lab, fmt) in ((T1, B1, [17.0, 17.5, 18.0, 18.5], Yg, "γd（kN/m³）", "%.1f"),
                                     (T2, B2, [2, 4, 6, 8, 10, 12, 14], Yc, "CBR（%）", "%d")):
        for w in range(8, 19, 2):
            seg(cv, (X(w), t), (X(w), b), C["border"], 1.0)
        for v in yt:
            seg(cv, (X(XA), Yf(v)), (X(XB), Yf(v)), C["border"], 1.0)
            cv.text_px(X(XA) - 9, Yf(v), fmt % v, 12.5, C["muted"], anchor="end")
        seg(cv, (X(XA), b), (X(XB), b), C["muted"], 1.9)
        seg(cv, (X(XA), b), (X(XA), t), C["muted"], 1.9)
        cv.text_px(X(XA) - 52, t - 14, lab, 13, C["text"], anchor="middle")
    for w in range(8, 19, 2):
        cv.text_px(X(w), B2 + 18, "%d" % w, 12.5, C["muted"])
    cv.text_px((X(XA) + X(XB)) / 2, B2 + 44, "含水量 ω（%）", 13.5, C["text"])

    # 夯實曲線
    curve(cv, [(X(x), Yg(y)) for x, y in smooth_curve()], C["bmd"], 3.0)
    for x, y in zip(W_PCT, GD):
        dot(cv, X(x), Yg(y), 5.5, C["bmd"])
    # 峰值
    seg(cv, (X(W_OPT), Yg(GD_MAX)), (X(W_OPT), B2), C["accent"], 1.3, dash="5 4")
    seg(cv, (X(XA), Yg(GD_MAX)), (X(W_OPT), Yg(GD_MAX)), C["accent"], 1.3, dash="5 4")
    dot(cv, X(W_OPT), Yg(GD_MAX), 6.5, C["accent"])
    tag_px(cv, X(W_OPT) + 12, Yg(GD_MAX) - 22, "γdmax = %.2f，ωOMC = %.1f%%" % (GD_MAX, W_OPT), 12.5, C["accent"], anchor="start")

    # CBR 折線與 CBR = 10
    curve(cv, [(X(x), Yc(c)) for x, c in zip(W_PCT, CBR)], C["sfd"], 2.6)
    for x, c in zip(W_PCT, CBR):
        dot(cv, X(x), Yc(c), 5.5, C["sfd"])
    seg(cv, (X(XA), Yc(CBR_REQ)), (X(XB), Yc(CBR_REQ)), C["load"], 1.8, dash="8 5")
    cv.text_px(X(XB) + 8, Yc(CBR_REQ), "CBR = 10（設計要求）", 12.5, C["load"], anchor="start", weight="700")
    # 合格區間
    cv.parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>'
                    % (X(W_DRY), Yc(CB), X(W_WET) - X(W_DRY), Yc(CBR_REQ) - Yc(CB), C["fill_m"]))
    for w_, g_, side in ((W_DRY, GD_DRY, "乾側"), (W_WET, GD_WET, "濕側")):
        seg(cv, (X(w_), Yc(CBR_REQ)), (X(w_), Yg(g_)), C["load"], 1.3, dash="4 4")
        dot(cv, X(w_), Yc(CBR_REQ), 5.5, C["load"])
        dot(cv, X(w_), Yg(g_), 5.5, C["load"])
        cv.text_px(X(w_) + (8 if side == "乾側" else -8), Yc(CBR_REQ) + (-14 if side == "乾側" else 18), "%s ω = %.2f%%" % (side, w_), 12, C["load"], anchor=("start" if side == "乾側" else "end"), weight="700")
    # γd 線性內插弦
    seg(cv, (X(W_PCT[1]), Yg(GD[1])), (X(W_PCT[2]), Yg(GD[2])), C["load"], 1.2, dash="2 3")
    seg(cv, (X(W_PCT[3]), Yg(GD[3])), (X(W_PCT[4]), Yg(GD[4])), C["load"], 1.2, dash="2 3")
    tag_px(cv, X(W_DRY) - 10, Yg(GD_DRY) + 24, "γd = %.2f（取此值）" % GD_DRY, 12, C["load"], anchor="end")
    tag_px(cv, X(W_WET) + 10, Yg(GD_WET) + 26, "γd = %.2f" % GD_WET, 12, C["load"], anchor="start")
    # 要求線與反例
    seg(cv, (X(XA), Yg(GD_REQ)), (X(XB), Yg(GD_REQ)), C["deform"], 1.6, dash="8 5")
    cv.text_px(X(XB) + 8, Yg(GD_REQ) - 10, "要求 γd ≥ %.2f" % GD_REQ, 12.5, C["deform"], anchor="start", weight="700")
    cv.text_px(X(XB) + 8, Yg(GD_REQ) + 12, "R = %.2f/%.2f = %.1f%%" % (GD_REQ, GD_MAX, RC * 100), 12.5, C["deform"], anchor="start", weight="700")
    seg(cv, (X(W_LOWX), Yg(GD_WET)), (X(W_LOWX), Yc(CBR_LOWX)), C["muted"], 1.2, dash="2 3")
    dot(cv, X(W_LOWX), Yc(CBR_LOWX), 5, C["muted"])
    dot(cv, X(W_LOWX), Yg(GD_WET), 4.5, C["muted"])
    seg(cv, (X(W_PCT[0]), Yg(GD[0])), (X(W_PCT[1]), Yg(GD[1])), C["muted"], 1.2, dash="2 3")
    tag_px(cv, X(W_LOWX) - 8, Yc(CBR_LOWX) + 26, "若取 %.2f：乾側 ω = %.1f%% 時 CBR = %.1f，小於 10" % (GD_WET, W_LOWX, CBR_LOWX),
           11.5, C["muted"], anchor="start", weight="400")
    cv.legend(W - R + 20, 280, [(C["bmd"], "夯實曲線 γd"), (C["sfd"], "CBR（試驗點連線）"),
                                (C["load"], "CBR = 10 邊界"), (C["deform"], "γd 要求值")], size=12)
    return cv

compose([fig()],
        title="圖 1　夯實曲線與 CBR = 10 的工地密度要求",
        sub="γdmax、ωOMC 取 ω = 10、12、16% 三點拋物線峰值；CBR = 10 邊界的 γd 以相鄰試驗點線性內插",
        note="攔錯用：取濕側較低的 18.05 當要求值時，乾側同一 γd 的 CBR 不到 10——要求值必須取兩側較高者。",
        path=os.path.join(OUT, "SM-2017-2-fig-1-compaction-cbr.svg"))
print("W_OPT %.3f GD_MAX %.3f W_DRY %.3f W_WET %.3f GD_DRY %.3f GD_WET %.3f RC %.4f W_LOWX %.2f CBR_LOWX %.2f"
      % (W_OPT, GD_MAX, W_DRY, W_WET, GD_DRY, GD_WET, RC, W_LOWX, CBR_LOWX))
