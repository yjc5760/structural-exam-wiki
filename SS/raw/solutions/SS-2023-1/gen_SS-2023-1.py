#!/usr/bin/env python3
"""
SS-2023-1 兩層不規則構架各柱有效長度係數 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2023-1.py [輸出目錄]

重繪依據：題目正本 SS-2023-1-problem.md §4 判讀清單（2026-11-02 已確認）。
只重繪構架（依比例）；所附對位圖屬設計圖表，不重繪。各構材 I 值見題目正本 §1 表格。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2023-1"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2023-1-problem.md §4，已確認）；單位 m
# ══════════════════════════════════════════════════════════
SP_AB, SP_BC = 6.0, 10.0          # #2 梁 DE（GH）6 m、EF 10 m
H1, H2 = 4.0, 4.0                 # #2 一樓、二樓各 4 m
SUPPORT = {"A": "fixed", "B": "fixed", "C": "pin"}    # #1 A、B 固接；C 鉸支
XA, XB, XC = 0.0, SP_AB, SP_AB + SP_BC
N = {"A": (XA, 0), "B": (XB, 0), "C": (XC, 0), "D": (XA, H1), "E": (XB, H1), "F": (XC, H1),
     "G": (XA, H1 + H2), "H": (XB, H1 + H2)}          # #4 二樓只在左跨
MEMBERS = ["AD", "BE", "CF", "DG", "EH", "DE", "EF", "GH"]   # #3 節點皆剛接


def fig1_problem():
    W, H, sx = 760, 540, 30
    cv = Canvas(W, H, sx=sx, ox=150, oy=110)
    cv.panel("構架", "依比例；節點皆剛接")
    for m in MEMBERS:
        cv.line(N[m[0]], N[m[1]], C["member"], 4.2, cap="butt")
    for n, kind in SUPPORT.items():
        cv.support(N[n], kind, 0, size=16 if kind == "pin" else 20)
    off = {"A": (-24, -8), "B": (24, -10), "C": (-24, -10), "D": (-16, -14), "E": (16, -14),
           "F": (16, -14), "G": (-16, -14), "H": (16, -14)}
    for n, (dx, dy) in off.items():
        cv.text(N[n], n, 16, C["text"], "middle", dx=dx, dy=dy, weight="700")
    for n, lab in (("A", "Fixed"), ("B", "Fixed"), ("C", "Hinge")):
        cv.text(N[n], lab, 13, C["muted"], dy=44)
    cv.dim((XA, 0), (XB, 0), f"{SP_AB:g}m", off=72, label_off=16)
    cv.dim((XB, 0), (XC, 0), f"{SP_BC:g}m", off=72, label_off=16)
    cv.dim((XA, 0), (XA, H1), f"{H1:g}m", off=-50, label_off=-24)
    cv.dim((XA, H1), (XA, H1 + H2), f"{H2:g}m", off=-50, label_off=-24)
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title="SS-2023-1 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#4；對位圖為設計圖表，不重繪",
            note="二樓只在左跨（柱 DG、EH，梁 GH）；F 只接柱 CF 與梁 EF；C 為鉸支",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "C 讀成固接；二樓多畫到右跨；跨度 6／10 m 對調"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
