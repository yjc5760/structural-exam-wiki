# -*- coding: utf-8 -*-
"""SM-2019-2 圖解。數值取自 SM-2019-2.md §4，表一逐列取自考卷第 3-2 頁。"""
import sys, math, os
sys.path.insert(0, "/tmp/sd")
from geo import *
from geo import tag_px

OUT = "/tmp/sd/out/SM-2019-2"
os.makedirs(OUT, exist_ok=True)

# ── 由 SM-2019-2 §4 解得 ────────────────────────────────
HCL, E0, CC, CV = 4.0, 0.9, 0.25, 0.008
P0, DP, DPF = 70.0, 150.0, 281.0
HDR = HCL / 2                                     # 雙面排水
SC  = CC * HCL / (1 + E0) * math.log10((P0 + DP) / P0)     # 0.26172 m
SCF = CC * HCL / (1 + E0) * math.log10((P0 + DPF) / P0)    # 0.36848 m
UREQ = SC / SCF                                            # 0.71026

# ── 考卷第 3-2 頁「表一」逐列轉錄（14 列，未經任何改寫）──
TBL = [(0.05, 0.31), (0.10, 5.07), (0.15, 13.58), (0.20, 22.77), (0.25, 31.46),
       (0.30, 39.32), (0.40, 52.55), (0.50, 62.92), (0.60, 71.03), (0.70, 77.36),
       (0.80, 82.31), (0.90, 86.18), (1.00, 89.2), (1.50, 96.86)]

def tv_from_table(u):
    for (t0, u0), (t1, u1) in zip(TBL, TBL[1:]):
        if u0 <= u <= u1:
            return t0 + (t1 - t0) * (u - u0) / (u1 - u0)
    return None

TV_TBL = tv_from_table(UREQ * 100)                 # 0.5999
T_TBL  = TV_TBL * HDR ** 2 / CV                    # ≈ 300 天
TV_THY = 1.781 - 0.933 * math.log10(100 - UREQ * 100)   # 0.41686
T_THY  = TV_THY * HDR ** 2 / CV                    # ≈ 208.4 天


def seg(cv, p0, p1, col, w, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    cv.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%s" '
                    'stroke-linecap="round"%s/>' % (p0[0], p0[1], p1[0], p1[1], col, w, d))
def curve(cv, pts, col, w, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    cv.parts.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" '
                    'stroke-linecap="round" stroke-linejoin="round"%s/>'
                    % (" ".join("%.2f,%.2f" % p for p in pts), col, w, d))

# ══════ fig-3：地層剖面（向量重繪，取代掃描截圖）══════
W, H = 900, 560
cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (0, 1), (-1, 0), 120, 250, 128, 108))
Y = lambda d: -d / 10.0          # 深度 0~10 對應 0~-1
xa, xb = 0.02, 0.90
D_TOPSAND, D_CLAY_T, D_CLAY_B, D_BOT = 0.0, 4.0, 8.0, 10.0
WTD = 1.6
for d0, d1, col, lab, dlab in [(D_TOPSAND, D_CLAY_T, "rgba(180,83,9,0.20)", "砂土（透水）", 2.6),
                               (D_CLAY_T, D_CLAY_B, "rgba(63,74,90,0.26)", "黏土（正常壓密 NC）", 4.7),
                               (D_CLAY_B, D_BOT, "rgba(180,83,9,0.20)", "砂土（透水）", 9.1)]:
    soil_fill(cv, xa, xb, Y(d1), Y(d0), col)
    cv.line((xa, Y(d1)), (xb, Y(d1)), C["member2"], 1.8)
    cv.text_px(cv.X(xa) + 10, cv.Y(Y(dlab)), lab, 13, C["text"], anchor="start")
cv.line((xa, Y(0)), (xb, Y(0)), C["member"], 2.6)
cv.udl((xa + 0.02, Y(0)), (xb - 0.02, Y(0)), 0.052, 9, C["load"], 2.0)
tag_px(cv, cv.X((xa + xb) / 2), cv.Y(Y(0)) - 46, "大面積均布載重（深度不折減）", 13, C["load"])
cv.line((xa, Y(WTD)), (xb, Y(WTD)), C["deform"], 1.8, dash="8 5")
wt_symbol(cv, 0.78, Y(WTD), C["deform"], 0.016)
cv.text_px(cv.X(xb) - 10, cv.Y(Y(WTD)) - 15, "地下水位", 12, C["deform"], anchor="end")
# 排水方向：上下皆為砂
for x in (0.30, 0.46, 0.62):
    cv.arrow((x, Y(6.0) + 0.005), (x, Y(D_CLAY_T) + 0.030), C["deform"], 2.2, 8)
    cv.arrow((x, Y(6.0) - 0.005), (x, Y(D_CLAY_B) - 0.030), C["deform"], 2.2, 8)
cv.line((xa, Y(6.0)), (xb, Y(6.0)), C["accent"], 2.0, dash="7 5")
tag_px(cv, cv.X(xb) - 10, cv.Y(Y(6.0)), "層中央（不排水面）", 12, C["accent"], anchor="end")
cv.dim((xb + 0.05, Y(D_CLAY_B)), (xb + 0.05, Y(D_CLAY_T)), "H = 4 m", 0, C["dim"], 13.5,
       label_off=18)
cv.dim((xb + 0.32, Y(6.0)), (xb + 0.32, Y(D_CLAY_T)), "H_{dr} = 2 m", 0, C["accent"], 13.5,
       label_off=58)
cv.text_px(W / 2, 32, "圖 3　黏土層上下皆為砂 ⇒ 雙面排水，H_{dr} 取層厚的一半", 17.5,
           C["text"], weight="700")
cv.text_px(W / 2, 58, "題幹給的黏土參數：e_0 = 0.9、C_c = 0.25、c_v = 0.008 m²/day、"
                      "層中央 p'_0 = 70 kPa", 12.5, C["muted"])
cv.text_px(W / 2, H - 44,
           "攔錯用：H_{dr} 誤取 4 m，t 會放大 4 倍。判準是「上下都有透水層」，不是層厚本身。",
           13, C["accent"], weight="700")
cv.text_px(W / 2, H - 20,
           "本圖為考卷圖一之向量重繪；原圖僅印出 4 m 一個尺寸，其餘由題幹文字給定。",
           12.5, C["muted"])
cv.save(OUT + "/SM-2019-2-fig-3-profile.svg")

# ══════ fig-4：考卷表一 vs 標準平均壓密度曲線 ══════
W, H = 980, 660
ML, MR, MT_, MB = 150, 150, 92, 190
cv = Canvas(W, H, bg="#FFFFFF")
XL, XR = 0.0, 1.05
PX = lambda t: ML + (t - XL) / (XR - XL) * (W - ML - MR)
PY = lambda u: H - MB - u / 100.0 * (H - MT_ - MB)
for t in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    seg(cv, (PX(t), PY(0)), (PX(t), PY(100)), C["border"], 1.1)
    cv.text_px(PX(t), PY(0) + 19, "%g" % t, 12.5, C["muted"])
for u in range(0, 101, 20):
    seg(cv, (PX(XL), PY(u)), (PX(XR), PY(u)), C["border"], 1.1)
    cv.text_px(PX(XL) - 12, PY(u), "%d" % u, 12.5, C["muted"], anchor="end")
seg(cv, (PX(XL), PY(0)), (PX(XR), PY(0)), C["muted"], 1.9)
seg(cv, (PX(XL), PY(0)), (PX(XL), PY(100)), C["muted"], 1.9)
cv.math_px((PX(XL) + PX(XR)) / 2, PY(0) + 48, "時間因子  T_{v}", 15, C["text"])
cv.text_px(PX(XL) - 74, (PY(0) + PY(100)) / 2, "壓密度（%）", 13.5, C["text"])

xs = [0.005 + i * 1.045 / 400 for i in range(401)]
curve(cv, [(PX(t), PY(U_avg(t) * 100)) for t in xs], C["bmd"], 3.4)
curve(cv, [(PX(t), PY(U_local(t, 1.0) * 100)) for t in xs], C["load"], 3.4)
for t, u in TBL:
    if t <= XR:
        cv.parts.append('<circle cx="%.2f" cy="%.2f" r="5.0" fill="#FFFFFF" stroke="%s" '
                        'stroke-width="2.4"/>' % (PX(t), PY(u), C["load"]))
tag_px(cv, PX(0.50), PY(92), "標準「平均」壓密度 U（課本表）", 13, C["bmd"], anchor="start")
tag_px(cv, PX(0.66), PY(26), "考卷圖二／表一（○＝表上 14 列）", 13, C["load"], anchor="start")

seg(cv, (PX(XL), PY(UREQ * 100)), (PX(TV_TBL), PY(UREQ * 100)), C["accent"], 2.0, "6 5")
for tv, col, lab in [(TV_THY, C["bmd"], "T_v = %.4f → t = %.1f 天" % (TV_THY, T_THY)),
                     (TV_TBL, C["load"], "T_v = %.4f → t = %.1f 天" % (TV_TBL, T_TBL))]:
    seg(cv, (PX(tv), PY(0)), (PX(tv), PY(UREQ * 100)), col, 2.0, "6 5")
    cv.parts.append('<circle cx="%.2f" cy="%.2f" r="7.0" fill="%s" stroke="#FFFFFF" '
                    'stroke-width="2.4"/>' % (PX(tv), PY(UREQ * 100), col))
tag_px(cv, PX(TV_THY) - 12, PY(UREQ * 100) - 30,
       "理論 T_v = %.4f → %.1f 天" % (TV_THY, T_THY), 13, C["bmd"], anchor="end")
tag_px(cv, PX(TV_TBL) + 12, PY(UREQ * 100) + 30,
       "查表一 T_v = %.4f → %.1f 天" % (TV_TBL, T_TBL), 13, C["load"], anchor="start")
tag_px(cv, PX(0.02), PY(UREQ * 100) + 22, "所需 U = 71.02%", 12.5, C["accent"], anchor="start")

cv.text_px(W / 2, 32, "圖 4　考卷「表一」畫的並不是平均壓密度", 17.5, C["text"], weight="700")
cv.text_px(W / 2, 58, "把表一 14 列全部代回理論式：與中央面局部壓密度 U_z(Z=1) 逐列吻合到小數第二位",
           12.5, C["muted"])
cv.text_px(W / 2, H - 140, "U_z = 1 − Σ (2/M) sin(MZ) exp(−M^{2}T_{v})　，　M = (2m+1)π/2　，　Z = z/H_{dr} = 1",
           13.5, C["load"], weight="700")
cv.text_px(W / 2, H - 112, "驗證：T_v = 0.05 → 0.31%（表：0.31）；0.60 → 71.03%（表：71.03）；"
                           "1.50 → 96.86%（表：96.86）", 12.5, C["muted"])
cv.text_px(W / 2, H - 80,
           "攔錯用：同一個 U = 71.02%，在兩條曲線上讀到的 T_v 差 44%，天數差 {:.0f} 天。"
           .format(T_TBL - T_THY), 13.5, C["accent"], weight="700")
cv.text_px(W / 2, H - 52,
           "考卷既然指名「如下圖二與表一」，考場上應以表一為主（300 天），"
           "並敘明理論值 208 天與差異來源。", 13, C["text"], weight="700")
cv.text_px(W / 2, H - 24,
           "若不查表、逕用背下來的 T_v–U 關係，會直接落在綠線上而不自知。", 12.5, C["muted"])
cv.save(OUT + "/SM-2019-2-fig-4-u-tv-table-vs-theory.svg")

# ══════ fig-5：預壓工法為什麼能縮短時間 ══════
W, H = 980, 620
ML, MR, MT_, MB = 150, 170, 92, 200
cv = Canvas(W, H, bg="#FFFFFF")
TMAX, SMAX = 560.0, 0.40
PXt = lambda t: ML + t / TMAX * (W - ML - MR)
PYs = lambda s: MT_ + s / SMAX * (H - MT_ - MB)      # 沉陷向下為正
for t in range(0, int(TMAX) + 1, 100):
    seg(cv, (PXt(t), PYs(0)), (PXt(t), PYs(SMAX)), C["border"], 1.1)
    cv.text_px(PXt(t), PYs(SMAX) + 19, str(t), 12.5, C["muted"])
for s in [0, 0.10, 0.20, 0.30, 0.40]:
    seg(cv, (PXt(0), PYs(s)), (PXt(TMAX), PYs(s)), C["border"], 1.1)
    cv.text_px(PXt(0) - 12, PYs(s), "%d" % (s * 100), 12.5, C["muted"], anchor="end")
seg(cv, (PXt(0), PYs(0)), (PXt(TMAX), PYs(0)), C["muted"], 1.9)
seg(cv, (PXt(0), PYs(0)), (PXt(0), PYs(SMAX)), C["muted"], 1.9)
cv.text_px((PXt(0) + PXt(TMAX)) / 2, PYs(SMAX) + 46, "時間 t（天）", 13.5, C["text"])
cv.text_px(PXt(0) - 76, (PYs(0) + PYs(SMAX)) / 2, "沉陷量 S（cm）", 13.5, C["text"])

ts = [1 + i * TMAX / 400 for i in range(401)]
Uf = lambda t: U_local(CV * t / HDR ** 2, 1.0)       # 依考卷表一所示之曲線
curve(cv, [(PXt(t), PYs(SC * Uf(t))) for t in ts], C["deform"], 3.2)
curve(cv, [(PXt(t), PYs(SCF * Uf(t))) for t in ts], C["load"], 3.6)
for s, col, lab in [(SC, C["deform"], "永久荷重 Δp = 150 kPa，S_∞ = 26.17 cm"),
                    (SCF, C["load"], "預壓荷重 Δp_f = 281 kPa，S_∞ = 36.85 cm")]:
    seg(cv, (PXt(0), PYs(s)), (PXt(TMAX), PYs(s)), col, 1.6, "7 5")
    tag_px(cv, PXt(TMAX) - 6, PYs(s) + (-20 if col == C["deform"] else 22),
           lab, 12.5, col, anchor="end")
seg(cv, (PXt(T_TBL), PYs(0)), (PXt(T_TBL), PYs(SC)), C["accent"], 2.2, "6 5")
cv.parts.append('<circle cx="%.2f" cy="%.2f" r="7.4" fill="%s" stroke="#FFFFFF" '
                'stroke-width="2.4"/>' % (PXt(T_TBL), PYs(SC), C["accent"]))
seg(cv, (PXt(T_TBL), PYs(SC)), (PXt(215), PYs(0.318)), C["accent"], 1.2, "3 3")
tag_px(cv, PXt(60), PYs(0.318),
       "t = {:.0f} 天：預壓曲線在此達到 26.17 cm".format(T_TBL), 13, C["accent"], anchor="start")
tag_px(cv, PXt(60), PYs(0.348),
       "此時預壓本身的壓密度僅 U = 71.0%（尚未壓完）", 12.5, C["muted"],
       anchor="start", weight="400")

cv.text_px(W / 2, 32, "圖 5　預壓工法：用「壓更多、壓一半」換掉「壓剛好、壓到底」", 17.5,
           C["text"], weight="700")
cv.text_px(W / 2, 58, "兩條曲線同形（同一個 c_v、同一個 H_{dr}），只是最終量不同", 12.5, C["muted"])
cv.text_px(W / 2, H - 128,
           "U = S_c / S_{cf} = 26.17 / 36.85 = 71.0%——注意分母是「預壓」的最終沉陷量，不是永久荷重的。",
           13, C["text"], weight="700")
cv.text_px(W / 2, H - 98,
           "攔錯用：若把 U 算成 S_c/S_c = 100%，會去查 T_v→∞，得不到有限的天數。",
           13, C["accent"], weight="700")
cv.text_px(W / 2, H - 66,
           "本圖曲線採考卷圖二／表一所示之關係（見圖 4）；若改用標準平均壓密度，交點提前至 {:.0f} 天。"
           .format(T_THY), 12.5, C["muted"])
cv.text_px(W / 2, H - 36,
           "實務上預壓完成後要卸載，卸載回彈量另計，本題未問。", 12.5, C["muted"])
cv.save(OUT + "/SM-2019-2-fig-5-precompression.svg")

print("Sc=%.5f m  Scf=%.5f m  U=%.5f" % (SC, SCF, UREQ))
print("表一 Tv=%.4f -> t=%.2f 天 ; 理論 Tv=%.4f -> t=%.2f 天" % (TV_TBL, T_TBL, TV_THY, T_THY))
print("表一逐列 vs U_z(Z=1) 檢核：")
for t, u in TBL:
    print("  Tv=%.2f 表=%6.2f  Uz=%6.2f  Uavg=%6.2f" % (t, u, U_local(t)*100, U_avg(t)*100))
