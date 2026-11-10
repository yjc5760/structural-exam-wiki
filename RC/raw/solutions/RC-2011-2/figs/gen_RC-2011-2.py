#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2011-2 T 形梁 As = 0.9Asb・斷面韌性容量 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2011-2.md §1 給定的原始資料；c_b、A_sb、a、c_u、k_yd、
     φ_y、φ_u、μ_φ 一律由 solve() 現算，檔尾對 §4／§5 公佈值 assert。
  2. 改 §1 任一數字（b_f、h_f、b_w、d、f'_c）重跑，三張圖全部跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

FIGURES
  fig-1-section    兩種尺寸讀法對照   攔：把附圖尺寸鏈直讀成 d=100 而不自覺
  fig-2-et-band    εt 規範帶狀圖      攔：φ 逕取 0.9、漏檢 εt ≥ 0.004
  fig-3-curvature  彈性 NA vs 塑性 NA 攔：φy 與 φu 混用同一條中性軸
"""
import sys, os, math

sys.path.insert(0, os.environ.get(
    "STRUCTDRAW_DIR", "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose                       # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2011-2"

# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
BF     = 80.0      # 翼板寬 (cm)
HF     = 10.0      # 翼板厚 (cm)
BW     = 40.0      # 腹板寬 (cm)
COV    = 10.0      # 底部鋼筋形心至底纖維 (cm)
H_MAIN = 100.0     # 本解採用的全深 (cm)   ← 依圖面比例判定
H_ALT  = 110.0     # 尺寸鏈直讀的全深 (cm)
FC     = 350.0
FY     = 4200.0
ES     = 2.04e6
EPS_CU = 0.003
RATIO  = 0.9       # As = 0.9 Asb

B1   = 0.85 if FC <= 280 else max(0.65, 0.85 - 0.05 * (FC - 280) / 70)
EPSY = FY / ES
# §4 逐步公佈的位數：a 取兩位小數、εy 取 0.002059、k_yd 取兩位小數。
# 圖上要與解題檔逐位相同，故沿用同一條四捨五入鏈。
EPSY_PUB = round(EPSY, 6)
EC   = 15000 * math.sqrt(FC)
NRAT = ES / EC


def phi_of(et):
    if et >= 0.005: return 0.90
    if et <= EPSY:  return 0.65
    return 0.65 + 0.25 * (et - EPSY) / (0.005 - EPSY)


def solve(h):
    """給定全深 h（→ d = h − 保護層），回傳整題的所有結果。"""
    d = h - COV
    cb = 6120 / (6120 + FY) * d
    ab = B1 * cb
    Cc = 0.85 * FC * (BF * HF + BW * (ab - HF))
    Asb = Cc / FY
    As = RATIO * Asb
    a = round(HF + (As * FY / (0.85 * FC) - BF * HF) / BW, 2)   # §4 Step 4 公佈值
    cu = a / B1                                                  # §4 Step 5：a/β1
    et = EPS_CU * (d - cu) / cu
    phi = phi_of(et)
    Cw = 0.85 * FC * BW * a
    Cf = 0.85 * FC * (BF - BW) * HF
    Mn = Cw * (d - a / 2) + Cf * (d - HF / 2)
    # 彈性轉換斷面中性軸（NA 在腹板）
    qa = BW / 2
    qb = (BF - BW) * HF + NRAT * As
    qc = -((BF - BW) * HF * HF / 2 + NRAT * As * d)
    ky_d = round((-qb + math.sqrt(qb * qb - 4 * qa * qc)) / (2 * qa), 2)  # §4 Step 7 公佈值
    phy = EPSY_PUB / (d - ky_d)
    phu = EPS_CU / cu
    return dict(h=h, d=d, cb=cb, ab=ab, Asb=Asb, As=As, a=a, cu=cu, et=et,
                phi=phi, Mn=Mn, ky_d=ky_d, phy=phy, phu=phu, mu=phu / phy,
                Cw=Cw, Cf=Cf)


M = solve(H_MAIN)      # 本解
A = solve(H_ALT)       # 直讀

# ══════════════════════════════════════════════════════════
# 共用：T 形斷面
# ══════════════════════════════════════════════════════════
def outline(h):
    return [((BF - BW) / 2, 0), ((BF + BW) / 2, 0), ((BF + BW) / 2, h - HF),
            (BF, h - HF), (BF, h), (0, h), (0, h - HF), ((BF - BW) / 2, h - HF)]


def draw_T(cv, h, d, nbar=5):
    cv.polygon(outline(h) + [outline(h)[0]], "#EDF1F6", C["member"], 2.6)
    cv.line((0, h - HF), (BF, h - HF), C["member2"], 1.4, dash="4 4")
    x0, x1 = (BF - BW) / 2 + 6, (BF + BW) / 2 - 6
    for i in range(nbar):
        x = x0 + (x1 - x0) * i / (nbar - 1)
        cv.dot((x, h - d), 5.4, fill=C["tension"], stroke="#FFFFFF", w=1.5)


# ══════════════════════════════════════════════════════════
# 圖 1　兩種尺寸讀法對照
# ══════════════════════════════════════════════════════════
PW, PH = 470, 650
TOPPX = 132                                       # 斷面頂緣距畫布上緣（兩格對齊）
sc = min((PW - 195) / BF, (PH - TOPPX - 205) / H_ALT)


def read_panel(R, title, sub, main, chain):
    cv = Canvas(PW, PH, sx=sc, ox=PW / 2 - BF * sc / 2, oy=PH - TOPPX - R["h"] * sc)
    cv.panel(title, sub)
    draw_T(cv, R["h"], R["d"])
    col = C["bmd"] if main else C["muted"]
    cv.dim((0, R["h"]), (BF, R["h"]), f"b_{{f}}={BF:.0f}", off=-42, label_off=-14)
    cv.dim((BF, R["h"]), (BF, R["h"] - HF), f"{HF:.0f}", off=-34, label_off=-12)
    cv.dim((BF, R["h"] - HF), (BF, R["h"] - R["d"]), f"{R['d']-HF:.0f}", off=-34, label_off=-12)
    cv.dim((BF, R["h"] - R["d"]), (BF, 0), f"{COV:.0f}", off=-34, label_off=-12)
    cv.dim((0, R["h"]), (0, 0), f"h={R['h']:.0f}", off=42, label_off=14)
    cv.line((0, R["h"] - R["d"]), (BF, R["h"] - R["d"]), C["tension"], 1.5, dash="6 4")
    cv.text_px(PW / 2, PH - 150, chain, 12, C["muted"])
    cv.text_px(PW / 2, PH - 118, f"d = {R['d']:.0f} cm", 15, col, weight="700")
    cv.text_px(PW / 2, PH - 92, f"A_{{sb}} = {R['Asb']:.2f} cm^{{2}}　"
                                f"A_{{s}} = {R['As']:.2f} cm^{{2}}", 12.5, C["muted"])
    cv.text_px(PW / 2, PH - 68, f"a = {R['a']:.2f} cm　φ = {R['phi']:.4f}", 12.5, C["muted"])
    cv.text_px(PW / 2, PH - 42, f"φM_{{n}} = {R['phi']*R['Mn']/1e5:.1f} tf·m　"
                                f"μ_{{φ}} = {R['mu']:.2f}", 15, col, weight="700")
    return cv


compose([read_panel(M, "本解：h = 100、d = 90", "依圖面比例判定　b_w = 40 cm", True,
                    "右側尺寸鏈讀成 10 + 80 + 10 = 100；圖上標「90」那段的下箭頭位置畫錯"),
         read_panel(A, "直讀尺寸鏈：h = 110、d = 100", "把「10 → 90 → 10」逐段相加　b_w = 40 cm", False,
                    "右側尺寸鏈讀成 10 + 90 + 10 = 110；但整張圖會比標註短 10%")],
        title=f"{TAG}　附圖尺寸鏈有兩種讀法，先把它講清楚再算",
        sub="兩種讀法之下 μφ 幾乎相同（無因次），但 φMn 差 20%",
        note=("量測圖檔像素：翼板厚與底部保護層都畫成 35～38 px、全斷面高 354 px ≈ 101 cm，"
              "整張圖對 h = 100 合乎比例"),
        path=f"{OUT}/{TAG}-fig-1-section.svg")

# ══════════════════════════════════════════════════════════
# 圖 2　εt 規範帶狀圖
# ══════════════════════════════════════════════════════════
W3, H3 = 900, 400
L, R, T, Bm = 90, 80, 110, 150
X0, X1 = 0.0015, 0.0065
pw = W3 - L - R
cv = Canvas(W3, H3, sx=pw, ox=L, oy=Bm)


def X(et): return (et - X0) / (X1 - X0)


BAND_H = 68 / pw                                  # 帶狀高度（模型單位）
cv.panel("淨拉應變 εt 落在哪一段？", "土木401-100：非預力撓曲構材 εt ≥ 0.004")

zones = [(X0, EPSY, "壓力控制", "rgba(29,78,216,0.16)", C["compr"]),
         (EPSY, 0.004, "梁不得使用（εt 小於 0.004）", "rgba(192,57,43,0.18)", C["load"]),
         (0.004, 0.005, "過渡區・梁可用", "rgba(180,83,9,0.16)", C["accent"]),
         (0.005, X1, "拉力控制 φ = 0.90", "rgba(46,125,111,0.16)", C["bmd"])]
for a0, a1, lab, fill, col in zones:
    cv.polygon([(X(a0), 0), (X(a1), 0), (X(a1), BAND_H), (X(a0), BAND_H)], fill, col, 1.6)
    cv.text_px((cv.X(X(a0)) + cv.X(X(a1))) / 2, cv.Y(BAND_H / 2), lab, 12.5, col, weight="700")

for v, lab in ((EPSY, f"ε_{{ty}}={EPSY:.6f}"), (0.004, "0.004"), (0.005, "0.005")):
    cv.line((X(v), 0), (X(v), BAND_H), C["text"], 1.6)
    cv.math_px(cv.X(X(v)), cv.Y(0) + 22, lab, 12.5, C["text"], weight="700")
cv.line((X(X0), 0), (X(X1), 0), C["muted"], 1.8)

# 本題的 εt
cv.arrow((X(M["et"]), BAND_H * 1.80), (X(M["et"]), BAND_H * 1.06), C["load"], 3.2, 11)
cv.text_px(cv.X(X(M["et"])), cv.Y(BAND_H * 1.80) - 16,
           f"本題 ε_{{t}} = {M['et']:.6f}", 14, C["load"], weight="700")
cv.text_px(cv.X(X(M["et"])), cv.Y(BAND_H * 1.80) - 38,
           f"（A_{{s}} = 0.9A_{{sb}}，c_{{u}} = {M['cu']:.2f} cm）", 12.5, C["load"])

cv.text_px(W3 / 2, H3 - 96,
           f"φ = 0.65 + 0.25 × (εt − εty)/(0.005 − εty) = {M['phi']:.4f}"
           f"　　不是 0.90（差 {100*(0.9-M['phi'])/M['phi']:.0f}%）",
           13.5, C["accent"], weight="700")
cv.text_px(W3 / 2, H3 - 68,
           f"εt = {M['et']:.6f} 小於 0.004 → 規範上此斷面不得作為梁；"
           f"μφ = {M['mu']:.2f} 正是這件事的量化證據",
           13.5, C["load"], weight="700")
cv.text_px(W3 / 2, H3 - 40,
           "「As 小於 Asb」不等於合法 —— 算完 εt 一律順手比 0.004", 13, C["muted"])
cv.save(f"{OUT}/{TAG}-fig-2-et-band.svg")

# ══════════════════════════════════════════════════════════
# 圖 3　彈性中性軸 vs 塑性中性軸（兩種曲率）
# ══════════════════════════════════════════════════════════
PW, PH = 470, 610
h, d = M["h"], M["d"]
sc = min((PW - 165) / BF, (PH - 250) / h)
MW = 88 / sc                                     # 應變圖最大半寬


def curvature_panel(title, sub, na, eps_top, eps_bot, col, phi_val, phi_lab, extra, formula):
    cv = Canvas(PW, PH, sx=sc, ox=PW * 0.40, oy=150)
    cv.panel(title, sub)
    cv.line((0, 0), (0, h), C["ghost"], 2, dash="5 4")
    wc = MW if eps_top >= eps_bot else MW * eps_top / eps_bot
    wt = MW if eps_bot >= eps_top else MW * eps_bot / eps_top
    cv.polygon([(0, h), (wc, h), (0, h - na)], C["fill_c"], C["compr"], 2.4)
    cv.polygon([(0, h - na), (-wt, h - d), (0, h - d)], C["fill_t"], C["tension"], 2.4)
    cv.line((-MW * 1.25, h - na), (MW * 1.25, h - na), col, 2.0, dash="6 4")
    cv.text_px(cv.X(MW * 1.25) + 4, cv.Y(h - na), "N.A.", 12, col, "start", weight="700")
    cv.math_px(cv.X(wc) + 6, cv.Y(h) - 13, f"ε={eps_top:.5f}", 12, C["compr"], "start",
               weight="700")
    cv.math_px(cv.X(-wt) - 6, cv.Y(h - d), f"ε={eps_bot:.5f}", 12, C["tension"], "end",
               weight="700")
    cv.dim((0, h), (0, h - na), f"{na:.2f}", off=32, label_off=12, color=col)
    cv.text_px(PW / 2, PH - 116, extra, 12, C["muted"])
    cv.text_px(PW / 2, PH - 88, formula, 12.5, C["text"])
    cv.text_px(PW / 2, PH - 58, f"{phi_lab} = {phi_val*1e5:.3f} × 10^{{-5}} rad/cm",
               14.5, col, weight="700")
    return cv


p_y = curvature_panel(
    "降伏曲率 φy（彈性轉換斷面）", f"n = Es/Ec = {NRAT:.2f}，鋼筋剛達 fy",
    M["ky_d"], EPSY * M["ky_d"] / (d - M["ky_d"]), EPSY, C["deform"],
    M["phy"], "φ_{y}",
    f"k_y·d = {M['ky_d']:.2f} cm 由轉換斷面一次矩 = 0 解出（幾何性質）",
    f"φ_{{y}} = ε_{{y}} / (d − k_{{y}}d) = {EPSY:.6f} / {d - M['ky_d']:.2f}")
p_u = curvature_panel(
    "極限曲率 φu（Whitney 塑性）", f"混凝土達 εcu = 0.003",
    M["cu"], EPS_CU, M["et"], C["accent"],
    M["phu"], "φ_{u}",
    f"c_u = a/β1 = {M['cu']:.2f} cm 由力平衡 Cc = As·fy 解出（配筋量決定）",
    f"φ_{{u}} = ε_{{cu}} / c_{{u}} = 0.003 / {M['cu']:.2f}")

compose([p_y, p_u],
        title=f"{TAG}　兩個中性軸不是同一條：φy 用彈性，φu 用塑性",
        sub=(f"kyd = {M['ky_d']:.2f} cm　vs　cu = {M['cu']:.2f} cm　"
             f"→ μφ = φu/φy = {M['mu']:.2f}"),
        note=("誰深誰淺沒有普適因果，只能實算比較 —— "
              "「矩形應力塊力臂大所以中性軸更深」是把 kyd 也當成力平衡決定的，因果講反了"),
        path=f"{OUT}/{TAG}-fig-3-curvature.svg")

# ══════════════════════════════════════════════════════════
# 對 .md §4／§5 公佈值 assert
# ══════════════════════════════════════════════════════════
assert abs(B1 - 0.80) < 1e-9,               B1
assert abs(NRAT - 7.27) < 0.005,            NRAT
assert abs(M["cb"] - 53.37) < 0.01,         M["cb"]
assert abs(M["ab"] - 42.70) < 0.01,         M["ab"]
assert abs(M["Asb"] - 149.31) < 0.02,       M["Asb"]
assert abs(M["As"] - 134.38) < 0.02,        M["As"]
assert abs(M["a"] - 37.43) < 0.01,          M["a"]
assert abs(M["cu"] - 46.79) < 0.005,        M["cu"]
assert abs(M["et"] - 0.002771) < 5e-6,      M["et"]
assert abs(M["phi"] - 0.7105) < 5e-4,       M["phi"]
assert abs(M["Mn"] / 1e5 - 418.7) < 0.2,    M["Mn"] / 1e5
assert abs(M["phi"] * M["Mn"] / 1e5 - 297.5) < 0.3, M["phi"] * M["Mn"] / 1e5
assert abs(M["ky_d"] - 40.95) < 0.02,       M["ky_d"]
assert abs(M["phy"] * 1e5 - 4.198) < 0.001, M["phy"] * 1e5
assert abs(M["phu"] * 1e5 - 6.412) < 0.005, M["phu"] * 1e5
assert abs(M["mu"] - 1.53) < 0.01,          M["mu"]
# 直讀版（§5 ⑥ 對照表）
assert abs(A["cb"] - 59.30) < 0.02,         A["cb"]
assert abs(A["Asb"] - 162.75) < 0.05,       A["Asb"]
assert abs(A["a"] - 41.70) < 0.02,          A["a"]
assert abs(A["cu"] - 52.13) < 0.01,         A["cu"]
assert abs(A["et"] - 0.002755) < 5e-6,      A["et"]
assert abs(A["Mn"] / 1e5 - 505.8) < 0.4,    A["Mn"] / 1e5
assert abs(A["ky_d"] - 45.63) < 0.05,       A["ky_d"]
assert abs(A["mu"] - 1.52) < 0.01,          A["mu"]
print(f"{TAG}: 3 圖 OK　d={M['d']:.0f} cb={M['cb']:.2f} Asb={M['Asb']:.2f} a={M['a']:.2f} "
      f"cu={M['cu']:.2f} et={M['et']:.6f} φ={M['phi']:.4f} φMn={M['phi']*M['Mn']/1e5:.1f} "
      f"kyd={M['ky_d']:.2f} μφ={M['mu']:.2f}　|| 直讀 φMn={A['phi']*A['Mn']/1e5:.1f} "
      f"μφ={A['mu']:.2f}")
