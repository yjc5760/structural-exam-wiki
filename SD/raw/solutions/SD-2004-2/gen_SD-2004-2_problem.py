#!/usr/bin/env python3
"""SD-2004-2：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U3-2 題目正本推廣 U3-2-G1）
幾何、元件、自由度逐項對應題目正本 SD-2004-2-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
考卷附圖沒有尺寸，各元件大小、間距為示意。
用法：python3 gen_SD-2004-2_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2004-2"
RW = 0.22                      # 方塊輪半徑（示意）
def hatch(cv, x0, x1, n=5):    # #9 地面剖線（只畫在三處，照考卷）
    h = 10 / cv.sx
    for i in range(n):
        x = x0 + (x1 - x0) * i / (n - 1)
        cv.line((x, 0), (x - h, -h), C["member"], 1.6)
def cart(cv, x0, x1, label):   # #5 #6 #7 方塊＋兩輪
    yb, yt = 2 * RW, 2 * RW + 1.35
    cv.polygon([(x0, yb), (x1, yb), (x1, yt), (x0, yt)], "#F2F4F7", C["member"], 2.4)
    for xc in (x0 + 0.42, x1 - 0.42):
        cv.circle((xc, RW), RW, "#FFFFFF", C["member"], 2.2)
    cv.math(((x0 + x1) / 2, (yb + yt) / 2), label, 17, C["text"])
    return yb, yt
def fig1():
    cv = fit(720, 300, (-0.7, 9.0), (-0.45, 3.05), L=16, R=16, T=14, B=40)
    cv.line((-0.6, 0), (8.9, 0), C["member"], 3.0)
    hatch(cv, -0.35, 0.65); hatch(cv, 3.5, 4.5); hatch(cv, 7.6, 8.6)
    # #2 左側直立桿（地面運動輸入端），桿底兩小滾輪
    px0, px1, rr = 0.05, 0.30, 0.11
    for xc in (0.06, 0.30):
        cv.circle((xc, rr), rr, "#FFFFFF", C["member"], 2.0)
    cv.line((-0.12, 2 * rr), (0.48, 2 * rr), C["member"], 2.4)
    cv.polygon([(px0, 2 * rr), (px1, 2 * rr), (px1, 2.35), (px0, 2.35)], "#FFFFFF", C["member"], 2.4)
    # #5 m_b、#6 m
    yb, yt = cart(cv, 2.3, 4.6, "m_{b}")
    cart(cv, 6.4, 8.6, "m")
    ys = (yb + yt) / 2
    # #3 彈簧 k_b：桿中段 → m_b 左面；#4 彈簧 k：m_b 右面 → m 左面
    spring(cv, (px1, ys), (2.3, ys), n=4, amp=0.22, lead=0.2)
    cv.math(((px1 + 2.3) / 2, ys + 0.42), "k_{b}", 16, C["text"])
    spring(cv, (4.6, ys), (6.4, ys), n=4, amp=0.22, lead=0.2)
    cv.math((5.5, ys + 0.42), "k", 16, C["text"])
    # #8 自由度與地面輸入（向右為正）
    def dof(x, y, lab, col):
        cv.line((x, y - 0.18), (x, y + 0.18), col, 2.0)
        cv.arrow((x, y), (x + 0.95, y), col, 2.4, 9)
        cv.math((x + 0.95, y), lab, 16, col, "start", dx=6)
    dof(0.175, 2.75, "u_{g}(t)", C["load"])
    dof(3.2, 2.25, "x_{1}(t)", C["deform"])
    dof(7.2, 2.25, "x_{2}(t)", C["deform"])
    cv.text_px(360, 284, "x_{1}、x_{2} 為絕對位移；題文令 m_{b} = 0；考卷未給阻尼（圖上無阻尼器）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "左側為地面運動輸入端、x1 x2 為絕對位移、無阻尼器")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
