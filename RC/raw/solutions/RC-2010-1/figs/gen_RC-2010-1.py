#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2010-1 圓形螺旋柱・降伏軸力 Py 與圍束極限軸力 Pu — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2010-1.md §1 給定的原始資料（外加明確標示的螺距假設）；
     其餘（Ag、Ach、rho_s、fL、f'cc、Py、Pu）一律由 section() 現算，檔尾對 §4 公佈值 assert。
  2. 改 §1 任一數字（D、Dc、f'c、fy、根數、螺距）重跑，三張圖全部跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2010-1"

# ══════════════════════════════════════════════════════════
# §1 原始給定（唯一手輸入區）
# ══════════════════════════════════════════════════════════
D_OUT  = 75.0        # 圓柱全斷面外徑 (cm)
D_C    = 68.0        # 螺旋筋外緣直徑（外到外, cm）
FC     = 350.0       # f'c (kgf/cm^2)
FY     = 4200.0      # fy = fyt (kgf/cm^2)
A_SP   = 1.27        # #4 螺旋筋單根面積 (cm^2)
D_B_SP = 1.27        # #4 標稱直徑 (cm)
A_BAR  = 8.17        # #10 主筋單根面積 (cm^2)
N_BAR  = 12          # 主筋根數
S_ASSUMED = 10.0     # ⚠ 螺距：題目未給，本解假設（見 .md §1 註）

# ── 由上列推得 ──────────────────────────────────────────
AG   = math.pi * (D_OUT / 2) ** 2
ACH  = math.pi * (D_C   / 2) ** 2
AST  = N_BAR * A_BAR
COVER_AREA = AG - ACH                       # 蓋層（犧牲層）
RHO_MIN = 0.45 * (AG / ACH - 1) * FC / FY   # 規範最小螺旋筋比
RHO_TH  = 0.4146 * (AG / ACH - 1) * FC / FY # Pu = Py 的理論門檻

KGF_TF = 1e-3


def rho_s(s):
    """螺旋筋體積比。分母核心與 A_ch 同基準（量到螺筋外緣）。"""
    return 4 * A_SP / (D_C * s)


def parts(s):
    """回傳 Py 與 Pu 的三段分解（kgf）。這支函式是三張圖唯一的數值來源。"""
    core = 0.85 * FC * (ACH - AST)      # 核心素混凝土（Py、Pu 共有）
    shell = 0.85 * FC * COVER_AREA      # 蓋層：只有 Py 有
    steel = FY * AST                    # 縱向鋼筋（兩者共有）
    r = rho_s(s)
    fL = r * FY / 2
    gain = 4.1 * fL * ACH               # 圍束增益：只有 Pu 有
    return dict(core=core, shell=shell, steel=steel, gain=gain, rho=r, fL=fL,
                fcc=FC + 4.1 * fL,
                Py=core + shell + steel,
                Pu=core + gain + steel,
                Pu_no085=(FC + 4.1 * fL) * (ACH - AST) + steel)   # 漏 0.85 的錯誤式


REF = parts(S_ASSUMED)


# ══════════════════════════════════════════════════════════
# 圖 1：斷面重繪（圓形螺旋柱）
# ══════════════════════════════════════════════════════════
def fig1_section():
    W, H = 720, 560
    R_out, R_c = D_OUT / 2, D_C / 2
    L, Rm, T, B = 70, 250, 88, 148
    sx = min((W - L - Rm) / D_OUT, (H - T - B) / D_OUT)
    cv = Canvas(W, H, sx=sx, ox=L + R_out * sx, oy=B + R_out * sx, bg="#FFFFFF")

    # 蓋層（環）：外圓填色、核心挖白
    cv.circle((0, 0), R_out, fill=C["fill_m"], stroke=C["member"], w=2.6)
    cv.circle((0, 0), R_c, fill="#FFFFFF", stroke="none", w=0)
    # 核心（圍束區）
    cv.circle((0, 0), R_c, fill=C["fill_c"], stroke=C["compr"], w=2.6, dash="7 4")

    # 主筋環：12 根，置於螺旋筋內側一個螺筋直徑
    R_bar = R_c - D_B_SP - 1.27          # 主筋形心圓半徑（#10 半徑約 1.27）
    for i in range(N_BAR):
        th = 2 * math.pi * i / N_BAR + math.pi / 2
        cv.dot((R_bar * math.cos(th), R_bar * math.sin(th)), 5.2,
               fill=C["member"], stroke="#FFFFFF", w=1.6)

    # 尺寸線
    cv.dim((-R_out, -R_out), (R_out, -R_out),
           f"D = {D_OUT:.0f} cm", off=32, color=C["dim"])
    cv.dim((-R_c, -R_out), (R_c, -R_out),
           f"D_c = {D_C:.0f} cm", off=78, color=C["compr"])

    # 右側註記
    x = W - Rm + 8
    rows = [
        (C["member"], f"A_g = πD^{{2}}/4 = {AG:,.1f} cm^{{2}}", "全斷面"),
        (C["compr"],  f"A_{{ch}} = πD_c^{{2}}/4 = {ACH:,.1f} cm^{{2}}", "核心，量到螺筋外緣"),
        (C["load"],   f"A_g − A_{{ch}} = {COVER_AREA:,.1f} cm^{{2}}", "蓋層＝犧牲層"),
        (C["member"], f"A_{{st}} = {N_BAR}×{A_BAR} = {AST:.2f} cm^{{2}}", f"{N_BAR}-#10 環排"),
    ]
    y = 118
    for col, expr, desc in rows:
        cv.rect_px(x, y - 15, 10, 30, col, 3)
        cv.math_px(x + 20, y - 7, expr, 14, col, "start", weight="700")
        cv.text_px(x + 20, y + 14, desc, 12.5, C["muted"], "start")
        y += 56
    cv.text_px(x, y + 4, "⚠ Ach 要用 Dc，不是 D", 13.5, C["load"], "start", weight="700")
    cv.text_px(x, y + 27, "誤用 D 會把核心高估 22%，", 12.5, C["muted"], "start")
    cv.text_px(x, y + 48, "蓋層就整個消失了。", 12.5, C["muted"], "start")

    cv.text_px(W / 2, 34, "圖 1　圓形螺旋柱斷面（向量重繪）", 17, C["text"], weight="700")
    cv.text_px(W / 2, 58, "外環＝蓋層（會剝落，不計入 P_u）　　內圈藍區＝螺旋筋圍束的核心", 12.8, C["muted"])
    cv.text_px(W / 2, H - 22,
               f"螺旋筋 #4 @ s = {S_ASSUMED:.0f} cm 為假設值——原卷圖上無間距標註",
               13, C["load"], weight="700")
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 2：Py 與 Pu 的三段分解（本題的核心）
# ══════════════════════════════════════════════════════════
def fig2_loss_gain():
    W, H = 900, 600
    cv = Canvas(W, H, sx=1, bg="#FFFFFF")
    p = REF
    peak = p["Pu_no085"]                      # 以錯誤式為滿格，讓它「爆表」看得見
    x0, bw = 250, 520
    BASE = 150
    ROW = 108

    def stacked(y, segs, total, label, sub):
        cv.text_px(x0 - 18, y - 8, label, 14.5, C["text"], "end", weight="700")
        cv.text_px(x0 - 18, y + 14, sub, 12, C["muted"], "end")
        cv.rect_px(x0, y - 22, bw, 44, "#EDF1F6", 8)
        cur = x0
        for val, col, name in segs:
            w = bw * val / peak
            cv.rect_px(cur, y - 22, w, 44, col, 6)
            if w > 50:
                cv.text_px(cur + w / 2, y - 6, name, 12.5, "#FFFFFF", weight="700")
                cv.text_px(cur + w / 2, y + 12, f"{val*KGF_TF:,.0f}", 12, "#FFFFFF")
            cur += w
        cv.math_px(cur + 14, y, f"= {total*KGF_TF:,.0f} tf", 15,
                   C["text"], "start", weight="700")

    core, shell, steel, gain = p["core"], p["shell"], p["steel"], p["gain"]
    stacked(BASE, [(core, C["compr"], "核心素混凝土"),
                   (shell, C["load"], "蓋層"),
                   (steel, C["member"], "鋼筋")],
            p["Py"], "P_y　降伏軸力", "蓋層剝落前，全斷面")
    stacked(BASE + ROW, [(core, C["compr"], "核心素混凝土"),
                         (gain, C["bmd"], "圍束"),
                         (steel, C["member"], "鋼筋")],
            p["Pu"], "P_u　極限軸力", "蓋層已剝落，僅核心")
    stacked(BASE + 2 * ROW, [(p["fcc"] * (ACH - AST), C["ghost"], "f'_{cc}(A_{ch}−A_{st})　未乘 0.85"),
                             (steel, C["member"], "鋼筋")],
            p["Pu_no085"], "錯誤式：漏掉 0.85", "P_u = f'_{cc}(A_{ch}−A_{st}) + f_y A_{st}")

    # 中段對照：蓋層損失 vs 圍束補償
    yA = BASE - 22 + 44 / 2
    xa = x0 + bw * core / peak
    xb = xa + bw * shell / peak
    xc = x0 + bw * core / peak + bw * gain / peak
    cv.line((xb, 0), (xb, 0), C["muted"])   # placeholder，實際用像素線
    cv.parts.append(
        f'<line x1="{xb:.1f}" y1="{BASE+22:.1f}" x2="{xc:.1f}" y2="{BASE+ROW-22:.1f}" '
        f'stroke="{C["accent"]}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    cv.text_px((xa + xb) / 2, BASE + ROW / 2 - 6,
               f"蓋層損失 {shell*KGF_TF:,.1f} tf", 13, C["load"], weight="700")
    cv.text_px((xa + xb) / 2, BASE + ROW / 2 + 14,
               f"圍束補償 {gain*KGF_TF:,.1f} tf　→　淨差 {(gain-shell)*KGF_TF:+.1f} tf",
               12.5, C["bmd"], weight="700")

    # ρs = 0 的反證
    yz = BASE + 3 * ROW + 4
    cv.rect_px(150, yz - 30, W - 300, 84, "#FFF6E8", 10, C["load"], 1.4)
    cv.text_px(W / 2, yz - 8, "為什麼一定要有那個 0.85：把 ρ_s 設為 0 檢驗",
               14, C["load"], weight="700")
    z_ok = (0.85 * FC * (ACH - AST) + FY * AST)
    z_bad = (FC * (ACH - AST) + FY * AST)
    cv.text_px(W / 2, yz + 16,
               f"正確式 → {z_ok*KGF_TF:,.0f} tf = {z_ok/REF['Py']:.3f} P_y"
               f"（恰為損失掉蓋層的 {100*(1-z_ok/REF['Py']):.1f}%）", 13, C["compr"])
    cv.text_px(W / 2, yz + 38,
               f"漏 0.85 → {z_bad*KGF_TF:,.0f} tf = {z_bad/REF['Py']:.3f} P_y"
               f"　沒有橫向鋼筋卻留 97% 承載力，不可能", 13, C["load"], weight="700")

    cv.text_px(W / 2, 34, "圖 2　P_y 與 P_u 的三段分解：蓋層損失 vs 圍束補償",
               17, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               "兩者只差中間那一塊——把蓋層換成圍束增益。長度幾乎相同，代表剛好打平",
               12.8, C["muted"])
    cv.text_px(W / 2, H - 26,
               f"P_u / P_y = {REF['Pu']/REF['Py']:.4f}　零餘裕；漏 0.85 會憑空多出 "
               f"{(REF['Pu_no085']-REF['Pu'])*KGF_TF:,.0f} tf",
               13, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 3：rho_s 隨螺距 s 的變化與兩條門檻
# ══════════════════════════════════════════════════════════
def fig3_rho_s():
    W, H = 760, 540
    s_lo, s_hi = 6.0, 14.0
    r_lo, r_hi = 0.004, 0.014
    L, Rm, T, B = 92, 210, 84, 74
    sx = (W - L - Rm) / (s_hi - s_lo)
    sy = (H - T - B) / (r_hi - r_lo)
    k = sy / sx                                  # y 軸相對縮放
    cv = Canvas(W, H, sx=sx, ox=L - s_lo * sx, oy=B - r_lo * sy, bg="#FFFFFF")

    def Y(r): return r * k

    # 合格區（rho >= rho_min）
    s_need = 4 * A_SP / (RHO_MIN * D_C)
    cv.polygon([(s_lo, Y(RHO_MIN)), (s_need, Y(RHO_MIN)),
                (s_need, Y(r_hi)), (s_lo, Y(r_hi))],
               "rgba(76,175,80,0.10)", "none")

    # 軸
    cv.arrow((s_lo, Y(r_lo)), (s_hi, Y(r_lo)), C["muted"], 1.8, 9)
    cv.arrow((s_lo, Y(r_lo)), (s_lo, Y(r_hi)), C["muted"], 1.8, 9)
    for s in range(6, 15, 2):
        cv.line((s, Y(r_lo)), (s, Y(r_lo) - 6 / sx), C["muted"], 1.4)
        cv.text_px(cv.X(s), cv.Y(Y(r_lo)) + 18, str(s), 12.5, C["muted"])
    for r in [0.004, 0.006, 0.008, 0.010, 0.012, 0.014]:
        cv.line((s_lo, Y(r)), (s_lo + 6 / sx, Y(r)), C["muted"], 1.4)
        cv.text_px(cv.X(s_lo) - 10, cv.Y(Y(r)), f"{r:.3f}", 12, C["muted"], "end")
    cv.text_px(cv.X((s_lo + s_hi) / 2), H - 34, "螺旋筋間距 s（cm）", 13.5, C["muted"])
    cv.text_px(cv.X(s_lo) - 62, cv.Y(Y((r_lo + r_hi) / 2)), "ρ_s", 15, C["muted"])

    # rho_s(s) 曲線
    pts = [(s / 20, Y(rho_s(s / 20))) for s in range(int(s_lo * 20), int(s_hi * 20) + 1)]
    cv.poly(pts, C["compr"], 3.2)

    # 兩條門檻
    cv.line((s_lo, Y(RHO_MIN)), (s_hi, Y(RHO_MIN)), C["load"], 2.0, dash="8 5")
    cv.text_px(cv.X(s_hi) + 8, cv.Y(Y(RHO_MIN)),
               f"ρ_s,min = {RHO_MIN:.5f}", 13, C["load"], "start", weight="700")
    cv.text_px(cv.X(s_hi) + 8, cv.Y(Y(RHO_MIN)) - 18,
               "規範值（係數 0.45）", 12, C["muted"], "start")
    cv.line((s_lo, Y(RHO_TH)), (s_hi, Y(RHO_TH)), C["accent"], 1.8, dash="4 4")
    cv.text_px(cv.X(s_hi) + 8, cv.Y(Y(RHO_TH)),
               f"ρ_s,th = {RHO_TH:.5f}", 13, C["accent"], "start", weight="700")
    cv.text_px(cv.X(s_hi) + 8, cv.Y(Y(RHO_TH)) + 19,
               "P_u = P_y 的理論門檻（0.4146）", 12, C["muted"], "start")

    # 兩個工作點
    r10 = rho_s(S_ASSUMED)
    cv.dot((S_ASSUMED, Y(r10)), 6.0, fill=C["load"], stroke="#FFFFFF", w=2.0)
    cv.text_px(cv.X(S_ASSUMED) - 12, cv.Y(Y(r10)) + 30,
               f"假設 s = {S_ASSUMED:.0f} cm → ρ_s = {r10:.5f}", 12.5, C["load"],
               "end", weight="700")
    cv.text_px(cv.X(S_ASSUMED) - 12, cv.Y(Y(r10)) + 50,
               "兩條門檻都過不了", 12, C["muted"], "end")
    cv.dot((s_need, Y(RHO_MIN)), 6.0, fill=C["bmd"], stroke="#FFFFFF", w=2.0)
    cv.text_px(cv.X(s_need) - 12, cv.Y(Y(RHO_MIN)) - 20,
               f"s ≤ {s_need:.2f} cm 才合格", 12.5, C["bmd"], "end", weight="700")

    cv.text_px(cv.X(s_lo) + 14, cv.Y(Y(r_hi)) + 24, "合格區", 13.5, C["bmd"],
               "start", weight="700")

    cv.text_px(W / 2, 34, "圖 3　螺旋筋比 ρ_s 與兩條門檻", 17, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               "ρ_s = 4A_{sp} /(D_c·s)：間距越密、螺旋筋比越高", 12.8, C["muted"])
    cv.text_px(W / 2, H - 16,
               "兩條門檻的間距（0.45 vs 0.4146）就是「理論剛好夠、規範還不夠」的那條縫",
               13, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
FIGURES = [
    ("1-section",   fig1_section,
     "A_ch 誤用全斷面直徑 D；把 D_c 當成核心直徑以外的量法"),
    ("2-loss-gain", fig2_loss_gain,
     "P_u 漏乘 0.85（會憑空多出 183 tf）；把「ρ_s 不足」與「P_u > P_y」同時寫出而不覺矛盾"),
    ("3-rho-s",     fig3_rho_s,
     "分不清 ρ_s,min（規範 0.45）與 P_u = P_y 的理論門檻（0.4146）"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    p = REF
    checks = [
        ("A_g",        AG,                    4417.9,   0.1),
        ("A_ch",       ACH,                   3631.7,   0.1),
        ("A_st",       AST,                   98.04,    0.01),
        ("A_g-A_ch",   COVER_AREA,            786.2,    0.1),
        ("rho_s",      p["rho"],              0.00747,  1e-5),
        ("rho_s,min",  RHO_MIN,               0.00812,  1e-5),
        ("f_L",        p["fL"],               15.69,    0.02),
        ("f'_cc",      p["fcc"],              414.3,    0.1),
        ("蓋層損失tf",  p["shell"] * KGF_TF,   233.9,    0.2),
        ("圍束增益tf",  p["gain"] * KGF_TF,    233.6,    0.2),
        ("P_y tf",     p["Py"] * KGF_TF,      1696.9,   0.5),
        ("P_u tf",     p["Pu"] * KGF_TF,      1696.6,   0.5),
        ("錯誤式 tf",   p["Pu_no085"] * KGF_TF, 1875.8,  0.5),
        ("s_need",     4 * A_SP / (RHO_MIN * D_C), 9.20, 0.02),
    ]
    print("── 與 RC-2010-1.md §4 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<12} 算得 {got:>12.5f}   .md {want:>9}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"

    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<32} 攔：{catches}")


if __name__ == "__main__":
    main()
