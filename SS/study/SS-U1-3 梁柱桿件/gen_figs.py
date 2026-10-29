#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""梁柱桿件（Beam-Column）觀念講義 — SVG 向量圖解產生器

鐵則：圖上每個數字都由本檔頂端的常數與算式推出，不得憑印象填。
改一個輸入（Fy、I、Pu/Pe1…），圖形自動跟著變。

注意：compose() 的 title/sub/note 走 esc()，不做上下標解析，
      故一律寫成純文字（B1、Pe1、phi_c 之類），不可用 _{} 語法。
"""
import sys, os, math, glob
SD = glob.glob("/root/.claude/skills/synced/*/struct-diagram")[0]
sys.path.insert(0, os.path.join(SD, "scripts"))
from structdraw import (Canvas, C, compose, column_shape, beam_shape, member_shape)

OUT = "figs"
os.makedirs(OUT, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# 輸入常數（所有圖上的數字皆由此推算）
# ═══════════════════════════════════════════════════════════════
FY, ES, GS = 2.5, 2040.0, 790.0        # tf/cm2
PHIC, PHIB = 0.85, 0.90

# 示範斷面 A：H 400x200x8x13（LTB 用）
b_f, t_f, d_s, t_w = 20.0, 1.3, 40.0, 0.8
h_w  = d_s - 2*t_f
A_s  = 2*b_f*t_f + h_w*t_w
Ix_A = 2*(b_f*t_f**3/12 + b_f*t_f*((d_s-t_f)/2)**2) + t_w*h_w**3/12
Iy_A = 2*(t_f*b_f**3/12) + h_w*t_w**3/12
Sx_A = Ix_A/(d_s/2)
Zx_A = 2*(b_f*t_f)*((d_s-t_f)/2) + t_w*h_w**2/4
J_A  = (2*b_f*t_f**3 + h_w*t_w**3)/3
Cw_A = Iy_A*(d_s-t_f)**2/4
ry_A = math.sqrt(Iy_A/A_s)

FR = 0.7
MP = Zx_A*FY
MR = Sx_A*(FY-FR)
LP = 1.76*ry_A*math.sqrt(ES/FY)
X1 = (math.pi/Sx_A)*math.sqrt(ES*GS*J_A*A_s/2)
X2 = 4*(Cw_A/Iy_A)*(Sx_A/(GS*J_A))**2
FL = FY - FR
LR = (ry_A*X1/FL)*math.sqrt(1+math.sqrt(1+X2*FL**2))

def Mcr_elastic(Lb):                       # Cb = 1.0
    return (math.pi/Lb)*math.sqrt(ES*Iy_A*GS*J_A + (math.pi*ES/Lb)**2*Iy_A*Cw_A)

def Mn_ltb(Lb):
    if Lb <= LP: return MP
    if Lb <= LR: return MP - (MP-MR)*(Lb-LP)/(LR-LP)
    return min(Mcr_elastic(Lb), MP)

# 示範斷面 B：H 400x400x13x21（雙軸放大對比；規格表值）
IX_B, IY_B = 66600.0, 22400.0
RATIO_I = IY_B/IX_B
ALPHA_X = 0.25
ALPHA_Y = ALPHA_X/RATIO_I
B1X, B1Y = 1.0/(1-ALPHA_X), 1.0/(1-ALPHA_Y)

# 二階迴圈示範
ALPHA_LOOP = 0.40
B_LOOP = 1.0/(1-ALPHA_LOOP)

# 靠桿示範
P_FRAME_EA, N_FRAME, P_LEAN, PE2_EA = 100.0, 2, 150.0, 1200.0
SUM_PU_RIGHT = N_FRAME*P_FRAME_EA + P_LEAN
SUM_PU_WRONG = N_FRAME*P_FRAME_EA
SUM_PE2 = N_FRAME*PE2_EA
B2_RIGHT = 1.0/(1-SUM_PU_RIGHT/SUM_PE2)
B2_WRONG = 1.0/(1-SUM_PU_WRONG/SUM_PE2)

# 柱曲線
def lam_c(sl): return (sl/math.pi)*math.sqrt(FY/ES)
def fcr(sl):
    lc = lam_c(sl)
    return (0.658**(lc**2))*FY if lc <= 1.5 else (0.877/lc**2)*FY
SL_T = 1.5*math.pi*math.sqrt(ES/FY)

# P-M 互制包絡線
def pm_m(p): return (9.0/8.0)*(1-p) if p >= 0.2 else 1-p/2.0


# ═══════════════════════════════════════════════════════════════
# 版面工具
# ═══════════════════════════════════════════════════════════════
def pcv(w, h, xr, yr, pad):
    """等向縮放的示意圖畫布（結構圖用）。pad = (left, right, top, bottom)"""
    L, R, T, B = pad
    sx = min((w-L-R)/(xr[1]-xr[0]), (h-T-B)/(yr[1]-yr[0]))
    ox = L + (w-L-R-(xr[1]-xr[0])*sx)/2 - xr[0]*sx
    oy = B + (h-T-B-(yr[1]-yr[0])*sx)/2 - yr[0]*sx
    return Canvas(w, h, sx=sx, ox=ox, oy=oy)


def plotbox(w, h, xr, yr, box):
    """非等向的函數圖畫布：模型座標 = 像素（y 由底部起算），
    再用 fx/fy 把資料座標映射進 box=(x0,x1,y0,y1)（像素，y 由底部起算）。"""
    cv = Canvas(w, h, sx=1, ox=0, oy=0)
    x0, x1, y0, y1 = box
    fx = lambda v: x0 + (v-xr[0])/(xr[1]-xr[0])*(x1-x0)
    fy = lambda v: y0 + (v-yr[0])/(yr[1]-yr[0])*(y1-y0)
    return cv, fx, fy, (lambda a, b: (fx(a), fy(b)))


def axis_frame(cv, x0, x1, y0, y1, xlab, ylab):
    cv.arrow((x0, y0), (x1+18, y0), C["muted"], 1.8, 9)
    cv.arrow((x0, y0), (x0, y1+18), C["muted"], 1.8, 9)
    cv.math_px(x1+26, cv.h-y0+5, xlab, 14.5, C["muted"], "start")
    cv.math_px(x0, cv.h-y1-32, ylab, 14.5, C["muted"])


def pow_label(cv, cx, y, base, exp, tail, col, size=15.5):
    """畫「底數^(含上下標的指數)」——mtext 不支援巢狀上下標，故拆成三段自行排版。"""
    from structdraw import est_width
    es = size*0.72
    wb, we, wt = est_width(base, size), est_width(exp, es), est_width(tail, size)
    x = cx - (wb+we+wt)/2
    cv.math_px(x, y, base, size, col, "start")
    cv.math_px(x+wb+1, y-size*0.42, exp, es, col, "start")
    cv.math_px(x+wb+we+3, y, tail, size, col, "start")


PW, PH = 520, 600


# ═══════════════════════════════════════════════════════════════
# 圖 1　三種構材的本質差別
# ═══════════════════════════════════════════════════════════════
def fig1():
    W3, H3 = 347, 476
    XR, YR = (-0.62, 0.62), (0.0, 1.30)
    PAD = (48, 48, 92, 100)

    a = pcv(W3, H3, XR, YR, PAD)
    a.panel("純柱（壓力桿件）", "只有 P，沒有外加彎矩")
    a.fixed_support((0, 0), size=20)
    a.line((0, 0), (0, 1.0), C["member"], 8, cap="butt")
    a.arrow((0, 1.26), (0, 1.03), C["load"], 3.4, 11)
    a.math((0, 1.20), "P", 19, C["load"], "start", dx=12)
    a.math_px(a.X(0)+18, a.Y(0.55), "M = 0", 16, C["muted"])
    a.text_px(W3/2, H3-62, "桿身保持直線，內力不回饋", 13, C["muted"])
    a.text_px(W3/2, H3-38, "→ 只查挫屈強度", 13.5, C["compr"], weight="700")

    b = pcv(W3, H3, XR, YR, PAD)
    b.panel("純梁（彎矩桿件）", "只有 δ，沒有軸力")
    yb, half, dlt = 0.62, 0.44, 0.20
    b.udl((-half, yb), (half, yb), 0.13, n=8, color=C["load"], w=2.0)
    b.line((-half, yb), (half, yb), C["ghost"], 2.2, dash="5 5")
    b.poly(member_shape((-half, yb), (half, yb),
                        lambda xi: -dlt*(16.0/5.0)*(xi-2*xi**3+xi**4)), C["deform"], 6.5)
    b.pin_support((-half, yb), size=15)
    b.roller_support((half, yb), size=15)
    b.arrow((0, yb), (0, yb-dlt), C["accent"], 2.4, 9)
    b.math_px(b.X(0)+12, b.Y(yb-dlt/2), "δ", 19, C["accent"], "start", weight="700")
    b.math_px(b.X(-half)-6, b.Y(yb-0.30), "P = 0", 16, C["muted"], "end")
    b.text_px(W3/2, H3-62, "有變形，但沒有軸力可乘", 13, C["muted"])
    b.text_px(W3/2, H3-38, "→ 一階彎矩就是答案", 13.5, C["bmd"], weight="700")

    c = pcv(W3, H3, XR, YR, PAD)
    c.panel("梁柱（Beam-Column）", "P 與 δ 同時存在")
    D = 0.20
    c.fixed_support((0, 0), size=20)
    c.line((0, 0), (0, 1.0), C["ghost"], 3.0, dash="6 6", cap="butt")
    c.poly(column_shape((0, 0), 1.0, D, -1.5*D), C["deform"], 7.0)
    c.arrow((D, 1.26), (D, 1.03), C["load"], 3.4, 11)
    c.math((D, 1.20), "P", 19, C["load"], "start", dx=12)
    c.arrow((-0.44, 1.0), (D-0.05, 1.0), C["load"], 3.0, 10)
    c.math_px(c.X(-0.44)-6, c.Y(1.0)-16, "H", 17, C["load"], "end")
    c.double_arrow((0, 0.72), (D, 0.72), C["accent"], 2.2, 8)
    c.math_px(c.X(D/2), c.Y(0.72)-15, "δ", 18, C["accent"], weight="700")
    c.text_px(c.X(D)+14, c.Y(0.34), "額外彎矩", 13, C["accent"], "start", weight="700")
    c.math_px(c.X(D)+14, c.Y(0.34)+19, "ΔM = P · δ", 15.5, C["accent"], "start", weight="700")
    c.text_px(W3/2, H3-62, "彎矩→變形→更多彎矩（回饋）", 13, C["muted"])
    c.text_px(W3/2, H3-38, "→ 一階彎矩必須放大", 13.5, C["load"], weight="700")

    compose([a, b, c], title="全鋼結構唯一「內力會自己長大」的構材",
            sub="差別不在斷面，而在「有沒有 P 與 δ 同時出現」",
            note="純柱缺 δ、純梁缺 P，兩者的乘積都是零；只有梁柱的 P×δ 不為零，二階效應才存在。",
            path=f"{OUT}/bc-fig-1-three-members.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 2　放大係數怎麼來的
# ═══════════════════════════════════════════════════════════════
def fig2():
    a = Canvas(PW, PH, sx=1, ox=0, oy=0)
    a.panel("回饋迴圈的和 = 幾何級數", f"以 P/P_{{cr}} = {ALPHA_LOOP:.1f} 示範")
    x0, xlim = 138, PW-96
    lim = B_LOOP
    cum, rows = 0.0, []
    for k in range(5):
        cum += ALPHA_LOOP**k
        rows.append(cum)
    labs = ["一階彎矩", "＋第 1 圈", "＋第 2 圈", "＋第 3 圈", "＋第 4 圈"]
    syms = ["M_{nt}", "+Pδ_{1}", "+Pδ_{2}", "+Pδ_{3}", "+Pδ_{4}"]
    ytop, bh, gap, span = 142, 36, 22, (xlim-x0)
    a.parts.append(f'<line x1="{xlim:.1f}" y1="{ytop-22}" x2="{xlim:.1f}" '
                   f'y2="{ytop+5*(bh+gap)+4}" stroke="{C["accent"]}" stroke-width="2.2" '
                   f'stroke-dasharray="6 5"/>')
    for i, v in enumerate(rows):
        y = ytop + i*(bh+gap)
        w = span*v/lim
        a.rect_px(x0, y, w, bh, C["fill_m"], 6, C["bmd"], 1.5)
        a.text_px(x0-12, y+bh/2, labs[i], 13.5, C["text"], "end")
        a.math_px(x0+10, y+bh/2, syms[i], 14, C["bmd"], "start", weight="700")
        a.text_px(x0+w-8, y+bh/2, f"{v:.3f}", 13, C["bmd"], "end", weight="700")
    a.text_px(xlim, ytop-56, "收斂極限", 12.5, C["accent"], weight="700")
    a.math_px(xlim, ytop-36, f"{lim:.3f} M_{{nt}}", 14.5, C["accent"], weight="700")
    a.math_px(PW/2, PH-74, "1 + α + α^{2} + α^{3} + ⋯ = 1 / (1 − α)",
              16.5, C["text"], weight="700")
    a.text_px(PW/2, PH-46, "每一圈的增量都是前一圈的 α = P/P_{cr} 倍", 13, C["muted"])

    b, fx, fy, P = plotbox(PW, PH, (0, 1.06), (0, 6.4), (96, PW-104, 104, PH-136))
    b.panel("放大係數隨軸力比急遽發散")
    axis_frame(b, fx(0), fx(1.06), fy(0), fy(6.4), "P/P_{cr}", "B")
    pts, x = [], 0.0
    while x <= 0.858:
        pts.append(P(x, 1/(1-x))); x += 0.004
    b.poly(pts, C["load"], 3.6)
    b.line(P(1.0, 0), P(1.0, 6.4), C["muted"], 1.8, dash="6 5")
    b.text_px(fx(1.0), PH-fy(6.4)-6, "挫屈", 12.5, C["muted"])
    b.line(P(0, 1.0), P(1.06, 1.0), C["ghost"], 1.6, dash="4 4")
    b.math_px(fx(0)-8, PH-fy(1.0), "1.0", 13, C["muted"], "end")
    for xv in (0.2, 0.4, 0.6, 0.8):
        yv = 1/(1-xv)
        hot = abs(xv-ALPHA_LOOP) < 1e-9
        b.dot(P(xv, yv), 5.6, fill=C["accent"] if hot else "#FFFFFF", stroke=C["accent"], w=2.4)
        b.text_px(fx(xv)-11, PH-fy(yv)-6, f"{yv:.2f}", 13, C["accent"], "end", weight="700")
        b.math_px(fx(xv), PH-fy(0)+20, f"{xv:.1f}", 12.5, C["muted"])
    b.text_px(PW/2, PH-64, "軸力用到 80% 挫屈載重時", 13, C["muted"])
    b.text_px(PW/2, PH-42, "彎矩已被放大 5 倍", 13.5, C["load"], weight="700")

    compose([a, b], title="二階放大係數 1 / (1 − P/Pcr) 的來源",
            sub="它不是規範硬塞的修正值，而是一個收斂級數的和",
            note="這條曲線說明為什麼 B1、B2 恆 ≥ 1.0：α ≥ 0 時級數各項皆為正，放大只會往上、不會往下。",
            path=f"{OUT}/bc-fig-2-amplification.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 3　兩欄解題骨架
# ═══════════════════════════════════════════════════════════════
def fig3():
    W, H = 1200, 440
    cv = Canvas(W, H, sx=1, ox=0, oy=0)
    cv.rect_px(0, 0, W, H, "#FFFFFF", 0)

    def box(x, y, w, h, fill, stroke, cn, sym):
        cv.rect_px(x, y, w, h, fill, 10, stroke, 1.8)
        cv.text_px(x+w/2, y+h*0.33, cn, 15, C["text"], weight="700")
        cv.math_px(x+w/2, y+h*0.70, sym, 16, stroke, weight="700")

    def vdown(x, y0, y1, col):
        cv.parts.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1-9}" stroke="{col}" stroke-width="2.4"/>')
        cv.parts.append(f'<polygon points="{x},{y1} {x-5.2},{y1-10} {x+5.2},{y1-10}" fill="{col}"/>')

    BW, BH = 430, 72
    LX, RX = 56, W-56-BW
    ys = [64, 176, 288]
    L = [("一階分析內力（未放大）", "M_{nt} , M_{lt} , P_{u}"),
         ("二階放大係數", "B_{1}  (P-δ)   ‧   B_{2}  (P-Δ)"),
         ("設計需求內力", "M_{u} = B_{1}M_{nt} + B_{2}M_{lt}")]
    R = [("軸壓強度（U1-1 複用）", "φ_{c}P_{n}   ←  KL/r"),
         ("彎曲強度（U1-2 複用）", "φ_{b}M_{nx} , φ_{b}M_{ny}"),
         ("強度側完成（不教新觀念）", "φ_{c}P_{n} , φ_{b}M_{n}")]
    for i in range(3):
        box(LX, ys[i], BW, BH, C["fill_t"], C["load"], L[i][0], L[i][1])
        box(RX, ys[i], BW, BH, C["fill_c"], C["compr"], R[i][0], R[i][1])
        if i < 2:
            vdown(LX+BW/2, ys[i]+BH, ys[i+1], C["load"])
            vdown(RX+BW/2, ys[i]+BH, ys[i+1], C["compr"])
    cv.text_px(LX+BW/2, 38, "左腿　需求側", 17, C["load"], weight="700")
    cv.text_px(RX+BW/2, 38, "右腿　強度側", 17, C["compr"], weight="700")

    CX, CY, CW_, CH_ = W/2-250, 376, 500, 56
    cv.rect_px(CX, CY, CW_, CH_, C["fill_m"], 12, C["bmd"], 2.2)
    cv.text_px(W/2, CY+20, "兩腿會合：P-M 互制方程式", 15.5, C["text"], weight="700")
    cv.text_px(W/2, CY+40, "總利用率 ≤ 1.0　（H1-1a / H1-1b 擇一）", 14.5, C["bmd"], weight="700")
    for sx_, col in ((LX+BW/2, C["load"]), (RX+BW/2, C["compr"])):
        ex = CX+40 if sx_ < W/2 else CX+CW_-40
        cv.parts.append(f'<line x1="{sx_}" y1="{ys[2]+BH}" x2="{ex}" y2="{CY-10}" '
                        f'stroke="{col}" stroke-width="2.4"/>')
        cv.parts.append(f'<polygon points="{ex},{CY} {ex-(6 if sx_<W/2 else -6)},{CY-11} '
                        f'{ex+(9 if sx_<W/2 else -9)},{CY-7}" fill="{col}"/>')

    compose([cv], title="進考場第一個動作：紙上先畫出左右兩欄",
            sub="需求側與強度側各自獨立算完，最後只在 P-M 互制式會合",
            note="兩欄法的價值在於「不會漏」：左欄漏了 B2 或右欄漏了弱軸上限，在會合前就會看出缺格。",
            path=f"{OUT}/bc-fig-3-two-legs.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 4　B1：構件自彎 P-δ（K = 1.0）
# ═══════════════════════════════════════════════════════════════
def fig4():
    PAD = (56, 56, 96, 104)
    a = pcv(PW, PH, (-0.55, 0.55), (-0.22, 1.24), PAD)
    a.panel("P-δ：桿件相對「自己的弦線」鼓出", "兩端不平移，中央撓出 δ")
    dlt = 0.155
    a.line((0, 0), (0, 1.0), C["ghost"], 2.6, dash="6 6", cap="butt")
    a.poly(member_shape((0, 0), (0, 1.0), lambda xi: dlt*math.sin(math.pi*xi)), C["deform"], 7.0)
    a.arrow((0, 1.22), (0, 1.03), C["load"], 3.4, 11)
    a.math((0, 1.18), "P_{u}", 18, C["load"], "start", dx=12)
    a.arrow((0, -0.20), (0, -0.01), C["load"], 3.4, 11)
    a.math((0, -0.16), "P_{u}", 18, C["load"], "start", dx=12)
    a.double_arrow((0, 0.5), (-dlt, 0.5), C["accent"], 2.2, 8)
    a.math_px(a.X(-dlt/2), a.Y(0.5)-16, "δ", 18, C["accent"], weight="700")
    a.dot((0, 1.0), 5.4, fill="#FFFFFF", stroke=C["member"], w=2.4)
    a.dot((0, 0), 5.4, fill="#FFFFFF", stroke=C["member"], w=2.4)
    a.text_px(a.X(0)+14, a.Y(0.84), "弦線（兩端連線）", 12.5, C["muted"], "start")
    a.text_px(PW/2, PH-62, "端點無相對側移，弦線仍為鉛直", 13, C["muted"])
    a.math_px(PW/2, PH-36, "B_{1} = C_{m} / (1 − P_{u}/P_{e1}) ≥ 1.0", 16, C["load"], weight="700")

    b = pcv(PW, PH, (-0.22, 1.24), (-0.18, 1.26), PAD)
    b.panel("有斜撐構架 → K 取非側移模式", "實務取 K = 1.0")
    b.line((0, 0), (0, 1.0), C["member"], 6.5, cap="butt")
    b.line((1.0, 0), (1.0, 1.0), C["member"], 6.5, cap="butt")
    b.line((0, 1.0), (1.0, 1.0), C["member"], 6.5, cap="butt")
    b.line((0, 0), (1.0, 1.0), C["compr"], 4.2, dash="10 6")
    b.pin_support((0, 0), size=16)
    b.pin_support((1.0, 0), size=16)
    b.arrow((0.5, 1.24), (0.5, 1.04), C["load"], 3.2, 10)
    b.math((0.5, 1.20), "P_{u}", 17, C["load"], "start", dx=11)
    b.text_px(b.X(0.32), b.Y(0.80), "斜撐吸收側力", 13, C["compr"], weight="700")
    b.math_px(b.X(0.32), b.Y(0.80)+20, "Δ ≈ 0", 15.5, C["compr"], weight="700")
    b.text_px(PW/2, PH-62, "沒有側移就沒有 P-Δ，故 M_{lt} = 0", 13, C["muted"])
    b.text_px(PW/2, PH-36, "整題只需要算 B_{1}", 15, C["bmd"], weight="700")

    compose([a, b], title="左腿第一段：B1 管的是「構件自己彎出來的」二階效應",
            sub="它跟整層有沒有側移無關，所以有效長度一律用非側移模式",
            note="最常見的錯誤是把對位圖查到的側移 K（K > 1.0）拿去算 Pe1——"
                 "Pe1 一律用 K = 1.0，側移 K 只屬於 B2 的 Pe2。",
            path=f"{OUT}/bc-fig-4-b1-member.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 5　Cm：單曲率 vs 雙曲率
# ═══════════════════════════════════════════════════════════════
def _cm_panel(title, sub, ratio, amp, shape_fn, mfun, tone):
    cv = pcv(PW, PH, (-0.72, 1.10), (-0.06, 1.18), (40, 40, 96, 116))
    cv.panel(title, sub)
    cm = 0.6 - 0.4*ratio
    cv.line((0, 0), (0, 1.0), C["ghost"], 2.4, dash="6 6", cap="butt")
    cv.poly(member_shape((0, 0), (0, 1.0), lambda xi: amp*shape_fn(xi)), C["deform"], 6.6)
    cv.arrow((0, 1.18), (0, 1.02), C["load"], 3.2, 10)
    cv.math((0, 1.14), "P_{u}", 17, C["load"], "start", dx=11)
    base, n = 0.60, 60
    pts = [(base + mfun(i/n)*0.30, i/n) for i in range(n+1)]
    cv.line((base, 0), (base, 1.0), C["muted"], 1.8)
    cv.polygon([(base, 0)] + pts + [(base, 1.0)], C["fill_m"], C["bmd"], 2.2)
    cv.math_px(cv.X(base+mfun(1.0)*0.30), cv.Y(1.0)-18, "M_{2}", 15, C["bmd"], "middle", weight="700")
    cv.math_px(cv.X(base+mfun(0.0)*0.30), cv.Y(0)+20, "M_{1}", 15, C["bmd"], "middle", weight="700")
    cv.text_px(cv.X(base)+6, cv.Y(0.52), "彎矩圖", 12, C["muted"], "start")
    cv.math_px(PW/2, PH-70, f"M_{{1}}/M_{{2}} = {ratio:+.0f}", 16, C["text"], weight="700")
    cv.math_px(PW/2, PH-44, f"C_{{m}} = 0.6 − 0.4({ratio:+.0f}) = {cm:.1f}", 17, tone, weight="700")
    return cv, cm


def fig5():
    a, cm_a = _cm_panel("單曲率（C 型）", "變形往同一側累積 → 取負", -1, 0.175,
                        lambda xi: math.sin(math.pi*xi), lambda xi: 1.0, C["load"])
    a.text_px(a.X(-0.68), a.Y(0.66), "最大 δ 與", 12.5, C["load"], "start", weight="700")
    a.text_px(a.X(-0.68), a.Y(0.66)+18, "最大 M 同位置", 12.5, C["load"], "start", weight="700")
    a.text_px(a.X(-0.68), a.Y(0.66)+40, "→ 不折減", 12.5, C["muted"], "start")

    b, cm_b = _cm_panel("雙曲率（S 型）", "上下變形互相抵消 → 取正", +1, 0.135,
                        lambda xi: math.sin(2*math.pi*xi), lambda xi: 1.0-2*xi, C["bmd"])
    b.text_px(b.X(-0.68), b.Y(0.66), "彎矩最大處", 12.5, C["bmd"], "start", weight="700")
    b.text_px(b.X(-0.68), b.Y(0.66)+18, "δ ≈ 0，不同步", 12.5, C["bmd"], "start", weight="700")
    b.text_px(b.X(-0.68), b.Y(0.66)+40, "→ 大幅折減", 12.5, C["muted"], "start")

    compose([a, b], title="Cm 在問的其實是：最大彎矩與最大變形同不同步",
            sub=f"同一支桿、同一個 Pu，Cm 差 {cm_a/cm_b:.0f} 倍",
            note=f"單曲率 Cm = {cm_a:.1f}（最危險，不折減）；雙曲率 Cm = {cm_b:.1f}"
                 "（彎矩大的地方變形小，可大幅折減）。符號代錯，B1 就直接差好幾倍。",
            path=f"{OUT}/bc-fig-5-cm-curvature.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 6　B2：整層 P-Δ 與靠桿
# ═══════════════════════════════════════════════════════════════
def fig6():
    a = pcv(PW, PH, (-0.20, 2.34), (-0.10, 1.30), (52, 52, 96, 112))
    a.panel("靠桿不抗側，但它的重量仍要人扛", "鉸接重力柱（leaning column）")
    D, xl = 0.17, 2.0
    th = -1.05*D
    for x in (0.0, 1.0):
        a.line((x, 0), (x, 1.0), C["ghost"], 2.2, dash="6 6", cap="butt")
        a.poly(column_shape((x, 0), 1.0, D, th), C["deform"], 6.4)
        a.fixed_support((x, 0), size=18)
    a.line((0, 1.0), (1.0, 1.0), C["ghost"], 2.2, dash="6 6", cap="butt")
    a.poly(beam_shape((D, 1.0), 1.0, th, th), C["deform"], 6.4)
    a.line((xl, 0), (xl, 1.0), C["ghost"], 2.2, dash="6 6", cap="butt")
    a.line((xl+D, 0.03), (xl+D, 0.97), C["member2"], 5.6, cap="butt")
    a.line((D+1.0, 1.0), (xl+D, 0.98), C["member2"], 4.0, cap="butt")
    a.dot((xl+D, 0.97), 6.0, fill="#FFFFFF", stroke=C["member2"], w=2.4)
    a.dot((xl+D, 0.03), 6.0, fill="#FFFFFF", stroke=C["member2"], w=2.4)
    a.pin_support((xl, 0), size=14, color=C["member2"])
    for x, p, col in ((0.0, P_FRAME_EA, C["load"]), (1.0, P_FRAME_EA, C["load"]),
                      (xl, P_LEAN, C["accent"])):
        a.arrow((x+D, 1.28), (x+D, 1.06), col, 3.0, 9.5)
        a.math_px(a.X(x+D), a.Y(1.28)-14, f"{p:.0f}", 13.5, col, weight="700")
    a.double_arrow((0, 1.14), (D, 1.14), C["accent"], 2.0, 8)
    a.math_px(a.X(D/2), a.Y(1.14)-14, "Δ", 16, C["accent"], weight="700")
    a.text_px(a.X(0.5), a.Y(0.42), "抗側系統", 13, C["deform"], weight="700")
    a.text_px(a.X(xl+D), a.Y(0.42), "靠桿", 13, C["accent"], weight="700")
    a.text_px(a.X(xl+D), a.Y(0.42)+18, "兩端鉸接", 12, C["muted"])
    a.text_px(PW/2, PH-64, "靠桿自己站不住，靠樓版拉著抗側柱才不倒", 13, C["muted"])
    a.text_px(PW/2, PH-40, "所以它的 P 進分子，它的勁度不進分母", 13.5, C["accent"], weight="700")

    b = Canvas(PW, PH, sx=1, ox=0, oy=0)
    b.panel("分子分母各自算什麼", "數字取自左圖（單位 tf）")
    rows = [("∑P_{u}（分子）", "全樓層所有柱：抗側柱 ＋ 靠桿",
             f"{N_FRAME}×{P_FRAME_EA:.0f} + {P_LEAN:.0f} = {SUM_PU_RIGHT:.0f}", C["load"]),
            ("∑P_{e2}（分母）", "只有抗側系統提供勁度",
             f"{N_FRAME}×{PE2_EA:.0f} = {SUM_PE2:.0f}", C["compr"])]
    y = 100
    for sym, cn, val, col in rows:
        b.rect_px(44, y, PW-88, 76, C["panel"], 9, col, 1.6)
        b.math_px(62, y+24, sym, 15.5, col, "start", weight="700")
        b.text_px(62, y+48, cn, 12.5, C["muted"], "start")
        b.text_px(PW-62, y+36, val, 15, C["text"], "end", weight="700")
        y += 94
    b.text_px(PW/2, y+10, "把靠桿算進分子 vs 忘了算", 13.5, C["text"], weight="700")
    bx0, bwmax = 132, PW-132-128
    for i, (lab, v, col) in enumerate([("正確", B2_RIGHT, C["bmd"]), ("漏算靠桿", B2_WRONG, C["load"])]):
        yy = y+34+i*50
        w = bwmax*(v-1.0)/(B2_RIGHT-1.0)
        b.rect_px(bx0, yy, max(w, 4), 32, C["fill_m"] if i == 0 else C["fill_t"], 6, col, 1.5)
        b.text_px(bx0-12, yy+16, lab, 13, C["text"], "end")
        b.math_px(bx0+max(w, 4)+10, yy+16, f"B_{{2}} = {v:.3f}", 14.5, col, "start", weight="700")
    b.text_px(PW/2, PH-38,
              f"漏算靠桿，彎矩低估 {100*(B2_RIGHT-B2_WRONG)/B2_RIGHT:.1f}%（偏不安全）",
              13.5, C["load"], weight="700")

    compose([a, b], title="左腿第二段：B2 的 Σ 指的是「整個樓層」",
            sub="B2 = 1 / (1 − ΣPu / ΣPe2) ≥ 1.0",
            note="B1 的 Pu、Pe1 是「這一支桿」的；B2 的 ΣPu、ΣPe2 是「這一層樓」的。"
                 "層與桿混用是本單元最大宗的失分點。",
            path=f"{OUT}/bc-fig-6-b2-story-leaning.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 7　柱強度曲線
# ═══════════════════════════════════════════════════════════════
def fig7():
    W, H = 1040, 600
    cv, fx, fy, P = plotbox(W, H, (0, 205), (0, 1.06), (112, 712, 110, 470))
    cv.panel(None)
    cv.polygon([P(0, 0), P(SL_T, 0), P(SL_T, 1.06), P(0, 1.06)], C["fill_c"], "none")
    cv.polygon([P(SL_T, 0), P(205, 0), P(205, 1.06), P(SL_T, 1.06)], C["fill_m"], "none")
    axis_frame(cv, fx(0), fx(205), fy(0), fy(1.06), "KL/r", "φ_{c}F_{cr}/F_{y}")
    cv.poly([P(s, PHIC*fcr(s)/FY) for s in [1+i*2 for i in range(102)]], C["compr"], 4.2)
    cv.line(P(SL_T, 0), P(SL_T, 1.06), C["accent"], 2.2, dash="7 5")
    cv.math_px(fx(SL_T), H-fy(1.06)-30, "λ_{c} = 1.5", 15.5, C["accent"], weight="700")
    cv.math_px(fx(SL_T), H-fy(1.06)-10, f"KL/r = {SL_T:.0f}", 13.5, C["accent"], weight="700")
    cv.text_px(fx(SL_T/2), H-fy(0.86), "非彈性挫屈（含殘留應力）", 14.5, C["compr"], weight="700")
    pow_label(cv, fx(SL_T/2), H-fy(0.86)+24, "F_{cr} = 0.658", "λ_c^{2}", " F_{y}", C["compr"])
    cv.text_px(fx((SL_T+205)/2), H-fy(0.86), "彈性挫屈（Euler）", 14.5, C["bmd"], weight="700")
    cv.math_px(fx((SL_T+205)/2), H-fy(0.86)+24, "F_{cr} = (0.877/λ_c^{2}) F_{y}", 15.5, C["bmd"])
    for s, lab, col, side in ((62, "KL/r_{x}", C["muted"], -1), (116, "KL/r_{y}", C["load"], 1)):
        yv = PHIC*fcr(s)/FY
        cv.line(P(s, 0), P(s, yv), col, 1.6, dash="4 4")
        cv.dot(P(s, yv), 6.0, fill="#FFFFFF", stroke=col, w=2.6)
        cv.math_px(fx(s)+side*14, H-fy(yv)+(20 if side < 0 else -12), f"{yv:.3f}", 13.5, col,
                   "start" if side > 0 else "end", weight="700")
        cv.math_px(fx(s), H-fy(0)+38, lab, 14, col, weight="700")
    cv.text_px(fx(116)+16, H-fy(0.16), "細長比大者控制 \u2192 弱軸", 13.5, C["load"], "start", weight="700")
    for tick in (50, 100, 150, 200):
        cv.line(P(tick, 0), P(tick, -0.018), C["muted"], 1.4)
        cv.math_px(fx(tick), H-fy(0)+18, str(tick), 12.5, C["muted"])
    for tick in (0.2, 0.4, 0.6, 0.8, 1.0):
        cv.line(P(0, tick), P(-3.4, tick), C["muted"], 1.4)
        cv.math_px(fx(0)-12, H-fy(tick), f"{tick:.1f}", 12.5, C["muted"], "end")
    cv.legend(W-262, 156, [(C["compr"], "φ_{c}P_{n} = φ_{c}F_{cr}A_{g}"),
                           (C["accent"], "λ_{c} = 1.5 分界"),
                           (C["load"], "本例控制軸")], size=13, gap=28)
    cv.math_px(W-170, 258, "φ_{c} = 0.85", 15, C["text"], weight="700")
    cv.text_px(W-170, 292, "強弱軸各算一次 KL/r，", 12.5, C["muted"])
    cv.text_px(W-170, 312, "只有較大者代入曲線。", 12.5, C["muted"])
    cv.text_px(W-170, 344, "另一軸的 I 不會浪費：", 12.5, C["muted"])
    cv.text_px(W-170, 364, "它回頭決定 B1 的 Pe1。", 12.5, C["accent"], weight="700")

    compose([cv], title="右腿（一）：軸壓強度 φcPn 完全複用壓桿單元",
            sub="梁柱題不教新的柱公式，只是換一個地方用",
            note="兩軸細長比要分開算，但只有「較大者」控制 φcPn；"
                 "另一軸的 KL/r 在這裡用不到（但它的 I 會回頭決定 B1 的 Pe1）。",
            path=f"{OUT}/bc-fig-7-column-curve.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 8　LTB 三區段
# ═══════════════════════════════════════════════════════════════
def fig8():
    W, H = 1040, 600
    LBMAX, ymax = 11.0, MP/100*1.12
    cv, fx, fy, P = plotbox(W, H, (0, LBMAX*1.04), (0, ymax), (120, 712, 112, 470))
    cv.panel(None)
    for x0, x1, col in ((0, LP/100, C["fill_c"]), (LP/100, LR/100, C["fill_m"]),
                        (LR/100, LBMAX*1.04, C["fill_s"])):
        cv.polygon([P(x0, 0), P(x1, 0), P(x1, ymax), P(x0, ymax)], col, "none")
    axis_frame(cv, fx(0), fx(LBMAX*1.04), fy(0), fy(ymax), "L_{b}  (m)", "M_{n}  (tf-m)")
    cv.poly([P(Lb/100, Mn_ltb(Lb)/100) for Lb in [2+i*4 for i in range(int(LBMAX*100/4))]],
            C["bmd"], 4.2)
    for xv, lab, val in ((LP/100, "L_{p}", f"{LP/100:.2f} m"), (LR/100, "L_{r}", f"{LR/100:.2f} m")):
        cv.line(P(xv, 0), P(xv, ymax), C["accent"], 2.0, dash="7 5")
        cv.math_px(fx(xv), H-fy(0)+20, lab, 15.5, C["accent"], weight="700")
        cv.math_px(fx(xv), H-fy(0)+40, val, 12.5, C["accent"])
    for yv, lab in ((MP/100, "M_{p}"), (MR/100, "M_{r}")):
        cv.line(P(0, yv), P(LBMAX*1.04, yv), C["ghost"], 1.6, dash="4 4")
        cv.math_px(fx(0)-12, H-fy(yv), lab, 15, C["muted"], "end", weight="700")
        cv.math_px(fx(0)-12, H-fy(yv)+18, f"{yv:.1f}", 12, C["muted"], "end")
    labs = [(LP/200, "塑性", "M_{n} = M_{p}", C["compr"], True),
            ((LP+LR)/200, "非彈性 LTB", "直線內插", C["bmd"], False),
            ((LR/100+LBMAX)/2, "彈性 LTB", "M_{n} = M_{cr}", C["sfd"], True)]
    for xv, cn, sym, col, is_math in labs:
        cv.text_px(fx(xv), H-fy(ymax*0.22), cn, 14.5, col, weight="700")
        if is_math:
            cv.math_px(fx(xv), H-fy(ymax*0.22)+24, sym, 14.5, col)
        else:
            cv.text_px(fx(xv), H-fy(ymax*0.22)+24, sym, 13.5, col)
    cv.legend(W-262, 152, [(C["bmd"], "φ_{b}M_{nx}　(φ_{b} = 0.90)")], size=13)
    cv.text_px(W-170, 206, "弱軸沒有 LTB", 14.5, C["load"], weight="700")
    cv.text_px(W-170, 234, "弱軸不會側傾，", 12.5, C["muted"])
    cv.text_px(W-170, 254, "改由形狀因數上限控制：", 12.5, C["muted"])
    cv.math_px(W-170, 284, "M_{ny} ≤ 1.5F_{y}S_{y}", 15, C["load"], weight="700")
    cv.text_px(W-170, 316, "題目同時給 Z_{y} 與 S_{y}，", 12.5, C["muted"])
    cv.text_px(W-170, 336, "就是在提示你要檢查。", 12.5, C["accent"], weight="700")
    cv.text_px(W/2, H-40, f"示範斷面 H {d_s*10:.0f}×{b_f*10:.0f}×{t_w*10:.0f}"
                          f"×{t_f*10:.0f}　F_{{y}} = {FY:.1f} tf/cm²", 12.5, C["muted"])

    compose([cv], title="右腿（二）：強軸彎曲強度的三個區段",
            sub="Lb 落在哪一段，決定 Mn 用哪一條式子",
            note=f"本例 Lp = {LP/100:.2f} m、Lr = {LR/100:.2f} m 皆由斷面性質算出，不是背來的；"
                 "考試時題目多半直接給 Lp、Lr，你只要會判區段。",
            path=f"{OUT}/bc-fig-8-ltb-zones.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 9　P-M 互制包絡線
# ═══════════════════════════════════════════════════════════════
def fig9():
    W, H = 1040, 600
    cv, fx, fy, P = plotbox(W, H, (0, 1.22), (0, 1.12), (140, 700, 112, 468))
    cv.panel(None)
    n = 100
    env = [(pm_m(i/n), i/n) for i in range(n+1)]
    cv.polygon([P(0, 0)] + [P(m, p) for m, p in env] + [P(0, 1.0)], C["fill_m"], C["bmd"], 3.4)
    axis_frame(cv, fx(0), fx(1.22), fy(0), fy(1.12), "M_{u}/φ_{b}M_{n}", "P_{u}/φ_{c}P_{n}")
    cv.line(P(0, 0.2), P(1.22, 0.2), C["accent"], 2.2, dash="7 5")
    cv.math_px(fx(1.22), H-fy(0.2)-12, "P_{u}/φ_{c}P_{n} = 0.2", 14, C["accent"], "end", weight="700")
    cv.dot(P(pm_m(0.2), 0.2), 6.4, fill=C["accent"], stroke="#FFFFFF", w=2.4)
    cv.math_px(fx(pm_m(0.2))+16, H-fy(0.2)+34, f"({pm_m(0.2):.2f}, 0.20)", 13.5, C["accent"], "start", weight="700")
    cv.text_px(fx(0.30), H-fy(0.60), "軸力主控", 16, C["compr"], weight="700")
    cv.math_px(fx(0.30), H-fy(0.60)-24, "H1-1a", 14.5, C["compr"], weight="700")
    cv.text_px(fx(0.30), H-fy(0.60)+22, "彎矩項係數 8/9", 13, C["muted"])
    cv.text_px(fx(0.42), H-fy(0.10), "彎矩主控　H1-1b（軸力項係數 1/2）", 14, C["bmd"], weight="700")
    cv.dot(P(0, 1.0), 6.0, fill="#FFFFFF", stroke=C["compr"], w=2.6)
    cv.text_px(fx(0)+14, H-fy(1.0)-14, "純軸壓", 13, C["compr"], "start", weight="700")
    cv.dot(P(1.0, 0), 6.0, fill="#FFFFFF", stroke=C["bmd"], w=2.6)
    cv.text_px(fx(1.0)+22, H-fy(0)-16, "純彎矩", 13, C["bmd"], "start", weight="700")
    pex, pey = 0.60, 0.45
    util = pey + (8.0/9.0)*pex
    cv.dot(P(pex, pey), 7.0, fill=C["load"], stroke="#FFFFFF", w=2.4)
    cv.text_px(fx(pex)-16, H-fy(pey)+4, "設計點", 13.5, C["load"], "end", weight="700")
    cv.math_px(fx(pex)-16, H-fy(pey)+26, f"0.45 + (8/9)(0.60) = {util:.2f}", 13, C["load"], "end")
    for t in (0.2, 0.4, 0.6, 0.8, 1.0):
        cv.line(P(t, 0), P(t, -0.018), C["muted"], 1.4)
        cv.math_px(fx(t), H-fy(0)+18, f"{t:.1f}", 12.5, C["muted"])
        cv.line(P(0, t), P(-0.020, t), C["muted"], 1.4)
        cv.math_px(fx(0)-12, H-fy(t), f"{t:.1f}", 12.5, C["muted"], "end")
    cv.text_px(W-176, 150, "包絡線內 = 安全", 14.5, C["bmd"], weight="700")
    cv.text_px(W-176, 180, "兩式在 0.2 處相接，", 12.5, C["muted"])
    cv.text_px(W-176, 200, "數值連續（皆為 0.90），", 12.5, C["muted"])
    cv.text_px(W-176, 220, "不是兩條獨立檢核。", 12.5, C["muted"])
    cv.text_px(W-176, 258, "利用率正常落在", 12.5, C["muted"])
    cv.text_px(W-176, 278, "0.8 ~ 1.0；", 12.5, C["muted"])
    cv.text_px(W-176, 298, "算出 0.2 或 3.0，", 12.5, C["muted"])
    cv.text_px(W-176, 318, "幾乎都是單位或", 12.5, C["muted"])
    cv.text_px(W-176, 338, "放大係數錯。", 12.5, C["accent"], weight="700")

    compose([cv], title="兩腿會合：P-M 互制式在量「斷面能力被吃掉幾成」",
            sub="不是兩個獨立檢核，而是一條共用的包絡線",
            note="先算 Pu/φcPn 判斷落在哪一區，再選 H1-1a 或 H1-1b——選錯式子，彎矩項的權重會差 1.8 倍。",
            path=f"{OUT}/bc-fig-9-pm-interaction.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 10　雙軸彎矩：弱軸放大遠大於強軸
# ═══════════════════════════════════════════════════════════════
def fig10():
    a = pcv(PW, PH, (-1.20, 1.20), (-1.10, 1.10), (60, 60, 104, 132))
    a.panel("同一支柱，兩軸的 P_{e1} 差很多",
            f"H 400×400×13×21　I_{{y}}/I_{{x}} = {RATIO_I:.3f}")
    bw, hh, tf2, tw2 = 0.92, 0.92, 0.14, 0.10
    a.polygon([(-bw/2, hh/2-tf2), (-bw/2, hh/2), (bw/2, hh/2), (bw/2, hh/2-tf2),
               (tw2/2, hh/2-tf2), (tw2/2, -hh/2+tf2), (bw/2, -hh/2+tf2), (bw/2, -hh/2),
               (-bw/2, -hh/2), (-bw/2, -hh/2+tf2), (-tw2/2, -hh/2+tf2),
               (-tw2/2, hh/2-tf2)], C["fill_c"], C["member"], 2.0)
    a.line((-bw/2-0.20, 0), (bw/2+0.20, 0), C["compr"], 2.0, dash="9 5")
    a.line((0, -hh/2-0.16), (0, hh/2+0.16), C["load"], 2.0, dash="9 5")
    a.math_px(a.X(bw/2+0.20)+10, a.Y(0), "x", 16, C["compr"], "start", weight="700")
    a.math_px(a.X(0)+12, a.Y(hh/2+0.16)-10, "y", 16, C["load"], "start", weight="700")
    a.math_px(a.X(-bw/2)-20, a.Y(0.26), f"I_{{x}} = {IX_B:,.0f}", 14.5, C["compr"], "end", weight="700")
    a.math_px(a.X(-bw/2)-20, a.Y(0.26)+18, "cm^{4}", 12, C["muted"], "end")
    a.math_px(a.X(bw/2)+20, a.Y(-0.26), f"I_{{y}} = {IY_B:,.0f}", 14.5, C["load"], "start", weight="700")
    a.math_px(a.X(bw/2)+20, a.Y(-0.26)+18, "cm^{4}", 12, C["muted"], "start")
    a.math_px(PW/2, PH-88, "P_{e1} = π^{2}EI / (KL)^{2}  ∝  I", 16.5, C["text"], weight="700")
    a.text_px(PW/2, PH-58, "自我檢查：兩軸 P_{e1} 的比值", 13, C["muted"])
    a.text_px(PW/2, PH-36, "必須剛好等於 I_{y}/I_{x}", 14, C["accent"], weight="700")

    b = Canvas(PW, PH, sx=1, ox=0, oy=0)
    b.panel("放大倍率的差距被 1/(1−α) 再拉開",
            f"以 P_{{u}}/P_{{e1x}} = {ALPHA_X:.2f}、C_{{m}} = 1.0 示範")
    x0, wmax, y = 150, PW-150-128, 118
    for lab, al, bv, col in (("強軸 x", ALPHA_X, B1X, C["compr"]),
                             ("弱軸 y", ALPHA_Y, B1Y, C["load"])):
        b.text_px(x0-14, y+18, lab, 14, C["text"], "end", weight="700")
        b.rect_px(x0, y, wmax, 36, C["panel"], 7, C["border"], 1.2)
        b.rect_px(x0, y, wmax*al, 36, C["fill_c"] if col == C["compr"] else C["fill_t"], 7, col, 1.6)
        b.math_px(x0+8, y+18, f"P_{{u}}/P_{{e1}} = {al:.3f}", 13.5, col, "start", weight="700")
        b.math_px(x0+wmax+10, y+18, f"→ B_{{1}} = {bv:.2f}", 14, col, "start", weight="700")
        y += 62
    b.text_px(PW/2, y+8, "軸力比差 3.0 倍，放大倍率差距更大", 13, C["muted"])
    ybase, bh_max = 452, 132
    for lab, bv, col in (("B_{1x}", B1X, C["compr"]), ("B_{1y}", B1Y, C["load"])):
        h = bh_max*(bv/B1Y)
        xx = PW/2 - 116 + (0 if col == C["compr"] else 148)
        b.rect_px(xx, ybase-h, 84, h, C["fill_c"] if col == C["compr"] else C["fill_t"], 7, col, 1.8)
        b.math_px(xx+42, ybase-h-14, f"{bv:.2f}", 17, col, weight="700")
        b.math_px(xx+42, ybase+18, lab, 14.5, C["text"], weight="700")
    b.text_px(PW/2, PH-38, f"弱軸的放大程度是強軸的 {B1Y/B1X:.1f} 倍 → 必須分開算",
              13.5, C["load"], weight="700")

    compose([a, b], title="雙軸彎矩題：B1x 與 B1y 絕對不能共用",
            sub="弱軸的 Pe1 小，同樣的 Pu 吃掉的比例大得多",
            note=f"本例 B1y / B1x = {B1Y/B1X:.2f}。若貪快用強軸的 B1 去放大弱軸彎矩，Muy 會嚴重低估。",
            path=f"{OUT}/bc-fig-10-weak-vs-strong.svg")


if __name__ == "__main__":
    print(f"Ix_A={Ix_A:.0f} Iy_A={Iy_A:.0f} Sx={Sx_A:.0f} Zx={Zx_A:.0f} ry={ry_A:.2f}")
    print(f"Mp={MP/100:.1f} tf-m  Mr={MR/100:.1f}  Lp={LP/100:.2f} m  Lr={LR/100:.2f} m")
    print(f"SL_T={SL_T:.1f}  B1x={B1X:.3f} B1y={B1Y:.3f}  B2={B2_RIGHT:.3f}/{B2_WRONG:.3f}")
    for f in (fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10):
        f()
    print("figs:", len(glob.glob(f"{OUT}/*.svg")))
