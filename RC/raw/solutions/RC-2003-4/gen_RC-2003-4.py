#!/usr/bin/env python3
"""
RC-2003-4 兩層樓剪力牆 — 題目附圖重繪腳本

用法：python3 gen_RC-2003-4.py [輸出目錄]（預設 figs/）
重繪依據：題目正本 RC-2003-4-problem.md §4 判讀清單（已確認）。只畫考卷給的東西。
FIGURES
  fig-1-problem  立面＋平面  攔：牆厚讀成 30、層高讀成 450+450、P 只算一個、900 當牆全長
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2003-4"

# ── 判讀清單（RC-2003-4-problem.md §4，已確認）──
L_CC = 900.0          # #1 邊界構材中心距
B_BE = 30.0           # #3 邊界構材 30×30
T_W = 15.0            # #2 腹版厚
H_UP, H_LO = 350.0, 450.0   # #4 屋頂–二樓、二樓–基礎面
L_W = L_CC + B_BE     # 牆全長（由 #1 推得，圖上不標尺寸）


def fig1_problem():
    W, H = 660, 680
    s = 0.5
    ev = Canvas(W, H, sx=s, ox=W / 2 - L_W * s / 2 + 20, oy=70)
    ev.panel("立面", "依題目正本判讀清單 #1、#4–#9")
    x0, x1 = 0.0, L_W
    yt = H_LO + H_UP
    # 牆與邊界構材
    ev.polygon([(x0, 0), (x1, 0), (x1, yt), (x0, yt)], "#EDF1F6", C["member"], 2.2)
    for xb in (x0, x1 - B_BE):
        ev.polygon([(xb, 0), (xb + B_BE, 0), (xb + B_BE, yt), (xb, yt)], "#DCE3EC", C["member"], 2.2)
    # 基礎面
    ev.line((x0 - 60, 0), (x1 + 60, 0), C["member"], 2.6)
    ev.text((x1 + 40, -34), "基礎面", 12.5, C["muted"])
    # 二樓
    ev.line((x0 + B_BE, H_LO), (x1 - B_BE, H_LO), C["member2"], 1.4, dash="5 4")
    # 載重：兩端 P、全長 w
    for xc in (B_BE / 2, L_W - B_BE / 2):
        ev.arrow((xc, yt + 130), (xc, yt + 4), C["load"], 3.0, 11)
        ev.math((xc, yt + 130), "P", 16, C["load"], dy=-12, weight="700")
    ev.udl((B_BE / 2 + 20, yt + 4), (L_W - B_BE / 2 - 20, yt + 4), 60, n=11, color=C["load"])
    ev.math((L_W * 0.3, yt + 64), "w", 16, C["load"], dy=-12, weight="700")
    # 地震力（向左）
    ev.arrow((L_W / 2 + 140, yt - 24), (L_W / 2 - 60, yt - 24), C["load"], 3.0, 11)
    ev.math((L_W / 2 + 160, yt - 24), "V_{R}", 16, C["load"], "start", weight="700")
    ev.arrow((L_W / 2 + 140, H_LO), (L_W / 2 - 60, H_LO), C["load"], 3.0, 11)
    ev.math((L_W / 2 + 160, H_LO), "V_{2}", 16, C["load"], "start", weight="700")
    # 樓層標記與尺寸
    ev.text((x0 - 95, yt), "屋頂", 13, C["text"])
    ev.text((x0 - 95, H_LO), "二樓", 13, C["text"])
    ev.dim((x0 - 30, yt), (x0 - 30, H_LO), "350 cm", off=10, label_off=26)
    ev.dim((x0 - 30, H_LO), (x0 - 30, 0), "450 cm", off=10, label_off=26)
    ev.dim((B_BE / 2, -60), (L_W - B_BE / 2, -60), "900 cm", off=0, label_off=16)
    ev.line((B_BE / 2, -2), (B_BE / 2, -70), C["dim"], 1, dash="3 3")
    ev.line((L_W - B_BE / 2, -2), (L_W - B_BE / 2, -70), C["dim"], 1, dash="3 3")

    # ---- 平面（厚度方向放大 4 倍以便標註）----
    W2, H2 = W, H
    ky = 4.0
    pl = Canvas(W2, H2, sx=s, ox=W2 / 2 - L_W * s / 2 + 10, oy=H2 / 2 - 10)
    pl.panel("平面（厚度方向放大 4 倍）", "依題目正本判讀清單 #1–#3")
    yc = 0.0
    hb, hw = B_BE * ky / 2, T_W * ky / 2
    pl.polygon([(B_BE, yc - hw), (L_W - B_BE, yc - hw), (L_W - B_BE, yc + hw), (B_BE, yc + hw)], "#EDF1F6", C["member"], 2.2)
    for xb in (0.0, L_W - B_BE):
        pl.polygon([(xb, yc - hb), (xb + B_BE, yc - hb), (xb + B_BE, yc + hb), (xb, yc + hb)], "#DCE3EC", C["member"], 2.2)
    pl.dim((B_BE / 2, yc + hb + 40), (L_W - B_BE / 2, yc + hb + 40), "900 cm", off=0, label_off=-14)
    for xc in (B_BE / 2, L_W - B_BE / 2):
        pl.line((xc, yc + hb + 2), (xc, yc + hb + 48), C["dim"], 1, dash="3 3")
    pl.dim((0, yc - hb - 30), (B_BE, yc - hb - 30), "30 cm", off=0, label_off=16)
    pl.dim((-40, yc + hb), (-40, yc - hb), "30 cm", off=0, label_off=24)
    pl.dim((L_W / 2, yc + hw), (L_W / 2, yc - hw), "15 cm", off=0, label_off=-26)
    pl.text((L_W - B_BE / 2, yc - hb - 52), "邊界構材", 12.5, C["muted"])
    pl.text_px(W2 / 2, H2 - 22, "900 cm 的兩條延伸線落在兩端邊界構材的中心", 12.5, C["accent"], weight="700")

    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([ev, pl], cols=2, title=f"{TAG} 題目附圖（圖 5，重繪）",
            sub="P＝50 tf 靜重＋25 tf 活重（兩端各一）；w＝5 tf/m 靜重＋1 tf/m 活重；VR＝30 tf、V2＝20 tf 地震力；皆為使用載重，已含自重",
            note="腹版厚 15 cm；邊界構材 30×30 cm；層高 350＋450 cm；牆全長 900＋30＝930 cm（由判讀 #1 推得）",
            path=path)
    return path


FIGURES = [(fig1_problem, "§1（題目正本 §4）", "牆厚讀成 30、層高 450+450、P 只算一個、900 當牆全長")]

# ══════════════════════════════════════════════════════════
# 解題圖解（2026-11-14 補繪；數值取自 RC-2003-4.md §4 Step 1–6，已驗證：盲解一致）
# ══════════════════════════════════════════════════════════
E_R, E_2 = 1.5 * 30.0, 1.5 * 20.0          # Step 1：地震力換到 αy＝1.0
H_W = H_UP + H_LO
M_U = E_R * H_W / 100 + E_2 * H_LO / 100   # 495 tf·m
F_OT = M_U / (L_CC / 100)                  # 覆沒軸力 55.0 tf
D_BE, L_BE = 50 + 5 * 4.5, 25 + 1 * 4.5    # 每端 BE 使用軸力
G_MAX = 1.2 * D_BE + 1.0 * L_BE            # 116.5
G_MIN = 0.9 * D_BE                         # 65.25
N_BE = 6                                   # Step 3：6-#8
S_BE, S_WEB = 15, 30                       # Step 3、4：箍筋 @15、腹版 #4@30


def fig2_wall_design():
    W, H = 980, 520
    s = 0.6
    a = Canvas(W, H, sx=s, ox=150, oy=170)
    HV = 420.0                                 # 立面高度（示意；兩層高度比例照 350／450）
    a.panel("覆沒彎矩 → 邊界構材軸力（地震向左）", "BE 力臂取中心距 9.0 m；E 已換到現行規範層級（×1.5）")
    yv = HV
    a.polygon([(0, 0), (L_W, 0), (L_W, yv), (0, yv)], "#EDF1F6", C["member"], 2.0)
    for x in (0, L_W - B_BE):
        a.polygon([(x, 0), (x + B_BE, 0), (x + B_BE, yv), (x, yv)], "#DCE3EC", C["member"], 2.0)
    a.arrow((L_W + 30, yv - 8), (L_W - 150, yv - 8), C["load"], 3.2, head=11)
    a.text((L_W + 40, yv - 8), f"E_R＝{E_R:.0f} tf", 13.5, C["load"], "start", weight="700")
    y2 = HV * H_LO / H_W
    a.arrow((L_W + 30, y2), (L_W - 150, y2), C["load"], 3.2, head=11)
    a.text((L_W + 40, y2), f"E_2＝{E_2:.0f} tf", 13.5, C["load"], "start", weight="700")
    a.line((-30, 0), (L_W + 30, 0), C["member"], 2.0)
    xl, xr = B_BE / 2, L_W - B_BE / 2
    a.arrow((xl, -6), (xl, -110), C["compr"], 3.6, head=11)
    a.text((xl + 18, -70), f"壓 {G_MAX:.1f}＋{F_OT:.1f}＝{G_MAX + F_OT:.1f} tf", 13.5, C["compr"], "start", weight="700")
    a.arrow((xr, -6), (xr, -110), C["compr"], 2.4, head=10)
    a.text((xr - 18, -70), f"壓 {G_MAX:.1f}−{F_OT:.1f}＝{G_MAX - F_OT:.1f} tf", 13.5, C["compr"], "end", weight="700")
    a.dim((xl, yv * 0.3), (xr, yv * 0.3), "900 cm（力臂）", off=0, label_off=-14, size=13)
    a.text_px(W / 2, H - 52, f"M_u＝{E_R:.0f}×8.0＋{E_2:.0f}×4.5＝{M_U:.0f} tf·m；F＝M_u/9.0＝{F_OT:.1f} tf（1.2D＋1.0L＋1.0E）", 13.5, C["text"], weight="700")
    a.text_px(W / 2, H - 28, f"0.9D＋1.0E 時另一端 {G_MIN:.2f}−{F_OT:.1f}＝{G_MIN - F_OT:.2f} tf：仍為壓力 → BE 不受拉，主筋由壓力控制", 13, C["bmd"], weight="700")

    b = Canvas(W, 520, sx=4.6, ox=60, oy=190)
    b.panel("斷面配筋（未依比例：腹版中段截斷）", f"BE 30×30：{N_BE}-#8、#4 閉合箍＋繫筋 @{S_BE}；腹版 t_w＝15：#4 @{S_WEB} 單層雙向")
    web_l = 55.0
    xs = [0.0, B_BE + web_l + 8, B_BE + 2 * web_l + 8]
    for k, x0 in enumerate((0.0, B_BE + 2 * web_l + 16)):
        b.polygon([(x0, 0), (x0 + B_BE, 0), (x0 + B_BE, B_BE), (x0, B_BE)], "#DCE3EC", C["member"], 2.2)
        b.polygon([(x0 + 4, 4), (x0 + 26, 4), (x0 + 26, 26), (x0 + 4, 26)], "none", C["deform"], 1.8)
        b.line((x0 + 15, 4), (x0 + 15, 26), C["deform"], 1.6)
        for i in range(3):
            for yb in (6.5, 23.5):
                b.circle((x0 + 6.5 + 8.5 * i, yb), 1.27, C["member"], C["member"], 1.0)
    yw0, yw1 = (B_BE - T_W) / 2, (B_BE + T_W) / 2
    for x0, x1 in ((B_BE, B_BE + web_l), (B_BE + web_l + 16, B_BE + 2 * web_l + 16)):
        b.polygon([(x0, yw0), (x1, yw0), (x1, yw1), (x0, yw1)], "#EDF1F6", C["member"], 2.0)
    for xb in (B_BE + web_l + 3, B_BE + web_l + 13):
        b.line((xb - 2, yw0 - 3), (xb + 2, yw1 + 3), C["member2"], 1.4)
    ym = B_BE / 2
    b.poly([(22, ym + 3), (22, ym), (B_BE + web_l, ym)], C["load"], 2.2)
    b.poly([(B_BE + web_l + 16, ym), (B_BE + 2 * web_l + 16 + 8, ym), (B_BE + 2 * web_l + 16 + 8, ym - 3)], C["load"], 2.2)
    for i in range(4):
        b.circle((B_BE + 8 + 15 * i, ym), 0.9, "#FFFFFF", C["member"], 1.4)
        b.circle((B_BE + web_l + 16 + 3 + 15 * i, ym), 0.9, "#FFFFFF", C["member"], 1.4)
    b.text((B_BE + web_l + 8, B_BE + 9), "紅線：水平筋 #4@30（單層，兩端彎鉤錨入 BE 核心，l_{dh}＝15 cm）", 13, C["load"], weight="700")
    b.text((B_BE + web_l + 8, -9), "空心圓：垂直筋 #4@30（h_w/l_w＝0.86 ≤ 2 → ρ_l ≥ ρ_t＝0.00282）", 13, C["member"], weight="700")
    b.text((B_BE / 2, -6), f"{N_BE}-#8", 13, C["text"], weight="700")
    b.text((B_BE + 2 * web_l + 16 + B_BE / 2, -6), f"{N_BE}-#8", 13, C["text"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-2-wall-design.svg")
    compose([a, b], cols=1, title=f"{TAG} 圖 2　剪力牆：覆沒軸力與斷面配筋",
            sub="l_w＝930 cm（BE 中心距 900）；h_w＝800 cm；現行規範組合 1.2D＋1.0L＋1.0E、0.9D＋1.0E",
            note="力臂用 BE 中心距 900 cm，不是 870 或 930；腹版厚 15 cm，不是 30",
            path=path)
    return path


FIGURES.append((fig2_wall_design, "§4 Step 2／Step 6", "力臂取錯、BE 被當成受拉、腹版厚讀成 30、垂直筋少於水平筋"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, where, catches in FIGURES:
        print(os.path.basename(fn()), "→", where, "攔：", catches)
