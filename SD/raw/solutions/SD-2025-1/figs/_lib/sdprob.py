"""sdprob.py — SD 題目附圖重繪用小工具（彈簧、阻尼器、剪力屋架）；建在 structdraw 之上。
所有幾何由呼叫端傳入的判讀清單數值決定。2026-11-15（SD-U1-3 批 1）"""
import math
from structdraw import Canvas, C

def fit(W, H, xr, yr, L=60, R=60, T=50, B=50):
    sx = min((W - L - R) / (xr[1] - xr[0]), (H - T - B) / (yr[1] - yr[0]))
    ox = L + ((W - L - R) - (xr[1] - xr[0]) * sx) / 2 - xr[0] * sx
    oy = B + ((H - T - B) - (yr[1] - yr[0]) * sx) / 2 - yr[0] * sx
    return Canvas(W, H, sx=sx, ox=ox, oy=oy, bg="#FFFFFF")

def spring(cv, p0, p1, n=6, amp=0.12, lead=0.18, color=C["member"], w=2.2):
    """p0→p1 之間畫鋸齒彈簧（amp、lead 為模型單位）"""
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    a = lead * L; b = L - lead * L
    pts = [p0, (x0 + ux * a, y0 + uy * a)]
    for i in range(1, 2 * n):
        t = a + (b - a) * i / (2 * n); s = amp * (1 if i % 2 else -1)
        pts.append((x0 + ux * t + nx * s, y0 + uy * t + ny * s))
    pts += [(x0 + ux * b, y0 + uy * b), p1]
    cv.poly(pts, color, w)

def dashpot(cv, p0, p1, wd=0.16, color=C["member"], w=2.2):
    """p0→p1 之間畫黏滯阻尼器（缸體開口朝 p0 側的活塞）"""
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    P = lambda t, s=0: (x0 + ux * t + nx * s, y0 + uy * t + ny * s)
    c0, c1 = 0.35 * L, 0.68 * L
    cv.line(p0, P(0.5 * L), color, w)                      # 活塞桿
    cv.line(P(0.5 * L, -wd * 0.75), P(0.5 * L, wd * 0.75), color, w + 0.6)  # 活塞
    cv.poly([P(c0, -wd), P(c1, -wd), P(c1, wd), P(c0, wd)], color, w)      # 缸體（p0 側開口）
    cv.line(P(c1), p1, color, w)

def ground(cv, p0, p1, color=C["member"], n=None):
    """地面線＋剖線（剖線在線段右側法線方向，水平由左往右畫時在下方）"""
    (x0, y0), (x1, y1) = p0, p1
    cv.line(p0, p1, color, 3.0)
    L = math.hypot(x1 - x0, y1 - y0); n = n or max(4, int(L * cv.sx / 14))
    ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = uy, -ux
    h = 10 / cv.sx
    for i in range(n + 1):
        t = L * i / n
        bx, by = x0 + ux * t, y0 + uy * t
        cv.line((bx, by), (bx - ux * h + nx * h, by - uy * h + ny * h), color, 1.6)
