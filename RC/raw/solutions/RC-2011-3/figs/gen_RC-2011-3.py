#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2011-3 矩形柱・0.9Pb 下的設計彎矩與斷面韌性 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2011-3.md §1 給定的原始資料；c_b、P_b、c、ε_t、φ、M_n、
     k、φ_y、c*、φ_u、μ_φ 全部由 section() / 求根現算，檔尾對 §4 公佈值 assert。
  2. 改 §1 任一數字重跑，三張圖跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

註：本檔採解讀 A（0.9P_b 視為標稱軸力 P_n），與 .md §5「題意歧義」的定案一致。
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2011-3"

# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
B, H = 40.0, 60.0
FC, FY, ES = 350.0, 4200.0, 2.04e6
A_BAR = 8.143            # #10
N_PER_ROW = 2            # 6-#10 分三排，每排 2 根
ROWS = (6.0, 30.0, 54.0)  # 各排距壓力面 (cm)
GAMMA = 1.3              # 載重係數
EPS_CU = 0.003

AS_ROW = N_PER_ROW * A_BAR
D = ROWS[-1]
EPSY = FY / ES
BETA1 = max(0.65, min(0.85, 0.85 - 0.05 * (FC - 280) / 70))
CB = EPS_CU * ES / (EPS_CU * ES + FY) * D
TF, TFM = 1e-3, 1e-5


def phi_of(et):
    if et >= 0.005:  return 0.90
    if et <= EPSY:   return 0.65
    return 0.65 + 0.25 * (et - EPSY) / (0.005 - EPSY)


def section(c):
    a = BETA1 * c
    Cc = 0.85 * FC * a * B
    P, M = Cc, Cc * (H / 2 - a / 2)
    bars = []
    for d in ROWS:
        eps = EPS_CU * (c - d) / c
        fs = max(-FY, min(FY, ES * eps))
        F = AS_ROW * (fs - 0.85 * FC) if (d < a and fs > 0) else AS_ROW * fs
        P += F
        M += F * (H / 2 - d)
        bars.append(dict(d=d, eps=eps, fs=fs, F=F))
    et = EPS_CU * (D - c) / c
    return dict(c=c, a=a, Cc=Cc, bars=bars, Pn=P, Mn=M, et=et, phi=phi_of(et))


BAL = section(CB)
P_TARGET = 0.9 * BAL["Pn"]        # 解讀 A：P_n = 0.9 P_b


def solve_c(target):
    lo, hi = 5.0, 55.0
    for _ in range(300):
        m = (lo + hi) / 2
        if section(m)["Pn"] > target: hi = m
        else:                          lo = m
    return m


C_WORK = solve_c(P_TARGET)
WORK = section(C_WORK)

# ── 韌性：φ_y（彈性裂縫斷面）與 φ_u（Whitney）──────────────
N_SERVICE = P_TARGET / GAMMA
N_RATIO = ES / (15000 * math.sqrt(FC))     # n = Es/Ec


def elastic_na(N):
    """在軸力 N 下，令最外層拉力筋恰達 ε_y 的彈性中性軸 k。"""
    def f(k):
        # 線性應變：壓力面 eps_c = eps_y * k/(d-k)；混凝土壓力 + 鋼筋力 = N
        eps_c = EPSY * k / (D - k)
        Ec = 15000 * math.sqrt(FC)
        Cc = 0.5 * eps_c * Ec * k * B
        tot = Cc
        for d in ROWS:
            eps = eps_c * (k - d) / k
            tot += AS_ROW * ES * eps * (1 if d >= k else 1)
        return tot - N
    lo, hi = 1.0, D - 0.5
    for _ in range(300):
        m = (lo + hi) / 2
        if f(m) > 0: hi = m
        else:        lo = m
    return m


K_Y = elastic_na(N_SERVICE)
PHI_Y = EPSY / (D - K_Y)
C_U = solve_c(N_SERVICE)          # 極限狀態同一軸力下的 Whitney 中性軸
PHI_U = EPS_CU / C_U
MU = PHI_U / PHI_Y


# ══════════════════════════════════════════════════════════
def _sec(cv, mark_mid=True):
    cv.polygon([(0, 0), (B, 0), (B, H), (0, H)], C["fill_m"], C["member"], 2.6)
    for d in ROWS:
        y = H - d                       # 壓力面在上
        col = C["accent"] if (mark_mid and abs(d - H / 2) < 1e-9) else C["member"]
        for i in range(N_PER_ROW):
            cv.dot((B * (i + 1) / (N_PER_ROW + 1), y), 6.2,
                   fill=col, stroke="#FFFFFF", w=1.8)


def fig1_section():
    W, HH = 700, 560
    L, Rm, T, Bm = 96, 286, 88, 92
    sx = min((W - L - Rm) / B, (HH - T - Bm) / H)
    cv = Canvas(W, HH, sx=sx, ox=L, oy=Bm, bg="#FFFFFF")
    _sec(cv)
    cv.line((-1, H / 2), (B + 1, H / 2), C["accent"], 1.8, dash="7 4")
    cv.text_px(cv.X(B) + 8, cv.Y(H / 2), "塑性形心 h/2 = 30", 12.5,
               C["accent"], "start", weight="700")
    cv.dim((0, 0), (B, 0), f"b = {B:.0f} cm", off=34, color=C["dim"])
    cv.dim((B, 0), (B, H), f"h = {H:.0f} cm", off=44, color=C["dim"])
    for d in ROWS:
        cv.text_px(cv.X(0) - 10, cv.Y(H - d), f"d = {d:.0f}", 12.2,
                   C["muted"], "end")

    x = W - Rm + 12
    y = 118
    for col, expr, desc in [
        (C["member"], f"6-#10 分三排，每排 {N_PER_ROW} 根", f"A_s（每排）= {AS_ROW:.3f} cm^{{2}}"),
        (C["accent"], "中排 d_m = 30 cm = h/2", "力臂為零 → 不貢獻彎矩"),
        (C["compr"], f"β_1 = {BETA1:.2f}", f"f'_c = {FC:.0f} > 280"),
        (C["compr"], f"c_b = {CB:.2f} cm", f"a_b = {BETA1*CB:.2f} cm"),
        (C["load"], f"P_b = {BAL['Pn']*TF:.1f} tf", f"M_b = {BAL['Mn']*TFM:.2f} tf·m"),
    ]:
        cv.rect_px(x, y - 15, 10, 30, col, 3)
        cv.math_px(x + 20, y - 7, expr, 13, col, "start", weight="700")
        cv.text_px(x + 20, y + 14, desc, 12, C["muted"], "start")
        y += 54

    cv.text_px(x, y + 10, "⚠ 中排的兩面性", 13.5, C["accent"], "start", weight="700")
    cv.text_px(x, y + 32, "彎矩：力臂 0，完全不貢獻", 12.2, C["muted"], "start")
    cv.text_px(x, y + 52, "軸力：照樣要算——c > 30 時", 12.2, C["muted"], "start")
    cv.text_px(x, y + 72, "受壓，c 小於 30 時受拉", 12.2, C["muted"], "start")

    cv.text_px(W / 2, 34, "圖 1　矩形柱斷面與三排鋼筋", 17, C["text"], weight="700")
    cv.text_px(W / 2, 58, "橘色中排恰在塑性形心上——考生最常忽略的一排",
               12.8, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
def fig2_balanced():
    """工作點（P_n = 0.9P_b）的斷面／應變／內力三聯圖。"""
    PW, PH = 320, 470
    s = WORK
    ymax = H

    SX = (PH - 130) / ymax

    def frame(sub, ox=64):
        cv = Canvas(PW, PH, sx=SX, ox=ox, oy=64, bg="#FFFFFF")
        cv.text_px(PW / 2, 30, sub, 13.5, C["text"], weight="700")
        return cv

    PX = lambda px: px / SX          # 像素 → 模型單位

    # (1) 斷面
    c1 = frame("斷面與壓力區")
    _sec(c1)
    y_na = H - s["c"]
    y_a = H - s["a"]
    c1.polygon([(0, y_a), (B, y_a), (B, H), (0, H)], C["fill_c"], "none")
    c1.line((-1, y_na), (B + 1, y_na), C["compr"], 2.0, dash="6 4")
    c1.line((-1, y_a), (B + 1, y_a), C["compr"], 2.4)
    c1.text_px(c1.X(B) - 6, c1.Y(y_na) + 14, f"c = {s['c']:.2f}", 12,
               C["compr"], "end", weight="700")
    c1.text_px(c1.X(B) - 6, c1.Y(y_a) - 12, f"a = {s['a']:.2f}", 12,
               C["compr"], "end", weight="700")
    c1.text_px(c1.X(B / 2), c1.Y(H) - 18, "壓力面", 12, C["muted"])

    # (2) 應變
    c2 = frame("應變分佈（線性）", ox=PW / 2 + 10)
    e_scale = PX(74.0) / EPS_CU     # 讓 ε_cu 對應 74 px
    c2.line((0, 0), (0, H), C["muted"], 1.6)
    pts = [(EPS_CU * e_scale, H), (0, y_na)]
    c2.polygon([(0, H), (EPS_CU * e_scale, H), (0, y_na)], C["fill_c"], C["compr"], 2.4)
    et_x = -s["et"] * e_scale
    c2.polygon([(0, y_na), (et_x, H - D), (0, H - D)], C["fill_t"], C["tension"], 2.4)
    c2.text_px(c2.X(EPS_CU * e_scale) + 6, c2.Y(H), f"ε_{{cu}} = {EPS_CU}", 12,
               C["compr"], "start")
    c2.text_px(c2.X(et_x) - 6, c2.Y(H - D), f"ε_t = {s['et']:.6f}", 12,
               C["tension"], "end")
    for bar in s["bars"]:
        yy = H - bar["d"]
        c2.dot((0, yy), 4.6, fill=C["member"], stroke="#FFFFFF", w=1.4)
        c2.text_px(c2.X(0) + 8, c2.Y(yy) - 12,
                   f"{bar['eps']:+.6f}", 11, C["muted"], "start")
    c2.text_px(PW / 2, PH - 42, f"φ = {s['phi']:.4f}（過渡區內插）", 12.5,
               C["accent"], weight="700")

    # (3) 內力
    c3 = frame("等值應力塊與合力", ox=PW / 2 - 20)
    c3.line((0, 0), (0, H), C["muted"], 1.4)
    fmax = max(abs(s["Cc"]), max(abs(b["F"]) for b in s["bars"]))
    scale = PX(96.0) / fmax
    c3.arrow((0, H - s["a"] / 2), (s["Cc"] * scale, H - s["a"] / 2),
             C["compr"], 3.4, 10)
    c3.text_px(c3.X(s["Cc"] * scale) + 6, c3.Y(H - s["a"] / 2),
               f"C_c = {s['Cc']*TF:.1f} tf", 12, C["compr"], "start", weight="700")
    for bar in s["bars"]:
        yy = H - bar["d"]
        col = C["compr"] if bar["F"] > 0 else C["tension"]
        c3.arrow((0, yy), (bar["F"] * scale, yy), col, 3.0, 9)
        lab = f"{abs(bar['F'])*TF:.2f} tf"
        anc = "start" if bar["F"] > 0 else "end"
        c3.text_px(c3.X(bar["F"] * scale) + (6 if bar["F"] > 0 else -6),
                   c3.Y(yy) - 12, lab, 11.5, col, anc, weight="700")
    c3.text_px(PW / 2, PH - 60, f"P_n = {s['Pn']*TF:.1f} tf = 0.9P_b", 12.5,
               C["text"], weight="700")
    c3.text_px(PW / 2, PH - 40,
               f"M_n = {s['Mn']*TFM:.2f} → φM_n = {s['phi']*s['Mn']*TFM:.2f} tf·m",
               12.5, C["load"], weight="700")

    return compose([c1, c2, c3],
                   title="圖 2　軸力 = 0.9Pb 時的斷面／應變／合力",
                   sub=f"c = {s['c']:.2f} cm、a = {s['a']:.2f} cm；"
                       f"中排位置 30 cm 大於 a，落在等值應力塊之外",
                   note="中排在應力塊外就不扣 0.85f\'c 占位，而且此時它其實受微拉——"
                        "這兩件事一起錯會讓軸力差一截")


# ══════════════════════════════════════════════════════════
def fig3_curvature():
    """φ_y（彈性）vs φ_u（Whitney）：兩張應變圖並列。"""
    PW, PH = 360, 440

    def panel(sub, na, eps_top, eps_bot, col, cap):
        SX = (PH - 130) / H
        cv = Canvas(PW, PH, sx=SX, ox=PW / 2 + 16, oy=64, bg="#FFFFFF")
        cv.text_px(PW / 2, 30, sub, 13.5, C["text"], weight="700")
        e_scale = (72.0 / SX) / max(eps_top, abs(eps_bot))
        y_na = H - na
        cv.line((0, 0), (0, H), C["muted"], 1.5)
        cv.polygon([(0, H), (eps_top * e_scale, H), (0, y_na)],
                   C["fill_c"], col, 2.4)
        cv.polygon([(0, y_na), (eps_bot * e_scale, H - D), (0, H - D)],
                   C["fill_t"], C["tension"], 2.4)
        _w = (78.0 / SX)
        cv.line((-_w, y_na), (_w, y_na), C["muted"], 1.3, dash="5 4")
        cv.text_px(cv.X(0) + 8, cv.Y(y_na) + 14, f"中性軸 {na:.2f} cm", 11.5,
                   C["muted"], "start")
        cv.text_px(cv.X(eps_top * e_scale) + 6, cv.Y(H), f"{eps_top:.6f}", 11.5,
                   col, "start", weight="700")
        cv.text_px(cv.X(eps_bot * e_scale) - 6, cv.Y(H - D), f"{abs(eps_bot):.6f}",
                   11.5, C["tension"], "end", weight="700")
        cv.text_px(PW / 2, PH - 52, cap, 12.5, col, weight="700")
        return cv

    eps_c_y = EPSY * K_Y / (D - K_Y)
    p1 = panel("降伏狀態（彈性裂縫斷面）", K_Y, eps_c_y, -EPSY, C["compr"],
               f"φ_y = ε_y/(d−k) = {PHI_Y:.3e} 1/cm")
    p2 = panel("極限狀態（Whitney）", C_U, EPS_CU,
               -EPS_CU * (D - C_U) / C_U, C["load"],
               f"φ_u = ε_cu/c = {PHI_U:.3e} 1/cm")
    return compose([p1, p2],
                   title=f"圖 3　曲率延展比 = 極限曲率 / 降伏曲率 = {MU:.2f}",
                   sub=f"同一服務軸力 N = {N_SERVICE*TF:.1f} tf 下的兩個狀態",
                   note="降伏曲率用彈性三角形應力分佈、極限曲率用 Whitney 矩形——"
                        "兩者本構不同，不可混用同一組公式")


# ══════════════════════════════════════════════════════════
FIGURES = [
    ("1-section",   fig1_section,
     "忽略中排：彎矩多算（它力臂為零），或軸力漏算（它照樣有力）"),
    ("2-balanced",  fig2_balanced,
     "中排在應力塊外仍誤扣 0.85f'_c；沒發現 c < 30 時中排其實受拉"),
    ("3-curvature", fig3_curvature,
     "φ_y 與 φ_u 混用同一種應力分佈（彈性三角形 vs Whitney 矩形）"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    w = WORK
    checks = [
        ("β_1",      BETA1,           0.80,     0.001),
        ("c_b",      CB,              32.023,   0.01),
        ("P_b tf",   BAL["Pn"] * TF,  306.3,    0.2),
        ("M_b tfm",  BAL["Mn"] * TFM, 84.08,    0.05),
        ("0.9P_b tf", P_TARGET * TF,  275.7,    0.2),
        ("c",        w["c"],          29.606,   0.01),
        ("a",        w["a"],          23.685,   0.01),
        ("ε_t",      w["et"],         0.002472, 5e-6),
        ("φ",        w["phi"],        0.6851,   0.001),
        ("M_n tfm",  w["Mn"] * TFM,   82.85,    0.05),
        ("φM_n tfm", w["phi"] * w["Mn"] * TFM, 56.75, 0.05),
        ("N tf",     N_SERVICE * TF,  212.1,    0.2),
        ("k",        K_Y,             24.955,   0.06),
        ("φ_y",      PHI_Y,           7.088e-5, 3e-7),
        ("c*",       C_U,             24.922,   0.06),
        ("φ_u",      PHI_U,           1.2038e-4, 5e-7),
        ("μ_φ",      MU,              1.698,    0.02),
    ]
    print("── 與 RC-2011-3.md §4 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<10} 算得 {got:>14.6g}   .md {want:>10}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"
    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<32} 攔：{catches}")


if __name__ == "__main__":
    main()
