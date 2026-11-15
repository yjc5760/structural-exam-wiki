# -*- coding: utf-8 -*-
"""SM-2020-1 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2020-1-problem.md §4 判讀清單（#2–#4、#8），不含任何解題結果。
fig-2-profile：解題圖解（2026-11-15 階段 E），σ、u、σ' 沿深度，數值取自解析 §4。
用法：python gen_SM-2020-1.py [輸出資料夾]（預設本題 figs/）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *                                      # Canvas, C, compose, fit, soil_fill, wt_symbol
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
H1, H2, H3 = 2.1, 0.9, 1.9     # #3 層厚
Z_B, Z_C = H1, H1 + H2         # #2 B 乾砂底、C 毛細區底＝地下水位（#4）
Z_D = Z_C + H3                 # #2、#8 D 黏土底＝岩盤頂
XL, XR = -3.0, 6.0

def wavy(cv, x, y0, y1, col):
    n = 40
    pts = [(x + 0.08 * math.sin(k / n * 6 * math.pi), y0 + (y1 - y0) * k / n) for k in range(n + 1)]
    cv.poly(pts[:-3], col, 1.6)
    cv.arrow(pts[-4], pts[-1], col, 1.6, 8)

def fig_problem():
    W, H = 900, 560
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (XL - 1.2, XR + 1.0), (-(Z_D + 0.7), 0.6), 30, 30, 20, 20))
    Y = lambda d: -d
    soil_fill(cv, XL, XR, Y(Z_B), Y(0), "rgba(180,83,9,0.10)")
    soil_fill(cv, XL, XR, Y(Z_C), Y(Z_B), "rgba(180,83,9,0.22)")
    soil_fill(cv, XL, XR, Y(Z_D), Y(Z_C), "rgba(63,74,90,0.22)")
    for d, w in ((0, 2.6), (Z_B, 1.6), (Z_C, 1.6), (Z_D, 2.6)):
        cv.line((XL, Y(d)), (XR, Y(d)), C["member"], w)
    for k in range(10):                                   # 岩盤剖線
        x = XL + 0.4 + k * 0.9
        cv.line((x, Y(Z_D)), (x - 0.25, Y(Z_D + 0.3)), C["member"], 1.3)
    for x in (-1.2, 0.6, 2.4):                            # 毛細上升（C → B）
        wavy(cv, x, Y(Z_C), Y(Z_B), C["deform"])
    wt_symbol(cv, 1.5, Y(Z_C) + 0.07 * 2.4, C["deform"], 0.07)
    cv.text((1.75, Y(Z_C) + 0.2), "G.W.T", 12.5, C["deform"], anchor="start", weight="700")
    for z, lab in ((0, "A"), (Z_B, "B"), (Z_C, "C"), (Z_D, "D")):
        cv.dot((0.0, Y(z)), 6, fill=C["text"])
        cv.text((0.3, Y(z) + 0.22), lab, 14.5, C["text"], anchor="start", weight="700")
    cv.text((3.3, Y(0) + 0.22), "G.L.", 12.5, C["muted"], anchor="start")
    cv.text((3.3, Y(1.0)), "乾砂  Gs = 2.65，e = 0.5", 12.5, C["text"], anchor="start")
    cv.text((3.3, Y(2.48)), "濕砂、毛細作用區", 12.5, C["text"], anchor="start")
    cv.text((3.3, Y(2.82)), "Gs = 2.65，e = 0.5，S = 50%", 12, C["text"], anchor="start")
    cv.text((3.3, Y(3.95)), "飽和黏土  Gs = 2.71，w = 42%", 12.5, C["text"], anchor="start")
    cv.text((1.0, Y(Z_D + 0.5)), "岩盤", 13, C["text"], weight="700")
    xd = XL - 0.3
    cv.dim((xd, Y(Z_B)), (xd, Y(0)), "H1 = 2.1 m", 0, C["dim"], 12, label_off=-40)
    cv.dim((xd, Y(Z_C)), (xd, Y(Z_B)), "H2 = 0.9 m", 0, C["dim"], 12, label_off=-40)
    cv.dim((xd, Y(Z_D)), (xd, Y(Z_C)), "H3 = 1.9 m", 0, C["dim"], 12, label_off=-40)
    return cv

compose([fig_problem()],
        title="SM-2020-1 題目附圖重繪",
        sub="依題目正本判讀清單；地下水位在 C，毛細上升到 B",
        note="攔錯用：地下水位在 C（毛細區底），B–C 間是負孔隙水壓區；濕砂用 S = 50% 的單位重，不是飽和單位重。",
        path=os.path.join(OUT, "SM-2020-1-fig-1-problem.svg"))

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
# ── 由 SM-2020-1 §4 Step 1–3 解得（γw = 9.81；毛細區 u = −Sγw h，題目正本 #1 定案）──
GW, S_CAP = 9.81, 0.50
from decimal import Decimal, ROUND_HALF_UP
r2 = lambda x: float(Decimal(repr(x)).quantize(Decimal("0.01"), ROUND_HALF_UP))   # 與 §4 相同：逐步取兩位
G_D = r2(2.65 / (1 + 0.5) * GW)                    # 17.33
G_M = r2((2.65 + S_CAP * 0.5) / (1 + 0.5) * GW)    # 18.97
E3 = 0.42 * 2.71
G_SAT = 17.65                                      # §4 取 17.65（精算 17.655，差異可忽略）
S_B = r2(G_D * H1); S_C = r2(S_B + r2(G_M * H2)); S_D = r2(S_C + r2(G_SAT * H3))   # 36.39、53.46、87.00
U_B = r2(-S_CAP * GW * H2)                          # −4.41（B 毛細區側）
U_D = r2(GW * H3)                                   # 18.64

def fig_profile():
    sig = [(0, 0), (Z_B, S_B), (Z_C, S_C), (Z_D, S_D)]
    u = [(0, 0), (Z_B, 0), (Z_B, U_B), (Z_C, 0), (Z_D, U_D)]
    se = [(0, 0), (Z_B, S_B), (Z_B, S_B - U_B), (Z_C, S_C), (Z_D, S_D - U_D)]
    curves = [(sig, C["member"], 2.6, None, "總應力 σ"), (u, C["deform"], 2.8, None, "孔隙水壓 u"),
              (se, C["bmd"], 3.0, None, "有效應力 σ'")]
    labels = [(Z_B, S_B, "σ = σ' = %.2f（乾砂側）" % S_B, C["member"], "end", -14),
              (Z_B, S_B - U_B, "σ' = %.2f（毛細側）" % (S_B - U_B), C["bmd"], "start", 14),
              (Z_B, U_B, "u = %.2f" % U_B, C["deform"], "end", 16),
              (Z_C, S_C, "σ = σ' = %.2f" % S_C, C["bmd"], "start", 0),
              (Z_D, S_D, "σ = %.2f" % S_D, C["member"], "start", -12),
              (Z_D, S_D - U_D, "σ' = %.2f" % (S_D - U_D), C["bmd"], "end", -16),
              (Z_D, U_D, "u = %.2f" % U_D, C["deform"], "start", 0)]
    layers = [(0, Z_B, "rgba(180,83,9,0.06)", "乾砂（u = 0）"), (Z_B, Z_C, "rgba(29,78,216,0.07)", "毛細區（u 為負）"),
              (Z_C, Z_D, "rgba(63,74,90,0.08)", "飽和黏土（靜水壓）")]
    cv, SX, SY = depth_profile(900, 600, Z_D, -10, 95, [-10, 0, 20, 40, 60, 80], [0, Z_B, Z_C, Z_D],
                               layers, curves, labels, legend_xy=(700, 520))
    for z, lab in ((0, "A"), (Z_B, "B"), (Z_C, "C"), (Z_D, "D")):
        cv.text_px(cv.X(0) - 34, cv.Y(SY(z)), lab, 13, C["text"], anchor="end", weight="700")
    return cv

compose([fig_profile()],
        title="圖 2　σ、u、σ' 沿深度：B 點（毛細區頂）孔隙水壓與有效應力不連續",
        sub="乾砂段 u = 0；B 點 u 由 0 跳到 −Sγw·h，B→C 線性回到 0，C 以下靜水壓（γw = 9.81，S = 50%）",
        note="攔錯用：u 不是從 A 線性降到 B（乾砂沒有水壓）；σ' 在 B 點向上跳一段後繼續增加，沒有局部峰值。",
        path=os.path.join(OUT, "SM-2020-1-fig-2-profile.svg"))
