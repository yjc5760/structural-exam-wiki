#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2025-3 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2025-3-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2025-3.py [輸出目錄，預設 figs]
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2025-3"

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


P_B, P_H = 40.0, 70.0     # 判讀 #2
P_CC = 4.0                # 判讀 #3 淨保護層（量到箍筋外緣）
P_DBS = 1.27              # D13
P_DB_TOP, P_DB_BOT = 2.87, 3.22   # D29、D32


def fig1_problem():
    B, H = P_B, P_H
    cv = _pc(B, H, t=80)
    _prect(cv, 0, 0, B, H)
    c = P_CC + P_DBS / 2
    _phoop(cv, c, c, B - c, H - c)
    rb = P_CC + P_DBS + P_DB_BOT / 2
    for i in range(4):
        _pbar(cv, (rb + i * (B - 2 * rb) / 3, rb), P_DB_BOT / 2)
    rt = P_CC + P_DBS + P_DB_TOP / 2
    for x in (rt, B - rt):
        _pbar(cv, (x, H - rt), P_DB_TOP / 2)
    cv.text((B / 2, H - 12), "2-D29", 14)
    cv.text((B / 2, 14), "4-D32", 14)
    cv.arrow((B + 9, H / 2), (B - c + 0.4, H / 2), C["muted"], 1.6, 8)
    cv.text((B + 10, H / 2), "D13", 14, anchor="start")
    cv.dim((0, H), (B, H), f"{B:.0f} cm", off=-30, label_off=-16)
    cv.dim((0, H), (0, 0), f"{H:.0f} cm", off=36, label_off=30)
    cv.dim((B, 0), (B, P_CC), f"{P_CC:.0f} cm", off=40, label_off=26)
    cv.dim((B - P_CC, 0), (B, 0), f"{P_CC:.0f} cm", off=34, label_off=16)
    return compose([cv], title=f"{TAG} 題目附圖（圖 2 重繪）",
                   sub="依題目正本判讀清單 #2–#5",
                   note="D13 閉合箍筋 @15 cm；淨保護層 4 cm 量到箍筋外緣")


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
S_FYT, S_AT, S_S = 2800.0, 1.27, 15.0
S_C = P_CC + P_DBS / 2
S_X1, S_Y1 = P_B - 2 * S_C, P_H - 2 * S_C
S_AOH, S_PH = S_X1 * S_Y1, 2 * (S_X1 + S_Y1)
S_AO = 0.85 * S_AOH
S_TN = 2 * S_AO * S_AT * S_FYT / S_S            # kgf·cm，θ = 45°


def fig2_aoh():
    B, H = P_B, P_H
    cv = _pc(B, H, maxpx=400, l=170, r=470, t=90, b=90)
    _prect(cv, 0, 0, B, H)
    c = S_C
    cv.polygon([(c, c), (B - c, c), (B - c, H - c), (c, H - c)], C["fill_m"])
    _prect(cv, P_CC, P_CC, B - P_CC, H - P_CC, fill="none", stroke=C["muted"], w=1.2, dash="4 3")
    _prect(cv, P_CC + P_DBS, P_CC + P_DBS, B - P_CC - P_DBS, H - P_CC - P_DBS, fill="none", stroke=C["muted"], w=1.2, dash="4 3")
    _phoop(cv, c, c, B - c, H - c, w=2.6, color=C["bmd"])
    cv.text((B / 2, H / 2 + 4), "Aoh", 15, color=C["bmd"], weight="700")
    cv.text((B / 2, H / 2 - 2), f"{S_X1:.2f} × {S_Y1:.2f}", 13, color=C["bmd"])
    cv.dim((c, H), (B - c, H), f"x1 = {S_X1:.2f}", off=-30, label_off=-16)
    cv.dim((B - c, c), (B - c, H - c), f"y1 = {S_Y1:.2f}", off=60, label_off=36)
    xr = cv.X(B) + 110
    for i, (txt, col) in enumerate((("綠實線＝箍筋中心線（Aoh、ph 取這條）", C["bmd"]),
                                    ("灰虛線＝箍筋外緣與內緣（不取）", C["muted"]),
                                    (f"Aoh = {S_X1:.2f} × {S_Y1:.2f} ≈ {S_AOH:.0f} cm²、ph = {S_PH:.2f} cm", C["text"]),
                                    (f"Ao = 0.85Aoh ≈ {S_AO:.0f} cm²", C["text"]),
                                    (f"Tn = 2Ao·At·fyt/s = {S_TN / 1e5:.2f} tf·m", C["load"]))):
        cv.text_px(xr, cv.Y(H / 2) - 50 + 24 * i, txt, 13, col, "start", weight="700" if i >= 2 else "400")
    return compose([cv], title="圖 2　扭力斷面幾何：Aoh 量到箍筋中心線、At 是單肢面積",
                   sub=f"{B:.0f} × {H:.0f} cm、淨保護層 {P_CC:.0f} cm 量到箍筋外緣、D13@{S_S:.0f}（箍筋只抗扭）",
                   note="外緣或內緣都會讓 Aoh 偏大或偏小；公式前的 2 已代表一圈箍筋的兩肢")


def check_solution():
    # .md 寫 1866.4（30.73×60.73 實為 1866.23，四捨五入差 0.01%，不影響 7.52 tf·m）
    ok = [("Aoh", S_AOH, 1866.4, 0.3), ("ph", S_PH, 182.92, 0.01), ("Ao", S_AO, 1586.4, 0.15), ("Tn kgf·cm", S_TN, 752165, 60)]
    for name, got, want, tol in ok:
        assert abs(got - want) <= tol, (name, got, want)
        print(f"  OK  {name:10s} 算得 {got:12.3f}  .md {want}")


FIGURES = [
    ("1-problem", fig1_problem, "保護層量測基準弄錯（4 cm 是到箍筋外緣）"),
    ("2-aoh", fig2_aoh, "Aoh 量到外緣或內緣；把 At 當兩肢面積"),
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
