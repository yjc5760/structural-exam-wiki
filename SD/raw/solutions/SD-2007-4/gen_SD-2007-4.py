#!/usr/bin/env python3
"""SD-2007-4 圖解產生器 — ㈡柱的容量設計：V_e 由柱端 M_pr 反算、l_o 圍束區與箍筋間距（混凝土結構設計規範 112 年版 18.4），
以及半高牆造成的短柱效應。幾何由頂端參數決定；短柱的 V_e 放大倍數由 l_u / l_u' 算出。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.join(HERE, "../../../../skills/struct-diagram/scripts")))
from structdraw import Canvas, C, compose
OUT = os.path.join(HERE, "figs")

# ── 示意參數（模型單位）：柱淨高 LU、斷面深度 HC；l_o = max(h, l_u/6, 45 cm) 以 LU = 300 cm、HC = 60 cm 示意 ──
LU, HC = 300.0, 60.0
LO = max(HC, LU / 6, 45.0)          # = 60 cm
WALL = 0.5                           # 半高牆：有效淨高 = (1 − WALL)·LU
LU_S = (1 - WALL) * LU
VE_RATIO = LU / LU_S                 # 同樣 ΣM_pr，V_e' / V_e

def column(cv, x0, y0, lu, lo, label_lu, wall=None):
    w = HC
    yh = y0 + (wall or 0)                       # 有效淨高的下端（短柱為牆頂）
    for yb in (y0 - 25, y0 + lu):
        cv.polygon([(x0 - 70, yb), (x0 + w + 70, yb), (x0 + w + 70, yb + 25), (x0 - 70, yb + 25)], C["ghost"])
    cv.polygon([(x0, y0), (x0 + w, y0), (x0 + w, y0 + lu), (x0, y0 + lu)], C["panel"], C["member"], 2.2)
    zones = [(y0 + lu - lo, y0 + lu), (yh, yh + lo)]
    for ya, yb in zones:
        cv.polygon([(x0, ya), (x0 + w, ya), (x0 + w, yb), (x0, yb)], C["fill_m"], "none")
    def hoops(ya, yb, s, col, wd):
        y = ya + s / 2
        while y < yb:
            cv.line((x0 + 4, y), (x0 + w - 4, y), col, wd); y += s
    for ya, yb in zones: hoops(ya, yb, 10, C["bmd"], 1.8)
    hoops(yh + lo, y0 + lu - lo, 25, C["member2"], 1.4)
    if wall:
        hoops(y0, yh, 25, C["member2"], 1.4)
        cv.polygon([(x0 + w, y0), (x0 + w + 60, y0), (x0 + w + 60, yh), (x0 + w, yh)], C["fill_c"], C["compr"], 1.4)
        cv.text((x0 + w + 30, y0 + wall / 2), "半高牆", 12, C["compr"], weight="700")
    cv.dim((x0 - 45, yh), (x0 - 45, y0 + lu), label_lu, off=0, size=13)
    # 端彎矩（同為順時針作用於柱）與對應的剪力偶（上端向左、下端向右）
    cv.moment_arrow((x0 + w / 2, y0 + lu - 30), r=24, ccw=False, color=C["bmd"], span=230, start=200)
    cv.moment_arrow((x0 + w / 2, yh + 30), r=24, ccw=False, color=C["load"] if wall else C["bmd"], span=230, start=20)
    cv.arrow((x0 + w + 75, y0 + lu - 12), (x0 + w + 12, y0 + lu - 12), C["sfd"], 2.8)
    cv.arrow((x0 - 75, yh + 12), (x0 - 12, yh + 12), C["sfd"], 2.8)
    cv.math((x0 + w + 92, y0 + lu - 12), "V_e" + ("'" if wall else ""), 14, C["sfd"], weight="700")
    cv.math((x0 - 92, yh + 12), "V_e" + ("'" if wall else ""), 14, C["sfd"], weight="700")
    cv.math((x0 + w + 92, y0 + lu - 75), "M_{pr,t}", 13.5, C["bmd"], weight="700")
    cv.math((x0 - 100, yh + 62), "M_{pr,b}", 13.5, C["load"] if wall else C["bmd"], weight="700")
    cv.text((x0 + w + 8, y0 + lu - lo / 2 - 8), "l_o", 13, C["bmd"], anchor="start", weight="700")
    cv.text((x0 + w + 8, yh + lo / 2 + 8), "l_o", 13, C["bmd"], anchor="start", weight="700")
    return x0, w

PW, PH = 500, 720
def panel_a():
    cv = Canvas(PW, PH, sx=1.3, ox=170, oy=200)
    cv.panel("一般柱：V_e 由柱端 M_pr 反算", "l_o 內圍束、符合條件時取 V_c = 0")
    column(cv, 0, 0, LU, LO, "l_u")
    cv.text_px(PW / 2, PH - 110, f"l_o ≥ max(h, l_u/6, 45 cm)（示意 l_o = {LO:.0f} cm）", 12.5, C["bmd"], weight="700")
    cv.text_px(PW / 2, PH - 84, "l_o 內 s ≤ min(最小尺寸/4, 6d_b, s_o)；l_o 外 s ≤ 15 cm", 12.5, C["text"])
    cv.text_px(PW / 2, PH - 58, "V_e = (M_pr,t + M_pr,b) / l_u，且 V_e ≥ 分析所得 V_u", 12.5, C["sfd"], weight="700")
    return cv

def panel_b():
    cv = Canvas(PW, PH, sx=1.3, ox=170, oy=200)
    cv.panel("短柱效應：半高牆縮短有效淨高", f"同樣的 ΣM_pr，l_u' = {1-WALL:.1f} l_u，牆頂處出鉸")
    column(cv, 0, 0, LU, LO, "l_u'", wall=WALL * LU)
    cv.text_px(PW / 2, PH - 110, f"V_e' = ΣM_pr / l_u' = {VE_RATIO:.2f} V_e", 13, C["load"], weight="700")
    cv.text_px(PW / 2, PH - 84, "撓曲控制的柱變成剪力控制（短柱剪力破壞）", 12.5, C["text"])
    cv.text_px(PW / 2, PH - 58, "對策：牆柱間設隔離縫，或以實際淨高設計並全高加密箍筋", 12.5, C["text"])
    return cv

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    compose([panel_a(), panel_b()], cols=2,
            title="圖 1　確保柱為彎矩韌性破壞：容量設計剪力與短柱效應",
            sub="混凝土結構設計規範 112 年版 18.4 節（特殊抗彎矩構架之柱）；尺寸為示意",
            note="攔錯：柱箍筋間距套用梁的 d/4；以分析剪力 Vu 設計柱剪力；忽略半高牆把柱變短",
            path=f"{OUT}/SD-2007-4-fig-1-column-capacity.svg")
    print("l_o =", LO, "Ve ratio =", VE_RATIO)
