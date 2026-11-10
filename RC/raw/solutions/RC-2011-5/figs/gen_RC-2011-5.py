#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2011-5 後拉法合成梁・三斷面應力疊加 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2011-5.md §1 給定的原始資料（F_i、F_0、三組斷面性質、n、A_sp）；
     纖維距離 y_t = I/Z_t、各應力分量、腱應力一律現算，檔尾對 §4 公佈值 assert。
  2. 改 §1 任一數字（F_0、M_L、Z_b3…）重跑，三張圖全部跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

FIGURES
  fig-1-sections  淨／變換／合成三斷面   攔：三組 Z 與三個 e_p 張冠李戴
  fig-2-stress    兩階段應力疊加         攔：偏心項與彎矩項的正負方向記反
  fig-3-tendon    腱應力三階段           攔：以為腱應力就是 F/A_sp
"""
import sys, os, math

sys.path.insert(0, os.environ.get(
    "STRUCTDRAW_DIR", "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose                       # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2011-5"

# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
FI  = 250_000.0      # 起始預力 (kgf)
F0  = 220_000.0      # 有效預力 (kgf)
MG  = 3_000_000.0    # 梁重彎矩 (kgf·cm)
MS  = 1_500_000.0    # 版重彎矩
ML  = 7_000_000.0    # 活載重彎矩
NR  = 6.0            # n = E_p/E_c
ASP = 24.0           # 鋼腱面積 (cm^2)

# (A_c, Z_t, Z_b, I, e_p)
NET  = dict(name="淨斷面",   A=2500.0, Zt=40_000.0,  Zb=39_000.0, I=1_800_000.0, e=25.0)
TRAN = dict(name="變換斷面", A=2800.0, Zt=41_000.0,  Zb=43_000.0, I=1_900_000.0, e=24.0)
COMP = dict(name="合成斷面", A=3900.0, Zt=137_000.0, Zb=74_000.0, I=4_300_000.0, e=39.0)

R2 = lambda x: round(x, 2)          # §4 逐項先取兩位小數再相加（與解題檔逐位一致）


def fibre(S):
    """由 y = I/Z 反算上下緣至形心的距離（純幾何，不是額外資料）。"""
    return dict(yt=S["I"] / S["Zt"], yb=S["I"] / S["Zb"])


for S in (NET, TRAN, COMP):
    S.update(fibre(S))
    S["h"] = S["yt"] + S["yb"]

# ── 施預力階段（淨斷面：F_i + M_G） ──────────────────────
P1 = dict(axial=R2(FI / NET["A"]),
          ecc_t=R2(FI * NET["e"] / NET["Zt"]), ecc_b=R2(FI * NET["e"] / NET["Zb"]),
          mom_t=R2(MG / NET["Zt"]),            mom_b=R2(MG / NET["Zb"]))
F1_TOP = R2(P1["axial"] - P1["ecc_t"] + P1["mom_t"])
F1_BOT = R2(P1["axial"] + P1["ecc_b"] - P1["mom_b"])
FS1 = FI / ASP

# ── 全載 Step A（變換斷面：F_0 + M_G + M_S） ─────────────
MGS = MG + MS
PA = dict(axial=R2(F0 / TRAN["A"]),
          ecc_t=R2(F0 * TRAN["e"] / TRAN["Zt"]), ecc_b=R2(F0 * TRAN["e"] / TRAN["Zb"]),
          mom_t=R2(MGS / TRAN["Zt"]),           mom_b=R2(MGS / TRAN["Zb"]))
FA_TOP = R2(PA["axial"] - PA["ecc_t"] + PA["mom_t"])
FA_BOT = R2(PA["axial"] + PA["ecc_b"] - PA["mom_b"])

# ── 全載 Step B（合成斷面：僅 M_L） ─────────────────────
FB_TOP = R2(ML / COMP["Zt"])
FB_BOT = R2(-ML / COMP["Zb"])
F2_TOP = R2(FA_TOP + FB_TOP)
F2_BOT = R2(FA_BOT + FB_BOT)

# ── 腱應力（相容性） ─────────────────────────────────────
FS_BASE = F0 / ASP
SIG_A = R2(MGS * TRAN["e"] / TRAN["I"])      # 腱位張應力（變換斷面）
SIG_B = R2(ML * COMP["e"] / COMP["I"])       # 腱位張應力（合成斷面）
SIG_GRAV = R2(SIG_A + SIG_B)
DFS = NR * SIG_GRAV
FS2 = FS_BASE + DFS
# 讀法 B（F_0 定義在 M_G 已作用之後）
SIG_B_ALT = R2(R2(MS * TRAN["e"] / TRAN["I"]) + SIG_B)
FS2_ALT = FS_BASE + NR * SIG_B_ALT
# 灌漿後全斷面回推（§5 ①）
AG = TRAN["A"] - (NR - 1) * ASP
A_DUCT = AG - NET["A"]


# ══════════════════════════════════════════════════════════
# 共用：線性應力分佈（壓為正 → 畫右側藍；拉為負 → 畫左側紅）
# ══════════════════════════════════════════════════════════
def stress_shape(cv, h, ftop, fbot, ss, x0=0.0, w=2.2):
    ys = [0.0, h]
    if ftop * fbot < 0:
        ys = [0.0, -fbot / (ftop - fbot) * h, h]
    for i in range(len(ys) - 1):
        ya, yb = ys[i], ys[i + 1]
        fa = fbot + (ftop - fbot) * ya / h
        fb = fbot + (ftop - fbot) * yb / h
        comp = (fa + fb) > 0
        cv.polygon([(x0, ya), (x0 + fa * ss, ya), (x0 + fb * ss, yb), (x0, yb)],
                   C["fill_c"] if comp else C["fill_t"],
                   C["compr"] if comp else C["tension"], w)
    cv.line((x0, 0), (x0, h), C["member"], 2.6)


# ══════════════════════════════════════════════════════════
# 圖 1　三斷面對照
# ══════════════════════════════════════════════════════════
PW, PH = 430, 600
HMAX = max(S["h"] for S in (NET, TRAN, COMP))
SLAB_T = 18.0                                     # 樓版示意厚度（僅示意，不參與計算）
sc = min((PW - 200) / 110.0, (PH - 268) / (HMAX + SLAB_T))
BW_D, BF_D = 34.0, 110.0                          # 示意腹板／翼板寬（僅示意）


def sect_panel(S, tag, stage, use, slab=False):
    cv = Canvas(PW, PH, sx=sc, ox=PW / 2, oy=PH - 150 - S["h"] * sc)
    cv.panel(tag, stage)
    top, bot = S["yt"], -S["yb"]
    # 梁本體（示意矩形；真正由解題決定的是 y_t、y_b 與形心位置）
    cv.polygon([(-BW_D / 2, bot), (BW_D / 2, bot), (BW_D / 2, top), (-BW_D / 2, top)],
               "#EDF1F6", C["member"], 2.6)
    if slab:
        cv.polygon([(-BF_D / 2, top), (BF_D / 2, top), (BF_D / 2, top + SLAB_T),
                    (-BF_D / 2, top + SLAB_T)], "#E3E9F2", C["member2"], 2.2)
        cv.text_px(cv.X(0), cv.Y(top + SLAB_T / 2), "樓版", 11.5, C["muted"])
    # 形心線
    cv.line((-BF_D / 2 * 0.92, 0), (BF_D / 2 * 0.92, 0), C["accent"], 2.0, dash="7 4")
    cv.text_px(cv.X(BF_D / 2 * 0.92) + 6, cv.Y(0), "形心", 11.5, C["accent"], "start",
               weight="700")
    # 鋼腱
    cv.dot((0, -S["e"]), 6.2, fill=C["tension"], stroke="#FFFFFF", w=1.8)
    cv.dim((BW_D / 2 + 4, 0), (BW_D / 2 + 4, -S["e"]), f"e_{{p}}={S['e']:.0f}",
           off=-34, label_off=-12, color=C["tension"])
    cv.dim((-BW_D / 2 - 4, top), (-BW_D / 2 - 4, 0), f"y_{{t}}={S['yt']:.2f}",
           off=42, label_off=13)
    cv.dim((-BW_D / 2 - 4, 0), (-BW_D / 2 - 4, bot), f"y_{{b}}={S['yb']:.2f}",
           off=42, label_off=13)
    cv.text_px(PW / 2, PH - 112, use, 12.5, C["bmd"], weight="700")
    cv.text_px(PW / 2, PH - 86,
               f"A_{{c}} = {S['A']:.0f} cm^{{2}}　I = {S['I']/1e6:.2f}×10^{{6}} cm^{{4}}",
               12, C["muted"])
    cv.text_px(PW / 2, PH - 62,
               f"Z_{{t}} = {S['Zt']:,.0f}　Z_{{b}} = {S['Zb']:,.0f} cm^{{3}}", 12, C["muted"])
    cv.text_px(PW / 2, PH - 38,
               f"y = I/Z 反算：上緣 {S['yt']:.2f}、下緣 {S['yb']:.2f} cm", 11.5, C["muted"])
    return cv


compose([sect_panel(NET, "① 淨斷面", "灌漿前（扣導管孔）",
                    "施預力時：F_i + M_G"),
         sect_panel(TRAN, "② 變換斷面", "灌漿後、合成前",
                    "恆載：F_0 + M_G + M_S"),
         sect_panel(COMP, "③ 合成斷面", "樓版硬化並結合後",
                    "活載：M_L", slab=True)],
        title=f"{TAG}　三個階段用三個斷面，e_p 也跟著換",
        sub=(f"形心隨斷面改變而上移，故 e_p 由 {NET['e']:.0f} → {TRAN['e']:.0f} → "
             f"{COMP['e']:.0f} cm；Zt3 量到梁頂（題目問的是梁的上下緣）"),
        note=(f"§5①：灌漿後孔洞已填實，Ac2 = Ag + (n−1)Asp，"
              f"回推 Ag = {AG:.0f}、導管孔 = {A_DUCT:.0f} cm²；"
              f"不是 Ac1 + n·Asp（那會得 {NET['A'] + NR*ASP:.0f} ≠ {TRAN['A']:.0f}）"),
        path=f"{OUT}/{TAG}-fig-1-sections.svg")

# ══════════════════════════════════════════════════════════
# 圖 2　兩階段應力疊加
# ══════════════════════════════════════════════════════════
PW, PH = 460, 620
SMAX = 200.0                                      # 應力繪圖半幅 (kgf/cm^2)
sc2 = (PH - 370) / HMAX                           # 1 cm → 像素（三格共用）
SS = (128.0 / SMAX) / sc2                         # 1 kgf/cm² → 模型單位
SEC_W = 26.0 / sc2                                # 斷面示意帶寬（模型單位）


def stage_panel(S, tag, sub, ftop, fbot, rows, foot):
    cv = Canvas(PW, PH, sx=sc2, ox=PW * 0.40, oy=PH - 176 - S["h"] * sc2)
    cv.panel(tag, sub)
    # 斷面示意帶（左側）：讓讀者看得到深度，y = 0 為下緣
    cv.polygon([(-SEC_W, 0), (0, 0), (0, S["h"]), (-SEC_W, S["h"])],
               "#EDF1F6", C["member"], 2.2)
    cv.dim((-SEC_W, S["h"]), (-SEC_W, 0), f"h≈{S['h']:.1f}", off=36, label_off=13)
    stress_shape(cv, S["h"], ftop, fbot, SS, x0=0.0)
    cv.math_px(cv.X(ftop * SS) + (8 if ftop > 0 else -8), cv.Y(S["h"]) - 2,
               f"{ftop:+.2f}", 13, C["compr"] if ftop > 0 else C["tension"],
               "start" if ftop > 0 else "end", weight="700")
    cv.math_px(cv.X(fbot * SS) + (8 if fbot > 0 else -8), cv.Y(0.0) + 2,
               f"{fbot:+.2f}", 13, C["compr"] if fbot > 0 else C["tension"],
               "start" if fbot > 0 else "end", weight="700")
    cv.text_px(cv.X(0) + 4, cv.Y(S["h"]) - 22, "上緣", 11.5, C["muted"], "start")
    cv.text_px(cv.X(0) + 4, cv.Y(0.0) + 22, "下緣", 11.5, C["muted"], "start")
    y0 = PH - 128
    for i, (lab, vt, vb) in enumerate(rows):
        cv.text_px(38, y0 + i * 21, lab, 11.5, C["muted"], "start")
        cv.text_px(PW - 118, y0 + i * 21, vt, 11.5, C["text"], "end")
        cv.text_px(PW - 24, y0 + i * 21, vb, 11.5, C["text"], "end")
    cv.text_px(38, y0 - 22, "分量（上緣／下緣）", 11.5, C["muted"], "start", weight="700")
    cv.text_px(PW / 2, PH - 26, foot, 12, C["bmd"], weight="700")
    return cv


p1 = stage_panel(
    NET, "施預力時（淨斷面）", f"F_i = {FI/1000:.0f} tf ＋ M_G",
    F1_TOP, F1_BOT,
    [("軸壓 F_i/A_c1", f"+{P1['axial']:.2f}", f"+{P1['axial']:.2f}"),
     ("偏心 F_i·e_p1/Z", f"−{P1['ecc_t']:.2f}", f"+{P1['ecc_b']:.2f}"),
     ("梁重 M_G/Z", f"+{P1['mom_t']:.2f}", f"−{P1['mom_b']:.2f}")],
    f"上緣 {F1_TOP:.2f}（壓）　下緣 {F1_BOT:.2f}（壓）")

p2 = stage_panel(
    TRAN, "全載 Step A（變換斷面）", f"F_0 = {F0/1000:.0f} tf ＋ M_G + M_S",
    FA_TOP, FA_BOT,
    [("軸壓 F_0/A_c2", f"+{PA['axial']:.2f}", f"+{PA['axial']:.2f}"),
     ("偏心 F_0·e_p2/Z", f"−{PA['ecc_t']:.2f}", f"+{PA['ecc_b']:.2f}"),
     ("恆載 (M_G+M_S)/Z", f"+{PA['mom_t']:.2f}", f"−{PA['mom_b']:.2f}")],
    f"上緣 {FA_TOP:.2f}（壓）　下緣 {FA_BOT:.2f}（壓）")

p3 = stage_panel(
    COMP, "全載 Step B ＋ 合計", "合成斷面只加 M_L",
    F2_TOP, F2_BOT,
    [("Step A 小計", f"+{FA_TOP:.2f}", f"+{FA_BOT:.2f}"),
     ("活載 M_L/Z（合成）", f"+{FB_TOP:.2f}", f"{FB_BOT:.2f}"),
     ("合計", f"+{F2_TOP:.2f}", f"+{F2_BOT:.2f}")],
    f"上緣 {F2_TOP:.2f}（壓）　下緣 {F2_BOT:.2f}（壓，幾乎為零）")

compose([p1, p2, p3],
        title=f"{TAG}　壓為正、拉為負：偏心壓下緣、彎矩壓上緣",
        sub=("同一支腱在下方 → 偏心項讓上緣減壓、下緣加壓；重力彎矩反過來。"
             "兩者方向相反，是本題所有正負號的來源"),
        note=(f"下緣最終 {F2_BOT:+.2f} kgf/cm²（仍為壓）＝ 斷面全程未開裂，"
              f"「三斷面未開裂彈性疊加」這套算法才成立（318-19 Class U）"),
        path=f"{OUT}/{TAG}-fig-2-stress.svg")

# ══════════════════════════════════════════════════════════
# 圖 3　腱應力三階段
# ══════════════════════════════════════════════════════════
W3, H3 = 880, 545
L_, R_, T_, B_ = 122, 182, 100, 152
pw, ph = W3 - L_ - R_, H3 - T_ - B_
asp = ph / pw
Y0, Y1 = 8800.0, 10850.0
cv = Canvas(W3, H3, sx=pw, ox=L_, oy=B_)
XS = [0.0, 1.0, 2.0]                              # 三個階段


def P(x, y): return (x / 2.4, (y - Y0) / (Y1 - Y0) * asp)


cv.panel("鋼腱應力不是一路遞減 —— 重力荷重會讓它回升", None)
cv.text_px(W3 / 2, 60, "縱軸：鋼腱應力 f_s（kgf/cm²）", 12.5, C["muted"])

for v in (9000, 9400, 9800, 10200, 10600):
    cv.line(P(0.0, v), P(2.4, v), C["border"], 1.0)
    cv.math_px(cv.X(P(0, v)[0]) - 10, cv.Y(P(0, v)[1]), f"{v:,}", 12.5, C["muted"], "end")
cv.line(P(0.0, Y0), P(2.4, Y0), C["muted"], 1.8)
cv.line(P(0.0, Y0), P(0.0, Y1), C["muted"], 1.8)

STAGES = [(0.0, FS1, "① 施預力時",
           f"f_{{s}} = F_{{i}}/A_{{sp}} = {FI/1000:.0f}×10^{{3}}/{ASP:.0f}", C["load"]),
          (1.0, FS_BASE, "② 有效預力",
           "f_{s} = F_{0}/A_{sp}（長期損失後）", C["muted"]),
          (2.0, FS2, "③ 全部載重",
           "f_{s} = F_{0}/A_{sp} + n·Δf_{c}", C["bmd"])]
cv.poly([P(x, v) for x, v, *_ in STAGES], C["member2"], 3.0)
for x, v, lab, expr, col in STAGES:
    cv.line(P(x, Y0), P(x, v), C["border"], 1.2, dash="4 4")
    cv.dot(P(x, v), 7.0, fill=col, stroke="#FFFFFF", w=2.2)
    cv.text_px(cv.X(P(x, 0)[0]), cv.Y(P(0, Y0)[1]) + 24, lab, 13, col, weight="700")
    cv.math_px(cv.X(P(x, 0)[0]) + (16 if x == 0.0 else 0),
               cv.Y(P(0, v)[1]) + (4 if x == 0.0 else -20),
               f"{v:,.0f}", 14.5, col, "start" if x == 0.0 else "middle", weight="700")
    cv.text_px(cv.X(P(x, 0)[0]), cv.Y(P(0, Y0)[1]) + 46, expr, 11.5, C["muted"])

# 兩個變化量
cv.arrow(P(0.5, FS1), P(0.5, FS_BASE), C["muted"], 2.6, 10)
cv.text_px(cv.X(P(0.5, 0)[0]) + 10, (cv.Y(P(0, FS1)[1]) + cv.Y(P(0, FS_BASE)[1])) / 2,
           f"損失 {FS1-FS_BASE:,.0f}", 12.5, C["muted"], "start", weight="700")
cv.arrow(P(1.5, FS_BASE), P(1.5, FS2), C["bmd"], 2.6, 10)
cv.text_px(cv.X(P(1.5, 0)[0]) + 10, (cv.Y(P(0, FS_BASE)[1]) + cv.Y(P(0, FS2)[1])) / 2,
           f"回升 +{DFS:,.0f}", 12.5, C["bmd"], "start", weight="700")

# 讀法 B
cv.dot(P(2.0, FS2_ALT), 5.4, fill="#FFFFFF", stroke=C["accent"], w=2.4)
cv.text_px(cv.X(P(2.0, 0)[0]) + 14, cv.Y(P(0, FS2_ALT)[1]),
           f"讀法 B：{FS2_ALT:,.0f}", 12, C["accent"], "start", weight="700")
cv.text_px(cv.X(P(2.0, 0)[0]) + 14, cv.Y(P(0, FS2_ALT)[1]) + 18,
           "（M_G 視為灌漿前已作用）", 11, C["accent"], "start")

cv.text_px(W3 / 2, H3 - 62,
           f"重力使腱位混凝土受張 {SIG_GRAV:.2f} kgf/cm²"
           f"（變換斷面 {SIG_A:.2f} ＋ 合成斷面 {SIG_B:.2f}）"
           f"　→　Δf_s = n × {SIG_GRAV:.2f} = {DFS:,.0f}", 13, C["text"])
cv.text_px(W3 / 2, H3 - 36,
           "有黏結腱與混凝土應變相容：混凝土被拉長，腱跟著被拉長，應力回升", 12.5, C["muted"])
cv.save(f"{OUT}/{TAG}-fig-3-tendon.svg")

# ══════════════════════════════════════════════════════════
# 對 .md §4 公佈值 assert
# ══════════════════════════════════════════════════════════
assert (P1["axial"], P1["ecc_t"], P1["ecc_b"], P1["mom_t"], P1["mom_b"]) == \
       (100.0, 156.25, 160.26, 75.0, 76.92), P1
assert F1_TOP == 18.75,   F1_TOP
assert F1_BOT == 183.34,  F1_BOT
assert abs(FS1 - 10417) < 1,  FS1
assert (PA["axial"], PA["ecc_t"], PA["ecc_b"], PA["mom_t"], PA["mom_b"]) == \
       (78.57, 128.78, 122.79, 109.76, 104.65), PA
assert FA_TOP == 59.55,   FA_TOP
assert FA_BOT == 96.71,   FA_BOT
assert FB_TOP == 51.09,   FB_TOP
assert FB_BOT == -94.59,  FB_BOT
assert F2_TOP == 110.64,  F2_TOP
assert F2_BOT == 2.12,    F2_BOT
assert abs(FS_BASE - 9167) < 1,       FS_BASE
assert SIG_A == 56.84,    SIG_A
assert SIG_B == 63.49,    SIG_B
assert SIG_GRAV == 120.33, SIG_GRAV
assert abs(DFS - 722) < 0.5,          DFS
assert abs(FS2 - 9889) < 1,           FS2
assert abs(FS2_ALT - 9661) < 2,       FS2_ALT
assert abs(AG - 2680) < 1e-9,         AG
assert abs(A_DUCT - 180) < 1e-9,      A_DUCT
print(f"{TAG}: 3 圖 OK　施預力 {F1_TOP}/{F1_BOT}　全載 {F2_TOP}/{F2_BOT}　"
      f"f_s {FS1:,.0f} → {FS_BASE:,.0f} → {FS2:,.0f}（讀法B {FS2_ALT:,.0f}）　"
      f"y_t/y_b = " + " ; ".join(f"{S['yt']:.2f}/{S['yb']:.2f}" for S in (NET, TRAN, COMP)))
