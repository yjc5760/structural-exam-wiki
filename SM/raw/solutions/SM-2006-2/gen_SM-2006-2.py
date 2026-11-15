# -*- coding: utf-8 -*-
"""SM-2006-2 解題圖解（數值取自解析正本 SM-2006-2.md，非題目重繪）。
用法：python gen_SM-2006-2.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)


# ══════ 解題圖解共用：像素座標的深度剖面框（G5，2026-11-15）══════
class PX:
    """值 v → 水平像素、深度 z → 垂直像素（向下）。p() 回傳 Canvas 模型座標（sx = 1）。"""
    def __init__(s, cv, L, R, T, B, vmax, zmax, vmin=0.0):
        s.cv, s.L, s.R, s.T, s.B = cv, L, cv.w - R, T, cv.h - B
        s.vmin, s.vmax, s.zmax = vmin, vmax, zmax
    def x(s, v): return s.L + (v - s.vmin) / (s.vmax - s.vmin) * (s.R - s.L)
    def y(s, z): return s.T + z / s.zmax * (s.B - s.T)
    def p(s, v, z): return (s.x(v), s.cv.h - s.y(z))

def px_axes(m, vt, zt, vlab, zlab="z（m）"):
    cv = m.cv
    for v in vt:
        cv.line(m.p(v, 0), m.p(v, m.zmax), C["border"], 1.0)
        cv.text_px(m.x(v), m.T - 12, "%g" % v, 12, C["muted"])
    for z in zt:
        cv.line(m.p(m.vmin, z), m.p(m.vmax, z), C["border"], 1.0)
        cv.text_px(m.L - 8, m.y(z), "%g" % z, 12, C["muted"], anchor="end")
    cv.line(m.p(m.vmin, 0), m.p(m.vmax, 0), C["muted"], 1.8)
    cv.line(m.p(m.vmin, 0), m.p(m.vmin, m.zmax), C["muted"], 1.8)
    cv.text_px((m.L + m.R) / 2, m.T - 34, vlab, 13, C["text"], weight="700")
    cv.text_px(m.L - 8, m.B + 22, zlab, 12.5, C["muted"], anchor="end")


# ══════ fig-1：樁頭勁度隨 λL 的變化（概念圖；推導題，無題給數值）══════
# ── 由 SM-2006-2 §4 Step 3–4：K/√(k_s S EA) = tanh(λL)，λ = √(k_s S/EA)；短樁極限 K → k_s S L ──
from math import tanh
LM = 4.0
def kn(t): return tanh(t)

def pan():
    cv = Canvas(860, 520); cv.panel("無因次勁度 K / √(ks·S·EA) 與 λL", "樁底反力忽略（情況一）；λL → ∞ 即情況二")
    m = PX(cv, 90, 60, 100, 80, LM, 1.25)        # v = λL、z = 1.25 − K*
    P_ = lambda t, k: m.p(t, 1.25 - k)
    for t in range(0, 5):
        cv.line(P_(t, 0), P_(t, 1.25), C["border"], 1.0)
        cv.text_px(m.x(t), m.B + 18, "%d" % t, 12, C["muted"])
    for k in (0, 0.25, 0.5, 0.75, 1.0, 1.25):
        cv.line(P_(0, k), P_(LM, k), C["border"], 1.0)
        cv.text_px(m.L - 8, m.y(1.25 - k), "%g" % k, 12, C["muted"], anchor="end")
    cv.line(P_(0, 0), P_(LM, 0), C["muted"], 1.8); cv.line(P_(0, 0), P_(0, 1.25), C["muted"], 1.8)
    cv.text_px((m.L + m.R) / 2, m.B + 44, "λL = L·√(ks·S / EA)", 13, C["text"], weight="700")
    ts = [LM * i / 400 for i in range(401)]
    cv.poly([P_(t, 1.0) for t in ts], C["load"], 1.8, dash="6 4")
    cv.poly([P_(t, t) for t in ts if t <= 1.25], C["member2"], 2.0, dash="3 4")
    cv.poly([P_(t, kn(t)) for t in ts], C["compr"], 3.0)
    t3 = 3.0
    cv.dot(P_(t3, kn(t3)), 5.5, fill=C["compr"])
    tag_px(cv, m.x(t3), m.y(1.25 - kn(t3)) + 24, "λL = 3：tanh = %.3f" % kn(t3), 12, C["compr"])
    tag_px(cv, m.x(3.9), m.y(0.25) - 24, "半無限長：K = √(ks·S·EA)", 12, C["load"], anchor="end")
    tag_px(cv, m.x(1.26) + 8, m.y(0.02) + 4, "短樁：K ≈ ks·S·L", 12, C["member2"], anchor="start", weight="400")
    tag_px(cv, m.x(1.75), m.y(1.25 - kn(1.6)) + 60, "K = √(ks·S·EA)·tanh(λL)", 12.5, C["compr"], anchor="start")
    return cv

compose([pan()],
        title="圖 1　樁頭軸向勁度：λL 超過約 3 之後，再加長樁也不增加勁度",
        sub="曲線由 §4 推得的閉合解計算，不含題給數值",
        note="攔錯用：正負號弄反（寫成 P = EA dv/dz）會得到三角函數解；正確的勁度隨 λL 單調收斂到 √(ks·S·EA)。",
        path=os.path.join(OUT, "SM-2006-2-fig-1-stiffness.svg"))
