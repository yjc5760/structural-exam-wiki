#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2011-4 解題圖解產生腳本（2026-11-15 圖解補繪）

數值全由常數區現算，檔尾對解析正本 §4 公佈值 assert。
用法：python figs/gen_RC-2011-4.py [輸出目錄，預設 figs]
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2011-4"

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
S_B, S_H, S_D, S_FC, S_FYT = 35.0, 60.0, 53.0, 280.0, 2800.0
S_AB, S_DB, S_S, S_CC, S_PHI = 1.267, 1.27, 8.0, 4.0, 0.75
S_SQ = _m.sqrt(S_FC)
S_ACP, S_PCP = S_B * S_H, 2 * (S_B + S_H)
S_TCR = 1.06 * S_SQ * S_ACP ** 2 / S_PCP                   # kgf·cm（Tu = Tcr）
S_C = S_CC + S_DB / 2
S_XOH, S_YOH = S_B - 2 * S_C, S_H - 2 * S_C
S_AO = 0.85 * S_XOH * S_YOH
S_ATS = S_TCR / (2 * S_PHI * S_AO * S_FYT)                 # 每肢扭力需求
S_ABS = S_AB / S_S                                         # 每肢供給
S_AV2S = S_ABS - S_ATS                                     # 每肢剩給剪力
S_VS = 2 * S_AV2S * S_FYT * S_D
S_VC = 0.53 * S_SQ * S_B * S_D
S_VU = S_PHI * (S_VC + S_VS)
S_OLD_REQ = 0.487 / 2          # 舊解答案 60.4 tf 所需 (Av+2At)/s 的每肢值（§5 對照表）


def fig1_legs():
    W, H = 1060, 470
    cv = Canvas(W, H, sx=1, bg="#FFFFFF")
    cv.text_px(W / 2, 32, "圖 1　一根兩肢箍筋要同時扛扭力與剪力：逐肢分配", 17, C["text"], weight="700")
    cv.text_px(W / 2, 56, "每一肢都承擔 At/s（扭力）＋ Av/2s（剪力）；兩肢合計的供給是 2Ab/s，不是 4Ab/s", 12.5, C["muted"])
    # 斷面示意（像素）
    s = 3.4
    ox, oy = 60, 110
    cv.rect_px(ox, oy, S_B * s, S_H * s, "#EDF1F6", rx=2, stroke=C["member"], sw=2)
    hx0, hy0 = ox + S_C * s, oy + S_C * s
    cv.rect_px(hx0, hy0, S_XOH * s, S_YOH * s, "none", rx=1, stroke=C["member"], sw=3)
    for x, lab in ((hx0, "左肢"), (hx0 + S_XOH * s, "右肢")):
        _pl(cv, x, hy0, x, hy0 + S_YOH * s, C["bmd"], 5)
        cv.text_px(x, hy0 + S_YOH * s + 22, lab, 12.5, C["bmd"], weight="700")
    cv.text_px(ox + S_B * s / 2, oy - 14, f"{S_B:.0f} × {S_H:.0f} cm、#4@{S_S:.0f}", 12.5, C["muted"])
    cv.text_px(ox + S_B * s / 2, oy + S_H * s / 2, "兩肢閉合箍", 12, C["muted"])
    rows = [
        ("本解：每肢需求", f"Vu = {S_VU / 1000:.1f} tf 時剛好用滿",
         [(S_ATS, C["bmd"], f"扭 {S_ATS:.5f}"), (S_AV2S, C["sfd"], f"剪 {S_AV2S:.5f}")],
         [(S_ABS, C["load"], f"每肢供給 Ab/s = {S_ABS:.4f}")], "箍筋控制"),
        ("舊解答案 60.4 tf", "所需 (Av+2At)/2s",
         [(S_OLD_REQ, C["ghost"], f"{S_OLD_REQ:.4f}")],
         [(S_ABS, C["load"], "真實供給"), (2 * S_ABS, C["muted"], "舊解誤算（4Ab/s ÷ 2）")], "超過真實供給（不足）"),
    ]
    _stack_rows(cv, 470, 150, 380, 2 * S_ABS * 1.04, rows, row_h=150, bar_h=30)
    cv.text_px(W / 2, H - 24, f"Tcr = {S_TCR / 1e5:.3f} tf·m → At/s = {S_ATS:.5f}；剩 {S_AV2S:.5f}/肢給剪力 → Vs = {S_VS / 1000:.2f} tf、"
               f"φ(Vc+Vs) = {S_VU / 1000:.1f} tf（單位 cm²/cm）", 13, C["muted"])
    return cv.svg()


def check_solution():
    ok = [("Tcr kgf·cm", S_TCR, 411680, 30), ("At/s", S_ATS, 0.08835, 1e-5), ("Av/s", 2 * S_AV2S, 0.14006, 2e-5),
          ("Vs kgf", S_VS, 20785, 5), ("Vu kgf", S_VU, 27928, 6)]
    for name, got, want, tol in ok:
        assert abs(got - want) <= tol, (name, got, want)
        print(f"  OK  {name:12s} 算得 {got:12.5f}  .md {want}")


FIGURES = [
    ("1-legs", fig1_legs, "兩肢箍筋供給算成 4Ab/s，重複計算"),
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
