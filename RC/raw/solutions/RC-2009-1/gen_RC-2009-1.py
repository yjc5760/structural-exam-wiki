#!/usr/bin/env python3
"""
RC-2009-1 耐震柱橫向鋼筋配置 — 解題圖解

用法：python3 gen_RC-2009-1.py [輸出目錄]（預設 figs/）
依據：RC-2009-1.md §4 二～七（建築物混凝土結構設計規範 112 年版 §18.4.5、表 18.4.5.4、§18.4.6.2.1）。
本題為說明題，無柱尺寸；圖為示意，分區長度與間距上限以規範式子標示。
FIGURES
  fig-1-column-zones  柱立面分區＋斷面箍筋型式  攔：l_o 三值取錯、圍束區間距漏 s_o、V_c＝0 只看軸力
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2009-1"

# ── 示意尺度（柱寬 b＝1）──
B = 1.0
LN = 6.0            # 柱淨高（示意 6b）
LO = 1.2            # 圍束區長（示意；規範 max(h, l_n/6, 45 cm)）
S_IN, S_OUT = 0.16, 0.34   # 示意間距：圍束區密、區外疏


def fig1_column_zones():
    W, H = 520, 640
    s = 62.0
    a = Canvas(W, H, sx=s, ox=W / 2 - 40, oy=125)
    a.panel("柱立面：分區與間距", "示意；兩端梁柱接頭內箍筋延續")
    for y0 in (-0.7, LN):
        a.polygon([(-1.4, y0), (B + 1.4, y0), (B + 1.4, y0 + 0.7), (-1.4, y0 + 0.7)], "#DCE3EC", C["member"], 2.0)
    a.polygon([(0, 0), (B, 0), (B, LN), (0, LN)], "#EDF1F6", C["member"], 2.2)
    for y0, y1 in ((0, LO), (LN - LO, LN)):
        a.polygon([(0, y0), (B, y0), (B, y1), (0, y1)], C["fill_c"], "none")
    y = 0.08
    while y < LN:
        dense = y < LO or y > LN - LO
        a.line((0.05, y), (B - 0.05, y), C["deform"], 2.0 if dense else 1.4)
        y += S_IN if dense else S_OUT
    a.polygon([(0, LN / 4), (B, LN / 4), (B, 3 * LN / 4), (0, 3 * LN / 4)], "none", C["bmd"], 2.0)
    a.dim((B + 0.15, LO), (B + 0.15, 0), "l_o", off=-6, label_off=-16, size=14)
    a.dim((B + 0.15, LN), (B + 0.15, LN - LO), "l_o", off=-6, label_off=-16, size=14)
    a.dim((-0.15, 3 * LN / 4), (-0.15, LN / 4), "l_n/2", off=-6, label_off=22, size=14)
    a.text((-0.95, LN / 2 - 0.55), "搭接只能", 12.5, C["bmd"], weight="700")
    a.text((-0.95, LN / 2 - 0.8), "在此段", 12.5, C["bmd"], weight="700")
    a.text((B + 1.15, LO / 2 + 0.12), "圍束區", 12.5, C["compr"], weight="700")
    a.text((B + 1.15, LN / 2 + 0.25), "區外", 12.5, C["muted"], weight="700")
    a.text((B + 1.15, LN / 2), "s ≤ min(6d_b, 15 cm)", 12, C["muted"])
    a.text_px(W / 2, H - 46, "l_o ≥ max(h, l_n/6, 45 cm)", 14, C["compr"], weight="700")
    a.text_px(W / 2, H - 22, "s ≤ min(b/4, 6d_b, s_o)，s_o＝10＋(35 − h_x)/3（10～15 cm）", 13, C["compr"], weight="700")

    b = Canvas(W, H, sx=300.0, ox=W / 2 - 150, oy=250)
    b.panel("圍束區斷面：箍筋＋繫筋", "每根角筋與隔根縱筋受支撐；h_x ≤ 35 cm")
    b.polygon([(0, 0), (1, 0), (1, 1), (0, 1)], "#EDF1F6", C["member"], 2.2)
    c0, c1 = 0.1, 0.9
    b.polygon([(c0, c0), (c1, c0), (c1, c1), (c0, c1)], "none", C["deform"], 2.6)
    bars = [c0 + 0.04 + (c1 - c0 - 0.08) * i / 3 for i in range(4)]
    for x in bars:
        for yb in (bars[0], bars[-1]):
            b.circle((x, yb), 0.025, C["member"], C["member"], 1.0)
    for yb in bars[1:3]:
        for x in (bars[0], bars[-1]):
            b.circle((x, yb), 0.025, C["member"], C["member"], 1.0)
    for x in bars[1:3]:
        b.line((x, c0), (x, c1), C["deform"], 2.0)
        b.poly([(x, c1), (x + 0.05, c1 - 0.05)], C["deform"], 2.0)
    for yb in bars[1:3]:
        b.line((c0, yb), (c1, yb), C["deform"], 2.0)
        b.poly([(c0, yb), (c0 + 0.05, yb + 0.05)], C["deform"], 2.0)
    b.dim((bars[1], -0.05), (bars[2], -0.05), "h_x", off=0, label_off=14, size=14)
    b.text((0.5, -0.2), "繫筋一端 135°、一端 90°，相鄰繫筋交替；彎鉤延伸 6d_b ≥ 7.5 cm", 12.5, C["text"])
    b.text_px(W / 2, H - 92, "A_{sh}/(s b_c) ≥ max[0.3(A_g/A_{ch} − 1), 0.09] × f'c/f_{yt}", 13.5, C["compr"], weight="700")
    b.text_px(W / 2, H - 66, "0.3 式：補回保護層剝落損失；0.09 式：大斷面最低量", 12.5, C["muted"])
    b.text_px(W / 2, H - 40, "V_c＝0：地震剪力 ≥ ½需求剪力 且 P_u ＜ A_g f'c/20（兩者同時）", 13, C["load"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-column-zones.svg")
    compose([a, b], title=f"{TAG} 圖 1　耐震柱橫向鋼筋配置",
            sub="特殊抗彎矩構架柱；題給軸壓力小於 0.05Ag f'c——只滿足「Vc＝0」兩條件中的軸力條件",
            note="示意圖（本題無尺寸）；藍底為圍束區、綠框為可搭接段",
            path=path)
    return path


FIGURES = [(fig1_column_zones, "§4 二～五", "l_o 三值取錯、圍束區間距漏 s_o、V_c＝0 只看軸力")]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, where, catches in FIGURES:
        print(os.path.basename(fn()), "→", where, "攔：", catches)
