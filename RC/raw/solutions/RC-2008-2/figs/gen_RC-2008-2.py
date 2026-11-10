#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2008-2 矩形柱（b = 40、h = 56）・「拉力側應變 = 0」 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2008-2.md §1 給定的原始資料；c、a、各排應變與內力、P_n、M_n、
     c_b、M_b 及 φM_n 峰值全部由 section() 現算，檔尾對 §4 公佈值 assert。
  2. 改 §1 任一數字重跑，三張圖跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2008-2"

# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
B, H = 40.0, 56.0                 # b 垂直彎曲方向（原卷圖二上下 20+20）、h 沿 X 軸（8+20+20+8）
FC, FY, ES = 350.0, 4200.0, 2.04e6
A_BAR = 5.07                       # #8
ROWS = ((8.0, 4), (28.0, 2), (48.0, 2))   # (距壓力面, 根數)：原卷圖二右排 4、中排 2、左排 2
EPS_CU = 0.003

EPSY = FY / ES
BETA1 = max(0.65, min(0.85, 0.85 - 0.05 * (FC - 280) / 70))
D = ROWS[-1][0]
AST = sum(n for _, n in ROWS) * A_BAR
CB = EPS_CU * ES / (EPS_CU * ES + FY) * D
C_ZERO = D                          # 拉力側應變 = 0 → 中性軸落在最外層拉力筋
TF, TFM = 1e-3, 1e-5


def phi_of(et):
    if et >= 0.005:  return 0.90
    if et <= EPSY:   return 0.65
    return 0.65 + 0.25 * (et - EPSY) / (0.005 - EPSY)


def section(c):
    a = min(BETA1 * c, H)
    Cc = 0.85 * FC * a * B
    P, M = Cc, Cc * (H / 2 - a / 2)
    bars = []
    for d, n in ROWS:
        As = n * A_BAR
        eps = EPS_CU * (c - d) / c
        fs = max(-FY, min(FY, ES * eps))
        inside = d < a and fs > 0
        F = As * (fs - 0.85 * FC) if inside else As * fs
        P += F
        M += F * (H / 2 - d)
        bars.append(dict(d=d, n=n, As=As, eps=eps, fs=fs, F=F, inside=inside))
    et = EPS_CU * (D - c) / c
    return dict(c=c, a=a, Cc=Cc, bars=bars, Pn=P, Mn=M, et=et, phi=phi_of(et))


THIS = section(C_ZERO)
BAL = section(CB)
C_TC = EPS_CU / (EPS_CU + 0.005) * D          # ε_t = 0.005
TC = section(C_TC)


def curve(n=400):
    cs = [0.05 * (H * 6 / 0.05) ** (i / n) for i in range(n + 1)]
    cs += [CB, C_TC]                 # 兩個折點必須取樣到，否則峰值會被略過
    out = [section(c) for c in sorted(cs)]
    return [s for s in out if s["Pn"] >= 0]   # 只畫到純彎矩點，P < 0 不在本題範圍


CURVE = curve()
M_PEAK = max(CURVE, key=lambda s: s["Mn"])
PHIM_PEAK = max(CURVE, key=lambda s: s["phi"] * s["Mn"])


def c_at_zero_axial():
    lo, hi = 1.0, D
    for _ in range(300):
        m = (lo + hi) / 2
        if section(m)["Pn"] > 0: hi = m
        else:                    lo = m
    return m


C0 = c_at_zero_axial()
PURE_M = section(C0)
P0 = 0.85 * FC * (B * H - AST) + FY * AST      # 純軸壓


# ══════════════════════════════════════════════════════════
def _sec(cv):
    cv.polygon([(0, 0), (B, 0), (B, H), (0, H)], C["fill_m"], C["member"], 2.6)
    for d, n in ROWS:
        y = H - d
        for i in range(n):
            x = 6.0 + (B - 12.0) * i / (n - 1) if n > 1 else B / 2
            cv.dot((x, y), 6.0,
                   fill=C["member"], stroke="#FFFFFF", w=1.7)


def fig1_section():
    W, HH = 760, 560
    L, Rm, T, Bm = 96, 282, 88, 92
    sx = min((W - L - Rm) / B, (HH - T - Bm) / H)
    cv = Canvas(W, HH, sx=sx, ox=L, oy=Bm, bg="#FFFFFF")
    _sec(cv)
    cv.dim((0, 0), (B, 0), f"b = {B:.0f} cm", off=34, color=C["dim"])
    cv.dim((B, 0), (B, H), f"h = {H:.0f} cm", off=44, color=C["dim"])
    for d, n in ROWS:
        cv.text_px(cv.X(0) - 10, cv.Y(H - d), f"d = {d:.0f}（{n} 根）", 12,
                   C["muted"], "end")
    cv.line((-1, H - D), (B + 1, H - D), C["tension"], 2.0, dash="6 4")
    cv.text_px(cv.X(B / 2), cv.Y(H - D) - 16,
               "拉力側鋼筋：本題條件是這一排應變 = 0", 12, C["tension"],
               weight="700")

    x = W - Rm + 12
    y = 118
    for col, expr, desc in [
        (C["member"], f"8-#8 分三排（4-2-2）", f"A_{{st}} = {AST:.2f} cm^{{2}}"),
        (C["compr"], f"β_1 = {BETA1:.2f}", f"f'_c = {FC:.0f} 大於 280"),
        (C["tension"], f"ε_t = 0 → c = d = {D:.0f} cm", "中性軸被條件鎖死"),
        (C["compr"], f"a = β_1 c = {THIS['a']:.1f} cm", "壓力區深度"),
        (C["load"], f"P_n = {THIS['Pn']*TF:.1f} tf", f"M_n = {THIS['Mn']*TFM:.2f} tf·m"),
    ]:
        cv.rect_px(x, y - 15, 10, 30, col, 3)
        cv.math_px(x + 20, y - 7, expr, 13, col, "start", weight="700")
        cv.text_px(x + 20, y + 14, desc, 12, C["muted"], "start")
        y += 54
    cv.text_px(x, y + 10, "⚠ 這題沒有「求 c」這一步", 13.5, C["load"],
               "start", weight="700")
    cv.text_px(x, y + 32, "「拉力側應變 = 0」直接把 c", 12.2, C["muted"], "start")
    cv.text_px(x, y + 52, f"鎖在 {D:.0f} cm，不需解方程。", 12.2, C["muted"], "start")
    cv.text_px(x, y + 74, "整個斷面全部受壓。", 12.2, C["muted"], "start")

    cv.text_px(W / 2, 34, "圖 1　矩形柱斷面與三排鋼筋（b = 40、h = 56）", 17, C["text"], weight="700")
    cv.text_px(W / 2, 58, "壓力面在上；三排各距壓力面 8 / 28 / 48 cm",
               12.8, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
def fig2_strain():
    PW, PH = 330, 470
    s = THIS
    SX = (PH - 130) / H
    PX = lambda px: px / SX

    def frame(sub, ox=64):
        cv = Canvas(PW, PH, sx=SX, ox=ox, oy=64, bg="#FFFFFF")
        cv.text_px(PW / 2, 30, sub, 13.5, C["text"], weight="700")
        return cv

    c1 = frame("斷面與壓力區")
    _sec(c1)
    y_a = H - s["a"]
    c1.polygon([(0, y_a), (B, y_a), (B, H), (0, H)], C["fill_c"], "none")
    c1.line((-1, y_a), (B + 1, y_a), C["compr"], 2.4)
    c1.line((-1, H - s["c"]), (B + 1, H - s["c"]), C["tension"], 2.0, dash="6 4")
    c1.text_px(c1.X(B) - 6, c1.Y(y_a) - 12, f"a = {s['a']:.1f}", 12,
               C["compr"], "end", weight="700")
    c1.text_px(c1.X(B) - 6, c1.Y(H - s["c"]) + 14, f"c = {s['c']:.0f}", 12,
               C["tension"], "end", weight="700")

    c2 = frame("應變分佈", ox=PW / 2 - 10)
    e_scale = PX(86.0) / EPS_CU
    c2.line((0, 0), (0, H), C["muted"], 1.6)
    c2.polygon([(0, H), (EPS_CU * e_scale, H), (0, H - s["c"])],
               C["fill_c"], C["compr"], 2.4)
    c2.text_px(c2.X(EPS_CU * e_scale) + 6, c2.Y(H), f"ε_{{cu}} = {EPS_CU}", 12,
               C["compr"], "start")
    for bar in s["bars"]:
        yy = H - bar["d"]
        c2.dot((bar["eps"] * e_scale, yy), 4.8, fill=C["member"],
               stroke="#FFFFFF", w=1.4)
        c2.text_px(c2.X(bar["eps"] * e_scale) + 8, c2.Y(yy) - 12,
                   f"{bar['eps']:.6f}", 11, C["muted"], "start")
    c2.text_px(PW / 2, PH - 44, "最下排 ε = 0 → 應力也是 0", 12.5,
               C["tension"], weight="700")

    c3 = frame("等值應力塊與合力", ox=PW / 2 - 26)
    c3.line((0, 0), (0, H), C["muted"], 1.4)
    fmax = max(abs(s["Cc"]), max(abs(b["F"]) for b in s["bars"]))
    scale = PX(100.0) / fmax
    c3.arrow((0, H - s["a"] / 2), (s["Cc"] * scale, H - s["a"] / 2),
             C["compr"], 3.4, 10)
    c3.text_px(c3.X(s["Cc"] * scale) + 6, c3.Y(H - s["a"] / 2),
               f"C_c = {s['Cc']*TF:.1f} tf", 12, C["compr"], "start", weight="700")
    for bar in s["bars"]:
        yy = H - bar["d"]
        if abs(bar["F"]) < 1:
            c3.dot((0, yy), 4.6, fill=C["ghost"], stroke="#FFFFFF", w=1.4)
            c3.text_px(c3.X(0) + 10, c3.Y(yy), "0（應變為零）", 11.5,
                       C["ghost"], "start")
            continue
        c3.arrow((0, yy), (bar["F"] * scale, yy), C["compr"], 3.0, 9)
        tag = "扣占位" if bar["inside"] else "不扣"
        c3.text_px(c3.X(bar["F"] * scale) + 6, c3.Y(yy) - 12,
                   f"{bar['F']*TF:.2f} tf（{tag}）", 11.2, C["compr"],
                   "start", weight="700")
    c3.text_px(PW / 2, PH - 62, f"P_n = {s['Pn']*TF:.1f} tf", 12.8,
               C["text"], weight="700")
    c3.text_px(PW / 2, PH - 42, f"M_n = {s['Mn']*TFM:.2f} tf·m", 12.8,
               C["load"], weight="700")

    return compose([c1, c2, c3],
                   title="圖 2　拉力側應變 = 0 的斷面／應變／合力",
                   sub=f"c 被條件鎖在 {s['c']:.0f} cm，a = {s['a']:.1f} cm；"
                       f"全斷面受壓，最下排應力為零",
                   note="上排與中排在應力塊內要扣 0.85f'c 占位、最下排在塊外不扣——"
                        "三排的處理各不相同，是本題真正的考點")


# ══════════════════════════════════════════════════════════
def fig3_pm():
    W, HH = 980, 640
    L, Rm, T, Bm = 100, 330, 92, 96
    Ms = [s["Mn"] * TFM for s in CURVE]
    Ps = [s["Pn"] * TF for s in CURVE]
    m_max, p_max = max(Ms) * 1.30, P0 * TF * 1.10
    p_min = min(min(Ps), 0) * 1.10
    sx = (W - L - Rm) / m_max
    sy = (HH - T - Bm) / (p_max - p_min)
    k = sy / sx
    cv = Canvas(W, HH, sx=sx, ox=L, oy=Bm - p_min * sy, bg="#FFFFFF")

    cv.arrow((0, p_min * k), (0, p_max * k), C["muted"], 1.8, 9)
    cv.arrow((0, 0), (m_max, 0), C["muted"], 1.8, 9)
    cv.text_px(cv.X(0) - 44, cv.Y(p_max * k * 0.5), "P (tf)", 13.5, C["muted"])
    cv.text_px(cv.X(m_max * 0.5), HH - 40, "M (tf·m)", 13.5, C["muted"])

    nom = [(s["Mn"] * TFM, s["Pn"] * TF * k) for s in CURVE]
    des = [(s["phi"] * s["Mn"] * TFM, s["phi"] * s["Pn"] * TF * k) for s in CURVE]
    cv.poly(nom, C["ghost"], 2.2, dash="7 4")
    cv.polygon([(0, des[0][1])] + des + [(0, des[-1][1])], C["fill_c"], "none")
    cv.poly(des, C["compr"], 3.0)

    marks = [
        (P0 * TF, 0.0, f"純軸壓 P_0 = {P0*TF:,.0f} tf", C["accent"]),
        (THIS["Pn"] * TF, THIS["Mn"] * TFM,
         f"本題點 ε_t = 0：({THIS['Mn']*TFM:.1f}, {THIS['Pn']*TF:.0f})", C["load"]),
        (BAL["Pn"] * TF, BAL["Mn"] * TFM,
         f"平衡點（標稱 M_n 峰值 {BAL['Mn']*TFM:.2f}）", C["accent"]),
        (0.0, PURE_M["Mn"] * TFM, f"純彎矩 {PURE_M['Mn']*TFM:.2f}", C["accent"]),
    ]
    for i, (p, m, lab, col) in enumerate(marks):
        cv.dot((m, p * k), 6.0, fill=col, stroke="#FFFFFF", w=2.0)
        left = (i == 2)                      # 平衡點標籤放左邊，避開右側表格
        cv.text_px(cv.X(m) + (-12 if left else 12), cv.Y(p * k) - 6, lab, 12.2,
                   col, "end" if left else "start", weight="700")

    # 設計曲線的彎矩峰值
    pm = PHIM_PEAK
    cv.dot((pm["phi"] * pm["Mn"] * TFM, pm["phi"] * pm["Pn"] * TF * k), 6.4,
           fill=C["compr"], stroke="#FFFFFF", w=2.0)
    cv.text_px(cv.X(pm["phi"] * pm["Mn"] * TFM) + 12,
               cv.Y(pm["phi"] * pm["Pn"] * TF * k) + 16,
               f"φM_n 峰值 {pm['phi']*pm['Mn']*TFM:.2f}（ε_t = 0.005）", 12.2,
               C["compr"], "start", weight="700")

    x = W - Rm + 14
    y = 120
    cv.text_px(x, y - 26, "四個關鍵點", 15, C["text"], "start", weight="700")
    for lab, val in [
        (f"純軸壓 P_0", f"{P0*TF:,.0f} tf"),
        (f"本題 ε_t = 0", f"P = {THIS['Pn']*TF:.0f}, M = {THIS['Mn']*TFM:.2f}"),
        (f"平衡點 c_b = {CB:.2f}", f"P = {BAL['Pn']*TF:.0f}, M = {BAL['Mn']*TFM:.2f}"),
        (f"純彎矩", f"M = {PURE_M['Mn']*TFM:.2f}"),
    ]:
        cv.math_px(x, y, lab, 12.2, C["muted"], "start")
        cv.text_px(x, y + 18, val, 12.2, C["text"], "start", weight="700")
        y += 44

    cv.rect_px(x - 6, y + 4, W - x - 20, 116, "#FFF6E8", 9, C["load"], 1.3)
    cv.text_px(x + 6, y + 28, "標稱峰值 ≠ 設計峰值", 13.5, C["load"],
               "start", weight="700")
    cv.text_px(x + 6, y + 50,
               f"max M_n = {M_PEAK['Mn']*TFM:.2f} @ c = {M_PEAK['c']:.2f}",
               12.2, C["muted"], "start")
    cv.text_px(x + 6, y + 70,
               f"max φM_n = {pm['phi']*pm['Mn']*TFM:.2f} @ ε_t = 0.005",
               12.2, C["muted"], "start")
    cv.text_px(x + 6, y + 90,
               f"φ×max M_n = {BAL['phi']*M_PEAK['Mn']*TFM:.2f}（較小）",
               12.2, C["load"], "start", weight="700")
    cv.text_px(x + 6, y + 108, "完整推導見 RC-2015-1", 11.8, C["muted"], "start")

    cv.text_px(W / 2, 34, "圖 3　本題點在 P-M 圖上的位置", 17, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               "灰虛線＝標稱強度，藍實線＝設計強度（乘 φ）", 12.8, C["muted"])
    cv.text_px(W / 2, HH - 18,
               f"本題點 P_n = {THIS['Pn']*TF:.0f} tf 遠在平衡點 "
               f"{BAL['Pn']*TF:.0f} tf 之上，屬壓力控制區", 13, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
FIGURES = [
    ("1-section", fig1_section,
     "還去解方程求 c——本題 ε_t = 0 已經把 c 鎖死在 48 cm"),
    ("2-strain",  fig2_strain,
     "三排鋼筋一律扣 0.85f'c 占位（最下排在應力塊外不該扣）；最下排誤給非零應力"),
    ("3-pm",      fig3_pm,
     "把平衡點的標稱峰值當成設計峰值（max φM_n ≠ φ×max M_n）"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    t = THIS
    b1, b2, b3 = t["bars"]
    checks = [
        ("β_1",       BETA1,          0.80,     0.001),
        ("A_st",      AST,            40.56,    0.01),
        ("c",         t["c"],         48.0,     0.001),
        ("a",         t["a"],         38.40,    0.01),
        ("ε_1",       b1["eps"],      0.002500, 1e-6),
        ("ε_2",       b2["eps"],      0.001250, 1e-6),
        ("f_s2",      b2["fs"],       2550.0,   1.0),
        ("C_c",       t["Cc"],        456960,   5),
        ("C_s1",      b1["F"],        79143,    5),
        ("C_s2",      b2["F"],        22840,    5),
        ("P_n tf",    t["Pn"] * TF,   558.94,   0.05),
        ("M_n tfm",   t["Mn"] * TFM,  56.04,    0.02),
        ("c_b",       CB,             28.465,   0.01),
        ("P_b tf",    BAL["Pn"] * TF, 308.56,   0.05),
        ("M_b tfm",   BAL["Mn"] * TFM, 69.37,   0.02),
        ("c(ε_t=.005)", C_TC,         18.0,     0.01),
        ("φM_n 峰 tfm", PHIM_PEAK["phi"] * PHIM_PEAK["Mn"] * TFM, 51.07, 0.05),
    ]
    print("── 與 RC-2008-2.md §4 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<12} 算得 {got:>12.5f}   .md {want:>9}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"
    print(f"  （補算）純彎矩點 c = {C0:.2f} cm、M_n = {PURE_M['Mn']*TFM:.2f} tf·m"
          f"（.md 未列此值，僅供圖 3 定位）")
    print(f"  （補算）max M_n = {M_PEAK['Mn']*TFM:.2f} @ c = {M_PEAK['c']:.2f}；"
          f"max φM_n = {PHIM_PEAK['phi']*PHIM_PEAK['Mn']*TFM:.2f} @ "
          f"ε_t = {PHIM_PEAK['et']:.5f}；φ×max M_n = "
          f"{BAL['phi']*M_PEAK['Mn']*TFM:.2f}")
    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<32} 攔：{catches}")


if __name__ == "__main__":
    main()
