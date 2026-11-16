#!/usr/bin/env python3
"""SD-2010-3 解題圖解（struct-diagram；2026-11-16，X-G1 階段 E）
fig-3-unit：縱向振動單元。第 2、4 墩（雙鉸）各帶兩跨上構縱向平移 U0、墩柱懸臂彎曲；第 1、3 墩（雙滾）梁端滑動、墩柱不受力。
攔下的錯誤：舊解把四墩都當成與梁銷接、四墩並聯、全橋只取 3 跨（T＝πL²√(m/EI)）。
圖上結果式由下方常數算出（係數 2π√(2/3)）；位移放大示意。用法：python3 gen_SD-2010-3.py [輸出目錄]；再跑 render.py 產 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2010-3"

N_SPAN = 2                      # 每支雙鉸墩承擔的跨數（判讀 #2、#3）
K_COEF = 3                      # 懸臂墩 k = 3EI/L³
U_COEF = N_SPAN / K_COEF        # U0 = (2/3) m g L⁴/EI
T_COEF = 2*math.pi*math.sqrt(U_COEF)   # T = 2π√(U0/g) → 係數 × L²√(m/EI)
T_OLD = math.pi
SP, HP, DK, GAP = 160, 170, 14, 6       # 跨長、墩高（皆 L）、梁深、梁縫（像素）
XP = [140, 300, 460, 620]; KIND = ["roller", "pin", "roller", "pin"]
YG, d = 120, 34                          # 墩底高程、示意位移

def fig3():
    W, H = 820, 470
    cv = Canvas(W, H, sx=1, bg="#FFFFFF")
    YT = YG + HP; YB = YT + 10
    cv.text_px(W/2, 28, "縱向振動單元：一支雙鉸墩＋兩跨（第 1、3 墩為雙滾，縱向不受力）", 15, C["text"], weight="700")
    spans = [(XP[0]-SP*0.55, XP[0], "ext"), (XP[0], XP[1], "A"), (XP[1], XP[2], "A"), (XP[2], XP[3], "B"), (XP[3], XP[3]+SP*0.55, "B")]
    col = {"A": C["deform"], "B": C["accent"], "ext": C["member2"]}
    fill = {"A": C["fill_c"], "B": "rgba(180,83,9,0.16)", "ext": "rgba(138,148,166,0.15)"}
    for a, b, u in spans:      # 原位置（ghost）
        cv.polygon([(a+GAP/2, YB), (b-GAP/2, YB), (b-GAP/2, YB+DK), (a+GAP/2, YB+DK)], "none", C["ghost"], 1.4)
    for x, k in zip(XP, KIND):
        cv.line((x, YG), (x, YT), C["ghost"], 6, cap="butt")
        cv.support((x, YG), "fixed", size=18)
    for a, b, u in spans:      # 變形後：所有單元同向平移 d
        cv.polygon([(a+GAP/2+d, YB), (b-GAP/2+d, YB), (b-GAP/2+d, YB+DK), (a+GAP/2+d, YB+DK)], fill[u], col[u], 2.2)
    for x, k in zip(XP, KIND):
        if k == "pin":         # 懸臂墩頂位移 d：w(ξ)=d(3ξ²−ξ³)/2
            pts = [(x + d*(3*(i/40)**2 - (i/40)**3)/2, YG + HP*i/40) for i in range(41)]
            cv.poly(pts, C["member"], 6)
            for s in (-1, 1): cv.polygon([(x+d+s*7, YB), (x+d+s*7-7, YT), (x+d+s*7+7, YT)], "#FFFFFF", C["member"], 2)
        else:                  # 滾支承：墩不動、梁端滑過
            cv.line((x, YG), (x, YT), C["member"], 6, cap="butt")
            for s in (-1, 1): cv.circle((x+s*7, YT+5), 5, "#FFFFFF", C["member"], 2)
            cv.arrow((x - 10, YB + DK + 16), (x + d - 4, YB + DK + 16), C["muted"], 1.6, 7)
    cv.text_px(XP[0], H - (YG - 30), "滾：梁端滑動", 12.5, C["muted"])
    cv.text_px(XP[2], H - (YG - 30), "滾：梁端滑動", 12.5, C["muted"])
    cv.text_px(XP[1], H - (YG - 30), "鉸：承擔兩跨", 12.5, C["deform"], weight="700")
    cv.text_px(XP[3], H - (YG - 30), "鉸：承擔兩跨", 12.5, C["accent"], weight="700")
    cv.text_px((XP[0]+XP[2])/2 + d, H - (YB + DK + 26), "單元 A：M＝2mL", 13, C["deform"], weight="700")
    cv.text_px((XP[2]+XP[3]+SP*0.55)/2 + d, H - (YB + DK + 26), "單元 B：M＝2mL", 13, C["accent"], weight="700")
    lines = [f"每支雙鉸墩：k＝{K_COEF}EI/L³，U0＝(2/3)·mgL⁴/EI",
             f"T＝2π√(U0/g)＝2πL²√(2m/3EI)≈{T_COEF:.3f}·L²√(m/EI)",
             f"（舊解四墩並聯、只取三跨：{T_OLD:.3f}·L²√(m/EI)，少 {100*(1-T_OLD/T_COEF):.0f}%）"]
    for i, s in enumerate(lines):
        cv.text_px(W/2, 68 + 22*i, s, 13.5 if i < 2 else 12.5, C["text"] if i < 2 else C["muted"], weight="700" if i == 1 else "400")
    return cv.save(f"{OUT}/{TAG}-fig-3-unit.svg")

FIGURES = [(fig3, "振動單元＝一支雙鉸墩＋兩跨（舊解四墩並聯）")]
if __name__ == "__main__":
    for fn, c in FIGURES: print(fn(), "—", c)
