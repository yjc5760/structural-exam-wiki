#!/usr/bin/env python3
"""
SS-2024-4 箱型柱–H 型梁接頭之銲接潛在破壞模式（申論）— 題目附圖重繪腳本

用法：
    python3 gen_SS-2024-4.py [輸出目錄]

重繪依據：題目正本 SS-2024-4-problem.md §4 判讀清單（待確認）。
只畫考卷附圖所示：箱型柱（柱壁內面虛線）、柱內上下橫隔板（虛線，與梁翼同高）、H 型梁、
上下翼板與柱面交會的工地銲接、腹板側剪力板（虛線框）與一排螺栓，以及六個圖面文字標註。
考卷未給任何尺寸，全圖為示意比例。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2024-4"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2024-4-problem.md §4，待確認）；考卷無尺寸，以下皆為示意
# ══════════════════════════════════════════════════════════
#   #1 柱內虛線＝內橫隔板，與上下梁翼同高；「電熱熔渣銲」＝隔板與柱壁的銲接（引線指向隔板兩端）
#   #2 「上／下翼板工地銲接」＝梁翼板與柱面交會處（圖未畫銲接符號）
#   #3 「螺栓工地安裝」＝梁腹板以螺栓接剪力板（虛線框＋一排螺栓）
BC, TC = 340.0, 14.0    # 箱型柱寬、柱壁厚（示意）
DB, TFB = 320.0, 12.0   # 梁深、翼板厚（示意）
LB = 680.0              # 梁畫出長度（示意）
HC = 210.0              # 柱伸出梁翼外的長度（示意）
NBOLT = 5               # 圖上螺栓 5 個
SPW, SPH = 42.0, 240.0  # 剪力板寬、高（示意）

PW, PHT = 1160, 760


def _zig(cv, x0, x1, y):
    xm = (x0 + x1) / 2
    cv.poly([(x0, y), (xm - 12, y), (xm - 4, y + 22), (xm + 4, y - 22), (xm + 12, y), (x1, y)],
            C["member"], 1.6)


def _leader(cv, pts_to, txt_at, txt, anchor="end"):
    x, y = cv.P(txt_at)
    for p in pts_to:
        px, py = cv.P(p)
        cv.parts.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{px:.1f}" y2="{py:.1f}" '
                        f'stroke="{C["muted"]}" stroke-width="1.1"/>')
        cv.dot(p, 2.6, C["muted"], C["muted"], 0)
    hx = x + (-60 if anchor == "end" else 60)
    cv.parts.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{hx:.1f}" y2="{y:.1f}" '
                    f'stroke="{C["muted"]}" stroke-width="1.1"/>')
    cv.text_px(hx + (-6 if anchor == "end" else 6), y, txt, 16, C["text"], anchor)


def panel():
    sx = 0.72
    cv = Canvas(PW, PHT, sx=sx, ox=540, oy=180)
    cv.panel("箱型柱–H 型梁接頭立面", "考卷未給尺寸（示意比例）")
    top, bot = DB + HC, -HC
    xl, xr = -BC, 0.0
    # 柱壁：外面實線、內面虛線
    for x in (xl, xr):
        cv.line((x, bot), (x, top), C["member"], 2.2)
    for x in (xl + TC, xr - TC):
        cv.line((x, bot), (x, top), C["member"], 1.3, dash="7 5")
    _zig(cv, xl - 12, xr + 12, top)
    _zig(cv, xl - 12, xr + 12, bot)
    # 內橫隔板（虛線雙線，與梁翼同高）
    for y0 in (DB - TFB, 0.0):
        for yy in (y0, y0 + TFB):
            cv.line((xl + TC, yy), (xr - TC, yy), C["member"], 1.3, dash="7 5")
    # 梁翼板（雙線）與梁端斷裂
    for y0 in (DB - TFB, 0.0):
        cv.polygon([(0, y0), (LB, y0), (LB, y0 + TFB), (0, y0 + TFB)], "#FFFFFF", C["member"], 1.8)
    ym = DB / 2
    cv.poly([(LB, -20), (LB, ym - 30), (LB + 18, ym - 10), (LB - 18, ym + 10), (LB, ym + 30), (LB, DB + 20)],
            C["member"], 1.6)
    # 翼板與柱面交會處（工地銲接位置，黑點）
    for yy in (DB - TFB, TFB):
        cv.dot((2, yy + (TFB / 2 if yy > ym else -TFB / 2)), 5, C["member"], C["member"], 0)
    # 剪力板（虛線框）與螺栓
    sy0 = (DB - SPH) / 2
    cv.poly([(0, sy0), (SPW, sy0), (SPW, sy0 + SPH), (0, sy0 + SPH)], C["member"], 1.3, dash="6 4")
    for i in range(NBOLT):
        y = sy0 + 24 + i * (SPH - 48) / (NBOLT - 1)
        cv.circle((SPW / 2, y), 6.5, "#FFFFFF", C["member"], 1.5)
    # 文字標註（照考卷）
    _leader(cv, [(xr, top - 40)], (110, top + 60), "箱型柱", "start")
    _leader(cv, [(2, DB)], (110, top - 10), "上翼板工地銲接", "start")
    _leader(cv, [(SPW / 2, sy0 + SPH)], (170, DB + 75), "螺栓工地安裝", "start")
    _leader(cv, [(xl + TC + 4, DB - TFB / 2), (xr - TC - 4, DB - TFB / 2)], (xl - 40, DB + 115),
            "電熱熔渣銲", "end")
    _leader(cv, [(xl + TC + 4, TFB / 2), (xr - TC - 4, TFB / 2)], (xl - 40, DB * 0.18 + 40),
            "電熱熔渣銲", "end")
    _leader(cv, [(2, 0)], (150, -150), "下翼板工地銲接", "start")
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([panel()], cols=1,
            title="SS-2024-4 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#3；考卷無尺寸，全圖示意比例",
            note="柱內兩道虛線是與梁翼同高的內橫隔板，「電熱熔渣銲」指隔板與柱壁的銲接，不是梁翼與柱面的銲接",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把電熱熔渣銲當成梁翼與柱面的銲接；漏掉柱內橫隔板這一類銲道的破壞模式"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
