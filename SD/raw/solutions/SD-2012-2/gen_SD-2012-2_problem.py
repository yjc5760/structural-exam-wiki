#!/usr/bin/env python3
"""SD-2012-2：題目附圖（圖二(a)）重繪（struct-diagram 規範；2026-11-16，SD-U3-2 組 U3-2-G2）
幾何、支承、元件逐項對應題目正本 SD-2012-2-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
圖二(b) 是表格，照錄於題目正本 §2，不重繪。
用法：python3 gen_SD-2012-2_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, dashpot
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2012-2"
TH = 30.0                                   # #2 斜撐與水平夾角（題文 30°；考卷附圖畫成約 35°，以題文為準）
BW = 5.2                                    # 跨度考卷未給，示意
H = BW * math.tan(math.radians(TH))         # 樓高由 30° 決定（示意比例）
def fig1():
    cv = fit(600, 440, (-1.3, BW + 0.9), (-1.5, H + 0.9), L=20, R=20, T=20, B=20)
    for x in (0, BW):
        cv.line((x, 0), (x, H), C["member"], 2.4, cap="butt"); cv.support((x, 0), "fixed")   # #7 柱底
    cv.line((0, H), (BW, H), C["member"], 7, cap="butt")                                      # #6 剛性樓版
    cv.math((BW/2, H), "m", 18, C["text"], dy=-18)                                            # #5 m＝2000 kg
    cv.math((0, H/2), "k", 17, C["text"], "end", dx=-10)                                      # #5 k＝8×10⁴ N/m
    dashpot(cv, (0, 0), (BW, H), wd=0.17, color=C["member"], w=2.0)                          # #3 #4 左柱底→右梁柱接頭
    r = 1.1                                                                                    # #2 夾角標註
    pts = [(r*math.cos(math.radians(a)), r*math.sin(math.radians(a))) for a in [i*TH/20 for i in range(21)]]
    cv.poly(pts, C["accent"], 1.6)
    cv.text((1.25*math.cos(math.radians(TH/2)), 1.25*math.sin(math.radians(TH/2))), "30°", 13.5, C["accent"], "start", dx=4)
    cv.text((BW*0.62, H*0.62), "線性黏滯消能元件", 13, C["text"], "start", dx=6, dy=26)        # #1 c 沿元件軸向
    cv.text_px(300, 405, "k = 8×10⁴ N/m，m = 2000 kg，阻尼比 5%；c = 4×10³ N·s/m（元件軸向）", 12.5, C["muted"])
    cv.text_px(300, 425, "斜撐軸向變形忽略；圖二(a)　（圖二(b) 為表格，見題目正本）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "斜撐 30°（附圖畫約 35°）、由左柱底到右梁柱接頭；c 為元件軸向阻尼係數")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
