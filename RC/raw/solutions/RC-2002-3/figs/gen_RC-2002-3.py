#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2002-3 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2002-3-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2002-3.py [輸出目錄，預設 figs]
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2002-3"

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


P_B, P_H = 36.0, 50.0     # 判讀 #3 斷面外緣
P_E = 12.0                # 判讀 #4／#7：e 為所求，圖上位置僅示意


def fig1_problem():
    B, H = P_B, P_H
    cv = _pc(B, H + 14)
    _prect(cv, 0, 0, B, H)
    xc = B / 2
    cv.line((xc, -4), (xc, H + 14), C["muted"], 1.4, dash="10 4 2 4")
    cv.text((xc, H + 16.5), "中心線", 12, color=C["muted"])
    xl = xc + P_E
    cv.arrow((xl, H + 11), (xl, H + 0.6), C["load"], 3.0, 11)
    cv.math((xl + 2, H + 12.5), "W_{u} = 2 t/m", 15, C["load"], anchor="start")
    cv.dim((xc, H + 6), (xl, H + 6), "e", off=0, label_off=-12, color=C["load"])
    cv.dim((0, 0), (B, 0), f"{B:.0f} cm", off=34, label_off=16)
    cv.dim((0, H), (0, 0), f"{H:.0f} cm", off=36, label_off=30)
    return compose([cv], title=f"{TAG} 題目附圖重繪",
                   sub="依題目正本判讀清單 #3–#7；載重箭頭位置僅示意（e 為所求）",
                   note="跨度 8 m 簡支；扭轉一端完全拘束、另一端自由；d = 45 cm（題文給）")


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
S_L, S_D, S_W = 800.0, 45.0, 20.0          # 梁長、有效深度（cm）、偏心載重 Wu（kgf/cm）
S_B, S_H, S_FC, S_PHI = 36.0, 50.0, 210.0, 0.75
S_ACP, S_PCP = S_B * S_H, 2 * (S_B + S_H)
S_PTTH = S_PHI * 0.27 * _m.sqrt(S_FC) * S_ACP ** 2 / S_PCP     # kgf·cm
S_EMAX = S_PTTH / (S_W * (S_L - S_D))
S_EFACE = S_PTTH / (S_W * S_L)
TFM = 1e-5


def fig2_torque():
    W, H = 860, 560
    mL, mR, mB = 92, 250, 74
    sx = (W - mL - mR) / S_L
    cv = Canvas(W, H, sx=sx, ox=mL, oy=mB, bg="#FFFFFF")
    tA = S_W * S_EMAX * S_L * TFM
    k = 270 / tA / sx
    cv.text_px(W / 2, 32, f"圖 2　扭矩圖（e = e,max = {S_EMAX:.2f} cm）與扭力忽略門檻", 17, C["text"], weight="700")
    cv.text_px(W / 2, 56, "一端拘束、一端自由：均佈扭矩 tu = Wu·e 全部由拘束端承擔，T(x) 由 tuL 線性降到 0", 12.5, C["muted"])
    yb = 270 / sx + 112 / sx
    cv.fixed_support((0, yb), ang=90, size=26)
    cv.line((0, yb), (S_L, yb), C["member"], 8, cap="butt")
    for i in range(9):
        x = S_L * (i + 0.5) / 9
        cv.moment_arrow((x, yb), r=13, ccw=True, color=C["load"], w=2.2, span=250, start=120)
    cv.text_px(cv.X(0) + 34, cv.Y(yb) + 30, "拘束端", 12.5, C["muted"], "start")
    cv.text_px(cv.X(S_L), cv.Y(yb) + 30, "自由端（無扭轉反力）", 12.5, C["muted"], "end")
    cv.text_px(cv.X(S_L) + 14, cv.Y(yb), f"tu = Wu·e = {S_W:.0f}e kgf·cm/cm", 13, C["load"], "start", weight="700")
    n = 41
    xs = [S_L * i / (n - 1) for i in range(n)]
    cv.polygon([(0, 0)] + [(x, S_W * S_EMAX * (S_L - x) * TFM * k) for x in xs] + [(S_L, 0)], C["fill_s"], C["sfd"], 2.6)
    # 兩端拘束對照（灰虛線）
    cv.line((0, S_W * S_EMAX * S_L / 2 * TFM * k), (S_L / 2, 0), C["ghost"], 2.0, dash="6 4")
    cv.text_px(cv.X(S_L * 0.30), cv.Y(S_W * S_EMAX * S_L * 0.2 * TFM * k) + 22, "若兩端拘束：各承擔 tuL/2（本題不是）", 12, C["muted"], "start")
    cv.arrow((0, 0), (S_L * 1.04, 0), C["muted"], 1.6, 9)
    pt = S_PTTH * TFM
    cv.line((0, pt * k), (S_L, pt * k), C["compr"], 1.8, dash="7 5")
    cv.text_px(cv.X(S_L) + 12, cv.Y(pt * k), f"φTth = {pt:.3f} tf·m", 13, C["compr"], "start", weight="700")
    cv.line((S_D, 0), (S_D, yb), C["accent"], 1.6, dash="4 3")
    cv.dot((S_D, pt * k), 6.2, fill=C["load"])
    cv.text_px(cv.X(S_D) + 14, cv.Y(pt * k) - 22, f"x = d = {S_D:.0f} cm：Tu = φTth → e,max = {S_EMAX:.2f} cm", 13.5, C["load"], "start", weight="700")
    cv.dot((0, tA * k), 5.4, fill=C["muted"])
    cv.text_px(cv.X(0) + 12, cv.Y(tA * k) - 52, f"支承處 {tA:.3f} tf·m（若取此處：e = {S_EFACE:.2f} cm）", 12.5, C["muted"], "start")
    for xv in (0, 200, 400, 600, 800):
        cv.text_px(cv.X(xv), cv.Y(0) + 20, f"{xv:g}", 12, C["muted"])
    cv.text_px(W / 2, H - 22, f"φTth = 0.75 × 0.27√f'c · Acp²/pcp = {S_PTTH:,.0f} kgf·cm；臨界斷面 Tu = tu(L − d) = {S_W * (S_L - S_D):,.0f}e", 13, C["muted"])
    return cv.svg()


def check_solution():
    ok = [("phiTth kgf·cm", S_PTTH, 55278, 3), ("e_max cm", S_EMAX, 3.66, 0.005), ("e_face cm", S_EFACE, 3.45, 0.005)]
    for name, got, want, tol in ok:
        assert abs(got - want) <= tol, (name, got, want)
        print(f"  OK  {name:14s} 算得 {got:10.4f}  .md {want}")


FIGURES = [
    ("1-problem", fig1_problem, "把 e 量錯基準（應由斷面中心線量到載重作用線）"),
    ("2-torque", fig2_torque, "以為兩端各分 tuL/2；臨界斷面位置取錯"),
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
