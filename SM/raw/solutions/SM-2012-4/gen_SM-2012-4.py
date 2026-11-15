# -*- coding: utf-8 -*-
"""SM-2012-4 圖解（2026-11-15 補解題圖解）：Peck 視土壓力包絡線＋鉸接法支撐荷重。
數值由本檔依 SM-2012-4.md §4 重算（等值參數 Peck 1943、K_s = 1；B、C 設鉸、開挖底為支點）。
用法：python gen_SM-2012-4.py [輸出資料夾]（預設本題 figs/）"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.expanduser("~/sd")))
from structdraw import Canvas, C, compose
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

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


H, HS, GS, PHI, GC, SU = 10.0, 5.0, 16.5, 30.0, 18.5, 30.0
GAV = (GS*HS + GC*(H-HS))/H                                   # 17.5
CAV = round((0.5*GS*HS**2*math.tan(math.radians(PHI)) + SU*(H-HS))/H, 2)  # 26.91（與 §4 同取兩位）
PA = round(max(GAV*H - 4*CAV, 0.3*GAV*H), 2)                  # 67.36（與 §4 同取兩位）
ZT = 0.25*H
F1a, F1b = 0.5*ZT*PA, (4.5-ZT)*PA
RA = (F1a*(4.5-2*ZT/3) + F1b*(4.5-ZT)/2)/3.0
RB = (F1a + F1b - RA) + 3.0*PA/2
RC = 3.0*PA/2 + 2.5*PA/2
RD = 2.5*PA/2
RC_WRONG = 3.0*PA/2 + (0.5*2.5*PA)*(2.5*2/3)/2.5              # 勘誤前（底部遞減三角形）157.1
cv = braced_fig(Canvas, C, H, PA, ZT, [("A", 1.5), ("B", 4.5), ("C", 7.5)], [RA, RB, RC], RD, "kN/m", [4.5, 7.5],
    wrong=("硬黏土型誤畫：C 只得約 %.0f" % RC_WRONG, [(PA, 7.5), (0, 10.0)], ""),
    extra=["N = γ_{av}H / c_{av} = %.2f ＞ 4 → 軟～中等黏土型" % (GAV*H/CAV),
           "c_{av} = %.2f kPa（Peck，K_s = 1）" % CAV,
           "B、C 設鉸，開挖底當支點",
           "A＋B＋C＋底 = %.1f ＝ 包絡線面積 %.1f" % (RA+RB+RC+RD, 0.5*ZT*PA + (H-ZT)*PA)],
    title="(一) 視土壓力包絡線與支撐荷重（單位寬度）",
    sub="0～0.25H 斜升，0.25H 以下維持 p_a 到開挖底；灰虛線為誤用的硬黏土型")
compose([cv], title="SM-2012-4　Peck 視土壓力包絡線 → 鉸接法支撐荷重",
        sub="γ_{av} = %.2f kN/m³、c_{av} = %.2f kPa、pa = γH − 4c = %.2f kN/m²" % (GAV, CAV, PA),
        note="軟～中等黏土的包絡線底部不收回零；誤畫成硬黏土形狀，最下層支撐 C 會低估約 15%。",
        path=os.path.join(OUT, "SM-2012-4-fig-1-envelope-struts.svg"))
print("A=%.1f B=%.1f C=%.1f D=%.1f Cwrong=%.1f pa=%.2f" % (RA, RB, RC, RD, RC_WRONG, PA))
