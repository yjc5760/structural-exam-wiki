#!/usr/bin/env python3
"""
SD-2014-4 含速度型消能元件建築物的三種設計狀態 — 解題圖解產生腳本

用法：python3 gen_SD-2014-4.py [輸出目錄]

圖 1  單自由度線性黏滯阻尼系統共振簡諧穩態一個循環內的彈性力 f_s、阻尼力 f_d 與合力，
      標出最大變位、最大速度、最大加速度三個狀態。
      攔「最大加速度情況來自高階振態」：單自由度就有第三狀態，該時刻兩力以 CF1、CF2 倍同時出現。
數值全部由 SD-2014-4.md §4 題(二) 的式子算出（f_s=kU sinθ、f_d=2ξkU cosθ），改 XI 重跑圖會跟著變。
"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.environ.get("STRUCT_DIAGRAM_SCRIPTS",
    os.path.join(HERE, "..", "..", "..", "..", "skills", "struct-diagram", "scripts"))
sys.path.insert(0, SKILL)
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
TAG = "SD-2014-4"

XI = 0.25                                   # §4 題(二) 例：ξ = 0.25
CF1 = math.cos(math.atan(2 * XI))           # 0.894
CF2 = math.sin(math.atan(2 * XI))           # 0.447
TH_A = math.atan(1 / (2 * XI))              # 合力最大的相位 tanθ = 1/(2ξ)
SMAX = math.sqrt(1 + 4 * XI * XI)           # 1.118
fs = lambda th: math.sin(th)
fd = lambda th: 2 * XI * math.cos(th)


def fig1(path):
    W, H = 940, 560
    L, R, T, B = 90, 40, 40, 90
    th_max = 2 * math.pi
    sx = (W - L - R) / th_max
    YS = (H - T - B) / (2 * 1.25) / sx
    cv = Canvas(W, H, sx=sx, ox=L, oy=B + (H - T - B) / 2)
    P = lambda th, f: (th, f * YS)
    # 軸
    cv.arrow(P(0, 0), P(th_max * 1.0, 0), C["muted"], w=1.5, head=8)
    cv.arrow(P(0, -1.22), P(0, 1.25), C["muted"], w=1.5, head=8)
    cv.text(P(th_max, 0), "ωt", 15, C["muted"], dx=-10, dy=-14, italic=True)
    cv.text(P(0, 1.25), "力 / kU", 13, C["muted"], anchor="start", dx=10, dy=4)
    for v in (-1, 1):
        cv.line(P(0, v), P(th_max, v), C["border"], 1, dash="4 4")
        cv.text(P(0, v), f"{v:+d}", 12, C["muted"], anchor="end", dx=-8)
    for k, lab in ((1, "π/2"), (2, "π"), (3, "3π/2"), (4, "2π")):
        cv.text(P(k * math.pi / 2, 0), lab, 12, C["muted"], dy=16)
    N = 400
    ths = [th_max * i / N for i in range(N + 1)]
    cv.poly([P(t, fs(t)) for t in ths], C["deform"], 2.6)
    cv.poly([P(t, fd(t)) for t in ths], C["sfd"], 2.6)
    cv.poly([P(t, fs(t) + fd(t)) for t in ths], C["bmd"], 3.0, dash="8 5")
    # 三狀態
    states = [(0.0, "最大速度", C["sfd"]), (math.pi / 2, "最大變位", C["deform"]), (TH_A, "最大加速度", C["accent"])]
    for th, lab, col in states:
        cv.line(P(th, -1.15), P(th, 1.15), col, 1.6, dash="3 4")
    cv.text(P(0.0, -1.15), "① 最大速度", 13, C["sfd"], anchor="start", dx=6, dy=12, weight="700")
    cv.text(P(math.pi / 2, -1.15), "② 最大變位", 13, C["deform"], anchor="start", dx=6, dy=12, weight="700")
    cv.text(P(TH_A, 1.15), "③ 最大加速度（合力最大）", 13, C["accent"], anchor="start", dx=6, dy=-10, weight="700")
    # ③ 時刻的分量
    cv.dot(P(TH_A, fs(TH_A)), 5, C["deform"])
    cv.dot(P(TH_A, fd(TH_A)), 5, C["sfd"])
    cv.dot(P(TH_A, SMAX), 5, C["bmd"])
    cv.text(P(TH_A, fs(TH_A)), f"{CF1:.3f}", 12.5, C["deform"], anchor="end", dx=-9, dy=-2)
    cv.text(P(TH_A, fd(TH_A)), f"{CF2*2*XI:.3f}", 12.5, C["sfd"], anchor="end", dx=-9, dy=-2)
    cv.dot(P(math.pi / 2, 1.0), 5, C["deform"]); cv.dot(P(0, 2 * XI), 5, C["sfd"])
    cv.text(P(0, 2 * XI), f"{2*XI:.2f}", 12, C["sfd"], anchor="end", dx=-8)
    # ③ 時刻數值說明框（右上空白區）
    bx, by = 3.35, 1.12
    cv.text(P(bx, by), "③ 最大加速度時刻（tan ωt = 1/(2ξ)）：", 13, C["accent"], anchor="start", weight="700")
    cv.text(P(bx, by - 0.14), f"f_{{s}} = CF_{{1}}·kU = {CF1:.3f}kU", 13, C["deform"], anchor="start")
    cv.text(P(bx, by - 0.28), f"f_{{d}} = CF_{{2}}·f_{{d,max}} = {CF2:.3f}×{2*XI:.2f}kU = {CF2*2*XI:.3f}kU", 13, C["sfd"], anchor="start")
    cv.text(P(bx, by - 0.42), f"合力 = (1+4ξ^{{2}})^{{1/2}}kU = {SMAX:.3f}kU", 13, C["bmd"], anchor="start")
    cv.text(P(bx, by - 0.56), f"f_{{d,max}} = 2ξkU = {2*XI:.2f}kU（① 時刻）", 13, C["sfd"], anchor="start")
    cv.legend(W - 250, H - 62, [(C["deform"], "彈性力 f_s = kU sin ωt"), (C["sfd"], "阻尼力 f_d = 2ξkU cos ωt"),
                                (C["bmd"], "合力（＝慣性力）")], size=12.5, gap=20)
    return compose([cv], title=f"圖 1　速度型元件的三種設計狀態（單自由度、共振簡諧穩態，ξ = {XI}）",
                   note="單自由度就有第三狀態：彈性力與阻尼力以 CF1、CF2 倍同時出現、合力最大——與高階振態無關",
                   path=path)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1(os.path.join(OUT, f"{TAG}-fig-1-three-states.svg"))
    print("ok", OUT)
