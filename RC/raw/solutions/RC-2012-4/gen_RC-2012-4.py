#!/usr/bin/env python3
"""
RC-2012-4 單跨抗彎構架（第二～四題共用附圖）— 題目附圖重繪腳本

用法：python3 gen_RC-2012-4.py [輸出目錄]（預設 figs/）
重繪依據：題目正本 RC-2012-4-problem.md §4 判讀清單（已確認）。只畫考卷給的東西。
FIGURES
  fig-1-problem  柱斷面＋E-W 剖面＋梁斷面  攔：48 cm 當核心或淨尺寸、6 cm 當淨保護層、圖示柱當內柱
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2012-4"

# ══════════════════════════════════════════════════════════
# 題目附圖重繪（2026-11-14，RC-U3-3 批 1；第二～四題共用附圖）
# 依題目正本 RC-2012-4-problem.md §4 判讀清單 G1–G7（已確認）。只畫考卷給的東西。
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
# 解題圖解（2026-11-14 補繪；數值取自 RC-2012-4.md §4 Step 1–6，已驗證：盲解一致）
# ══════════════════════════════════════════════════════════
from structdraw import Canvas, C, compose
import math
FC, FY = 280.0, 4200.0
AS_TOP = 6 * 5.07                     # 6-#8
T1 = 1.25 * FY * AS_TOP / 1000        # Step 1：159.7 tf
M_PR_NEG = 75.52                      # RC-2012-2 M_pr^-（tf·m）
VCOL = M_PR_NEG / P_LN_COL            # Step 2：25.17 tf
VJH = T1 - VCOL                       # Step 2：134.5 tf
AJ = P_COL_B * P_COL_B                # Step 4：60×60
PHI_VN = 0.85 * 3.2 * math.sqrt(FC) * AJ / 1000   # Step 5：163.85 tf


def fig2_joint_fbd():
    PW, PH = 520, 470
    s = 2.3
    a = Canvas(PW, PH, sx=s, ox=120, oy=150)
    a.panel("接頭上半部自由體（EQ 向右）", "梁端 M_{pr}^{-}：頂筋受拉")
    cb, hb = P_COL_B, P_BM_H
    a.polygon([(0, -22), (cb, -22), (cb, hb + 48), (0, hb + 48)], "#EDF1F6", C["member"], 2.2)
    for yy in (-22, hb + 48):
        a.line((-8, yy), (cb + 8, yy), C["member2"], 1.4, dash="4 3")
    a.polygon([(cb, 0), (cb + 80, 0), (cb + 80, hb), (cb, hb)], "#EDF1F6", C["member"], 2.2)
    a.line((cb + 80, -6), (cb + 80, hb + 6), C["member2"], 1.4, dash="4 3")
    a.polygon([(0, 0), (cb, 0), (cb, hb), (0, hb)], C["fill_m"], C["bmd"], 2.0)
    a.line((-12, hb / 2), (cb + 12, hb / 2), C["bmd"], 1.6, dash="6 4")
    yt = hb - P_BM_E
    a.poly([(cb + 78, yt), (8, yt), (8, P_BM_E), (cb + 78, P_BM_E)], C["load"], 2.2)
    a.arrow((cb + 10, yt), (cb + 60, yt), C["load"], 4.0, head=12)
    a.text((cb + 35, yt + 13), f"T_1＝{T1:.1f} tf", 14, C["load"], weight="700")
    a.arrow((cb - 6, hb + 30), (8, hb + 30), C["deform"], 3.4, head=11)
    a.text((cb / 2, hb + 40), f"V_{{col}}＝{VCOL:.2f} tf", 14, C["deform"], weight="700")
    a.arrow((cb - 4, hb / 2 + 7), (6, hb / 2 + 7), C["bmd"], 3.0, head=10)
    a.text((cb / 2, hb / 2 + 17), f"V_{{jh}}＝{VJH:.1f} tf", 14, C["bmd"], weight="700")
    a.text((cb + 40, -12), "梁（淨跨 7 m）", 12, C["muted"])
    a.text_px(PW / 2, PH - 58, "取接頭水平中線以上：T_1 向右、柱剪力向左", 13, C["text"], weight="700")
    a.text_px(PW / 2, PH - 34, f"V_{{jh}}＝T_1 − V_{{col}}＝{T1:.1f} − {VCOL:.2f}＝{VJH:.1f} tf", 13, C["bmd"], weight="700")

    b = Canvas(PW, PH)
    b.panel("需求 vs 強度（角隅外接頭，γ＝3.2）", f"A_j＝60×60＝{AJ:.0f} cm^{{2}}，φ＝0.85")
    rows = (("V_{jh}", VJH, C["bmd"], "本解：T_1 − V_{col}", False),
            ("T_1 + V_{col}", T1 + VCOL, C["load"], "符號錯：柱剪力當加項", True),
            ("φV_n", PHI_VN, C["deform"], "強度：3.2√f'c A_j × 0.85", False))
    x0, x1 = 150, PW - 80
    vmax = max(r[1] for r in rows) * 1.02
    for i, (name, v, col, tag, hollow) in enumerate(rows):
        y = 120 + i * 88
        wpx = (x1 - x0) * v / vmax
        b.rect_px(x0, y, wpx, 32, "#FFFFFF" if hollow else col, rx=6, stroke=col, sw=2 if hollow else 0)
        b.text_px(x0 - 12, y + 16, name, 15, col, anchor="end", weight="700")
        b.text_px(x0 + wpx + 6, y + 16, (f"{v:.2f}" if name.startswith("φ") else f"{v:.1f}"), 14, col, anchor="start", weight="700")
        b.text_px(x0, y + 48, tag, 12, C["muted"], anchor="start")
    b.text_px(PW / 2, PH - 58, f"本解 V_{{jh}}/φV_n＝{VJH / PHI_VN:.2f} → 足夠", 13.5, C["bmd"], weight="700")
    b.text_px(PW / 2, PH - 34, f"柱剪力當加項：{T1 + VCOL:.1f} tf 大於 φV_n → 誤判不足", 13, C["load"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-2-joint-fbd.svg")
    compose([a, b], title=f"{TAG} 圖 2　外接頭水平剪力：自由體與檢核",
            sub="柱 60×60；梁 50×60 頂 6-#8（1.25fy）；柱剪力由梁端可能彎矩經上下柱各半分擔、淨高 3 m",
            note="柱剪力與梁筋拉力方向相反，是減項",
            path=path)
    return path


FIGURES.append((fig2_joint_fbd, "§4 Step 2", "V_jh 寫成 T_1＋V_col（柱剪力方向畫反）"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, where, catches in FIGURES:
        print(os.path.basename(fn()), "→", where, "攔：", catches)
