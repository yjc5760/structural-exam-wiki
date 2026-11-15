#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"

"""RC-2018-3 解題圖解（2026-11-15 圖解補繪 DIAG-RC-U3-B1）；數值由常數現算，檔尾對解析 §4 assert。"""
TAG = "RC-2018-3"
BW, H, D, HF, SPC, LN = 40.0, 120.0, 113.0, 15.0, 300.0, 1200.0
NB, DB, DS, COVER, FY = 12, 2.54, 1.27, 4.0, 4200.0
OVH = min(8 * HF, (SPC - BW) / 2, LN / 8)
BE = BW + 2 * OVH
WDIST = min(BE, LN / 10)
FS = 2 / 3 * FY
CC = COVER + DS
SMAX = min(38 * (2800 / FS) - 2.5 * CC, 30 * (2800 / FS))
SBAR = WDIST / NB
SKIN_ZONE = H / 2


def fig1():
    W, Hh = 1180, 640
    cv = Canvas(W, Hh, sx=3.1, ox=W / 2, oy=40, bg="#FFFFFF")
    cv.text_px(W / 2, 30, f"{TAG} 圖 1　負彎矩 T 梁：主筋分布寬度與側面表層筋範圍", 17.5, weight="700")
    cv.text_px(W / 2, 54, "主筋分布寬度＝min(有效翼寬, ℓn/10)；表層筋自受拉面（頂面）起 h/2", 13, C["muted"])
    top = H
    # 翼版（畫到有效翼寬外一些）＋梁腹
    xs = BE / 2 + 20
    cv.polygon([(-xs, top), (xs, top), (xs, top - HF), (BW / 2, top - HF), (BW / 2, 0), (-BW / 2, 0),
                (-BW / 2, top - HF), (-xs, top - HF)], "#EDF1F6", C["member"], 2)
    cv.polygon([(-WDIST / 2, top), (WDIST / 2, top), (WDIST / 2, top - HF), (-WDIST / 2, top - HF)], C["fill_t"])
    for k in range(NB):
        x = -WDIST / 2 + SBAR * (k + 0.5)
        cv.circle((x, top - CC - DB / 2), DB / 2 + 0.4, C["tension"], C["tension"], 1)
    for s in (-1, 1):                                    # 外側翼版另配縱筋（示意）
        for k in range(4):
            x = s * (WDIST / 2 + (OVH - (WDIST - BW) / 2) * (k + 0.5) / 4)
            cv.circle((x, top - CC - 0.8), 0.9, C["member2"], C["member2"], 1)
    for s in (-1, 1):                                    # 表層筋區
        x = s * BW / 2
        cv.line((x + s * 2.5, top - HF), (x + s * 2.5, top - SKIN_ZONE), C["accent"], 5)
        for y in (top - 30, top - 50):
            cv.circle((x - s * (CC + 0.8), y), 0.9, C["accent"], C["accent"], 1)
    cv.line((-BE / 2 - 10, top - SKIN_ZONE), (BE / 2 + 10, top - SKIN_ZONE), C["accent"], 1, dash="5 4")
    cv.text((BW / 2 + 14, top - SKIN_ZONE - 4), "h/2 線（距頂 60）", 12, C["accent"], anchor="start")
    cv.text((BW / 2 + 14, top - (HF + SKIN_ZONE) / 2), f"表層筋：梁腹兩側 15～60 cm，間距 ≤ {SMAX:.1f}", 12.5, C["accent"], anchor="start")
    cv.dim((-BE / 2, top), (BE / 2, top), f"{BE:.0f}", off=-62, label_off=-13)
    cv.dim((-WDIST / 2, top), (WDIST / 2, top), f"{WDIST:.0f}", off=-26, label_off=-13)
    cv.text((BE / 4 + 10, top + 62 / 3.1 + 4.2), f"有效翼寬 b_{{e}}＝40＋2×{OVH:.0f}", 12.5, C["muted"])
    cv.text((WDIST / 2 + 4, top + 26 / 3.1 + 4.2), "主筋分布寬度＝ℓn/10", 12.5, C["tension"], anchor="start")
    cv.line((-BE / 2, top + 4), (-BE / 2, top - HF - 4), C["dim"], 1, dash="3 3")
    cv.line((BE / 2, top + 4), (BE / 2, top - HF - 4), C["dim"], 1, dash="3 3")
    cv.text((-(WDIST / 2 + BE / 2) / 2, top - HF - 8), "另配縱向筋", 12, C["muted"])
    cv.text(((WDIST / 2 + BE / 2) / 2, top - HF - 8), "另配縱向筋", 12, C["muted"])
    cv.dim((-BW / 2, 0), (BW / 2, 0), "40", off=14, label_off=12)
    cv.dim((-BW / 2, 0), (-BW / 2, top - HF), "105", off=-30, label_off=-20)
    cv.text((-BW / 2 - 16, top - HF - 12), "梁腹（全深 h 120）", 12, C["muted"], anchor="end")
    tx = 40
    rows = [(f"12-D25 均布於 {WDIST:.0f} cm，中心距 {SBAR:.0f} cm ≤ s_{{max}}", C["tension"]),
            (f"主筋 c_{{c}}＝淨保護層 4＋肋筋 1.27＝{CC:.2f} cm", C["text"]),
            (f"s_{{max}}＝38(2800/f_{{s}})−2.5c_{{c}}＝{SMAX:.1f} cm（f_{{s}}＝2/3 f_{{y}}）", C["text"]),
            ("", C["text"]),
            ("舊解：分布寬 b_w＋ℓn/10＝160（條文比的是有效翼寬全寬）", C["load"]),
            ("     c_{c} 取 4 → 28.75；表層筋 d/6＝18.8（舊規定）", C["load"])]
    for i, (s, col) in enumerate(rows):
        if s:
            cv.text_px(tx, Hh - 150 + i * 22, s, 12.5, col, "start")
    return cv.svg()


FIGURES = [("1-flange-distribution", fig1, "分布寬度取有效翼寬與 ℓn/10 較小者；表層筋從頂面量 h/2")]


def check_solution():
    for name, got, want, tol in [("be", BE, 280, 0), ("width", WDIST, 120, 0), ("cc", CC, 5.27, 1e-9),
                                 ("smax", SMAX, 24.8, 0.05), ("s", SBAR, 10, 0), ("zone", SKIN_ZONE, 60, 0)]:
        assert abs(got - want) <= tol, (name, got, want)
    print("check_solution：§4 對帳全過")


def main():
    check_solution(); os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        p = os.path.join(OUT, f"{TAG}-fig-{name}.svg"); open(p, "w", encoding="utf-8").write(fn()); print("寫出", p, "｜攔：", why)


if __name__ == "__main__":
    main()
