#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2008-3 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2008-3-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2008-3.py [輸出目錄，預設 figs]
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2008-3"

# ══════════════════════════════════════════════════════════
# 題目附圖重繪（2026-11-15，RC-U2-1／U2-2 題目正本推廣・批 1）
# 依據：題目正本 <id>-problem.md §4 判讀清單（已確認）。只畫考卷給的東西，不含解題結果；
# 考卷未標尺寸的位置畫成示意，並在副標寫明。
# ══════════════════════════════════════════════════════════
def _pc(Wm, Hm, maxpx=330, l=150, r=170, t=40, b=90):
    s = maxpx / max(Wm, Hm)
    return Canvas(int(Wm * s + l + r), int(Hm * s + t + b), sx=s, ox=l, oy=b)


def _prect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _pbar(cv, p, r=1.25, fill=None):
    cv.circle(p, r, fill=fill or C["member"], stroke=C["member"], w=1.2)


def _phoop(cv, x0, y0, x1, y1, w=3.0, color=None):
    """閉合箍筋（以箍筋中心線畫）"""
    cv.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], color or C["member"], w)


def _phook(cv, p, ang_deg, L=3.0, w=3.0):
    """箍筋彎鉤：由 p 往 ang 方向畫一段（135° 彎鉤用 -45° 指向斷面內）"""
    import math
    a = math.radians(ang_deg)
    cv.line(p, (p[0] + L * math.cos(a), p[1] + L * math.sin(a)), C["member"], w)


P_B, P_H = 30.0, 60.0     # 判讀 #1
P_CC = 4.0                # 判讀 #4 淨保護層（量到肋筋外緣）
P_DB = 1.27               # #4 直徑
P_YMID = 30.0             # 判讀 #2 中高縱筋距頂面 30 cm


def fig1_problem():
    B, H = P_B, P_H
    cv = _pc(B, H)
    _prect(cv, 0, 0, B, H)
    c = P_CC + P_DB / 2                       # 肋筋中心線
    _phoop(cv, c, c, B - c, H - c)
    r = P_CC + P_DB + P_DB / 2                # 縱筋中心距外緣
    for x in (r, B - r):
        for y in (r, H - P_YMID, H - r):
            _pbar(cv, (x, y), 0.9)
    cv.text((B / 2, H / 2 + 8), "#4@15 cm", 13, color=C["muted"])
    cv.dim((0, 0), (B, 0), f"{B:.0f} cm", off=34, label_off=16)
    cv.dim((B, 0), (B, H), f"{H:.0f} cm", off=40, label_off=30)
    cv.dim((0, H - P_YMID), (0, H), f"{P_YMID:.0f} cm", off=-36, label_off=-30)
    return compose([cv], title=f"{TAG} 題目附圖（圖三重繪）",
                   sub="依題目正本判讀清單 #1–#4",
                   note="#4 閉合肋筋；淨保護層 4 cm；縱筋 6 根（含兩側中高）")


# ── 解題圖解共用小工具（2026-11-15 圖解補繪）──
import math as _m


def _pl(cv, x0, y0, x1, y1, color, w=2, dash=None):
    """像素座標（y 由上往下）畫線"""
    cv.line((x0, cv.h - y0), (x1, cv.h - y1), color, w, dash=dash)


def _stack_rows(cv, x0, y0, wmax, vmax, rows, row_h=78, bar_h=26):
    """水平堆疊長條。rows: [(名稱, 說明, [(值, 色, 段落文字)], [(標記值, 色, 標記文字)], 右側結論)]"""
    sc = wmax / vmax
    for i, (name, sub, segs, marks, verdict) in enumerate(rows):
        y = y0 + i * row_h
        cv.text_px(x0 - 16, y + 4, name, 14, C["text"], "end", weight="700")
        cv.text_px(x0 - 16, y + 24, sub, 12, C["muted"], "end")
        cv.rect_px(x0, y, wmax, bar_h, "#EEF1F5", rx=5)
        x = x0
        for v, col, lab in segs:
            w = v * sc
            cv.rect_px(x, y, w, bar_h, col, rx=4)
            if lab and w > 60:
                cv.text_px(x + w / 2, y + bar_h / 2, lab, 12, "#FFFFFF", weight="700")
            x += w
        for j, (v, col, lab) in enumerate(marks):
            xm = x0 + v * sc
            _pl(cv, xm, y - 8, xm, y + bar_h + 8, col, 2.4, dash="5 3")
            cv.text_px(xm, y + bar_h + 22 + 15 * j, lab, 12, col, "middle", weight="700")
        if verdict:
            cv.text_px(x0 + wmax + 14, y + bar_h / 2, verdict, 13, C["text"], "start", weight="700")


# ══════════════════════════════════════════════════════════
# 解題圖解（2026-11-15 圖解補繪；數值全由下方常數現算，檔尾對 §4 assert）
# ══════════════════════════════════════════════════════════
from recipes import bar_compare
S_B, S_H, S_FC, S_PHI = 30.0, 60.0, 280.0, 0.75
S_TU = 300000.0                              # kgf·cm
S_CEFF = 4.0 + 1.27 / 2
S_XOH, S_YOH = S_B - 2 * S_CEFF, S_H - 2 * S_CEFF
S_AOH, S_POH = S_XOH * S_YOH, 2 * (S_XOH + S_YOH)
S_SQ = _m.sqrt(S_FC)
S_TAU = S_TU * S_POH / (1.7 * S_AOH ** 2)
S_VCB = 0.53 * S_SQ
S_LIM = S_PHI * (S_VCB + 2.12 * S_SQ)                 # kgf 制（現行規範）
S_LIM_SI = S_PHI * (S_VCB + 2 / 3 * S_SQ)             # 舊解：SI 係數 2/3 直接代 kgf/cm²


def M_(s):
    assert not any(ord(ch) > 0x2E80 for ch in s), s
    return s


def fig2_limit():
    cases = [
        ("扭剪應力需求", "Tu·ph / 1.7Aoh²（Vu = 0）", S_TAU, M_(f"τ_{{T}} = {S_TAU:.2f} kgf/cm^2"), C["load"]),
        ("現行上限（kgf 制）", "φ(Vc/bwd + 2.12√f'c)", S_LIM, M_(f"{S_LIM:.2f} kgf/cm^2"), C["bmd"]),
        ("誤用 SI 係數", "2/3·√f'c 直接代（舊解）", S_LIM_SI, M_(f"{S_LIM_SI:.2f} kgf/cm^2"), C["ghost"]),
    ]
    return bar_compare(
        cases,
        title="圖 2　斷面大小檢核：需求與上限",
        sub="SI 制 √f'c（MPa）換成 kgf/cm² 須乘 √10.197 = 3.19：2/3 → 2.12",
        note=f"{S_TAU:.2f} ≤ {S_LIM:.2f} → 斷面合適；若把 SI 係數 2/3 直接代 kgf 制，上限只剩 {S_LIM_SI:.2f}，會誤判不合適").svg()


def check_solution():
    ok = [("Aoh cm2", S_AOH, 1051.6, 0.1), ("poh cm", S_POH, 142.92, 0.01), ("tau kgf/cm2", S_TAU, 22.81, 0.01),
          ("limit kgf/cm2", S_LIM, 33.26, 0.01), ("SI limit", S_LIM_SI, 15.02, 0.01)]
    for name, got, want, tol in ok:
        assert abs(got - want) <= tol, (name, got, want)
        print(f"  OK  {name:14s} 算得 {got:10.4f}  .md {want}")


FIGURES = [
    ("1-problem", fig1_problem, "漏掉兩側中高縱筋（只算四角 4 根）"),
    ("2-limit", fig2_limit, "SI 係數 2/3·√f'c 直接代 kgf 制，誤判斷面不合適"),
]


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
