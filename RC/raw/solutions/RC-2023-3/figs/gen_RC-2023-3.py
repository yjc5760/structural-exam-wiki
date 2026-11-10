#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2023-3 懸臂梁偏心載重：臨界斷面剪力與扭力忽略門檻 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2023-3.md §1 給定的原始資料；V_u、A_cp、p_cp、T_th（SI 與
     kgf 兩法）、φT_th、e_max、V_c、φV_c、0.5φV_c、A_v,min，以及「直接把 kgf 制
     代進 SI 式」與「讀法 B（容量）」的對照值全部現算，檔尾對 §4／§5 assert。
  2. 改 §1 任一數字重跑，三張圖跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

規範：土木 401-110（＝ ACI 318-19 藍本）。
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose
from recipes import bar_compare

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2023-3"


def M_(s):
    assert not any(ord(ch) > 0x2E80 for ch in s), f"math 字串不得含中日韓字元：{s}"
    return s


# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
B = 35.0                        # cm 梁寬
H = 60.0                        # cm 梁深
D = 53.0                        # cm 有效深度（題目已給）
L = 350.0                       # cm 懸臂跨度
WU = 25.0                       # kgf/cm（= 2.5 tf/m）
FC = 280.0                      # kgf/cm^2
FY = 4200.0                     # kgf/cm^2
PHI = 0.75                      # 題目指定
A_D13, DB_D13 = 1.27, 1.27      # cm^2 / cm
S_ASSUMED = 15.0                # cm 用於 A_v,min 檢核之假設間距

SQFC = math.sqrt(FC)
KGF_PER_MPA = 10.197            # 1 MPa = 10.197 kgf/cm^2
NCM_PER_KGFCM = 98.07           # 1 kgf·cm = 98.07 N·mm
TF, TFM = 1e-3, 1e-5

# ── 臨界斷面（d 偏移三條件均成立 → 距固定端 d） ──────────────
V_FIXED = WU * L                        # 固定端面
VU = WU * (L - D)                       # 臨界斷面

# ── 斷面幾何 ──────────────────────────────────────────────
ACP = B * H
PCP = 2 * (B + H)

# ── 扭力忽略門檻：SI 法與 kgf 制等效係數法 ─────────────────
FC_MPA = FC / KGF_PER_MPA
ACP_MM2 = ACP * 100.0
PCP_MM = PCP * 10.0
TTH_SI_NMM = math.sqrt(FC_MPA) / 12 * ACP_MM2 ** 2 / PCP_MM
TTH_SI = TTH_SI_NMM / NCM_PER_KGFCM            # kgf·cm
K_KGF = 0.265                                  # kgf 制等效係數（§5-2）
TTH_KGF = K_KGF * SQFC * ACP ** 2 / PCP
PHI_TTH = PHI * TTH_SI
TCR = 4 * TTH_SI                               # 裂縫扭矩

# 陷阱①：直接把 kgf/cm² 與 cm 代進 SI 式
TTH_WRONG = SQFC / 12 * ACP ** 2 / PCP
E_WRONG = PHI * TTH_WRONG / VU

# ── 最大偏心量 ────────────────────────────────────────────
E_MAX = PHI_TTH / VU

# ── 剪力容量檢核（D13 箍筋的用途） ─────────────────────────
VC = 0.53 * SQFC * B * D
PHI_VC = PHI * VC
HALF_PHI_VC = 0.5 * PHI_VC
AV = 2 * A_D13
AV_MIN = max(0.2 * SQFC * B * S_ASSUMED / FY, 3.5 * B * S_ASSUMED / FY)

# ── 讀法 B（把「所能承受」讀成容量） ────────────────────────
VU_CAP = 5 * PHI * VC                          # φ(V_c + 4V_c)
E_CAP = PHI_TTH / VU_CAP


# ══════════════════════════════════════════════════════════
# 圖 1　懸臂梁偏心載重與臨界斷面
# ══════════════════════════════════════════════════════════
def fig1():
    PW, PH = 480, 430

    # ---- 立面 ----
    e = Canvas(PW, PH, sx=1)
    mL, mR, mT, mB = 84, 76, 122, 118
    sx = min((PW - mL - mR) / L, (PH - mT - mB) / (H * 2.0))
    e.sx, e.ox, e.oy = sx, mL, mB
    e.panel("立面（懸臂）", "固定端在左，剪力由固定端往自由端遞減")
    e.polygon([(0, 0), (L, 0), (L, H), (0, H)], "#EDF1F6", C["member"], 2.4)
    e.fixed_support((0, H / 2), ang=90, size=int(H * sx / 2) or 20)
    e.udl((0, H), (L, H), 30.0, n=10, w=1.8)
    e.math_px(e.X(L * 0.52) - 42, e.Y(H + 30.0) - 15, M_("W_{u}"), 14.5,
              C["load"], weight="700")
    e.text_px(e.X(L * 0.52) - 24, e.Y(H + 30.0) - 15, "＝ 2.5 tf/m（偏心 e）",
              12.5, C["load"], "start", weight="700")

    e.line((D, -14), (D, H + 12), C["load"], 2.6)
    e.text_px(e.X(D) + 8, e.Y(0) + 26, f"臨界斷面 x = d = {D:g} cm", 12,
              C["load"], "start", weight="700")
    e.line((0, -14), (0, 0), C["muted"], 1.6, dash="4 3")
    e.dim((0, 0), (D, 0), M_(f"d = {D:g}"), off=52, label_off=15)
    e.dim((0, 0), (L, 0), M_(f"L = {L:g}"), off=84, label_off=15)
    e.dim((L, 0), (L, H), M_(f"h = {H:g}"), off=36, label_off=13)

    e.math_px(e.X(L * 0.58), e.Y(H * 0.55), M_(f"V_u = {VU * TF:.3f} tf"), 14,
              C["sfd"], weight="700")
    e.text_px(e.X(L * 0.58), e.Y(H * 0.55) + 19,
              f"固定端面 {V_FIXED * TF:.2f} tf（折減 "
              f"{1 - VU / V_FIXED:.1%}）", 12, C["muted"])

    # ---- 斷面 ----
    s = Canvas(PW, PH, sx=1)
    sL, sR, sT, sB = 176, 200, 152, 128
    ssx = min((PW - sL - sR) / B, (PH - sT - sB) / H)
    s.sx, s.ox, s.oy = ssx, sL, sB
    s.panel("斷面與偏心量", "載重偏心 e → 同時產生剪力與扭矩")
    s.polygon([(0, 0), (B, 0), (B, H), (0, H)], "#EDF1F6", C["member"], 2.6)
    s.polygon([(3.5, 3.5), (B - 3.5, 3.5), (B - 3.5, H - 3.5), (3.5, H - 3.5)],
              "none", C["load"], 2.0)
    for i in range(3):                              # 拉力筋在頂部（懸臂）
        s.dot((B * (0.22 + 0.28 * i), D), 4.8, fill=C["tension"],
              stroke="#FFFFFF", w=1.2)
    for i in range(2):                              # 壓力筋在底部
        s.dot((B * (0.28 + 0.44 * i), H - D), 4.8, fill=C["compr"],
              stroke="#FFFFFF", w=1.2)

    # 偏心載重：作用線離斷面中心 e
    ecc = B * 0.40
    s.line((B / 2, H), (B / 2, H + 16), C["muted"], 1.4, dash="4 3")
    s.arrow((B / 2 + ecc, H + 13), (B / 2 + ecc, H), C["load"], 3.4, 11)
    s.dim((B / 2, H + 15), (B / 2 + ecc, H + 15), M_("e"), off=-20,
          label_off=-11, color=C["load"])
    s.moment_arrow((B / 2, H * 0.48), r=36, ccw=False, color=C["accent"], w=2.4,
                   span=250, start=115)
    s.math_px(s.X(B / 2), s.Y(H * 0.48), M_("T = V e"), 13.5, C["accent"],
              weight="700")

    s.dim((0, 0), (B, 0), M_(f"b = {B:g}"), off=42, label_off=15)
    s.dim((B, 0), (B, H), M_(f"h = {H:g}"), off=40, label_off=14)
    s.dim((0, 0), (0, D), M_(f"d = {D:g}"), off=-44, label_off=-15)
    s.text_px(s.X(B) + 54, s.Y(H * 0.36),
              f"A_{{cp}} = b×h = {ACP:,.0f} cm²", 12, C["text"], "start",
              weight="700")
    s.text_px(s.X(B) + 54, s.Y(H * 0.36) + 19,
              f"p_{{cp}} = 2(b+h) = {PCP:g} cm", 12, C["text"], "start",
              weight="700")
    s.text_px(s.X(B) + 54, s.Y(H * 0.36) + 42, "D13 閉合箍", 12, C["load"],
              "start")
    s.text_px(s.X(B) + 54, s.Y(H * 0.36) + 60, f"A_{{v}} = {AV:g} cm²", 12,
              C["load"], "start")
    s.text_px(s.X(B) + 54, s.Y(H * 0.36) + 80,
              f"A_{{v,min}} = {AV_MIN:.3f} cm² ✓", 12, C["muted"], "start")

    return compose([e, s], cols=2,
                   title=f"圖 1　{TAG} 懸臂梁偏心均佈載重與臨界斷面",
                   sub=f"b × h = {B:g} × {H:g} cm，d = {D:g} cm，"
                       f"懸臂 {L:g} cm，f'c = {FC:g} kgf/cm²，φ = {PHI:g}",
                   note=f"φVc = {PHI_VC * TF:.2f} tf ＞ Vu = {VU * TF:.3f} tf "
                        f"＞ 0.5φVc = {HALF_PHI_VC * TF:.2f} tf → 混凝土夠、"
                        f"但仍須最小箍筋（這就是題目給 D13 閉合箍的理由）")


# ══════════════════════════════════════════════════════════
# 圖 2　T_th 的單位陷阱
# ══════════════════════════════════════════════════════════
def fig2():
    cases = [
        ("誤用：kgf 直接代 SI 式", f"低估 {TTH_SI / TTH_WRONG:.2f} 倍",
         TTH_WRONG * TFM, M_(f"{TTH_WRONG * TFM:.3f} tf-m"), C["ghost"]),
        ("φT_{th} ← 本題門檻", f"φ = {PHI:g}", PHI_TTH * TFM,
         M_(f"{PHI_TTH * TFM:.3f} tf-m"), C["load"]),
        ("T_{th}（忽略門檻）", "＝ T_{cr} / 4", TTH_SI * TFM,
         M_(f"{TTH_SI * TFM:.3f} tf-m"), C["accent"]),
        ("T_{cr}（裂縫扭矩）", "扭轉裂縫形成", TCR * TFM,
         M_(f"{TCR * TFM:.3f} tf-m"), C["bmd"]),
    ]
    return bar_compare(
        cases,
        title=f"圖 2　扭力門檻的單位陷阱：同一條公式，代錯單位差 {TTH_SI / TTH_WRONG:.2f} 倍",
        sub="規範式以 MPa／mm／N·mm 為基礎；kgf 制的等效係數是 0.265，不是 1/12",
        note=f"Tth = 0.265√f'c·Acp²/pcp = {TTH_KGF:,.0f} kgf·cm，"
             f"與 SI 法 {TTH_SI:,.0f} kgf·cm 差 "
             f"{abs(TTH_KGF / TTH_SI - 1):.1%}（純進位）；"
             f"若代錯單位，emax 會由 {E_MAX:.2f} cm 低估成 {E_WRONG:.2f} cm").svg()


# ══════════════════════════════════════════════════════════
# 圖 3　T = V·e 直線族與 φT_th 門檻
# ══════════════════════════════════════════════════════════
def fig3():
    W, HH = 860, 500
    E_HI = 20.0                                  # cm
    Y_HI = TTH_SI * TFM * 1.45                   # tf·m
    mL, mR, mT, mB = 96, 226, 112, 96
    sc_x = (W - mL - mR) / E_HI
    sc_y = (HH - mT - mB) / Y_HI
    cv = Canvas(W, HH, sx=sc_x, ox=mL, oy=mB, bg="#FFFFFF")
    k = sc_y / sc_x                              # tf·m → 模型單位

    cv.text_px(W / 2, 34, "圖 3　T = V·e 與扭力忽略門檻：門檻反過來讀就是 e 的上限",
               17.0, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               "橫軸：偏心量 e（cm）　縱軸：臨界斷面扭矩 T = V·e（tf·m）",
               12.5, C["muted"])

    # 可忽略扭力的安全區
    cv.polygon([(0, 0), (E_HI, 0), (E_HI, PHI_TTH * TFM * k),
                (0, PHI_TTH * TFM * k)], C["fill_m"], "none")
    cv.text_px(cv.X(E_HI * 0.62), cv.Y(PHI_TTH * TFM * k * 0.45),
               "T_{u} ＜ φT_{th}：扭力可忽略", 13, C["bmd"], weight="700")

    # 兩條門檻
    for val, col, lab in ((TTH_SI * TFM, C["accent"],
                           f"T_{{th}} = {TTH_SI * TFM:.3f} tf·m"),
                          (PHI_TTH * TFM, C["load"],
                           f"φT_{{th}} = {PHI_TTH * TFM:.3f} tf·m")):
        cv.line((0, val * k), (E_HI, val * k), col, 2.0, dash="7 5")
        cv.text_px(cv.X(E_HI) + 12, cv.Y(val * k), lab, 12.5, col, "start",
                   weight="700")

    # T = V·e 直線族
    def line_of(v_kgf, col, w, dash=None):
        pts = [(x, v_kgf * x * TFM * k) for x in
               (E_HI * i / 100 for i in range(101))
               if v_kgf * x * TFM <= Y_HI]
        cv.poly(pts, col, w, dash=dash)
        return pts

    line_of(VU, C["sfd"], 3.0)
    line_of(VU_CAP, C["muted"], 2.2, dash="6 4")

    # 工作點：讀法 A
    cv.dot((E_MAX, PHI_TTH * TFM * k), 6.2, fill=C["sfd"], stroke="#FFFFFF",
           w=1.8)
    cv.line((E_MAX, 0), (E_MAX, PHI_TTH * TFM * k), C["sfd"], 1.4, dash="4 3")
    cv.text_px(cv.X(E_MAX) - 16, cv.Y(PHI_TTH * TFM * k) - 44,
               f"讀法 A（本解）V_{{u}} = {VU * TF:.3f} tf", 12.5, C["sfd"], "end",
               weight="700")
    cv.text_px(cv.X(E_MAX) - 16, cv.Y(PHI_TTH * TFM * k) - 24,
               f"→ e_{{max}} = {E_MAX:.2f} cm", 13.5, C["sfd"], "end",
               weight="700")
    cv.text_px(cv.X(E_MAX), cv.Y(0) + 40, f"e_{{max}} = {E_MAX:.2f}", 12,
               C["sfd"], weight="700")

    # 工作點：讀法 B（容量）
    cv.dot((E_CAP, PHI_TTH * TFM * k), 5.4, fill=C["muted"], stroke="#FFFFFF",
           w=1.8)
    cv.text_px(cv.X(E_CAP) + 10, cv.Y(Y_HI * k * 0.86),
               f"讀法 B（容量）{VU_CAP * TF:.1f} tf", 12, C["muted"], "start")
    cv.text_px(cv.X(E_CAP) + 10, cv.Y(Y_HI * k * 0.86) + 17,
               f"→ e = {E_CAP:.2f} cm", 12, C["muted"], "start")

    # 軸標
    for ev in (0, 5, 10, 15, 20):
        cv.line((ev, 0), (ev, -Y_HI * k * 0.018), C["muted"], 1.3)
        cv.text_px(cv.X(ev), cv.Y(0) + 20, f"{ev:g}", 12, C["muted"])
    for yv in (0.0, 0.4, 0.8, 1.2):
        cv.text_px(cv.X(0) - 12, cv.Y(yv * k), f"{yv:g}", 12, C["muted"], "end")
    cv.arrow((0, 0), (E_HI * 1.02, 0), C["muted"], 1.6, 9)
    cv.arrow((0, 0), (0, Y_HI * k), C["muted"], 1.6, 9)

    cv.text_px(W / 2, HH - 24,
               f"T(x) = Wu·e·(L−x)、V(x) = Wu·(L−x) → T = e·V 與 x 無關，"
               f"故 emax = {E_MAX:.2f} cm 是全梁通用的限制值", 13, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
FIGURES = [
    ("1-beam", fig1,
     "懸臂梁的臨界斷面取到自由端；忘了 D13 閉合箍是最小鋼筋量而非為扭力而設"),
    ("2-threshold", fig2,
     "把 kgf/cm² 與 cm 直接代進 SI 制的 T_th 式（低估 3.19 倍）；"
     "kgf·cm 與 tf·m 換算差 10⁵"),
    ("3-envelope", fig3,
     "把 T = V·e 當成只在臨界斷面成立；「所能承受」讀成容量而未註明"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    checks = [
        ("V_u kgf",         VU,              7425,     1),
        ("固定端 V kgf",      V_FIXED,         8750,     1),
        ("A_cp cm2",        ACP,             2100,     0.1),
        ("p_cp cm",         PCP,             190,      0.1),
        ("f'c MPa",         FC_MPA,          27.46,    0.01),
        ("T_th(SI) N·mm",   TTH_SI_NMM,      1.0136e7, 1e4),
        ("T_th(SI) kgf·cm", TTH_SI,          103354,   10),
        ("T_th(kgf) kgf·cm", TTH_KGF,        102920,   10),
        ("φT_th kgf·cm",    PHI_TTH,         77515,    10),
        ("φT_th tf·m",      PHI_TTH * TFM,   0.775,    0.001),
        ("e_max cm",        E_MAX,           10.44,    0.01),
        ("誤用 T_th kgf·cm", TTH_WRONG,       32363,    10),
        ("誤用倍數",          TTH_SI / TTH_WRONG, 3.19,  0.01),
        ("倍數封閉式",         1000 / (math.sqrt(KGF_PER_MPA) * NCM_PER_KGFCM),
                                              3.19,     0.01),
        ("誤用 e cm",        E_WRONG,         3.3,      0.04),
        ("V_c kgf",         VC,              16451,    5),
        ("φV_c tf",         PHI_VC * TF,     12.34,    0.01),
        ("0.5φV_c tf",      HALF_PHI_VC * TF, 6.17,    0.01),
        ("A_v cm2",         AV,              2.54,     0.001),
        ("A_v,min cm2",     AV_MIN,          0.438,    0.001),
        ("讀法B V tf",       VU_CAP * TF,     61.7,     0.05),
        ("讀法B e cm",       E_CAP,           1.26,     0.01),
        ("T_cr kgf·cm",     TCR,             413418,   40),
    ]
    print(f"── 與 {TAG}.md §4／§5 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<16} 算得 {got:>14.6g}   .md {want:>9}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"
    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<34} 攔：{catches}")


if __name__ == "__main__":
    main()
