#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"

"""RC-2002-1 解題圖解（2026-11-15 圖解補繪 DIAG-RC-U3-B1）：外角隅特殊配筋（考卷要求繪圖）。
本題無數值；版格長短跨取 ℓ：ℓs＝4：3 示意，角隅區邊長由 ℓ/5 現算（不是短跨），檔尾 assert 對解析 §4 規定。"""
TAG = "RC-2002-1"
LL, LS = 400.0, 300.0                 # 示意：長跨 ℓ、短跨 ℓs（比例 4：3）
ZONE = LL / 5                         # §4 Step 2(c)：長跨 1/5
WRONG = LS / 5                        # 舊解：短跨 1/5（對照）
PW, PH = 560, 460


def _panel(title, sub, mode):
    XV, YV = 0.55 * LL, 0.50 * LS                    # 只畫角隅附近（其餘以折斷線省略）
    cv = Canvas(PW, PH, sx=2.0, ox=90, oy=PH - 130 - LS * 2.0)
    cv.panel(title, sub)
    cv.polygon([(0, LS - YV), (XV, LS - YV), (XV, LS), (0, LS)], "#EDF1F6")
    cv.line((0, LS), (XV, LS), C["member"], 7)          # 外邊梁（上）
    cv.line((0, LS - YV), (0, LS), C["member"], 7)      # 外邊梁（左）
    cv.line((XV, LS - YV), (XV, LS), C["member2"], 1.4, dash="8 3 2 3")
    cv.line((0, LS - YV), (XV, LS - YV), C["member2"], 1.4, dash="8 3 2 3")
    cv.polygon([(0, LS), (ZONE, LS), (ZONE, LS - ZONE), (0, LS - ZONE)], C["fill_m"], C["bmd"], 1.6)
    cv.poly([(0, LS - WRONG), (WRONG, LS - WRONG), (WRONG, LS)], C["load"], 1.4, dash="4 3")
    n = 7
    if mode == 1:
        for k in range(1, n + 1):                    # 頂層：平行對角線（自角隅往版內 ╲）
            c = ZONE * 2 * k / (n + 1) - ZONE
            xa, xb = max(0, c), min(ZONE, ZONE + c)
            cv.line((xa, LS - xa + c), (xb, LS - xb + c), C["tension"], 2.4)
        for k in range(1, n + 1):                    # 底層：垂直對角線（╱）
            c = ZONE * 2 * k / (n + 1)
            xa, xb = max(0, c - ZONE), min(ZONE, c)
            cv.line((xa, LS - (c - xa)), (xb, LS - (c - xb)), C["compr"], 2.2, dash="7 4")
    else:
        for k in range(1, n + 1):
            v = ZONE * k / (n + 1)
            cv.line((v, LS - ZONE), (v, LS), C["tension"], 2.2)
            cv.line((0, LS - v), (ZONE, LS - v), C["tension"], 2.2)
            cv.line((v + 2.5, LS - ZONE), (v + 2.5, LS), C["compr"], 1.8, dash="6 4")
            cv.line((0, LS - v - 2.5), (ZONE, LS - v - 2.5), C["compr"], 1.8, dash="6 4")
    cv.dim((0, LS), (ZONE, LS), "ℓ/5", off=-22, label_off=-14)
    cv.dim((0, LS - ZONE), (0, LS), "ℓ/5", off=-22, label_off=14)
    cv.text((ZONE + 8, LS - 12), "外邊梁（α_{f}＞1.0）或邊牆", 12.5, C["member"], anchor="start")
    cv.text((ZONE + 6, LS - ZONE - 40), "長跨 ℓ 的 1/5", 12.5, C["bmd"], anchor="start", weight="700")
    cv.line((WRONG, LS - WRONG), (ZONE + 8, LS - WRONG - 26), C["load"], 1)
    cv.text((ZONE + 10, LS - WRONG - 26), "紅虛框：短跨 ℓs/5（舊解，偏小）", 11.5, C["load"], anchor="start")
    cv.text((XV - 4, LS - YV + 12), "版內（其餘未畫）", 12, C["muted"], anchor="end")
    return cv


def fig1():
    return compose([_panel("配置方式 1：對角線向", "頂層平行對角線（紅實線）、底層垂直對角線（藍虛線）", 1),
                    _panel("配置方式 2：平行版邊", "頂層 x、y 兩向（紅實線）＋底層 x、y 兩向（藍虛線）", 2)],
                   title=f"{TAG} 圖 1　雙向版外角隅特殊配筋（平面示意）",
                   sub="範圍：自角隅沿兩向各延伸長跨 ℓ 的 1/5；強度：每單位寬設計彎矩＝該版格最大正彎矩；頂、底層都要配",
                   note="攔：範圍取短跨 ℓn/5；只配頂層；漏寫適用條件（邊牆或 αf＞1.0 邊梁）")


FIGURES = [("1-corner-reinforcement", fig1, "範圍用長跨 ℓ/5、頂底層都配、兩種配置方式")]


def check_solution():
    assert ZONE == LL / 5 and ZONE > WRONG
    print("check_solution：§4 規定對帳全過（ℓ/5 取長跨）")


def main():
    check_solution(); os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        p = os.path.join(OUT, f"{TAG}-fig-{name}.svg"); open(p, "w", encoding="utf-8").write(fn()); print("寫出", p, "｜攔：", why)


if __name__ == "__main__":
    main()
