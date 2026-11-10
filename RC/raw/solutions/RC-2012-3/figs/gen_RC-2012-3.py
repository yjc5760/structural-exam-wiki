#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2012-3 強柱弱梁下柱塑鉸區箍筋設計 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2012-3.md §1 給定的原始資料（含由 RC-2012-2 帶入的 Mpr）；
     Vu、lo、bc、Ach、Ash1/s、Ash2/s、s0、6db、s_shear、Vs、φVs、
     以及「舊版把整個 Mpr 給單一柱端」與「bc 依規範量至箍筋外緣」兩組
     對照值全部現算，檔尾對 §4／§5 公佈值 assert。
  2. 改 §1 任一數字重跑，三張圖跟著變（含反曲點位置、長條圖比例、核心虛線位置）。
  3. FIGURES 表寫明每張圖攔什麼錯。

用法：
    STRUCTDRAW_DIR=<skill>/scripts python3 gen_RC-2012-3.py figs
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose
from recipes import bar_compare

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2012-3"

# ══════════════════════════════════════════════════════════
# §1 原始給定（材料、幾何、配筋）
# ══════════════════════════════════════════════════════════
FC, FYT = 280.0, 4200.0        # kgf/cm^2　混凝土、箍筋降伏強度
BCOL = HCOL = 60.0             # cm　柱斷面 60x60
COVER = 6.0                    # cm　保護層（量至主筋中心）
N_BAR_FACE = 4                 # 每面主筋根數（12-#7：頂底各 4、側面各 2 不含角筋）
DB_MAIN = 2.22                 # cm　#7 主筋直徑
AB_MAIN = 3.87                 # cm^2 一支 #7
DB_TIE = 1.27                  # cm　#4 箍筋直徑
AB_TIE = 1.27                  # cm^2 一支 #4
N_LEG = 4                      # 4 legs #4
LN = 3.00                      # m　柱淨高
NU = 50.0e3                    # kgf　柱設計極限軸力
PHI_V = 0.75                   # 剪力強度折減

# §1「由第二題得」——RC-2012-2 之梁端可能彎矩強度
MPR_NEG = 75.52                # tf·m　頂筋 6-#8 受拉（控制）
MPR_POS = 41.11                # tf·m　底筋 4-#7 受拉

# §1 附圖標註：核心尺寸 48 cm（保護層 6 cm 量至主筋中心）
BC_FIG = BCOL - 2 * COVER      # = 48.0，取法 A 的依據

TF = 1e-3                      # kgf → tf

# ── §4 Step 1：柱地震設計剪力（接頭彎矩由上下柱分擔）─────────
SUM_M_JOINT = MPR_NEG                     # 單跨外圍接頭只有一根梁
K_SHARE_TOP, K_SHARE_BOT = 1.0, 1.0       # 上、下柱相對勁度（等淨高等斷面 ⇒ 1:1）
N_COL_AT_JOINT = 2                        # 接頭上、下各一根柱
M_COL_TOP = SUM_M_JOINT * K_SHARE_TOP / (K_SHARE_TOP + K_SHARE_BOT)
M_COL_BOT = SUM_M_JOINT * K_SHARE_BOT / (K_SHARE_TOP + K_SHARE_BOT)
M_COL_HALF = M_COL_TOP                    # 等勁度 ⇒ 各半 ⇒ 兩者相同
VU = (M_COL_TOP + M_COL_BOT) / LN         # tf
VU_WRONG = (MPR_NEG + MPR_NEG) / LN       # 舊版錯誤：兩端各給一個完整 Mpr
XI_INFL = M_COL_BOT / (M_COL_BOT + M_COL_TOP)      # 反曲點（由柱端彎矩線性內插）

# ── §4 Step 2：塑鉸區長度 ────────────────────────────────
LO = max(LN * 100 / 6, max(BCOL, HCOL), 45.0)      # cm

# ── §4 Step 3：斷面幾何 ─────────────────────────────────
AG = BCOL * HCOL
D_EFF = HCOL - COVER                       # 剪力用有效深度
AV = N_LEG * AB_TIE
SQFC = math.sqrt(FC)


def confinement(bc):
    """給定核心尺寸 bc，回傳整組圍束需求與其容許間距。"""
    ach = bc * bc
    r = AG / ach - 1.0
    a1 = 0.3 * bc * (FC / FYT) * r          # A_sh1 / s
    a2 = 0.09 * bc * (FC / FYT)             # A_sh2 / s
    return dict(bc=bc, ach=ach, ratio=r, a1=a1, a2=a2,
                s1=AV / a1, s2=AV / a2)


CASE_A = confinement(BC_FIG)                                    # 量至主筋中心
BC_OUT = BCOL - 2 * (COVER - DB_MAIN / 2 - DB_TIE)              # 量至箍筋外緣
CASE_B = confinement(BC_OUT)

# ── §4 Step 4：幾何間距上限 ─────────────────────────────
HX = BC_FIG / (N_BAR_FACE - 1)             # 相鄰被支撐主筋中心距
S0_RAW = 10.0 + (35.0 - HX) / 3.0
S0_CAP = 15.0                              # 規範上限 150 mm
S0 = min(S0_RAW, S0_CAP)
S_B4 = BCOL / 4.0
S_6DB = 6.0 * DB_MAIN
S_GEOM = min(S_B4, S_6DB, S0)

# ── §4 Step 5／6：剪力需求（Vc = 0 條件）─────────────────
VC0_THRESH = 0.05 * FC * AG * TF           # tf　＝ A_g f'c / 20
VC_IS_ZERO = NU * TF <= VC0_THRESH
VS_REQ = VU / PHI_V                        # tf（Vc = 0）
S_SHEAR = AV * FYT * D_EFF / (VS_REQ / TF)

# ── §4 Step 7／8：採用間距與驗算 ────────────────────────
S_CANDIDATES = [S_SHEAR, CASE_A["s2"], S_B4, S0, S_6DB, CASE_A["s1"]]
S_ADOPT = math.floor(min(S_CANDIDATES))                 # 9 cm
S_OUTSIDE = math.floor(min(S_6DB, S0_CAP))              # 塑鉸區外 13 cm
ASH1_AT_S = CASE_A["a1"] * S_ADOPT
ASH2_AT_S = CASE_A["a2"] * S_ADOPT
VS_AT_S = AV * FYT * D_EFF / S_ADOPT * TF
PHI_VS_AT_S = PHI_V * VS_AT_S
MARGIN = PHI_VS_AT_S / VU

# ── §5①／§6：若不取 Vc = 0 的兩種 Vc 公式（僅供註記）───────
VC_AXIAL_OLD = 0.53 * (1 + NU / (140 * AG)) * SQFC * BCOL * D_EFF * TF
VC_318_19 = (0.53 * SQFC + NU / (6 * AG)) * BCOL * D_EFF * TF


def M(s):
    """FONT_M（數學襯線）缺中日韓字，cairosvg 會靜默丟字。
    所有進 math()/math_px() 的字串一律經此守衛。"""
    assert not any(ord(ch) > 0x2E80 for ch in s), f"math 字串不得含中日韓字元：{s}"
    return s


def break_mark(cv, p, vertical, s=0.16, gap=0.13, color=C["member2"]):
    """構材示意斷開（雙斜線）。"""
    x, y = p
    for k in (0.0, gap):
        if vertical:
            cv.line((x - s, y + k - s * 0.45), (x + s, y + k + s * 0.45), color, 2.2)
        else:
            cv.line((x + k - s * 0.45, y - s), (x + k + s * 0.45, y + s), color, 2.2)


def dash_rect(cv, a, b, color, w=1.8, dash="6 4"):
    """以模型座標畫虛線矩形（左下 a、右上 b）。"""
    (x0, y0), (x1, y1) = a, b
    cv.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], color, w, dash=dash)


# ══════════════════════════════════════════════════════════
# 圖 1　塑鉸機構與接頭彎矩分擔
# ══════════════════════════════════════════════════════════
PW1, PH1 = 600, 600

JH = 0.30                 # 接頭半寬（柱寬 0.6 m 的一半，m）
BEAM_DRAW = 2.60          # 梁只畫到此處後示意斷開（m）
BEAM_CLEAR = 7.00         # m　梁淨跨（RC-2012-2 附圖）


def fig1_left():
    XMIN, XMAX = -0.62, 2.80
    YMIN, YMAX = -(LN + JH + 0.15), (LN + JH + 0.15)
    mL, mR, mT, mB = 120, 270, 100, 110
    sx = min((PW1 - mL - mR) / (XMAX - XMIN), (PH1 - mT - mB) / (YMAX - YMIN))
    cv = Canvas(PW1, PH1, sx=sx, ox=mL - XMIN * sx, oy=mB - YMIN * sx)
    cv.panel("塑鉸機構與接頭彎矩平衡", "單跨構架局部：一根梁 ＋ 接頭 ＋ 上下柱")

    ytop, ybot = JH + LN, -(JH + LN)

    # 上、下柱（淨高各 LN）與梁（僅繪端部）
    cv.line((0, JH), (0, ytop), C["member"], 7.0, cap="butt")
    cv.line((0, -JH), (0, ybot), C["member"], 7.0, cap="butt")
    cv.line((JH, 0), (BEAM_DRAW, 0), C["member"], 7.0, cap="butt")
    break_mark(cv, (0, ytop), vertical=True)
    break_mark(cv, (0, ybot - 0.13), vertical=True)
    break_mark(cv, (BEAM_DRAW - 0.13, 0), vertical=False)

    # 接頭
    cv.polygon([(-JH, -JH), (JH, -JH), (JH, JH), (-JH, JH)], "#EDF1F6", C["member"], 2.4)

    # 梁端塑鉸
    cv.dot((JH + 0.12, 0), 9.0, fill="#FFFFFF", stroke=C["accent"], w=3.2)
    cv.text_px(cv.X(JH + 0.12), cv.Y(0) + 26, "塑鉸", 12.5, C["accent"], weight="700")

    # 梁端 Mpr 傳入接頭
    cv.moment_arrow((1.30, 0), r=30, ccw=True, color=C["load"], w=3.0, span=250, start=110)
    cv.text_px(cv.X(BEAM_DRAW) + 28, cv.Y(0) - 13, "梁端可能彎矩強度", 12.5,
               C["load"], "start")
    cv.math_px(cv.X(BEAM_DRAW) + 28, cv.Y(0) + 11,
               M(f"M_{{pr}}^{{-}} = {MPR_NEG:.2f} tf·m"), 15.5, C["load"],
               "start", weight="700")

    # 上、下柱各分擔一半
    for ys, tag, mv in ((2.15, "top", M_COL_TOP), (-2.15, "bot", M_COL_BOT)):
        cv.moment_arrow((0, ys), r=30, ccw=True, color=C["bmd"], w=2.8, span=250, start=110)
        cv.math_px(cv.X(0) + 44, cv.Y(ys),
                   M(f"M_{{col,{tag}}} = {mv:.2f}"), 13.5, C["bmd"],
                   "start", weight="700")
        cv.text_px(cv.X(0) + 44, cv.Y(ys) + 18, "tf·m（各分擔一半）", 12, C["bmd"], "start")

    # 淨高尺寸
    cv.dim((0, JH), (0, ytop), M(f"l_{{n}} = {LN:.1f} m"), off=-58, label_off=-15)
    cv.dim((0, ybot), (0, -JH), M(f"l_{{n}} = {LN:.1f} m"), off=-58, label_off=-15)

    cv.text_px(cv.X(0) + 20, cv.Y(ytop) - 6, "續上層柱", 12, C["muted"], "start")
    cv.text_px(cv.X(0) + 20, cv.Y(ybot) + 8, "續下層柱", 12, C["muted"], "start")
    cv.text_px(cv.X(1.60), cv.Y(0) + 50,
               f"梁淨跨 {BEAM_CLEAR:.1f} m（僅繪端部）", 12.5, C["muted"])

    cv.math_px(PW1 / 2, PH1 - 82,
               M(f"ΣM_{{col}} = ΣM_{{pr,beam}} = {SUM_M_JOINT:.2f} tf·m"),
               15.5, C["bmd"], weight="700")
    cv.text_px(PW1 / 2, PH1 - 56,
               "上下柱淨高與斷面相同 ⇒ 勁度相同 ⇒ 各分擔一半", 13, C["muted"])
    cv.math_px(PW1 / 2, PH1 - 30,
               M(f"M_{{col,top}} = M_{{col,bot}} = {SUM_M_JOINT:.2f}/{N_COL_AT_JOINT:g}"
                 f" = {M_COL_TOP:.2f} tf·m"), 14, C["load"], weight="700")
    return cv


def fig1_right():
    MS = 0.75 / max(M_COL_TOP, M_COL_BOT)  # 彎矩圖繪圖比例（模型單位 / tf·m）
    XMIN, XMAX = -1.45, 1.45
    YMIN, YMAX = -0.35, LN + 0.35
    mL, mR, mT, mB = 110, 110, 100, 170
    sx = min((PW1 - mL - mR) / (XMAX - XMIN), (PH1 - mT - mB) / (YMAX - YMIN))
    cv = Canvas(PW1, PH1, sx=sx, ox=mL - XMIN * sx, oy=mB - YMIN * sx)
    cv.panel("單根柱的彎矩圖與剪力",
             f"上下端各 {M_COL_HALF:.2f} tf·m，反曲點在柱淨高中點")

    mbb, mbt = M_COL_BOT * MS, M_COL_TOP * MS   # 下、上端彎矩的繪圖長度
    yi = XI_INFL * LN                      # 反曲點高度（由柱端彎矩線性內插）

    # 彎矩圖：下端受拉側在左、上端受拉側在右，直線通過反曲點
    cv.polygon([(0, 0), (-mbb, 0), (0, yi)], C["fill_m"], C["bmd"], 2.2)
    cv.polygon([(0, yi), (mbt, LN), (0, LN)], C["fill_m"], C["bmd"], 2.2)

    # 柱與兩端接頭面
    cv.line((0, 0), (0, LN), C["member"], 8.0, cap="butt")
    for yy in (0.0, LN):
        cv.line((-0.19, yy), (0.19, yy), C["member"], 5.0, cap="butt")

    # 反曲點（標註放在軸線左側，避開上半彎矩圖）
    cv.dot((0, yi), 6.2, fill="#FFFFFF", stroke=C["accent"], w=2.9)
    cv.text_px(cv.X(0) - 18, cv.Y(yi) - 9, "反曲點 M = 0", 13, C["accent"],
               "end", weight="700")
    cv.math_px(cv.X(0) - 18, cv.Y(yi) + 11,
               M(f"l_{{n}}/2 = {yi:.1f} m"), 13, C["accent"], "end")

    # 端點彎矩值
    cv.math_px(cv.X(-mbb) - 10, cv.Y(0) - 16, M(f"{M_COL_BOT:.2f} tf·m"), 13.5,
               C["bmd"], "end", weight="700")
    cv.math_px(cv.X(mbt) + 10, cv.Y(LN) + 16, M(f"{M_COL_TOP:.2f} tf·m"), 13.5,
               C["bmd"], "start", weight="700")

    # 柱剪力（上下等值反向）
    cv.arrow((-0.02, LN + 0.24), (0.62, LN + 0.24), C["load"], 3.2, 11)
    cv.math_px(cv.X(0.62) + 10, cv.Y(LN + 0.24), M(f"V_{{u}} = {VU:.2f} tf"), 14,
               C["load"], "start", weight="700")
    cv.arrow((0.02, -0.22), (-0.62, -0.22), C["load"], 3.2, 11)
    cv.text_px(cv.X(-0.62) - 10, cv.Y(-0.22), "（反向、等值）", 12, C["muted"], "end")

    cv.dim((0, 0), (0, LN), M(f"l_{{n}} = {LN:.1f} m"), off=110, label_off=16)

    cv.math_px(PW1 / 2, PH1 - 144,
               M(f"V_{{u}} = ({M_COL_TOP:.2f} + {M_COL_BOT:.2f}) / {LN:.1f}"
                 f" = {VU:.2f} tf"), 16.5, C["load"], weight="700")

    cv.rect_px(40, PH1 - 124, PW1 - 80, 100, C["fill_t"], 12, C["load"], 1.4)
    cv.text_px(PW1 / 2, PH1 - 102, "【舊版錯誤】把整個 Mpr 給單一柱端", 13.5,
               C["load"], weight="700")
    cv.math_px(PW1 / 2, PH1 - 76,
               M(f"V_{{u}} = ({MPR_NEG:.2f} + {MPR_NEG:.2f}) / {LN:.1f}"
                 f" = {VU_WRONG:.1f} tf"), 15, C["load"], weight="700")
    cv.text_px(PW1 / 2, PH1 - 50,
               f"→ 大了一倍（正解為其半數 {VU:.2f} tf）", 13, C["muted"])
    return cv


def fig1():
    return compose(
        [fig1_left(), fig1_right()],
        title=f"圖 1　{TAG} 塑鉸機構：梁端 Mpr 如何變成柱的設計剪力",
        sub="梁端形成塑鉸 → 接頭彎矩平衡 → 上下柱依勁度分擔 → 反曲點在柱淨高中點 → 柱剪力",
        note="關鍵：分子是「一個接頭」的梁 Mpr 總和，不是上下兩個接頭的總和",
        cols=2)


# ══════════════════════════════════════════════════════════
# 圖 2　柱斷面與核心尺寸 bc 的兩種取法
# ══════════════════════════════════════════════════════════
PW2, PH2 = 560, 640
TIE_MID = COVER - DB_MAIN / 2 - DB_TIE / 2      # 箍筋中心線至混凝土表面
TIE_OUT = COVER - DB_MAIN / 2 - DB_TIE          # 箍筋外緣至混凝土表面
BAR_POS = [COVER + HX * i for i in range(N_BAR_FACE)]   # 主筋座標（每面 4 根）


def _section_panel(title, sub, core_half, dim_pts, dim_label, note_start, ann):
    mL, mR, mT, mB = 150, 150, 150, 230
    sx = min((PW2 - mL - mR) / BCOL, (PH2 - mT - mB) / HCOL)
    cv = Canvas(PW2, PH2, sx=sx, ox=mL, oy=mB)
    cv.panel(title, sub)

    # 混凝土毛斷面
    cv.polygon([(0, 0), (BCOL, 0), (BCOL, HCOL), (0, HCOL)],
               "#EDF1F6", C["member"], 2.6)

    # 4 legs #4：外圍箍 ＋ 兩向繫筋（線寬＝真實箍筋直徑）
    tw = DB_TIE * cv.sx
    a, b = TIE_MID, BCOL - TIE_MID
    cv.poly([(a, a), (b, a), (b, b), (a, b), (a, a)], C["load"], tw)
    for t in BAR_POS[1:-1]:
        cv.line((t, a), (t, b), C["load"], tw, cap="butt")
        cv.line((a, t), (b, t), C["load"], tw, cap="butt")

    # 12-#7 主筋（半徑為真實 db/2）
    for x in BAR_POS:
        for y in BAR_POS:
            if x in (BAR_POS[0], BAR_POS[-1]) or y in (BAR_POS[0], BAR_POS[-1]):
                cv.circle((x, y), DB_MAIN / 2, C["member"], "#FFFFFF", 1.2)

    # 核心邊界（虛線）——本格採用的 bc 量測邊界，畫在最上層才看得出量測起點
    dash_rect(cv, (core_half, core_half), (BCOL - core_half, HCOL - core_half),
              C["accent"], 2.0)

    # hx：相鄰被支撐主筋中心距（放在底面，讓頂面留給 bc 註記）
    cv.dim((BAR_POS[0], BAR_POS[0]), (BAR_POS[1], BAR_POS[0]),
           M(f"h_{{x}} = {HX:.0f}"), off=-26, label_off=-13, size=12)

    # bc 量測起點註記
    cv.text_px(cv.X(BCOL / 2), cv.Y(HCOL / 2) - 10, "b_c 量至", 13, C["accent"],
               weight="700")
    cv.text_px(cv.X(BCOL / 2), cv.Y(HCOL / 2) + 10, ann, 13, C["accent"],
               weight="700")
    # 引線指向 bc 的量測起點（箭頭端退開 2.5 cm，避免被箍筋與核心虛線蓋住）
    x0, y0 = BCOL / 2 - 4, HCOL / 2 + 12
    x1, y1 = dim_pts[0]
    dl = math.hypot(x1 - x0, y1 - y0)
    cv.arrow((x0, y0), (x1 - (x1 - x0) / dl * 2.5, y1 - (y1 - y0) / dl * 2.5),
             C["accent"], 2.2, 9)

    # bc 尺寸線（拉到斷面上方同一高度）
    off = 116 - cv.Y(dim_pts[0][1])
    cv.dim(dim_pts[0], dim_pts[1], M(dim_label), off=off, label_off=-16)
    for p in dim_pts:
        cv.dot(p, 3.6, fill=C["accent"], stroke="#FFFFFF", w=1.2)

    # 毛斷面尺寸
    cv.dim((0, 0), (BCOL, 0), M(f"{BCOL:.0f} cm"), off=40, label_off=16)
    cv.dim((BCOL, 0), (BCOL, HCOL), M(f"{HCOL:.0f}"), off=34, label_off=13)

    cv.text_px(PW2 / 2, PH2 - 148, note_start, 13, C["muted"])
    return cv


def fig2():
    a = _section_panel(
        "取法 A（本解主線）：b_c 量至主筋中心",
        f"依原卷附圖標註 {BC_FIG:.0f} cm",
        COVER,
        [(BAR_POS[0], BAR_POS[-1]), (BAR_POS[-1], BAR_POS[-1])],
        f"b_{{c}} = {BC_FIG:.1f} cm",
        f"b_c 量測起點：主筋中心（保護層 {COVER:.0f} cm 至主筋心）",
        "主筋中心")
    a.math_px(PW2 / 2, PH2 - 124,
              M(f"b_{{c}} = {BCOL:.0f} - 2({COVER:.0f}) = {BC_FIG:.1f} cm"),
              14.5, C["accent"], weight="700")
    a.math_px(PW2 / 2, PH2 - 100,
              M(f"A_{{ch}} = {BC_FIG:.1f} × {BC_FIG:.1f} = {CASE_A['ach']:.0f} cm^{{2}}"
                f" ; A_{{g}}/A_{{ch}} - 1 = {CASE_A['ratio']:.4f}"), 14, C["text"])
    a.math_px(PW2 / 2, PH2 - 76,
              M(f"A_{{sh1}}/s = {CASE_A['a1']:.3f} cm^{{2}}/cm  →  "
                f"s ≤ {AV:.2f}/{CASE_A['a1']:.3f} = {CASE_A['s1']:.2f} cm"),
              14, C["load"], weight="700")
    a.text_px(PW2 / 2, PH2 - 50, f"最終 s = {S_ADOPT:g} cm　←　圍束公式一控制",
              15, C["load"], weight="700")
    a.text_px(PW2 / 2, PH2 - 26, "（剪力需求與幾何上限均寬鬆，不控制）",
              12.5, C["muted"])

    b = _section_panel(
        "取法 B（嚴格依規範）：b_c 量至箍筋外緣",
        f"b_c = {BCOL:.0f} - 2({COVER:.0f} - {DB_MAIN/2:.2f} - {DB_TIE:.2f})",
        TIE_OUT,
        [(TIE_OUT, HCOL - TIE_OUT), (BCOL - TIE_OUT, HCOL - TIE_OUT)],
        f"b_{{c}} = {BC_OUT:.2f} cm",
        f"b_c 量測起點：箍筋外緣（{COVER:.0f} - {DB_MAIN/2:.2f} - {DB_TIE:.2f}"
        f" = {TIE_OUT:.2f} cm）",
        "箍筋外緣")
    b.math_px(PW2 / 2, PH2 - 124,
              M(f"b_{{c}} = {BCOL:.0f} - 2({TIE_OUT:.2f}) = {BC_OUT:.2f} cm"),
              14.5, C["accent"], weight="700")
    b.math_px(PW2 / 2, PH2 - 100,
              M(f"A_{{ch}} = {BC_OUT:.2f} × {BC_OUT:.2f} = {CASE_B['ach']:.1f} cm^{{2}}"
                f" ; A_{{g}}/A_{{ch}} - 1 = {CASE_B['ratio']:.4f}"), 14, C["text"])
    b.math_px(PW2 / 2, PH2 - 76,
              M(f"A_{{sh1}}/s = {CASE_B['a1']:.3f} cm^{{2}}/cm  →  "
                f"s ≤ {AV:.2f}/{CASE_B['a1']:.3f} = {CASE_B['s1']:.1f} cm"),
              14, C["load"], weight="700")
    b.text_px(PW2 / 2, PH2 - 50,
              f"最終 s = {S_OUTSIDE:g} cm　←　6d_b 幾何上限控制",
              15, C["load"], weight="700")
    b.text_px(PW2 / 2, PH2 - 26,
              f"（圍束需求放寬 {CASE_A['a1']/CASE_B['a1']-1:.0%}，"
              f"改由 6d_b = {S_6DB:.2f} cm 控制）", 12.5, C["muted"])

    return compose(
        [a, b],
        title="圖 2　核心尺寸 bc 的兩種取法：規範定義（箍筋外緣）vs 原卷附圖標註（主筋中心）",
        sub=f"柱 {BCOL:.0f}×{HCOL:.0f} cm；12-#7 主筋 db = {DB_MAIN} cm；"
            f"4 legs #4 箍筋 Av = {N_LEG:g}×{AB_TIE} = {AV:.2f}；"
            f"橘虛線＝該取法的核心邊界",
        note=f"同一斷面、同一組箍筋，量測起點只差 {(BC_OUT-BC_FIG)/2:.2f} cm，"
             f"Ash 需求就差 {CASE_A['a1']/CASE_B['a1']-1:.0%}，"
             f"最終間距由 {S_ADOPT:g} cm 變成 {S_OUTSIDE:g} cm",
        cols=2)


# ══════════════════════════════════════════════════════════
# 圖 3　六個間距候選比較
# ══════════════════════════════════════════════════════════
def fig3():
    cases = [
        ("剪力強度需求", f"Vc = 0，餘裕 {MARGIN:.1f} 倍", S_SHEAR,
         M(f"s ≤ A_{{v}}f_{{yt}}d/(V_{{u}}/φ) = {S_SHEAR:.2f} cm"), C["sfd"]),
        ("圍束公式二", "純配箍率下限", CASE_A["s2"],
         M(f"s ≤ {AV:.2f}/{CASE_A['a2']:.3f} = {CASE_A['s2']:.2f} cm"), C["member2"]),
        ("柱最小邊 / 4", f"{BCOL:.0f}/4，不控制", S_B4,
         M(f"s ≤ b/4 = {S_B4:.2f} cm"), C["muted"]),
        ("s_0 主筋橫向間距", f"被 {S0_CAP:.0f} cm 上限截住", S0,
         M(f"s ≤ min(10+(35-h_{{x}})/3, {S0_CAP:.0f}) = {S0:.2f} cm"), C["accent"]),
        ("6d_b 主筋直徑", "塑鉸區外的控制值", S_6DB,
         M(f"s ≤ 6d_{{b}} = {S_6DB:.2f} cm"), C["compr"]),
        ("圍束公式一 ← 控制", "含 Ag/Ach 項，最嚴格", CASE_A["s1"],
         M(f"s ≤ {AV:.2f}/{CASE_A['a1']:.3f} = {CASE_A['s1']:.2f} cm"), C["load"]),
    ]
    I_S0 = 3                                   # s_0 那一列（與 cases 順序一致）
    assert cases[I_S0][2] == S0 < S0_RAW
    cv = bar_compare(
        cases,
        title="圖 3　柱塑鉸區箍筋間距：六個候選上限同時攤開，取最嚴格者",
        sub="長條越長＝間距越大＝越寬鬆；四個幾何／規範上限與兩個圍束需求、一個剪力需求並列",
        note=f"採用 s = {S_ADOPT:g} cm（圍束公式一控制）；剪力需求 {S_SHEAR:.2f} cm "
             f"餘裕 {MARGIN:.1f} 倍；塑鉸區外 s ≤ min(6d_b, {S0_CAP:.0f}) = "
             f"{min(S_6DB, S0_CAP):.2f} → 取 {S_OUTSIDE:g} cm")

    # s_0 那一列：把「公式值 16.33 被 15 上限截住」畫成虛線延伸段
    peak = max(c[2] for c in cases)
    x0, bw, row_h = 320, 400, 86
    y = 122 + I_S0 * row_h
    xa, xb = x0 + bw * S0 / peak, x0 + bw * S0_RAW / peak
    cv.parts.append(f'<rect x="{xa:.1f}" y="{y-17}" width="{xb-xa:.1f}" height="34" '
                    f'rx="8" fill="none" stroke="{C["accent"]}" stroke-width="1.8" '
                    f'stroke-dasharray="5 4"/>')
    cv.math_px(xb + 8, y - 8, M(f"→ {S0_RAW:.2f}"), 12, C["accent"], "start")
    cv.text_px(xb + 8, y + 10, "公式值被截住", 11.5, C["accent"], "start")
    return cv.svg()


# ══════════════════════════════════════════════════════════
FIGURES = [
    ("1-mechanism", fig1,
     "把一根柱的上下兩端各給一個「完整的」梁 Mpr，得 Vu = 50.3 tf（正解 25.17）"),
    ("3-section", fig2,
     "bc／Ach 的量測起點搞錯（規範量至箍筋外緣，原卷附圖標的是主筋心）"),
    ("2-spacing", fig3,
     "以為剪力需求控制（其實寬鬆到 34.33 cm）；沒有取六者中最嚴格的那一個"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    checks = [
        ("Vu tf",            VU,               25.17,   0.01),
        ("Mcol_half tf·m",   M_COL_HALF,       37.76,   0.01),
        ("Vu_wrong tf",      VU_WRONG,         50.33,   0.02),
        ("XI_infl",          XI_INFL,          0.50,    1e-9),
        ("lo cm",            LO,               60.0,    1e-9),
        ("bc_A cm",          CASE_A["bc"],     48.0,    1e-9),
        ("Ach_A cm2",        CASE_A["ach"],    2304.0,  1e-6),
        ("Ag cm2",           AG,               3600.0,  1e-9),
        ("Av cm2",           AV,               5.08,    1e-9),
        ("Ag/Ach-1 (A)",     CASE_A["ratio"],  0.5625,  1e-6),
        ("Ash1/s (A)",       CASE_A["a1"],     0.540,   0.001),
        ("Ash2/s",           CASE_A["a2"],     0.288,   0.001),
        ("s_conf_A cm",      CASE_A["s1"],     9.41,    0.01),
        ("s_Ash2 cm",        CASE_A["s2"],     17.64,   0.01),
        ("hx cm",            HX,               16.0,    1e-9),
        ("s0_raw cm",        S0_RAW,           16.33,   0.01),
        ("s0 cm",            S0,               15.0,    1e-9),
        ("6db cm",           S_6DB,            13.32,   1e-9),
        ("s_geom cm",        S_GEOM,           13.32,   1e-9),
        ("Ash1@9 cm2",       ASH1_AT_S,        4.86,    0.01),
        ("Ash2@9 cm2",       ASH2_AT_S,        2.59,    0.01),
        ("Vc0_thresh tf",    VC0_THRESH,       50.4,    0.01),
        ("Vs_req tf",        VS_REQ,           33.56,   0.01),
        ("s_shear cm",       S_SHEAR,          34.33,   0.01),
        ("Vs@9 tf",          VS_AT_S,          128.0,   0.05),
        ("phiVs@9 tf",       PHI_VS_AT_S,      96.0,    0.05),
        ("s_adopt cm",       S_ADOPT,          9.0,     1e-9),
        ("s_outside cm",     S_OUTSIDE,        13.0,    1e-9),
        ("bc_B cm",          CASE_B["bc"],     52.76,   1e-9),
        ("Ach_B cm2",        CASE_B["ach"],    2783.6,  0.05),
        ("Ash1/s (B)",       CASE_B["a1"],     0.310,   0.001),
        ("s_conf_B cm",      CASE_B["s1"],     16.4,    0.05),
        ("Vc_axial_old tf",  VC_AXIAL_OLD,     31.6,    0.05),
        ("Vc_318_19 tf",     VC_318_19,        36.2,    0.05),
    ]
    print(f"── 與 {TAG}.md §4／§5 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<17} 算得 {got:>12.6g}   .md {want:>9}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"
    assert VC_IS_ZERO, "Vc = 0 條件未成立，圖 3 的剪力列前提改變"

    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<34} 攔：{catches}")


if __name__ == "__main__":
    main()
