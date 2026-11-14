#!/usr/bin/env python3
"""
RC-2003-3 梁柱接頭組件 — 題目附圖重繪腳本

用法：python3 gen_RC-2003-3.py [輸出目錄]（預設 figs/）
重繪依據：題目正本 RC-2003-3-problem.md §4 判讀清單（已確認）。只畫考卷給的東西。
FIGURES
  fig-1-problem  斷面 A-A 平面＋斷面 B-B  攔：柱 X／Y 讀反、X 向梁當成置中
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2003-3"

# ── 判讀清單（RC-2003-3-problem.md §4，已確認）──
COL_X, COL_Y = 40.0, 50.0      # #1 柱 X 向 40、Y 向 50
BW_X, H_X = 24.0, 60.0         # #4 X 向梁 24×60
BW_Y = 40.0                    # #7 Y 向梁寬 40（＝柱 X 向）
FLUSH_TOP = True               # #2 X 向梁上緣與柱 +Y 面齊平
N_TOP, N_BOT = 4, 2            # #4 頂 4-#6、底 2-#6
STUB = 26.0                    # 梁畫出的長度（示意，斷線收尾）


def fig1_problem():
    # ---- 斷面 A-A 平面 ----
    W, H = 600, 540
    s = 4.6
    pa = Canvas(W, H, sx=s, ox=W / 2 - COL_X * s / 2 - 45, oy=H / 2 - COL_Y * s / 2 - 30)
    pa.panel("斷面 A-A（平面）", "依題目正本判讀清單 #1–#3")
    y_top = COL_Y
    yb_hi = y_top if FLUSH_TOP else (COL_Y + BW_X) / 2
    yb_lo = yb_hi - BW_X
    fill = "#EDF1F6"
    # X 向梁（左右）
    for x0, x1 in ((-STUB, 0.0), (COL_X, COL_X + STUB)):
        pa.polygon([(x0, yb_lo), (x1, yb_lo), (x1, yb_hi), (x0, yb_hi)], fill, "none")
        pa.line((x0, yb_lo), (x1, yb_lo), C["member"], 2.2)
        pa.line((x0, yb_hi), (x1, yb_hi), C["member"], 2.2)
        xe = x0 if x0 < 0 else x1
        pa.line((xe, yb_lo - 2), (xe, yb_hi + 2), C["member2"], 1.4, dash="4 3")
    # Y 向梁（上下，寬同柱）
    for y0, y1 in ((COL_Y, COL_Y + STUB * 0.55), (-STUB * 0.55, 0.0)):
        pa.polygon([(0, y0), (BW_Y, y0), (BW_Y, y1), (0, y1)], fill, "none")
        pa.line((0, y0), (0, y1), C["member"], 2.2)
        pa.line((BW_Y, y0), (BW_Y, y1), C["member"], 2.2)
        ye = y1 if y1 > COL_Y else y0
        pa.line((-2, ye), (BW_Y + 2, ye), C["member2"], 1.4, dash="4 3")
    # 柱
    pa.polygon([(0, 0), (COL_X, 0), (COL_X, COL_Y), (0, COL_Y)], "#DCE3EC", C["member"], 2.8)
    pa.text((COL_X / 2, COL_Y / 2 - 9), "柱", 15, C["text"], weight="700")
    pa.text((-STUB / 2, (yb_lo + yb_hi) / 2), "X 向梁", 12.5, C["muted"])
    pa.text((COL_X + STUB * 0.32, (yb_lo + yb_hi) / 2), "X 向梁", 12.5, C["muted"])
    pa.text((COL_X / 2, COL_Y + STUB * 0.27), "Y 向梁 40×65", 12.5, C["muted"])
    pa.text((COL_X / 2, -STUB * 0.45), "Y 向梁", 12.5, C["muted"])
    # 尺寸
    pa.dim((0, COL_Y + STUB * 0.55), (COL_X, COL_Y + STUB * 0.55), "40 cm", off=-18, label_off=-14)
    pa.dim((COL_X + STUB, COL_Y), (COL_X + STUB, 0), "50 cm", off=-60, label_off=-30)
    pa.dim((COL_X + STUB, yb_hi), (COL_X + STUB, yb_lo), "24 cm", off=-8, label_off=-26)
    pa.line((COL_X, 0), (COL_X + STUB + 14, 0), C["dim"], 1, dash="3 3")
    # 座標軸
    pa.axes((-STUB + 1, -STUB * 0.5), lx=10, ly=10, labels=("X", "Y"))
    pa.text_px(W / 2, H - 22, "X 向梁上緣與柱上緣齊平（偏心），不是置中", 12.5, C["accent"], weight="700")

    # ---- 斷面 B-B ----
    W2 = W
    s2 = 5.2
    pb = Canvas(W2, H, sx=s2, ox=W2 / 2 - BW_X * s2 / 2 + 6, oy=H / 2 - H_X * s2 / 2 - 4)
    pb.panel("斷面 B-B（X 向梁）", "箍筋未示")
    pb.polygon([(0, 0), (BW_X, 0), (BW_X, H_X), (0, H_X)], "#EDF1F6", C["member"], 2.4)
    for n, y in ((N_TOP, H_X - 5), (N_BOT, 5)):
        for i in range(n):
            x = 5 + (BW_X - 10) * i / (n - 1)
            pb.circle((x, y), 1.0, C["member"], C["member"], 1.2)
    pb.text((BW_X + 4, H_X - 5), "4-#6", 14, C["text"], "start")
    pb.text((BW_X + 4, 5), "2-#6", 14, C["text"], "start")
    pb.dim((0, H_X), (BW_X, H_X), "24 cm", off=-20, label_off=-14)
    pb.dim((0, H_X), (0, 0), "60 cm", off=26, label_off=24)

    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([pa, pb], title=f"{TAG} 題目附圖（圖 4，重繪）",
            sub="柱 X 向 40、Y 向 50；X 向梁 24×60（頂 4-#6、底 2-#6）兩側框入，上緣貼齊柱面；Y 向梁 40×65 寬同柱",
            note="X 向接頭深度 h = 40 cm；X 向梁軸線距柱近側面 12 cm、遠側面 38 cm",
            path=path)
    return path


FIGURES = [(fig1_problem, "§1（題目正本 §4）", "柱 X／Y 讀反、X 向梁當成置中")]

# ══════════════════════════════════════════════════════════
# 解題圖解（2026-11-14 補繪；數值取自 RC-2003-3.md §4 Step 1–6，已驗證：盲解一致）
# ══════════════════════════════════════════════════════════
import math
FC = 280.0
GAMMA = 3.9                    # Step 5 一雙對面受圍束（現行規範表 18.5.4.3）
PHI_J = 0.85
VU = 77.55                     # Step 3 V_u（tf）


def bj_eff(b, h_col, width_col, x_near):
    """有效接頭寬：min(b+h, b+2x) ≤ 柱寬；x＝梁緣至柱側面較小距離"""
    return min(b + h_col, b + 2 * x_near, width_col)


def fig2_joint_width():
    W, H = 470, 470
    s = 4.4
    panels = []
    cases = (("本題：X 向梁貼齊柱面", COL_Y - BW_X),        # 梁上緣齊平 → 梁下緣距柱 +Y 面 24
             ("對照：若 X 向梁置中", (COL_Y + BW_X) / 2))
    for title, yb_hi in cases:
        yb_lo = yb_hi - BW_X if title.startswith("對照") else COL_Y - BW_X
        yb_hi = yb_lo + BW_X
        x_near = min(yb_lo, COL_Y - yb_hi)
        bj = bj_eff(BW_X, COL_X, COL_Y, x_near)
        aj = bj * COL_X
        vn = GAMMA * math.sqrt(FC) * aj / 1000
        phivn = PHI_J * vn
        cv = Canvas(W, H, sx=s, ox=W / 2 - COL_X * s / 2, oy=118)
        ok = phivn >= VU
        cv.panel(title, f"x＝{x_near:.0f} cm → b_j＝min(b+h, b+2x)＝{bj:.0f} cm")
        for x0, x1 in ((-16.0, 0.0), (COL_X, COL_X + 16.0)):
            cv.polygon([(x0, yb_lo), (x1, yb_lo), (x1, yb_hi), (x0, yb_hi)], "#EDF1F6", C["member"], 1.8)
        cv.polygon([(0, 0), (COL_X, 0), (COL_X, COL_Y), (0, COL_Y)], "#F4F6F9", C["member"], 2.6)
        yc = (yb_lo + yb_hi) / 2
        ja, jb = max(0.0, yc - bj / 2), min(COL_Y, yc + bj / 2)
        cv.polygon([(0, ja), (COL_X, ja), (COL_X, jb), (0, jb)], C["fill_m"], C["bmd"], 2.0)
        cv.line((-16, yc), (COL_X + 16, yc), C["muted"], 1.0, dash="6 4")
        cv.text((COL_X / 2, (ja + jb) / 2), f"A_j＝{aj:.0f} cm^{{2}}", 14, C["bmd"], weight="700", dy=-14)
        cv.dim((0, COL_Y), (COL_X, COL_Y), "h = 40 cm", off=-16, label_off=-14, size=12.5)
        cv.dim((COL_X + 16, jb), (COL_X + 16, ja), f"b_j = {bj:.0f}", off=-10, label_off=-30, size=12.5)
        cv.dim((-16, COL_Y), (-16, 0), "50", off=10, label_off=14, size=12.5)
        cv.arrow((-14, yc + 3), (-2, yc + 3), C["load"], 2.6, head=8)
        cv.text_px(W / 2, H - 70, f"φV_n＝0.85×{GAMMA}√f'c×{aj:.0f}＝{round(phivn, 2):g} tf", 13.5, C["text"], weight="700")
        cv.text_px(W / 2, H - 44, f"V_u＝{VU} tf → {'符合' if ok else '不符合'}", 13.5,
                   C["deform"] if ok else C["load"], weight="700")
        panels.append(cv)
    path = os.path.join(OUT, f"{TAG}-fig-2-joint-width.svg")
    compose(panels, title=f"{TAG} 圖 2　X 向接頭有效寬：偏心梁 vs 置中梁",
            sub="平面（X 向右、Y 向上）；綠色為 X 向剪力的有效接頭面積（有效寬 × 柱 X 向深 40 cm）；紅箭頭為梁筋拉力方向",
            note="梁軸線離柱側面越近，有效寬越窄——偏心時不能拿柱寬 50 cm 當有效寬",
            path=path)
    return path


FIGURES.append((fig2_joint_width, "§4 Step 4", "偏心梁仍取 b_j＝柱寬 50 cm（高估 A_j 一倍、結論由不符合變符合）"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, where, catches in FIGURES:
        print(os.path.basename(fn()), "→", where, "攔：", catches)
