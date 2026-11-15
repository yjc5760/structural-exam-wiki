#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2006-1 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2006-1-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2006-1.py [輸出目錄，預設 figs]
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2006-1"

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


P_B = 30.0          # 判讀 #3 梁寬（外緣）
P_D = 45.0          # 判讀 #1 受壓面（底面）至上方兩排拉力筋形心＝d
P_DP = 8.0          # 判讀 #2 底面至下排壓力筋中心＝d'
P_ROW = 5.0         # 上方兩排筋心距（考卷未標，示意）
P_H = P_D + P_ROW / 2 + 6.0   # 全深考卷未給：圖上高度僅示意


def fig1_problem():
    B, H = P_B, P_H
    cv = _pc(B, H)
    _prect(cv, 0, 0, B, H)
    _phoop(cv, 3.5, 3.5, B - 3.5, H - 3.5)
    _phook(cv, (3.5, 3.5), 45)
    xs = (6.5, B / 2, B - 6.5)
    for y in (P_D + P_ROW / 2, P_D - P_ROW / 2):       # 上方兩排 A_s（各 3 根）
        for x in xs:
            _pbar(cv, (x, y), 1.5)
    for x in xs:                                       # 下方一排 A'_s
        _pbar(cv, (x, P_DP), 1.5)
    cv.math((B / 2, P_D - P_ROW / 2 - 6), "A_{s}", 15)
    cv.math((B / 2, P_DP + 6), "A'_{s}", 15)
    cv.text((B / 2, H / 2 - 2), "#3 肋筋", 13, color=C["muted"])
    cv.dim((0, 0), (B, 0), f"{B:.0f} cm", off=34, label_off=16)
    cv.dim((B, 0), (B, P_D), f"{P_D:.0f} cm", off=40, label_off=30)
    cv.dim((0, P_DP), (0, 0), f"{P_DP:.0f} cm", off=36, label_off=26)
    return compose([cv], title=f"{TAG} 題目附圖（圖一重繪）",
                   sub="依題目正本判讀清單 #1–#5；全深考卷未給，圖上高度與兩排筋距為示意",
                   note="下方受壓；45 cm 量到兩排拉力筋形心（＝d）")


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
S_L, S_D, S_B = 450.0, 45.0, 30.0          # 懸臂長、有效深度、梁寬（cm）
S_FC, S_FY, S_ES, S_B1 = 280.0, 4200.0, 2.04e6, 0.85
S_AS, S_ASP, S_DP = 40.0, 24.0, 8.0        # cm², cm², cm
S_AV, S_PHI_V, S_PHI_M = 1.42, 0.75, 0.90  # #3 兩肢；剪力、撓曲 φ
TF = 1e-3


def _solve():
    k1 = 0.85 * S_FC * S_B * S_B1
    k2 = S_ASP * S_ES * 0.003
    bq = k2 - S_ASP * 0.85 * S_FC - S_AS * S_FY
    c = (-bq + _m.sqrt(bq * bq + 4 * k1 * k2 * S_DP)) / (2 * k1)
    a = S_B1 * c
    fsp = S_ES * 0.003 * (c - S_DP) / c
    mn = 0.85 * S_FC * a * S_B * (S_D - a / 2) + S_ASP * (fsp - 0.85 * S_FC) * (S_D - S_DP)
    wu = 2 * S_PHI_M * mn / S_L ** 2
    vc = 0.53 * _m.sqrt(S_FC) * S_B * S_D
    r = dict(c=c, et=0.003 * (S_D - c) / c, mn=mn, wu=wu, vc=vc)
    for key, x in (("d", S_D), ("face", 0.0)):
        vu = wu * (S_L - x)
        vs = vu / S_PHI_V - vc
        r[key] = (vu, vs, S_AV * S_FY * S_D / vs)
    return r


R = _solve()


def fig2_shear():
    W, H = 860, 590
    mL, mR, mB = 92, 250, 74
    sx = (W - mL - mR) / S_L
    cv = Canvas(W, H, sx=sx, ox=mL, oy=mB, bg="#FFFFFF")
    vmax = R["face"][0] * TF
    k = 290 / vmax / sx                      # 1 tf → 模型單位
    cv.text_px(W / 2, 32, "圖 2　懸臂剪力圖與臨界斷面：設計剪力取距支承面 d", 17, C["text"], weight="700")
    cv.text_px(W / 2, 56, "橫軸：距固定端支承面距離（cm）　縱軸：設計剪力 Vu（tf）；wu 由 φMn = wuL²/2 反推", 12.5, C["muted"])
    # 梁示意
    yb = 290 / sx + 120 / sx
    cv.fixed_support((0, yb), ang=90, size=26)
    cv.udl((0, yb), (S_L, yb), 34 / sx, n=13)
    cv.line((0, yb), (S_L, yb), C["member"], 8, cap="butt")
    cv.text_px(cv.X(S_L) + 14, cv.Y(yb) - 26, f"wu = {R['wu'] * 100 * TF:.2f} tf/m", 13.5, C["load"], "start", weight="700")
    cv.text_px(cv.X(S_L) + 14, cv.Y(yb) - 6, "（頂面載重、無集中載重）", 12, C["muted"], "start")
    cv.dim((0, yb), (S_D, yb), f"d = {S_D:.0f}", off=24, label_off=14)
    # SFD
    n = 46
    xs = [S_L * i / (n - 1) for i in range(n)]
    cv.polygon([(0, 0)] + [(x, R["wu"] * (S_L - x) * TF * k) for x in xs] + [(S_L, 0)], C["fill_s"], C["sfd"], 2.6)
    cv.arrow((0, 0), (S_L * 1.04, 0), C["muted"], 1.6, 9)
    pvc = S_PHI_V * R["vc"] * TF
    cv.line((0, pvc * k), (S_L, pvc * k), C["compr"], 1.8, dash="7 5")
    cv.text_px(cv.X(S_L) + 12, cv.Y(pvc * k), f"φVc = {pvc:.2f} tf", 13, C["compr"], "start", weight="700")
    # 臨界斷面
    vd, vsd, sd = R["d"]
    cv.line((S_D, 0), (S_D, yb), C["accent"], 1.6, dash="4 3")
    cv.dot((S_D, vd * TF * k), 6.2, fill=C["load"])
    cv.text_px(cv.X(S_D) + 14, cv.Y(vd * TF * k) - 4, f"x = d：Vu = {vd * TF:.2f} tf → s = {sd:.1f} cm（本解）", 13.5, C["load"], "start", weight="700")
    vf, vsf, sf = R["face"]
    cv.dot((0, vf * TF * k), 5.4, fill=C["muted"])
    cv.text_px(cv.X(0) + 12, cv.Y(vf * TF * k) - 20, f"支承面 {vf * TF:.2f} tf → s = {sf:.1f} cm（對照，偏保守）", 12.5, C["muted"], "start")
    for xv in (0, 100, 200, 300, 400):
        cv.text_px(cv.X(xv), cv.Y(0) + 20, f"{xv:g}", 12, C["muted"])
    for yv in (0, 10, 20):
        cv.text_px(cv.X(0) - 12, cv.Y(yv * k), f"{yv:g}", 12, C["muted"], "end")
    cv.text_px(W / 2, H - 22, f"c = {R['c']:.2f} cm、εt = {R['et']:.5f} ≥ 0.005 → φ = 0.90；"
               f"Vs = Vu/φ − Vc = {vsd * TF:.2f} tf，s = Av fy d / Vs = {sd:.1f} cm", 13, C["muted"])
    return cv.svg()


def check_solution():
    ok = [("c cm", R["c"], 16.30, 0.01), ("wu kgf/cm", R["wu"], 56.20, 0.02),
          ("Vu@d kgf", R["d"][0], 22760, 6), ("s@d cm", R["d"][2], 14.6, 0.05),
          ("s@face cm", R["face"][2], 12.3, 0.05), ("phiMn tf·m", S_PHI_M * R["mn"] * 1e-5, 56.90, 0.01)]
    for name, got, want, tol in ok:
        assert abs(got - want) <= tol, (name, got, want)
        print(f"  OK  {name:12s} 算得 {got:10.4f}  .md {want}")


FIGURES = [
    ("1-problem", fig1_problem, "把 45 cm 讀成全深（再扣 8 cm 得 d＝37）"),
    ("2-shear", fig2_shear, "臨界斷面一律取固定端面；把 45 cm 當全深"),
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
