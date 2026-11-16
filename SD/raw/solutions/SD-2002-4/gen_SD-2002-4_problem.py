#!/usr/bin/env python3
"""SD-2002-4：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U2-2 組 U2-2-G1）
幾何、支承、質量逐項對應題目正本 SD-2002-4-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2002-4_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2002-4"
# ── 判讀清單 ──
L = 3.0            # #7 各樓層柱高 L = 3 m
BW = 4.6           # 跨度考卷未給（示意；考卷圖上兩屋同寬）
GAP = 1.4          # Δ 為待求，繪圖間距僅示意（#10、#11）
XA, XB = 0.0, BW + GAP          # 單層屋左柱、雙層屋左柱 x
T = 0.22           # 樓版畫粗線（#5 剪力房屋：剛性樓版）
def slab(cv, x0, y):
    cv.polygon([(x0 - 0.05, y), (x0 + BW + 0.05, y), (x0 + BW + 0.05, y + T), (x0 - 0.05, y + T)], C["member"])
def fig1():
    cv = fit(760, 440, (-1.2, 2*BW + GAP + 2.4), (-1.3, 2*L + 0.7), L=20, R=20, T=20, B=20)
    ground(cv, (-1.0, 0), (2*BW + GAP + 2.2, 0))                      # #9 柱底固定於地面
    # 單層屋（#6 兩柱、#7 柱高 L、#8 屋頂 m）
    for x in (XA, XA + BW):
        cv.line((x, 0), (x, L), C["member"], 3.0, cap="butt")
        cv.math((x, L/2), "EI", 16, C["text"], "start" if x == XA else "end", dx=12 if x == XA else -12)
    slab(cv, XA, L); cv.math((XA, L + T), "m", 17, C["text"], "end", dx=-6, dy=-10)
    # 雙層屋（#6、#7、#8）
    for x in (XB, XB + BW):
        cv.line((x, 0), (x, 2*L), C["member"], 3.0, cap="butt")
        for y in (L/2, 1.5*L):
            cv.math((x, y), "EI", 16, C["text"], "start" if x == XB else "end", dx=12 if x == XB else -12)
    for y in (L, 2*L):
        slab(cv, XB, y); cv.math((XB, y + T), "m", 17, C["text"], "end", dx=-6, dy=-10)
    # #2 單層屋屋頂與雙層屋二樓同高（同一條 y = L）
    cv.line((XA + BW, L + T/2), (XB, L + T/2), C["muted"], 1.2, dash="5,4")
    # 尺寸：#7 兩段 L
    xd = XB + BW + 0.9
    cv.dim((xd, 0), (xd, L), "L", label_off=-16); cv.dim((xd, L), (xd, 2*L), "L", label_off=-16)
    # #10 Δ：單層屋右柱外緣 ↔ 雙層屋左柱外緣，標在地面下
    cv.line((XA + BW, 0), (XA + BW, -0.85), C["dim"], 1.2); cv.line((XB, 0), (XB, -0.85), C["dim"], 1.2)
    cv.double_arrow((XA + BW, -0.6), (XB, -0.6), C["dim"], 1.8, 8); cv.math(((XA + BW + XB)/2, -0.6), "Δ", 16, C["text"], dy=-12)
    cv.text_px(380, 428, "m = 800 Ton（質量）；L = 3 m；每根柱 EI = 4.5×10⁴ kN·m²；Δ 為所求（圖上間距示意）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "碰撞高度：單層屋屋頂與雙層屋二樓同在 L；Δ 量到兩柱外緣；每層兩根柱各 EI")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
