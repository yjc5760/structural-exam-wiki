#!/usr/bin/env python3
"""
SS-2010-3 四角鋼組合受壓柱 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2010-3.py [輸出目錄]

重繪依據：題目正本 SS-2010-3-problem.md §4 判讀清單（2026-11-02 已確認）與 §2 單角鋼性質。
組合斷面與單角鋼依比例；柱側視僅示意兩端鉸接。不含任何解題結果。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2010-3"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2010-3-problem.md §4，已確認）；單位 cm
# ══════════════════════════════════════════════════════════
LL, LS, T = 15.0, 10.0, 1.5   # §2 L 15 × 10 × 1.5；#3 長肢 15 垂直、短肢 10 水平
CX, CY = 5.0, 2.53            # #4 c_x 垂直（水平肢外緣至形心）；#5 c_y 水平（垂直肢背至形心）
IX, IY, A1 = 782, 276, 35.3   # §2 單角鋼 I_x、I_y、A（照錄）
OUT_W = 40.0                  # #6、#7 四角配置，外廓 40 × 40 量到角鋼外緣
KL = 25.0                     # #8 有效長度 25 m，兩端鉸接（題文）

PW, PH = 440, 500


def _angle(sx_, sy_):
    """角鋼外緣頂點（heel 在外廓角落），sx_、sy_ = ±1 決定所在象限"""
    h = OUT_W / 2
    pts = [(h, h), (h - LS, h), (h - LS, h - T), (h - T, h - T), (h - T, h - LL), (h, h - LL)]
    return [(sx_ * x, sy_ * y) for x, y in pts]


def side_panel():
    cv = Canvas(PW, PH, sx=1, ox=PW / 2, oy=0)
    cv.panel("柱", "兩端鉸接")
    top, bot = PH - 130, 110
    cv.line((0, bot), (0, top), C["member"], 3, cap="butt")
    cv.support((0, bot), "pin", 0, size=13)
    cv.support((0, top), "pin", 180, size=13)
    cv.arrow((0, top + 70), (0, top + 24), C["load"], 2.6, 10)
    cv.arrow((0, bot - 70), (0, bot - 24), C["load"], 2.6, 10)
    cv.math_px(cv.X(0) + 12, cv.Y((top + bot) / 2), f"KL = {KL:g} m", 13, C["text"], "start")
    return cv


def composite_panel():
    sx = 7.0
    cv = Canvas(PW, PH, sx=sx, ox=PW / 2 - 20, oy=PH / 2 - 10)
    cv.panel("組合斷面", "依比例；虛線為繫板／繫條")
    h = OUT_W / 2
    g = h + 1.2
    cv.poly([(-g, -g), (g, -g), (g, g), (-g, g), (-g, -g)], C["muted"], 1.3, dash="6 4")
    for a in (-1, 1):
        for b in (-1, 1):
            cv.polygon(_angle(a, b), C["fill_c"], C["member"], 1.8)
    cv.circle((0, 0), 0.9, stroke=C["text"], w=1.6)
    cv.line((-0.9, 0), (0.9, 0), C["text"], 1.4)
    cv.line((0, -0.9), (0, 0.9), C["text"], 1.4)
    cv.text((0, 0), "C.G.", 13, C["text"], dy=-18, weight="700")
    cv.dim((h, -h), (h, h), f"{OUT_W:g} cm", off=40, label_off=30)
    cv.dim((-h, -h), (h, -h), f"{OUT_W:g} cm", off=40, label_off=16)
    return cv


def single_panel():
    sx = 11.0
    cv = Canvas(PW, PH, sx=sx, ox=150, oy=PH - 320)
    cv.panel("單角鋼斷面尺寸及性質", "依比例；長肢垂直、短肢水平")
    pts = [(0, 0), (LS, 0), (LS, T), (T, T), (T, LL), (0, LL)]
    cv.polygon(pts, C["fill_c"], C["member"], 1.8)
    cv.line((-2.5, CX), (LS + 2.5, CX), C["muted"], 1.3, dash="8 3 2 3")
    cv.line((CY, -4.5), (CY, LL + 2.0), C["muted"], 1.3, dash="8 3 2 3")
    cv.math((-2.5, CX), "X", 15, C["text"], "end", dx=-4, weight="700")
    cv.math((LS + 2.5, CX), "X", 15, C["text"], "start", dx=4, weight="700")
    cv.math((CY, LL + 2.0), "Y", 15, C["text"], dy=-10, weight="700")
    cv.math((CY, -4.5), "Y", 15, C["text"], "start", dx=8, weight="700")
    cv.circle((CY, CX), 0.45, stroke=C["text"], w=1.5)
    cv.dim((0, 0), (0, CX), "c_{x}", off=-26, label_off=-18, color=C["accent"])
    cv.dim((0, 0), (CY, 0), "c_{y}", off=26, label_off=16, color=C["accent"])
    x0, y0 = 40, PH - 92
    lines = [f"L {LL:g} cm × {LS:g} cm × {T:g} cm",
             f"c_{{x}} = {CX:.1f} cm, c_{{y}} = {CY:.2f} cm",
             f"I_{{x}} = {IX} cm^{{4}}, I_{{y}} = {IY} cm^{{4}}",
             f"A = {A1:g} cm^{{2}}"]
    for k, t in enumerate(lines):
        cv.math_px(x0, y0 + 22 * k, t, 14, C["text"], "start")
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    panels = [side_panel(), composite_panel(), single_panel()]
    compose(panels, cols=3,
            title="SS-2010-3 題目附圖（重繪）",
            sub="依題目正本判讀清單 #3–#8；只畫考卷所給條件",
            note="cx 為垂直尺寸（對 X 軸）、cy 為水平尺寸（對 Y 軸）；外廓 40 cm 量到角鋼外緣",
            path=path)
    return path


# ── 解題圖解共用小工具（像素座標；y 由上往下）──
def _hl(cv, PH, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line((x0, PH - y0), (x1, PH - y1), color, w, dash=dash, cap="butt")


def rsum(terms, nd=3):
    """與解析相同的加法：各項先四捨五入到 nd 位再相加"""
    return round(sum(round(t, nd) for t in terms), nd)


def _stack_row(cv, x0, y, scale, terms, colors, name, total_color, h=34, fmt="{:.3f}"):
    """水平堆疊長條：互制比 1.0 對應 scale 像素"""
    cv.text_px(x0 - 14, y, name, 14, C["text"], "end", weight="700")
    xx = x0
    for t, col in zip(terms, colors):
        w = scale * t
        cv.rect_px(xx, y - h/2, w, h, col, 0)
        if w > 44:
            cv.text_px(xx + w/2, y, fmt.format(t), 12.5, "#FFFFFF", weight="700")
        xx += w
    tot = rsum(terms)
    cv.text_px(xx + 12, y, "= " + fmt.format(tot), 15, total_color, "start", weight="700")
    return tot


# ══════════════════════════════════════════════════════════════
# 柱強度曲線（ASD Fa 與 LRFD φcFcr，舊版 LRFD φc = 0.85）
# ══════════════════════════════════════════════════════════════
import math


def q_fa(klr, fy, e):
    cc = math.sqrt(2 * math.pi ** 2 * e / fy)
    if klr <= cc:
        r = klr / cc
        return (1 - r * r / 2) * fy / (5 / 3 + 3 * r / 8 - r ** 3 / 8)
    return 12 * math.pi ** 2 * e / (23 * klr ** 2)


def q_phifcr(klr, fy, e, phi=0.85):
    lam = klr / math.pi * math.sqrt(fy / e)
    f = math.exp(-0.419 * lam ** 2) * fy if lam <= 1.5 else 0.877 / lam ** 2 * fy
    return phi * f


def q_curve_panel(W1, H1, title, sub, fy, e, marks, kmax=200.0, fmax=None):
    """marks: [(klr, '標籤', 是否控制)]；縱軸應力 tf/cm²"""
    cv = Canvas(W1, H1, sx=1)
    cv.panel(title, sub)
    X0, X1, YB, YT = 90, W1 - 40, H1 - 110, 110
    fmax = fmax or fy
    PX = lambda k: X0 + (X1 - X0) * k / kmax
    PY = lambda f: YB - (YB - YT) * f / fmax
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT - 10, C["muted"], 1.5)
    for k in range(0, int(kmax) + 1, 50):
        cv.text_px(PX(k), YB + 18, f"{k}", 11.5, C["muted"])
    for f in [fmax * i / 4 for i in range(5)]:
        cv.text_px(X0 - 8, PY(f), f"{f:.2f}", 11, C["muted"], "end")
    cv.text_px((X0 + X1) / 2, YB + 42, "KL/r", 13, C["text"], weight="700")
    cv.text_px(X0 - 6, YT - 22, "tf/cm²", 12, C["text"], "start", weight="700")
    ks = [kmax * i / 300 for i in range(1, 301)]
    cv.poly([(PX(k), H1 - PY(min(q_phifcr(k, fy, e), fmax))) for k in ks], C["bmd"], 2.6)
    cv.poly([(PX(k), H1 - PY(min(q_fa(k, fy, e), fmax))) for k in ks], C["compr"], 2.6, dash="8 5")
    cc = math.sqrt(2 * math.pi ** 2 * e / fy)
    _hl(cv, H1, PX(cc), YB, PX(cc), YT, C["ghost"], 1.2, dash="3 4")
    cv.text_px(PX(cc) + 4, YT + 4, f"Cc = {cc:.1f}", 11.5, C["muted"], "start")
    for k, lab, ctrl in marks:
        col = C["load"] if ctrl else C["muted"]
        _hl(cv, H1, PX(k), YB, PX(k), PY(q_phifcr(k, fy, e)) - 4, col, 1.4 if ctrl else 1.0, dash="4 3")
        cv.dot((PX(k), H1 - PY(q_phifcr(k, fy, e))), 5.5 if ctrl else 4, fill=C["bmd"])
        cv.dot((PX(k), H1 - PY(q_fa(k, fy, e))), 5.5 if ctrl else 4, fill=C["compr"])
        cv.text_px(PX(k) + 4, YB - 10, lab, 11.5, col, "start", weight="700" if ctrl else "400")
    cv.legend(X1 - 200, YT + 10, [(C["bmd"], "LRFD φc·Fcr（φc = 0.85）"), (C["compr"], "ASD Fa")], size=12, gap=19)
    return cv


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2010-3.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
Q_FY, Q_E = 2.52, 2040.0                 # tf/cm²（§4 二）
Q_A = 4 * A1
Q_DX = OUT_W / 2 - CX                    # 15.0（垂直距離，對水平軸 X）
Q_DY = OUT_W / 2 - CY                    # 17.47（水平距離，對垂直軸 Y）
Q_IXG = 4 * (IX + A1 * Q_DX ** 2)        # 34,898（控制）
Q_IYG = 4 * (IY + A1 * Q_DY ** 2)        # 44,198
Q_IBAD = 4 * (IY + A1 * Q_DX ** 2)       # 平行軸配錯：276 配 15 cm → 32,874
Q_R = math.sqrt(min(Q_IXG, Q_IYG) / Q_A)
Q_KLR = round(KL * 100 / round(Q_R, 2), 1)          # 159.0（與解析相同取位）
Q_KLR_BAD = round(KL * 100 / round(math.sqrt(Q_IBAD / Q_A), 2), 1)   # 163.8
Q_FA = q_fa(Q_KLR, Q_FY, Q_E)
Q_PA = Q_FA * Q_A
Q_PHIFCR = q_phifcr(Q_KLR, Q_FY, Q_E)
Q_PU = 0.85 * round(Q_FCR := Q_PHIFCR / 0.85, 3) * Q_A
Q_PCR = math.pi ** 2 * Q_E * Q_IXG / (KL * 100) ** 2


def fig2_section():
    W1, H1 = 1000, 560
    sx = 9.0
    cv = Canvas(W1, H1, sx=sx, ox=260, oy=H1 / 2 - 20)
    cv.panel("組合斷面：各角鋼形心到 C.G. 的距離", "長肢垂直 ⇒ cx = 5.0 是垂直量、配單角鋼 Ix = 782")
    h = OUT_W / 2
    for a in (-1, 1):
        for b in (-1, 1):
            cv.polygon(_angle(a, b), C["fill_c"], C["member"], 1.6)
            cv.dot((a * Q_DY, b * Q_DX), 4.5, fill=C["accent"])
    cv.line((-h - 3, 0), (h + 3, 0), C["muted"], 1.2, dash="8 3 2 3")
    cv.line((0, -h - 3), (0, h + 3), C["muted"], 1.2, dash="8 3 2 3")
    cv.text((h + 3, 0), "X", 14, C["text"], "start", dx=6, weight="700")
    cv.text((0, h + 3), "Y", 14, C["text"], dy=-12, weight="700")
    cv.line((Q_DY, Q_DX), (Q_DY, 0), C["compr"], 2.2)
    cv.line((0, Q_DX), (Q_DY, Q_DX), C["sfd"], 2.2)
    cv.text((Q_DY, Q_DX / 2), f"dX = {Q_DX:.1f}", 13, C["compr"], "end", dx=-8, weight="700")
    cv.text((Q_DY / 2, Q_DX), f"dY = {Q_DY:.2f}", 13, C["sfd"], dy=-12, weight="700")
    cv.dim((h, -h), (h, h), f"{OUT_W:g} cm", off=30, label_off=34)
    xt = 540
    rows = [("繞水平軸 X（用垂直距離 dX）", C["compr"], "700"),
            (f"4 × ({IX} + {A1} × {Q_DX:.1f}²) = {Q_IXG:,.0f} cm⁴ ← 控制", C["text"], "400"),
            ("繞垂直軸 Y（用水平距離 dY）", C["sfd"], "700"),
            (f"4 × ({IY} + {A1} × {Q_DY:.2f}²) = {Q_IYG:,.0f} cm⁴", C["text"], "400"),
            ("", C["text"], "400"),
            (f"r = √({Q_IXG:,.0f} / {Q_A:.1f}) = {Q_R:.2f} cm", C["bmd"], "700"),
            (f"KL/r = 2500 / {Q_R:.2f} = {Q_KLR:.1f}", C["bmd"], "700"),
            ("", C["text"], "400"),
            (f"配錯：{IY} 配 {Q_DX:.1f} cm ⇒ {Q_IBAD:,.0f}、KL/r {Q_KLR_BAD:.1f}", C["load"], "700")]
    for i, (s, col, wt) in enumerate(rows):
        if s:
            cv.text_px(xt, 140 + i * 34, s, 13, col, "start", weight=wt)
    path = os.path.join(OUT, f"{TAG}-fig-1-section.svg")
    compose([cv], cols=1,
            title=f"圖 1　平行軸定理：I_X = {Q_IXG:,.0f} 小於 I_Y = {Q_IYG:,.0f}，繞 X 控制，KL/r = {Q_KLR:.1f}",
            sub="單角鋼的 I 與距離 d 必須是同一個軸",
            note="形心距離由外緣量入：dX = 20 − cx、dY = 20 − cy；40 cm 不是形心間距",
            path=path)
    return path


def fig3_curve():
    cv = q_curve_panel(1000, 540, "柱強度曲線（彈性挫屈區）", f"Fy = {Q_FY}、E = {Q_E:g} tf/cm²；KL/r 超過 Cc 與 λc = 1.5",
                       Q_FY, Q_E, [(Q_KLR, f"{Q_KLR:.1f}", True), (Q_KLR_BAD, "", False)], kmax=200.0)
    cv.text_px(90 + 870 * Q_KLR_BAD / 200 + 6, 540 - 110 - 34, f"配錯 {Q_KLR_BAD:.1f}", 11.5, C["muted"], "start")
    path = os.path.join(OUT, f"{TAG}-fig-2-curve.svg")
    compose([cv], cols=1,
            title=f"圖 2　Pa = {Q_FA:.4f} × {Q_A:.1f} = {Q_PA:.1f} tf；φcPn = 0.85 × {Q_FCR:.3f} × {Q_A:.1f} = {Q_PU:.1f} tf",
            sub=f"Euler：Pcr = π²EI_X/(KL)² = {Q_PCR:.1f} tf；ASD Pa = Pcr / (23/12)",
            note="兩種方法都落在彈性段：ASD 用 12π²E/23(KL/r)²、LRFD 用 0.877Fy/λc²，不能套非彈性式",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "角鋼長短肢方向放錯；c_x、c_y 對應的軸對調；40 cm 當成形心間距"),
    (fig2_section, "§4 一",
     "單角鋼 Iy = 276 配上 15 cm（平行軸配對錯）；40 cm 當形心間距；控制軸選錯"),
    (fig3_curve, "§4 二、三",
     "KL/r > Cc 仍用非彈性式；把 Euler 112.4 tf 當容許載重"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
