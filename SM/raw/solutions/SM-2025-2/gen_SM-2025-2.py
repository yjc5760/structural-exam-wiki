# -*- coding: utf-8 -*-
"""SM-2025-2 圖解。數值由本檔依 SM-2025-2.md §4 重算（非硬寫座標）。
用法：STRUCTDRAW=<struct-diagram/scripts> python gen_SM-2025-2.py"""
# -*- coding: utf-8 -*-
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
D, Rad = math.degrees, math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
# ── L1：試體一、二（σ3, Δσ, u）、試體三 CD σ3 ──
T1, T2, S3_3 = (75.0, 40.0, 35.0), (150.0, 70.0, 70.0), 200.0
# ── §4 ──
def eff(t): s3, d, u = t; return s3-u, s3+d-u
A3, A1 = eff(T1); B3, B1 = eff(T2)                   # (40,80)、(80,150)
NPHI = (B1-A1)/(B3-A3)                               # 1.75
K = A1 - NPHI*A3                                     # 2c'√Nφ = 10
PHIP = 2*(D(math.atan(math.sqrt(NPHI)))-45)          # 15.83°
CP = K/(2*math.sqrt(NPHI))                           # 3.78
C3, C1 = S3_3, NPHI*S3_3 + K                         # 200、360
DS3 = C1 - C3                                        # 160

# ── 莫爾圓平面共用小工具（各題腳本內含同一段，便於單檔重跑）──
def plane(W, H, xr, yr, title, sub, L=60, R=40, T=78, B=46):
    sx = min((W-L-R)/(xr[1]-xr[0]), (H-T-B)/(yr[1]-yr[0]))
    cv = Canvas(W, H, sx=sx, ox=L-xr[0]*sx, oy=B-yr[0]*sx, bg="#FFFFFF")
    cv.panel(title=title, sub=sub)
    cv.line((xr[0], 0), (xr[1], 0), C["muted"], 1.6)
    cv.line((0, max(yr[0], -5/sx)), (0, yr[1]), C["muted"], 1.6)
    cv.text_px(cv.X(xr[1])-2, cv.Y(0)-12, "σ (kPa)", 12.5, C["muted"], anchor="end")
    cv.text_px(cv.X(0)+8, cv.Y(yr[1])+4, "τ (kPa)", 12.5, C["muted"], anchor="start")
    return cv

def circ(cv, s3, s1, col, fill="none", w=2.6, dash=None):
    cen, r = (s1+s3)/2.0, (s1-s3)/2.0
    cv.circle((cen, 0), r, fill=fill, stroke=col, w=w, dash=dash)
    for v in (s3, s1): cv.dot((v, 0), 4.2, fill=col)
    return cen, r

def env(cv, c, phi, x1, col, w=2.6, dash=None):
    t = math.tan(Rad(phi))
    cv.line((-c/t if c > 0 and False else 0, c), (x1, c+x1*t), col, w, dash=dash)
    return (x1, c+x1*t)

def tpoint(s3, s1, phi):
    cen, r = (s1+s3)/2.0, (s1-s3)/2.0
    a = Rad(90.0+phi)
    return (cen+r*math.cos(a), r*math.sin(a))

def tp_c(s3, s1, c, phi):
    cen, r = (s1+s3)/2.0, (s1-s3)/2.0
    a = Rad(90.0+phi); return (cen+r*math.cos(a), r*math.sin(a))

W, H = 1000, 640
cv = plane(W, H, (-10, 400), (-100, 150),
           "有效應力莫爾圓與破壞包絡線（c' = %.2f、φ' = %.2f°）" % (CP, PHIP),
           "實線：試體一、二扣孔隙水壓後的有效圓；虛線：未扣 u 的總應力圓（不可用）")
e = env(cv, CP, PHIP, 395, C["load"])
cv.text_px(cv.X(e[0])-4, cv.Y(e[1])-14, "τ = %.2f + σ' tan %.2f°" % (CP, PHIP), 13, C["load"], anchor="end", weight="700")
for t in (T1, T2):
    circ(cv, t[0], t[0]+t[1], C["member2"], dash="6 4", w=1.6)
for (a, b), col, nm in (((A3, A1), C["deform"], "試體一"), ((B3, B1), C["bmd"], "試體二"), ((C3, C1), C["accent"], "試體三（CD）")):
    circ(cv, a, b, col, fill="rgba(29,78,216,0.06)")
    cv.dot(tp_c(a, b, CP, PHIP), 5, fill="#FFFFFF", stroke=col, w=2.4)
    cv.text_px(cv.X((a+b)/2), cv.Y(-(b-a)/2)+18, "%s %g～%g" % (nm, a, b), 12.5, col, weight="700")
cv.text_px(W/2, H-22, "Nφ = (150 − 80)/(80 − 40) = %.2f；2c'√Nφ = %g ⇒ 試體三 Δσ_{f} = %.2f × 200 + %g − 200 = %g kN/m²" % (NPHI, K, NPHI, K, DS3), 12.5, C["text"])
cv.save(os.path.join(OUT, "SM-2025-2-fig-1-mohr-cphi.svg"))
print("Nphi=%.3f K=%.2f phi=%.2f c=%.2f ds=%.1f" % (NPHI, K, PHIP, CP, DS3))
