#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2013-3 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2013-3-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2013-3.py [輸出目錄，預設 figs]
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2013-3"

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


P_B, P_H = 30.0, 50.0     # 判讀 #2
P_XO, P_YO = 20.0, 40.0   # 判讀 #1（使用者確認）：量到箍筋外緣
P_DBS = 0.96              # D10 箍筋直徑
P_DBL = 1.27              # D13 縱筋直徑


def fig1_problem():
    B, H = P_B, P_H
    cv = _pc(B, H, t=80)
    _prect(cv, 0, 0, B, H)
    x0, y0 = (B - P_XO) / 2, (H - P_YO) / 2        # 箍筋外緣（判讀 #3：四周各 5 cm）
    t = P_DBS / 2
    _phoop(cv, x0 + t, y0 + t, x0 + P_XO - t, y0 + P_YO - t)
    _phook(cv, (x0 + t, y0 + P_YO - t), -45, 3.0)
    r = P_DBS + P_DBL / 2
    for x in (x0 + r, x0 + P_XO - r):
        for y in (y0 + r, y0 + P_YO - r):
            _pbar(cv, (x, y), 0.9)
    cv.text((B / 2, y0 + P_YO - 5), "D13", 13)
    cv.text((B / 2, y0 + 5), "D13", 13)
    cv.text((B / 2, H / 2), "閉合箍筋 D10", 13, color=C["muted"])
    cv.dim((x0, H), (x0 + P_XO, H), f"{P_XO:.0f} cm", off=-30, label_off=-16)
    cv.dim((x0 + P_XO, y0), (x0 + P_XO, y0 + P_YO), f"{P_YO:.0f} cm", off=50, label_off=30)
    cv.dim((0, 0), (B, 0), f"{B:.0f} cm", off=34, label_off=16)
    cv.dim((0, H), (0, 0), f"{H:.0f} cm", off=36, label_off=30)
    return compose([cv], title=f"{TAG} 題目附圖（圖二重繪）",
                   sub="依題目正本判讀清單 #1–#5（#1 使用者確認：20、40 cm 量到箍筋外緣）",
                   note="箍筋中心線 19.04 × 39.04 cm；四周保護層 5 cm（推得）")


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
S_FC, S_FY, S_PHI, S_TU = 280.0, 2800.0, 0.75, 150000.0
S_XO, S_YO = P_XO - P_DBS, P_YO - P_DBS           # 外緣 20×40 扣一個箍筋直徑 → 中心線
S_AOH, S_PH = S_XO * S_YO, 2 * (S_XO + S_YO)
S_AO = 0.85 * S_AOH
S_ATS = S_TU / (2 * S_PHI * S_AO * S_FY)
S_SCALC = 0.71 / S_ATS
S_AL = S_ATS * S_PH
S_AB13 = 1.27
S_SL_CORNER = S_YO - 0.0                             # 長邊角筋間距（以箍筋中心線計，同 §4 Step 6）


def fig2_section():
    B, H = P_B, P_H
    cv = _pc(B, H, maxpx=380, l=200, r=300, t=96, b=96)
    _prect(cv, 0, 0, B, H)
    x0, y0 = (B - P_XO) / 2, (H - P_YO) / 2
    t = P_DBS / 2
    cv.polygon([(x0 + t, y0 + t), (x0 + P_XO - t, y0 + t), (x0 + P_XO - t, y0 + P_YO - t), (x0 + t, y0 + P_YO - t)],
               C["fill_m"])
    _prect(cv, x0, y0, x0 + P_XO, y0 + P_YO, fill="none", stroke=C["muted"], w=1.4)
    _phoop(cv, x0 + t, y0 + t, x0 + P_XO - t, y0 + P_YO - t, w=2.6, color=C["bmd"])
    r = P_DBS + P_DBL / 2
    for x in (x0 + r, x0 + P_XO - r):
        for y in (y0 + r, y0 + P_YO - r):
            _pbar(cv, (x, y), 0.9)
        _pbar(cv, (x, H / 2), 0.9, fill=C["accent"])
    cv.text((B / 2, H / 2 + 3), "Aoh（箍筋中心線所圍）", 13, color=C["bmd"], weight="700")
    cv.text((B / 2, H / 2 - 3), f"{S_AOH:.1f} cm²", 13, color=C["bmd"])
    cv.dim((x0, H), (x0 + P_XO, H), f"{P_XO:.0f}（外緣）", off=-34, label_off=-16)
    cv.dim((x0 + t, 0), (x0 + P_XO - t, 0), f"{S_XO:.2f}（中心線）", off=40, label_off=18)
    cv.dim((x0 + P_XO, y0), (x0 + P_XO, y0 + P_YO), f"{P_YO:.0f}（外緣）", off=70, label_off=40)
    cv.dim((x0 + t, y0 + P_YO - t), (x0 + t, y0 + t), f"{S_YO:.2f}", off=60, label_off=30)
    xr = cv.X(B) + 120
    cv.text_px(xr, cv.Y(H / 2) - 40, "長邊角筋間距", 13, C["accent"], "start", weight="700")
    cv.text_px(xr, cv.Y(H / 2) - 20, f"≈ {S_SL_CORNER:.1f} cm ＞ 30 cm", 13, C["accent"], "start", weight="700")
    cv.text_px(xr, cv.Y(H / 2) + 4, "→ 兩長邊中點各加 1 根 D13", 13, C["accent"], "start")
    cv.text_px(xr, cv.Y(H / 2) + 24, f"（間距 {S_SL_CORNER / 2:.1f} cm）", 13, C["accent"], "start")
    return compose([cv], title="圖 2　扭力斷面：Aoh 量到箍筋中心線，縱筋沿周邊 ≤ 30 cm",
                   sub="灰細線＝箍筋外緣（考卷 20 × 40）；綠線＝箍筋中心線；橘點＝補加的 D13",
                   note=f"At/s = {S_ATS:.4f} → s = {S_SCALC:.1f} cm（D10@12）；Aℓ = {S_AL:.2f} cm² ＞ 4-D13 {4 * S_AB13:.2f} → 6-D13 {6 * S_AB13:.2f} cm²")


def check_solution():
    ok = [("Aoh", S_AOH, 743.3, 0.05), ("ph", S_PH, 116.16, 0.01), ("At/s", S_ATS, 0.05653, 1e-5),
          ("s calc", S_SCALC, 12.56, 0.01), ("Al", S_AL, 6.57, 0.005)]
    for name, got, want, tol in ok:
        assert abs(got - want) <= tol, (name, got, want)
        print(f"  OK  {name:8s} 算得 {got:10.5f}  .md {want}")


FIGURES = [
    ("1-problem", fig1_problem, "把箍筋外緣尺寸 20×40 當成中心線尺寸"),
    ("2-section", fig2_section, "Aoh 用外緣 20×40；長邊縱筋間距 > 30 cm 未補筋"),
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
