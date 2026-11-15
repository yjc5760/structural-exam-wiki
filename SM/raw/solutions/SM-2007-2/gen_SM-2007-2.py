# -*- coding: utf-8 -*-
"""SM-2007-2 ㈡ 圖解（題目要求「繪圖說明」的示意圖）。
本題無數值；只保留 SM-2007-2.md §4（二）的相對關係：
SUU：B = 1，圍壓全由孔隙水承擔 → 總應力圓等大、包絡線水平（φu = 0），有效圓只有一個。
UUU：B < 1，圍壓部分轉為有效應力 → 圓隨圍壓變大、包絡線上彎；氣體壓縮溶解達飽和後轉水平。
UUU 的圓由包絡線函數反算（圓心到曲線的最短距離 = 半徑），不是手擺座標。
用法：STRUCTDRAW=<struct-diagram/scripts> python gen_SM-2007-2.py"""
# -*- coding: utf-8 -*-
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
D, Rad = math.degrees, math.radians
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
# ── 示意參數（無單位）──
CU = 1.0                                 # SUU 水平包絡線高度 = c_u
S3_SUU = (1.5, 3.5, 5.5)                 # 三個圍壓
SP3 = 0.55                               # 唯一的有效應力圓 σ3'（示意）
TAU_MAX, A0, T0 = 1.45, 1.6, 0.35         # UUU 包絡線 τ = T0 + (TAU_MAX − T0)(1 − e^{−σ/A0})
ENV = lambda s: T0 + (TAU_MAX-T0)*(1-math.exp(-s/A0))
CENT_UUU = (1.0, 2.0, 3.4, 5.4, 7.4)     # 圓心（示意）

def r_tangent(p):
    return min(math.hypot(s-p, ENV(s)) for s in [i*0.002 for i in range(0, 5001)])

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

PW, PH = 640, 470
def frame_(title, sub):
    xr, yr = (-0.4, 9.6), (-2.05, 1.9)
    L, R, T, B = 40, 30, 80, 40
    sx = min((PW-L-R)/(xr[1]-xr[0]), (PH-T-B)/(yr[1]-yr[0]))
    cv = Canvas(PW, PH, sx=sx, ox=L-xr[0]*sx, oy=B-yr[0]*sx, bg="#FFFFFF")
    cv.panel(title=title, sub=sub)
    cv.line((xr[0], 0), (xr[1], 0), C["muted"], 1.6); cv.line((0, yr[0]+0.1), (0, yr[1]), C["muted"], 1.6)
    cv.text_px(cv.X(xr[1])-2, cv.Y(0)-12, "σ", 13, C["muted"], anchor="end")
    cv.text_px(cv.X(0)+8, cv.Y(yr[1])+6, "τ", 13, C["muted"], anchor="start")
    return cv

a = frame_("SUU（飽和）：φ_{u} = 0", "B = 1：加圍壓 Δσ_{3} 全由孔隙水承擔，有效應力不變")
for s3 in S3_SUU:
    circ(a, s3, s3+2*CU, C["member"], fill="rgba(63,74,90,0.05)", w=2.2)
circ(a, SP3, SP3+2*CU, C["deform"], fill="rgba(29,78,216,0.12)", dash="6 4", w=2.2)
a.line((0, CU), (9.4, CU), C["load"], 2.8)
a.text_px(a.X(9.3), a.Y(CU)-14, "τ_{f} = c_{u}（水平）", 13, C["load"], anchor="end", weight="700")
a.text_px(a.X(SP3+CU), a.Y(-CU)+20, "有效應力圓（只有一個）", 12, C["deform"])
a.text_px(a.X(5.0), a.Y(-1.75), "總應力圓：半徑相同、只是左右平移", 12.5, C["member"])

b = frame_("UUU（不飽和）：φ_{u} ＞ 0 → 0", "B ＜ 1：圍壓一部分變成有效應力，強度隨圍壓上升")
ss = [i*0.05 for i in range(0, 189)]
b.poly([(s, ENV(s)) for s in ss], C["load"], 2.8)
for p in CENT_UUU:
    r = r_tangent(p)
    circ(b, p-r, p+r, C["member"], fill="rgba(63,74,90,0.05)", w=2.2)
b.text_px(b.X(1.6), b.Y(ENV(1.6))-30, "初段傾斜：φ_{u} ＞ 0", 12.5, C["load"], anchor="middle", weight="700")
b.text_px(b.X(9.3), b.Y(TAU_MAX)-16, "後段水平：已飽和 φ_{u} → 0", 12.5, C["load"], anchor="end", weight="700")
b.text_px(b.X(4.8), b.Y(-1.75), "圓先變大、再維持等大（空氣壓縮／溶解後 B → 1）", 12.5, C["member"])

compose([a, b], title="SM-2007-2 圖 1（示意，無數值）　SUU 與 UUU 的總應力莫爾圓與包絡線",
        sub="題目㈡要求的繪圖：差別只在孔隙中有沒有可壓縮的空氣（B 值）",
        cols=2, path=os.path.join(OUT, "SM-2007-2-fig-1-suu-uuu.svg"))
print("radii UUU:", ["%.3f" % r_tangent(p) for p in CENT_UUU])
