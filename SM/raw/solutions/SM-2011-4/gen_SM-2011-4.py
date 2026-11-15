# -*- coding: utf-8 -*-
"""SM-2011-4 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2011-4-problem.md §4 判讀清單，不含任何解題結果
（鋼鈑樁貫入長度考卷未標，為示意）。
用法：python gen_SM-2011-4.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *                                      # Canvas, C, compose, fit, soil_fill, wt_symbol
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
SAND, SAND2, CLAY = "rgba(180,83,9,0.12)", "rgba(180,83,9,0.24)", "rgba(63,74,90,0.20)"


def ground(cv, x0, x1, y, n=4, s=0.35):
    """地面剖線（短斜線）。"""
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n
        cv.line((x, y), (x - s, y - s), C["member"], 1.3)


def wall(cv, x, y0, y1, t=0.18, fill="#3F4A5A"):
    cv.polygon([(x - t / 2, y0), (x + t / 2, y0), (x + t / 2, y1), (x - t / 2, y1)], fill)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
Z_A, Z_B, Z_C = 1.0, 4.0, 6.0   # 支撐深度（1 m、+3 m、+2 m）
H_EXC = 7.0                     # 開挖深度（C 下 1 m）
B_EXC = 6.0                     # 兩鋼鈑樁間距
D_SK  = 1.2                     # 鋼鈑樁貫入段（示意）


def fig_problem():
    Wd, Ht = 900, 560
    XL, XR = -3.0, B_EXC + 5.2
    cv = Canvas(Wd, Ht, bg="#FFFFFF", **fit(Wd, Ht, (XL - 1.4, XR + 0.2), (-(H_EXC + D_SK + 0.7), 1.6), 30, 30, 40, 40))
    Y = lambda d: -d
    soil_fill(cv, XL, 0, Y(H_EXC + D_SK + 0.4), Y(0), CLAY)
    soil_fill(cv, B_EXC, XR, Y(H_EXC + D_SK + 0.4), Y(0), CLAY)
    soil_fill(cv, 0, B_EXC, Y(H_EXC + D_SK + 0.4), Y(H_EXC), CLAY)
    cv.line((XL, Y(0)), (0, Y(0)), C["member"], 2.4)
    cv.line((B_EXC, Y(0)), (XR, Y(0)), C["member"], 2.4)
    ground(cv, XL + 0.4, -0.6, Y(0), 3, 0.3)
    ground(cv, B_EXC + 0.8, B_EXC + 2.6, Y(0), 3, 0.3)
    cv.line((0, Y(H_EXC)), (B_EXC, Y(H_EXC)), C["member"], 2.4)
    ground(cv, 2.0, 3.6, Y(H_EXC), 3, 0.3)
    for x in (0, B_EXC):
        wall(cv, x, Y(0), Y(H_EXC + D_SK), 0.16)
    for lab, z in (("A 支撐", Z_A), ("B 支撐", Z_B), ("C 支撐", Z_C)):
        cv.line((0.1, Y(z)), (B_EXC - 0.1, Y(z)), C["member"], 4.0)
        for x in (0.18, B_EXC - 0.18):
            cv.polygon([(x - 0.13, Y(z) - 0.17), (x + 0.13, Y(z) - 0.17), (x + 0.13, Y(z) + 0.17), (x - 0.13, Y(z) + 0.17)], C["member"])
        cv.text_px(cv.X(3.4), cv.Y(Y(z)) - 16, lab, 13.5, C["text"], weight="700")
    cv.text_px(cv.X(3.4), cv.Y(Y(H_EXC)) - 16, "開挖底面", 13, C["muted"])
    cv.text_px(cv.X(-1.6), cv.Y(Y(3.0)), "鋼鈑樁", 13, C["muted"])
    cv.text_px(cv.X(B_EXC + 0.6), cv.Y(Y(1.6)), "黏土", 14, C["text"], anchor="start", weight="700")
    for i, s in enumerate(["G_{s} = 2.70", "e = 0.617", "S_{r} = 30%", "c = 30 kN/m^{2}", "φ = 0"]):
        cv.math_px(cv.X(B_EXC + 0.6), cv.Y(Y(2.5 + 0.8 * i)), s, 14, C["text"], anchor="start")
    # 尺寸線
    xd = 1.1
    pts = [0, Z_A, Z_B, Z_C, H_EXC]
    for (d0, d1), lab in zip(zip(pts[:-1], pts[1:]), ["1 m", "3 m", "2 m", "1 m"]):
        cv.dim((xd, Y(d1)), (xd, Y(d0)), lab, 0, C["dim"], 12.5, label_off=-22)
    cv.dim((0, Y(-0.9)), (B_EXC, Y(-0.9)), "6 m", 0, C["dim"], 13, label_off=14)
    xo = XL - 0.6
    cv.dim((xo, Y(H_EXC)), (xo, Y(0)), "H = 7 m", 0, C["dim"], 12.5, label_off=-34)
    for d in (0, H_EXC):
        cv.line((xo - 0.15, Y(d)), (XL, Y(d)), C["dim"], 0.9, dash="2 3")
    return cv


compose([fig_problem()],
        title="SM-2011-4 題目附圖重繪",
        sub="依題目正本判讀清單；三道支撐、開挖寬 6 m，黏土非飽和、無地下水",
        note="攔錯用：支撐在地表下 1、4、6 m，開挖深 H = 1 + 3 + 2 + 1 = 7 m；尺寸是相鄰支撐間距，不是由地表起算。",
        path=os.path.join(OUT, "SM-2011-4-fig-1-problem.svg"))


# ══════ fig-2-envelope-struts：解題圖解（2026-11-15 補解題圖解；數值依 SM-2011-4.md §4 重算）══════
import math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas as _Cv
def braced_fig(Canvas, C, H, pa, zt, struts, reacts, bottom, unit, hinge, wrong=None, extra=None, title="", sub="", mmax=None):
    """Peck 視土壓力包絡線＋鉸接法支撐反力。struts=[(名,z)]、reacts=[數值]、bottom=開挖底分擔；wrong=(標籤, 點列, 支撐值字串)"""
    W1, H1 = 980, 660
    PS = 5.2 / pa                         # 壓力軸：pa 畫成 5.2 m
    sx = 470.0 / (H + 1.2)
    cv = Canvas(W1, H1, sx=sx, ox=330, oy=80, bg=C["panel"])
    cv.panel(title, sub=sub)
    Yz = lambda z: H - z
    # 牆
    cv.line((0, Yz(0)), (0, Yz(H) - 0.35), C["member"], 5.0)
    cv.line((-2.6, Yz(0)), (0, Yz(0)), C["member"], 1.4)
    cv.line((0, Yz(H)), (6.6, Yz(H)), C["member"], 1.4, dash="6 4")
    cv.text_px(cv.X(6.6), cv.Y(Yz(H)) + 18, "開挖底 z = %g m" % H, 11.5, C["muted"], anchor="end")
    # 深度刻度
    for z in range(0, int(H) + 1):
        cv.line((-0.08, Yz(z)), (0.08, Yz(z)), C["muted"], 1)
    # 包絡線（牆右側）
    pts = [(0, Yz(0)), (pa * PS, Yz(zt)), (pa * PS, Yz(H)), (0, Yz(H))]
    cv.polygon(pts, "rgba(220,38,38,0.20)", C["load"], 2.6)
    cv.text_px(cv.X(pa * PS) + 8, cv.Y(Yz(zt)), "p_a = %.2f kN/m²" % pa, 12.5, C["load"], anchor="start", weight="700")
    cv.text_px(cv.X(pa * PS) + 8, cv.Y(Yz(zt)) + 17, "z = 0.25H = %g m" % zt, 11.5, C["muted"], anchor="start")
    cv.text_px(cv.X(pa * PS) + 8, cv.Y(Yz(H)) - 6, "到開挖底仍為 %.2f" % pa, 12, C["load"], anchor="start", weight="700")
    if wrong:
        lab, wp, wtxt = wrong
        cv.poly([(x * PS, Yz(z)) for x, z in wp], C["muted"], 2.2, dash="7 5")
        zl = wp[0][1] + 0.4
        cv.text_px(cv.X(pa * PS * 0.45), cv.Y(Yz(H - 1.9)), lab, 11.5, C["muted"], anchor="middle")
    # 支撐與反力（牆左側箭頭指向牆）
    for (nm, z), r in zip(struts, reacts):
        cv.arrow((-2.5, Yz(z)), (-0.12, Yz(z)), C["accent"], 3.0, 10)
        cv.text_px(cv.X(-2.6), cv.Y(Yz(z)) - 8, "%s（z = %g m）" % (nm, z), 12, C["accent"], anchor="end", weight="700")
        cv.text_px(cv.X(-2.6), cv.Y(Yz(z)) + 10, "%.1f %s" % (r, unit), 12, C["accent"], anchor="end")
    for z in hinge:
        cv.dot((0, Yz(z)), 5.5, fill="#FFFFFF", stroke=C["member"], w=2)
    # 開挖底支點
    cv.polygon([(0, Yz(H)), (-0.35, Yz(H) - 0.55), (0.35, Yz(H) - 0.55)], "#FFFFFF", C["member"], 1.8)
    cv.text_px(cv.X(-0.5), cv.Y(Yz(H) - 0.3), "開挖底支點 %.1f %s" % (bottom, unit), 11.5, C["member"], anchor="end")
    if mmax:
        zm, mv = mmax
        cv.line((0, Yz(zm)), (1.2, Yz(zm)), C["bmd"], 1.2, dash="3 3")
        cv.text_px(cv.X(1.3), cv.Y(Yz(zm)) + 4, "M_{max} ≈ %.1f kN·m/m（z = %.2f m）" % (mv, zm), 11.5, C["bmd"], anchor="start", weight="700")
    if extra:
        bx, by = cv.X(pa * PS) + 8, cv.Y(Yz(H * 0.55))
        for k, s in enumerate(extra):
            cv.text_px(bx, by + k * 19, s, 11.5, C["text"] if k else C["text"], anchor="start", weight="700" if k == 0 else "400")
    return cv


_G = round((2.70 + 0.30*0.617)/(1 + 0.617)*9.81, 2)   # 17.50（與 §4 同）
_H, _c, _s = 7.0, 30.0, 5.0
_PA = max(_G*_H - 4*_c, 0.3*_G*_H)
_ZT = 0.25*_H
_F1, _F2 = 0.5*_ZT*_PA, (4-_ZT)*_PA
_RA = (_F1*(4-2*_ZT/3) + _F2*(4-_ZT)/2)/3.0
_RB = (_F1 + _F2 - _RA) + 2*_PA/2
_RC = 2*_PA/2 + 1*_PA/2
_RD = 1*_PA/2
_zm = _ZT + (_RA - _F1)/_PA
_M = _RA*(_zm-1) - _F1*(_zm - 2*_ZT/3) - _PA*(_zm-_ZT)**2/2
_cv2 = braced_fig(_Cv, C, _H, _PA, _ZT, [("A", 1), ("B", 4), ("C", 6)], [_RA*_s, _RB*_s, _RC*_s], _RD*_s, "kN", [4, 6],
    extra=["γ = %.2f kN/m³、γH/c = %.2f ＞ 4 → 軟～中等黏土型" % (_G, _G*_H/_c),
           "γH − 4c = %.1f ＜ 0.3γH = %.2f → 由下限控制" % (_G*_H-4*_c, 0.3*_G*_H),
           "支撐力 = 單寬反力 × s（s = 5 m）",
           "S = M_{max}/σ_{all} ≈ %.2f×10^{-4} m³/m" % (_M/170000*1e4)],
    title="(一)(二)(三) 包絡線、支撐力與最大彎矩", sub="B、C 設鉸，開挖底當支點；M_{max} 在 A–B 間剪力為零處",
    mmax=(_zm, _M))
compose([_cv2], title="SM-2011-4　Peck 包絡線 → 鉸接法支撐力 → 截面模數",
        sub="pa = max(γH − 4c, 0.3γH) = %.2f kN/m²；支撐水平間距 5 m" % _PA,
        note="γH/c 只比 4 大一點：先判型再畫圖；包絡線面積是每延米荷重，支撐力要乘水平間距 5 m。",
        path=os.path.join(OUT, "SM-2011-4-fig-2-envelope-struts.svg"))
print("A=%.1f B=%.1f C=%.1f D=%.1f kN  zm=%.3f M=%.2f" % (_RA*_s, _RB*_s, _RC*_s, _RD*_s, _zm, _M))
