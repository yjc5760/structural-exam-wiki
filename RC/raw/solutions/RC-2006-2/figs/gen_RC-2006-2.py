#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2006-2 無側移細長柱・彎矩放大法 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2006-2.md §1 給定的原始資料；r、kl/r、界限、E_c、I_g、I_se、
     EI、P_c、C_m、δ_ns、M_c、M_2,min 全部現算，檔尾對 §4 公佈值 assert。
  2. 改 §1 任一數字（斷面、l_u、k、P_u、β_d、M_1、M_2）重跑，三張圖跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, beam_shape

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2006-2"

# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
B = H = 50.0        # 方形斷面 (cm)
LU    = 600.0       # 淨高 (cm)
K     = 0.9         # 有效長度係數
FC    = 280.0       # f'c
FY    = 4200.0
ES    = 2.04e6
A_BAR = 8.14        # #10 單根面積
N_BAR = 8           # 3×3 扣中心
PU    = 400_000.0   # 設計軸力 (kgf)
BETA_D = 0.3
M1    = 15e5        # kgf·cm（小端）
M2    = 27e5        # kgf·cm（大端）
COVER_TO_BAR = 7.0  # 鋼筋心距柱面 (cm)

# ── 由上列推得 ──────────────────────────────────────────
AST  = N_BAR * A_BAR
AG   = B * H
R    = 0.3 * H                       # 方形斷面的迴轉半徑近似
SLEND = K * LU / R
RATIO = M1 / M2                      # 單曲率取正（ACI 318-02 慣例）
LIMIT = min(40.0, 34 - 12 * RATIO)
EC   = 15000 * math.sqrt(FC)
IG   = B * H ** 3 / 12
# I_se：3×3 扣中心 → 繞形心軸，兩外排各 3 根 @ 18 cm，中排 2 根 @ 0
ARM  = H / 2 - COVER_TO_BAR
ISE  = 6 * A_BAR * ARM ** 2 + 2 * A_BAR * 0 ** 2
EI_S = 0.4 * EC * IG / (1 + BETA_D)                  # 簡化式
EI_P = (0.2 * EC * IG + ES * ISE) / (1 + BETA_D)     # 精確式
PC_S = math.pi ** 2 * EI_S / (K * LU) ** 2
PC_P = math.pi ** 2 * EI_P / (K * LU) ** 2
CM   = max(0.4, 0.6 + 0.4 * RATIO)
DNS_S = max(1.0, CM / (1 - PU / (0.75 * PC_S)))
DNS_P = max(1.0, CM / (1 - PU / (0.75 * PC_P)))
M2MIN = PU * (1.5 + 0.03 * H)
M2_USE = max(M2, M2MIN)
MC_S = DNS_S * M2_USE
MC_P = DNS_P * M2_USE

TFM = 1e-5
TF = 1e-3


# ══════════════════════════════════════════════════════════
def fig1_section():
    W, HH = 720, 560
    L, Rm, T, Bm = 92, 268, 88, 106
    sx = min((W - L - Rm) / B, (HH - T - Bm) / H)
    cv = Canvas(W, HH, sx=sx, ox=L, oy=Bm, bg="#FFFFFF")
    cv.polygon([(0, 0), (B, 0), (B, H), (0, H)], C["fill_m"], C["member"], 2.6)

    xs = [COVER_TO_BAR, B / 2, B - COVER_TO_BAR]
    ys = [COVER_TO_BAR, H / 2, H - COVER_TO_BAR]
    for xx in xs:
        for yy in ys:
            if xx == B / 2 and yy == H / 2:
                continue                       # 中心無筋（3×3 扣中心 = 8 根）
            arm = abs(xx - B / 2)
            col = C["load"] if arm > 0 else C["ghost"]
            cv.dot((xx, yy), 6.4, fill=col, stroke="#FFFFFF", w=1.8)

    # 彎曲軸（繞 Y 軸 → 力臂沿 x 量）
    cv.line((B / 2, -2), (B / 2, H + 2), C["accent"], 1.8, dash="7 4")
    cv.text_px(cv.X(B / 2), cv.Y(H) - 22, "Y 軸（彎曲軸）", 12.5, C["accent"],
               weight="700")
    cv.dim((COVER_TO_BAR, COVER_TO_BAR), (B / 2, COVER_TO_BAR),
           f"{ARM:.0f} cm", off=40, color=C["load"])
    cv.dim((0, 0), (B, 0), f"b = h = {B:.0f} cm", off=84, color=C["dim"])

    x = W - Rm + 12
    y = 118
    for col, expr, desc in [
        (C["member"], f"A_{{st}} = {N_BAR}×{A_BAR} = {AST:.2f} cm^{{2}}", "3×3 扣中心"),
        (C["load"],   f"6 根 @ {ARM:.0f} cm", "對 Y 軸有力臂"),
        (C["ghost"],  f"2 根 @ 0 cm", "落在彎曲軸上，不貢獻 I_{se}"),
        (C["member"], f"I_{{se}} = 6({A_BAR})({ARM:.0f})^{{2}} = {ISE:,.0f} cm^{{4}}",
         "鋼筋對形心的慣性矩"),
        (C["compr"],  f"I_g = bh^{{3}}/12 = {IG:,.0f} cm^{{4}}", "毛斷面"),
    ]:
        cv.rect_px(x, y - 15, 10, 30, col, 3)
        cv.math_px(x + 20, y - 7, expr, 13, col, "start", weight="700")
        cv.text_px(x + 20, y + 14, desc, 12, C["muted"], "start")
        y += 54

    cv.text_px(x, y + 10, "⚠ 最常數錯的一步", 13.5, C["load"], "start", weight="700")
    cv.text_px(x, y + 32, "8 根不是「每排 4 根」，", 12.2, C["muted"], "start")
    cv.text_px(x, y + 52, "而是 3×3 扣掉正中心。", 12.2, C["muted"], "start")
    cv.text_px(x, y + 74, "繞 Y 軸時 6 根有力臂、", 12.2, C["muted"], "start")
    cv.text_px(x, y + 94, "2 根力臂為零。", 12.2, C["muted"], "start")

    cv.legend(L, HH - 44, [(C["load"], f"力臂 {ARM:.0f} cm（6 根）"),
                           (C["ghost"], "力臂 0（2 根）")], size=12.5)
    cv.text_px(W / 2, 34, "圖 1　柱斷面與 I_{se} 的力臂", 17, C["text"], weight="700")
    cv.text_px(W / 2, 58, "8-#10 呈 3×3 扣中心；繞 Y 軸彎曲時只有 6 根有力臂",
               12.8, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
def fig2_curvature():
    """單曲率 vs 雙曲率：變形形狀＋彎矩圖＋C_m。"""
    W, HH = 880, 672
    cv = Canvas(W, HH, sx=1, bg="#FFFFFF")

    def panel(px, title, ratio, m1, m2, note, col):
        """px 為該欄中心像素；ratio 為 M1/M2（本慣例：單曲率正）。"""
        top, bot = 150, 470
        Lp = bot - top
        # 柱身（原始位置）
        cv.parts.append(f'<line x1="{px:.1f}" y1="{top}" x2="{px:.1f}" y2="{bot}" '
                        f'stroke="{C["ghost"]}" stroke-width="2" stroke-dasharray="6 4"/>')
        # 挫屈變形：單曲率為單一弓形，雙曲率為 S 形
        amp = 40.0
        pts = []
        for i in range(81):
            t = i / 80
            if ratio > 0:                       # 單曲率
                w = math.sin(math.pi * t)
            else:                               # 雙曲率
                w = math.sin(2 * math.pi * t)
            pts.append((px + amp * w, top + Lp * t))
        cv.parts.append('<polyline points="' +
                        " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) +
                        f'" fill="none" stroke="{C["deform"]}" stroke-width="4" '
                        'stroke-linecap="round"/>')
        # 端點彎矩圖（線性內插）
        mx = 96.0
        m_top, m_bot = m1, m2
        poly = [(px + 150, top), (px + 150 + mx * m_top / abs(m2), top),
                (px + 150 + mx * m_bot / abs(m2), bot), (px + 150, bot)]
        cv.parts.append('<polygon points="' +
                        " ".join(f"{a:.1f},{b:.1f}" for a, b in poly) +
                        f'" fill="{C["fill_m"]}" stroke="{C["bmd"]}" stroke-width="2.4"/>')
        cv.parts.append(f'<line x1="{px+150:.1f}" y1="{top}" x2="{px+150:.1f}" '
                        f'y2="{bot}" stroke="{C["muted"]}" stroke-width="1.4"/>')
        cv.text_px(px + 150 + mx * m_top / abs(m2) + 8, top + 8,
                   f"M_1 = {abs(m1)*TFM:.0f}", 12.5, C["bmd"], "start", weight="700")
        cv.text_px(px + 150 + mx * m_bot / abs(m2) + 8, bot - 8,
                   f"M_2 = {abs(m2)*TFM:.0f}", 12.5, C["bmd"], "start", weight="700")

        cv.text_px(px + 60, 116, title, 15, col, weight="700")
        cv.text_px(px + 60, bot + 34, f"M_1/M_2 = {ratio:+.3f}", 13.5, col,
                   weight="700")
        cm = max(0.4, 0.6 + 0.4 * ratio)
        raw = 0.6 + 0.4 * ratio
        cv.text_px(px + 60, bot + 58,
                   f"C_m = 0.6 + 0.4({ratio:+.3f}) = {raw:.3f}", 12.8, C["muted"])
        cv.text_px(px + 60, bot + 80,
                   f"→ C_m = {cm:.3f}" + ("（取 0.4 下限）" if raw < 0.4 else ""),
                   13, col, weight="700")
        cv.text_px(px + 60, bot + 104, note, 12.5, C["muted"])

    panel(120, "單曲率（本題）", RATIO, M1, M2,
          "同向彎曲，最大彎矩與挫屈變形疊在一起", C["load"])
    panel(580, "雙曲率（對照）", -RATIO, -M1, M2,
          "有反曲點，兩者錯開", C["compr"])

    cv.parts.append(f'<line x1="{450}" y1="120" x2="{450}" y2="{600}" '
                    f'stroke="{C["border"]}" stroke-width="1.4"/>')

    cv.text_px(W / 2, 34, "圖 2　單曲率 vs 雙曲率：C_m 為何差這麼多", 17,
               C["text"], weight="700")
    cv.text_px(W / 2, 58,
               "灰虛線＝原位置，藍線＝挫屈變形，綠塊＝端點彎矩圖", 12.8, C["muted"])
    cv.rect_px(40, HH - 62, W - 80, 44, "#FFF6E8", 9, C["load"], 1.2)
    cv.text_px(W / 2, HH - 48,
               "本頁採 ACI 318-02 慣例：單曲率 M_1/M_2 取正，配 34−12(·) 與 0.6+0.4(·)",
               12.5, C["muted"])
    cv.text_px(W / 2, HH - 28,
               "318-14 之後單曲率取負、公式同步變號，結果相同——混搭才會得出「不需放大」的相反結論",
               12.5, C["load"], weight="700")
    return cv.svg()


# ══════════════════════════════════════════════════════════
def fig3_magnifier():
    W, HH = 860, 580
    L, Rm, T, Bm = 96, 268, 88, 100
    x_max, y_max = 0.9, 4.2
    sx = (W - L - Rm) / x_max
    sy = (HH - T - Bm) / (y_max - 1)
    k = sy / sx

    def Y(d): return (d - 1) * k

    cv = Canvas(W, HH, sx=sx, ox=L, oy=Bm, bg="#FFFFFF")
    cv.arrow((0, Y(1)), (x_max, Y(1)), C["muted"], 1.8, 9)
    cv.arrow((0, Y(1)), (0, Y(y_max)), C["muted"], 1.8, 9)

    pts = [(t / 1000, Y(min(y_max, CM / (1 - t / 1000))))
           for t in range(0, int(x_max * 1000) + 1)
           if CM / (1 - t / 1000) <= y_max]
    cv.poly(pts, C["compr"], 3.2)

    for t in [0, 0.2, 0.4, 0.6, 0.8]:
        cv.line((t, Y(1)), (t, Y(1) - 6 / sx), C["muted"], 1.3)
        if t > 0:
            cv.text_px(cv.X(t), cv.Y(Y(1)) + 18, f"{t:.1f}", 12.5, C["muted"])
    for d in [1, 2, 3, 4]:
        cv.line((0, Y(d)), (0.012, Y(d)), C["muted"], 1.3)
        cv.text_px(cv.X(0) - 10, cv.Y(Y(d)), f"{d:.1f}", 12.5, C["muted"], "end")
    cv.text_px(cv.X(x_max / 2), HH - 40, "P_u / (0.75 P_c)", 13.5, C["muted"])
    cv.text_px(cv.X(0) - 62, cv.Y(Y((1 + y_max) / 2)), "δ_{ns}", 15, C["muted"])

    # δ_ns = 1.0 的下限線（低於此值一律取 1.0）
    cv.line((0, Y(1)), (x_max, Y(1)), C["ghost"], 1.6, dash="6 4")
    cv.text_px(cv.X(x_max) - 4, cv.Y(Y(1)) - 14,
               "δ_{ns} 下限 1.0（不可小於 1）", 12, C["ghost"], "end")

    # 本題工作點
    t0 = PU / (0.75 * PC_S)
    cv.dot((t0, Y(DNS_S)), 6.4, fill=C["load"], stroke="#FFFFFF", w=2.0)
    cv.line((t0, Y(1)), (t0, Y(DNS_S)), C["load"], 1.4, dash="4 4")
    cv.line((0, Y(DNS_S)), (t0, Y(DNS_S)), C["load"], 1.4, dash="4 4")
    cv.text_px(cv.X(t0) + 12, cv.Y(Y(DNS_S)) - 14,
               f"本題 δ_{{ns}} = {DNS_S:.3f}", 13.5, C["load"], "start", weight="700")
    cv.text_px(cv.X(t0) + 12, cv.Y(Y(DNS_S)) + 8,
               f"P_u/(0.75P_c) = {t0:.4f}", 12.2, C["muted"], "start")

    # 精確 EI 的對照點
    t1 = PU / (0.75 * PC_P)
    cv.dot((t1, Y(DNS_P)), 5.6, fill=C["compr"], stroke="#FFFFFF", w=1.8)
    cv.text_px(cv.X(t1) - 14, cv.Y(Y(DNS_P)) - 16,
               f"精確 EI 式 → {DNS_P:.3f}", 12.2, C["compr"], "end", weight="700")

    x = W - Rm + 10
    y = 116
    for lab, val, unit, col in [
        ("kl_u/r", SLEND, "", C["text"]),
        ("界限 34−12(M_1/M_2)", LIMIT, "", C["text"]),
        ("E_c", EC, "kgf/cm^{2}", C["muted"]),
        ("EI（簡化式）", EI_S, "kgf·cm^{2}", C["muted"]),
        ("P_c", PC_S * TF, "tf", C["compr"]),
        ("C_m", CM, "", C["compr"]),
        ("δ_{ns}", DNS_S, "", C["load"]),
        ("M_{2,min}", M2MIN * TFM, "tf·m", C["accent"]),
        ("M_c", MC_S * TFM, "tf·m", C["load"]),
    ]:
        cv.math_px(x, y, lab, 12.5, col, "start")
        v = f"{val:,.4g}" if abs(val) < 1e5 else f"{val:.3e}"
        cv.text_px(x + 150, y, v, 12.5, col, "start", weight="700")
        y += 27

    cv.rect_px(x - 6, y + 10, W - x - 20, 76, "#FFF6E8", 9, C["accent"], 1.3)
    cv.text_px(x + 6, y + 32, "M_{2,min} 檢核不可省", 13, C["accent"],
               "start", weight="700")
    cv.text_px(x + 6, y + 54,
               f"{M2MIN*TFM:.1f} 小於 {M2*TFM:.0f} → 由 M_2 控制", 12.2,
               C["muted"], "start")
    cv.text_px(x + 6, y + 74, "若反過來，C_m 須取 1.0", 12.2, C["muted"], "start")

    cv.text_px(W / 2, 34, "圖 3　放大係數 δ_{ns} 隨軸力比的變化", 17,
               C["text"], weight="700")
    cv.text_px(W / 2, 58,
               "δ_{ns} = C_m /(1 − P_u/0.75P_c)：軸力越接近 0.75P_c，放大越劇烈",
               12.8, C["muted"])
    cv.text_px(W / 2, HH - 20,
               f"M_c = δ_{{ns}} × max(M_2, M_{{2,min}}) = {DNS_S:.3f} × {M2_USE*TFM:.0f}"
               f" = {MC_S*TFM:.1f} tf·m", 13, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
FIGURES = [
    ("1-section",   fig1_section,
     "把 8-#10 當成每排 4 根；I_se 少算或多算力臂為零的中排 2 根"),
    ("2-curvature", fig2_curvature,
     "M_1/M_2 的正負與細長比界限／C_m 公式混搭不同版本，導出「不需放大」的相反結論"),
    ("3-magnifier", fig3_magnifier,
     "漏掉 0.75 折減；漏掉 δ_ns ≥ 1.0 下限；完全不做 M_2,min 檢核"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    checks = [
        ("r",        R,        15.0,     0.001),
        ("kl_u/r",   SLEND,    36.0,     0.001),
        ("M1/M2",    RATIO,    0.5556,   0.0005),
        ("界限",      LIMIT,    27.333,   0.005),
        ("E_c",      EC,       250998,   3),
        ("I_g",      IG,       520833,   1),
        ("I_se",     ISE,      15824,    1),
        ("EI 簡化",   EI_S,     4.0224e10, 5e6),
        ("P_c 簡化",  PC_S*TF,  1361.4,   0.3),
        ("C_m",      CM,       0.8222,   0.0005),
        ("δ_ns",     DNS_S,    1.3518,   0.0005),
        ("M_2,min",  M2MIN*TFM, 12.0,    0.01),
        ("M_c",      MC_S*TFM, 36.50,    0.02),
        ("EI 精確",   EI_P,     4.4944e10, 5e6),
        ("P_c 精確",  PC_P*TF,  1521.2,   0.3),
        ("δ_ns 精確", DNS_P,    1.2661,   0.0005),
        ("M_c 精確",  MC_P*TFM, 34.19,    0.02),
    ]
    print("── 與 RC-2006-2.md §4 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<10} 算得 {got:>14.5g}   .md {want:>10}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"
    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<32} 攔：{catches}")


if __name__ == "__main__":
    main()
