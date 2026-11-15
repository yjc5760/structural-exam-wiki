#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2020-2 倒 T 型梁・d 偏移適用性與支承位置箍筋間距 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2020-2.md §1 給定的原始資料；V_c、V_u、V_s、2V_c、4V_c、
     s_strength、s_code、V_u,max 以及「誤判載重位置」的對照值全部現算，
     檔尾對 §4 公佈值 assert。
  2. 改 §1 任一數字重跑，四張圖跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose, esc
from recipes import bar_compare, plot_function

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2020-2"

# ══════════════════════════════════════════════════════════
# §1 原始給定（倒 T 型梁：腹板在上、翼板在下）
# ══════════════════════════════════════════════════════════
FC, FY = 280.0, 4200.0          # kgf/cm^2
WU = 150.0                      # kgf/cm（= 15 tf/m）
L = 800.0                       # cm 跨度
BW, HT = 35.0, 70.0             # 腹板寬、全高（考卷 70 為頂面到底面，題目正本判讀 #2）
BF, HF = 100.0, 20.0            # 翼板寬、翼板深（下方）
COVER = 6.0                     # 上下保護層（至鋼筋重心）
A_D13 = 1.267                   # cm^2 一支 D13
PHI = 0.75                      # 剪力強度折減（108 年規範／土木 401-100）

H = HT                          # 全深 70
HW = H - HF                     # 梁腹高 50（翼版頂面以上）
D = H - COVER                   # 有效深度 64
AV = 2 * A_D13                  # 閉合箍一組兩腳
SQFC = math.sqrt(FC)
TF = 1e-3                       # kgf → tf

# ── 現算 ──────────────────────────────────────────────────
VC = 0.53 * SQFC * BW * D                  # 原卷給定之 V_c 公式
PHI_VC = PHI * VC
VU_SUPPORT = WU * L / 2                    # 支承面（本題臨界斷面）
VU_AT_D = VU_SUPPORT - WU * D              # 若誤判為梁頂載重才可用
TWO_VC, FOUR_VC = 2 * VC, 4 * VC


def design(vu):
    """給定臨界斷面 V_u，回傳整組間距設計結果。"""
    vs = vu / PHI - VC
    s_code = min(D / 4, 30.0) if vs > TWO_VC else min(D / 2, 60.0)
    s_str = AV * FY * D / vs
    return dict(vu=vu, vs=vs, s_code=s_code, s_str=s_str,
                s=min(s_str, s_code), branch=("d/4" if vs > TWO_VC else "d/2"))


RIGHT = design(VU_SUPPORT)      # 正解：不可 d 偏移
WRONG = design(VU_AT_D)         # 陷阱：誤判載重在梁頂
VU_MAX = PHI * (VC + FOUR_VC)   # 斷面最大設計剪力容量

S_PROVIDED = 11.0               # 實配 D13 @ 11 cm
AV_MIN = max(0.2 * SQFC * BW * S_PROVIDED / FY, 3.5 * BW * S_PROVIDED / FY)
A_HANGER = WU / (PHI * FY)      # 懸吊鋼筋需求 cm^2/cm

XW0 = (BF - BW) / 2             # 腹板在斷面座標中的左緣 32.5


def M(s):
    """數學襯線字型（FONT_M）缺中文字，cairosvg 會靜默丟字。
    所有進 math()/math_px() 的字串一律經此守衛。"""
    assert not any(ord(ch) > 0x2E80 for ch in s), f"math 字串不得含中日韓字元：{s}"
    return s


# ══════════════════════════════════════════════════════════
# 圖 1　題目重繪：側視（載重止於下翼板頂面）＋ 倒 T 斷面
# ══════════════════════════════════════════════════════════
def fig_beam():
    PW, PH = 760, 380
    e = Canvas(PW, PH, sx=1)
    mL, mR, mT, mB = 92, 92, 150, 104
    sx = min((PW - mL - mR) / L, (PH - mT - mB) / H)
    e.sx, e.ox, e.oy = sx, mL, mB
    e.panel("側視圖", "載重箭頭終止於下翼板頂面（拉力側）")

    e.polygon([(0, 0), (L, 0), (L, H), (0, H)], "#EDF1F6", C["member"], 2.4)
    e.line((0, HF), (L, HF), C["member2"], 1.6, dash="7 5")

    # 均佈載重：箭頭尖端落在 y = HF（翼板頂面），不是 y = H
    e.udl((0, HF), (L, HF), 34.0, n=11, w=1.9)
    e.math_px(e.X(L / 2), e.Y(H) - 14, "w_{u} = 15 tf/m", 15.5,
              C["load"], weight="700")
    e.support((0, 0), "pin"); e.support((L, 0), "roller")

    # 臨界斷面：支承面（正解）與 d 處（誤用）
    e.line((0, 0), (0, H + 16), C["load"], 2.6)
    e.text_px(e.X(0) - 4, e.Y(H) - 44, "臨界斷面", 12.5, C["load"], "start",
              weight="700")
    e.text_px(e.X(0) - 4, e.Y(H) - 28, "＝支承面", 12.5, C["load"], "start",
              weight="700")
    e.line((D, 0), (D, H + 16), C["muted"], 1.8, dash="6 4")
    e.text_px(e.X(D) + 8, e.Y(H) - 36, f"d = {D:g} cm", 12, C["muted"], "start")
    e.text_px(e.X(D) + 8, e.Y(H) - 20, "（本題不可偏移）", 12, C["muted"], "start")

    e.dim((0, 0), (L, 0), f"L = {L:g} cm", off=58, label_off=17)
    e.dim((L, 0), (L, H), f"h = {H:g}", off=42, label_off=26)
    e.text_px(e.X(L * 0.60), e.Y(HF / 2), "下翼板（拉力側）", 12.5, C["muted"])
    return e


def fig_beam_section():
    PW, PH = 760, 380
    s = Canvas(PW, PH, sx=1)
    mL, mR, mT, mB = 268, 244, 122, 86
    sx = min((PW - mL - mR) / BF, (PH - mT - mB) / H)
    s.sx, s.ox, s.oy = sx, mL, mB
    s.panel("斷面（倒 T）", "腹板在上、翼板在下")

    s.polygon([(XW0, HF), (XW0, H), (XW0 + BW, H), (XW0 + BW, HF),
               (BF, HF), (BF, 0), (0, 0), (0, HF)],
              "#EDF1F6", C["member"], 2.6)

    # D13 閉合箍筋（腹板內，示意）
    s.polygon([(XW0 + 4, HF + 4), (XW0 + BW - 4, HF + 4),
               (XW0 + BW - 4, H - 4), (XW0 + 4, H - 4)],
              "none", C["load"], 2.0)
    for i in range(3):
        s.dot((XW0 + BW * (0.22 + 0.28 * i), COVER), 5.0,
              fill=C["tension"], stroke="#FFFFFF", w=1.3)
    for i in range(2):
        s.dot((XW0 + BW * (0.30 + 0.40 * i), H - COVER), 5.0,
              fill=C["compr"], stroke="#FFFFFF", w=1.3)

    s.dim((XW0, H), (XW0 + BW, H), f"b_{{w}} = {BW:g}", off=-30, label_off=-12)
    s.dim((0, 0), (BF, 0), f"{BF:g}", off=44, label_off=16)
    s.dim((BF, 0), (BF, HF), f"{HF:g}", off=34, label_off=13)
    s.dim((0, H), (0, 0), f"h = {H:g}", off=118, label_off=15)
    s.dim((0, H), (0, COVER), f"d = {D:g}", off=36, label_off=15)
    s.text_px(s.X(BF) + 66, s.Y(H * 0.72),
              f"A_{{v}} = 2×{A_D13:g} = {AV:g} cm^{{2}}", 12.5, C["load"], "start",
              weight="700")
    s.text_px(s.X(BF) + 66, s.Y(H * 0.72) + 19,
              "D13 閉合箍（一組兩腳）", 12, C["muted"], "start")
    s.text_px(s.X(BF) + 66, s.Y(H * 0.72) + 38,
              "紅＝拉力筋　藍＝壓力筋", 12, C["muted"], "start")
    return s


def fig1():
    return compose([fig_beam(), fig_beam_section()],
                   title=f"圖 1　{TAG} 題目重繪：獨立倒 T 型梁（腹板在上、載重壓在下翼板）",
                   sub=f"f'c = {FC:g} kgf/cm²　f_y = {FY:g} kgf/cm²　"
                       f"跨度 {L:g} cm　h = {H:g} cm　d = {D:g} cm",
                   note="載重自下翼板（拉力側）進入 → 屬懸吊式載重，"
                        "d 偏移三條件之 (b) 不成立",
                   cols=2)


# ══════════════════════════════════════════════════════════
# 圖 2　力流對照：梁頂載重（可偏移）vs 下翼板載重（不可偏移）
# ══════════════════════════════════════════════════════════
XEND = 240.0        # 只畫端區
PW2, PH2 = 500, 350


def _panel(title, sub):
    cv = Canvas(PW2, PH2, sx=1)
    mL, mR, mT, mB = 58, 58, 120, 128
    sx = min((PW2 - mL - mR) / XEND, (PH2 - mT - mB) / H)
    cv.sx, cv.ox, cv.oy = sx, mL, mB
    cv.panel(title, sub)
    cv.polygon([(0, 0), (XEND, 0), (XEND, H), (0, H)], "#EDF1F6", C["member"], 2.2)
    cv.line((0, HF), (XEND, HF), C["member2"], 1.4, dash="7 5")
    cv.support((0, 0), "pin", size=13)
    return cv


def _below(cv, x, crit, vu, why):
    """臨界斷面標線與線下兩行說明。"""
    cv.line((x, -16), (x, H + 8), C["load"], 2.6)
    anchor = "start" if x < XEND * 0.15 else "middle"
    cv.text_px(cv.X(x) + (6 if anchor == "start" else 0), cv.Y(0) + 46, crit,
               12.5, C["load"], anchor, weight="700")
    cv.math_px(cv.X(XEND / 2), cv.Y(0) + 74, M(f"V_{{u}} = {vu * TF:.1f} tf"), 15.5,
               C["load"], weight="700")
    cv.text_px(cv.X(XEND / 2), cv.Y(0) + 96, why, 12.5, C["muted"])


def fig2():
    # ---- (a) 載重在腹板頂面 → 直接斜壓撐 → 可 d 偏移 ----
    a = _panel("(a) 載重在腹板頂面", "壓力側進入 → 形成直接斜壓撐")
    a.udl((0, H), (XEND, H), 17.0, n=7, w=1.8)
    a.math_px(a.X(XEND * 0.5) - 34, a.Y(H + 17.0) - 12, M("w_{u}"), 14,
              C["load"], weight="700")
    a.text_px(a.X(XEND * 0.5) - 22, a.Y(H + 17.0) - 12, "（施於梁頂）", 12.5,
              C["load"], "start", weight="700")
    for xt in (D * 0.5, D, D * 1.5):
        a.line((xt, H), (0, 0), C["compr"], 4.6, cap="butt", op=0.55)
    a.text_px(a.X(XEND * 0.70), a.Y(H * 0.62), "斜壓撐直達支承", 12.5,
              C["compr"], weight="700")
    a.text_px(a.X(XEND * 0.70), a.Y(H * 0.62) + 19, "端區不必靠腹筋跨越", 12,
              C["muted"])
    _below(a, D, f"臨界斷面 x = d = {D:g} cm", VU_AT_D, "端區剪力可折減 w_u·d")

    # ---- (b) 載重在下翼板 → 懸吊 → 不可偏移 ----
    b = _panel("(b) 載重在下翼板（本題）", "拉力側進入 → 須先被懸吊筋吊上壓力區")
    b.udl((0, HF), (XEND, HF), 14.0, n=7, w=1.8)
    b.math_px(b.X(XEND * 0.62) - 46, b.Y(HF * 0.42), M("w_{u}"), 13.5,
              C["load"], weight="700")
    b.text_px(b.X(XEND * 0.62) - 34, b.Y(HF * 0.42), "壓在下翼板頂面", 12.5,
              C["load"], "start", weight="700")
    for xt in (D * 0.5, D * 0.95):
        b.arrow((xt, HF + 2), (xt, H - 5), C["accent"], 3.0, 9)
        b.line((xt, H - 5), (0, HF), C["compr"], 4.4, cap="butt", op=0.5)
    b.text_px(b.X(XEND * 0.68), b.Y(H * 0.90), "① 懸吊筋吊上壓力區", 12.5,
              C["accent"], weight="700")
    b.text_px(b.X(XEND * 0.68), b.Y(H * 0.90) + 19, "② 之後才形成斜壓撐", 12.5,
              C["compr"], weight="700")
    _below(b, 0.0, "臨界斷面 x = 0（支承面）", VU_SUPPORT,
           "斜裂縫穿越整個端區，剪力不得折減")

    return compose([a, b],
                   title="圖 2　d 偏移的物理基礎：載重從哪一側進入，決定端區能不能折減",
                   sub="規範條件 (b)「載重施加於構材頂部或其附近」——判準是條件，不是構件名稱",
                   note=f"兩者臨界斷面剪力相差 {VU_SUPPORT / VU_AT_D - 1:.1%}"
                        f"（{VU_SUPPORT * TF:.1f} 對 {VU_AT_D * TF:.1f} tf）",
                   cols=2)


# ══════════════════════════════════════════════════════════
# 圖 3　剪力包絡線與三條門檻
# ══════════════════════════════════════════════════════════
def fig3():
    W, HH = 800, 430
    HALF = L / 2
    n = 81
    xs = [HALF * i / (n - 1) for i in range(n)]
    vu = [(VU_SUPPORT - WU * x) * TF for x in xs]

    mL, mR, mT, mB = 86, 214, 104, 78
    ytop = VU_MAX * TF * 1.10
    sc_x = (W - mL - mR) / HALF
    sc_y = (HH - mT - mB) / ytop
    cv = Canvas(W, HH, sx=sc_x, ox=mL, oy=mB, bg="#FFFFFF")
    k = sc_y / sc_x                      # 縱軸相對縮放（tf → 模型單位）

    cv.text_px(W / 2, 34, "圖 3　剪力需求包絡線與三條規範門檻", 17.0, C["text"],
               weight="700")
    cv.text_px(W / 2, 58, "橫軸：距支承面距離（cm，半跨）　縱軸：剪力（tf）", 12.5,
               C["muted"])

    # 座標軸
    cv.arrow((0, 0), (HALF * 1.04, 0), C["muted"], 1.6, 9)
    cv.arrow((0, 0), (0, ytop * k), C["muted"], 1.6, 9)

    # V_u(x)
    cv.polygon([(0, 0)] + [(x, v * k) for x, v in zip(xs, vu)] + [(HALF, 0)],
               C["fill_s"], C["sfd"], 2.6)

    # 三條水平門檻
    for val, col, lab in (
            (VU_MAX * TF, C["accent"],
             f"V_{{u,max}} = 5φV_{{c}} = {VU_MAX * TF:.1f} tf"),
            (PHI * (VC + RIGHT["vs"]) * TF, C["bmd"],
             f"φ(V_{{c}}+V_{{s}}) = {PHI * (VC + RIGHT['vs']) * TF:.1f} tf"),
            (PHI_VC * TF, C["compr"], f"φV_{{c}} = {PHI_VC * TF:.1f} tf")):
        cv.line((0, val * k), (HALF, val * k), col, 1.8, dash="7 5")
        cv.math_px(cv.X(HALF) + 12, cv.Y(val * k), M(lab), 13, col, "start",
                   weight="700")

    # 兩個工作點
    cv.dot((0, VU_SUPPORT * TF * k), 6.0, fill=C["load"], stroke="#FFFFFF", w=1.8)
    cv.math_px(cv.X(0) + 12, cv.Y(VU_SUPPORT * TF * k) - 30,
               M(f"V_{{u}} = {VU_SUPPORT * TF:.1f} tf"), 14.5,
               C["load"], "start", weight="700")
    cv.text_px(cv.X(0) + 12, cv.Y(VU_SUPPORT * TF * k) - 12, "支承面（本題採用）",
               12.5, C["load"], "start", weight="700")
    cv.dot((D, VU_AT_D * TF * k), 5.4, fill=C["muted"], stroke="#FFFFFF", w=1.8)
    cv.math_px(cv.X(D) + 14, cv.Y(VU_AT_D * TF * k) + 72,
               M(f"{VU_AT_D * TF:.1f} tf @ x = d"), 12.5, C["muted"], "start")
    cv.text_px(cv.X(D) + 14, cv.Y(VU_AT_D * TF * k) + 90, "（本題不適用）", 12,
               C["muted"], "start")
    cv.line((D, 0), (D, VU_AT_D * TF * k), C["muted"], 1.4, dash="4 3")

    # 軸標
    for xv in (0, D, 200, 300, 400):
        cv.line((xv, 0), (xv, -ytop * k * 0.018), C["muted"], 1.4)
        cv.text_px(cv.X(xv), cv.Y(0) + 20, f"{xv:g}", 12, C["muted"])
    for yv in [v for v in (0, 20, 40, 60, 80, 100) if v <= ytop]:
        cv.text_px(cv.X(0) - 12, cv.Y(yv * k), f"{yv:g}", 12, C["muted"], "end")

    cv.text_px(W / 2, HH - 22,
               f"支承面 {VU_SUPPORT * TF:.1f} tf ＜ V_u,max {VU_MAX * TF:.1f} tf → "
               f"斷面尺寸足夠（餘裕 {VU_MAX / VU_SUPPORT - 1:.0%}），"
               f"但 V_s = {RIGHT['vs'] * TF:.2f} tf 已超過 2V_c = {TWO_VC * TF:.2f} tf",
               13, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 4　間距上限：四個候選值與控制值
# ══════════════════════════════════════════════════════════
def fig4():
    """bar_compare 左欄僅約 170 px，名稱與說明務必精簡；理由寫在 note。"""
    cases = [
        ("誤用 d/2 上限", "本題不適用", min(D / 2, 60.0),
         M(f"min(d/2, 60) = {min(D / 2, 60.0):.1f} cm"), C["ghost"]),
        ("誤判載重在梁頂", f"偏寬 {WRONG['s_str'] / RIGHT['s'] - 1:.0%}，不安全",
         WRONG["s_str"], M(f"s = {WRONG['s_str']:.2f} cm"), C["muted"]),
        ("規範上限 d/4", "V_s ＞ 2V_c 分支", RIGHT["s_code"],
         M(f"min(d/4, 30) = {RIGHT['s_code']:.1f} cm"), C["accent"]),
        ("強度需求 ← 控制", f"實配 D13 @ {S_PROVIDED:g} cm", RIGHT["s_str"],
         M(f"s = {RIGHT['s_str']:.2f} cm"), C["load"]),
    ]
    return bar_compare(
        cases,
        title="圖 4　支承位置箍筋間距：四個候選值同時攤開",
        sub="長條越長＝間距越大＝越不安全；控制值取「強度需求」與「規範上限」之最小者",
        note=f"V_s = {RIGHT['vs'] * TF:.2f} tf 超過 2V_c = {TWO_VC * TF:.2f} tf "
             f"（{RIGHT['vs'] / TWO_VC - 1:.0%}），規範上限由 "
             f"{min(D / 2, 60.0):.0f} cm 減為 {RIGHT['s_code']:.0f} cm；"
             f"最終仍由強度需求 {RIGHT['s_str']:.2f} cm 控制").svg()


# ══════════════════════════════════════════════════════════
FIGURES = [
    ("1-beam", fig1,
     "把載重箭頭誤讀成梁頂均佈載重（本題全部得分的樞紐）"),
    ("2-loadpath", fig2,
     "反射性套 d 偏移；說不出「為什麼拉力側進入就不能折減」"),
    ("3-shear", fig3,
     "忘記 V_s,max = 4V_c 也是斷面容量的天花板；把 φV_c 當成 V_u 上限"),
    ("4-spacing", fig4,
     "間距上限選錯分支（d/2 vs d/4）；忘記與強度需求取小"),
]


# ══════════════════════════════════════════════════════════
# 題目附圖重繪（2026-11-15，RC-U2-1／U2-2 題目正本推廣・批 1）
# 依據：題目正本 <id>-problem.md §4 判讀清單（已確認）。只畫考卷給的東西，不含解題結果；
# 考卷未標尺寸的位置畫成示意，並在副標寫明。
# ══════════════════════════════════════════════════════════
def _pc(Wm, Hm, maxpx=330, l=150, r=170, t=40, b=90):
    s = maxpx / max(Wm, Hm)
    return Canvas(int(Wm * s + l + r), int(Hm * s + t + b), sx=s, ox=l, oy=b)


def _prect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _pbar(cv, p, r=1.25, fill=None):
    cv.circle(p, r, fill=fill or C["member"], stroke=C["member"], w=1.2)


def _phoop(cv, x0, y0, x1, y1, w=3.0, color=None):
    """閉合箍筋（以箍筋中心線畫）"""
    cv.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], color or C["member"], w)


def _phook(cv, p, ang_deg, L=3.0, w=3.0):
    """箍筋彎鉤：由 p 往 ang 方向畫一段（135° 彎鉤用 -45° 指向斷面內）"""
    import math
    a = math.radians(ang_deg)
    cv.line(p, (p[0] + L * math.cos(a), p[1] + L * math.sin(a)), C["member"], w)


P_L = 800.0               # 判讀 #7 支承中心距
P_EXT = 10.0              # 梁端伸出支承中心線（考卷未標，示意）
P_H = 70.0                # 判讀 #2 全高
P_BF, P_TF = 100.0, 20.0  # 判讀 #4 下翼版寬、厚
P_BW = 35.0               # 判讀 #4 梁腹寬
P_CT, P_CB = 6.0, 6.0     # 判讀 #3 頂面至上排筋心、下排筋心至底面


def fig1_problem():
    PW, PH = 760, 300
    # 立面（水平、垂直同比例）
    s1 = (PW - 160) / (P_L + 2 * P_EXT)
    e = Canvas(PW, PH, sx=s1, ox=80 + P_EXT * s1, oy=120)
    _prect(e, -P_EXT, 0, P_L + P_EXT, P_H, fill="#FFFFFF")
    e.line((-P_EXT, P_TF), (P_L + P_EXT, P_TF), C["member"], 1.6)
    e.udl((0, P_TF), (P_L, P_TF), 38, n=21, color=C["load"], w=1.6)
    e.math_px(e.X(P_L / 2), e.Y(P_H) - 22, "w_{u} = 15 tf/m", 16, C["load"], weight="700")
    e.support((0, 0), "pin"); e.support((P_L, 0), "roller")
    for x in (0, P_L):
        e.line((x, -40), (x, P_H + 30), C["muted"], 1.0, dash="6 4")
    e.dim((0, -40), (P_L, -40), f"{P_L:.0f}", off=30, label_off=16)
    e.text_px(PW / 2, PH - 12, "立面：載重作用在下翼版頂面（距底面 20）", 13, C["muted"])
    # 斷面
    s2 = 2.6
    c = Canvas(PW, PH, sx=s2, ox=(PW - P_BF * s2) / 2, oy=60)
    xw0 = (P_BF - P_BW) / 2
    pts = [(0, 0), (P_BF, 0), (P_BF, P_TF), (xw0 + P_BW, P_TF), (xw0 + P_BW, P_H),
           (xw0, P_H), (xw0, P_TF), (0, P_TF), (0, 0)]
    c.polygon(pts, "#EDF1F6"); c.poly(pts, C["member"], 2.4)
    _phoop(c, xw0 + 4, 4, xw0 + P_BW - 4, P_H - 4)
    _phook(c, (xw0 + 4, P_H - 4), -45, 3.0); _phook(c, (xw0 + P_BW - 4, P_H - 4), -135, 3.0)
    for x in (8, 18, xw0 + 6, P_BF / 2, xw0 + P_BW - 6, P_BF - 18, P_BF - 8):   # 位置考卷未標（示意）
        _pbar(c, (x, P_CB), 1.3)
    for x in (xw0 + 6, xw0 + P_BW - 6):
        _pbar(c, (x, P_H - P_CT), 1.3)
    c.text((xw0 + P_BW + 6, P_H - 22), "D13", 13, anchor="start")
    c.dim((xw0, P_H), (xw0 + P_BW, P_H), f"{P_BW:.0f}", off=-26, label_off=-14)
    c.dim((0, 0), (P_BF, 0), f"{P_BF:.0f}", off=30, label_off=16)
    c.dim((0, P_TF), (0, 0), f"{P_TF:.0f}", off=30, label_off=18)
    c.dim((P_BF, 0), (P_BF, P_H), f"{P_H:.0f}", off=56, label_off=20)
    c.dim((xw0 + P_BW, P_H - P_CT), (xw0 + P_BW, P_H), f"{P_CT:.0f}", off=28, label_off=14)
    c.dim((P_BF, 0), (P_BF, P_CB), f"{P_CB:.0f}", off=28, label_off=14)
    return compose([e, c], cols=1, title=f"{TAG} 題目附圖重繪（單位 cm）",
                   sub="依題目正本判讀清單 #1–#7；梁端伸出長度、鋼筋號數與位置考卷未標（示意）",
                   note="70 為全高（頂面到底面）；d = 70 − 6 = 64 cm")


FIGURES_PROBLEM = ("1-problem", fig1_problem, "把 70 讀成梁腹高（全高 90、d = 84）；把載重當成作用在梁頂")
FIGURES.insert(0, FIGURES_PROBLEM)


def main():
    os.makedirs(OUT, exist_ok=True)
    checks = [
        ("V_c kgf",        VC,                 19866,  3),
        ("φV_c tf",        PHI_VC * TF,        14.90,  0.05),
        ("V_u 支承 tf",     VU_SUPPORT * TF,    60.0,   0.01),
        ("V_s tf",         RIGHT["vs"] * TF,   60.13,  0.01),
        ("2V_c tf",        TWO_VC * TF,        39.73,  0.01),
        ("4V_c tf",        FOUR_VC * TF,       79.46,  0.02),
        ("s_code cm",      RIGHT["s_code"],    16.0,   0.01),
        ("s_strength cm",  RIGHT["s_str"],     11.33,  0.01),
        ("V_u,max tf",     VU_MAX * TF,        74.50,  0.02),
        ("誤判 V_u,d tf",   VU_AT_D * TF,       50.4,   0.01),
        ("誤判 V_s tf",     WRONG["vs"] * TF,   47.33,  0.01),
        ("誤判 s cm",       WRONG["s_str"],     14.39,  0.01),
        ("A_v,min cm2",    AV_MIN,             0.321,  0.001),
        ("A_h cm2/cm",     A_HANGER,           0.0476, 0.0001),
    ]
    print(f"── 與 {TAG}.md §4 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<14} 算得 {got:>13.6g}   .md {want:>10}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"
    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<34} 攔：{catches}")


if __name__ == "__main__":
    main()
