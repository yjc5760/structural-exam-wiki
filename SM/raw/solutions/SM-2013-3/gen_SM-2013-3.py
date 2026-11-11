# -*- coding: utf-8 -*-
"""SM-2013-3 圖解。
輸入分兩類：
  (a) 題目給定值（K0、σ_cell、σ_axial）與 §4 讀圖判定的破壞點 —— 取自 SM-2013-3.md §3.5 L1；
  (b) 考卷圖二兩條曲線的取樣點 —— 由掃描圖以像素判讀數位化（格線校準：左圖每 50、右圖每 20 kN/m²，
      ε=0 截距回落在 120 = 400−280，可作為校準檢核）。曲線中段讀值誤差約 ±5 kPa。
所有導出量（Af、φ'、φcu、θ、p-q 座標、u_LE）一律由本檔重算。
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
D, Rad = math.degrees, math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")

# ── L1：題目給定 ────────────────────────────────────────────
K0, S3C, S1C = 0.7, 280.0, 400.0
DEV0 = S1C - S3C                                # 120，圖二左圖 ε=0 的截距
EPS_F, DEV_F, UAC_F = 0.9, 275.0, 125.0         # §4 讀圖判定的破壞點

# ── 圖二數位化取樣（ε%, 值）；破壞點以 §4 判定值為準 ──────────
AC_DEV = [(0.00, 120), (0.10, 150), (0.20, 178), (0.30, 200), (0.40, 220), (0.50, 238),
          (0.60, 253), (0.70, 264), (0.80, 272), (0.90, DEV_F), (1.00, 271), (1.20, 261),
          (1.40, 253), (1.60, 241), (1.80, 230), (2.00, 216), (2.25, 202)]
AC_U   = [(0.00, 0), (0.10, 21), (0.20, 42), (0.30, 62), (0.40, 83), (0.50, 100),
          (0.60, 112), (0.70, 118), (0.80, 123), (0.90, UAC_F), (1.00, 130), (1.20, 138),
          (1.40, 143), (1.60, 146), (1.80, 148), (2.00, 151), (2.20, 153), (2.40, 155)]
def at(tab, e):
    for i in range(len(tab)-1):
        if tab[i][0] <= e <= tab[i+1][0]:
            (x0, y0), (x1, y1) = tab[i], tab[i+1]
            return y0 + (y1-y0)*(e-x0)/(x1-x0)
    return tab[-1][1]

# ── L2：由解題算出 ──────────────────────────────────────────
DDEV_F = DEV_F - DEV0                                   # 155
AF     = UAC_F / DDEV_F                                 # 0.806
S1F_AC, S3F_AC = S3C + DEV_F, S3C                       # 555, 280
S1P, S3P = S1F_AC - UAC_F, S3F_AC - UAC_F               # 430, 155
PHIP   = D(math.asin((S1P-S3P)/(S1P+S3P)))              # 28.04°
PHI_AC = D(math.asin(DEV_F/(S1F_AC+S3F_AC)))            # 19.23°
S1F_LE, S3F_LE = S1C, S1C - DEV_F                       # 400, 125
PHI_LE = D(math.asin(DEV_F/(S1F_LE+S3F_LE)))            # 31.59°
ULE_F  = UAC_F - DDEV_F                                 # -30
THETA  = 45.0 + PHIP/2.0                                # 59.02°
SU     = DEV_F/2.0                                      # 137.5
P0, Q0 = (S1C+S3C)/2.0, DEV0/2.0                        # 340, 60
PF_AC, QF = (S1F_AC+S3F_AC)/2.0, DEV_F/2.0              # 417.5, 137.5
PF_LE     = (S1F_LE+S3F_LE)/2.0                         # 262.5
PPF       = PF_AC - UAC_F                               # 292.5（以 LE 驗算：262.5−(−30)=292.5）
assert abs((PF_LE - ULE_F) - PPF) < 1e-9
def ule(e): return at(AC_U, e) - (at(AC_DEV, e) - DEV0)

# ══════════════════════════════════════════════════════════
# fig-1　考卷圖二的向量重繪：破壞點必須在同一個應變讀取
# ══════════════════════════════════════════════════════════
PW, PH = 700, 600
EXS = 105.0                                  # 1% 應變 = 105 個繪圖單位（兩軸單位不同）

def panel_curve(tab, ymaxv, ystep, ylab, col, title, sub, marky, markname):
    xmin, xmax, ymin, ymax = -0.18*EXS, 2.62*EXS, -0.10*ymaxv, ymaxv*1.06
    L, R, T, B = 68, 40, 68, 96
    sx = min((PW-L-R)/(xmax-xmin), (PH-T-B)/(ymax-ymin))
    cv = Canvas(PW, PH, sx=sx, ox=L-xmin*sx, oy=B-ymin*sx, bg="#FFFFFF")
    cv.panel(title=title, sub=sub)
    for v in range(0, int(ymaxv)+1, ystep):
        cv.line((0, v), (2.55*EXS, v), C["border"], 1.0)
        cv.text_px(cv.X(-0.04*EXS), cv.Y(v), "%d" % v, 11, C["muted"], anchor="end")
    for e10 in range(0, 6):
        e = e10*0.5
        cv.line((e*EXS, 0), (e*EXS, ymaxv), C["border"], 1.0)
        cv.text_px(cv.X(e*EXS), cv.Y(0)+17, "%.1f" % e, 11, C["muted"])
    cv.line((0, 0), (2.55*EXS, 0), C["muted"], 1.6)
    cv.line((0, 0), (0, ymaxv), C["muted"], 1.6)
    cv.text_px(cv.X(1.95*EXS), cv.Y(0)+38, "軸向應變 ε (%)", 12.5, C["muted"], weight="700")
    cv.text_px(cv.X(0.02*EXS), cv.Y(ymaxv)+2, ylab, 12, C["muted"], anchor="start", weight="700")
    cv.poly([(e*EXS, v) for e, v in tab], col, 3.0)
    cv.line((EPS_F*EXS, 0), (EPS_F*EXS, marky), C["accent"], 1.8, dash="5 4")
    cv.line((0, marky), (EPS_F*EXS, marky), C["accent"], 1.8, dash="5 4")
    cv.dot((EPS_F*EXS, marky), 6.2, fill="#FFFFFF", stroke=C["accent"], w=3.0)
    cv.text_px(cv.X(EPS_F*EXS)+12, cv.Y(marky)-16, markname, 12.5, C["accent"],
               anchor="start", weight="700")
    cv.text_px(cv.X(EPS_F*EXS), cv.Y(0)+38, "ε ≈ %.1f%%" % EPS_F, 12, C["accent"], weight="700")
    return cv

left = panel_curve(AC_DEV, 300, 50, "(σ1 − σ3)  (kN/m²)", C["member"],
                   "左圖：應力差 — 應變", "ε = 0 的截距 120 = 400 − 280（K0 壓密的初始應力差）",
                   DEV_F, "峰值 (σ1−σ3)f ≈ %g" % DEV_F)
right = panel_curve(AC_U, 180, 20, "Δu  (kN/m²)", C["deform"],
                    "右圖：孔隙水壓 — 應變", "必須回到左圖的峰值應變讀值，不可讀 ε = 1.0%",
                    UAC_F, "同一應變 Δuf ≈ %g" % UAC_F)
compose([left, right],
        title="SM-2013-3 圖 1　考卷圖二的向量重繪與破壞點判讀",
        sub="Δ(σ1−σ3) = %g − %g = %g ⇒ Af = %g / %g = %.3f" % (DEV_F, DEV0, DDEV_F, UAC_F, DDEV_F, AF),
        note="曲線取樣點由掃描圖數位化（中段誤差約 ±5 kPa）；破壞點與其後所有導出量由 §4 判定值算出。",
        cols=2, path=os.path.join(OUT, "SM-2013-3-fig-1-chart-reading.svg"))

# ══════════════════════════════════════════════════════════
# fig-2　p–q 應力路徑：兩條 TSP、一條共用 ESP
# ══════════════════════════════════════════════════════════
W2, H2 = 1120, 660
xmin, xmax, ymin, ymax = 225.0, 470.0, 20.0, 195.0
L, R, T, B = 62, 296, 74, 90
sx = min((W2-L-R)/(xmax-xmin), (H2-T-B)/(ymax-ymin))
cv = Canvas(W2, H2, sx=sx, ox=L-xmin*sx, oy=B-ymin*sx, bg="#FFFFFF")
cv.panel(title="SM-2013-3 圖 2　AC 與 LE 的總應力路徑與（共用的）有效應力路徑",
         sub="p = (σ1+σ3)/2、q = (σ1−σ3)/2；p' = p − u")
for v in range(240, 461, 40):
    cv.line((v, ymin+4), (v, ymax-8), C["border"], 1.0)
    cv.text_px(cv.X(v), cv.Y(ymin+4)+17, "%d" % v, 11, C["muted"])
for v in range(40, 181, 20):
    cv.line((xmin+3, v), (xmax-4, v), C["border"], 1.0)
    cv.text_px(cv.X(xmin+3)-8, cv.Y(v), "%d" % v, 11, C["muted"], anchor="end")
cv.text_px(cv.X(347), cv.Y(ymin+4)+38, "p 或 p'  (kN/m²)", 12.5, C["muted"], weight="700")
cv.text_px(cv.X(xmin+6), cv.Y(ymax-10), "q (kN/m²)", 12.5, C["muted"], anchor="start", weight="700")
# Kf 線（過原點）
for sl, col, lab in ((math.sin(Rad(PHIP)), C["load"], "有效 Kf 線  q = p' sinφ'"),
                     (math.sin(Rad(PHI_AC)), C["member2"], "AC 總應力 Kf 線"),
                     (math.sin(Rad(PHI_LE)), C["bmd"], "LE 總應力 Kf 線")):
    x1 = min(xmax-6, (ymax-12)/sl)
    cv.line((xmin+4, (xmin+4)*sl), (x1, x1*sl), col, 2.2, dash="9 6")
    cv.text_px(cv.X(x1)-6, cv.Y(x1*sl)-12 - (0 if "有效" in lab else 20), lab, 12, col,
               anchor="end", weight="700")
# TSP
cv.line((P0, Q0), (PF_AC, QF), C["member"], 3.0)
cv.line((P0, Q0), (PF_LE, QF), C["member"], 3.0)
cv.text_px(cv.X((P0+PF_AC)/2.0)+6, cv.Y((Q0+QF)/2.0)+16, "AC 的 TSP（斜率 +1）", 12.5,
           C["member"], anchor="start", weight="700")
cv.text_px(cv.X((P0+PF_LE)/2.0)-6, cv.Y((Q0+QF)/2.0)+16, "LE 的 TSP（斜率 −1）", 12.5,
           C["member"], anchor="end", weight="700")
# ESP（由數位化資料逐點算出）
esp = []
for i in range(0, 91):
    e = EPS_F*i/90.0
    dev, uu = at(AC_DEV, e), at(AC_U, e)
    esp.append((P0 + (dev-DEV0)/2.0 - uu, dev/2.0))
cv.poly(esp, C["load"], 3.4)
cv.text_px(cv.X(esp[45][0])-10, cv.Y(esp[45][1]), "ESP（AC 與 LE 共用）", 12.5, C["load"],
           anchor="end", weight="700")
for p, q, col, lab in ((P0, Q0, C["accent"], "起點 (%g, %g)" % (P0, Q0)),
                       (PF_AC, QF, C["member"], "AC 破壞 (%.1f, %.1f)" % (PF_AC, QF)),
                       (PF_LE, QF, C["member"], "LE 破壞 (%.1f, %.1f)  " % (PF_LE, QF)),
                       (PPF, QF, C["load"], "共同有效破壞點 (%.1f, %.1f)" % (PPF, QF))):
    cv.dot((p, q), 6.2, fill="#FFFFFF", stroke=col, w=3.0)
    dy = 20 if q == Q0 else (-38 if p == PF_LE else -16)
    cv.text_px(cv.X(p), cv.Y(q)+dy, lab, 12, col, weight="700")
cv.line((PPF, QF), (PF_AC, QF), C["accent"], 1.6, dash="4 3")
cv.line((PF_LE, QF), (PPF, QF), C["accent"], 1.6, dash="4 3")
rows = [("兩條 TSP 從同一起點往相反方向走，", C["text"], "400"),
        ("卻在同一個 q = %.1f 破壞、" % QF, C["text"], "400"),
        ("扣掉各自的 u 之後落在同一個 p'：", C["text"], "700"),
        ("", C["muted"], "400"),
        ("AC： %.1f − (+%g) = %.1f" % (PF_AC, UAC_F, PPF), C["load"], "700"),
        ("LE： %.1f − (%g) = %.1f" % (PF_LE, ULE_F, PPF), C["load"], "700"),
        ("", C["muted"], "400"),
        ("這就是「ESP 唯一」的具體驗證，", C["muted"], "400"),
        ("也是本題能由 AC 推出 LE 的唯一依據。", C["muted"], "400"),
        ("", C["muted"], "400"),
        ("φ' = %.2f°（唯一）" % PHIP, C["load"], "700"),
        ("φcu：AC %.2f° vs LE %.2f°" % (PHI_AC, PHI_LE), C["bmd"], "700"),
        ("⇒ 總應力參數不是土壤性質。", C["text"], "700")]
for i, (t, col, wt) in enumerate(rows):
    if t: cv.text_px(W2-R+14, 120+i*25, t, 12.5, col, anchor="start", weight=wt)
cv.save(os.path.join(OUT, "SM-2013-3-fig-2-stress-paths.svg"))

# ══════════════════════════════════════════════════════════
# fig-3　(二) LE 試驗的孔隙水壓對應變圖
# ══════════════════════════════════════════════════════════
W3, H3 = 1060, 620
EXS3 = 150.0
xmin, xmax, ymin, ymax = -0.14*EXS3, 1.12*EXS3, -60.0, 160.0
L, R, T, B = 74, 320, 74, 90
sx = min((W3-L-R)/(xmax-xmin), (H3-T-B)/(ymax-ymin))
cv = Canvas(W3, H3, sx=sx, ox=L-xmin*sx, oy=B-ymin*sx, bg="#FFFFFF")
cv.panel(title="SM-2013-3 圖 3　(二) LE 試驗的孔隙水壓對應變",
         sub="u_LE = u_AC − Δ(σ1−σ3) = (A − 1)·Δ(σ1−σ3)；A ＜ 1 ⇒ u_LE 全程為負")
for v in range(-60, 161, 20):
    cv.line((0, v), (1.05*EXS3, v), C["border"], 1.0)
    cv.text_px(cv.X(-0.03*EXS3), cv.Y(v), "%d" % v, 11, C["muted"], anchor="end")
for e in (0.0, 0.25, 0.5, 0.75, 1.0):
    cv.line((e*EXS3, -60), (e*EXS3, 160), C["border"], 1.0)
    cv.text_px(cv.X(e*EXS3), cv.Y(-60)+17, "%.2f" % e, 11, C["muted"])
cv.line((0, 0), (1.05*EXS3, 0), C["member"], 2.0)
cv.line((0, -60), (0, 155), C["muted"], 1.6)
cv.text_px(cv.X(0.5*EXS3), cv.Y(-60)+38, "軸向應變 ε (%)", 12.5, C["muted"], weight="700")
cv.text_px(cv.X(0.02*EXS3), cv.Y(152), "孔隙水壓 u (kN/m²)", 12, C["muted"], anchor="start", weight="700")
es = [i*EPS_F/90.0 for i in range(91)]
cv.poly([(e*EXS3, at(AC_U, e)) for e in es], C["deform"], 3.0)
cv.poly([(e*EXS3, ule(e)) for e in es], C["load"], 3.4)
cv.text_px(cv.X(0.40*EXS3), cv.Y(at(AC_U, 0.40))+24, "AC（正孔壓）", 12.5, C["deform"], weight="700")
cv.text_px(cv.X(0.62*EXS3), cv.Y(ule(0.62))+20, "LE（負孔壓／吸力）", 12.5, C["load"], weight="700")
for e in (0.25, 0.50, 0.75, EPS_F):
    cv.dot((e*EXS3, ule(e)), 5.4, fill="#FFFFFF", stroke=C["load"], w=2.6)
cv.dot((EPS_F*EXS3, ULE_F), 6.6, fill="#FFFFFF", stroke=C["accent"], w=3.2)
cv.text_px(cv.X(EPS_F*EXS3)+10, cv.Y(ULE_F), "破壞時 %g" % ULE_F, 12.5, C["accent"],
           anchor="start", weight="700")
cv.dot((EPS_F*EXS3, UAC_F), 6.6, fill="#FFFFFF", stroke=C["accent"], w=3.2)
cv.text_px(cv.X(EPS_F*EXS3)+10, cv.Y(UAC_F), "破壞時 %g" % UAC_F, 12.5, C["accent"],
           anchor="start", weight="700")
rows = [("ε (%)　(σ1−σ3)　Δ(σ1−σ3)　u_AC　u_LE", C["text"], "700")]
for e in (0.0, 0.25, 0.5, 0.75, EPS_F):
    dev = at(AC_DEV, e)
    rows.append(("%.2f　　%5.0f　　%5.0f　　%4.0f　　%+.0f"
                 % (e, dev, dev-DEV0, at(AC_U, e), ule(e)),
                 C["accent"] if e == EPS_F else C["muted"], "700" if e == EPS_F else "400"))
rows += [("", C["muted"], "400"),
         ("A = u_AC / Δ(σ1−σ3) 全程在 0.74～0.85", C["text"], "400"),
         ("之間，恆小於 1 ⇒ u_LE = (A−1)·Δ(σ1−σ3)", C["text"], "400"),
         ("從一開始就是負的，不會先升到正值。", C["load"], "700"),
         ("", C["muted"], "400"),
         ("物理意義：LE 是側向解壓，土體想膨脹，", C["muted"], "400"),
         ("不排水不許它膨脹 ⇒ 孔隙水被拉出吸力。", C["muted"], "400")]
for i, (t, col, wt) in enumerate(rows):
    if t: cv.text_px(W3-R+14, 118+i*24, t, 12, col, anchor="start", weight=wt)
cv.save(os.path.join(OUT, "SM-2013-3-fig-3-le-pore-pressure.svg"))
print("Af=%.4f phi'=%.3f phiAC=%.3f phiLE=%.3f theta=%.3f Su=%.1f uLE=%g p'f=%.1f"
      % (AF, PHIP, PHI_AC, PHI_LE, THETA, SU, ULE_F, PPF))
for e in (0.25, 0.5, 0.75, 0.9): print(" eps=%.2f dev=%.0f uAC=%.0f uLE=%.0f" % (e, at(AC_DEV,e), at(AC_U,e), ule(e)))
