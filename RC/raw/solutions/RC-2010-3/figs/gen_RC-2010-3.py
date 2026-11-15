#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2010-3 解題圖解產生腳本（2026-11-15 圖解補繪）

數值全由常數區現算，檔尾對解析正本 §4 公佈值 assert。
用法：python figs/gen_RC-2010-3.py [輸出目錄，預設 figs]
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2010-3"

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
S_BW, S_D, S_H, S_FC, S_PHI = 40.0, 52.0, 60.0, 280.0, 0.75
S_AG, S_BD = S_BW * S_H, S_BW * S_D
S_SQ = _m.sqrt(S_FC)
S_NUS = (0.0, 30000.0, -30000.0)               # (a)(b)(c)，壓為正（kgf）
TF = 1e-3


def vc_now(nu):
    """現行規範簡化式 [0.53√f'c + Nu/6Ag]bwd（≥ 0）"""
    return max(0.0, (0.53 * S_SQ + nu / (6 * S_AG)) * S_BD)


def vc_old(nu):
    """舊規範（本庫 2026-11-15 前舊解）：壓 0.53(1+Nu/140Ag)、拉 0.53(1+Nu/35Ag)"""
    f = 140.0 if nu >= 0 else 35.0
    return max(0.0, 0.53 * (1 + nu / (f * S_AG)) * S_SQ * S_BD)


def phi_vc_tf(f, nu):
    """同 §4 的進位程序：Vc 先取整數 kgf，再乘 φ 取整數 kgf，最後換 tf"""
    return round(S_PHI * round(f(nu))) * TF


def crack_incl(nu):
    """斜裂縫與梁軸夾角（度）：開裂時 τ 取 Vc/bwd、σx = −Nu/Ag（拉為正），裂縫垂直於主拉應力"""
    tau = vc_now(nu) / S_BD
    sx = -nu / S_AG
    th1 = 0.5 * _m.degrees(_m.atan2(2 * tau, sx))
    return 90.0 - th1


def fig1_vc_axial():
    W, H = 600, 470
    # 左：φVc–Nu
    a = Canvas(W, H, sx=1, bg="#FFFFFF")
    a.panel("φVc 隨設計軸力 Nu 的變化", "壓為正；實線＝現行規範，灰虛線＝舊規範（舊解）")
    x0, x1, yb, yt = 80, W - 40, H - 70, 100
    nmin, nmax, vmax = -60.0, 60.0, 24.0
    X = lambda n: x0 + (n - nmin) / (nmax - nmin) * (x1 - x0)
    Y = lambda v: yb - v / vmax * (yb - yt)
    _pl(a, x0, yb, x1, yb, C["muted"], 1.4)
    _pl(a, X(0), yb, X(0), yt - 10, C["muted"], 1.2, dash="3 3")
    for f, col, w, dash in ((vc_now, C["bmd"], 3.0, None), (vc_old, C["ghost"], 2.4, "6 4")):
        pts = [(X(n), Y(S_PHI * f(n * 1000) * TF)) for n in [nmin + i * (nmax - nmin) / 60 for i in range(61)]]
        for (p, q) in zip(pts, pts[1:]):
            _pl(a, p[0], p[1], q[0], q[1], col, w, dash)
    lab = {0.0: "(a)", 30000.0: "(b)", -30000.0: "(c)"}
    for nu in S_NUS:
        v = phi_vc_tf(vc_now, nu)
        vo = phi_vc_tf(vc_old, nu)
        a.dot((X(nu * TF), a.h - Y(v)), 5.8, fill=C["bmd"])
        a.text_px(X(nu * TF), Y(v) - 16, f"{lab[nu]} {v:.2f}", 12.5, C["bmd"], weight="700")
        if abs(vo - v) > 0.05:
            a.dot((X(nu * TF), a.h - Y(vo)), 4.6, fill=C["ghost"])
            a.text_px(X(nu * TF), Y(vo) + 18, f"舊 {vo:.2f}", 11.5, C["muted"])
    for n in (-60, -30, 0, 30, 60):
        a.text_px(X(n), yb + 18, f"{n:g}", 12, C["muted"])
    for v in (0, 10, 20):
        a.text_px(x0 - 10, Y(v), f"{v:g}", 12, C["muted"], "end")
    a.text_px((x0 + x1) / 2, yb + 40, "Nu（tf）", 12.5, C["muted"])
    a.text_px(x0 - 10, yt - 22, "φVc（tf）", 12.5, C["muted"], "start")
    # 右：裂縫方向
    b = Canvas(W, H, sx=1, bg="#FFFFFF")
    b.panel("腹部單元與斜裂縫方向（開裂時示意）", "τ 取 Vc/bwd、σx = Nu/Ag；裂縫垂直於主拉應力")
    for i, (nu, name) in enumerate(((30000.0, "(b) 軸壓"), (0.0, "(a) 無軸力"), (-30000.0, "(c) 軸拉"))):
        cx, cy, s = 105 + i * 195, 250, 46
        b.rect_px(cx - s, cy - s, 2 * s, 2 * s, "#EDF1F6", rx=3, stroke=C["member"], sw=1.6)
        if nu > 0:
            b.arrow((cx - s - 34, b.h - cy), (cx - s - 4, b.h - cy), C["compr"], 2.4, 9)
            b.arrow((cx + s + 34, b.h - cy), (cx + s + 4, b.h - cy), C["compr"], 2.4, 9)
        elif nu < 0:
            b.arrow((cx - s - 4, b.h - cy), (cx - s - 34, b.h - cy), C["tension"], 2.4, 9)
            b.arrow((cx + s + 4, b.h - cy), (cx + s + 34, b.h - cy), C["tension"], 2.4, 9)
        al = _m.radians(crack_incl(nu))
        L = s * 1.25
        _pl(b, cx - L * _m.cos(al), cy + L * _m.sin(al), cx + L * _m.cos(al), cy - L * _m.sin(al), C["load"], 3.4)
        b.text_px(cx, cy + s + 34, name, 13.5, C["text"], weight="700")
        b.text_px(cx, cy + s + 56, f"裂縫約 {crack_incl(nu):.0f}°", 13, C["load"], weight="700")
    b.text_px(W / 2, H - 52, "軸壓 → 裂縫較平緩、開裂較晚；軸拉 → 裂縫較陡、開裂較早", 13, C["muted"])
    return compose([a, b], title="圖 1　軸力對混凝土剪力強度與斜裂縫的影響",
                   sub="(a) Nu = 0、(b) 軸壓 30 tf、(c) 軸拉 30 tf；bw = 40、d = 52、h = 60 cm、f'c = 280",
                   note="現行式對壓、拉採對稱加法修正 Nu/6Ag；舊式拉力折減較陡（35Ag），故 (c) 新舊差最大")


def check_solution():
    ok = [("phiVc a tf", S_PHI * vc_now(0) * TF, 13.83, 0.006), ("phiVc b tf", S_PHI * vc_now(30000) * TF, 17.08, 0.006),
          ("phiVc c tf", S_PHI * vc_now(-30000) * TF, 10.59, 0.006),
          ("old b tf", S_PHI * vc_old(30000) * TF, 15.07, 0.006), ("old c tf", S_PHI * vc_old(-30000) * TF, 8.89, 0.006)]
    for name, got, want, tol in ok:
        assert abs(got - want) <= tol, (name, got, want)
        print(f"  OK  {name:12s} 算得 {got:10.4f}  .md {want}")
    assert crack_incl(30000) < 45 < crack_incl(-30000)


FIGURES = [
    ("1-vc-axial", fig1_vc_axial, "軸壓／軸拉的裂縫角度寫反；沿用舊規範式"),
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
