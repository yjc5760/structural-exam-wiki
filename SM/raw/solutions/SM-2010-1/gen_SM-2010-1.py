# -*- coding: utf-8 -*-
"""SM-2010-1 圖解。所有數值由本檔依 SM-2010-1.md §3.5 的 L1 輸入重算，非硬寫座標。"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
D, Rad = math.degrees, math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")

# ── L1（§3.5）───────────────────────────────────────────────
GSAT, PHI, Z, ZW, GW, S3CELL = 17.5, 28.0, 12.0, 2.0, 9.81, 50.0
# ── L2（§4）────────────────────────────────────────────────
SV0  = GSAT * Z                          # 210.00
U0   = GW * (Z - ZW)                     # 98.10
SVP0 = SV0 - U0                          # 111.90
KP   = math.tan(Rad(45 + PHI/2))**2      # 2.7698
S3F  = SVP0 / KP                         # 40.40
SU   = (SVP0 - S3F) / 2.0                # 35.75
SU2  = SVP0 * math.sin(Rad(PHI)) / (1 + math.sin(Rad(PHI)))   # 交叉驗算
DSDF = 2 * SU                            # 71.50
UF   = S3CELL - S3F                      # 9.60
S1F  = S3CELL + DSDF                     # 121.50
DUC  = S3CELL                            # B = 1 ⇒ Δu = Δσ3 = 50

# ══════════════════════════════════════════════════════════
# fig-1　現地應力剖面（σ_v、u、σ_v'）
# ══════════════════════════════════════════════════════════
W1, H1 = 1020, 620
ZS = 15.0                                 # 1 m 深度 = 15 個繪圖單位（兩軸單位不同，需自行換算）
def ZY(z): return -z * ZS
xmin, xmax, ymin, ymax = -10.0, 236.0, ZY(Z) - 26.0, 22.0
L, R, T, B = 76, 300, 84, 58
sx = min((W1-L-R)/(xmax-xmin), (H1-T-B)/(ymax-ymin))
cv = Canvas(W1, H1, sx=sx, ox=L-xmin*sx, oy=B-ymin*sx, bg="#FFFFFF")
cv.panel(title="SM-2010-1 圖 1　現地應力剖面（取樣深度 12 m）",
         sub="γsat = %g kN/m³ 全段適用；地下水位在地表下 %g m" % (GSAT, ZW))
cv.line((0, ZY(0)), (0, ZY(Z) - 16), C["muted"], 1.6)
cv.line((xmin+4, 0), (xmax-4, 0), C["member"], 2.4)
cv.text_px(cv.X(xmax-4), cv.Y(0)-16, "地表", 12.5, C["member"], anchor="end")
cv.text_px(cv.X(xmax-4), cv.Y(ZY(Z)-16)+4, "應力 (kPa) →", 12.5, C["muted"], anchor="end")
for zz in range(0, int(Z)+1, 2):
    cv.line((-5, ZY(zz)), (0, ZY(zz)), C["muted"], 1.2)
    cv.text_px(cv.X(-8), cv.Y(ZY(zz)), "%d m" % zz, 11.5, C["muted"], anchor="end")
cv.line((-6, ZY(ZW)), (xmax-8, ZY(ZW)), C["deform"], 1.6, dash="7 5")
cv.text_px(cv.X(xmax-8), cv.Y(ZY(ZW))-12, "地下水位（地表下 %g m）" % ZW, 12, C["deform"], anchor="end")
zs = [i*0.2 for i in range(int(Z/0.2)+1)]
sv  = [(GSAT*z, ZY(z)) for z in zs]
u   = [(0.0 if z <= ZW else GW*(z-ZW), ZY(z)) for z in zs]
svp = [(a[0]-b[0], a[1]) for a, b in zip(sv, u)]
for pts, col, lab, val, dy in ((sv, C["member"], "σ_{v}", SV0, 0),
                               (u,  C["deform"], "u",     U0,  22),
                               (svp, C["load"],  "σ_{v}'", SVP0, -22)):
    cv.poly(pts, col, 2.8)
    cv.dot(pts[-1], 4.8, fill=col)
    cv.math_px(cv.X(pts[-1][0])+9, cv.Y(ZY(Z))+dy, "%s = %.2f" % (lab, val), 13, col,
               anchor="start", weight="700")
cv.line((0, ZY(Z)), (SV0, ZY(Z)), C["muted"], 1.4, dash="4 3")
cv.text_px(cv.X(8), cv.Y(ZY(Z))-14, "取樣深度 12 m", 12.5, C["muted"], anchor="start")
for i, (t, col, wt) in enumerate([
    ("σv  = 17.5 × 12 = 210.00 kPa", C["member"], "400"),
    ("u   = 9.81 × (12 − 2) = 98.10 kPa", C["deform"], "400"),
    ("σv' = 210.00 − 98.10 = 111.90 kPa", C["load"], "700"),
    ("", C["muted"], "400"),
    ("正常壓密黏土、完美取樣、Af = 1：", C["text"], "700"),
    ("Su = σv' · sinφ' / (1 + sinφ')", C["text"], "400"),
    ("   = 111.90 × 0.4695 / 1.4695", C["text"], "400"),
    ("   = %.2f kPa" % SU, C["text"], "700"),
    ("", C["muted"], "400"),
    ("水位以上仍取 γsat：題目只給一個", C["muted"], "400"),
    ("單位重，且考卷首頁允許合理假設。", C["muted"], "400"),
    ("u 的起算點在水位、不是地表 ——", C["muted"], "400"),
    ("寫成 9.81×12 = 117.7 是常見錯誤。", C["muted"], "400")]):
    if t: cv.text_px(W1-R+14, 190+i*26, t, 12.5, col, anchor="start", weight=wt)
cv.save(os.path.join(OUT, "SM-2010-1-fig-1-profile.svg"))

# ══════════════════════════════════════════════════════════
# fig-2　從現地到破壞的四個階段：總應力、孔隙水壓、有效應力
# ══════════════════════════════════════════════════════════
W2, H2 = 1120, 680
STAGES = [("① 現地\n（深度 12 m，垂直向）", SV0, U0, SVP0, "σv = 210"),
          ("② 完美取樣後\n（外加應力歸零）", 0.0, -SVP0, SVP0, "u 變成負壓"),
          ("③ 裝機、施加圍壓 50\n（飽和 ⇒ B = 1）", S3CELL, -SVP0 + DUC, SVP0, "Δu = Δσ3 = 50"),
          ("④ 剪至破壞\n（Δσd = 71.5、Af = 1）", S3CELL, UF, S3F, "u 由負轉正")]
ymin2, ymax2 = -140.0, 235.0
L, R, T, B = 74, 40, 92, 150
sx = min((W2-L-R)/4.4, (H2-T-B)/(ymax2-ymin2))
cv = Canvas(W2, H2, sx=1.0, ox=0.0, oy=0.0, bg="#FFFFFF")
cv.panel(title="SM-2010-1 圖 2　同一個試體，從現地到 UU 破壞的孔隙水壓歷程",
         sub="關鍵：③ 施加圍壓 50 全部由孔隙水承擔，有效應力一動也不動 ⇒ φu = 0")
PX0, PXW = 92, 240                       # 每欄的左緣與寬度
YB, YS = 420, 0.85                       # 基線像素、每 kPa 幾像素
SER = [("rgba(63,74,90,0.62)", "rgba(63,74,90,0.24)", "總應力 σ（圍壓／覆土壓力）"),
       ("rgba(29,78,216,0.58)", "rgba(29,78,216,0.22)", "孔隙水壓 u（可為負）"),
       ("rgba(192,57,43,0.58)", "rgba(192,57,43,0.22)", "有效應力 σ'")]
def bar(i, k, val):
    x = PX0 + i*PXW + k*58
    y0, y1 = YB, YB - val*YS
    cv.rect_px(x, min(y0, y1), 44, max(abs(y1-y0), 2),
               SER[k][0] if val >= 0 else SER[k][1], 4, C["border"], 1)
    cv.text_px(x+22, y1 + (-13 if val >= 0 else 15), "%.1f" % val, 12, C["text"], weight="700")
for i, (name, tot, uu, eff, note) in enumerate(STAGES):
    cv.rect_px(PX0 + i*PXW - 14, 108, PXW - 16, 424, "#FFFFFF" if i % 2 else "rgba(0,0,0,0.025)", 10)
    for j, ln in enumerate(name.split("\n")):
        cv.text_px(PX0 + i*PXW + 84, 128 + j*20, ln, 13 if j == 0 else 12,
                   C["text"] if j == 0 else C["muted"], weight="700" if j == 0 else "400")
    bar(i, 0, tot); bar(i, 1, uu); bar(i, 2, eff)
    cv.text_px(PX0 + i*PXW + 84, 556, note, 12.5, C["accent"], weight="700")
cv.rect_px(PX0-34, YB-1, 4*PXW - 4, 2, C["member"], 0)
cv.text_px(PX0-38, YB, "0", 12, C["muted"], anchor="end")
for k, (col, _n, lab) in enumerate(SER):
    lx = 120 + k*330
    cv.rect_px(lx, 592, 26, 13, col, 3, C["border"], 1)
    cv.text_px(lx + 34, 599, lab, 12.5, C["muted"], anchor="start")
cv.text_px(W2/2, 636, "② → ③ 有效應力 111.90 完全不變（紅柱等高）：這就是 UU 試驗 Su 與圍壓無關的原因。"
                      "　④ 破壞時 u = 50 − 40.40 = %.1f kPa。" % UF, 13, C["text"], weight="700")
cv.save(os.path.join(OUT, "SM-2010-1-fig-2-stress-history.svg"))

# ══════════════════════════════════════════════════════════
# fig-3　破壞時的莫爾圓：φu = 0 與 φ' 兩條包絡線
# ══════════════════════════════════════════════════════════
W3, H3 = 1080, 620
S3X = 150.0                              # 另一個示範圍壓（示範 φu = 0）
xmin, xmax, ymin, ymax = -12.0, 250.0, -62.0, 130.0
L, R, T, B = 54, 44, 86, 96
sx = min((W3-L-R)/(xmax-xmin), (H3-T-B)/(ymax-ymin))
cv = Canvas(W3, H3, sx=sx, ox=L-xmin*sx, oy=B-ymin*sx, bg="#FFFFFF")
cv.panel(title="SM-2010-1 圖 3　UU 破壞時的總應力圓與有效應力圓",
         sub="總應力圓可以左右平移（隨圍壓），有效應力圓永遠停在同一處")
cv.line((xmin+4, 0), (xmax-4, 0), C["muted"], 1.6)
cv.line((0, ymin+6), (0, ymax-6), C["muted"], 1.6)
cv.math_px(cv.X(xmax-4)-2, cv.Y(0)+20, "σ (kPa)", 12.5, C["muted"], anchor="end")
cv.math_px(cv.X(0)+8, cv.Y(ymax-6)+3, "τ (kPa)", 12.5, C["muted"], anchor="start")
# φ' 包絡線（c' = 0）
xe = min(xmax-6, (ymax-16)/math.tan(Rad(PHI)))
cv.line((0, 0), (xe, xe*math.tan(Rad(PHI))), C["load"], 2.6)
cv.text_px(cv.X(xe)+6, cv.Y(xe*math.tan(Rad(PHI)))-8, "有效應力包絡線  φ' = %g°、c' = 0" % PHI, 13,
           C["load"], anchor="end", weight="700")
# φu = 0 水平包絡線
cv.line((xmin+4, SU), (xmax-6, SU), C["bmd"], 2.6, dash="8 5")
cv.text_px(cv.X(xmax-6), cv.Y(SU)-14, "總應力包絡線  φu = 0、cu = Su = %.2f" % SU, 13, C["bmd"],
           anchor="end", weight="700")
# 有效應力圓
cv.circle(((SVP0+S3F)/2.0, 0), SU, fill="rgba(192,57,43,0.10)", stroke=C["load"], w=2.8)
for v in (S3F, SVP0): cv.dot((v, 0), 4.4, fill=C["load"])
cv.math_px(cv.X(S3F)-4, cv.Y(0)+22, "σ_{3f}' = %.2f" % S3F, 12.5, C["load"], anchor="end", weight="700")
cv.math_px(cv.X(SVP0)-4, cv.Y(0)+22, "σ_{1f}' = %.2f" % SVP0, 12.5, C["load"], anchor="end", weight="700")
a = Rad(90+PHI)
cv.dot(((SVP0+S3F)/2.0 + SU*math.cos(a), SU*math.sin(a)), 5.4, fill="#FFFFFF", stroke=C["accent"], w=2.8)
# 總應力圓（試驗圍壓 50）
cv.circle(((S3CELL+S1F)/2.0, 0), SU, fill="rgba(63,74,90,0.07)", stroke=C["member"], w=2.8)
for v in (S3CELL, S1F): cv.dot((v, 0), 4.4, fill=C["member"])
cv.math_px(cv.X(S3CELL)+4, cv.Y(0)+44, "σ_{3} = %g" % S3CELL, 12.5, C["member"], anchor="start", weight="700")
cv.math_px(cv.X(S1F)+4, cv.Y(0)+44, "σ_{1} = %.2f" % S1F, 12.5, C["member"], anchor="start", weight="700")
cv.dot(((S3CELL+S1F)/2.0, SU), 5.0, fill="#FFFFFF", stroke=C["bmd"], w=2.6)
# 另一個圍壓的總應力圓（虛線）－ 示範 φu = 0
cv.circle(((S3X+S3X+DSDF)/2.0, 0), SU, fill="none", stroke=C["member2"], w=2.2, dash="7 5")
cv.dot(((S3X+S3X+DSDF)/2.0, SU), 4.6, fill="#FFFFFF", stroke=C["member2"], w=2.2)
cv.text_px(cv.X(S3X+DSDF/2.0), cv.Y(-SU)-18, "若改用 σ3 = %g，半徑仍是 %.2f" % (S3X, SU),
           12.5, C["member2"], weight="700")
# u_f 平移
cv.double_arrow((S3F, -SU-26/sx), (S3CELL, -SU-26/sx), C["accent"], 2.4, 9)
cv.math_px(cv.X((S3F+S3CELL)/2.0), cv.Y(-SU-26/sx)+20, "u_{f} = %.1f" % UF, 12.5, C["accent"], weight="700")
for i, t in enumerate([
    "有效應力圓（紅）與 φ' 包絡線相切 —— 破壞的真正條件；它的位置只由現地 σv' = 111.90 決定。",
    "總應力圓（灰）＝ 有效應力圓右移 u_f = %.1f kPa。改變試驗圍壓只會讓灰圓左右平移，半徑恆為 Su。" % UF,
    "所以總應力包絡線是一條水平線（φu = 0），這就是第 2 小題「Δu = 50 ⇒ σ' 不變」的圖形版本。"]):
    cv.text_px(W3/2, H3 - 74 + i*21, t, 12.5, C["text"] if i == 2 else C["muted"],
               weight="700" if i == 2 else "400")
cv.save(os.path.join(OUT, "SM-2010-1-fig-3-uu-mohr.svg"))
print("svp0=%.2f Kp=%.4f s3f=%.2f Su=%.3f (chk %.3f) uf=%.2f s1f=%.2f duc=%g" % (SVP0, KP, S3F, SU, SU2, UF, S1F, DUC))
