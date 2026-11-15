#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2008-1 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2008-1-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2008-1.py [輸出目錄，預設 figs]
（2026-11-15，RC-U3-1／U3-2 題目正本推廣・批 1）
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2008-1"
PW, PH = 560, 420          # 各子圖畫布尺寸（px，compose 要求相同）


def _rect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    if fill:
        cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _bar(cv, p, r, fill=None):
    cv.circle(p, r, fill=fill or C["member"], stroke=C["member"], w=1.2)


# ── 判讀清單數值（題目正本 §4）──
L_CANT = 5.0                     # #4 懸臂長 5 m（固定面至 B）
B = 40.0                         # #3 梁寬
C_T, MID, C_B = 10.0, 50.0, 10.0 # #1 尺寸鏈：頂面→頂筋 10、頂筋→底筋 50、底筋→底面 10
H = C_T + MID + C_B              # #1 全深 70
R = 1.4                          # 鋼筋半徑（考卷未給號數，示意）


def panel_elev():
    cv = Canvas(PW, PH, sx=78, ox=70, oy=170)
    hb = 0.30
    _rect(cv, 0, 0, L_CANT, hb)
    cv.support((0, hb / 2), "fixed", ang=90, size=34)    # #4 A 端固定
    cv.arrow((L_CANT, hb + 1.45), (L_CANT, hb + 0.04), C["load"], 3.2)   # #5 B 端集中載重
    cv.math((L_CANT - 0.12, hb + 1.62), "P = 2 tf", 14, color=C["load"], anchor="end")
    cv.text((0.18, -0.32), "A", 15, anchor="start")
    cv.text((L_CANT - 0.1, -0.32), "B", 15, anchor="end")
    cv.text((L_CANT / 2, hb + 0.45), "自重另計（與 P 同時、持續一年）", 12, color=C["muted"])
    cv.dim((0, 0), (L_CANT, 0), "5 m", off=62, label_off=14)
    cv.text((L_CANT / 2, -1.55), "懸臂梁立面", 13, color=C["muted"])
    return cv


def panel_sec():
    cv = Canvas(PW, PH, sx=4.2, ox=160, oy=44)
    _rect(cv, 0, 0, B, H)
    c = 6.0                                              # 箍筋位置（考卷未標，示意）
    cv.poly([(c, c), (B - c, c), (B - c, H - c), (c, H - c), (c, c)], C["member"], 2.2)
    yt, yb = H - C_T, C_B
    for x in (c + 3, B / 2, B - c - 3):
        _bar(cv, (x, yt), R)                             # #2 頂部 3 根 A_s（拉）
    for x in (c + 3, B - c - 3):
        _bar(cv, (x, yb), R)                             # #2 底部 2 根 A'_s（壓）
    cv.math((B / 2, yt - 5.5), "A_{s} = 50 cm^{2}", 14)
    cv.math((B / 2, yb + 5.5), "A'_{s} = 20 cm^{2}", 14)
    cv.dim((0, H), (B, H), "40 cm", off=-30, label_off=-14)
    cv.dim((B, H), (B, yt), "10 cm", off=-34, label_off=-30)
    cv.dim((B, yt), (B, yb), "50 cm", off=-34, label_off=-30)
    cv.dim((B, yb), (B, 0), "10 cm", off=-34, label_off=-30)
    cv.text((B / 2, -7), "梁斷面（全深 10＋50＋10＝70 cm）", 13, color=C["muted"])
    return cv


def fig1_problem():
    return compose([panel_elev(), panel_sec()], title=f"{TAG} 題目附圖（圖一重繪）",
                   sub="依題目正本判讀清單 #1–#5；箍筋位置、筋徑、梁立面高度為示意",
                   note="50 cm 為頂筋中心至底筋中心；上下各 10 cm 量到筋心 → 全深 70 cm")


FIGURES = [("1-problem", fig1_problem, "把 50 cm 讀成全深（漏加上下各 10 cm）")]


# ══ 解題圖解（2026-11-15 圖解補繪 DIAG-RC-U3-B1；數值由常數現算，檔尾對 §4 assert）══
BB, HH, DD_, DP_, ASX, ASP_, NN, EC_ = 40.0, 70.0, 60.0, 10.0, 50.0, 20.0, 8.0, 2.04e6 / 8
LC, PB, WSW = 500.0, 2000.0, 2400 * 0.40 * 0.70 / 100
IG_ = BB * HH ** 3 / 12; MCR_ = 2 * math.sqrt(280) * IG_ / (HH / 2)
_qa, _qb = BB / 2, (NN - 1) * ASP_ + NN * ASX
_qc = -((NN - 1) * ASP_ * DP_ + NN * ASX * DD_)
KD_ = (-_qb + math.sqrt(_qb ** 2 - 4 * _qa * _qc)) / (2 * _qa)
ICR_ = BB * KD_ ** 3 / 3 + (NN - 1) * ASP_ * (KD_ - DP_) ** 2 + NN * ASX * (DD_ - KD_) ** 2
MA_ = PB * LC + WSW * LC ** 2 / 2
_t = 2 / 3 * MCR_ / MA_
IE_ = min(IG_, ICR_ / (1 - _t * _t * (1 - ICR_ / IG_)))
DI = PB * LC ** 3 / (3 * EC_ * IE_) + WSW * LC ** 4 / (8 * EC_ * IE_)
LAM = 1.4 / (1 + 50 * ASP_ / (BB * DD_))
DTOT = DI * (1 + LAM)


def panel_csec():
    cv = Canvas(PW, PH, sx=4.6, ox=PW / 2 - 10, oy=40)
    cv.panel("固定端斷面（負彎矩：頂拉、底壓）", None)
    _rect(cv, -BB / 2, 0, BB / 2, HH, fill="#EDF1F6", w=2.2)
    _rect(cv, -BB / 2, 0, BB / 2, KD_, fill="rgba(29,78,216,0.18)", stroke="none", w=0)
    cv.line((-BB / 2 - 3, KD_), (BB / 2 + 3, KD_), C["compr"], 1.6, dash="6 4")
    for k in range(3):
        _bar(cv, (-12 + 12 * k, HH - 10), 2.0, C["tension"])
    for k in range(2):
        _bar(cv, (-12 + 24 * k, DP_), 1.6, C["compr"])
    cv.text((0, HH - 4), f"A_{{s}}＝{ASX:.0f}（受拉）", 12, C["tension"])
    cv.text((0, DP_ + 5), f"A'_{{s}}＝{ASP_:.0f}（受壓）", 12, C["compr"])
    cv.text((0, KD_ / 2 - 3), "壓力區", 12, C["compr"])
    cv.dim((BB / 2, 0), (BB / 2, KD_), f"kd {KD_:.2f}", off=14, label_off=32)
    cv.dim((BB / 2, 0), (BB / 2, DD_), "d 60", off=70, label_off=22)
    cv.dim((-BB / 2, 0), (-BB / 2, DP_), "10", off=-14, label_off=-16)
    cv.dim((-BB / 2, DP_), (-BB / 2, HH - 10), "50", off=-14, label_off=-16)
    cv.dim((-BB / 2, HH - 10), (-BB / 2, HH), "10", off=-14, label_off=-16)
    cv.dim((-BB / 2, 0), (-BB / 2, HH), "70", off=-52, label_off=-16)
    cv.text((-BB / 2 - 15, HH + 4), "全深 h", 12, C["muted"], anchor="end")
    cv.text((0, -5.5), "kd 由壓力緣（底面）量起", 12, C["muted"])
    return cv


def panel_cant():
    cv = Canvas(PW, PH, sx=0.86, ox=60, oy=PH / 2 + 30)
    cv.panel("懸臂撓度（放大示意）", f"I_{{e}}（固定端）＝{IE_:,.0f} cm^{{4}}")
    cv.line((0, 0), (LC, 0), C["ghost"], 6)
    sc = 60.0                                     # 撓度放大倍率（僅形狀示意）
    pts = []
    for i in range(51):
        x = LC * i / 50
        v = (PB * x * x * (3 * LC - x) / 6 + WSW * x * x * (6 * LC ** 2 - 4 * LC * x + x * x) / 24) / (EC_ * IE_)
        pts.append((x, -v * sc))
    cv.poly(pts, C["deform"], 4)
    cv.fixed_support((0, 0), ang=0, size=26)
    cv.arrow((LC, 70), (LC, 8), C["load"], 3, 10)
    cv.text((LC, 82), "P＝2 tf", 13, C["load"])
    cv.text((LC / 2, 46), f"自重 w＝{WSW/10:.3f} tf/m", 12, C["load"])
    yb = -DI * sc
    cv.text((LC - 10, yb - 24), f"δ_{{i}}＝{DI:.3f} cm", 13, C["deform"], anchor="end")
    cv.text((LC - 10, yb - 50), f"λ_{{Δ}}＝1.4/(1+50ρ')＝{LAM:.3f}", 12.5, C["text"], anchor="end")
    cv.text((LC - 10, yb - 76), f"1 年總撓度 δ_{{i}}(1+λ_{{Δ}})＝{DTOT:.2f} cm", 13.5, C["bmd"], anchor="end", weight="700")
    cv.text((0, -36), "A（固定）", 12, C["muted"], anchor="start")
    cv.text((LC, -16), "B", 13, C["muted"])
    return cv


def fig2_section_cant():
    return compose([panel_csec(), panel_cant()], title=f"{TAG} 圖 2　懸臂梁開裂斷面與一年總撓度",
                   sub="數值取自解析 §4（Ec＝Es/n、n＝8；自重以全深 70 cm 計）",
                   note="攔：全深讀成 50；把底部當受拉；ρ' 用頂筋")


def check_solution():
    for name, got, want, tol in [("kd", KD_, 24.61, 0.006), ("Icr", ICR_, 729599, 80), ("Ma", MA_, 1840000, 1),
                                 ("Ie", IE_, 773515, 80), ("di", DI, 0.689, 0.0015), ("lam", LAM, 0.988, 0.0006),
                                 ("tot", DTOT, 1.37, 0.006)]:
        assert abs(got - want) <= tol, (name, got, want)
    print("check_solution：§4 對帳全過")


FIGURES.append(("2-section-cantilever", fig2_section_cant, "全深 70、頂拉底壓、kd 由底量起"))


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
