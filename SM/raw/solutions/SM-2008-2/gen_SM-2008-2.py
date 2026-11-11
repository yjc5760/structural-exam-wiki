# -*- coding: utf-8 -*-
"""SM-2008-2 圖解。所有數值由本檔依 SM-2008-2.md §3.5 的 L1 輸入重算，非硬寫座標。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
D, Rad = math.degrees, math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")

# ── L1（§3.5）───────────────────────────────────────────────
GS, E, S, GW = 2.66, 0.7, 0.5, 9.81
GSAT_C, ZSAND, ZA, PHI, K0, AF = 19.0, 2.0, 3.5, 30.0, 0.5, 0.7
DIA = 10.0
# ── L2（§4）────────────────────────────────────────────────
GSAND = (GS + S*E)/(1+E) * GW                 # 17.3695
SV0   = GSAND*ZSAND + GSAT_C*ZA               # 101.239
U0    = GW*ZA                                 # 34.335
SVP0  = SV0 - U0                              # 66.904
SHP0  = K0*SVP0                               # 33.452
KP    = (1+math.sin(Rad(PHI)))/(1-math.sin(Rad(PHI)))     # 3.0
def dq_of(af): return 3.0*(KP*K0 - 1.0)*SVP0/(1.0 - af + KP*af)
DQ    = dq_of(AF)                             # 41.815
H     = DQ/GW                                 # 4.262
DU    = (1+AF)/3.0*DQ                         # 23.695
S1F   = SVP0 + (1-AF)/3.0*DQ                  # 71.085
S3F   = SHP0 - AF/3.0*DQ                      # 23.695

# ══════════════════════════════════════════════════════════
# fig-1　剖面與 A 點初始有效應力
# ══════════════════════════════════════════════════════════
PW, PH = 700, 660

def panel_profile():
    """全部用公尺為單位（兩軸同尺度），儲水槽高度以水深 H 的實際比例畫。"""
    HT = H                                     # 儲水槽水深＝解出的破壞水位
    xmin, xmax, ymin, ymax = -0.8, 12.8, -7.6, HT + 1.9
    L, R, T, B = 46, 40, 66, 108
    sx = min((PW-L-R)/(xmax-xmin), (PH-T-B)/(ymax-ymin))
    cv = Canvas(PW, PH, sx=sx, ox=L-xmin*sx, oy=B-ymin*sx, bg="#FFFFFF")
    cv.panel(title="題目剖面與 A 點初始應力",
             sub="A 點在地表下 %g m（砂土 %g ＋ 黏土 %g）" % (ZSAND+ZA, ZSAND, ZA))
    cv.polygon([(0.4, 0), (11.6, 0), (11.6, -ZSAND), (0.4, -ZSAND)],
               "rgba(180,83,9,0.14)", C["accent"], 1.6)
    cv.polygon([(0.4, -ZSAND), (11.6, -ZSAND), (11.6, -7.0), (0.4, -7.0)],
               "rgba(63,74,90,0.12)", C["member"], 1.6)
    cv.text_px(cv.X(1.05), cv.Y(-0.75), "砂土  S = 50%、e = 0.7、Gs = 2.66", 12, C["accent"],
               anchor="start", weight="700")
    cv.text_px(cv.X(1.05), cv.Y(-1.30), "γ = (Gs+S·e)/(1+e)·γw = %.2f kN/m³" % GSAND, 11.5,
               C["muted"], anchor="start")
    cv.text_px(cv.X(0.7), cv.Y(-6.15), "黏土  γsat = %g、c' = 0、φ' = %g°" % (GSAT_C, PHI), 12,
               C["member"], anchor="start", weight="700")
    cv.text_px(cv.X(0.7), cv.Y(-6.65), "K0 = %g、Af = %g" % (K0, AF), 12, C["member"], anchor="start")
    cv.line((0.4, -7.0), (11.6, -7.0), C["member"], 3.2)
    cv.text_px(cv.X(6.0), cv.Y(-7.0)+18, "透水性良好之岩盤", 11.5, C["muted"])
    cv.line((0.1, -ZSAND), (11.9, -ZSAND), C["deform"], 1.8, dash="7 5")
    cv.text_px(cv.X(11.6), cv.Y(-ZSAND)-11, "地下水位（地表下 2 m）", 11.5, C["deform"], anchor="end")
    cv.polygon([(3.5, 0), (8.5, 0), (8.5, HT), (3.5, HT)], "rgba(29,78,216,0.12)", C["deform"], 2.2)
    cv.text_px(cv.X(6.0), cv.Y(HT/2.0), "儲水槽  D = %g m" % DIA, 12, C["deform"], weight="700")
    cv.double_arrow((9.3, 0.0), (9.3, HT), C["deform"], 2.0, 8)
    cv.text_px(cv.X(9.5), cv.Y(HT/2.0), "H", 13.5, C["deform"], anchor="start", weight="700")
    cv.text_px(cv.X(6.0), cv.Y(HT + 0.85), "Δq = γw · H", 12.5, C["deform"], weight="700")
    cv.dot((6.0, -(ZSAND+ZA)), 6.0, fill=C["load"])
    cv.text_px(cv.X(6.3), cv.Y(-(ZSAND+ZA)), "A 點", 12.5, C["load"], anchor="start", weight="700")
    cv.line((0.4, -(ZSAND+ZA)), (11.6, -(ZSAND+ZA)), C["load"], 1.4, dash="4 3")
    cv.dim((0.4, 0), (0.4, -ZSAND), "2 m", off=-34, color=C["dim"], size=11.5)
    cv.dim((11.6, -ZSAND), (11.6, -7.0), "5 m", off=22, color=C["dim"], size=11.5)
    rows = ["σv0 = %.2f×2 + %g×3.5 = %.2f　　u0 = 9.81×3.5 = %.2f" % (GSAND, GSAT_C, SV0, U0),
            "σv0' = %.2f      σh0' = K0·σv0' = %.2f" % (SVP0, SHP0),
            "檢核：σv0'/σh0' = 2.00 ＜ Kp = 3.00 ⇒ 蓄水前未破壞"]
    for i, t in enumerate(rows):
        cv.text_px(PW/2, PH - 84 + i*22, t, 12.5, C["text"] if i else C["muted"],
                   weight="700" if i else "400")
    return cv

def panel_paths():
    xmin, xmax, ymin, ymax = -3.0, 64.0, -6.0, 86.0
    L, R, T, B = 62, 46, 70, 138
    sx = min((PW-L-R)/(xmax-xmin), (PH-T-B)/(ymax-ymin))
    cv = Canvas(PW, PH, sx=sx, ox=L-xmin*sx, oy=B-ymin*sx, bg="#FFFFFF")
    cv.panel(title="兩個有效應力隨 Δq 的走向", sub="垂直向幾乎不動，水平向被超額水壓吃掉")
    cv.line((0, 0), (xmax-3, 0), C["muted"], 1.6)
    cv.line((0, 0), (0, ymax-4), C["muted"], 1.6)
    cv.text_px(cv.X(30), cv.Y(0)+40, "水槽荷重增量  Δq (kN/m²)", 12.5, C["muted"], weight="700")
    cv.text_px(cv.X(0)+6, cv.Y(ymax-4)+2, "有效應力 (kN/m²)", 11.5, C["muted"], anchor="start")
    for q in range(0, 61, 20):
        cv.line((q, 0), (q, -2.5), C["muted"], 1.2)
        cv.text_px(cv.X(q), cv.Y(0)+16, "%d" % q, 11.5, C["muted"])
    for v in (20, 40, 60, 80):
        cv.line((0, v), (-1.6, v), C["muted"], 1.2)
        cv.text_px(cv.X(-2.4), cv.Y(v), "%d" % v, 11.5, C["muted"], anchor="end")
    qs = [i*0.5 for i in range(0, 121)]
    fv = lambda q: SVP0 + (1-AF)/3.0*q
    fh = lambda q: SHP0 - AF/3.0*q
    cv.poly([(q, fv(q)) for q in qs], C["load"], 3.0)
    cv.poly([(q, fh(q)) for q in qs], C["deform"], 3.0)
    cv.poly([(q, fv(q)/KP) for q in qs], C["bmd"], 2.2, dash="7 5")
    cv.text_px(cv.X(34), cv.Y(fv(34))+22, "σv'（垂直有效）", 12.5, C["load"], weight="700")
    cv.text_px(cv.X(12), cv.Y(fh(12))-15, "σh'（水平有效）", 12.5, C["deform"], weight="700")
    cv.text_px(cv.X(12), cv.Y(fv(12)/KP)+18, "破壞門檻 σv'/Kp", 12, C["bmd"], weight="700")
    cv.dot((DQ, fh(DQ)), 6.4, fill="#FFFFFF", stroke=C["accent"], w=3.0)
    cv.line((DQ, 0), (DQ, fv(DQ)), C["accent"], 1.6, dash="5 4")
    cv.text_px(cv.X(DQ)+8, cv.Y(fv(DQ))+18, "Δq = %.2f" % DQ, 12.5, C["accent"],
               anchor="start", weight="700")
    cv.text_px(cv.X(DQ)+10, cv.Y(fh(DQ))-16, "兩線相交 ⇒ 破壞", 12.5, C["accent"],
               anchor="start", weight="700")
    rows = [("破壞時 σv' = %.2f（比初始 %.2f 還高）" % (S1F, SVP0), C["load"], "400"),
            ("破壞時 σh' = %.2f（比初始 %.2f 掉了 29%%）" % (S3F, SHP0), C["deform"], "400"),
            ("Δu = (1+Af)/3 · Δq = %.3f Δq ＞ Δσh = Δq/3" % ((1+AF)/3.0), C["text"], "700"),
            ("⇒ 破壞是「圍壓被抽掉」，不是被垂直向壓垮", C["text"], "700"),
            ("H = Δq / γw = %.2f / 9.81 = %.2f m" % (DQ, H), C["accent"], "700")]
    for i, (t, col, wt) in enumerate(rows):
        cv.text_px(PW/2, PH - 118 + i*22, t, 12.5, col, weight=wt)
    return cv

compose([panel_profile(), panel_paths()],
        title="SM-2008-2 圖 1　A 點的初始應力，以及蓄水過程中兩個有效應力的走向",
        sub="γsand = %.2f、σv0' = %.2f、σh0' = %.2f ⇒ Δq = %.2f kN/m²、H = %.2f m" % (GSAND, SVP0, SHP0, DQ, H),
        note="右圖三條線都是 Δq 的一次函數，交點即破壞；係數 (1−Af)/3 與 −Af/3 由 Skempton 公式導出。",
        cols=2, path=os.path.join(OUT, "SM-2008-2-fig-1-profile-paths.svg"))

# ══════════════════════════════════════════════════════════
# fig-2　Af 敏感度：破壞水位 H 對 Af 的依賴
# ══════════════════════════════════════════════════════════
W2, H2 = 1020, 600
AXS = 9.0                                   # 1.0 的 Af 對應 9 個繪圖單位（兩軸單位不同）
def AX(a): return a * AXS
xmin, xmax, ymin, ymax = AX(-0.06), AX(1.14), -0.9, 9.6
L, R, T, B = 78, 300, 86, 78
sx = min((W2-L-R)/(xmax-xmin), (H2-T-B)/(ymax-ymin))
cv = Canvas(W2, H2, sx=sx, ox=L-xmin*sx, oy=B-ymin*sx, bg="#FFFFFF")
cv.panel(title="SM-2008-2 圖 2　破壞水位 H 對孔隙水壓參數 Af 的敏感度",
         sub="H = Δq/γw，Δq = 3(Kp·K0 − 1)σv0' / (1 − Af + Kp·Af)")
cv.line((AX(0), 0), (AX(1.09), 0), C["muted"], 1.6)
cv.line((AX(0), 0), (AX(0), 9.2), C["muted"], 1.6)
for a in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    cv.line((AX(a), 0), (AX(a), -0.18), C["muted"], 1.2)
    cv.text_px(cv.X(AX(a)), cv.Y(0)+18, "%.1f" % a, 12, C["muted"])
for v in range(0, 10, 2):
    cv.line((AX(0), v), (AX(-0.014), v), C["muted"], 1.2)
    cv.text_px(cv.X(AX(-0.022)), cv.Y(v), "%d" % v, 12, C["muted"], anchor="end")
cv.text_px(cv.X(AX(0.55)), cv.Y(0)+42, "破壞時孔隙水壓參數  Af", 13, C["muted"], weight="700")
cv.text_px(cv.X(AX(-0.055)), cv.Y(9.5), "H (m)", 13, C["muted"], anchor="start", weight="700")
cv.poly([(AX(a/200.0), dq_of(a/200.0)/GW) for a in range(0, 209)], C["load"], 3.0)
for a in (0.3, 0.5, AF, 1.0):
    hh = dq_of(a)/GW
    cv.dot((AX(a), hh), 5.8, fill="#FFFFFF" if a == AF else C["load"],
           stroke=C["accent"] if a == AF else C["load"], w=3.0 if a == AF else 1.6)
    cv.text_px(cv.X(AX(a)), cv.Y(hh)-17, "%.2f m" % hh, 12.5,
               C["accent"] if a == AF else C["muted"], weight="700")
cv.line((AX(AF), 0), (AX(AF), dq_of(AF)/GW), C["accent"], 1.6, dash="5 4")
cv.text_px(cv.X(AX(AF)), cv.Y(0)+64, "本題 Af = 0.7", 12.5, C["accent"], weight="700")
rows = [("Af 越大 ⇒ 同樣的 Δq 生出越多超額水壓", C["text"], "700"),
        ("⇒ 水平有效應力掉得越快 ⇒ 越早破壞。", C["text"], "400"),
        ("", C["muted"], "400"),
        ("Af = 0.3 → H = %.2f m" % (dq_of(0.3)/GW), C["muted"], "400"),
        ("Af = 0.5 → H = %.2f m" % (dq_of(0.5)/GW), C["muted"], "400"),
        ("Af = 0.7 → H = %.2f m（本題）" % (dq_of(0.7)/GW), C["accent"], "700"),
        ("Af = 1.0 → H = %.2f m" % (dq_of(1.0)/GW), C["muted"], "400"),
        ("", C["muted"], "400"),
        ("Af 由 0.3 升到 1.0，容許水位幾乎腰斬。", C["load"], "700"),
        ("實務上 Af 必須由三軸試驗實測，", C["muted"], "400"),
        ("不可憑經驗表硬套。", C["muted"], "400")]
for i, (t, col, wt) in enumerate(rows):
    if t: cv.text_px(W2-R+14, 150+i*25, t, 12.5, col, anchor="start", weight=wt)
cv.save(os.path.join(OUT, "SM-2008-2-fig-2-af-sensitivity.svg"))
print("gsand=%.4f svp0=%.3f shp0=%.3f dq=%.4f H=%.4f du=%.3f s1f=%.3f s3f=%.3f ratio=%.4f"
      % (GSAND, SVP0, SHP0, DQ, H, DU, S1F, S3F, S1F/S3F))
