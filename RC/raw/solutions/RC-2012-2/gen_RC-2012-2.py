#!/usr/bin/env python3
"""
RC-2012-2 單跨抗彎構架（第二～四題共用附圖）— 題目附圖重繪腳本

用法：python3 gen_RC-2012-2.py [輸出目錄]（預設 figs/）
重繪依據：題目正本 RC-2012-2-problem.md §4 判讀清單（已確認）。只畫考卷給的東西。
FIGURES
  fig-1-problem  柱斷面＋E-W 剖面＋梁斷面  攔：48 cm 當核心或淨尺寸、6 cm 當淨保護層、圖示柱當內柱
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2012-2"

# ══════════════════════════════════════════════════════════
# 題目附圖重繪（2026-11-14，RC-U3-3 批 1；第二～四題共用附圖）
# 依題目正本 RC-2012-2-problem.md §4 判讀清單 G1–G7（已確認）。只畫考卷給的東西。
# 本段在 RC-2012-2／3／4 三支腳本各存一份（腳本須可獨立重跑）
# ══════════════════════════════════════════════════════════
P_COL_B = 60.0            # G2 柱 60×60
P_COL_E = 6.0             # G2 主筋中心距柱面
P_COL_N = 4               # G2 每邊 4 根（12-#7）
P_BM_B, P_BM_H = 50.0, 60.0   # G3 梁 50×60
P_BM_E = 6.0              # G3 主筋中心距梁面
P_N_TOP, P_N_BOT = 6, 4   # G3 頂 6-#8、底 4-#7
P_LN_COL, P_LN_BM = 3.0, 7.0  # G4 柱淨高、梁淨跨（m）


def fig_problem_2012():
    from structdraw import Canvas, C, compose
    PW, PH = 440, 520
    # ---- 柱斷面 ----
    s = 4.2
    a = Canvas(PW, PH, sx=s, ox=PW / 2 - P_COL_B * s / 2 + 6, oy=100)
    a.panel("柱斷面（2 樓與 3 樓）", "判讀 G2；箍筋考卷未畫")
    B, e = P_COL_B, P_COL_E
    a.polygon([(0, 0), (B, 0), (B, B), (0, B)], "#EDF1F6", C["member"], 2.4)
    xs = [e + (B - 2 * e) * i / (P_COL_N - 1) for i in range(P_COL_N)]
    pts = {(x, y) for x in xs for y in (e, B - e)} | {(x, y) for x in (e, B - e) for y in xs}
    for p in sorted(pts):
        a.circle(p, 1.11, C["member"], C["member"], 1.0)
    a.text((B / 2, B / 2), "12-#7", 15, C["text"], weight="700")
    a.dim((0, B), (B, B), "60 cm", off=-22, label_off=-14)
    a.dim((B, B), (B, 0), "60 cm", off=-24, label_off=-30)
    a.dim((0, B - e), (0, e), "48 cm", off=36, label_off=28)
    a.dim((0, B), (0, B - e), "6", off=14, label_off=12, size=12)
    a.dim((0, e), (0, 0), "6", off=14, label_off=12, size=12)
    a.dim((B - e, 0), (B, 0), "6 cm", off=20, label_off=14, size=12)
    a.text_px(PW / 2, PH - 30, "6 cm、48 cm 都量到主筋中心", 12.5, C["accent"], weight="700")

    # ---- E-W 向剖面 ----
    s2 = 0.75
    b = Canvas(PW, PH, sx=s2, ox=60, oy=-25)
    b.panel("E-W 向剖面（外圍）", "判讀 G1、G4、G7")
    cw = P_COL_B
    yb0, yb1 = 300.0, 300.0 + P_BM_H        # 梁底、梁頂（cm）
    ybot_col = 100.0                          # 下柱畫出一段（淨高 3 m，示意截斷）
    ytop = yb1 + 140.0                        # 上柱畫出一段
    b.polygon([(0, ybot_col), (cw, ybot_col), (cw, ytop), (0, ytop)], "#EDF1F6", C["member"], 2.2)
    b.polygon([(cw, yb0), (cw + 380, yb0), (cw + 380, yb1), (cw, yb1)], "#EDF1F6", C["member"], 2.2)
    b.line((cw + 380, yb0 - 10), (cw + 380, yb1 + 10), C["member2"], 1.4, dash="4 3")
    for yy in (ybot_col, ytop):
        b.line((-10, yy), (cw + 10, yy), C["member2"], 1.4, dash="4 3")
    for xx in (8.0, 22.0, 38.0, 52.0):
        b.line((xx, ybot_col), (xx, ytop), C["member"], 1.6)
    yt, ybot = yb1 - P_BM_E, yb0 + P_BM_E
    b.poly([(cw + 374, yt), (12, yt), (12, ybot), (cw + 374, ybot)], C["load"], 3.0)
    b.text((cw + 120, yt + 22), "6-#8", 13, C["text"])
    b.text((cw + 120, ybot - 22), "4-#7", 13, C["text"])
    b.text((cw + 190, (yb0 + yb1) / 2), "（梁淨跨距＝7 m）", 12.5, C["muted"])
    b.text((cw + 150, yb1 + 85), "3 樓淨高＝3 m", 13, C["text"])
    b.text((cw + 150, yb0 - 85), "2 樓淨高＝3 m", 13, C["text"])
    b.text_px(PW / 2, PH - 30, "柱左側沒有梁：單跨構架的外柱", 12.5, C["accent"], weight="700")

    # ---- 梁斷面 ----
    s3 = 4.2
    c = Canvas(PW, PH, sx=s3, ox=PW / 2 - P_BM_B * s3 / 2 + 6, oy=100)
    c.panel("梁斷面", "判讀 G3")
    bw, h, e2 = P_BM_B, P_BM_H, P_BM_E
    c.polygon([(0, 0), (bw, 0), (bw, h), (0, h)], "#EDF1F6", C["member"], 2.4)
    for n, y, rr in ((P_N_TOP, h - e2, 1.27), (P_N_BOT, e2, 1.11)):
        for i in range(n):
            x = e2 + (bw - 2 * e2) * i / (n - 1)
            c.circle((x, y), rr, C["member"], C["member"], 1.0)
    c.text((bw / 2, h - e2 - 5), "6-#8", 14, C["text"], weight="700")
    c.text((bw / 2, e2 + 5), "4-#7", 14, C["text"], weight="700")
    c.dim((0, h), (bw, h), "50 cm", off=-22, label_off=-14)
    c.dim((bw, h), (bw, 0), "60 cm", off=-24, label_off=-30)
    c.dim((0, h - e2), (0, e2), "48 cm", off=36, label_off=28)
    c.dim((0, h), (0, h - e2), "6", off=14, label_off=12, size=12)
    c.dim((0, e2), (0, 0), "6", off=14, label_off=12, size=12)
    c.text_px(PW / 2, PH - 30, "d＝54 cm、d′＝6 cm（量到主筋中心）", 12.5, C["accent"], weight="700")

    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([a, b, c], cols=3, title=f"{TAG} 題目附圖（第二～四題共用，重繪）",
            sub="單跨多層抗彎構架 2、3 樓外圍；f'c＝280、所有鋼筋 fy＝4200 kgf/cm²；Nu＝50 tf；wu＝6.1 tf/m",
            note="附圖只有 E-W 向剖面；N-S 向梁考卷沒有畫也沒有寫",
            path=path)
    return path

FIGURES = [(fig_problem_2012, "§1（題目正本 §4）", "48 cm 當核心或淨尺寸、6 cm 當淨保護層、圖示柱當內柱")]

# ══════════════════════════════════════════════════════════
# 解題圖解（2026-11-14 補繪；數值取自 RC-2012-2.md §4，已驗證：盲解一致）
# ══════════════════════════════════════════════════════════
from structdraw import Canvas, C, compose
import math
FC, FY = 280.0, 4200.0
FPS = 1.25 * FY                                  # Step 1
D_EFF = P_BM_H - P_BM_E                          # Step 2：d＝54
AS_T, AS_B = 6 * 5.07, 4 * 3.87                  # 6-#8、4-#7


def mpr(As):
    T = As * FPS
    a = T / (0.85 * FC * P_BM_B)
    return T / 1000, a, (D_EFF - a / 2), T * (D_EFF - a / 2) / 1e5


def fig2_mpr():
    PW, PH = 470, 500
    panels = []
    for case in ("neg", "pos"):
        As = AS_T if case == "neg" else AS_B
        T, a, z, M = mpr(As)
        s = 3.4
        cv = Canvas(PW, PH, sx=s, ox=125, oy=170)
        top_tension = case == "neg"
        cv.panel("M_{pr}^{-}：頂筋 6-#8 受拉" if top_tension else "M_{pr}^{+}：底筋 4-#7 受拉",
                 "地震使梁端反覆受彎，兩個方向都要算")
        b, h, e = P_BM_B, P_BM_H, P_BM_E
        cv.polygon([(0, 0), (b, 0), (b, h), (0, h)], "#EDF1F6", C["member"], 2.4)
        ya, yb = (0, a) if top_tension else (h - a, h)
        cv.polygon([(0, ya), (b, ya), (b, yb), (0, yb)], C["fill_c"], C["compr"], 1.8)
        yT = h - e if top_tension else e
        n, r = (6, 1.27) if top_tension else (4, 1.11)
        for i in range(n):
            cv.circle((e + (b - 2 * e) * i / (n - 1), yT), r, C["tension"], C["tension"], 1.0)
        yo = e if top_tension else h - e
        no, ro = (4, 1.11) if top_tension else (6, 1.27)
        for i in range(no):
            cv.circle((e + (b - 2 * e) * i / (no - 1), yo), ro, "#FFFFFF", C["member2"], 1.4)
        yC = (ya + yb) / 2
        cv.arrow((b + 4, yT), (b + 20, yT), C["tension"], 3.4, head=10)
        cv.text((b + 4, yT + (5 if top_tension else -5)), f"T＝{T:.1f} tf", 13.5, C["tension"], "start", weight="700")
        cv.arrow((b + 20, yC), (b + 4, yC), C["compr"], 3.4, head=10)
        cv.text((b + 4, yC - (5 if top_tension else -5)), f"C＝{T:.1f} tf", 13.5, C["compr"], "start", weight="700")
        cv.dim((-4, yb), (-4, ya), f"a = {a:.2f}", off=14, label_off=34, size=12.5)
        cv.dim((b + 28, yT), (b + 28, yC), f"z = {z:.2f}", off=-6, label_off=-34, size=12.5)
        cv.dim((0, -2), (b, -2), "50 cm", off=14, label_off=14, size=12.5)
        cv.text_px(PW / 2, PH - 70, f"T＝{As:.2f}×1.25×4200＝{T:.1f} tf；z＝d − a/2", 13, C["text"])
        cv.text_px(PW / 2, PH - 42, f"M_{{pr}}＝{T:.1f}×{z / 100:.4f}＝{M:.1f} tf·m",
                   14.5, C["bmd"], weight="700")
        panels.append(cv)
    path = os.path.join(OUT, f"{TAG}-fig-2-mpr.svg")
    compose(panels, title=f"{TAG} 圖 2　梁端可能彎矩強度的兩個方向",
            sub="梁 50×60，d＝54 cm；鋼筋應力取 1.25fy＝1.25×4200、φ＝1；藍色為等值應力塊（0.85f'c），力臂量到應力塊形心",
            note="負彎矩應力塊在梁底、正彎矩在梁頂；壓力筋（空心）未計入，計入時負彎矩可能強度約 77.9 tf·m",
            path=path)
    return path


FIGURES.append((fig2_mpr, "§4 結論彙整", "用 fy 算 M_n 當 M_pr、正負向用錯鋼筋、應力塊畫在受拉側"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, where, catches in FIGURES:
        print(os.path.basename(fn()), "→", where, "攔：", catches)
