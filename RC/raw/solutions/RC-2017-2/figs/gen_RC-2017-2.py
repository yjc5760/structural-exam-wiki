#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2017-2 加大柱新舊混凝土介面剪力與植筋設計 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2017-2.md §1（承 RC-2017-1）給定的原始資料；ε_y、c_b、
     轉折點、翼板各點應力、C_1／C_2／C_c,wing、C'_s、V_u、A_vf、支數、
     V_n 上限與 L_min 全部由 fc_of() / 積分現算，檔尾對 §4 公佈值 assert。
  2. 改 §1 任一數字（含雙折線的兩個轉折）重跑，三張圖跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

雙折線本構（題目指定）：0→0.002 線性升至 1.0f'c；0.002→0.003 線性降至 0.8f'c。
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose
from recipes import bar_compare

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2017-2"


def M_(s):
    assert not any(ord(ch) > 0x2E80 for ch in s), f"math 字串不得含中日韓字元：{s}"
    return s


# ══════════════════════════════════════════════════════════
# §1 原始給定（承 RC-2017-1）
# ══════════════════════════════════════════════════════════
BW = 40.0                       # cm 柱寬（＝介面寬度）
HH = 70.0                       # cm 加大後柱深（彎曲方向）
TW = 15.0                       # cm 每側新混凝土翼板厚
FC = 210.0                      # kgf/cm^2（新舊相同）
FY = 4200.0                     # kgf/cm^2
ES = 2.04e6                     # kgf/cm^2
D_PRIME = 6.5                   # cm 壓力筋（至鋼筋中心）
A_D25 = 5.067                   # cm^2
N_D25 = 4                       # 每側 4 支
A_D19_PAPER = 3.871             # cm^2 原卷給定值（實為 D22）
A_D19_REAL = 2.865              # cm^2 實際 D19
PHI = 0.75                      # 剪力類
MU = 1.0                        # 故意粗糙化、常重混凝土
EPS_CU = 0.003
EPS_PEAK = 0.002                # 雙折線轉折應變
F_AT_CU = 0.8                   # ε=0.003 時之 f_c / f'c

D_EFF = HH - D_PRIME
AS_ROW = N_D25 * A_D25
TF = 1e-3

# ── 平衡點（承 Q1 Part c） ────────────────────────────────
EPS_Y = FY / ES
CB = EPS_CU / (EPS_CU + EPS_Y) * D_EFF
X_PEAK = CB * (1 - EPS_PEAK / EPS_CU)          # ε = 0.002 之位置 = c_b/3


def eps_of(x):
    """距壓力面 x 處之應變（平面保持平面）。"""
    return EPS_CU * (CB - x) / CB


def fc_of(x):
    """題給雙折線本構下的混凝土應力（kgf/cm^2）。"""
    e = eps_of(x)
    if e <= 0:
        return 0.0
    if e <= EPS_PEAK:
        return FC * e / EPS_PEAK                                   # 上升段
    return FC * (1 - (1 - F_AT_CU) * (e - EPS_PEAK) /
                 (EPS_CU - EPS_PEAK))                              # 下降段


F0 = fc_of(0.0)
F_PEAK = fc_of(X_PEAK)
F_IF = fc_of(TW)                               # 介面①處應力
F_BAR = fc_of(D_PRIME)                         # 壓力筋位置之混凝土應力

# 翼板內混凝土壓力：分兩段梯形積分（本構為分段線性，梯形即精確值）
C1 = (F0 + F_PEAK) / 2 * X_PEAK * BW
C2 = (F_PEAK + F_IF) / 2 * (TW - X_PEAK) * BW
CC_WING = C1 + C2
CS_PRIME = (FY - F_BAR) * AS_ROW               # 扣除排開的混凝土
VU = CC_WING + CS_PRIME
TS = FY * AS_ROW                               # 拉力側介面（對照）

# 均勻 0.8f'c 假設（錯誤解法之一）
CC_UNIFORM = F0 * TW * BW

# ── 摩擦剪力法 ────────────────────────────────────────────
def design(vu, ab=A_D19_PAPER):
    avf = vu / (PHI * MU * FY)
    n = math.ceil(avf / ab)
    vn = vu / PHI
    cap = min(0.2 * FC, (3.3 + 0.08 * (FC / 10.197)) * 10.197, 11.0 * 10.197)
    ac = vn / cap
    return dict(vu=vu, avf=avf, n=n, vn=vn, cap=cap, ac=ac, lmin=ac / BW)


MAIN = design(VU)
UNIF = design(CC_UNIFORM)
CONC = design(CC_WING)
MAIN_REAL = design(VU, A_D19_REAL)
S_SPACING = MAIN["lmin"] / MAIN["n"]
L_AVAILABLE = 150.0             # cm 柱淨高 300、反曲點在中央時的可用傳遞長度（§4 Step 7）


# ══════════════════════════════════════════════════════════
# 圖 1　斷面與兩個介面：壓力筋整支埋在新混凝土翼板內
# ══════════════════════════════════════════════════════════
def fig1():
    W, H = 780, 520
    mL, mR, mT, mB = 268, 300, 152, 104
    sx = min((W - mL - mR) / BW, (H - mT - mB) / HH)
    cv = Canvas(W, H, sx=sx, ox=mL, oy=mB, bg="#FFFFFF")

    cv.text_px(W / 2, 34, f"圖 1　{TAG} 加大柱斷面與兩個新舊混凝土介面", 17.0,
               C["text"], weight="700")
    cv.text_px(W / 2, 58,
               f"{BW:g} × {HH:g} cm（原柱 {BW:g} × {HH - 2 * TW:g}，兩側各加 "
               f"{TW:g} cm）　彎曲繞 {HH:g} cm 長邊", 12.5, C["muted"])

    def y(depth):
        """距壓力面 depth（cm）→ 模型 y（壓力面在上）。"""
        return HH - depth

    # 舊核心
    cv.polygon([(0, y(HH - TW)), (BW, y(HH - TW)), (BW, y(TW)), (0, y(TW))],
               "#E3E8EF", C["member"], 2.0)
    # 兩側新混凝土翼板
    for d0, d1 in ((0.0, TW), (HH - TW, HH)):
        cv.polygon([(0, y(d0)), (BW, y(d0)), (BW, y(d1)), (0, y(d1))],
                   C["fill_c"], C["member"], 2.0)
    cv.polygon([(0, y(0)), (BW, y(0)), (BW, y(HH)), (0, y(HH))], "none",
               C["member"], 2.8)

    # 介面①②
    for i, d in enumerate((TW, HH - TW)):
        cv.line((0, y(d)), (BW, y(d)), C["load"], 3.4)
        cv.text_px(cv.X(BW) + 14, cv.Y(y(d)), f"介面{'①②'[i]}（x = {d:g} cm）",
                   12.5, C["load"], "start", weight="700")

    # 鋼筋：兩側各 4-D25，整支埋在新混凝土翼板內
    for d, col, lab in ((D_PRIME, C["compr"], "壓力筋"),
                        (D_EFF, C["tension"], "拉力筋")):
        for i in range(N_D25):
            cv.dot((BW * (0.14 + 0.24 * i), y(d)), 5.6, fill=col,
                   stroke="#FFFFFF", w=1.4)
        cv.text_px(cv.X(BW) + 14, cv.Y(y(d)),
                   f"{N_D25}-D25 {lab}（x = {d:g}）", 12, col, "start",
                   weight="700")

    cv.text_px(cv.X(BW / 2), cv.Y(y(TW * 0.86)), "新混凝土", 12, C["compr"])
    cv.text_px(cv.X(BW / 2), cv.Y(y(HH / 2)), "舊混凝土", 12.5, C["muted"],
               weight="700")
    cv.text_px(cv.X(BW / 2), cv.Y(y(HH - TW * 0.86)), "新混凝土", 12, C["compr"])

    cv.dim((0, y(0)), (BW, y(0)), M_(f"b = {BW:g}"), off=-36, label_off=-13)
    cv.dim((0, y(0)), (0, y(TW)), M_(f"tw = {TW:g}"), off=42, label_off=15)
    cv.dim((0, y(TW)), (0, y(HH - TW)), M_(f"{HH - 2 * TW:g}"), off=42,
           label_off=15)
    cv.dim((0, y(HH - TW)), (0, y(HH)), M_(f"tw = {TW:g}"), off=42, label_off=15)
    cv.dim((BW, y(0)), (BW, y(HH)), M_(f"h = {HH:g}"), off=-104, label_off=-15)

    cv.text_px(cv.X(0) - 154, cv.Y(y(0)), "壓力面", 12.5, C["compr"], "start",
               weight="700")
    cv.text_px(cv.X(0) - 154, cv.Y(y(HH)), "拉力面", 12.5, C["tension"], "start",
               weight="700")

    gy = H - 62
    cv.text_px(W / 2, gy,
               f"d' = {D_PRIME:g} ＜ tw = {TW:g} → 壓力筋整支埋在新混凝土翼板內，"
               f"它的 {CS_PRIME * TF:.1f} tf 同樣必須跨越介面", 12.5, C["accent"],
               weight="700")
    cv.text_px(W / 2, gy + 22,
               f"每側翼板斷面積 A_{{wing}} = {TW:g} × {BW:g} = {TW * BW:,.0f} cm²；"
               f"介面為垂直平面，各寬 {BW:g} cm、沿柱高延伸", 12.5, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 2　翼板內雙折線應力分布：分段積分 vs 均勻 0.8f'c
# ══════════════════════════════════════════════════════════
def fig2():
    PW, PH = 440, 540
    mT, mB = 122, 118
    sc = (PH - mT - mB) / HH                    # 兩格共用之垂直比例
    SSC = 0.2667                                # 1 kgf/cm^2 → 模型長度

    def y(depth):
        return HH - depth

    # ---- 左：斷面（僅為對位用，尺度與右格相同） ----
    p1 = Canvas(PW, PH, sx=sc, ox=PW / 2 - BW * sc / 2, oy=mB)
    p1.panel("斷面", f"深度尺度與右圖共用（{HH:g} cm）")
    p1.polygon([(0, y(HH - TW)), (BW, y(HH - TW)), (BW, y(TW)), (0, y(TW))],
               "#E3E8EF", C["member"], 1.8)
    for d0, d1 in ((0.0, TW), (HH - TW, HH)):
        p1.polygon([(0, y(d0)), (BW, y(d0)), (BW, y(d1)), (0, y(d1))],
                   C["fill_c"], C["member"], 1.8)
    p1.line((0, y(TW)), (BW, y(TW)), C["load"], 3.0)
    p1.line((0, y(HH - TW)), (BW, y(HH - TW)), C["load"], 3.0)
    p1.line((-2, y(CB)), (BW + 2, y(CB)), C["accent"], 2.0, dash="6 4")
    p1.text_px(p1.X(BW) + 6, p1.Y(y(CB)), "N.A.", 11.5, C["accent"], "start",
               weight="700")
    for d, col in ((D_PRIME, C["compr"]), (D_EFF, C["tension"])):
        for i in range(N_D25):
            p1.dot((BW * (0.14 + 0.24 * i), y(d)), 4.8, fill=col,
                   stroke="#FFFFFF", w=1.2)
    p1.dim((0, y(0)), (0, y(TW)), M_(f"tw = {TW:g}"), off=34, label_off=13)
    p1.dim((0, y(0)), (0, y(CB)), M_(f"cb = {CB:.2f}"), off=74, label_off=15)

    # ---- 右：應力分布 ----
    p2 = Canvas(PW, PH, sx=sc, ox=104, oy=mB)
    p2.panel("雙折線應力分布", "翼板內應力不是常數，須分段積分")
    p2.line((0, y(0)), (0, y(HH)), C["ghost"], 1.6, dash="5 4")

    # 均勻 0.8f'c 假設（灰虛線矩形，供對照）
    p2.poly([(0, y(0)), (F0 * SSC, y(0)), (F0 * SSC, y(TW)), (0, y(TW))],
            C["muted"], 1.8, dash="5 4")

    # 翼板段（0 ~ tw）填色：介面必須傳遞的混凝土壓力
    seg1 = [X_PEAK * i / 40 for i in range(41)]
    seg2 = [X_PEAK + (TW - X_PEAK) * i / 20 for i in range(21)]
    p2.polygon([(0, y(0))] + [(fc_of(d) * SSC, y(d)) for d in seg1 + seg2]
               + [(0, y(TW))], C["fill_c"], "none")

    # 應力曲線（壓力面 → 中性軸）
    ds = [CB * i / 240 for i in range(241)]
    p2.poly([(fc_of(d) * SSC, y(d)) for d in ds], C["compr"], 2.8)

    # 介面①與轉折點的水平參考線（標註放左側，避開曲線）
    p2.line((0, y(TW)), (F0 * 1.30 * SSC, y(TW)), C["load"], 3.0)
    p2.text_px(20, p2.Y(y(TW)) + 15, f"介面① x = {TW:g}", 11.5, C["load"],
               "start", weight="700")
    p2.line((0, y(X_PEAK)), (F_PEAK * 1.06 * SSC, y(X_PEAK)), C["accent"], 1.4,
            dash="4 3")
    p2.text_px(20, p2.Y(y(X_PEAK)) - 12, f"轉折 x = {X_PEAK:.2f}", 11.5,
               C["accent"], "start", weight="700")
    p2.line((0, y(CB)), (18 * SSC, y(CB)), C["accent"], 1.8, dash="6 4")
    p2.text_px(20, p2.Y(y(CB)), f"N.A. x = {CB:.2f}", 11.5, C["accent"], "start")

    # 三個關鍵應力值（標在曲線右側）
    for d, lab, dy in ((0.0, f"{F0:.1f}", -4), (X_PEAK, f"{F_PEAK:.1f}", -4),
                       (TW, f"{F_IF:.1f}", 14)):
        p2.dot((fc_of(d) * SSC, y(d)), 5.0, fill=C["compr"], stroke="#FFFFFF",
               w=1.6)
        p2.math_px(p2.X(fc_of(d) * SSC) + 11, p2.Y(y(d)) + dy, M_(lab), 13,
                   C["compr"], "start", weight="700")

    # 壓力筋位置（引線拉到左側標註槽）
    p2.dot((F_BAR * SSC, y(D_PRIME)), 5.0, fill=C["tension"], stroke="#FFFFFF",
           w=1.6)
    p2.line((0, y(D_PRIME)), (F_BAR * SSC, y(D_PRIME)), C["tension"], 1.2,
            dash="3 3")
    p2.text_px(20, p2.Y(y(D_PRIME)) - 11, f"壓力筋 x = {D_PRIME:g}", 11.5,
               C["tension"], "start", weight="700")
    p2.text_px(20, p2.Y(y(D_PRIME)) + 7, f"該處 f_c = {F_BAR:.2f}", 11.5,
               C["tension"], "start")

    p2.text_px(p2.X(F0 * 0.30 * SSC), p2.Y(y(X_PEAK * 0.40)),
               f"C1 = {C1 * TF:.1f} tf", 12, C["compr"], weight="700")
    p2.text_px(p2.X(F0 * 0.30 * SSC), p2.Y(y(X_PEAK * 0.40)) + 18,
               f"C2 = {C2 * TF:.1f} tf", 12, C["compr"])
    p2.text_px(p2.X(F0 * 0.42 * SSC), p2.Y(y(TW)) + 42,
               f"灰虛線＝均勻 0.8f'c = {CC_UNIFORM * TF:.1f} tf", 11.5,
               C["muted"])
    p2.text_px(PW / 2, PH - 72, f"分段積分 C_c,wing = {CC_WING * TF:.1f} tf",
               13, C["compr"], weight="700")
    p2.text_px(PW / 2, PH - 50,
               f"均勻假設低估 {1 - CC_UNIFORM / CC_WING:.1%}", 12.5, C["muted"])

    return compose([p1, p2], cols=2,
                   title="圖 2　平衡點時壓力側翼板的應力分布：轉折點就落在翼板內",
                   sub=f"c_b = {CB:.2f} cm，雙折線轉折（ε = {EPS_PEAK:g}）在 "
                       f"x = c_b/3 = {X_PEAK:.2f} cm ＜ tw = {TW:g} cm",
                   note=f"翼板內側應變只有 {eps_of(TW):.5f}，應力 {F_IF:.1f} 反而"
                        f"比壓力面的 {F0:.1f} 高——雙折線在 ε = {EPS_PEAK:g} 有峰值，"
                        f"均勻假設把整個翼板當成 ε = {EPS_CU:g} 才會低估")


# ══════════════════════════════════════════════════════════
# 圖 3　介面設計剪力的三種定義
# ══════════════════════════════════════════════════════════
def fig3():
    cases = [
        ("拉力側介面（對照）", f"Ts = fy·As = {TS * TF:.1f} tf", TS * TF,
         M_(f"{TS * TF:.1f} tf"), C["tension"]),
        ("均勻 0.8f'c", f"{UNIF['n']} 支，Lmin {UNIF['lmin']:.0f} cm",
         CC_UNIFORM * TF, M_(f"{CC_UNIFORM * TF:.1f} tf"), C["ghost"]),
        ("雙折線・只計混凝土", f"{CONC['n']} 支，Lmin {CONC['lmin']:.0f} cm",
         CC_WING * TF, M_(f"{CC_WING * TF:.1f} tf"), C["muted"]),
        ("雙折線＋壓力筋 ← 本解", f"{MAIN['n']} 支，Lmin {MAIN['lmin']:.0f} cm",
         VU * TF, M_(f"{VU * TF:.1f} tf"), C["load"]),
    ]
    return bar_compare(
        cases,
        title="圖 3　介面設計剪力該取哪一個定義：三種算法差到兩倍",
        sub="介面剪力＝新混凝土翼板在該斷面承擔的「全部」軸力（混凝土＋埋在其中的鋼筋）",
        note=f"本解 Vu = {VU * TF:.1f} tf → Avf = {MAIN['avf']:.2f} cm²、"
             f"D19 {MAIN['n']} 支/介面（實際 D19 面積則需 {MAIN_REAL['n']} 支）；"
             f"Lmin = {MAIN['lmin']:.1f} cm ＞ 可用長度約 {L_AVAILABLE:g} cm → "
             f"卡在 0.2f'c·Ac 上限，多打植筋沒用").svg()


# ══════════════════════════════════════════════════════════
FIGURES = [
    ("1-interface", fig1,
     "漏算落在翼板內的壓力筋力（低估 42%）；把介面當水平面或只設計壓力側"),
    ("2-stress", fig2,
     "假設翼板應力均勻 0.8f'c（低估 12%）；忘了雙折線峰值就在翼板內"),
    ("3-definition", fig3,
     "介面剪力定義選錯；以為多打植筋就能過（實際卡在介面應力上限）"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    checks = [
        ("ε_y",           EPS_Y,              0.002059, 1e-6),
        ("c_b cm",        CB,                 37.66,    0.01),
        ("x_peak cm",     X_PEAK,             12.55,    0.01),
        ("f_c(0)",        F0,                 168.0,    0.05),
        ("f_c(peak)",     F_PEAK,             210.0,    0.05),
        ("f_c(15)",       F_IF,               189.5,    0.05),
        ("ε(15)",         eps_of(TW),         0.00181,  1e-5),
        ("f_c(d') ",      F_BAR,              189.75,   0.05),
        ("C1 kgf",        C1,                 94896,    3),
        ("C2 kgf",        C2,                 19558,    6),
        ("C_c,wing kgf",  CC_WING,            114454,   8),
        ("A's cm2",       AS_ROW,             20.27,    0.01),
        ("C's kgf",       CS_PRIME,           81288,    10),
        ("V_u kgf",       VU,                 195742,   16),
        ("T_s kgf",       TS,                 85134,    10),
        ("均勻 kgf",       CC_UNIFORM,         100800,   1),
        ("A_vf cm2",      MAIN["avf"],        62.14,    0.01),
        ("D19 支數",       MAIN["n"],          17,       0),
        ("V_n kgf",       MAIN["vn"],         260989,   20),
        ("介面上限",        MAIN["cap"],        42.0,     0.01),
        ("L_min cm",      MAIN["lmin"],       155.4,    0.1),
        ("間距 cm",        S_SPACING,          9.1,      0.05),
        ("實際 D19 支數",   MAIN_REAL["n"],     22,       0),
        ("均勻 支數",       UNIF["n"],          9,        0),
        ("均勻 L_min cm",  UNIF["lmin"],       80.0,     0.05),
        ("只混凝土 支數",    CONC["n"],          10,       0),
        ("只混凝土 L_min",  CONC["lmin"],       90.8,     0.3),
    ]
    print(f"── 與 {TAG}.md §4／§5 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<14} 算得 {got:>14.6g}   .md {want:>9}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"
    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<34} 攔：{catches}")


if __name__ == "__main__":
    main()
