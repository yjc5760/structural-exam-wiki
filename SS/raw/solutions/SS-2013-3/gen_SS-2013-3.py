#!/usr/bin/env python3
"""
SS-2013-3 W14x61 受軸壓柱（兩平面邊界不同、弱軸分段）— 解題圖解產生腳本

用法：
    python3 gen_SS-2013-3.py [輸出目錄]

三條鐵則的落實：
  1. 圖上每個數字都標明來自 SS-2013-3.md 哪一節
  2. 反曲點位置由挫屈特徵方程 tan(u)=u 解出（XI_INF_PF），不是寫死 0.3
  3. 每張圖在 FIGURES 表寫明攔什麼錯
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose, member_shape
from recipes import bar_compare

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2013-3"

# ══════════════════════════════════════════════════════════
# 解題結果（全部來自 SS-2013-3.md，勿手動改動）
# ══════════════════════════════════════════════════════════
# §1 題目給定
L_TOT   = 1600.0        # 柱總長 (cm)
XB      = 0.60          # B 點側撐位置（距 A，以 L 為單位）
# §4-一 斷面迴旋半徑
RX      = 15.17         # cm
RY      = 6.215         # cm
# §4-二～四 三個有效長細比（採考卷表列之理論 K 值）
K_X,  L_X  = 0.7, L_TOT                 # 強軸全柱：A 鉸 - C 固（無側位移）
K_YL, L_YL = 0.7, XB * L_TOT            # 弱軸下段 A-B：A 固 - B 鉸
K_YU, L_YU = 1.0, (1 - XB) * L_TOT      # 弱軸上段 B-C：B 鉸 - C 鉸
SR_X   = K_X  * L_X  / RX               # 73.8
SR_YL  = K_YL * L_YL / RY               # 108.1 ← 控制
SR_YU  = K_YU * L_YU / RY               # 103.0
SR_MAX = max(SR_X, SR_YL, SR_YU)
# §5.1 設計啟示：把 B 點下移至兩段 KL 相等之位置
A_OPT  = K_YU * L_TOT / (K_YL + K_YU)   # 0.7a = 1.0(L-a) → a = 941 cm
SR_OPT = K_YL * A_OPT / RY              # 106.0
# §4-五、六 最終答案
PA      = 96.8          # tf（ASD）
PHI_PN  = 134.3         # tf（LRFD, phi_c = 0.85）

# ── 挫屈模態：由特徵方程解出，不是憑印象畫 ──
# 固接-鉸接（propped cantilever）之特徵值為 tan(u) = u 的最小正根
def _solve_tan_u():
    lo, hi = math.pi * 1.0001, math.pi * 1.4999   # 根落在 (pi, 3pi/2)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if math.tan(mid) - mid > 0: hi = mid
        else: lo = mid
    return 0.5 * (lo + hi)

U_PF      = _solve_tan_u()          # = 4.4934
K_PF      = math.pi / U_PF          # = 0.6992 → 考卷表列理論值 0.7
XI_INF_PF = math.pi / U_PF          # 反曲點距「鉸端」之比例（＝ K_PF；鉸端本身即彎矩零點）

def _mode_pf(xi):
    """鉸端在 xi=0、固接端在 xi=1 之挫屈模態（未正規化）"""
    return math.sin(U_PF * xi) - U_PF * math.cos(U_PF) * xi

_PF_PEAK = max(abs(_mode_pf(i / 400)) for i in range(401))

def mode_pf(xi):   return _mode_pf(xi) / _PF_PEAK          # 鉸(0) - 固(1)
def mode_fp(xi):   return mode_pf(1 - xi)                  # 固(0) - 鉸(1)
def mode_pp(xi):   return math.sin(math.pi * xi)           # 鉸(0) - 鉸(1)

AMP = 0.105        # 繪圖用模態振幅（純視覺，不影響任何物理量）


# ══════════════════════════════════════════════════════════
def _guided_fixed(cv, p, half=0.085, hh=0.052):
    """『固接可沿軸向滑動』：方塊夾於兩排滾輪導軌之間
       轉動被拘束、側向位移被拘束，僅容許沿軸向滑動"""
    x, y = p
    px, py = cv.X(x), cv.Y(y)
    s = cv.sx
    cv.rect_px(px - 0.030 * s, py - hh * s, 0.060 * s, 2 * hh * s, C["member"], 3)
    for sgn in (-1, +1):
        wx = px + sgn * half * s
        cv.parts.append(f'<line x1="{wx:.2f}" y1="{py - (hh + 0.030) * s:.2f}" '
                        f'x2="{wx:.2f}" y2="{py + (hh + 0.030) * s:.2f}" '
                        f'stroke="{C["member"]}" stroke-width="3.2" stroke-linecap="round"/>')
        for k in range(5):
            yy = py - (hh + 0.026) * s + k * (2 * (hh + 0.026) * s) / 4
            cv.parts.append(f'<line x1="{wx:.2f}" y1="{yy:.2f}" '
                            f'x2="{wx + sgn * 9:.2f}" y2="{yy - 8:.2f}" '
                            f'stroke="{C["member"]}" stroke-width="1.8" stroke-linecap="round"/>')
        for t in (-0.55, 0.0, 0.55):
            cv.parts.append(f'<circle cx="{px + sgn * 0.0435 * s:.2f}" '
                            f'cy="{py + t * hh * s:.2f}" r="{0.0125 * s:.2f}" '
                            f'fill="none" stroke="{C["member"]}" stroke-width="1.9"/>')
    cv.arrow((x, y + 0.125), (x, y + 0.060), C["load"], 3.4, 11)
    cv.math_px(px, cv.Y(y + 0.125) - 15, "P", 18, C["load"], weight="700")


def _lateral_brace(cv, p, side=+1, half=0.085):
    """鉸接側向支撐：滾輪貼牆（只拘束側向位移、容許轉動）"""
    x, y = p
    px, py = cv.X(x), cv.Y(y)
    s = cv.sx
    wx = px + side * half * s
    cv.parts.append(f'<line x1="{wx:.2f}" y1="{py - 0.058 * s:.2f}" x2="{wx:.2f}" '
                    f'y2="{py + 0.058 * s:.2f}" stroke="{C["member"]}" '
                    f'stroke-width="3.2" stroke-linecap="round"/>')
    for k in range(5):
        yy = py - 0.050 * s + k * (0.100 * s) / 4
        cv.parts.append(f'<line x1="{wx:.2f}" y1="{yy:.2f}" x2="{wx + side * 9:.2f}" '
                        f'y2="{yy - 8:.2f}" stroke="{C["member"]}" stroke-width="1.8" '
                        f'stroke-linecap="round"/>')
    for t in (-0.5, 0.5):
        cv.parts.append(f'<circle cx="{px + side * 0.055 * s:.2f}" cy="{py + t * 0.032 * s:.2f}" '
                        f'r="{0.0125 * s:.2f}" fill="none" stroke="{C["member"]}" stroke-width="1.9"/>')
    cv.parts.append(f'<line x1="{px:.2f}" y1="{py:.2f}" x2="{px + side * 0.042 * s:.2f}" '
                    f'y2="{py:.2f}" stroke="{C["member"]}" stroke-width="2.4"/>')
    cv.dot((x, y), 4.6, fill="#FFFFFF", stroke=C["member"], w=2.4)


def _seg_mode(cv, y0, y1, f, amp, color, w=5.0):
    """在 [y0,y1] 區間畫挫屈模態（模型座標，柱位於 x=0）"""
    cv.poly(member_shape((0, y0), (0, y1), lambda xi: -amp * f(xi), n=90), color, w)


def mode_x(f, xi, amp=AMP):
    """該模態在局部座標 xi 處的整體 x 座標。
    member_shape 的法向為 (-dy,dx)/L，垂直上行桿件即 (-1,0)，
    故 w = -amp*f 對應到 x = +amp*f —— 標註點必須用同一式，否則會標到曲線另一側。"""
    return amp * f(xi)


def _kl_bracket(cv, x, y0, y1, color, label, sub=None):
    """在 x 處畫一段有效長度的括號並標註"""
    cv.line((x, y0), (x, y1), color, 2.4)
    for yy in (y0, y1):
        cv.line((x - 0.022, yy), (x + 0.022, yy), color, 2.4)
    cv.math_px(cv.X(x) + 11, cv.Y((y0 + y1) / 2) + (-9 if sub else 0),
               label, 13.5, color, "start", weight="700")
    if sub:
        cv.text_px(cv.X(x) + 11, cv.Y((y0 + y1) / 2) + 13, sub, 12.5, color, "start", weight="700")


# ══════════════════════════════════════════════════════════
def fig2_boundaries():
    """兩平面邊界條件與挫屈模態：K 值 = 兩個彎矩零點之間的距離"""
    PW, PH = 520, 620
    SX, OX, OY = 350, 200, 134
    XBR = 0.20                      # 有效長度括號的擺放位置

    # ── 左：y-z 面（強軸）──
    a = Canvas(PW, PH, sx=SX, ox=OX, oy=OY)
    a.panel("y-z 面（強軸，用 I_x、r_x）", "A 鉸 - C 固接可滑動｜全長無中間支撐")
    a.line((0, 0), (0, 1), C["ghost"], 3.0, dash="6 5", cap="butt")
    _seg_mode(a, 0, 1, mode_pf, AMP, C["deform"])
    a.pin_support((0, 0), size=17)
    _guided_fixed(a, (0, 1))
    a.dot((0, 0), 5.2, fill=C["member"])
    a.text((0, 0), "A", 16, C["text"], weight="700", dx=-30, dy=-8)
    a.text((0, 1), "C", 16, C["text"], weight="700", dx=-60, dy=6)
    a.dot((0, XB), 4.2, fill=C["muted"])
    a.text((0, XB), "B", 15, C["muted"], weight="700", dx=-24, dy=0)
    yi = XI_INF_PF                                  # 反曲點：由 tan(u)=u 解出，非目測
    a.dot((mode_x(mode_pf, yi), yi), 5.6, fill="#FFFFFF", stroke=C["accent"], w=2.9)
    a.text_px(a.X(0) - 14, a.Y(yi), "反曲點", 12.5, C["accent"], "end", weight="700")
    a.dim((0, 0), (0, 1), f"L = {L_TOT:.0f} cm", off=-108, label_off=-14)
    _kl_bracket(a, XBR, 0, yi, C["accent"], f"K_{{x}}L = 0.7(1600) = {K_X * L_X:.0f} cm")
    a.text_px(PW / 2, PH - 84, "強軸全柱（B 點側撐不在本平面，故不分段）", 12.5, C["muted"])
    a.math_px(PW / 2, PH - 59, f"(KL/r)_{{x}} = {K_X * L_X:.0f} / {RX} = {SR_X:.1f}",
              15.5, C["deform"], weight="700")
    a.text_px(PW / 2, PH - 34,
              f"不控制　｜　挫屈方程理論解 {K_PF:.3f}L = {K_PF * L_TOT:.0f} cm，考卷表列取 0.7",
              11.5, C["muted"])

    # ── 右：x-z 面（弱軸）──
    b = Canvas(PW, PH, sx=SX, ox=OX, oy=OY)
    b.panel("x-z 面（弱軸，用 I_y、r_y）", "A 固接｜B、C 鉸接側向支撐 → 分兩段")
    b.line((0, 0), (0, 1), C["ghost"], 3.0, dash="6 5", cap="butt")
    _seg_mode(b, 0, XB, mode_fp, AMP, C["accent"])          # 下段：控制段
    _seg_mode(b, XB, 1, mode_pp, AMP * 0.78, C["deform"])   # 上段
    b.fixed_support((0, 0), size=19)
    _lateral_brace(b, (0, XB))
    _lateral_brace(b, (0, 1))
    b.arrow((0, 1.125), (0, 1.035), C["load"], 3.4, 11)
    b.math_px(b.X(0), b.Y(1.125) - 15, "P", 18, C["load"], weight="700")
    b.text((0, 0), "A", 16, C["text"], weight="700", dx=-32, dy=-8)
    b.text((0, XB), "B", 16, C["text"], weight="700", dx=-28, dy=0)
    b.text((0, 1), "C", 16, C["text"], weight="700", dx=-28, dy=0)
    yj = (1 - XI_INF_PF) * XB                       # 下段反曲點：距固接端 (1-0.699) 之比例
    b.dot((mode_x(mode_fp, yj / XB), yj), 5.6, fill="#FFFFFF", stroke=C["accent"], w=2.9)
    b.text_px(b.X(0) - 14, b.Y(yj), "反曲點", 12.5, C["accent"], "end", weight="700")
    b.dim((0, 0), (0, XB), f"0.6L = {L_YL:.0f} cm", off=-108, label_off=-14)
    b.dim((0, XB), (0, 1), f"0.4L = {L_YU:.0f} cm", off=-108, label_off=-14)
    _kl_bracket(b, XBR, 0, XB, C["accent"],
                f"KL = 0.7({L_YL:.0f}) = {K_YL * L_YL:.0f} cm", "← 控制")
    _kl_bracket(b, XBR, XB, 1, C["deform"],
                f"KL = 1.0({L_YU:.0f}) = {K_YU * L_YU:.0f} cm")
    b.text_px(PW / 2, PH - 84, "弱軸分兩段，兩段各自檢核", 12.5, C["muted"])
    b.math_px(PW / 2, PH - 59, f"(KL/r)_{{y}} = {K_YL * L_YL:.0f} / {RY} = {SR_YL:.1f}",
              15.5, C["accent"], weight="700")
    b.text_px(PW / 2, PH - 34,
              f"下段 A–B 控制全題　｜　上段 B–C：{K_YU * L_YU:.0f} / {RY} = {SR_YU:.1f}，不控制",
              11.5, C["accent"])

    compose([a, b],
            title="同一根柱、兩個平面：邊界條件與分段各自獨立判斷",
            sub="有效長度 KL ＝ 該平面內兩個彎矩零點（反曲點或鉸端）之間的距離",
            note="柱底條件在兩平面相反（強軸鉸、弱軸固）；B 點側撐畫在 x-z 面，"
                 "只切弱軸，強軸仍為全長 1600 cm",
            path=f"{OUT}/{TAG}-fig-2-boundaries.svg")
    return f"{OUT}/{TAG}-fig-2-boundaries.svg"


# ══════════════════════════════════════════════════════════
def fig3_slenderness():
    """三段長細比比較：最長的 KL 未必控制，最短的 L 也未必安全"""
    A = 0.30            # 迷你示意圖的模態振幅（僅為在 120x74 的小格中看得出形狀）

    def sketch(mini, i):
        mini.line((0, 0), (0, 1), C["ghost"], 2.0, dash="4 4", cap="butt")
        segs = {0: [((0, 1), mode_pf, C["deform"])],
                1: [((0, XB), mode_fp, C["accent"])],
                2: [((XB, 1), mode_pp, C["deform"])],
                3: [((0, A_OPT / L_TOT), mode_fp, C["muted"]),
                    ((A_OPT / L_TOT, 1), mode_pp, C["muted"])]}[i]
        for (y0, y1), f, col in segs:
            mini.poly(member_shape((0, y0), (0, y1), lambda x: -A * f(x), 50), col, 3.0)
            for yy in (y0, y1):                       # 該段的端點（＝彎矩零點或束制點）
                mini.line((-0.13, yy), (0.13, yy), col, 2.0)

    bar_compare(
        [("強軸　y-z 面（全柱）", "A 鉸-C 固，K = 0.7",
          SR_X, f"L = {L_X:.0f}, KL = {K_X * L_X:.0f} cm, KL/r = {SR_X:.1f}", C["deform"]),
         ("弱軸　下段 A–B　控制", "A 固-B 鉸，K = 0.7",
          SR_YL, f"L = {L_YL:.0f}, KL = {K_YL * L_YL:.0f} cm, KL/r = {SR_YL:.1f}", C["accent"]),
         ("弱軸　上段 B–C", "B 鉸-C 鉸，K = 1.0",
          SR_YU, f"L = {L_YU:.0f}, KL = {K_YU * L_YU:.0f} cm, KL/r = {SR_YU:.1f}", C["deform"]),
         (f"B 點下移至 {A_OPT:.0f} cm", "§5.1 設計啟示",
          SR_OPT, f"KL = {K_YL * A_OPT:.0f} cm (2 seg), KL/r = {SR_OPT:.1f}", C["muted"])],
        title="三段各自算完再比：控制的是 KL/r 最大者，不是 KL 最大者、也不是 L 最長者",
        sub=f"強軸 KL = {K_X * L_X:.0f} cm 為三者最大，卻因 r_x = {RX} cm 而長細比最小；"
            f"弱軸上段 L 最短（{L_YU:.0f} cm），但 K = 1.0 使其 KL 反而逼近下段的 "
            f"{K_YL * L_YL:.0f} cm",
        note=f"控制值 (KL/r)_{{max}} = {SR_MAX:.1f}，低於規範建議上限 200 ✓　→　"
             f"P_a = {PA} tf（ASD）、φ_c P_n = {PHI_PN:.0f} tf（LRFD, φ_c = 0.85）",
        sketch=sketch, W=1180,
        path=f"{OUT}/{TAG}-fig-3-slenderness.svg")
    return f"{OUT}/{TAG}-fig-3-slenderness.svg"


# ══════════════════════════════════════════════════════════
FIGURES = [
    (fig2_boundaries,  "§1·§4二·§4三",
     "兩平面柱底條件相反被誤讀成同一組；B 點側撐被誤用來切割強軸"),
    (fig3_slenderness, "§4四·§5.1",
     "拿 L（或 KL）互比而非比 KL/r → 控制段選錯"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"特徵方程 tan(u)=u 之根 u = {U_PF:.4f} → K = pi/u = {K_PF:.4f}（考卷表列 0.7）")
    print(f"反曲點距鉸端 = {XI_INF_PF:.4f} L")
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<44} {section:<16} 攔：{catches}")
