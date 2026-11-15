# -*- coding: utf-8 -*-
"""SM-2021-1 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2021-1-problem.md §4 判讀清單（#1–#8），不含任何解題結果。
fig-2-profile：解題圖解（2026-11-15 階段 E），σ、u、σ' 沿深度，數值取自解析 §4。
用法：python gen_SM-2021-1.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *                                      # Canvas, C, compose, fit, soil_fill, wt_symbol, hatch_band
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
WT   = 1.0     # #1 地下水位
Z_A  = 3.0     # #2、#3 上層砂底＝黏土頂
Z_B  = Z_A + 3.0   # #5
Z_C  = Z_A + 6.0   # #4、#6 黏土底
Z_R  = Z_C + 2.0   # #7 下層砂底＝岩盤（不透水）
H_SP = 1.0     # #8 豎管水位高出地表
XL, XR = -4.0, 7.0
XP = 2.2       # 豎管位置（示意）

def fig_problem():
    W, H = 900, 640
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (XL - 1.0, XR + 0.2), (-(Z_R + 0.8), H_SP + 1.2), 30, 30, 20, 20))
    Y = lambda d: -d
    soil_fill(cv, XL, XR, Y(WT), Y(0), "rgba(180,83,9,0.10)")
    soil_fill(cv, XL, XR, Y(Z_A), Y(WT), "rgba(180,83,9,0.22)")
    soil_fill(cv, XL, XR, Y(Z_C), Y(Z_A), "rgba(63,74,90,0.22)")
    soil_fill(cv, XL, XR, Y(Z_R), Y(Z_C), "rgba(180,83,9,0.22)")
    for d, w in ((0, 2.6), (Z_A, 1.6), (Z_C, 1.6), (Z_R, 2.6)):
        cv.line((XL, Y(d)), (XR, Y(d)), C["member"], w)
    for k in range(12):
        x = XL + 0.4 + k * 0.9
        cv.line((x, Y(Z_R)), (x - 0.25, Y(Z_R + 0.3)), C["member"], 1.3)
    cv.line((XL, Y(WT)), (XR, Y(WT)), C["deform"], 1.8, dash="8 5")
    wt_symbol(cv, -3.0, Y(WT) + 0.09 * 2.4, C["deform"], 0.09)
    # 開口豎管：由地表上方插到 C 高程
    for dx in (-0.12, 0.12):
        cv.line((XP + dx, Y(-H_SP - 0.6)), (XP + dx, Y(Z_C)), C["member"], 1.8)
    cv.polygon([(XP - 0.12, Y(-H_SP)), (XP + 0.12, Y(-H_SP)), (XP + 0.12, Y(Z_C)), (XP - 0.12, Y(Z_C))],
               "rgba(29,78,216,0.25)")
    cv.line((XP - 0.4, Y(-H_SP)), (XP + 0.4, Y(-H_SP)), C["deform"], 1.8)
    cv.text((XP, Y(-H_SP - 0.95)), "開口豎管", 12.5, C["text"], weight="700")
    cv.dim((XP + 0.6, Y(0)), (XP + 0.6, Y(-H_SP)), "1 m", 0, C["dim"], 12, label_off=22)
    # 點位
    for z, lab in ((Z_A, "A"), (Z_B, "B"), (Z_C, "C")):
        cv.dot((0.6, Y(z)), 6, fill=C["text"])
        cv.text((0.95, Y(z) + 0.3), lab, 14.5, C["text"], anchor="start", weight="700")
    # 層名與參數
    cv.text((3.2, Y(0.5)), "乾砂 γ_{d} = 18 kN/m^{3}", 12.5, C["text"], anchor="start")
    cv.text((3.2, Y(2.0)), "飽和砂 γ_{sat} = 20 kN/m^{3}", 12.5, C["text"], anchor="start")
    cv.text((3.2, Y(5.6)), "飽和黏土 γ_{sat} = 19 kN/m^{3}", 12.5, C["text"], anchor="start")
    cv.text((3.2, Y(6.4)), "k = 5×10^{-7} cm/sec", 12.5, C["text"], anchor="start")
    cv.text((3.2, Y(10.0)), "飽和砂 γ_{sat} = 20 kN/m^{3}", 12.5, C["text"], anchor="start")
    cv.text((3.2, Y(Z_R + 0.5)), "岩盤（不透水）", 12.5, C["text"], anchor="start", weight="700")
    # 尺寸線（左側，端點對齊判讀清單）
    xd = XL - 0.3
    for d0, d1, lab in ((0, WT, "1 m"), (WT, Z_A, "2 m"), (Z_A, Z_C, "6 m"), (Z_C, Z_R, "2 m")):
        cv.dim((xd, Y(d1)), (xd, Y(d0)), lab, 0, C["dim"], 12, label_off=-24)
    cv.dim((-0.4, Y(Z_B)), (-0.4, Y(Z_A)), "3 m", 0, C["dim"], 12, label_off=-22)
    return cv

compose([fig_problem()],
        title="SM-2021-1 題目附圖重繪",
        sub="依題目正本判讀清單；豎管下端在 C（黏土底），管內水位高出地表 1 m",
        note="攔錯用：地下水位在地表下 1 m，豎管水頭屬於黏土下方的砂層；黏土上下兩面水頭不同，層內有穩態滲流。",
        path=os.path.join(OUT, "SM-2021-1-fig-1-problem.svg"))

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
# ── 由 SM-2021-1 §4（一）解得（γw = 9.81；黏土內總水頭線性，C 點豎管 +1 m）──
GW = 9.81
G_D, G_SS, G_CL = 18.0, 20.0, 19.0          # 題給
sv = lambda z: (G_D * z if z <= WT else G_D * WT + G_SS * (z - WT) if z <= Z_A
                else G_D * WT + G_SS * (Z_A - WT) + G_CL * (z - Z_A))
U_A = GW * (Z_A - WT)                       # 19.62
U_C = GW * (Z_C + H_SP)                     # 98.1
uu = lambda z: 0.0 if z <= WT else (GW * (z - WT) if z <= Z_A else U_A + (U_C - U_A) * (z - Z_A) / (Z_C - Z_A))

def fig_profile():
    zs = [0, WT, Z_A, Z_B, Z_C]
    sig = [(z, sv(z)) for z in zs]
    u = [(z, uu(z)) for z in zs]
    uh = [(WT, 0), (Z_C, GW * (Z_C - WT))]
    se = [(z, sv(z) - uu(z)) for z in zs]
    curves = [(sig, C["member"], 2.6, None, "總應力 σ"), (uh, C["deform"], 1.8, "6 4", "u 若全為靜水壓"),
              (u, C["deform"], 2.8, None, "孔隙水壓 u（向上滲流）"), (se, C["bmd"], 3.0, None, "有效應力 σ'")]
    labels = []
    for z in (Z_A, Z_B, Z_C):
        labels += [(z, sv(z), "σ = %g" % sv(z), C["member"], "start", -14),
                   (z, uu(z), "u = %.2f" % uu(z), C["deform"], "start", 16 if z < Z_C else -16),
                   (z, sv(z) - uu(z), "σ' = %.2f" % (sv(z) - uu(z)), C["bmd"], "end", -14)]
    layers = [(0, WT, "rgba(180,83,9,0.05)", "乾砂"), (WT, Z_A, "rgba(180,83,9,0.12)", "飽和砂（靜水壓）"),
              (Z_A, Z_C, "rgba(63,74,90,0.08)", "飽和黏土（i = 1/3 向上）")]
    cv, SX, SY = depth_profile(900, 620, Z_C, 0, 180, [0, 40, 80, 120, 160], [0, WT, Z_A, Z_B, Z_C],
                               layers, curves, labels, legend_xy=(690, 520))
    for z, lab in ((0, "地表"), (Z_A, "A"), (Z_B, "B"), (Z_C, "C")):
        cv.text_px(cv.X(0) - 34, cv.Y(SY(z)), lab, 13, C["text"], anchor="end", weight="700")
    return cv

compose([fig_profile()],
        title="圖 2　σ、u、σ' 沿深度：黏土內向上穩態滲流，u 由 A 到 C 線性增加",
        sub="A 點總水頭 −1 m、C 點 +1 m（以地表為基準），黏土 6 m 內水頭線性；虛線為假設整層靜水壓的錯誤結果",
        note="攔錯用：C 點 u 由豎管決定（98.1 kPa），比靜水壓多 2γw；B 點取 A、C 線性內插，不是靜水壓。",
        path=os.path.join(OUT, "SM-2021-1-fig-2-profile.svg"))
