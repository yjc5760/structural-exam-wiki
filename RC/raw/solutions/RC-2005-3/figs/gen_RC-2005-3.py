#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2005-3 角柱梁柱接頭剪力強度檢核 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2005-3.md §1 給定的原始資料（外加 §5②／§6 的規範 γ 表與 §5⑥ 的
     彎鉤公式係數）；A_s、T、a、M_pr、V_col、V_jh、b_j、A_j、φV_n、利用率、屋頂層折減、
     以及「用 f_y」與「舊版 2M/H」的對照值全部現算，檔尾對 §4／§6 公佈值 assert。
  2. 改 §1 任一數字重跑，三張圖跟著變（力偶臂、反曲點、長條比例、γ 對應的 φV_n）。
  3. FIGURES 表寫明每張圖攔什麼錯。

用法：
    STRUCTDRAW_DIR=<skill>/scripts python3 gen_RC-2005-3.py figs
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose
from recipes import bar_compare

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2005-3"

# ══════════════════════════════════════════════════════════
# §1 原始給定（角柱梁柱接頭）
# ══════════════════════════════════════════════════════════
H = 365.0                  # cm 樓層高（柱上下接頭中心距）
BC = HC = 60.0             # cm 柱斷面 60×60（h_c 為分析方向柱深）
BW = 60.0                  # cm 梁寬（＝柱寬）
D = 70.0                   # cm 梁有效深度
N_BAR, A_BAR = 6, 5.07     # 6-#8，#8 ＝ D25，A_b = 5.07 cm^2
DB = 2.54                  # cm D25 標稱直徑（§5⑥ 錨定長度用）
FC, FY = 280.0, 4200.0     # kgf/cm^2
ALPHA_O = 1.25             # 耐震超強係數（土木 401-112 §15.6.2／ACI 318-19 §18.8.2.1）
PHI = 0.85                 # 接頭剪力強度折減（§21.2.1(e)）
K_HOOK = 17.2              # §5⑥ 90° 彎鉤 l_dh = f_y·d_b/(17.2√f'c)（kgf 制）

# §5② 土木 401 之 γ（kgf/cm^2 制）與 SI 制 √f'c 係數；§6 另列屋頂層（柱未延伸）一組
GAMMA = {"four": 5.3, "three": 3.9, "other": 3.2, "roof_other": 2.2}
GAMMA_SI = {"four": 1.7, "three": 1.2, "other": 1.0, "roof_other": 0.7}

TF = 1e-3                  # kgf → tf
TFM = 1e-5                 # kgf·cm → tf·m
SQFC = math.sqrt(FC)

# ── 現算 ──────────────────────────────────────────────────
AS = N_BAR * A_BAR                       # 梁拉力筋面積
T_FORCE = ALPHA_O * AS * FY              # ① 梁受拉鋼筋拉力（耐震 1.25f_y）
A_BLK = T_FORCE / (0.85 * FC * BW)       # ② Whitney 應力塊深度
MPR = T_FORCE * (D - A_BLK / 2)          # ② 梁可能彎矩強度
M_COL = MPR / 2                          # ③ 上下柱等勁度 → 各分擔一半
V_COL = M_COL / (H / 2)                  # ③ ＝ M_pr/H（反曲點在樓層中高）
V_JH = T_FORCE - V_COL                   # ④ 接頭水平剪力需求

BJ = min(min(BW + HC, BW + 0.0), BC)     # ⑤ b_j = min(b+h, b+2x) ≤ b_col，本題 x = 0
AJ = BJ * HC
PHI_UNIT = PHI * SQFC * AJ               # ⑥ φV_n 中除 γ 以外的部分（每單位 γ 的 tf 數）


def phi_vn(g):
    """φV_n = φ·γ·√f'c·A_j"""
    return PHI * g * SQFC * AJ


PHI_VN = phi_vn(GAMMA["other"])          # 中間樓層角柱接頭（本題主線）
PHI_VN_ROOF = phi_vn(GAMMA["roof_other"])   # §6 屋頂層角柱接頭（318-19 新增）
UTIL = V_JH / PHI_VN
UTIL_ROOF = V_JH / PHI_VN_ROOF
UTIL_T = T_FORCE / PHI_VN                # 保守下限（忽略 V_col）

# 對照組 A：不計超強，T = A_s f_y（§4 兩種讀法對照表）
T_FY = AS * FY
A_FY = T_FY / (0.85 * FC * BW)
MN_FY = T_FY * (D - A_FY / 2)
V_COL_FY = MN_FY / H
V_JH_FY = T_FY - V_COL_FY
UTIL_FY = V_JH_FY / PHI_VN

# 對照組 B：舊版錯誤（分子多一倍，且未計超強）
V_COL_WRONG = 2 * MN_FY / H

# §5⑥ 梁頂筋 90° 彎鉤錨定長度與柱深可用長度
L_DH = FY * DB / (K_HOOK * SQFC)
L_AVAIL = 55.0             # §5⑥「柱深 60 cm 扣保護層後可用約 55 cm」

# ── 純繪圖用參數（不進入任何計算；改動只影響外觀）────────────
HB_DRAW = 80.0             # 梁全高（原卷未給，僅供繪圖示意）
CB_DRAW = 6.0              # 梁頂筋至梁頂距離（示意）
LB_DRAW = 150.0            # 梁繪圖長度
LG_DRAW = 110.0            # 「此側無梁」ghost 梁長度
EXT_DRAW = 68.0            # fig-2 俯視圖中梁伸出柱面的長度

HALF = H / 2               # 反曲點至接頭中心的力臂
XCL, XCR = -HC / 2, HC / 2
XBR = XCR + LB_DRAW
Y_BAR = HB_DRAW / 2 - CB_DRAW


def M(s):
    """math()/math_px() 用的襯線字型缺中日韓字，cairosvg 會靜默丟字 → 進來就攔。"""
    assert not any(ord(ch) > 0x2E80 for ch in s), f"math 字串不得含中日韓字元：{s}"
    return s


def win(cv, xl, xr, yb, yt, L=28, R=28, T=84, B=118):
    """先定留白再反推 sx／ox／oy，避免寫死縮放塞不下。"""
    aw, ah = cv.w - L - R, cv.h - T - B
    sx = min(aw / (xr - xl), ah / (yt - yb))
    cv.sx = sx
    cv.ox = L + (aw - (xr - xl) * sx) / 2 - xl * sx
    cv.oy = B + (ah - (yt - yb) * sx) / 2 - yb * sx
    return sx


def cross(cv, p, s=9, col=C["load"], w=2.6):
    """在模型點 p 畫一個交叉標記（s 為像素半長）"""
    x, y = cv.P(p)
    for sgn in (1, -1):
        cv.parts.append(f'<line x1="{x-s:.2f}" y1="{y-s*sgn:.2f}" x2="{x+s:.2f}" '
                        f'y2="{y+s*sgn:.2f}" stroke="{col}" stroke-width="{w}" '
                        f'stroke-linecap="round"/>')


# ══════════════════════════════════════════════════════════
# 圖 1　柱彎矩分擔（左）與「接頭＋上半柱」自由體（右）
#        兩格共用同一模型視窗與同一 sx，幾何可直接對照
# ══════════════════════════════════════════════════════════
PW1, PH1 = 580, 560
XL1, XR1 = -235.0, 310.0
YB1, YT1 = -(HALF + 30), HALF + 30


def _geom(cv, ghost=False):
    """柱線＋接頭＋單側梁。ghost=True 畫成灰虛線（被移除的部分）。"""
    if ghost:
        col, w, dash = C["ghost"], 1.6, "7 5"
        for pts in ([(XCL, -HALF), (XCR, -HALF), (XCR, HALF), (XCL, HALF), (XCL, -HALF)],
                    [(XCR, -HB_DRAW / 2), (XBR, -HB_DRAW / 2), (XBR, HB_DRAW / 2),
                     (XCR, HB_DRAW / 2)]):
            cv.poly(pts, col, w, dash=dash)
        return
    # 柱（上下延伸以虛線示意續接）
    for x in (XCL, XCR):
        cv.line((x, HALF), (x, HALF + 22), C["ghost"], 1.6, dash="6 5")
        cv.line((x, -HALF), (x, -HALF - 22), C["ghost"], 1.6, dash="6 5")
    cv.polygon([(XCL, -HALF), (XCR, -HALF), (XCR, HALF), (XCL, HALF)],
               C["border"], C["member"], 2.2)
    # 梁（單側）
    cv.polygon([(XCR, -HB_DRAW / 2), (XBR, -HB_DRAW / 2), (XBR, HB_DRAW / 2),
                (XCR, HB_DRAW / 2)], C["border"], C["member"], 2.2)
    # 接頭（剪力區 → 紫）
    cv.polygon([(XCL, -HB_DRAW / 2), (XCR, -HB_DRAW / 2), (XCR, HB_DRAW / 2),
                (XCL, HB_DRAW / 2)], C["fill_s"], C["member"], 2.0)


def fig1_left():
    cv = Canvas(PW1, PH1)
    win(cv, XL1, XR1, YB1, YT1)
    cv.panel("接頭彎矩分擔與柱剪力",
             f"上下柱等勁度各分擔 M_{{pr}}/2　柱 {BC:g}×{HC:g} cm")
    _geom(cv)

    # 此側無梁（角柱在分析平面內只有一根梁）
    cv.poly([(XCL, -HB_DRAW / 2), (XCL - LG_DRAW, -HB_DRAW / 2),
             (XCL - LG_DRAW, HB_DRAW / 2), (XCL, HB_DRAW / 2)],
            C["ghost"], 1.8, dash="7 5")
    cross(cv, (XCL - LG_DRAW / 2, 0), 13, C["load"], 2.8)
    cv.text_px(cv.X(XCL - LG_DRAW / 2), cv.Y(HB_DRAW / 2) - 15,
               "此側無梁", 12.5, C["load"], weight="700")
    cv.text_px(cv.X(XCL - LG_DRAW / 2), cv.Y(-HB_DRAW / 2) + 16,
               "（角柱）", 12, C["muted"])

    # 梁端傳入的 M_pr（梁頂受拉 → 對接頭為順時針）
    cv.moment_arrow((XCR + 30, 0), r=22, ccw=False, color=C["load"], w=2.8,
                    span=250, start=110)
    cv.math_px(cv.X(XCR + LB_DRAW / 2), cv.Y(105),
               M(f"M_{{pr}} = {MPR*TFM:.2f} tf·m"), 14.5, C["load"], weight="700")
    cv.text_px(cv.X(XCR + LB_DRAW / 2), cv.Y(105) + 18, "梁端傳入接頭",
               12, C["load"])
    cv.line((XCL + 6, Y_BAR), (XBR, Y_BAR), C["tension"], 2.6)
    cv.text_px(cv.X(XCR + LB_DRAW / 2), cv.Y(HB_DRAW / 2) - 14,
               f"{N_BAR}-#8　A_{{s}} = {AS:.2f} cm^{{2}}", 12, C["tension"])

    # 上下柱各分擔 M_pr/2（對接頭為逆時針，與梁的順時針平衡）
    for ys in (1, -1):
        cv.moment_arrow((0, ys * (HB_DRAW / 2 + 50)), r=25, ccw=True,
                        color=C["deform"], w=2.6, span=250, start=110)
        cv.math_px(cv.X(XCL) - 12, cv.Y(ys * (HB_DRAW / 2 + 50)),
                   M(f"M_{{pr}}/2 = {M_COL*TFM:.2f} tf·m"), 13, C["deform"],
                   "end", weight="700")
    cv.text_px(cv.X(0), cv.Y(0), "接頭", 12, C["text"], weight="700")

    # 反曲點與柱剪力（兩個 V_col 反向 → 構成力偶 V_col·H）
    for ys, xa, xb, anc, ldx in ((1, -6, -118, "start", 40), (-1, 6, 118, "end", -40)):
        y = ys * HALF
        cv.arrow((xa, y), (xb, y), C["deform"], 3.4, 12)
        cv.math_px(cv.X((xa + xb) / 2), cv.Y(y) - 17,
                   M(f"V_{{col}} = {V_COL*TF:.2f} tf"), 13.5, C["deform"],
                   weight="700")
        cv.dot((0, y), 5.6, fill="#FFFFFF", stroke=C["accent"], w=2.9)
        cv.text_px(cv.X(0) + ldx, cv.Y(y) + 1, "反曲點（M = 0）", 12,
                   C["accent"], anc, weight="700")

    # 巢狀尺寸：內 H/2（力臂）、外 H（力偶臂）
    cv.double_arrow((215, 0), (215, HALF), C["accent"], 2.0, 9)
    cv.math_px(cv.X(215) - 8, cv.Y(140), M(f"H/2 = {HALF:.1f} cm"), 13,
               C["accent"], "end", weight="700")
    cv.double_arrow((240, -HALF), (240, HALF), C["accent"], 2.2, 9)
    px, py = cv.X(240), cv.Y(-100)
    cv.rect_px(px - 54, py - 30, 108, 60, "#FFFFFF", 8)
    cv.text_px(px, py - 15, "力偶臂", 12.5, C["accent"], weight="700")
    cv.math_px(px, py + 8, M(f"H = {H:g} cm"), 13.5, C["accent"], weight="700")

    cv.text_px(PW1 / 2, PH1 - 96,
               f"柱剪力由力偶算出：V_{{col}} = (M_{{pr}}/2)/(H/2) = M_{{pr}}/H "
               f"= {V_COL*TF:.2f} tf", 13.5, C["text"], weight="700")
    cv.text_px(PW1 / 2, PH1 - 72,
               f"檢查：V_{{col}} × H = {V_COL*TF:.2f} × {H/100:.2f} "
               f"= {V_COL*H*TFM:.1f} tf·m ＝ 一個接頭的梁彎矩 ✓", 12.5, C["muted"])
    cv.text_px(PW1 / 2, PH1 - 48,
               f"× 舊版寫 V_{{col}} = 2M/H = {V_COL_WRONG*TF:.1f} tf：分子多算一倍",
               12.5, C["load"], weight="700")
    cv.text_px(PW1 / 2, PH1 - 26,
               "（該版另以 f_y 計算，未含 1.25 超強係數）", 11.5, C["muted"])
    return cv


def fig1_right():
    """幾何與左格同一 sx；模型視窗整體左移 SHIFT，好讓向左的力有標註空間。"""
    SHIFT = 65.0
    XBOX = 60.0                                   # 隔離框半寬
    cv = Canvas(PW1, PH1)
    win(cv, XL1 - SHIFT, XR1 - SHIFT, YB1, YT1)
    cv.panel("接頭＋上半柱自由體", "切斷面：接頭中高（下）與上柱反曲點（上）")
    _geom(cv, ghost=True)

    # 隔離體本體：接頭上半 + 上柱至反曲點
    cv.polygon([(XCL, 0), (XCR, 0), (XCR, HALF), (XCL, HALF)],
               C["border"], C["member"], 2.2)
    cv.polygon([(XCL, 0), (XCR, 0), (XCR, HB_DRAW / 2), (XCL, HB_DRAW / 2)],
               C["fill_s"], C["member"], 2.0)
    # 虛線隔離框
    cv.poly([(-XBOX, 0), (XBOX, 0), (XBOX, HALF + 10), (-XBOX, HALF + 10),
             (-XBOX, 0)], C["accent"], 2.0, dash="8 6")

    # 兩個切斷面
    cv.line((XCL - 4, 0), (XCR + 4, 0), C["accent"], 3.6)
    cv.text_px(cv.X(0), cv.Y(0) + 19, "切斷面（接頭中高）", 12, C["accent"],
               weight="700")
    cv.line((XCL - 4, HALF), (XCR + 4, HALF), C["accent"], 3.6)
    cv.dot((0, HALF), 5.6, fill="#FFFFFF", stroke=C["accent"], w=2.9)
    cv.text_px(cv.X(XBOX) + 10, cv.Y(HALF) + 1, "切斷面＝反曲點（M = 0）", 12,
               C["accent"], "start", weight="700")

    # 梁頂筋：90° 彎鉤錨入接頭，拉力 T 向右傳出隔離體
    cv.line((XCL + 8, Y_BAR), (XBR - 10, Y_BAR), C["tension"], 2.6)
    cv.line((XCL + 8, Y_BAR), (XCL + 8, 4), C["tension"], 2.6)
    cv.arrow((XBOX, Y_BAR), (XBOX + 118, Y_BAR), C["tension"], 3.6, 13)
    cv.math_px(cv.X(XBOX) + 8, cv.Y(Y_BAR) - 20,
               M(f"T = 1.25A_{{s}}f_{{y}} = {T_FORCE*TF:.2f} tf"), 13.5,
               C["tension"], "start", weight="700")
    cv.text_px(cv.X(XBOX) + 8, cv.Y(Y_BAR) + 18, "梁頂筋拉力（向右）", 11.5,
               C["tension"], "start")

    # 上柱剪力 V_col（向左）
    cv.arrow((-8, HALF), (-128, HALF), C["deform"], 3.4, 12)
    cv.math_px(cv.X(-XBOX) - 26, cv.Y(HALF) - 20,
               M(f"V_{{col}} = {V_COL*TF:.2f} tf"), 13.5, C["deform"], "end",
               weight="700")
    # 接頭水平剪力 V_jh（向左，切斷面上的內力）
    cv.arrow((-8, 14), (-152, 14), C["sfd"], 3.8, 13)
    cv.math_px(cv.X(-XBOX) - 26, cv.Y(14) - 20,
               M(f"V_{{jh}} = {V_JH*TF:.2f} tf"), 14.5, C["sfd"], "end",
               weight="700")
    cv.text_px(cv.X(-XBOX) - 10, cv.Y(14) + 18, "接頭水平剪力（待求）", 11.5,
               C["sfd"], "end")

    cv.text_px(PW1 / 2, PH1 - 96,
               "水平力平衡（向右為正）：T − V_{col} − V_{jh} = 0", 13.5,
               C["text"], weight="700")
    cv.text_px(PW1 / 2, PH1 - 71,
               f"V_{{jh}} = T − V_{{col}} = {T_FORCE*TF:.2f} − {V_COL*TF:.2f} "
               f"= {V_JH*TF:.2f} tf", 14.5, C["sfd"], weight="700")
    cv.text_px(PW1 / 2, PH1 - 47,
               "× 不是 T + V_{col}：V_{col} 與 T 反向，是減項", 12.5, C["load"],
               weight="700")
    cv.text_px(PW1 / 2, PH1 - 25,
               f"梁底壓力 C 在切斷面下方，不進入本隔離體｜彎鉤錨定 "
               f"l_{{dh}} = {L_DH:.1f} cm ≤ 可用 {L_AVAIL:g} cm ✓", 11.5, C["muted"])
    return cv


def fig1():
    return compose(
        [fig1_left(), fig1_right()], cols=2,
        title=f"圖 1　{TAG} 角柱梁柱接頭：柱彎矩分擔與接頭水平剪力自由體",
        sub=f"H = {H:g} cm｜柱 {BC:g}×{HC:g} cm｜梁 d = {D:g} cm、{N_BAR}-#8｜"
            f"f'c = {FC:g}、fy = {FY:g} kgf/cm²",
        note="紅＝梁鋼筋拉力與梁彎矩　藍＝柱剪力與柱彎矩　紫＝接頭水平剪力 Vjh　"
             "橙＝切斷面與反曲點　灰虛線＝被移除（或不存在）的部分")


# ══════════════════════════════════════════════════════════
# 圖 2　接頭圍束分類與 γ（四格俯視平面）
# ══════════════════════════════════════════════════════════
PW2, PH2 = 440, 460
XY2 = HC / 2 + EXT_DRAW + 8          # 平面視窗半寬

CASES = [
    dict(no="①", title="四面受梁圍束（內接頭）", sub="四個方向都有梁",
         faces="NSEW", key="four", tag=""),
    dict(no="②", title="三面或一雙對面受圍束", sub="三個方向有梁",
         faces="NEW", key="three", tag=""),
    dict(no="③", title="其他（含角柱，本題）", sub="兩個正交方向各一根梁",
         faces="NE", key="other", tag="★ 本題採用"),
    dict(no="④", title="屋頂層之「其他」", sub="柱未延伸至接頭上方",
         faces="NE", key="roof_other", tag="ACI 318-19 新增"),
]

FACE_SEG = {"E": ((XCR, -BW / 2), (XCR, BW / 2)),
            "W": ((XCL, -BW / 2), (XCL, BW / 2)),
            "N": ((-BW / 2, HC / 2), (BW / 2, HC / 2)),
            "S": ((-BW / 2, -HC / 2), (BW / 2, -HC / 2))}
BEAM_RECT = {
    "E": [(XCR, -BW / 2), (XCR + EXT_DRAW, -BW / 2), (XCR + EXT_DRAW, BW / 2),
          (XCR, BW / 2)],
    "W": [(XCL, -BW / 2), (XCL - EXT_DRAW, -BW / 2), (XCL - EXT_DRAW, BW / 2),
          (XCL, BW / 2)],
    "N": [(-BW / 2, HC / 2), (-BW / 2, HC / 2 + EXT_DRAW), (BW / 2, HC / 2 + EXT_DRAW),
          (BW / 2, HC / 2)],
    "S": [(-BW / 2, -HC / 2), (-BW / 2, -HC / 2 - EXT_DRAW),
          (BW / 2, -HC / 2 - EXT_DRAW), (BW / 2, -HC / 2)]}
BEAM_LABEL = {"E": (XCR + EXT_DRAW / 2, 0), "W": (XCL - EXT_DRAW / 2, 0),
              "N": (0, HC / 2 + EXT_DRAW / 2), "S": (0, -HC / 2 - EXT_DRAW / 2)}


def _roof_icon(cv):
    """屋頂層示意：柱到接頭為止，上方無柱（畫於平面圖西南象限空白處）。"""
    x0, x1 = -100.0, -66.0
    cv.polygon([(x0, -104), (x1, -104), (x1, -78), (x0, -78)], C["border"],
               C["member"], 1.8)                          # 下柱
    cv.polygon([(x0, -78), (x1, -78), (x1, -64), (x0, -64)], C["fill_s"],
               C["member"], 1.8)                          # 接頭
    cv.poly([(x0, -64), (x0, -42), (x1, -42), (x1, -64)], C["ghost"], 1.6,
            dash="5 4")                                   # 本應有的上柱
    cross(cv, ((x0 + x1) / 2, -53), 8, C["load"], 2.4)
    cv.text_px(cv.X((x0 + x1) / 2), cv.Y(-32), "上方無柱（側視）", 11, C["load"],
               weight="700")


def fig2_panel(case):
    g, gsi = GAMMA[case["key"]], GAMMA_SI[case["key"]]
    mine = case["key"] == "other"
    roof = case["key"] == "roof_other"
    col = C["accent"] if mine else (C["load"] if roof else C["text"])

    cv = Canvas(PW2, PH2)
    win(cv, -XY2, XY2, -XY2, XY2, L=30, R=30, T=80, B=126)
    cv.panel(f"{case['no']} {case['title']}", case["sub"])

    # 分析平面畫在構材之下（只在空白處露出），避免壓到「梁」與柱標註
    if mine:
        cv.line((-XY2 + 4, 0), (XY2 - 4, 0), C["accent"], 1.8, dash="9 6")
        cv.text_px(cv.X(-XY2 + 8), cv.Y(0) - 12, "分析平面", 11.5, C["accent"],
                   "start", weight="700")
    for f in case["faces"]:
        cv.polygon(BEAM_RECT[f], C["border"], C["member2"], 1.8)
        cv.text_px(*cv.P(BEAM_LABEL[f]), "梁", 12.5, C["muted"], weight="700")
    cv.polygon([(XCL, -HC / 2), (XCR, -HC / 2), (XCR, HC / 2), (XCL, HC / 2)],
               C["fill_s"], C["load"] if roof else C["member"], 2.4)
    for f in "NSEW":
        p0, p1 = FACE_SEG[f]
        if f in case["faces"]:
            cv.line(p0, p1, C["deform"], 5.0, cap="butt")
        else:
            cv.line(p0, p1, C["load"], 3.4, dash="7 5", cap="butt")
    cv.text_px(cv.X(0), cv.Y(14), f"柱 {BC:g}×{HC:g}", 12,
               C["load"] if roof else C["text"], weight="700")

    if roof:
        _roof_icon(cv)
    if mine:
        cv.text_px(cv.X(-XY2 + 8), cv.Y(-HC / 2 - EXT_DRAW / 2),
                   "此平面內僅 1 根梁", 11.5, C["accent"], "start", weight="700")
        cv.text_px(cv.X(-XY2 + 8), cv.Y(-HC / 2 - EXT_DRAW / 2) + 17,
                   "→ 不滿足三面／一雙對面", 11, C["accent"], "start")

    cv.math_px(PW2 / 2, PH2 - 104, M(f"γ = {g:g}"), 25, col, weight="700")
    cv.text_px(PW2 / 2, PH2 - 78, f"SI 制：{gsi:.1f}√f'_{{c}}（MPa）", 12.5,
               C["muted"])
    cv.text_px(PW2 / 2, PH2 - 54,
               f"φV_{{n}} = {phi_vn(g)*TF:.1f} tf", 14, col, weight="700")
    if case["tag"]:
        cv.text_px(PW2 / 2, PH2 - 30, case["tag"], 12.5, col, weight="700")
    else:
        cv.text_px(PW2 / 2, PH2 - 30, "本題不適用", 12, C["muted"])
    return cv


def fig2():
    return compose(
        [fig2_panel(c) for c in CASES], cols=2,
        title="圖 2　接頭圍束分類與 γ 值：角柱為什麼落入「其他」類",
        sub="俯視平面圖｜藍粗實線＝該面受梁圍束　紅虛線＝該面未受圍束｜"
            "圍束判準：梁寬 ≥ 3/4 柱寬且梁深 ≥ 最深梁的 3/4",
        note=f"γ 為 kgf/cm² 制（土木 401），括號內為 SI 制 √f'c 係數；"
             f"接頭強度與 γ 成正比（同一 Aj = {AJ:,.0f} cm²，"
             f"每 1.0 之 γ ＝ {PHI_UNIT*TF:.1f} tf）")


# ══════════════════════════════════════════════════════════
# 圖 3　需求 vs 容量：兩條容量線把三個需求值夾在中間
# ══════════════════════════════════════════════════════════
def fig3():
    cases = [
        (f"容量 φV_{{n}}｜γ = {GAMMA['other']:g}", "中間樓層（柱延伸至上方）",
         PHI_VN * TF, M(f"φV_{{n}} = {PHI_VN*TF:.2f} tf"), C["compr"]),
        ("需求 V_{jh} ≈ T（保守）", f"忽略 V_{{col}}｜利用率 {UTIL_T:.0%}",
         T_FORCE * TF, M(f"V_{{jh}} ≈ {T_FORCE*TF:.2f} tf"), C["accent"]),
        ("需求 V_{jh} = T − V_{col}", f"主線｜利用率 {UTIL:.0%}　通過 ✓",
         V_JH * TF, M(f"V_{{jh}} = {V_JH*TF:.2f} tf"), C["load"]),
        (f"容量 φV_{{n}}｜γ = {GAMMA['roof_other']:g}", "屋頂層｜柱未延伸　不通過",
         PHI_VN_ROOF * TF, M(f"φV_{{n}} = {PHI_VN_ROOF*TF:.2f} tf"), C["muted"]),
        ("需求 V_{jh}（改用 f_{y}）", f"不計超強｜利用率 {UTIL_FY:.0%}",
         V_JH_FY * TF, M(f"V_{{jh}} = {V_JH_FY*TF:.2f} tf"), C["member2"]),
    ]
    return bar_compare(
        cases,
        title="圖 3　角柱接頭剪力：三個需求值與兩條容量線放在同一尺標",
        sub=f"列名前綴標明需求或容量；百分比皆以最大值 "
            f"φV_{{n}}（γ = {GAMMA['other']:g}）= {PHI_VN*TF:.2f} tf 為 100%，"
            f"故需求列的百分比即為利用率",
        note=f"交叉點：屋頂層容量 {PHI_VN_ROOF*TF:.1f} tf ＜ 主線需求 {V_JH*TF:.1f} tf"
             f"（超出 {UTIL_ROOF-1:.1%}）× 不通過；"
             f"忽略 Vcol 的保守下限利用率已達 {UTIL_T:.0%}，餘裕僅 {1-UTIL_T:.0%}").svg()


# ══════════════════════════════════════════════════════════
FIGURES = [
    ("1-joint-fbd", fig1,
     "V_col 寫成 2M_pr/H（忘記接頭梁彎矩由上下兩根柱分擔）；"
     "V_jh 寫成 T + V_col（V_col 其實是減項）"),
    ("2-gamma", fig2,
     "角柱接頭誤歸為三面（3.9）或四面（5.3）——角柱在任一分析平面內只遮住一面"),
    ("3-check", fig3,
     "只算中間樓層就宣告通過（318-19 屋頂層 γ=2.2 會不通過）；"
     "忽略 V_col 時餘裕其實只剩 3%"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    checks = [
        ("A_s cm2",        AS,                 30.42,   0.001),
        ("T kgf",          T_FORCE,            159705,  1.0),
        ("a cm",           A_BLK,              11.18,   0.01),
        ("M_pr tf-m",      MPR * TFM,          102.86,  0.01),
        ("V_col tf",       V_COL * TF,         28.18,   0.01),
        ("V_col 舊版 tf",   V_COL_WRONG * TF,   45.89,   0.05),
        ("V_jh tf",        V_JH * TF,          131.52,  0.01),
        ("b_j cm",         BJ,                 60.0,    0.001),
        ("A_j cm2",        AJ,                 3600.0,  0.01),
        ("φV_n tf",        PHI_VN * TF,        163.85,  0.01),
        ("利用率",          UTIL,               0.803,   0.001),
        ("φV_n 屋頂 tf",    PHI_VN_ROOF * TF,   112.65,  0.01),
        ("利用率 屋頂",      UTIL_ROOF,          1.168,   0.001),
        ("T (f_y) kgf",    T_FY,               127764,  1.0),
        ("a (f_y) cm",     A_FY,               8.946,   0.002),
        ("M_n (f_y) tf-m", MN_FY * TFM,        83.72,   0.01),
        ("V_col (f_y) tf", V_COL_FY * TF,      22.94,   0.01),
        ("V_jh (f_y) tf",  V_JH_FY * TF,       104.83,  0.01),
        ("利用率 (f_y)",    UTIL_FY,            0.640,   0.001),
        ("l_dh cm",        L_DH,               37.1,    0.05),
    ]
    print(f"── 與 {TAG}.md §4／§6 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<16} 算得 {got:>13.6g}   .md {want:>10}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"
    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<34} 攔：{catches}")


if __name__ == "__main__":
    main()
