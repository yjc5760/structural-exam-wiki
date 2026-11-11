# -*- coding: utf-8 -*-
"""SM-2022-1 圖解。數值取自 SM-2022-1.md §4(二) 計算表格。"""
import sys, math, os
sys.path.insert(0, "/tmp/sd")
from geo import *
from geo import tag_px

OUT = "/tmp/sd/out/SM-2022-1"
os.makedirs(OUT, exist_ok=True)

# ── 由 SM-2022-1 §4(二) 計算表格 ────────────────────────
V = 1000.0                                             # cm³
W_ = [5.3, 7.8, 9.7, 12.9, 13.8, 17.0]                 # 含水量 %
MT = [1669, 1891, 2013, 2046, 2021, 1977]              # 溼土質量 g
RT = [m / V for m in MT]
RD = [rt / (1 + w / 100) for rt, w in zip(RT, W_)]
GD = [rd * 9.81 for rd in RD]                          # kN/m³
assert abs(GD[2] - 18.00) < 0.01 and abs(GD[0] - 15.55) < 0.01


def parab(idx):
    """三點二次內插的頂點（Lagrange 解析解）。"""
    (x1, y1), (x2, y2), (x3, y3) = [(W_[i], GD[i]) for i in idx]
    d12 = (y2 - y1) / (x2 - x1)
    d23 = (y3 - y2) / (x3 - x2)
    a = (d23 - d12) / (x3 - x1)
    b = d12 - a * (x1 + x2)
    c = y1 - a * x1 * x1 - b * x1
    xv = -b / (2 * a)
    return xv, a * xv * xv + b * xv + c, (a, b, c)

XV1, YV1, CO1 = parab([1, 2, 3])          # 7.8 / 9.7 / 12.9
XV2, YV2, CO2 = parab([2, 3, 4])          # 9.7 / 12.9 / 13.8
OMC, GDMAX = 10.9, 18.1                   # §4(二) 採用之推估值

# ══════ fig-2：夯實曲線與峰值內插 ══════
W, H = 900, 620
ML, MR, MT_, MB = 172, 150, 88, 182
XL, XR, YL, YH = 3.0, 19.0, 15.0, 18.6
cv = Canvas(W, H, bg="#FFFFFF")
PX = lambda x: ML + (x - XL) / (XR - XL) * (W - ML - MR)
PY = lambda y: H - MB - (y - YL) / (YH - YL) * (H - MT_ - MB)
def seg(p0, p1, col, w, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    cv.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%s" '
                    'stroke-linecap="round"%s/>' % (p0[0], p0[1], p1[0], p1[1], col, w, d))
def curve(pts, col, w, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    cv.parts.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" '
                    'stroke-linecap="round" stroke-linejoin="round"%s/>'
                    % (" ".join("%.2f,%.2f" % p for p in pts), col, w, d))

for x in range(4, 19, 2):
    seg((PX(x), PY(YL)), (PX(x), PY(YH)), C["border"], 1.1)
    cv.text_px(PX(x), PY(YL) + 19, str(x), 12.5, C["muted"])
for y in [15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5]:
    seg((PX(XL), PY(y)), (PX(XR), PY(y)), C["border"], 1.1)
    cv.text_px(PX(XL) - 12, PY(y), "%.1f" % y, 12.5, C["muted"], anchor="end")
seg((PX(XL), PY(YL)), (PX(XR), PY(YL)), C["muted"], 1.9)
seg((PX(XL), PY(YL)), (PX(XL), PY(YH)), C["muted"], 1.9)
cv.text_px((PX(XL) + PX(XR)) / 2, PY(YL) + 46, "含水量 ω（%）", 13.5, C["text"])
cv.text_px(PX(XL) - 96, (PY(YL) + PY(YH)) / 2, "乾單位重 γ_d（kN/m³）", 13.5, C["text"])

# 平滑夯實曲線：峰值段用最小二乘拋物線（過 7.8/9.7/12.9/13.8 四點），
# 兩端以 Hermite 平滑接回實測端點（5.3 與 17.0）
def ls_parab(idx):
    """對 idx 這幾點做二次最小二乘（正規方程，不依賴 numpy）。"""
    n = len(idx)
    Sx = [sum(W_[i] ** k for i in idx) for k in range(5)]
    Sy = [sum(GD[i] * W_[i] ** k for i in idx) for k in range(3)]
    A = [[Sx[4], Sx[3], Sx[2]], [Sx[3], Sx[2], Sx[1]], [Sx[2], Sx[1], Sx[0]]]
    B = [Sy[2], Sy[1], Sy[0]]
    for i in range(3):                       # 高斯消去
        piv = A[i][i]
        for j in range(i + 1, 3):
            f = A[j][i] / piv
            for k in range(3):
                A[j][k] -= f * A[i][k]
            B[j] -= f * B[i]
    x = [0.0] * 3
    for i in (2, 1, 0):
        x[i] = (B[i] - sum(A[i][k] * x[k] for k in range(i + 1, 3))) / A[i][i]
    return x

A2, B2, C2 = ls_parab([1, 2, 3, 4])
Pf = lambda x: A2 * x * x + B2 * x + C2
dP = lambda x: 2 * A2 * x + B2
XVL, YVL = -B2 / (2 * A2), Pf(-B2 / (2 * A2))
CUT_L, CUT_R = 7.0, 14.0

def herm(x0, y0, m0, x1, y1, m1, n=60):
    out = []
    for i in range(n + 1):
        t = i / n
        h00 = 2*t**3 - 3*t**2 + 1; h10 = t**3 - 2*t**2 + t
        h01 = -2*t**3 + 3*t**2;    h11 = t**3 - t**2
        dx = x1 - x0
        out.append((x0 + dx*t, h00*y0 + h10*dx*m0 + h01*y1 + h11*dx*m1))
    return out

mid = [(x, Pf(x)) for x in [CUT_L + i*(CUT_R-CUT_L)/240 for i in range(241)]]
left = herm(W_[0], GD[0], (Pf(CUT_L)-GD[0])/(CUT_L-W_[0]), CUT_L, Pf(CUT_L), dP(CUT_L))
right = herm(CUT_R, Pf(CUT_R), dP(CUT_R), W_[5], GD[5], (GD[5]-Pf(CUT_R))/(W_[5]-CUT_R))
curve([(PX(x), PY(y)) for x, y in left + mid + right], C["bmd"], 3.4)

for w_, g in zip(W_, GD):
    cv.parts.append('<circle cx="%.2f" cy="%.2f" r="6.0" fill="#FFFFFF" stroke="%s" '
                    'stroke-width="2.8"/>' % (PX(w_), PY(g), C["member"]))
    cv.text_px(PX(w_), PY(g) + 22, "%.2f" % g, 11.5, C["muted"])

# 峰值
seg((PX(OMC), PY(YL)), (PX(OMC), PY(GDMAX)), C["load"], 2.0, "6 5")
seg((PX(XL), PY(GDMAX)), (PX(OMC), PY(GDMAX)), C["load"], 2.0, "6 5")
cv.parts.append('<circle cx="%.2f" cy="%.2f" r="7.4" fill="%s" stroke="#FFFFFF" '
                'stroke-width="2.4"/>' % (PX(OMC), PY(GDMAX), C["load"]))
tag_px(cv, PX(OMC) + 16, PY(GDMAX) - 26,
       "峰值　OMC = 10.9%，γ_{d,max} = 18.1", 13.5, C["load"], anchor="start")
# 錯誤取法：直接取實測最大點
cv.parts.append('<circle cx="%.2f" cy="%.2f" r="10.5" fill="none" stroke="%s" '
                'stroke-width="2.2" stroke-dasharray="4 4"/>' % (PX(9.7), PY(18.00), C["accent"]))
seg((PX(7.9), PY(17.78)), (PX(9.35), PY(18.0)), C["accent"], 1.2, "3 3")
tag_px(cv, PX(6.9), PY(17.78), "× 直接取實測最大點", 12.5, C["accent"],
       anchor="middle", weight="400")

cv.text_px(W / 2, 32, "圖 2　夯實曲線：峰值不在任何一個實驗點上", 17.5, C["text"], weight="700")
cv.text_px(W / 2, 58, "六點由 ρ_t = M_t/1000、ρ_d = ρ_t/(1+ω)、γ_d = 9.81ρ_d 逐點算出", 12.5, C["muted"])
cv.text_px(W / 2, H - 100,
           "三點二次內插：(7.8, 9.7, 12.9) → ({:.2f}%, {:.2f})　；"
           "(9.7, 12.9, 13.8) → ({:.2f}%, {:.2f})　；"
           "四點最小二乘 → ({:.2f}%, {:.2f})".format(XV1, YV1, XV2, YV2, XVL, YVL),
           13, C["text"])
cv.text_px(W / 2, H - 74,
           "三種取法一致收斂 ⇒ 取 OMC ≈ 10.9%、γ_{d,max} ≈ 18.1 kN/m³", 13.5, C["bmd"], weight="700")
cv.text_px(W / 2, H - 42,
           "攔錯用：左半支斜率 +0.42 /% 遠陡於右半支 −0.07 /%，峰值必偏左且高於實測最大值 18.00。",
           13, C["accent"], weight="700")
cv.text_px(W / 2, H - 18,
           "若直接把 (9.7%, 18.00) 當答案，OMC 低估 1.2 個百分點、γ_{d,max} 低估 0.1 kN/m³。",
           12.5, C["muted"])
cv.save(OUT + "/SM-2022-1-fig-2-compaction-curve.svg")

# ══════ fig-3：夯實能量增加的影響（趨勢示意，不含數值）══════
W, H = 900, 580
ML, MR, MT_, MB = 120, 140, 92, 150
cv = Canvas(W, H, bg="#FFFFFF")
PXn = lambda t: ML + t * (W - ML - MR)          # t ∈ [0,1] 為無因次含水量
PYn = lambda t: H - MB - t * (H - MT_ - MB)     # t ∈ [0,1] 為無因次乾單位重
seg((PXn(0), PYn(0)), (PXn(1), PYn(0)), C["muted"], 1.9)
seg((PXn(0), PYn(0)), (PXn(0), PYn(1)), C["muted"], 1.9)
cv.text_px((PXn(0) + PXn(1)) / 2, PYn(0) + 34, "含水量 ω  →", 13.5, C["text"])
cv.text_px(PXn(0) - 56, (PYn(0) + PYn(1)) / 2, "γ_d  ↑", 13.5, C["text"])

def bell(x0, y0, amp, wid):
    return [(PXn(x), PYn(y0 + amp * math.exp(-((x - x0) / wid) ** 2)))
            for x in [i / 300 for i in range(301)]]

STD = (0.60, 0.10, 0.46, 0.22)      # 標準夯實（示意）
MOD = (0.42, 0.10, 0.68, 0.20)      # 改良夯實（示意）：左移＋上移
curve(bell(*STD), C["bmd"], 3.6)
curve(bell(*MOD), C["load"], 3.6, "10 6")
for (x0, y0, amp, wid), col, lab, ax, dxp in [
        (STD, C["bmd"], "標準夯實（能量小）", "start", 20),
        (MOD, C["load"], "改良夯實（能量大）", "end", -20)]:
    px, py = PXn(x0), PYn(y0 + amp)
    cv.parts.append('<circle cx="%.2f" cy="%.2f" r="7.0" fill="%s" stroke="#FFFFFF" '
                    'stroke-width="2.4"/>' % (px, py, col))
    seg((px, py), (px, PYn(0)), col, 1.4, "3 4")
    seg((PXn(0), py), (px, py), col, 1.4, "3 4")
    tag_px(cv, px + dxp, py - (46 if col == C["load"] else 24), lab, 13, col, anchor=ax)
# 移動方向箭頭
cv.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="3.2" '
                'stroke-linecap="round"/>' % (PXn(STD[0]) - 8, PYn(STD[1] + STD[2]) - 8,
                                              PXn(MOD[0]) + 14, PYn(MOD[1] + MOD[2]) + 12, C["accent"]))
cv.parts.append('<polygon points="%s" fill="%s"/>' % (
    "%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
        PXn(MOD[0]) + 6, PYn(MOD[1] + MOD[2]) + 4,
        PXn(MOD[0]) + 26, PYn(MOD[1] + MOD[2]) + 10,
        PXn(MOD[0]) + 18, PYn(MOD[1] + MOD[2]) + 26), C["accent"]))
tag_px(cv, (PXn(STD[0]) + PXn(MOD[0])) / 2 - 30,
       (PYn(STD[1] + STD[2]) + PYn(MOD[1] + MOD[2])) / 2 - 34,
       "能量↑ ⇒ 曲線往「左上」移", 13.5, C["accent"])
# OMC / γdmax 的位移方向
cv.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="2.4"/>'
                % (PXn(STD[0]), PYn(0) - 14, PXn(MOD[0]) + 10, PYn(0) - 14, C["muted"]))
cv.text_px((PXn(STD[0]) + PXn(MOD[0])) / 2, PYn(0) - 30, "OMC 減少", 12.5, C["muted"])
cv.parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="2.4"/>'
                % (PXn(0) + 14, PYn(STD[1] + STD[2]), PXn(0) + 14,
                   PYn(MOD[1] + MOD[2]) + 10, C["muted"]))
cv.text_px(PXn(0) + 66, (PYn(STD[1] + STD[2]) + PYn(MOD[1] + MOD[2])) / 2,
           "γ_{d,max} 增加", 12.5, C["muted"])

cv.text_px(W / 2, 32, "圖 3　夯實能量增加，曲線往左上移", 17.5, C["text"], weight="700")
cv.text_px(W / 2, 58, "本圖為趨勢示意，兩軸皆無因次、不含數值——考題只問方向", 12.5, C["muted"])
cv.text_px(W / 2, H - 96, "E = W · h · N · L / V", 15.5, C["text"], weight="700")
cv.text_px(W / 2, H - 72,
           "W 夯錘重　h 落距　N 每層夯擊數　L 層數　V 模具體積", 13, C["muted"])
cv.text_px(W / 2, H - 44,
           "攔錯用：方向只有一種——OMC 往左（減少）、γ_{d,max} 往上（增加）。", 13,
           C["accent"], weight="700")
cv.text_px(W / 2, H - 20,
           "物理原因：能量大時，較低含水量即可克服土粒間摩擦而重排；記成「右下移」是最常見的失分。",
           12.5, C["muted"])
cv.save(OUT + "/SM-2022-1-fig-3-energy-shift.svg")

print("gd =", ["%.2f" % g for g in GD])
print("三點內插 (7.8,9.7,12.9) -> (%.3f, %.3f)" % (XV1, YV1))
print("三點內插 (9.7,12.9,13.8) -> (%.3f, %.3f)" % (XV2, YV2))
print("LS 拋物線頂點 (%.3f, %.3f)" % (XVL, YVL))
print("左半支斜率 %.3f ; 右半支斜率 %.3f"
      % ((GD[2]-GD[1])/(W_[2]-W_[1]), (GD[3]-GD[2])/(W_[3]-W_[2])))
