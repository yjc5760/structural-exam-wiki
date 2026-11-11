# -*- coding: utf-8 -*-
"""SM-2024-1 圖解。所有數值由本檔依 SM-2024-1.md §3.5 的 L1 輸入重算，非硬寫座標。
執行：STRUCTDRAW=<struct-diagram/scripts> python3 gen_SM-2024-1.py
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "figs")

# ── L1：題目給定（§3.5）──────────────────────────────────────────
S3, DSD, CC = 100.0, 240.0, 25.0
S3B         = 200.0                                       # (四) 的新圍壓

# ── L2：由解題算出（§4）─────────────────────────────────────────
S1   = S3 + DSD                                           # 340
CEN  = (S1 + S3) / 2.0                                    # 220
RAD  = (S1 - S3) / 2.0                                    # 120
Y    = (-2*CC + math.sqrt(4*CC*CC + 4*S3*S1)) / (2*S3)    # tan(45°+φ'/2)
PHI  = 2.0 * (math.degrees(math.atan(Y)) - 45.0)          # 26.33°
KP   = Y * Y
SFF  = CEN - RAD * math.sin(math.radians(PHI))            # 166.77
TFF  = RAD * math.cos(math.radians(PHI))                  # 107.55
TH   = 45.0 + PHI / 2.0                                   # 58.17°
S1B  = S3B * KP + 2 * CC * Y                              # 599.46
DSDB = S1B - S3B                                          # 399.46
DSD_WRONG = DSD * S3B / S3                                # 480（比例外推，錯）
CENB, RADB = (S1B + S3B)/2.0, (S1B - S3B)/2.0
X0   = -CC / math.tan(math.radians(PHI))                  # 包絡線與 σ 軸交點
def env(x): return CC + x * math.tan(math.radians(PHI))

# ══════════════════════════════════════════════════════════════
# fig-1　破壞莫爾圓與切點（左）／試體破壞面與 (二) 證明（右）
# ══════════════════════════════════════════════════════════════
PW, PH = 680, 660

def panel_mohr():
    xmin, xmax, ymin, ymax = -85.0, 400.0, -160.0, 205.0
    L, R, T, B = 62, 34, 62, 40
    sx = min((PW-L-R)/(xmax-xmin), (PH-T-B)/(ymax-ymin))
    cv = Canvas(PW, PH, sx=sx, ox=L-xmin*sx, oy=B-ymin*sx, bg="#FFFFFF")
    cv.panel(title="(一)(三) 破壞莫爾圓與切點",
             sub="圓心 C = %g、半徑 R = %g；切點即破壞面上的應力狀態" % (CEN, RAD))
    a = math.radians(PHI)
    cv.line((xmin+6, 0), (xmax-4, 0), C["muted"], 1.6)
    cv.line((0, ymin+6), (0, ymax-6), C["muted"], 1.6)
    cv.math_px(cv.X(xmax-4)-2, cv.Y(0)+20, "σ (kPa)", 13, C["muted"], anchor="end")
    cv.math_px(cv.X(0)+8, cv.Y(ymax-6)+3, "τ (kPa)", 13, C["muted"], anchor="start")
    # 包絡線
    cv.line((X0, 0), (xmax-8, env(xmax-8)), C["load"], 2.6)
    cv.text_px(cv.X(300), cv.Y(env(300))-50, "破壞包絡線", 13, C["load"], weight="700")
    cv.math_px(cv.X(300), cv.Y(env(300))-30, "τ = c' + σ tanφ'", 13, C["load"])
    # c' 截距與 φ'
    cv.line((0, 0), (0, CC), C["load"], 2.2)
    cv.math_px(cv.X(0)-10, cv.Y(CC)+16, "c' = %g" % CC, 13, C["load"], anchor="end", weight="700")
    cv.line((X0, 0), (X0+130, 0), C["muted"], 1.4, dash="3 3")
    cv.poly([(X0+58*math.cos(t*a/24), 58*math.sin(t*a/24)) for t in range(25)], C["load"], 1.8)
    cv.math_px(cv.X(X0+66), cv.Y(-26), "φ' = %.2f°" % PHI, 13.5, C["load"], anchor="start", weight="700")
    # 莫爾圓
    cv.circle((CEN, 0), RAD, fill="rgba(29,78,216,0.10)", stroke=C["deform"], w=2.8)
    cv.dot((CEN, 0), 4.2, fill=C["deform"])
    cv.math_px(cv.X(CEN), cv.Y(0)+19, "C = %g" % CEN, 13, C["deform"])
    for v, lab in ((S3, "σ_{3}' = %g" % S3), (S1, "σ_{1}' = %g" % S1)):
        cv.dot((v, 0), 4.6, fill=C["member"])
        cv.math_px(cv.X(v), cv.Y(0)+40, lab, 13.5, C["member"], weight="700")
    cv.dim((S3, -RAD-30/sx), (S1, -RAD-30/sx), "Δσ_d = %g" % DSD, off=0, color=C["dim"], size=13)
    cv.line((CEN, 0), (CEN, RAD), C["deform"], 1.8, dash="5 4")
    cv.math_px(cv.X(CEN)+8, cv.Y(RAD*0.42), "R = %g" % RAD, 13, C["deform"], anchor="start")
    # 2θ 圓心角（弧畫小一點，標籤放圓內偏下，避開 R 標籤）
    a2 = math.radians(90.0 + PHI)
    cv.poly([(CEN + 62*math.cos(t*a2/30), 62*math.sin(t*a2/30)) for t in range(31)], C["bmd"], 2.0)
    cv.math_px(cv.X(CEN), cv.Y(-74), "2θ = 90° + φ' = %.2f°" % (90+PHI), 13, C["bmd"], weight="700")
    # 切點 F
    cv.line((CEN, 0), (SFF, TFF), C["accent"], 2.4)
    cv.dot((SFF, TFF), 5.6, fill="#FFFFFF", stroke=C["accent"], w=3.0)
    cv.text_px(cv.X(SFF)-4, cv.Y(TFF)-52, "切點 F ＝ 破壞面", 13, C["accent"], anchor="end", weight="700")
    cv.math_px(cv.X(SFF)-4, cv.Y(TFF)-34, "(%.2f, %.2f)" % (SFF, TFF), 12.5, C["accent"], anchor="end")
    u = (math.cos(a), math.sin(a)); v = (-math.sin(a), math.cos(a)); d = 14.0/sx
    cv.poly([(SFF+d*u[0], TFF+d*u[1]), (SFF+d*(u[0]-v[0]), TFF+d*(u[1]-v[1])), (SFF-d*v[0], TFF-d*v[1])],
            C["muted"], 1.5)
    cv.line((SFF, 0), (SFF, TFF), C["accent"], 1.5, dash="4 3")
    cv.line((0, TFF), (SFF, TFF), C["accent"], 1.5, dash="4 3")
    cv.math_px(cv.X(SFF)-6, cv.Y(34), "σ_{ff} = %.2f" % SFF, 12.5, C["accent"], anchor="end", weight="700")
    cv.math_px(cv.X(0)+8, cv.Y(TFF)-13, "τ_{ff} = %.2f" % TFF, 12.5, C["accent"], anchor="start", weight="700")
    return cv

def panel_specimen():
    xmin, xmax, ymin, ymax = -1.35, 1.35, -1.35, 1.35
    L, R, T, B = 40, 40, 62, 148
    sx = min((PW-L-R)/(xmax-xmin), (PH-T-B)/(ymax-ymin))
    cv = Canvas(PW, PH, sx=sx, ox=PW/2.0, oy=B-ymin*sx, bg="#FFFFFF")
    cv.panel(title="(二) 破壞面與最大主應力面的夾角",
             sub="θ 由 φ' 決定；莫爾圓上的角度是實體角的兩倍")
    w, h = 0.40, 0.70
    cv.polygon([(-w,-h),(w,-h),(w,h),(-w,h)], "rgba(63,74,90,0.07)", C["member"], 2.6)
    t = math.radians(TH); m = math.tan(t); ys = m*w
    p0, p1 = ((-w, -ys), (w, ys)) if ys <= h else ((-h/m, -h), (h/m, h))
    cv.line(p0, p1, C["load"], 3.4)
    cv.line(p0, (p0[0]+0.82, p0[1]), C["muted"], 1.6, dash="4 3")
    cv.poly([(p0[0]+0.34*math.cos(k*t/24), p0[1]+0.34*math.sin(k*t/24)) for k in range(25)], C["load"], 1.8)
    cv.math_px(cv.X(w+0.10), cv.Y(p0[1]+0.10), "θ = 45° + φ'/2 = %.2f°" % TH,
               13.5, C["load"], anchor="start", weight="700")
    # σ1（上下）
    for yy, s in ((h+0.30, -1), (-h-0.30, 1)):
        cv.arrow((0, yy), (0, yy+0.18*s), C["compr"], 3.2, 10)
    cv.math_px(cv.X(0), cv.Y(h+0.50), "σ_{1}' = %g kPa" % S1, 13.5, C["compr"], weight="700")
    cv.text_px(cv.X(-w)-10, cv.Y(h)-2, "最大主應力面（水平）", 12, C["compr"], anchor="end")
    # σ3（左右）
    for xx, s in ((-w-0.44, 1), (w+0.44, -1)):
        cv.arrow((xx, 0.30), (xx+0.20*s, 0.30), C["member2"], 3.0, 9)
    cv.math_px(cv.X(-w-0.48), cv.Y(0.44), "σ_{3}' = %g" % S3, 13, C["member2"], anchor="end")
    cv.math_px(cv.X(w+0.48), cv.Y(0.44), "σ_{3}' = %g" % S3, 13, C["member2"], anchor="start")
    # 破壞面上的應力（作用點取面上 -0.35 處，避開紅線中段）
    b = (p0[0]*0.42 + p1[0]*0.58, p0[1]*0.42 + p1[1]*0.58)
    n = (math.sin(t), -math.cos(t))
    cv.arrow((b[0]+0.46*n[0], b[1]+0.46*n[1]), (b[0]+0.10*n[0], b[1]+0.10*n[1]), C["accent"], 3.0, 9)
    cv.math_px(cv.X(b[0]+0.52*n[0])+4, cv.Y(b[1]+0.52*n[1])+4, "σ_{ff} = %.2f" % SFF,
               12.5, C["accent"], anchor="start", weight="700")
    tv = (math.cos(t), math.sin(t))
    cv.arrow((b[0]-0.34*tv[0], b[1]-0.34*tv[1]), (b[0]-0.02*tv[0], b[1]-0.02*tv[1]), C["sfd"], 3.0, 9)
    cv.math_px(cv.X(-w)-10, cv.Y(-0.34), "τ_{ff} = %.2f" % TFF,
               12.5, C["sfd"], anchor="end", weight="700")
    # (二) 證明鏈（畫在下方保留帶）
    for i, s in enumerate(["(二) 證明鏈：半徑 CF ⊥ 包絡線（相切）",
                           "⇒ CF 與 σ 軸夾角 ＝ 90° + φ'，即莫爾圓上的圓心角 2θ",
                           "⇒ 莫爾圓上的圓心角 ＝ 實體平面夾角的兩倍",
                           "⇒ θ = (90° + φ') / 2 = 45° + φ'/2"]):
        cv.text_px(PW/2, PH - 116 + i*21, s, 13, C["text"] if i == 3 else C["muted"],
                   weight="700" if i == 3 else "400")
    return cv

compose([panel_mohr(), panel_specimen()],
        title="SM-2024-1 圖 1　CD 三軸試驗的破壞莫爾圓、切點應力與破壞面傾角",
        sub="σ_3' = %g、Δσ_d = %g、c' = %g ⇒ φ' = %.2f°、σ_ff = %.2f、τ_ff = %.2f kPa" % (S3, DSD, CC, PHI, SFF, TFF),
        note="圖上每一個座標都由 σ_1' = σ_3' + Δσ_d 與切線條件 R = C sinφ' + c' cosφ' 算出，未量測、未描摹。",
        cols=2, path=os.path.join(OUT, "SM-2024-1-fig-1-mohr-failure.svg"))

# ══════════════════════════════════════════════════════════════
# fig-2　兩個圍壓的破壞莫爾圓：c' ≠ 0 ⇒ 不可比例外推
# ══════════════════════════════════════════════════════════════
W2, H2 = 1180, 720
xmin, xmax, ymin, ymax = -90.0, 700.0, -330.0, 250.0
L, R, T, B = 54, 330, 74, 44          # 右側 330 px 留給圖例與說明
sx = min((W2-L-R)/(xmax-xmin), (H2-T-B)/(ymax-ymin))
cv = Canvas(W2, H2, sx=sx, ox=L-xmin*sx, oy=B-ymin*sx, bg="#FFFFFF")
cv.panel(title="SM-2024-1 圖 2　同一土壤、兩個圍壓的破壞莫爾圓",
         sub="c' ≠ 0 ⇒ 軸差應力不與圍壓成正比")
cv.line((xmin+6, 0), (xmax-4, 0), C["muted"], 1.6)
cv.line((0, ymin+8), (0, ymax-6), C["muted"], 1.6)
cv.math_px(cv.X(xmax-4)-2, cv.Y(0)+20, "σ (kPa)", 13, C["muted"], anchor="end")
cv.math_px(cv.X(0)+8, cv.Y(ymax-6)+3, "τ (kPa)", 13, C["muted"], anchor="start")
XE = min(xmax-8, (ymax - 24 - CC) / math.tan(math.radians(PHI)))   # 包絡線裁到畫布內
cv.line((X0, 0), (XE, env(XE)), C["load"], 2.6)
cv.math_px(cv.X(XE)+8, cv.Y(env(XE)), "τ = %g + σ tan %.2f°" % (CC, PHI),
           13, C["load"], anchor="start", weight="700")
ph = math.radians(90.0 + PHI)
for cen, rad, s3, s1, col in ((CEN, RAD, S3, S1, C["deform"]),
                              (CENB, RADB, S3B, S1B, C["bmd"])):
    cv.circle((cen, 0), rad, fill="none", stroke=col, w=2.6)
    cv.dot((cen, 0), 4.0, fill=col)
    for v in (s3, s1): cv.dot((v, 0), 4.6, fill=col)
    cv.dot((cen+rad*math.cos(ph), rad*math.sin(ph)), 5.4, fill="#FFFFFF", stroke=C["accent"], w=2.8)
cv.math_px(cv.X(S3), cv.Y(0)+38, "%g" % S3, 13, C["deform"], weight="700")
cv.math_px(cv.X(S1), cv.Y(0)+38, "%g" % S1, 13, C["deform"], weight="700")
cv.math_px(cv.X(S3B), cv.Y(0)+58, "%g" % S3B, 13, C["bmd"], weight="700")
cv.math_px(cv.X(S1B), cv.Y(0)+38, "%.2f" % S1B, 13, C["bmd"], weight="700")
# 軸差應力對照（畫在圓下方的乾淨帶）
cv.dim((S3, -235.0), (S1, -235.0), "Δσ_d = %g" % DSD, off=0, color=C["deform"], size=13)
cv.dim((S3B, -275.0), (S1B, -275.0), "Δσ_d = %.2f" % DSDB, off=0, color=C["bmd"], size=13)
cv.line((S3B, -318.0), (S3B+DSD_WRONG, -318.0), C["load"], 2.4, dash="7 5")
cv.line((S3B+DSD_WRONG, -308.0), (S3B+DSD_WRONG, -328.0), C["load"], 2.2)
cv.text_px(cv.X(S3B+DSD_WRONG/2.0), cv.Y(-318.0)-11,
           "錯誤做法：240 × 2 = %g" % DSD_WRONG, 13, C["load"], weight="700")
# 右欄：圖例與說明
tx = W2 - R + 14
cv.legend(tx, 108, [(C["deform"], "題給狀態  σ3' = 100"),
                    (C["bmd"],    "(四) 新圍壓  σ3' = 200"),
                    (C["load"],   "比例外推（錯誤做法）")], size=13, gap=26)
for i, (txt, col, wt) in enumerate([
    ("正解（截距不為零的直線）", C["text"], "700"),
    ("σ1' = σ3'·Kp + 2c'·√Kp", C["text"], "400"),
    ("Kp = %.4f，  2c'√Kp = %.2f" % (KP, 2*CC*Y), C["muted"], "400"),
    ("", C["muted"], "400"),
    ("圍壓 +100 只讓 σ1' 增加", C["text"], "400"),
    ("100 × Kp = %.2f，不是加倍。" % (100*KP), C["text"], "400"),
    ("", C["muted"], "400"),
    ("比例外推 480 高估 %.1f%%。" % ((DSD_WRONG/DSDB-1)*100), C["load"], "700"),
    ("", C["muted"], "400"),
    ("只有 c' = 0（正常壓密黏土）時", C["muted"], "400"),
    ("包絡線才過原點，Δσd 也才與", C["muted"], "400"),
    ("圍壓成正比 —— 見 SM-2018-2。", C["muted"], "400")]):
    if not txt: continue
    cv.text_px(tx, 212 + i*24, txt, 13, col, anchor="start", weight=wt)
cv.save(os.path.join(OUT, "SM-2024-1-fig-2-two-circles.svg"))
print("phi=%.4f Kp=%.5f sff=%.3f tff=%.3f theta=%.3f s1b=%.3f dsdb=%.3f" % (PHI, KP, SFF, TFF, TH, S1B, DSDB))
