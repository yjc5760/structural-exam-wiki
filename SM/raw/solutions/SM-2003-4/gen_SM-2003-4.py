"""SM-2003-4 圖解。數值由本檔依 SM-2003-4.md §3.5 L1 與 §4 重算（非硬寫座標）。
用法：STRUCTDRAW=<struct-diagram/scripts> python gen_SM-2003-4.py"""
# -*- coding: utf-8 -*-
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
D, Rad = math.degrees, math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── L1（§3.5）──
GSAT, GW, Z, PHIP = 17.5, 9.81, 12.0, 30.0
# ── §4 ──
SV0 = (GSAT-GW)*Z                                   # 92.28
S   = math.sin(Rad(PHIP))
def su(A): return SV0*S/(1+(2*A-1)*S)               # 完美取樣、等向 σ'c = σ'v0 的 CU 強度
SU1, SU05 = su(1.0), su(0.5)                        # 30.76、46.14（替代解讀）
def eff_circle(A):                                  # 破壞時有效主應力
    r = su(A); p = r/S; return p-r, p+r
S3F, S1F = eff_circle(1.0)                          # 30.76、92.28（σ'1f = σ'v0）
S3B, S1B = eff_circle(0.5)                          # 46.14、138.42

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

W, H = 1000, 720
cv = plane(W, H, (-10, 175), (-75, 95),
           "破壞時的有效應力莫爾圓（c' = 0、φ' = %g°）" % PHIP,
           "主答 A_{f} = 1：σ'_{1f} 恰回到 σ'_{v0}；A_{f} 未給，虛線為 A_{f} = 0.5 的對照")
pe = env(cv, 0, PHIP, 172, C["load"])
cv.text_px(cv.X(150), cv.Y(150*math.tan(Rad(PHIP)))-26, "φ' = 30°", 13, C["load"], weight="700")
circ(cv, S3B, S1B, C["member2"], dash="7 5", w=2.0)
circ(cv, S3F, S1F, C["deform"], fill="rgba(29,78,216,0.10)")
for (a, b), col in (((S3F, S1F), C["deform"]), ((S3B, S1B), C["member2"])):
    tp = tpoint(a, b, PHIP); cv.dot(tp, 5, fill="#FFFFFF", stroke=col, w=2.4)
cen = (S3F+S1F)/2
cv.line((cen, 0), (cen, SU1), C["accent"], 2.2, dash="4 3")
cv.text_px(cv.X(cen)+6, cv.Y(SU1/2), "S_{u} = %.2f" % SU1, 13, C["accent"], anchor="start", weight="700")
cv.text_px(cv.X(S3F)-52, cv.Y(0)+20, "σ'_{3f} = %.2f" % S3F, 12.5, C["deform"], weight="700")
cv.text_px(cv.X(S1F)+80, cv.Y(0)+20, "σ'_{1f} = σ'_{v0} = %.2f" % S1F, 12.5, C["deform"], weight="700")
cv.text_px(cv.X(S1B)+30, cv.Y(0)+20, "%.2f" % S1B, 12, C["member2"])
cv.text_px(cv.X(S3B)+10, cv.Y(0)+42, "%.2f" % S3B, 12, C["member2"])
cv.text_px(cv.X(S1B)+10, cv.Y(SU05*0.8), "A_{f} = 0.5：S_{u} = %.2f（對照）" % SU05, 12.5, C["member2"], anchor="start")
cv.text_px(W/2, H-22, "S_{u} = σ'_{v0} sinφ' / [1 + (2A_{f} − 1) sinφ']：A_{f} 是唯一的未知假設，取 1 或 0.5 答案差 1.5 倍", 12.5, C["text"])
cv.save(os.path.join(OUT, "SM-2003-4-fig-1-mohr-af.svg"))
print("sv0=%.2f su1=%.2f su05=%.2f s3f=%.2f s1b=%.2f" % (SV0, SU1, SU05, S3F, S1B))
