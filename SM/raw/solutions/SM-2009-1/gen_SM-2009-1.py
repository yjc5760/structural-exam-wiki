# -*- coding: utf-8 -*-
"""SM-2009-1 圖解（題目要求「繪圖說明」的示意圖）。
本題無數值；曲線為示意，只保留 SM-2009-1.md §4 Step 1 的相對關係：
現地能量 > 標準夯實 → 曲線往左上移；原設定含水量在實驗室曲線乾側、落到現地曲線濕側。
用法：python gen_SM-2009-1.py [輸出資料夾]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 示意參數（無單位，只表相對位置）──
GS = 2.70                                   # 繪零空氣孔隙曲線用的假設比重（示意）
ZAV = lambda w: GS / (1 + GS * w / 100)     # γd/γw
ZS = lambda w, S: GS / (1 + GS * w / 100 / S)   # 濕側沿近似等飽和度線（示意）
LAB = dict(wopt=19.0, k=0.0030, S=0.86); LAB["peak"] = ZS(LAB["wopt"], LAB["S"])   # 標準夯實
FLD = dict(wopt=15.0, k=0.0045, S=0.92); FLD["peak"] = ZS(FLD["wopt"], FLD["S"])   # 高能量（現地）
W_SET = 16.8                                # 原設定含水量：LAB 乾側、FLD 濕側
assert FLD["wopt"] < W_SET < LAB["wopt"]
curve_ = lambda c, w: (c["peak"] - c["k"] * (w - c["wopt"]) ** 2) if w <= c["wopt"] else ZS(w, c["S"])

def fig():
    W, H = 900, 560
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (0, 1.6), (0, 1.0), 70, 230, 70, 70))
    X0, X1, Y0, Y1 = 8.0, 28.0, 1.50, 2.05
    SX = lambda w: (w - X0) / (X1 - X0) * 1.6
    SY = lambda g: (g - Y0) / (Y1 - Y0)
    frame(cv, 0, 1.6, 0, 1.0, [], [], "含水量 w", "", grid=False)
    cv.text_px(cv.X(0) - 10, cv.Y(1.0) - 22, "乾單位重 γd", 13, C["text"], anchor="start")
    ws = [X0 + i * (X1 - X0) / 200 for i in range(201)]
    cv.poly([(SX(w), SY(ZAV(w))) for w in ws if SY(ZAV(w)) <= 1.0], C["muted"], 2.0, dash="6 4")
    for c, col, lab in ((LAB, C["deform"], "實驗室標準夯實"), (FLD, C["load"], "現地（能量較高）")):
        pts = [(SX(w), SY(curve_(c, w))) for w in ws if 0 <= SY(curve_(c, w)) <= 1.0 and (w > c["wopt"] - 8.5)]
        cv.poly(pts, col, 3.0)
        cv.dot((SX(c["wopt"]), SY(c["peak"])), 5, fill=col)
        cv.line((SX(c["wopt"]), 0), (SX(c["wopt"]), SY(c["peak"])), col, 1.2, dash="3 3")
        cv.text_px(cv.X(SX(c["wopt"])), cv.Y(0) + 18, ("最佳含水量（實驗室）" if c is LAB else "最佳含水量（現地）"), 12, col)
    # 95% 標準
    g95 = 0.95 * LAB["peak"]
    cv.line((0, SY(g95)), (1.6, SY(g95)), C["accent"], 1.6, dash="8 4")
    cv.text_px(cv.X(1.6) + 8, cv.Y(SY(g95)), "95% γd,max（實驗室）", 12.5, C["accent"], anchor="start")
    # 原設定含水量
    cv.line((SX(W_SET), 0), (SX(W_SET), 1.0), C["bmd"], 2.2, dash="7 4")
    cv.text_px(cv.X(SX(W_SET)) + 40, cv.Y(1.0) - 14, "原設定含水量", 13, C["bmd"], weight="700")
    for c, col, lab in ((LAB, C["deform"], "實驗室曲線的乾側"), (FLD, C["load"], "現地曲線的濕側")):
        g = curve_(c, W_SET)
        cv.dot((SX(W_SET), SY(g)), 6, fill="#FFFFFF", stroke=col, w=2.6)
        tag_px(cv, cv.X(SX(W_SET)) + 14, cv.Y(SY(g)) + (14 if c is LAB else -14), lab, 12.5, col, anchor="start")
    lx, ly = cv.X(1.6) + 8, cv.Y(0.92)
    for k, (col, dash, lab) in enumerate([(C["deform"], None, "標準夯實"), (C["load"], None, "現地高能量"), (C["muted"], "6 4", "零空氣孔隙曲線")]):
        d_ = ' stroke-dasharray="%s"' % dash if dash else ""
        cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3"%s/>' % (lx, ly + k * 24, lx + 28, ly + k * 24, col, d_))
        cv.text_px(lx + 36, ly + k * 24, lab, 12.5, col, anchor="start", weight="700")
    return cv

compose([fig()],
        title="圖 1　能量提高後，同一含水量由乾側變成濕側（示意）",
        sub="現地曲線較高、峰值左移；含水量照原設定控制，γd 仍過 95%，但結構轉為分散、透水性下降",
        note="攔錯用：只看相對夯實度合格就以為達標；同一含水量相對於現地曲線已在最佳含水量濕側，透水性要求失敗。",
        path=os.path.join(OUT, "SM-2009-1-fig-1-compaction.svg"))
