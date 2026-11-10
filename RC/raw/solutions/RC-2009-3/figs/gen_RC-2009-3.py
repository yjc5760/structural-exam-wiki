#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2009-3 深梁壓拉桿模式（STM）最大載重與破壞模式 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2009-3.md §1 給定的原始資料（含七段尺寸鏈）；L、a、z、θ、
     T、F_diag、w_s、五個限制的 P 上限全部由 stm() 現算，檔尾對 §4 公佈值 assert。
  2. 改尺寸鏈或任一材料數字重跑，四張圖跟著變（讀法 B 即以同一函式代不同 a 求得）。
  3. FIGURES 表寫明每張圖攔什麼錯。

ACI 318-14 主線：β_s（瓶形＋腹筋）= 0.75、β_s（棱柱／邊界）= 1.0、
β_n（CCT）= 0.80、β_n（CCC）= 1.0；題目指定 φ = 1.0。
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose
from recipes import bar_compare, truss_forces

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2009-3"


def M_(s):
    assert not any(ord(ch) > 0x2E80 for ch in s), f"math 字串不得含中日韓字元：{s}"
    return s


# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
HH = 70.0                       # cm 梁高
BW = 20.0                       # cm 梁寬
CHAIN = [20.0, 30.0, 20.0, 30.0, 20.0, 30.0, 20.0]   # 底部七段尺寸鏈
LB = 20.0                       # cm 承壓鈑／載重鈑寬（＝鏈中四段 20）
HC = 20.0                       # cm 純彎區水平壓桿寬（題目明給）
HT = 20.0                       # cm 拉力桿分布範圍 → CCT 節點高
N_BAR, A_D19 = 6, 2.87          # 6-D19
FC, FY = 250.0, 4200.0          # kgf/cm^2
PHI = 1.0                       # 題目指定不考慮強度折減
BETA_S_BOTTLE, BETA_S_PRISM = 0.75, 1.00
BETA_N_CCT, BETA_N_CCC = 0.80, 1.00

AS = N_BAR * A_D19
TF = 1e-3

# ── 由尺寸鏈定幾何（累加 → 各鈑中心） ─────────────────────
EDGE = [0.0]
for seg in CHAIN:
    EDGE.append(EDGE[-1] + seg)
TOTAL = EDGE[-1]
CEN = [(EDGE[i] + EDGE[i + 1]) / 2 for i in (0, 2, 4, 6)]   # 四塊鈑中心
X_SUP_L, X_LOAD_L, X_LOAD_R, X_SUP_R = CEN
SPAN = X_SUP_R - X_SUP_L                 # 支承跨度
A_SHEAR = X_LOAD_L - X_SUP_L             # 剪力跨
PURE_BEND = (EDGE[3], EDGE[4])           # 純彎區（中央 30 cm）

E_T = HT / 2                             # 拉力桿形心距底
E_C = HC / 2                             # 水平壓桿形心距頂
Z = HH - E_C - E_T                       # 力臂
D_EFF = HH - E_T
FCE_BOTTLE = 0.85 * BETA_S_BOTTLE * FC
FCE_PRISM = 0.85 * BETA_S_PRISM * FC
FCE_CCT = 0.85 * BETA_N_CCT * FC
FCE_CCC = 0.85 * BETA_N_CCC * FC


def stm(a, z=Z, lb=LB, ht=HT, hc=HC):
    """給定剪力跨 a，回傳 STM 幾何、桿力係數與五項 P 上限（kgf）。"""
    th = math.atan2(z, a)
    sn, cs = math.sin(th), math.cos(th)
    kT = 0.5 * a / z                     # T / P
    kD = 0.5 / sn                        # F_diag / P
    ws = lb * sn + ht * cs               # 節點處斜壓桿寬
    lim = {
        "tie": AS * FY / kT,
        "strut_diag": FCE_BOTTLE * ws * BW / kD,
        "strut_horiz": FCE_PRISM * hc * BW / kT,
        "cct": min(FCE_CCT * lb * BW / 0.5,        # 承壓面（反力 P/2）
                   FCE_CCT * ht * BW / kT,         # 背面（拉桿面）
                   FCE_CCT * ws * BW / kD),        # 斜壓桿面
        "ccc": min(FCE_CCC * lb * BW / 0.5,
                   FCE_CCC * ws * BW / kD,
                   FCE_CCC * hc * BW / kT),
    }
    return dict(theta=math.degrees(th), sin=sn, cos=cs, kT=kT, kD=kD, ws=ws,
                lim=lim, pmax=min(lim.values()),
                control=min(lim, key=lim.get))


A_ = stm(A_SHEAR)                                    # 讀法 A（本解）
B_ = stm(EDGE[1] - EDGE[0] + CHAIN[1] - CHAIN[1])    # 佔位，下一行覆寫
B_ = stm(30.0)                                       # 讀法 B（30 cm 誤讀為淨跨）

PMAX = A_["pmax"]
T_AT_PMAX = A_["kT"] * PMAX
W_T = T_AT_PMAX / (FCE_CCT * BW)                     # 拉力桿於節點內所需寬度
SIG_FACE = A_["kD"] * PMAX / (A_["ws"] * BW)         # 斜壓桿面應力 @ P_max
PHI_PMAX = 0.75 * PMAX                              # 若依 318-19 取 φ = 0.75

FACE_ORDER = ["strut_diag", "cct", "tie", "ccc", "strut_horiz"]
FACE_NAME = {"tie": "拉力桿降伏", "strut_diag": "斜向壓桿（瓶形）",
             "strut_horiz": "純彎區水平壓桿", "cct": "CCT 節點（三面）",
             "ccc": "CCC 節點（三面）"}


# ══════════════════════════════════════════════════════════
# 圖 1　題目重繪：七段尺寸鏈
# ══════════════════════════════════════════════════════════
def fig1():
    W, H = 880, 530
    mL, mR, mT, mB = 78, 78, 122, 196
    sx = min((W - mL - mR) / TOTAL, (H - mT - mB) / HH)
    cv = Canvas(W, H, sx=sx, ox=mL, oy=mB, bg="#FFFFFF")

    cv.text_px(W / 2, 34, f"圖 1　{TAG} 題目重繪：七段尺寸鏈定出 a 與 L", 17.0,
               C["text"], weight="700")
    cv.text_px(W / 2, 58,
               f"梁 {BW:g} × {HH:g} cm，全長 {TOTAL:g} cm　"
               f"f'c = {FC:g} kgf/cm²　fy = {FY:g} kgf/cm²　"
               f"{N_BAR}-D19（As = {AS:g} cm²）", 12.5, C["muted"])

    # 梁本體
    cv.polygon([(0, 0), (TOTAL, 0), (TOTAL, HH), (0, HH)], "#EDF1F6",
               C["member"], 2.6)

    # 純彎區網底
    cv.polygon([(PURE_BEND[0], 0), (PURE_BEND[1], 0),
                (PURE_BEND[1], HH), (PURE_BEND[0], HH)], C["fill_m"], "none")
    cv.text_px(cv.X(sum(PURE_BEND) / 2), cv.Y(HH * 0.62), "純彎區", 12.5,
               C["bmd"], weight="700")
    cv.text_px(cv.X(sum(PURE_BEND) / 2), cv.Y(HH * 0.62) + 17,
               "（原圖標註處）", 11.5, C["bmd"])

    # 承壓鈑（底部）與載重鈑（頂部）
    PLT = 3.2
    for x in (X_SUP_L, X_SUP_R):
        cv.polygon([(x - LB / 2, -PLT), (x + LB / 2, -PLT),
                    (x + LB / 2, 0), (x - LB / 2, 0)], C["member"], C["member"])
        cv.support((x, -PLT), "pin", size=13)
    for x in (X_LOAD_L, X_LOAD_R):
        cv.polygon([(x - LB / 2, HH), (x + LB / 2, HH),
                    (x + LB / 2, HH + PLT), (x - LB / 2, HH + PLT)],
                   C["member"], C["member"])
        cv.arrow((x, HH + 13), (x, HH + PLT), C["load"], 3.4, 11)
        cv.math_px(cv.X(x), cv.Y(HH + 13) - 14, M_("P/2"), 15, C["load"],
                   weight="700")

    # 6-D19：立面上三層縱向筋（每層 2 支）＋ 形心線
    for r in range(3):
        cv.line((2.0, 3.5 + r * 6.5), (TOTAL - 2.0, 3.5 + r * 6.5),
                C["tension"], 2.4)
    cv.line((0, HT), (TOTAL, HT), C["tension"], 1.6, dash="6 4")
    cv.dot((X_LOAD_L - 16, E_T), 5.0, fill=C["tension"], stroke="#FFFFFF", w=1.4)
    cv.text_px(cv.X(TOTAL * 0.30), cv.Y(HT) - 32,
               f"{N_BAR}-D19（3 層 × 2 支）", 11.5, C["tension"], weight="700")
    cv.text_px(cv.X(TOTAL * 0.30), cv.Y(HT) - 14,
               f"形心距底 et = {E_T:g} cm → 節點高 ht = {HT:g} cm", 11.5,
               C["tension"])

    # 七段尺寸鏈
    for i in range(len(CHAIN)):
        cv.dim((EDGE[i], 0), (EDGE[i + 1], 0), M_(f"{CHAIN[i]:g}"), off=42,
               label_off=14)
    cv.dim((X_SUP_L, 0), (X_LOAD_L, 0), M_(f"a = {A_SHEAR:g}"), off=92,
           label_off=15, color=C["accent"])
    cv.dim((X_SUP_L, 0), (X_SUP_R, 0), M_(f"L = {SPAN:g}"), off=136,
           label_off=15, color=C["accent"])
    cv.dim((TOTAL, 0), (TOTAL, HH), M_(f"h = {HH:g}"), off=44, label_off=14)

    # 四塊鈑的中心線（a 與 L 都自鈑中心量起）
    for x in (X_SUP_L, X_LOAD_L, X_LOAD_R, X_SUP_R):
        cv.line((x, -PLT), (x, HH + PLT), C["accent"], 1.1, dash="3 4")

    cv.text_px(W / 2, H - 26,
               f"四段 {LB:g} cm 是鈑寬、三段 {CHAIN[1]:g} cm 是淨距；"
               f"「純彎區」必在兩載重鈑之間 → 30 不可能是鈑寬。"
               f"a/d = {A_SHEAR:g}/{D_EFF:g} = {A_SHEAR / D_EFF:.3f} ＜ 2 → 適用 STM",
               12.5, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 2　STM 桁架力流（桿力以 P 的倍數表示）
# ══════════════════════════════════════════════════════════
def fig2():
    nodes = {"A": (X_SUP_L, E_T), "B": (X_SUP_R, E_T),
             "C": (X_LOAD_L, HH - E_C), "D": (X_LOAD_R, HH - E_C)}
    members = [("A", "C", -A_["kD"]), ("C", "D", -A_["kT"]),
               ("D", "B", -A_["kD"]), ("A", "B", +A_["kT"])]
    cv = truss_forces(
        nodes, members,
        supports=[("A", "pin"), ("B", "roller")],
        loads=[("C", (0, -34), M_("P/2")), ("D", (0, -34), M_("P/2"))],
        title="圖 2　STM 桁架：桿力全部是 P 的倍數（正＝受拉、負＝受壓）",
        note=None, W=880, H=470, margin=124, fmt="{:+.4g}")

    # 幾何標註（truss_forces 回傳 Canvas，可續繪）
    cv.text_px(cv.w / 2, 58,
               f"力臂 z = h − hc/2 − ht/2 = {Z:g} cm　"
               f"tanθ = z/a = {Z:g}/{A_SHEAR:g} → θ = {A_['theta']:.1f}°"
               f"（＞ 25° 符合 ACI 下限）", 12.5, C["muted"])
    cv.moment_arrow((X_SUP_L, E_T), r=52, ccw=True, color=C["accent"],
                    w=1.8, span=A_["theta"], start=0)
    cv.text_px(cv.X(X_SUP_L) + 62, cv.Y(E_T) - 26,
               f"θ = {A_['theta']:.0f}°", 13.5, C["accent"], "start",
               weight="700")
    cv.dim(((X_LOAD_L + X_LOAD_R) / 2, E_T),
           ((X_LOAD_L + X_LOAD_R) / 2, HH - E_C), M_(f"z = {Z:g}"),
           off=0, label_off=-15, color=C["dim"])
    cv.dim((X_SUP_L, E_T - 14), (X_LOAD_L, E_T - 14), M_(f"a = {A_SHEAR:g}"),
           off=34, label_off=14, color=C["dim"])
    cv.text_px(cv.w / 2, cv.h - 24,
               f"驗核：√(T² + R²) = P√({A_['kT']:.2f}² + 0.5²) = "
               f"{A_['kD']:.4f}P ＝ 斜壓桿力 ✓　"
               f"讀法 B（誤把 30 讀成淨跨）會得 θ = {B_['theta']:.1f}°、"
               f"T = {B_['kT']:.3f}P，桿力全錯", 12.5, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 3　CCT 節點幾何：三個面與 w_s 的來源
# ══════════════════════════════════════════════════════════
def fig3():
    W, H = 900, 530
    mL, mR, mT, mB = 232, 348, 132, 172
    sx = min((W - mL - mR) / (LB * 1.30), (H - mT - mB) / (HT * 1.30))
    cv = Canvas(W, H, sx=sx, ox=mL, oy=mB, bg="#FFFFFF")

    cv.text_px(W / 2, 34, "圖 3　CCT 節點：三個面各自驗核，ws 由幾何投影決定",
               17.0, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               f"θ = {A_['theta']:.0f}° 時 ws = lb·sinθ + ht·cosθ = "
               f"{LB:g}×{A_['sin']:.4f} + {HT:g}×{A_['cos']:.4f} = "
               f"{A_['ws']:.2f} cm = √2·lb", 12.5, C["muted"])

    # 節點三角形：承壓面 (0,0)-(lb,0)、背面 (0,0)-(0,ht)、斜邊即斜壓桿面
    cv.polygon([(0, 0), (LB, 0), (0, HT)], C["fill_c"], "none")
    cv.line((0, 0), (LB, 0), C["load"], 4.0, cap="butt")        # 承壓面
    cv.line((0, 0), (0, HT), C["tension"], 4.0, cap="butt")     # 背面
    cv.line((LB, 0), (0, HT), C["compr"], 4.0, cap="butt")      # 斜壓桿面

    # 承壓鈑與反力
    cv.polygon([(0, -2.4), (LB, -2.4), (LB, 0), (0, 0)], C["member"], C["member"])
    xr = LB * 0.5
    cv.arrow((xr, -8.4), (xr, -2.4), C["load"], 3.4, 10)
    cv.math_px(cv.X(LB) + 24, cv.Y(-5.4), M_("R = P/2"), 14, C["load"],
               "start", weight="700")

    # 背面：拉力桿
    yt = HT * 0.72
    cv.arrow((1.2, yt), (-8.6, yt), C["tension"], 3.4, 11)
    cv.math_px(cv.X(-8.6) - 10, cv.Y(yt), M_(f"T = {A_['kT']:.1f}P"), 14,
               C["tension"], "end", weight="700")

    # 斜壓桿力：自斜邊往節點內部推
    mid = (LB / 2, HT / 2)
    ox_, oy_ = A_["sin"], A_["cos"]                 # 斜邊外法向（指向右上）
    cv.arrow((mid[0] + ox_ * 3.0, mid[1] + oy_ * 3.0),
             (mid[0] - ox_ * 8.0, mid[1] - oy_ * 8.0), C["compr"], 3.6, 12)
    cv.math_px(cv.X(LB * 0.54), cv.Y(HT * 0.16),
               M_(f"F = {A_['kD']:.4f}P"), 14, C["compr"], "middle", weight="700")

    # 尺寸
    cv.dim((0, -2.4), (LB, -2.4), M_(f"lb = {LB:g}"), off=46, label_off=15)
    cv.dim((0, HT), (0, 0), M_(f"ht = {HT:g}"), off=44, label_off=15)
    cv.dim((LB, 0), (0, HT), M_(f"ws = {A_['ws']:.2f}"), off=32, label_off=22,
           color=C["compr"])

    # 三面對照表（右側）
    gx = W - mR + 24
    rows = [
        ("承壓面（反力）", LB * BW, "P/2", 0.5, C["load"]),
        ("背面（拉桿面）", HT * BW, f"T = {A_['kT']:.1f}P", A_["kT"], C["tension"]),
        ("斜壓桿面", A_["ws"] * BW, f"F = {A_['kD']:.4f}P", A_["kD"], C["compr"]),
    ]
    cv.text_px(gx, 126, f"CCT 三面（βn = {BETA_N_CCT:g} → fce = {FCE_CCT:.1f}）",
               13, C["text"], "start", weight="700")
    for i, (nm, area, force, kk, col) in enumerate(rows):
        y = 156 + i * 56
        cv.text_px(gx, y, nm, 12.5, col, "start", weight="700")
        cv.text_px(gx, y + 18, f"面積 {area:,.1f} cm²　作用力 {force}", 12,
                   C["muted"], "start")
        cv.text_px(gx, y + 36, f"→ P ≤ {FCE_CCT * area / kk * TF:,.1f} tf", 12.5,
                   C["accent"], "start", weight="700")

    y0 = 156 + 3 * 56 + 14
    cv.text_px(gx, y0, "桿身 vs 節點面，取小者控制", 13, C["text"], "start",
               weight="700")
    cv.text_px(gx, y0 + 21,
               f"桿身 fce = 0.85×{BETA_S_BOTTLE:g}×{FC:g} = {FCE_BOTTLE:.3f}",
               12, C["compr"], "start")
    cv.text_px(gx, y0 + 39,
               f"節點面 fce = 0.85×{BETA_N_CCT:g}×{FC:g} = {FCE_CCT:.1f}", 12,
               C["accent"], "start")
    cv.text_px(gx, y0 + 60,
               f"{FCE_BOTTLE:.3f} ＜ {FCE_CCT:.1f} → 桿身控制", 12.5,
               C["compr"], "start", weight="700")
    cv.text_px(gx, y0 + 82,
               f"節點內拉力桿所需寬 wt = {W_T:.2f} ≤ ht = {HT:g} ✓", 12,
               C["tension"], "start")

    cv.text_px(W / 2, H - 24,
               f"θ = {A_['theta']:.0f}° 時 R = T = P/2 且 ws = √2·lb，"
               f"三個面的應力比例完全一致 → 三面同時給出 "
               f"P ≤ {A_['lim']['cct'] * TF:,.1f} tf（算對了的自我驗證）",
               12.5, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 4　五個限制條件的 P 上限
# ══════════════════════════════════════════════════════════
def fig4():
    desc = {
        "strut_diag": f"βs = {BETA_S_BOTTLE:g}，脆性 ← 控制",
        "cct": f"βn = {BETA_N_CCT:g}，脆性",
        "tie": "fy 降伏，延性",
        "ccc": f"βn = {BETA_N_CCC:g}，脆性",
        "strut_horiz": f"βs = {BETA_S_PRISM:g}，脆性",
    }
    col = {"strut_diag": C["compr"], "cct": C["accent"], "tie": C["tension"],
           "ccc": C["ghost"], "strut_horiz": C["muted"]}
    order = sorted(FACE_ORDER, key=lambda k: -A_["lim"][k])
    cases = [(FACE_NAME[k], desc[k], A_["lim"][k] * TF,
              M_(f"{A_['lim'][k] * TF:,.1f} tf"), col[k]) for k in order]
    return bar_compare(
        cases,
        title="圖 4　五個限制條件同時攤開：最小者決定 Pmax，也決定破壞模式",
        sub="長條以最大值為 100%；每一項都要算、節點還要分面算，漏一項就可能高估承載力",
        note=f"Pmax = {PMAX * TF:,.1f} tf 由斜向瓶形壓桿控制（脆性）；"
             f"CCT 節點僅高 {A_['lim']['cct'] / PMAX - 1:.1%}、"
             f"拉力桿降伏高 {A_['lim']['tie'] / PMAX - 1:.1%} → "
             f"延性模式被擋住，本梁為壓力控制之脆性破壞").svg()


# ══════════════════════════════════════════════════════════
FIGURES = [
    ("1-beam", fig1,
     "把七段尺寸鏈讀成「支承至載重 30、純彎區 20」（a、L、θ 全錯）"),
    ("2-stm", fig2,
     "STM 幾何建錯（力臂 z 沒扣兩個節點高）；桿力正負與拉壓判斷反了"),
    ("3-node", fig3,
     "節點只驗承壓面；把 w_s 當成 lb；忘了桿身 βs 與節點面 βn 要取小"),
    ("4-capacity", fig4,
     "沒把五項全算完就下結論；破壞模式誤判成延性的拉力桿降伏"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    checks = [
        ("全長 cm",        TOTAL,                    170,     0.01),
        ("支承跨度 L cm",   SPAN,                     150,     0.01),
        ("剪力跨 a cm",     A_SHEAR,                  50,      0.01),
        ("力臂 z cm",       Z,                        50,      0.01),
        ("θ 度",           A_["theta"],              45.0,    0.01),
        ("A_s cm2",       AS,                       17.22,   0.001),
        ("T/P",           A_["kT"],                 0.5,     1e-6),
        ("F_diag/P",      A_["kD"],                 0.7071,  1e-4),
        ("d cm",          D_EFF,                    60,      0.01),
        ("a/d",           A_SHEAR / D_EFF,          0.833,   0.001),
        ("w_s cm",        A_["ws"],                 28.28,   0.01),
        ("拉力桿 P tf",     A_["lim"]["tie"] * TF,    144.6,   0.05),
        ("水平壓桿 P tf",    A_["lim"]["strut_horiz"] * TF, 170.0, 0.05),
        ("斜壓桿 P tf",     A_["lim"]["strut_diag"] * TF,  127.5, 0.05),
        ("CCT P tf",      A_["lim"]["cct"] * TF,    136.0,   0.05),
        ("CCC P tf",      A_["lim"]["ccc"] * TF,    170.0,   0.05),
        ("P_max tf",      PMAX * TF,                127.5,   0.05),
        ("w_t cm",        W_T,                      18.75,   0.01),
        ("φP_max tf",     PHI_PMAX * TF,            95.6,    0.05),
        ("讀法B θ 度",     B_["theta"],              59.0,    0.05),
        ("讀法B T/P",      B_["kT"],                 0.300,   0.001),
        ("讀法B F/P",      B_["kD"],                 0.5831,  1e-4),
        ("讀法B 拉桿 tf",   B_["lim"]["tie"] * TF,    241.1,   0.1),
        ("讀法B 斜壓 tf",   B_["lim"]["strut_diag"] * TF, 149.9, 0.25),
        ("讀法B CCT tf",   B_["lim"]["cct"] * TF,    136.0,   0.05),
    ]
    print(f"── 與 {TAG}.md §4／§5 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<16} 算得 {got:>13.6g}   .md {want:>9}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"
    assert A_["control"] == "strut_diag", "控制項應為斜向瓶形壓桿"
    assert B_["control"] == "cct", "讀法 B 的控制項應為 CCT 節點"
    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<34} 攔：{catches}")


if __name__ == "__main__":
    main()
