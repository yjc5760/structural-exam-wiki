# -*- coding: utf-8 -*-
"""SM-2009-3 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2009-3-problem.md §4 判讀清單（#1–#5），不含任何解題結果。
fig-2-profile：解題圖解（2026-11-15 階段 E），σ、u、σ' 沿深度，數值取自解析 §4。
用法：python gen_SM-2009-3.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *                                      # Canvas, C, compose, fit, soil_fill, wt_symbol
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
WT   = 0.0     # #1 地下水位在地表
H_CL = 3.0     # #2 黏土層厚（地表→A）
H_AB = 2.0     # #3 A→B
H_BC = 2.0     # #3 B→C（砂土層底）
H_PZ = 1.0     # #5 水壓計水位高出地表
Z_A, Z_B, Z_C = H_CL, H_CL + H_AB, H_CL + H_AB + H_BC
XL, XR = -4.0, 6.0
XP = 0.9      # 水壓計位置（示意）

def fig_problem():
    W, H = 900, 560
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (XL - 1.4, XR + 1.0), (-(Z_C + 0.8), H_PZ + 1.0), 30, 30, 20, 20))
    Y = lambda d: -d
    soil_fill(cv, XL, XR, Y(Z_A), Y(0), "rgba(63,74,90,0.20)")
    soil_fill(cv, XL, XR, Y(Z_C), Y(Z_A), "rgba(180,83,9,0.20)")
    for d, w in ((0, 2.6), (Z_A, 1.8), (Z_C, 2.2)):
        cv.line((XL, Y(d)), (XR, Y(d)), C["member"], w)
    # 地下水位（地表）
    wt_symbol(cv, 2.6, Y(WT) + 0.09 * 2.4, C["deform"], 0.09)
    cv.text((3.0, Y(WT) + 0.45), "地下水位（地表面）", 12.5, C["deform"], anchor="start", weight="700")
    # 水壓計：雙線管由地表上方到 C
    for dx in (-0.12, 0.12):
        cv.line((XP + dx, Y(-H_PZ - 0.5)), (XP + dx, Y(Z_C)), C["member"], 1.8)
    cv.polygon([(XP - 0.12, Y(-H_PZ)), (XP + 0.12, Y(-H_PZ)), (XP + 0.12, Y(Z_C)), (XP - 0.12, Y(Z_C))],
               "rgba(29,78,216,0.25)")
    cv.line((XP - 0.4, Y(-H_PZ)), (XP + 0.4, Y(-H_PZ)), C["deform"], 1.8)
    cv.text((XP - 0.5, Y(-H_PZ) + 0.6), "水壓計", 12.5, C["muted"], anchor="end")
    cv.dim((XP - 0.75, Y(0)), (XP - 0.75, Y(-H_PZ)), "1.0 m", 0, C["dim"], 12.5, label_off=-28)
    # 點位
    for z, lab in ((Z_A, "A"), (Z_B, "B"), (Z_C, "C")):
        cv.dot((3.2, Y(z)), 6, fill=C["text"])
        cv.text((3.6, Y(z) + 0.0), lab, 15, C["text"], anchor="start", weight="700")
    # 層名與參數
    cv.text((-3.7, Y(1.2)), "飽和黏土", 13.5, C["text"], anchor="start", weight="700")
    cv.text((-3.7, Y(1.95)), "ω = 30%，e = 0.8", 12.5, C["text"], anchor="start")
    cv.text((-3.7, Y(4.6)), "飽和砂土（受壓水層）", 13.5, C["text"], anchor="start", weight="700")
    cv.text((-3.7, Y(5.35)), "Gs = 2.65，ω = 18.5%", 12.5, C["text"], anchor="start")
    # 尺寸線（右側，端點對齊判讀清單 #2、#3）
    xd = XR - 0.6
    cv.dim((xd, Y(Z_A)), (xd, Y(0)), "3 m", 0, C["dim"], 12.5, label_off=26)
    cv.dim((xd, Y(Z_B)), (xd, Y(Z_A)), "2 m", 0, C["dim"], 12.5, label_off=26)
    cv.dim((xd, Y(Z_C)), (xd, Y(Z_B)), "2 m", 0, C["dim"], 12.5, label_off=26)
    cv.line((3.2, Y(Z_B)), (xd, Y(Z_B)), C["dim"], 0.9, dash="2 3")
    return cv

compose([fig_problem()],
        title="SM-2009-3 題目附圖重繪",
        sub="依題目正本判讀清單；水壓計量測點在砂土層底 C，管內水位高出地表 1.0 m",
        note="攔錯用：A 是砂土頂（黏土底），水壓計讀的是受壓砂土層的水頭，不是地表水位的靜水壓。",
        path=os.path.join(OUT, "SM-2009-3-fig-1-problem.svg"))

# ── 深度剖面共用小工具（本檔自含，不改 geo.py）──
def depth_profile(W, H, zmax, smin, smax, sticks, zticks, layers, curves, labels, legend_xy=None,
                  L=96, R=230, T=40, B=70, ylab="深度（m）", xlab="應力（kPa）"):
    """curves: [(pts[(z, s)...], 色, 線寬, dash, 圖例)]，同一深度可重複以畫跳躍。
    labels: [(z, s, 文字, 色, anchor, dy)]；layers: [(z0, z1, 填色, 名稱)]"""
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (0, 1.0), (-1.0, 0), L, R, T, B))
    SX = lambda s: (s - smin) / (smax - smin)
    SY = lambda z: -z / zmax
    for z0, z1, col, name in layers:
        cv.polygon([(0, SY(z0)), (1.0, SY(z0)), (1.0, SY(z1)), (0, SY(z1))], col)
        cv.text_px(cv.X(1.0) + 10, (cv.Y(SY(z0)) + cv.Y(SY(z1))) / 2, name, 12, C["muted"], anchor="start")
    for v in sticks:
        cv.line((SX(v), -1.0), (SX(v), 0), C["border"], 1.0)
        cv.text_px(cv.X(SX(v)), cv.Y(-1.0) + 17, "%g" % v, 12.5, C["muted"])
    for z in zticks:
        cv.line((0, SY(z)), (1.0, SY(z)), C["border"], 1.0, dash="3 3")
        cv.text_px(cv.X(0) - 9, cv.Y(SY(z)), "%g" % z, 12.5, C["muted"], anchor="end")
    if smin < 0:
        cv.line((SX(0), -1.0), (SX(0), 0), C["muted"], 1.4)
    cv.line((0, 0), (1.0, 0), C["muted"], 1.9)
    cv.line((0, 0), (0, -1.0), C["muted"], 1.9)
    cv.text_px((cv.X(0) + cv.X(1.0)) / 2, cv.Y(-1.0) + 44, xlab, 13.5, C["text"])
    cv.text_px(cv.X(0) - 52, (cv.Y(0) + cv.Y(-1.0)) / 2, ylab, 13.5, C["text"])
    for pts, col, w, dash, _ in curves:
        cv.poly([(SX(s), SY(z)) for z, s in pts], col, w, dash=dash)
        for z, s in pts:
            cv.dot((SX(s), SY(z)), 3.6, fill=col)
    for z, s, txt, col, anc, dy in labels:
        tag_px(cv, cv.X(SX(s)) + (10 if anc == "start" else -10 if anc == "end" else 0),
               cv.Y(SY(z)) + dy, txt, 12, col, anchor=anc, weight="700")
    if legend_xy:
        lx, ly = legend_xy
        k = 0
        for pts, col, w, dash, lab in curves:
            if not lab: continue
            d_ = ' stroke-dasharray="%s"' % dash if dash else ""
            cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3"%s/>'
                            % (lx, ly + k * 22, lx + 26, ly + k * 22, col, d_))
            cv.text_px(lx + 34, ly + k * 22, lab, 12.5, col, anchor="start", weight="700")
            k += 1
    return cv, SX, SY


# ══════ fig-2：σ、u、σ' 沿深度分布（解題圖解）══════
# ── 由 SM-2009-3 §4 Step 1–3 解得（γw = 9.81；砂層總水頭 = 地表上 1.0 m 均一）──
GW = 9.81
G_CL, G_SA = 18.89, 20.67          # §4 Step 1（取兩位）
S_A = G_CL * H_CL; S_B = S_A + G_SA * H_AB; S_C = S_B + G_SA * H_BC     # 56.67、98.01、139.35
uS = lambda z: GW * (z + H_PZ)      # 砂層：h = +1.0 m 均一
uH = lambda z: GW * z               # 靜水壓（對照）

def fig_profile():
    sig = [(0, 0), (Z_A, S_A), (Z_B, S_B), (Z_C, S_C)]
    u = [(0, 0), (Z_A, uS(Z_A)), (Z_B, uS(Z_B)), (Z_C, uS(Z_C))]
    uh = [(0, 0), (Z_C, uH(Z_C))]
    se = [(0, 0), (Z_A, S_A - uS(Z_A)), (Z_B, S_B - uS(Z_B)), (Z_C, S_C - uS(Z_C))]
    curves = [(sig, C["member"], 2.6, None, "總應力 σ"), (uh, C["deform"], 1.8, "6 4", "u 若誤用靜水壓"),
              (u, C["deform"], 2.8, None, "孔隙水壓 u（受壓水層）"), (se, C["bmd"], 3.0, None, "有效應力 σ'")]
    labels = []
    for z, s, lab in ((Z_A, S_A, "A"), (Z_B, S_B, "B"), (Z_C, S_C, "C")):
        labels += [(z, s, "σ = %.2f" % s, C["member"], "start", -14),
                   (z, uS(z), "u = %.2f" % uS(z), C["deform"], "start", 16 if z < Z_C else -16),
                   (z, s - uS(z), "σ' = %.2f" % (s - uS(z)), C["bmd"], "end", -14)]
    layers = [(0, Z_A, "rgba(63,74,90,0.08)", "飽和黏土（向上滲流）"), (Z_A, Z_C, "rgba(180,83,9,0.10)", "飽和砂（h = +1.0 m）")]
    cv, SX, SY = depth_profile(900, 600, Z_C, 0, 160, [0, 40, 80, 120, 160], [0, Z_A, Z_B, Z_C],
                               layers, curves, labels, legend_xy=(690, 500))
    for z, lab in ((0, "地表"), (Z_A, "A"), (Z_B, "B"), (Z_C, "C")):
        cv.text_px(cv.X(0) - 34, cv.Y(SY(z)), lab, 13, C["text"], anchor="end", weight="700")
    return cv

compose([fig_profile()],
        title="圖 2　σ、u、σ' 沿深度：砂層內總水頭均一，孔隙水壓比靜水壓多 1.0γw",
        sub="砂層 u = γw(z + 1.0)；虛線為誤用靜水壓 u = γw z 的結果（每點少 9.81 kPa、σ' 多 9.81 kPa）",
        note="攔錯用：受壓水層的 u 由水壓計總水頭決定，不是由地下水位起算的靜水壓；黏土層內因此有向上滲流。",
        path=os.path.join(OUT, "SM-2009-3-fig-2-profile.svg"))
