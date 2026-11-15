#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2018-1 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2018-1-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2018-1.py [輸出目錄，預設 figs]
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2018-1"

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


P_B = 50.0                # 判讀 #2 寬
P_D, P_BOT = 43.0, 7.0    # 判讀 #2／#3：頂面至下排筋心 43、下排筋心至底面 7
P_H = P_D + P_BOT
P_CC = 4.0                # 判讀 #4 淨保護層（量到箍筋外緣）
P_DBS = 1.27              # D13 箍筋


def fig1_problem():
    B, H = P_B, P_H
    cv = _pc(B, H, t=80)
    _prect(cv, 0, 0, B, H)
    c = P_CC + P_DBS / 2
    _phoop(cv, c, c, B - c, H - c)
    _phook(cv, (c, H - c), -45, 3.5)
    xs = [P_BOT + i * (B - 2 * P_BOT) / 3 for i in range(4)]   # 縱筋號數與間距考卷未標（示意）
    for x in xs:
        _pbar(cv, (x, P_BOT), 1.7)
        _pbar(cv, (x, H - P_BOT), 1.7)
    # 內部 2 支繫筋（判讀 #1：端部單支彎鉤，非閉合）
    for x, top, bot in ((xs[1] - 2.2, 135, 135), (xs[2] + 2.2, 90, 135)):
        cv.line((x, c), (x, H - c), C["member"], 3.0)
        cv.line((x, H - c), (x + (3.6 if top == 135 else -4.5), H - c - (3.6 if top == 135 else 0)), C["member"], 3.0)
        cv.line((x, c), (x - 3.6, c + 3.6), C["member"], 3.0)
    yl = H / 2
    cv.line((c, yl), (B + 6, yl), C["muted"], 1.2)
    cv.text((B + 7, yl), "4-D13", 14, anchor="start")
    cv.dim((0, H), (B, H), f"{B:.0f} cm", off=-30, label_off=-16)
    cv.dim((0, H), (0, P_BOT), f"{P_D:.0f} cm", off=36, label_off=30)
    cv.dim((0, P_BOT), (0, 0), f"{P_BOT:.0f} cm", off=36, label_off=30)
    cv.dim((B, 0), (B, P_CC), f"{P_CC:.0f} cm", off=40, label_off=26)
    cv.dim((B - P_CC, 0), (B, 0), f"{P_CC:.0f} cm", off=34, label_off=16)
    return compose([cv], title=f"{TAG} 題目附圖重繪",
                   sub="依題目正本判讀清單 #1–#5；縱筋號數與位置考卷未標（示意）",
                   note="外圍閉合箍＋2 支繫筋＝4 肢（抗剪 4 肢、抗扭只計外圍箍）；h = 50、d = 43 cm")


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
import math as _m
S_FC, S_FYT, S_PHI, S_AB = 280.0, 2800.0, 0.75, 1.27
S_TU, S_VU = 400000.0, 20000.0
S_C = P_CC + P_DBS / 2
S_X1 = P_B - 2 * S_C
S_AO = 0.85 * S_X1 ** 2
S_VC = 0.53 * _m.sqrt(S_FC) * P_B * P_D
S_ATS = S_TU / (2 * S_PHI * S_AO * S_FYT)
S_AVS = (S_VU / S_PHI - S_VC) / (S_FYT * P_D)
S_OUT4 = S_ATS + S_AVS / 4                 # 本解：抗剪 4 肢
S_OUT2 = S_ATS + S_AVS / 2                 # 對照：抗剪只計外圍 2 肢


def fig2_legs():
    W, H = 1080, 560
    cv = Canvas(W, H, sx=1, bg="#FFFFFF")
    cv.text_px(W / 2, 32, "圖 2　外圍箍每一肢同時扛扭力與剪力：需求要疊加在同一肢", 17, C["text"], weight="700")
    cv.text_px(W / 2, 56, "抗剪 4 肢（外圍箍 2 肢＋繫筋 2 肢）分攤 Av/s；抗扭只靠外圍閉合箍（單位 cm²/cm）", 12.5, C["muted"])
    s = 4.0
    ox, oy = 50, 120
    cv.rect_px(ox, oy, P_B * s, P_H * s, "#EDF1F6", rx=2, stroke=C["member"], sw=2)
    hx, hy, hw = ox + S_C * s, oy + S_C * s, S_X1 * s
    cv.rect_px(hx, hy, hw, hw, "none", rx=1, stroke=C["bmd"], sw=4)
    for x in (hx + hw / 3, hx + 2 * hw / 3):
        _pl(cv, x, hy, x, hy + hw, C["sfd"], 3.6)
    cv.text_px(hx, hy + hw + 24, "外圍箍肢", 12.5, C["bmd"], weight="700")
    cv.text_px(hx + hw / 2, hy + hw + 24, "繫筋", 12.5, C["sfd"], weight="700")
    cv.text_px(ox + P_B * s / 2, oy - 14, f"{P_B:.0f} × {P_H:.0f} cm（h = 43 + 7）", 12.5, C["muted"])
    rows = [
        ("外圍箍每肢（本解）", "At/s ＋ Av/4s",
         [(S_ATS, C["bmd"], f"扭 {S_ATS:.4f}"), (S_AVS / 4, C["sfd"], f"{S_AVS / 4:.4f}")],
         [], f"s ≤ {S_AB:.2f}/{S_OUT4:.4f} = {S_AB / S_OUT4:.1f} cm ← 控制"),
        ("繫筋每肢", "只有 Av/4s",
         [(S_AVS / 4, C["sfd"], "")], [], f"Av/4s = {S_AVS / 4:.4f} → s ≤ {S_AB / (S_AVS / 4):.0f} cm（不控制）"),
        ("對照：抗剪只計 2 肢", "At/s ＋ Av/2s",
         [(S_ATS, C["ghost"], f"扭 {S_ATS:.4f}"), (S_AVS / 2, C["muted"], f"剪 {S_AVS / 2:.4f}")],
         [], f"s ≤ {S_AB / S_OUT2:.1f} cm"),
    ]
    _stack_rows(cv, 520, 140, 300, S_OUT2 * 1.05, rows, row_h=104, bar_h=30)
    cv.text_px(W / 2, H - 48, f"舊解把扭力、剪力各算一個間距再取小（等於沒疊加），又漏了 Ao = 0.85Aoh；"
               f"疊加後外圍箍每肢需 {S_OUT4:.4f}", 13, C["muted"])
    cv.text_px(W / 2, H - 24, f"Vs = Vu/φ − Vc = {int(S_VU / S_PHI - S_VC):,} kgf → Av/s = {S_AVS:.5f}；"
               f"At/s = Tu / (2φAo fyt) = {S_ATS:.5f}", 13, C["muted"])
    return cv.svg()


def check_solution():
    ok = [("Ao", S_AO, 1410.1, 0.1), ("At/s", S_ATS, 0.06754, 1e-5), ("Av/s", S_AVS, 0.06311, 1e-5),
          ("s4", S_AB / S_OUT4, 15.24, 0.01), ("s2", S_AB / S_OUT2, 12.8, 0.05)]
    for name, got, want, tol in ok:
        assert abs(got - want) <= tol, (name, got, want)
        print(f"  OK  {name:6s} 算得 {got:10.5f}  .md {want}")


FIGURES = [
    ("1-problem", fig1_problem, "把 43 cm 讀成全深；把 4-D13 讀成角隅縱筋或 4 支閉合箍"),
    ("2-legs", fig2_legs, "扭剪各算間距取小、沒疊加到同一肢"),
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
