#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2016-1 兩端固定梁・雙曲度地震彎矩組合 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2016-1.md §1 給定的原始資料；固端／跨中彎矩、四種組合、
     A_s、M_n 一律由下方函式現算，檔尾對 §4 公佈值 assert。
  2. 改 §1 任一數字（L、w_D、w_L、M_E、b、d）重跑，三張圖全部跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

FIGURES
  fig-1-bmd        三種組合的彎矩圖   攔：漏算「地震反向那一端翻號成正彎矩」
  fig-2-envelope   控制彎矩彙整       攔：組合表少一格就不知道底筋由誰控制
  fig-3-ratio      Mn 比 vs 面積比    攔：耐震底筋規定拿面積比當結論
"""
import sys, os, math

sys.path.insert(0, os.environ.get(
    "STRUCTDRAW_DIR", "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose                       # noqa: E402
from recipes import bar_compare                                  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2016-1"

# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
B      = 35.0      # 梁寬 cm
HH     = 70.0      # 梁深 cm
D      = 63.0      # 有效深度 cm
L      = 7.5       # 淨跨度 m
WD     = 2.0       # tf/m
WL     = 1.0       # tf/m
ME     = 16.5      # tf·m（兩端等值，雙曲度）
FC     = 280.0
FY     = 4200.0
ES     = 2.04e6
EPS_CU = 0.003
PHI    = 0.90
AB_D22 = 3.87      # cm^2
AB_D29 = 6.47      # cm^2
DB_D22 = 2.22      # cm
COVER  = 4.0
D_STIR = 1.0

B1   = 0.85 if FC <= 280 else max(0.65, 0.85 - 0.05 * (FC - 280) / 70)
EPSY = FY / ES
KA   = FY / (0.85 * FC * B)                       # a = KA · As

RHO_B  = 0.85 * B1 * FC / FY * 6120 / (6120 + FY)
C_MAX  = 3 / 7 * D                                # εt = 0.004
A_MAX  = B1 * C_MAX
AS_MAX = 0.85 * FC * A_MAX * B / FY
RHO_MAX = AS_MAX / (B * D)
RHO_MIN = max(14 / FY, 0.8 * math.sqrt(FC) / FY)
AS_MIN  = RHO_MIN * B * D
# 舊制對照
RHO_MAX_OLD = 0.75 * RHO_B
AS_MAX_OLD  = RHO_MAX_OLD * B * D
C_OLD  = (AS_MAX_OLD * KA) / B1
ET_OLD = EPS_CU * (D - C_OLD) / C_OLD

# ── 彈性分析彎矩（服務載重）；正 = 底部受拉 ────────────────
def M_grav(w, x):
    return -w * L**2 / 12 + w * L * x / 2 - w * x**2 / 2


def M_eq(x):
    """雙曲度：一端 +ME、另一端 −ME，沿跨度線性。"""
    return ME - 2 * ME * x / L


COMBOS = [
    ("組合一　1.2D + 1.6L", 1.2 * WD + 1.6 * WL, 0.0, C["muted"]),
    ("組合二　1.2D + 1.0L + 1.0E", 1.2 * WD + 1.0 * WL, 1.0, C["bmd"]),
    ("組合三　0.9D + 1.0E", 0.9 * WD, 1.0, C["accent"]),
]


def M_of(w, kE, x):
    return M_grav(w, x) + kE * M_eq(x)


# ── 控制彎矩 ─────────────────────────────────────────────
END_NEG = max(abs(min(M_of(w, k, x) for x in (0.0, L)))
              for _, w, k, _ in COMBOS)
END_POS = max(max(M_of(w, k, x) for x in (0.0, L)) for _, w, k, _ in COMBOS)
MID_POS = max(M_of(w, k, L / 2) for _, w, k, _ in COMBOS)
MU_TOP = END_NEG
MU_BOT = max(END_POS, MID_POS)


def As_for(Mu_tfm):
    """由 φ·As·fy(d − a/2) = Mu 解 As（取合理小根）。"""
    qa = -PHI * FY * KA / 2
    qb = PHI * FY * D
    qc = -Mu_tfm * 1e5
    return (-qb + math.sqrt(qb * qb - 4 * qa * qc)) / (2 * qa)


AS_TOP_REQ = As_for(MU_TOP)
AS_MID_REQ = As_for(MID_POS)
AS_BOT_REQ = max(AS_MID_REQ, AS_MIN)

N_TOP, N_BOT = 4, 2                               # §4 Step 7 選配 4-D22 / 2-D22
AS_TOP = N_TOP * AB_D22
AS_BOT = N_BOT * AB_D22


def Mn_of(As):
    a = KA * As
    return As * FY * (D - a / 2) / 1e5, a          # tf·m


MN_TOP, A_TOP = Mn_of(AS_TOP)
MN_BOT, A_BOT = Mn_of(AS_BOT)
RATIO_MN = MN_BOT / MN_TOP
RATIO_AS = AS_BOT / AS_TOP
S_CLEAR = (B - 2 * (COVER + D_STIR) - N_TOP * DB_D22) / (N_TOP - 1)

# ══════════════════════════════════════════════════════════
# 圖 1　三種組合的彎矩圖（含梁端翻號）
# ══════════════════════════════════════════════════════════
PW, PH = 400, 480
XS = [L * i / 120 for i in range(121)]
MMAX = 34.0                                        # 彎矩繪圖上限 tf·m
sx = (PW - 96) / L
msc = ((PH - 250) / 2) / MMAX / sx                 # 1 tf·m 對應的模型長度


def fmt_m(v):
    """與 .md 逐位相同：能用兩位小數就用兩位，否則若三位可整除則用三位。"""
    if abs(v * 100 - round(v * 100)) < 1e-9:
        return f"{v:+.2f}"
    if abs(v * 1000 - round(v * 1000)) < 1e-9:
        return f"{v:+.3f}".rstrip("0").rstrip(".")
    return f"{v:+.2f}"


def bmd_panel(name, w, kE, col):
    cv = Canvas(PW, PH, sx=sx, ox=48, oy=PH * 0.46)
    cv.panel(name, None)
    vals = [M_of(w, kE, x) for x in XS]
    # 彎矩畫在受拉側：正彎矩（底部受拉）畫在梁線下方
    pts = [(x, -v * msc) for x, v in zip(XS, vals)]
    cv.polygon([(0, 0)] + pts + [(L, 0)], C["fill_m"], col, 2.6)
    cv.line((0, 0), (L, 0), C["member"], 5, cap="butt")
    cv.support((0, 0), "fixed", 90, 18)
    cv.support((L, 0), "fixed", -90, 18)
    for x, tag in ((0.0, "左端"), (L, "右端"), (L / 2, "跨中")):
        v = M_of(w, kE, x)
        dy = 16 if v > 0 else -16
        cv.dot((x, -v * msc), 4.8, fill=col, stroke="#FFFFFF", w=1.6)
        cv.math_px(cv.X(x) + (30 if x == 0 else (-30 if x == L else 0)),
                   cv.Y(-v * msc) + dy, fmt_m(v), 13, col,
                   "start" if x == 0 else ("end" if x == L else "middle"), weight="700")
    cv.text_px(PW / 2, PH - 92, "（正 = 底部受拉，畫在梁線下方）", 11.5, C["muted"])
    cv.text_px(PW / 2, PH - 66,
               f"w = {w:.1f} tf/m" + ("　＋　雙曲度 M_E = ±16.5" if kE else ""),
               12, C["muted"])
    flip = [x for x in (0.0, L) if M_of(w, kE, x) > 0]
    if flip:
        cv.text_px(PW / 2, PH - 40, "梁端翻號成正彎矩（底部受拉）", 12.5, C["load"],
                   weight="700")
    return cv


compose([bmd_panel(n, w, k, c) for n, w, k, c in COMBOS], cols=3,
        title=f"{TAG}　雙曲度地震彎矩讓「一端」翻號，不是兩端一起加大",
        sub=("M_E 在兩端方向相反（一端 +、一端 −）；與重力固端負彎矩同向的那端疊加變大，"
             "反向的那端相減"),
        note=(f"因 M_E = {ME:.1f} 大於 0.9M_D,end = {0.9*WD*L**2/12:.2f} tf·m，"
              f"組合三的左端合成後翻號成 +{M_of(0.9*WD, 1.0, 0.0):.2f} tf·m —— "
              f"組合表若沒有「固端正彎矩」這一格，根本不會發現"),
        path=f"{OUT}/{TAG}-fig-1-bmd.svg")

# ══════════════════════════════════════════════════════════
# 圖 2　控制彎矩彙整
# ══════════════════════════════════════════════════════════
rows = [
    ("固端負彎矩（頂部受拉）", "組合二　← 控制頂筋", MU_TOP,
     f"{MU_TOP:.2f} tf·m", C["load"]),
    ("固端負彎矩（純重力）", "組合一　對照用", abs(M_of(1.2 * WD + 1.6 * WL, 0, 0.0)),
     f"{abs(M_of(1.2*WD+1.6*WL,0,0.0)):.2f} tf·m", C["muted"]),
    ("跨中正彎矩（底部受拉）", "組合一　← 控制底筋", MID_POS,
     f"{MID_POS:.3f} tf·m", C["bmd"]),
    ("梁端正彎矩（底部受拉）", "組合三　地震反向端", END_POS,
     f"{END_POS:.2f} tf·m", C["accent"]),
]
bar_compare(rows,
            title=f"{TAG}　四個控制點都要算過，才知道誰不控制",
            sub=("組合一 1.2D+1.6L　　組合二 1.2D+1.0L+1.0E　　組合三 0.9D+1.0E　　"
                 f"梁端正彎矩 {END_POS:.2f} 小於跨中 {MID_POS:.3f} tf·m，故不控制底筋"),
            note=("「算過才知道不控制」與「沒算」在卷面上是兩件事；"
                  "只要 M_E 再大一些或跨度再短一些，底筋就會改由梁端控制"),
            path=f"{OUT}/{TAG}-fig-2-envelope.svg")

# ══════════════════════════════════════════════════════════
# 圖 3　耐震底筋規定：彎矩強度比 vs 面積比
# ══════════════════════════════════════════════════════════
W3, H3 = 1020, 412
cv = Canvas(W3, H3, sx=1, bg="#FFFFFF")
cv.text_px(W3 / 2, 34, f"{TAG}　梁端底筋規定比的是「彎矩強度」，面積比只是快篩",
           17.5, C["text"], weight="700")
cv.text_px(W3 / 2, 60, f"頂筋 {N_TOP}-D22（A_s = {AS_TOP:.2f} cm²）　"
                       f"底筋 {N_BOT}-D22（A_s = {AS_BOT:.2f} cm²）", 13, C["muted"])

X0, BAR_W, TOP = 520, 360, 128
ROW_H = 92
LIMIT = 0.50
FULL = 0.62                                        # 長條滿刻度


def ratio_row(i, name, desc, val, col):
    y = TOP + i * ROW_H
    cv.text_px(150, y - 10, name, 14, C["text"], "start", weight="700")
    cv.text_px(150, y + 14, desc, 12, C["muted"], "start")
    cv.rect_px(X0, y - 18, BAR_W, 36, "#EDF1F6", 8)
    cv.rect_px(X0, y - 18, BAR_W * val / FULL, 36, col, 8)
    cv.text_px(X0 + BAR_W * val / FULL - 14, y, f"{val:.3f}", 14, "#FFFFFF", "end",
               weight="700")


ratio_row(0, "鋼筋面積比", f"A_s,bot / A_s,top = {AS_BOT:.2f} / {AS_TOP:.2f}",
          RATIO_AS, C["muted"])
ratio_row(1, "彎矩強度比（規範真正要求的）",
          f"M_n,bot / M_n,top = {MN_BOT:.2f} / {MN_TOP:.2f} tf·m", RATIO_MN, C["bmd"])

# 0.50 門檻線
xl = X0 + BAR_W * LIMIT / FULL
cv.parts.append(f'<line x1="{xl}" y1="{TOP-40}" x2="{xl}" y2="{TOP+ROW_H+40}" '
                f'stroke="{C["load"]}" stroke-width="2.4" stroke-dasharray="7 5"/>')
cv.text_px(xl, TOP - 54, "規範下限 0.50", 13, C["load"], weight="700")

cv.text_px(W3 / 2, TOP + ROW_H + 74,
           f"面積比 {RATIO_AS:.3f}  小於  彎矩強度比 {RATIO_MN:.3f}", 15, C["text"],
           weight="700")
cv.text_px(W3 / 2, TOP + ROW_H + 102,
           f"因為 M_n = A_s·f_y(d − a/2)，A_s 小的那一根力臂反而長"
           f"（底筋 d − a/2 = {D - A_BOT/2:.2f} cm  對  頂筋 {D - A_TOP/2:.2f} cm）",
           12.5, C["muted"])
cv.text_px(W3 / 2, TOP + ROW_H + 132,
           "→ 只要底筋量少於頂筋量，面積比就恆「不大於」彎矩強度比 —— 偏保守，不會誤放行",
           13, C["bmd"], weight="700")
cv.text_px(W3 / 2, TOP + ROW_H + 160,
           f"本題兩者都過關：{RATIO_AS:.3f} 與 {RATIO_MN:.3f} 均不小於 0.50 ✓"
           f"（彎矩強度比餘裕 {100*(RATIO_MN-LIMIT)/LIMIT:.0f}%）",
           13, C["muted"])
cv.save(f"{OUT}/{TAG}-fig-3-ratio.svg")

# ══════════════════════════════════════════════════════════
# 對 .md §4 公佈值 assert（含本次修正後的 §4 Step 8）
# ══════════════════════════════════════════════════════════
assert abs(abs(M_grav(WD, 0.0)) - 9.375) < 1e-9
assert abs(M_grav(WD, L / 2) - 4.688) < 0.001
assert abs(abs(M_of(1.2 * WD + 1.6 * WL, 0, 0.0)) - 18.75) < 1e-9
assert abs(M_of(1.2 * WD + 1.6 * WL, 0, L / 2) - 9.375) < 1e-9
assert abs(MU_TOP - 32.44) < 0.01,           MU_TOP
assert abs(abs(M_of(0.9 * WD, 1.0, L)) - 24.94) < 0.01
assert abs(END_POS - 8.06) < 0.01,           END_POS
assert abs(M_of(1.2 * WD + 1.0 * WL, 1.0, 0.0) - 0.56) < 0.01
assert abs(MID_POS - 9.375) < 1e-9,          MID_POS
assert abs(RHO_B - 0.02856) < 5e-5,          RHO_B          # ← 修正後（原 .md 誤植 0.02849）
assert abs(AS_MAX - 45.52) < 0.02,           AS_MAX
assert abs(RHO_MAX - 0.02064) < 5e-5,        RHO_MAX
assert abs(AS_MAX_OLD - 47.24) < 0.05,       AS_MAX_OLD     # ← 修正後（原 .md 誤植 47.11）
assert abs(ET_OLD - 0.003745) < 5e-6,        ET_OLD
assert abs(RHO_MIN - 0.003333) < 5e-6,       RHO_MIN
assert abs(AS_MIN - 7.35) < 0.01,            AS_MIN
assert abs(AS_TOP_REQ - 14.46) < 0.01,       AS_TOP_REQ
assert abs(AS_MID_REQ - 4.00) < 0.01,        AS_MID_REQ
assert abs(AS_TOP - 15.48) < 1e-9,           AS_TOP
assert abs(AS_BOT - 7.74) < 1e-9,            AS_BOT
assert abs(A_TOP - 7.805) < 0.005,           A_TOP
assert abs(A_BOT - 3.903) < 0.005,           A_BOT
assert abs(MN_TOP - 38.41) < 0.02,           MN_TOP
assert abs(MN_BOT - 19.84) < 0.02,           MN_BOT
assert abs(RATIO_MN - 0.517) < 0.001,        RATIO_MN
assert abs(RATIO_AS - 0.500) < 0.001,        RATIO_AS       # ← 修正後（原 .md 誤植 0.535）
assert RATIO_AS <= RATIO_MN,                 (RATIO_AS, RATIO_MN)
assert abs(S_CLEAR - 5.37) < 0.01,           S_CLEAR
print(f"{TAG}: 3 圖 OK　固端負 {MU_TOP:.2f}／梁端正 {END_POS:.2f}／跨中正 {MID_POS:.3f}　"
      f"As,top需求 {AS_TOP_REQ:.2f}→4-D22 {AS_TOP:.2f}　As,bot {AS_BOT:.2f}　"
      f"Mn 比 {RATIO_MN:.3f} 大於 面積比 {RATIO_AS:.3f}　ρb={RHO_B:.5f} "
      f"As,max(舊制)={AS_MAX_OLD:.2f}")
