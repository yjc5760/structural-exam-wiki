# -*- coding: utf-8 -*-
"""SM-2003-2 圖解。所有數值取自 SM-2003-2.md §4／§5。"""
import sys, math, os
sys.path.insert(0, "/tmp/sd")
from geo import *
from geo import tag_px

OUT = "/tmp/sd/out/SM-2003-2"
os.makedirs(OUT, exist_ok=True)

# ── 由 SM-2003-2 §4 解得 ────────────────────────────────
GW      = 9.81
DF      = 1.5;  WT = 1.5
Z_SAND  = 5.0;  Z_BOT = 11.0
G_DRY   = 18.5; G_SAT_S = 18.5; G_SAT_C = 18.0
B = L   = 2.0;  Q = 1200.0
ZMID    = Z_SAND + (Z_BOT - Z_SAND) / 2          # 8.0 m
ZP      = ZMID - DF                              # 6.5 m
P0      = G_DRY*DF + (G_SAT_S-GW)*(Z_SAND-DF) + (G_SAT_C-GW)*(ZMID-Z_SAND)   # 82.735
DSIG    = Q / ((B+ZP)*(L+ZP))                    # 16.609
PC      = 90.0
PF      = P0 + DSIG                              # 99.344
E0, CC, CS, HCLAY = 0.8, 0.25, 0.06, 6.0
S1      = CS*HCLAY/(1+E0)*math.log10(PC/P0)
S2      = CC*HCLAY/(1+E0)*math.log10(PF/PC)
SC      = S1 + S2                                # 0.04307 m
SC_WRONG= CC*HCLAY/(1+E0)*math.log10(PF/P0)      # 全程用 Cc
DSIG_TOP= Q/((B+(Z_SAND-DF))**2)                 # 39.67（黏土頂）
DSIG_BOT= Q/((B+(Z_BOT-DF))**2)                  # 9.07（黏土底）
DSIG_BAD= Q/((B+ZMID)**2)                        # 12.00（z 誤從地表起算）

def sv(z):
    if z <= DF:  return G_DRY*z
    if z <= Z_SAND: return G_DRY*DF + G_SAT_S*(z-DF)
    return G_DRY*DF + G_SAT_S*(Z_SAND-DF) + G_SAT_C*(z-Z_SAND)
def uw(z): return max(0.0, GW*(z-WT))

# ══════ fig-1：土層剖面 ＋ 應力深度剖線 ══════
PW, PH = 560, 560
DTOP, DBOT = 0.0, 12.0     # 繪圖深度範圍（模型 y = -深度）

def panel_profile():
    cv = Canvas(PW, PH, **fit(PW, PH, (0, 1), (-DBOT/12.0, 0), 118, 150, 84, 62))
    cv.panel("地層剖面與代表點", "深度向下為正")
    Y = lambda d: -d/12.0
    xa, xb = 0.02, 0.86
    bands = [(0.0, DF, "rgba(180,83,9,0.13)", "乾砂  γ = 18.5", 0.75),
             (DF, Z_SAND, "rgba(180,83,9,0.24)", "飽和砂  γ_{sat} = 18.5", 3.25),
             (Z_SAND, Z_BOT, "rgba(63,74,90,0.22)", "黏土  γ_{sat} = 18.0", 6.3),
             (Z_BOT, DBOT, "rgba(63,74,90,0.42)", "下臥層", 11.5)]
    for d0, d1, col, lab, dlab in bands:
        soil_fill(cv, xa, xb, Y(d1), Y(d0), col)
        cv.line((xa, Y(d1)), (xb, Y(d1)), C["member2"], 1.6)
        cv.text_px(cv.X(xa) + 8, cv.Y(Y(dlab)), lab, 12.5, C["text"], anchor="start")
    cv.line((xa, Y(0)), (xb, Y(0)), C["member"], 2.6)
    # 基礎（置於剖面右半，避開左側層名）
    fx0, fx1 = 0.46, 0.76
    cv.polygon([(fx0, Y(DF)), (fx1, Y(DF)), (fx1, Y(DF-0.55)), (fx0, Y(DF-0.55))],
               "rgba(29,78,216,0.30)", C["deform"], 2.2)
    fc = (fx0 + fx1) / 2
    cv.arrow((fc, Y(-1.5)), (fc, Y(DF-0.62)), C["load"], 3.2, 10)
    cv.math_px(cv.X(fc), cv.Y(Y(-1.8)), "Q = 1200 kN", 14, C["load"], weight="700")
    cv.text_px(cv.X(fc), cv.Y(Y(DF-0.27)), "2 m × 2 m", 12, C["deform"])
    # 地下水位
    cv.line((xa, Y(WT)), (xb, Y(WT)), C["deform"], 1.8, dash="8 5")
    wt_symbol(cv, 0.09, Y(WT), C["deform"], 0.018)
    tag_px(cv, cv.X(xa) + 6, cv.Y(Y(WT)) + 22, "地下水位 GL−1.5 m", 12,
           C["deform"], anchor="start", weight="400")
    # 代表點
    cv.line((xa, Y(ZMID)), (xb, Y(ZMID)), C["accent"], 2.0, dash="7 5")
    cv.dot((fc, Y(ZMID)), 6.0, fill=C["accent"], stroke="#FFFFFF", w=2.0)
    tag_px(cv, cv.X(xb) - 4, cv.Y(Y(ZMID)) + 20, "黏土層中點 z = 8 m", 12.5,
           C["accent"], anchor="end")
    # 尺寸
    cv.dim((xa - 0.10, Y(DF)), (xa - 0.10, Y(0)), "1.5", 0, C["dim"], 12.5, label_off=-24)
    cv.dim((xa - 0.10, Y(Z_SAND)), (xa - 0.10, Y(DF)), "3.5", 0, C["dim"], 12.5, label_off=-24)
    cv.dim((xa - 0.10, Y(Z_BOT)), (xa - 0.10, Y(Z_SAND)), "6.0", 0, C["dim"], 12.5, label_off=-24)
    cv.text_px(cv.X(xa) - 78, cv.Y(Y(11.4)), "（m）", 12, C["muted"])
    return cv


def panel_stress():
    cv = Canvas(PW, PH, **fit(PW, PH, (0, 1), (-1.0, 0), 118, 150, 84, 62))
    cv.panel("垂直應力沿深度的變化", "σ_v（全）、u（水）、σ'_v（有效）")
    SMAX = 220.0
    MX = lambda s_: s_ / SMAX * 0.86
    MY = lambda d: -d / 12.0
    for s_ in (0, 50, 100, 150, 200):
        cv.line((MX(s_), MY(0)), (MX(s_), MY(DBOT)), C["border"], 1.1)
        cv.text_px(cv.X(MX(s_)), cv.Y(MY(DBOT)) + 18, "%d" % s_, 12, C["muted"])
    for d in (0, DF, Z_SAND, ZMID, Z_BOT):
        cv.line((0, MY(d)), (MX(SMAX), MY(d)), C["border"], 1.1)
        cv.text_px(cv.X(0) - 10, cv.Y(MY(d)), "%g" % d, 12, C["muted"], anchor="end")
    cv.line((0, MY(0)), (MX(SMAX), MY(0)), C["muted"], 1.9)
    cv.line((0, MY(0)), (0, MY(DBOT)), C["muted"], 1.9)
    cv.text_px(cv.X(MX(SMAX/2)), cv.Y(MY(DBOT)) + 44, "應力（kPa）", 13, C["text"])
    cv.text_px(cv.X(0) - 54, cv.Y(MY(6)), "深度（m）", 13, C["text"])
    ds = [0, DF, Z_SAND, ZMID, Z_BOT]
    cv.poly([(MX(sv(d)), MY(d)) for d in ds], C["member"], 3.0)
    cv.poly([(MX(uw(d)), MY(d)) for d in ds], C["deform"], 3.0)
    cv.poly([(MX(sv(d)-uw(d)), MY(d)) for d in ds], C["bmd"], 3.4)
    # 圖例放在右上空白區（應力大、深度淺處必為空）
    lx, ly = cv.X(MX(118)), cv.Y(MY(1.0))
    for i, (col, lab) in enumerate([(C["member"], "σ_v　全（總）應力"),
                                    (C["deform"], "u　　孔隙水壓"),
                                    (C["bmd"], "σ'_v　有效應力")]):
        cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                        'stroke-width="3.2"/>' % (lx, ly + i*24, lx + 26, ly + i*24, col))
        cv.text_px(lx + 34, ly + i*24, lab, 12.5, col, anchor="start", weight="700")
    # 代表點
    cv.dot((MX(P0), MY(ZMID)), 6.4, fill="#FFFFFF", stroke=C["accent"], w=3.0)
    tag_px(cv, cv.X(MX(P0)) + 14, cv.Y(MY(ZMID)) + 26,
           "p'_0 = 82.73 kPa", 13, C["accent"], anchor="start")
    # 中點處的三個分量標尺
    cv.line((MX(P0), MY(ZMID)), (MX(sv(ZMID)), MY(ZMID)), C["muted"], 1.4, dash="3 3")
    tag_px(cv, cv.X(MX((P0 + sv(ZMID))/2)), cv.Y(MY(ZMID)) - 22,
           "u = 63.77", 12, C["deform"], weight="400")
    return cv


compose([panel_profile(), panel_stress()],
        title="圖 1　黏土層中點的初始有效應力 p'_0 是怎麼疊出來的",
        sub="水位以上用 γ_dry，水位以下用 γ' = γ_sat − γ_w；三條線的水平間距就是孔隙水壓",
        note="攔錯用：若水位以下仍用 γ_sat 而忘了扣 u，p'_0 會變成 146.5 kPa（已大於 p'_c = 90），"
             "整題會誤判成正常壓密而全程用 C_c。",
        path=OUT + "/SM-2003-2-fig-1-profile-stress.svg")

# ══════ fig-2：2:1 應力分散 ══════
W, H = 940, 620
cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-7.0, 10.6), (-11.9, 1.9), 60, 60, 96, 96))
Y = lambda d: -d
XL, XR = -6.6, 5.9
for d0, d1, col in [(0, DF, "rgba(180,83,9,0.13)"), (DF, Z_SAND, "rgba(180,83,9,0.24)"),
                    (Z_SAND, Z_BOT, "rgba(63,74,90,0.22)")]:
    soil_fill(cv, XL, XR, Y(d1), Y(d0), col)
cv.line((XL, Y(0)), (XR, Y(0)), C["member"], 2.4)
cv.line((XL, Y(Z_SAND)), (XR, Y(Z_SAND)), C["member2"], 1.8)
cv.line((XL, Y(Z_BOT)), (XR, Y(Z_BOT)), C["member2"], 1.8)
cv.text_px(cv.X(XL) + 10, cv.Y(Y(3.2)), "砂土", 13, C["muted"], anchor="start")
cv.text_px(cv.X(XL) + 10, cv.Y(Y(9.6)), "黏土", 13, C["muted"], anchor="start")
# 基礎
cv.polygon([(-1, Y(DF)), (1, Y(DF)), (1, Y(DF - 0.6)), (-1, Y(DF - 0.6))],
           "rgba(29,78,216,0.30)", C["deform"], 2.2)
cv.arrow((0, Y(-1.5)), (0, Y(DF - 0.68)), C["load"], 3.2, 10)
cv.text_px(cv.X(0), cv.Y(Y(-1.75)), "Q = 1200 kN（2 m × 2 m 方形基腳）", 14,
           C["load"], weight="700")
cv.line((-1, Y(DF - 0.95)), (1, Y(DF - 0.95)), C["deform"], 1.2)
for sgn in (-1, 1):
    cv.line((sgn, Y(DF - 0.6)), (sgn, Y(DF - 1.05)), C["deform"], 1.0, dash="3 3")
tag_px(cv, cv.X(-1.25), cv.Y(Y(DF - 0.95)), "B = 2 m", 12.5, C["deform"], anchor="end")
# 2:1 分散錐（水平 1 : 垂直 2）
for sgn in (-1, 1):
    cv.line((sgn * 1, Y(DF)), (sgn * (1 + (Z_BOT - DF) / 2), Y(Z_BOT)), C["accent"], 2.6, dash="9 5")
cv.polygon([(-1, Y(DF)), (1, Y(DF)),
            (1 + (Z_BOT - DF) / 2, Y(Z_BOT)), (-(1 + (Z_BOT - DF) / 2), Y(Z_BOT))],
           "rgba(180,83,9,0.10)")
# 2:1 斜率小三角
tx, ty = 3.05, 2.4
cv.line((tx, Y(ty)), (tx + 1, Y(ty)), C["accent"], 2.0)
cv.line((tx + 1, Y(ty)), (tx + 1, Y(ty + 2)), C["accent"], 2.0)
cv.text_px(cv.X(tx + 0.5), cv.Y(Y(ty)) - 12, "1", 12.5, C["accent"], weight="700")
cv.text_px(cv.X(tx + 1) + 12, cv.Y(Y(ty + 1)), "2", 12.5, C["accent"],
           anchor="start", weight="700")
# 代表點
half = (B + ZP) / 2
cv.line((-half, Y(ZMID)), (half, Y(ZMID)), C["bmd"], 3.0)
cv.dot((0, Y(ZMID)), 6.2, fill=C["bmd"], stroke="#FFFFFF", w=2.0)
cv.dim((-half, Y(ZMID + 0.85)), (half, Y(ZMID + 0.85)), "B + z' = 8.5 m", 0, C["bmd"],
       13.5, label_off=20)
cv.dim((-1.55, Y(DF)), (-1.55, Y(ZMID)), "z' = 6.5 m", 0, C["accent"], 13.5, label_off=-46)
tag_px(cv, cv.X(0), cv.Y(Y(ZMID)) - 22, "Δσ_z = 1200 / 8.5² = 16.61 kPa", 14, C["bmd"])
# 黏土層頂／底的 Δσ（顯示厚層內差異）
for d, val, lab in [(Z_SAND, DSIG_TOP, "黏土頂 Δσ = %.1f kPa" % DSIG_TOP),
                    (Z_BOT, DSIG_BOT, "黏土底 Δσ = %.1f kPa" % DSIG_BOT)]:
    hw = (B + (d - DF)) / 2
    cv.line((-hw, Y(d)), (hw, Y(d)), C["muted"], 2.0, dash="4 4")
    cv.line((hw, Y(d)), (6.4, Y(d)), C["muted"], 1.0, dash="2 3")
    tag_px(cv, cv.X(6.6), cv.Y(Y(d)), lab, 12.5, C["muted"], anchor="start", weight="400")
tag_px(cv, cv.X(6.6), cv.Y(Y(ZMID)), "中點 Δσ = 16.6 kPa", 12.5, C["bmd"],
       anchor="start", weight="700")
cv.text_px(W / 2, 30, "圖 2　2:1 分散法的深度 z' 從「基礎底面」起算，不是從地表", 17.5,
           C["text"], weight="700")
cv.text_px(W / 2, 54, "水平 1 : 垂直 2，作用面積由 B×L 擴大為 (B+z')(L+z')", 12.5, C["muted"])
cv.text_px(W / 2, H - 48,
           "攔錯用：若把 z 誤取為地表起算的 8 m，(2+8)² = 100 m²，Δσ 只剩 {:.2f} kPa，少了 28%。"
           .format(DSIG_BAD), 13, C["load"], weight="700")
cv.text_px(W / 2, H - 22,
           "另注意黏土層厚 6 m 是基礎寬 2 m 的 3 倍，頂底 Δσ 相差 {:.0f} ÷ {:.0f} ≈ 4.4 倍，"
           "取中點只是考試簡化。".format(DSIG_TOP, DSIG_BOT), 12.5, C["muted"])
cv.save(OUT + "/SM-2003-2-fig-2-two-to-one.svg")

# ══════ fig-3：e–log p' 雙段路徑 ══════
W, H = 900, 620
PLO, PHI = 72.0, 118.0
ELO, EHI = 0.7780, 0.8020
LO, HI = math.log10(PLO), math.log10(PHI)
ML, MR, MT, MB = 155, 130, 88, 172
cv = Canvas(W, H, bg="#FFFFFF")
sxp = (W - ML - MR) / (HI - LO)
syp = (H - MT - MB) / (EHI - ELO)
PX = lambda p: ML + (math.log10(p) - LO) * sxp
PY_ = lambda e: H - MB - (e - ELO) * syp
def ln(p0, e0_, p1, e1, col, w, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    cv.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" '
                    'stroke-width="%s" stroke-linecap="round"%s/>'
                    % (PX(p0), PY_(e0_), PX(p1), PY_(e1), col, w, d))

E_PC = E0 - CS * math.log10(PC / P0)
E_PF = E_PC - CC * math.log10(PF / PC)
E_PF_WRONG = E0 - CC * math.log10(PF / P0)

for p in (75, 80, 85, 90, 95, 100, 110):
    cv.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.1"/>'
                    % (PX(p), PY_(ELO), PX(p), PY_(EHI), C["border"]))
    cv.text_px(PX(p), PY_(ELO) + 19, str(p), 12.5, C["muted"])
for e in (0.780, 0.785, 0.790, 0.795, 0.800):
    cv.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.1"/>'
                    % (PX(PLO), PY_(e), PX(PHI), PY_(e), C["border"]))
    cv.text_px(PX(PLO) - 12, PY_(e), "%.3f" % e, 12.5, C["muted"], anchor="end")
cv.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.9"/>'
                % (PX(PLO), PY_(ELO), PX(PHI), PY_(ELO), C["muted"]))
cv.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.9"/>'
                % (PX(PLO), PY_(ELO), PX(PLO), PY_(EHI), C["muted"]))
cv.text_px((PX(PLO) + PX(PHI)) / 2, PY_(ELO) + 48, "有效應力 p'（kPa，對數刻度）", 13.5, C["text"])
cv.text_px(PX(PLO) - 82, (PY_(ELO) + PY_(EHI)) / 2, "孔隙比 e", 13.5, C["text"])

cv.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.6" '
                'stroke-dasharray="4 4"/>' % (PX(PC), PY_(ELO), PX(PC), PY_(E_PC), C["accent"]))
ln(P0, E0, PF, E_PF_WRONG, C["muted"], 2.4, "8 5")     # 全程 Cc（錯誤作法）
ln(P0, E0, PC, E_PC, C["deform"], 4.6)                 # ① 回脹段 Cs
ln(PC, E_PC, PF, E_PF, C["load"], 4.6)                 # ② 壓縮段 Cc
for p, e, lab, ax, dxp, dyp in [
        (P0, E0, "p'_0 = 82.74", "end", -14, -20),
        (PC, E_PC, "p'_c = 90（預壓密應力）", "start", 14, -22),
        (PF, E_PF, "p'_f = 99.34", "start", 16, 22)]:
    cv.parts.append('<circle cx="%.2f" cy="%.2f" r="6.4" fill="#FFFFFF" stroke="%s" '
                    'stroke-width="3"/>' % (PX(p), PY_(e), C["accent"]))
    tag_px(cv, PX(p) + dxp, PY_(e) + dyp, lab, 12.8, C["accent"], anchor=ax)
tag_px(cv, (PX(P0) + PX(PC)) / 2 - 44, PY_((E0 + E_PC) / 2) + 30,
       "① C_s = 0.06（回脹）", 13, C["deform"])
tag_px(cv, (PX(PC) + PX(PF)) / 2 + 74, PY_((E_PC + E_PF) / 2),
       "② C_c = 0.25（處女壓縮）", 13, C["load"])
tag_px(cv, PX(106), PY_(0.7828), "全程用 C_c（錯）", 12.5, C["muted"],
       anchor="middle", weight="400")

cv.text_px(W / 2, 32, "圖 3　最終應力跨過 p'_c，沉陷必須拆成兩段", 17.5, C["text"], weight="700")
cv.text_px(W / 2, 58, "p'_0 ＜ p'_c ＜ p'_f ⇒ 前段走回脹線 C_s，後段才走處女壓縮線 C_c", 12.5, C["muted"])
cv.text_px(W / 2, H - 74, "① %.3f cm  ＋  ② %.3f cm  ＝  S_c = %.2f cm"
           % (S1 * 100, S2 * 100, SC * 100), 15.5, C["text"], weight="700")
cv.text_px(W / 2, H - 46,
           "攔錯用：若不分段、全程用 C_c，得 S_c = {:.2f} cm，高估 {:.0f}%。"
           .format(SC_WRONG * 100, (SC_WRONG / SC - 1) * 100), 13, C["load"], weight="700")
cv.text_px(W / 2, H - 22,
           "反之若誤判為仍在回脹段而全程用 C_s，只得 {:.2f} cm——兩種錯的方向相反。"
           .format(CS * HCLAY / (1 + E0) * math.log10(PF / P0) * 100), 12.5, C["muted"])
cv.save(OUT + "/SM-2003-2-fig-3-e-logp.svg")

print("p0'=%.3f  dsig=%.3f  pf'=%.3f  S1=%.4f S2=%.4f Sc=%.4f m (%.2f cm)"
      % (P0, DSIG, PF, S1, S2, SC, SC*100))
print("Sc全程Cc=%.2f cm ; 全程Cs=%.2f cm ; dsig_top=%.2f bot=%.2f 誤用地表z=%.2f"
      % (SC_WRONG*100, CS*HCLAY/(1+E0)*math.log10(PF/P0)*100, DSIG_TOP, DSIG_BOT, DSIG_BAD))
print("e: e0=%.4f e_pc=%.4f e_pf=%.4f e_pf_wrong=%.4f" % (E0, E_PC, E_PF, E_PF_WRONG))
