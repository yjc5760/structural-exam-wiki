#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2014-3 軸力對混凝土剪力強度 V_c 的三條規範路徑 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2014-3.md §1 給定的原始資料；ρ_w、V_u、M_u、V_ud/M_u、M_m、
     軸壓加強上限、軸拉折減因子、三個 V_c 與歸零點全部由 vc_of() 現算，
     檔尾對 §4 公佈值 assert。
  2. 改 §1 任一數字重跑，三張圖跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

規範：土木 401-100（原卷指定）。軸壓 N_u > 0、軸拉 N_u < 0。
BMD 一律繪於受拉側（簡支梁下垂彎矩 → 畫在軸線下方）。
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose
from recipes import bar_compare, plot_function

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2014-3"


def M_(s):
    """FONT_M（數學襯線）缺中日韓字，cairosvg 會靜默丟字 → 守衛。"""
    assert not any(ord(ch) > 0x2E80 for ch in s), f"math 字串不得含中日韓字元：{s}"
    return s


# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
B, D, H = 30.0, 60.0, 70.0      # cm 梁寬、有效深度、梁高
FC = 280.0                      # kgf/cm^2
WU = 50.0                       # kgf/cm（= 5 tf/m）
L = 500.0                       # cm 跨距（簡支）
AS = 24.42                      # cm^2（3-D32）
NU_C = +25000.0                 # Case 2 軸壓（正）
NU_T = -25000.0                 # Case 3 軸拉（負）

SQFC = math.sqrt(FC)
BWD = B * D
AG = B * H
RHO_W = AS / BWD
TF, TFM = 1e-3, 1e-5

# ── 臨界斷面（距支承面 d，三條件均成立） ──────────────────
R_SUP = WU * L / 2
VU = R_SUP - WU * D
MU = R_SUP * D - WU * D ** 2 / 2
VD_M = VU * D / MU
ARM = (4 * H - D) / 8                       # 27.5 cm
VC_CAP0 = 0.93 * SQFC * BWD                 # 無軸力之基本上限
VC_SIMPLE = 0.53 * SQFC * BWD               # 簡化式（參考）
NU_ZERO = -AG / 0.0284                      # 軸拉使 V_c 歸零之軸力


def vc_detail(mm, clip=True):
    """詳細式。clip=True 時 V_ud/M_m 受 1.0 限制（無軸力／軸拉才有此限）。"""
    r = VU * D / mm
    if clip:
        r = min(r, 1.0)
    return (0.50 * SQFC + 175 * RHO_W * r) * BWD


def vc_cap_comp(nu):
    """軸壓加強後的上限：0.93√f'c·b_w·d·√(1+0.0284 N_u/A_g)。"""
    return VC_CAP0 * math.sqrt(1 + 0.0284 * nu / AG)


def vc_of(nu):
    """土木 401-100 的三條路徑；回傳 (V_c, 路徑代號)。"""
    if nu > 0:                                     # 軸壓
        cap = vc_cap_comp(nu)
        mm = MU - nu * ARM
        if mm <= 0:
            return cap, "cap"
        return min(vc_detail(mm, clip=False), cap), "detail+cap"
    if nu == 0:                                    # 無軸力
        return min(vc_detail(MU), VC_CAP0), "detail"
    return max(0.53 * (1 + 0.0284 * nu / AG) * SQFC * BWD, 0.0), "tension"


VC1, _ = vc_of(0.0)
VC2, _ = vc_of(NU_C)
VC3, _ = vc_of(NU_T)
MM2 = MU - NU_C * ARM
KAPPA = math.sqrt(1 + 0.0284 * NU_C / AG)
LAMBDA_T = 1 + 0.0284 * NU_T / AG
NU_MM0 = MU / ARM                               # M_m 由正轉負的軸力

# 坊間另一讀法（軸拉硬套 M_m 路徑），留檔對照
MM3_ALT = MU - NU_T * ARM
VC3_ALT = vc_detail(MM3_ALT)

# ACI 318-19 / 土木 401-112 對照（§5-⑤）
def vc_318_19(nu):
    return VC_SIMPLE + nu / (6 * AG) * BWD


VC19 = {k: vc_318_19(v) for k, v in (("c1", 0.0), ("c2", NU_C), ("c3", NU_T))}


# ══════════════════════════════════════════════════════════
# 圖 1　臨界斷面：載重／SFD／BMD 三聯圖
# ══════════════════════════════════════════════════════════
def fig1():
    PW, PHP = 800, 244
    sx = (PW - 210) / L
    pad = 108
    n = 101
    xs = [L * i / (n - 1) for i in range(n)]
    v = [(R_SUP - WU * x) * TF for x in xs]
    m = [(R_SUP * x - WU * x * x / 2) * TFM for x in xs]

    def crit(cv, ytop_model):
        cv.line((D, 0), (D, ytop_model), C["load"], 2.2, dash="6 4")

    # ---- 載重與支承 ----
    top = Canvas(PW, PHP, sx=sx, ox=pad, oy=PHP * 0.40)
    top.panel("載重與支承", "簡支梁，均佈載重自梁頂施加")
    top.line((0, 0), (L, 0), C["member"], 6, cap="butt")
    top.support((0, 0), "pin"); top.support((L, 0), "roller")
    top.udl((0, 0), (L, 0), 0.078 * L, n=11)
    top.math_px(top.X(L / 2), top.Y(0.078 * L) - 16, M_("w_{u} = 5 tf/m"), 14.5,
                C["load"], weight="700")
    top.line((D, -0.06 * L), (D, 0.09 * L), C["load"], 2.4)
    top.text_px(top.X(D) + 8, top.Y(0) + 30, "臨界斷面（距支承面 d）", 12,
                C["load"], "start", weight="700")
    top.dim((0, 0), (D, 0), M_(f"d = {D:g}"), off=38, label_off=14)
    top.dim((D, 0), (L, 0), M_(f"{L - D:g}"), off=38, label_off=14)

    # ---- SFD / BMD ----
    def strip(vals, color, fill, name, sub, unit, keys, flip=False):
        top_px, bot_px = 76, 38
        vmax, vmin = max(max(vals), 0.0), min(min(vals), 0.0)
        rng = (vmax - vmin) or 1.0
        px_per = (PHP - top_px - bot_px) / rng
        cv = Canvas(PW, PHP, sx=sx, ox=pad,
                    oy=PHP - (top_px + vmax * px_per))
        cv.panel(name, sub)
        plot_function(cv, xs, vals, px_per / sx, 0.0, 0.0, color, fill, marks=keys)
        cv.text_px(pad - 14, cv.Y(0), "0", 12, C["muted"], "end")
        cv.text_px(PW - 24, 34, unit, 12, C["muted"], "end")
        cv.line((D, 0), (D, vals[int(D / L * (n - 1))] * px_per / sx),
                C["load"], 2.0, dash="5 4")
        return cv

    key_v = [(0.0, M_(f"R = {R_SUP * TF:.2f} tf"), -16),
             (D, M_(f"V_u = {VU * TF:.2f} tf"), -16)]
    key_m = [(D, M_(f"M_u = {MU * TFM:.2f} tf-m"), 20),
             (L / 2, M_(f"{WU * L * L / 8 * TFM:.3f}"), 20)]

    mid = strip(v, C["sfd"], C["fill_s"], "剪力圖 SFD", "支承面 → 臨界斷面遞減",
                "tf", key_v)
    bot = strip([-x for x in m], C["bmd"], C["fill_m"], "彎矩圖 BMD",
                "繪於受拉側（簡支梁下垂 → 軸線下方）", "tf·m", key_m)

    return compose([top, mid, bot], cols=1,
                   title=f"圖 1　{TAG} 臨界斷面位置與該處的 Vu、Mu",
                   sub=f"bw × d = {B:g} × {D:g} cm　h = {H:g} cm　"
                       f"跨距 {L:g} cm　As = {AS:g} cm²（ρw = {RHO_W:.5f}）",
                   note=f"Vu·d / Mu = {VD_M:.4f} ≤ 1.0（無軸力／軸拉時此限制須檢核；"
                        f"軸壓改用 Mm 後解除）")


# ══════════════════════════════════════════════════════════
# 圖 2　V_c 隨軸力變化：兩條規範路徑與歸零點
# ══════════════════════════════════════════════════════════
def fig2():
    W, HH = 900, 530
    NLO, NHI = -86000.0, 46000.0            # kgf
    n = 529
    ns = [NLO + (NHI - NLO) * i / (n - 1) for i in range(n)]
    vs = [vc_of(x)[0] * TF for x in ns]

    mL, mR, mT, mB = 92, 196, 112, 108
    ytop = 37.0                              # tf
    sc_x = (W - mL - mR) / (NHI - NLO)
    sc_y = (HH - mT - mB) / ytop
    cv = Canvas(W, HH, sx=sc_x, ox=mL - NLO * sc_x, oy=mB, bg="#FFFFFF")
    k = sc_y / sc_x                          # tf → 模型單位

    cv.text_px(W / 2, 34, "圖 2　Vc 隨軸力的變化：軸壓抬高天花板、軸拉線性折減",
               17.0, C["text"], weight="700")
    cv.text_px(W / 2, 58, "橫軸：設計軸力 Nu（tf，壓為正）　縱軸：混凝土剪力強度 Vc（tf）",
               12.5, C["muted"])

    # 座標軸
    cv.arrow((NLO, 0), (NHI, 0), C["muted"], 1.6, 9)
    cv.line((0, 0), (0, ytop * k), C["muted"], 1.4, dash="5 4")

    # 參考水平線（中英混排 → 用 text_px，不用 math_px）
    for val, col, lab in ((VC_CAP0 * TF, C["ghost"],
                           f"基本上限 {VC_CAP0 * TF:.2f} tf"),
                          (VC_SIMPLE * TF, C["muted"],
                           f"簡化式 {VC_SIMPLE * TF:.2f} tf")):
        cv.line((NLO, val * k), (NHI, val * k), col, 1.6, dash="7 5")
        cv.text_px(cv.X(NHI) + 12, cv.Y(val * k), lab, 12, col, "start")

    # 規範路徑曲線
    cv.poly([(x, y * k) for x, y in zip(ns, vs)], C["bmd"], 3.0)

    # 三個工作點（標註各自避開曲線）
    def mark(nu, vc, col, lab, anchor, dx, dy):
        cv.dot((nu, vc * TF * k), 6.0, fill=col, stroke="#FFFFFF", w=1.8)
        cv.text_px(cv.X(nu) + dx, cv.Y(vc * TF * k) + dy,
                   f"{lab}　{vc * TF:.2f} tf", 12.5, col, anchor, weight="700")

    mark(NU_T, VC3, C["tension"], "Case 3 軸拉 −25 tf：專用式", "end", -14, 24)
    mark(0.0, VC1, C["bmd"], "Case 1 無軸力：詳細式", "end", -16, -26)
    mark(NU_C, VC2, C["compr"], "Case 2 軸壓 +25 tf：Mm ≤ 0 → 上限", "end", -14, -22)

    # 常見錯誤：軸壓忘乘 κ（自 cap 線垂直拉到工作點）
    cv.dot((NU_C, VC_CAP0 * TF * k), 5.2, fill="#FFFFFF", stroke=C["muted"], w=2.0)
    cv.line((NU_C, VC_CAP0 * TF * k), (NU_C, VC2 * TF * k), C["accent"], 1.8,
            dash="4 3")
    ymid = (VC_CAP0 + VC2) / 2 * TF * k
    cv.text_px(cv.X(NU_C) + 12, cv.Y(ymid) - 14, f"× {KAPPA:.4f} 加強因子", 12,
               C["accent"], "start", weight="700")
    cv.text_px(cv.X(NU_C) + 12, cv.Y(ymid) + 4, f"漏乘就得 {VC_CAP0 * TF:.2f} tf", 12,
               C["accent"], "start")

    # 軸拉歸零點
    cv.dot((NU_ZERO, 0), 5.4, fill=C["tension"], stroke="#FFFFFF", w=1.6)
    cv.text_px(cv.X(NU_ZERO) + 8, cv.Y(0) + 44,
               f"Nu = {NU_ZERO * TF:.1f} tf → Vc 歸零", 12, C["tension"],
               "start", weight="700")

    # M_m 由正轉負的分界
    cv.line((NU_MM0, 0), (NU_MM0, ytop * k * 0.60), C["muted"], 1.3, dash="3 4")
    cv.text_px(cv.X(NU_MM0), cv.Y(0) + 44, f"Mm = 0 @ {NU_MM0 * TF:.0f} tf", 11.5,
               C["muted"])

    # 規範分流造成的跳階（Nu = 0 兩側用不同式子）
    cv.line((0, VC_SIMPLE * TF * k), (0, VC1 * TF * k), C["accent"], 1.6,
            dash="4 3")
    cv.text_px(cv.X(0) - 16, cv.Y((VC_SIMPLE + VC1) / 2 * TF * k), "規範分流跳階",
               11.5, C["accent"], "end")

    # 軸標
    for nv in (-80, -60, -40, -20, 20, 40):
        cv.line((nv * 1000, 0), (nv * 1000, -ytop * k * 0.016), C["muted"], 1.3)
        cv.text_px(cv.X(nv * 1000), cv.Y(0) + 20, f"{nv:g}", 12, C["muted"])
    cv.text_px(cv.X(0), cv.Y(0) + 20, "0", 12, C["muted"])
    for yv in (0, 10, 20, 30):
        cv.text_px(cv.X(NLO) - 12, cv.Y(yv * k), f"{yv:g}", 12, C["muted"], "end")

    cv.text_px(W / 2, HH - 26,
               f"趨勢檢核：軸壓 {VC2 * TF:.2f} ＞ 無軸力 {VC1 * TF:.2f} ＞ "
               f"軸拉 {VC3 * TF:.2f} tf，單調且符合物理直覺", 13, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 3　五個 V_c 候選值同時攤開
# ══════════════════════════════════════════════════════════
def fig3():
    cases = [
        ("Case 3 軸拉 −25 tf", f"折減因子 {LAMBDA_T:.4f}", VC3 * TF,
         M_(f"V_c = {VC3 * TF:.2f} tf"), C["tension"]),
        ("簡化式（無軸力）", "保守估算用", VC_SIMPLE * TF,
         M_(f"0.53*sqrt(f'c)*bw*d = {VC_SIMPLE * TF:.2f}"), C["muted"]),
        ("Case 1 無軸力", f"Vu·d/Mu = {VD_M:.4f}", VC1 * TF,
         M_(f"V_c = {VC1 * TF:.2f} tf"), C["bmd"]),
        ("誤答：軸壓漏因子", f"低估 {1 - VC_CAP0 / VC2:.1%}", VC_CAP0 * TF,
         M_(f"0.93*sqrt(f'c)*bw*d = {VC_CAP0 * TF:.2f}"), C["ghost"]),
        ("Case 2 軸壓 +25 tf", f"Mm = {MM2:,.0f} ＜ 0 → 上限", VC2 * TF,
         M_(f"V_c = {VC2 * TF:.2f} tf"), C["compr"]),
    ]
    return bar_compare(
        cases,
        title="圖 3　同一斷面、同一臨界位置，三種軸力狀態的 Vc",
        sub="長條以最大值為 100%；灰色那一列是「軸壓上限忘了乘 √(1+0.0284Nu/Ag)」的錯誤答案",
        note=f"軸壓加強因子 √(1+0.0284×{NU_C / AG:.3f}) = {KAPPA:.4f}；"
             f"漏掉它就把 {VC2 * TF:.2f} tf 寫成 {VC_CAP0 * TF:.2f} tf（低估 "
             f"{1 - VC_CAP0 / VC2:.1%}）").svg()


# ══════════════════════════════════════════════════════════
FIGURES = [
    ("1-critical", fig1,
     "臨界斷面自支承中心起算；V_u·d/M_u 的 1.0 限制忘了檢核"),
    ("2-nu-curve", fig2,
     "N_u 符號搞混、軸壓上限漏乘加強因子、以為軸拉也走 M_m 路徑"),
    ("3-compare", fig3,
     "把 0.93√f'c·b_w·d 當成軸壓時的上限（低估 13.5%）"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    checks = [
        ("ρ_w",            RHO_W,          0.01357,  1e-5),
        ("√f'c",           SQFC,           16.733,   0.001),
        ("A_g cm2",        AG,             2100,     0.1),
        ("V_u kgf",        VU,             9500,     1),
        ("M_u kgf·cm",     MU,             660000,   1),
        ("V_ud/M_u",       VD_M,           0.8636,   1e-4),
        ("(4h−d)/8 cm",    ARM,            27.5,     0.01),
        ("基本上限 kgf",     VC_CAP0,        28011,    2),
        ("簡化式 kgf",       VC_SIMPLE,      15963,    2),
        ("Case1 V_c kgf",  VC1,            18751,    2),
        ("M_m kgf·cm",     MM2,            -27500,   1),
        ("κ 加強因子",       KAPPA,          1.1568,   1e-3),
        ("Case2 V_c kgf",  VC2,            32402,    3),
        ("軸拉折減因子",      LAMBDA_T,       0.6619,   1e-4),
        ("Case3 V_c kgf",  VC3,            10566,    2),
        ("歸零 N_u tf",     NU_ZERO * TF,   -73.9,    0.05),
        ("軸拉套 Mm kgf",   VC3_ALT,        16868,    2),
        ("318-19 C1 tf",   VC19["c1"] * TF, 15.96,   0.01),
        ("318-19 C2 tf",   VC19["c2"] * TF, 19.53,   0.01),
        ("318-19 C3 tf",   VC19["c3"] * TF, 12.39,   0.01),
    ]
    print(f"── 與 {TAG}.md §4／§5 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<15} 算得 {got:>14.6g}   .md {want:>10}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"
    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<34} 攔：{catches}")


if __name__ == "__main__":
    main()
