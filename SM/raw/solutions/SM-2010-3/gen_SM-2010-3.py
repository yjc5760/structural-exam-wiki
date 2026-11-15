# -*- coding: utf-8 -*-
"""SM-2010-3 圖解。
fig-1-problem：題目附圖重繪，依題目正本 SM-2010-3-problem.md §4 判讀清單；
考卷附圖未依比例（#附圖比例），本重繪改依題文數值按比例繪製，不含任何解題結果。
用法：python gen_SM-2010-3.py [輸出資料夾]（預設本題 figs/）"""
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
Z_CL  = 2.0    # 黏土底＝砂層頂
Z_SB  = 8.0    # 砂層底
Z_WT  = 1.0    # 地下水位（外側）
H_EXC = 4.0    # 開挖深度（開挖內水位同高）
Z_TIP = 5.0    # 擋土壁底


def fig_problem():
    Wd, Ht = 900, 600
    XL, XR = -6.0, 9.0
    cv = Canvas(Wd, Ht, bg="#FFFFFF", **fit(Wd, Ht, (XL - 3.0, XR + 0.3), (-(Z_SB + 0.9), 0.8), 30, 30, 40, 40))
    Y = lambda d: -d
    soil_fill(cv, XL, 0, Y(Z_CL), Y(0), CLAY)
    soil_fill(cv, XL, XR, Y(Z_SB), Y(Z_CL), SAND2)
    soil_fill(cv, 0, XR, Y(Z_CL), Y(Z_CL), SAND2)
    cv.polygon([(0, Y(Z_CL)), (XR, Y(Z_CL)), (XR, Y(H_EXC)), (0, Y(H_EXC))], "#FFFFFF")
    cv.line((XL, Y(0)), (0, Y(0)), C["member"], 2.4)
    ground(cv, XL + 0.6, XL + 2.4, Y(0), 3, 0.3)
    cv.line((XL, Y(Z_CL)), (0, Y(Z_CL)), C["member2"], 1.6)
    cv.line((0, Y(H_EXC)), (XR, Y(H_EXC)), C["member"], 2.4)
    cv.line((XL, Y(Z_SB)), (XR, Y(Z_SB)), C["member2"], 1.6, dash="6 4")
    wall(cv, 0, Y(0), Y(Z_TIP), 0.3)
    wt_symbol(cv, -1.8, Y(Z_WT), C["deform"], 0.13)
    cv.line((XL, Y(Z_WT)), (-0.3, Y(Z_WT)), C["deform"], 1.3, dash="6 4")
    wt_symbol(cv, 5.5, Y(H_EXC), C["deform"], 0.13)
    cv.dot((0.15, Y(H_EXC)), 5.5, C["load"])
    cv.text_px(cv.X(0.45), cv.Y(Y(H_EXC)) - 14, "A", 15, C["load"], anchor="start", weight="700")
    cv.text_px(cv.X(-3.4), cv.Y(Y(1.35)), "黏土", 13, C["text"], weight="700")
    cv.math_px(cv.X(-3.4), cv.Y(Y(1.75)), "γ_{sat} = 17.5 kN/m^{3}", 13, C["text"])
    cv.text_px(cv.X(3.0), cv.Y(Y(6.3)), "砂土", 13, C["text"], weight="700")
    cv.math_px(cv.X(3.0), cv.Y(Y(7.1)), "γ_{sat} = 18 kN/m^{3}", 13, C["text"])
    cv.text_px(cv.X(4.5), cv.Y(Y(2.6)), "開挖區（水位抽降至開挖面）", 12.5, C["muted"])
    cv.text_px(cv.X(XR - 0.2), cv.Y(Y(Z_SB)) + 16, "8 m 以下考卷未給", 11.5, C["muted"], anchor="end")
    # 尺寸線（左側）
    xd = XL - 0.5
    cv.dim((xd, Y(Z_WT)), (xd, Y(0)), "1 m", 0, C["dim"], 12, label_off=-24)
    cv.dim((xd, Y(Z_CL)), (xd, Y(Z_WT)), "1 m", 0, C["dim"], 12, label_off=-24)
    cv.dim((xd - 1.8, Y(Z_CL)), (xd - 1.8, Y(0)), "2 m", 0, C["dim"], 12.5, label_off=-24)
    cv.dim((xd - 1.8, Y(Z_SB)), (xd - 1.8, Y(Z_CL)), "6 m", 0, C["dim"], 12.5, label_off=-24)
    for d in (0, Z_CL, Z_SB):
        cv.line((xd - 2.0, Y(d)), (XL, Y(d)), C["dim"], 0.9, dash="2 3")
    cv.line((xd - 0.2, Y(Z_WT)), (XL, Y(Z_WT)), C["dim"], 0.9, dash="2 3")
    cv.dim((1.4, Y(H_EXC)), (1.4, Y(0)), "4 m", 0, C["dim"], 12.5, label_off=24)
    cv.line((0.2, Y(0)), (1.6, Y(0)), C["dim"], 0.9, dash="2 3")
    cv.dim((-0.7, Y(Z_TIP)), (-0.7, Y(0)), "5 m", 0, C["dim"], 12.5, label_off=-22)
    cv.line((-0.9, Y(Z_TIP)), (-0.15, Y(Z_TIP)), C["dim"], 0.9, dash="2 3")
    return cv


compose([fig_problem()],
        title="SM-2010-3 題目附圖重繪（依題文數值按比例）",
        sub="依題目正本判讀清單；考卷原圖未依比例，A 點在開挖底面、緊貼擋土壁內側",
        note="攔錯用：開挖 4 m 已進入砂層 2 m，擋土壁只到 5 m（開挖面下 1 m）；外側水位 1 m、坑內水位在開挖面。",
        path=os.path.join(OUT, "SM-2010-3-fig-1-problem.svg"))


# ══════ fig-2-flowpath：解題圖解（2026-11-15 補解題圖解；數值依 SM-2010-3.md §4 重算）══════
def fig_flowpath():
    gw = 9.81; dh = 4.0 - 1.0; L = (5.0 - 2.0) + (5.0 - 4.0); i = dh / L
    ic = (18.0 - gw) / gw; e83 = 2 * (18 - gw) * 1.0 / (gw * 3.0); e84 = (18 - gw) * 5.0 / (gw * 3.0)
    W2, H2 = 1100, 640
    cv = Canvas(W2, H2, sx=52.0, ox=470, oy=70, bg=C["panel"])
    cv.panel("沿壁最短流徑（只在砂層內）→ A 點坡降與砂湧檢核", sub="黏土幾乎不透水：水頭 3 m 全耗在砂層內 3 m 下行＋1 m 上行")
    Yz = lambda z: 8.6 - z
    CL_, SA_ = "rgba(63,74,90,0.22)", "rgba(180,83,9,0.14)"
    cv.polygon([(-6.5, Yz(0)), (0, Yz(0)), (0, Yz(2)), (-6.5, Yz(2))], CL_)
    cv.polygon([(-6.5, Yz(2)), (0, Yz(2)), (0, Yz(4)), (5.5, Yz(4)), (5.5, Yz(8)), (-6.5, Yz(8))], SA_)
    cv.line((0, Yz(0)), (0, Yz(5)), C["member"], 5)
    cv.line((-6.5, Yz(0)), (0, Yz(0)), C["member"], 1.4); cv.line((0, Yz(4)), (5.5, Yz(4)), C["member"], 1.6)
    cv.line((-6.5, Yz(8)), (5.5, Yz(8)), C["muted"], 1.2, dash="6 4")
    cv.line((-6.5, Yz(1)), (0, Yz(1)), C["deform"], 1.4, dash="6 4")
    cv.text_px(cv.X(-6.4), cv.Y(Yz(1)) - 6, "外側水位 1 m", 11, C["deform"], anchor="start")
    cv.text_px(cv.X(5.4), cv.Y(Yz(4)) - 6, "開挖面＝坑內水位 4 m", 11, C["deform"], anchor="end")
    cv.text_px(cv.X(-3.4), cv.Y(Yz(1.55)), "黏土（不參與滲流）", 11.5, C["member"])
    cv.text_px(cv.X(-3.4), cv.Y(Yz(6.8)), "砂　γ_{sat} = 18 kN/m³", 11.5, C["accent"])
    cv.text_px(cv.X(0) - 8, cv.Y(Yz(5)) + 16, "壁底 5 m", 11, C["member"], anchor="end")
    # 流徑
    cv.arrow((-0.3, Yz(2.05)), (-0.3, Yz(4.95)), C["load"], 3.0, 10)
    cv.line((-0.3, Yz(5.25)), (0.3, Yz(5.25)), C["load"], 3.0)
    cv.line((-0.3, Yz(4.95)), (-0.3, Yz(5.25)), C["load"], 3.0)
    cv.arrow((0.3, Yz(5.25)), (0.3, Yz(4.08)), C["load"], 3.0, 10)
    cv.text_px(cv.X(-0.45), cv.Y(Yz(3.5)), "外側下行 3 m", 11.5, C["load"], anchor="end", weight="700")
    cv.text_px(cv.X(0.45), cv.Y(Yz(4.65)), "內側上行 1 m", 11.5, C["load"], anchor="start", weight="700")
    cv.dot((0.3, Yz(4.0)), 5.5, fill=C["load"])
    cv.text_px(cv.X(0.5), cv.Y(Yz(4.0)) - 12, "A", 13, C["load"], anchor="start", weight="700")
    rows = ["Δh = 4 − 1 = %.1f m，L = 3 + 1 = %.1f m" % (dh, L),
            "i = Δh/L = %.2f，j = iγ_w = %.2f kN/m³（向上）" % (i, i * gw),
            "i_{cr} = γ'/γ_w = %.3f，FS = i_{cr}/i = %.2f ＞ 1" % (ic, ic / i),
            "現行規範 8.8.3：式 8.8-3 = %.2f ＜ 1.5、式 8.8-4 = %.2f ＜ 2.0" % (e83, e84),
            "⇒ 不符規範，有管湧（砂湧）之虞"]
    bx, by = cv.X(1.0), cv.Y(Yz(5.9))
    cv.rect_px(bx - 10, by - 22, 430, 118, "#FFFFFFF2", 8, C["load"], 1.4)
    for k, s in enumerate(rows):
        cv.text_px(bx, by + k * 21, s, 12, C["load"] if k == 4 else C["text"], anchor="start",
                   weight="700" if k == 4 else "400")
    return cv, i, ic / i, e83, e84


_cvf, _i, _fs, _e3, _e4 = fig_flowpath()
compose([_cvf], title="SM-2010-3　管湧：最短流徑只算砂層，FS 要和規範比",
        sub="FS = icr/i = %.2f 只表示平均坡降未達臨界；現行規範要求 1.5／2.0" % _fs,
        note="把黏土厚度算進流徑會低估坡降；只拿 FS 與 1.0 比，會把不符規範的設計判成安全。",
        path=os.path.join(OUT, "SM-2010-3-fig-2-flowpath.svg"))
print("i=%.3f FS=%.3f e83=%.3f e84=%.3f" % (_i, _fs, _e3, _e4))
