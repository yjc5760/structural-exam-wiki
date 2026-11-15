# -*- coding: utf-8 -*-
"""SM-2012-1 圖解。數值由本檔依 SM-2012-1.md §4 重算（非硬寫座標）。
用法：STRUCTDRAW=<struct-diagram/scripts> python gen_SM-2012-1.py"""
# -*- coding: utf-8 -*-
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
D, Rad = math.degrees, math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
# ── L1 ──
PHICU, PHIP, SU, GSAT, GW, ZW = 22.0, 32.0, 50.0, 18.0, 9.81, 2.0
# ── §4 ──
SC  = SU/math.sin(Rad(PHICU)) - SU          # σ'c = σ'v0 = 83.47（總應力圓 σ3）
Z   = ZW + (SC - GSAT*ZW)/(GSAT-GW)         # 7.80 m
PE  = SU/math.sin(Rad(PHIP))                # 有效圓圓心 94.35
DU  = (SC+SU) - PE                          # 39.12
S3T, S1T = SC, SC+2*SU                      # 83.47、183.47
S3E, S1E = PE-SU, PE+SU                     # 44.35、144.35

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

W, H = 1000, 700
cv = plane(W, H, (-10, 215), (-66, 104),
           "破壞時的總應力圓與有效應力圓（NC：c = c' = 0）",
           "同一半徑 S_{u} = 50；總應力圓切 φ_{cu} 線定出 σ'_{v0}，左移 Δu_{f} 後切 φ' 線")
for phi, col, lab, dy in ((PHICU, C["member"], "φ_{cu} = 22°（總應力）", 30), (PHIP, C["load"], "φ' = 32°（有效應力）", -22)):
    e = env(cv, 0, phi, 210 if phi == PHICU else 160, col)
    xl = 210 if phi == PHICU else 120
    cv.text_px(cv.X(xl)-4, cv.Y(xl*math.tan(Rad(phi)))+dy, lab, 13, col, anchor="end", weight="700")
circ(cv, S3T, S1T, C["member"], fill="rgba(63,74,90,0.07)")
circ(cv, S3E, S1E, C["deform"], fill="rgba(29,78,216,0.10)")
for a, b, phi, col in ((S3T, S1T, PHICU, C["member"]), (S3E, S1E, PHIP, C["deform"])):
    cv.dot(tpoint(a, b, phi), 5, fill="#FFFFFF", stroke=col, w=2.4)
cv.text_px(cv.X(S3T)+14, cv.Y(-SU-8), "σ_{3} = σ'_{c} = σ'_{v0} = %.2f" % S3T, 12.5, C["member"], weight="700", anchor="start")
cv.text_px(cv.X(S1T), cv.Y(0)+20, "σ_{1} = %.2f" % S1T, 12.5, C["member"], weight="700", anchor="start")
cv.text_px(cv.X(S3E)-4, cv.Y(0)+20, "σ'_{3f} = %.2f" % S3E, 12.5, C["deform"], weight="700", anchor="end")
cv.text_px(cv.X(S1E)-6, cv.Y(0)+20, "%.2f" % S1E, 12.5, C["deform"], weight="700", anchor="end")
cv.double_arrow((S3E, -SU-8), (S3T, -SU-8), C["accent"], 2.4, 9)
cv.text_px(cv.X((S3E+S3T)/2), cv.Y(-SU-8)+20, "Δu_{f} = %.2f" % DU, 13, C["accent"], weight="700")
cv.line(((S3T+S1T)/2, 0), ((S3T+S1T)/2, SU), C["accent"], 2.0, dash="4 3")
cv.text_px(cv.X((S3T+S1T)/2)+6, cv.Y(SU*0.55), "S_{u} = 50", 13, C["accent"], anchor="start", weight="700")
cv.text_px(W/2, H-22, "σ'_{v0} = %.2f ⇒ z = %.2f m（γ_{w} = 9.81）；A_{f} = Δu_{f}/(2S_{u}) = %.3f" % (SC, Z, DU/(2*SU)), 12.5, C["text"])
cv.save(os.path.join(OUT, "SM-2012-1-fig-1-two-mohr.svg"))
print("sc=%.2f z=%.2f pe=%.2f du=%.2f s3e=%.2f" % (SC, Z, PE, DU, S3E))
