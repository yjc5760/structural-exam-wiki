#!/usr/bin/env python3
"""
SS-2015-3 2×C200×75 組合柱（最小迴旋半徑 ＋ ASD 反算最大長度）— 解題圖解產生腳本

用法：
    python3 gen_SS-2015-3.py [輸出目錄]

三條鐵則的落實：
  1. 圖上每個數字都標明來自 SS-2015-3.md 哪一節
  2. 形心位置 d 由「外寬/2 − C_y」現算，慣性矩由平行軸定理現算；
     改外寬或 C_y，斷面圖與 I_X／I_Y 會一起變
  3. 每張圖在 FIGURES 表寫明攔什麼錯
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose, member_shape

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2015-3"

# ══════════════════════════════════════════════════════════
# 解題結果（全部來自 SS-2015-3.md，勿手動改動）
# ══════════════════════════════════════════════════════════
# §1 題目給定（單根 C200×75）
IX1, IY1, A1, CY = 1970.0, 170.0, 29.9, 2.49      # cm^4, cm^4, cm^2, cm
W_OUT = 30.0        # 兩腹板外緣總寬（cm）
D_SEC = 20.0        # 腹板高＝斷面深度（cm）＝ C200 的「200 mm」
FY, ES = 2.52, 2040.0
PA = 21.1           # tf
KK = 2.0            # 有效長度係數（題目給定；固接*-鉸接）
KK_CANT = 2.1       # 懸臂柱之「設計」k（§5 進階表）
# §4 Part(一)
D_OFF = W_OUT / 2 - CY                 # 12.51 cm　每根形心距組合 Y 軸
A_TOT = 2 * A1                         # 59.8 cm^2
I_X = 2 * IX1                          # 3,940 cm^4（形心都在 X 軸上，不需平行軸）
I_Y = 2 * (IY1 + A1 * D_OFF ** 2)      # 9,698 cm^4（需平行軸 Ad^2）
R_X = math.sqrt(I_X / A_TOT)           # 8.12 cm ← 控制
R_Y = math.sqrt(I_Y / A_TOT)           # 12.73 cm
# §4 Part(二)
FA = PA / A_TOT                        # 0.353 tf/cm^2
CC = math.sqrt(2 * math.pi ** 2 * ES / FY)          # 126.4
SR = math.sqrt(12 * math.pi ** 2 * ES / (23 * FA))  # 172.5
L_MAX = SR * R_X / KK                  # 700 cm
L_IF_CANT = SR * R_X / KK_CANT         # 若誤取設計 k = 2.1

# 斷面繪圖用板厚（示意，題目未給；圖上不標註厚度數值）
TW, TF = 0.7, 1.3
BF = 7.5            # C200×75 之翼板寬 75 mm


# ══════════════════════════════════════════════════════════
# 圖 2：組合斷面幾何與兩軸慣性矩
# ══════════════════════════════════════════════════════════
PW2, PH2 = 400, 430
SX2, OX2, OY2 = 8.53, 200, 222


def _channel(cv, side, fill, stroke, w=1.6):
    """單根 C200×75，翼板朝內、腹板朝外。side=-1 為左（「[」）、+1 為右（「]」）"""
    xo = side * W_OUT / 2                 # 腹板外緣
    xw = xo - side * TW                   # 腹板內緣
    xi = xo - side * BF                   # 翼板內端
    h = D_SEC / 2
    cv.polygon([(xo, -h), (xw, -h), (xw, h), (xo, h)], fill, stroke, w)          # 腹板
    for sgn in (+1, -1):
        y0, y1 = sgn * h, sgn * (h - TF)
        cv.polygon([(xw, y0), (xi, y0), (xi, y1), (xw, y1)], fill, stroke, w)    # 翼板


def _section(cv, fill=C["fill_c"], stroke=C["member"]):
    for side in (-1, +1):
        _channel(cv, side, fill, stroke)


def _panel2(title, sub):
    cv = Canvas(PW2, PH2, sx=SX2, ox=OX2, oy=OY2)
    cv.panel(title, sub)
    return cv


def _p_geom():
    cv = _panel2("① 斷面尺寸判讀", "翼板朝內、腹板朝外（「[ ]」型）")
    _section(cv)
    for side in (-1, +1):
        cv.dot((side * (W_OUT / 2 - CY), 0), 5.0, fill=C["accent"])
    cv.dim((-W_OUT / 2, -D_SEC / 2), (W_OUT / 2, -D_SEC / 2),
           f"外寬 {W_OUT:.0f} cm", off=26, label_off=12)
    cv.dim((-W_OUT / 2, D_SEC / 2), (-W_OUT / 2, -D_SEC / 2),
           f"{D_SEC:.0f} cm", off=34, label_off=13)
    cv.dim((-W_OUT / 2, D_SEC / 2 + 1.2), (-W_OUT / 2 + CY, D_SEC / 2 + 1.2),
           f"C_y = {CY}", off=-26, label_off=-12)
    cv.text_px(PW2 / 2, PH2 - 78,
               f"{D_SEC:.0f} cm 是腹板高（C200 的「200」），不是形心間距", 12.5, C["load"],
               weight="700")
    cv.math_px(PW2 / 2, PH2 - 53,
               f"d = {W_OUT:.0f}/2 − C_y = 15 − {CY} = {D_OFF:.2f} cm", 14,
               C["accent"], weight="700")
    cv.text_px(PW2 / 2, PH2 - 29, "（每根槽鋼形心距組合 Y 軸）", 11.5, C["muted"])
    return cv


def _p_x():
    cv = _panel2("② 繞 X 軸（弱軸 ← 控制）", "兩形心都落在 X 軸上")
    _section(cv, "#FFFFFF", C["ghost"])
    cv.line((-W_OUT / 2 - 2.4, 0), (W_OUT / 2 + 2.4, 0), C["accent"], 3.0)
    cv.math_px(cv.X(W_OUT / 2 + 2.4) + 8, cv.Y(0), "X", 15, C["accent"], "start", weight="700")
    for side in (-1, +1):
        cv.dot((side * (W_OUT / 2 - CY), 0), 5.4, fill=C["accent"])
    cv.text_px(PW2 / 2, PH2 - 104, "形心到 X 軸的距離 = 0 ⇒ 不需平行軸 Ad²",
               12.5, C["muted"])
    cv.math_px(PW2 / 2, PH2 - 78,
               f"I_X = 2({IX1:,.0f}) = {I_X:,.0f} cm^{{4}}", 14, C["accent"], weight="700")
    cv.text_px(PW2 / 2, PH2 - 52,
               f"r_X = √({I_X:,.0f}/{A_TOT}) = {R_X:.2f} cm", 14, C["accent"], weight="700")
    cv.text_px(PW2 / 2, PH2 - 28, "← 最小迴旋半徑，控制本題", 12.5, C["accent"], weight="700")
    return cv


def _p_y():
    cv = _panel2("③ 繞 Y 軸", "形心偏離 Y 軸 d，必須用平行軸")
    _section(cv, "#FFFFFF", C["ghost"])
    cv.line((0, -D_SEC / 2 - 1.6), (0, D_SEC / 2 + 2.4), C["deform"], 3.0)
    cv.math_px(cv.X(0) + 13, cv.Y(D_SEC / 2 + 2.4) - 8, "Y", 15, C["deform"],
               "start", weight="700")
    for side in (-1, +1):
        xc = side * (W_OUT / 2 - CY)
        cv.dot((xc, 0), 5.4, fill=C["deform"])
        cv.line((xc, 0), (xc, 4.5), C["deform"], 1.2, dash="3 3")
        cv.dim((0, 4.5), (xc, 4.5),
               f"d = {D_OFF:.2f}" if side > 0 else "d", off=0,
               label_off=(-13 if side > 0 else 13))
    cv.text_px(PW2 / 2, PH2 - 104, "形心偏離 Y 軸 ⇒ 必須加 Ad²", 12.5, C["muted"])
    cv.math_px(PW2 / 2, PH2 - 78,
               f"I_Y = 2({IY1:.0f} + {A1}×{D_OFF:.2f}^{{2}}) = {I_Y:,.0f} cm^{{4}}",
               13.5, C["deform"], weight="700")
    cv.math_px(PW2 / 2, PH2 - 52,
               f"r_Y = {R_Y:.2f} cm", 14, C["deform"], weight="700")
    cv.text_px(PW2 / 2, PH2 - 28, "不控制（加大槽鋼間距只會讓它更大）", 12.5, C["muted"])
    return cv


def fig2_section():
    compose([_p_geom(), _p_x(), _p_y()], cols=3,
            title="組合斷面：哪一軸需要平行軸定理，決定了誰是弱軸",
            sub=f"加大兩槽鋼間距只會增加繞 Y 軸的慣性矩，對繞 X 軸完全無效 ⇒ "
                f"無論間距多大，X 軸永遠是弱軸（{I_X:,.0f} 小於 {I_Y:,.0f} cm⁴）",
            note=f"最小迴旋半徑 r = {R_X:.2f} cm（繞 X 軸）；"
                 f"若誤把圖上的 {D_SEC:.0f} cm 當成形心間距，d 會由 {D_OFF:.2f} 變成 10，"
                 f"繞 Y 軸的慣性矩隨之算錯",
            path=f"{OUT}/{TAG}-fig-2-section.svg")
    return f"{OUT}/{TAG}-fig-2-section.svg"


# ══════════════════════════════════════════════════════════
# 圖 3：k = 2.0 的邊界型式 vs 懸臂柱
# ══════════════════════════════════════════════════════════
PW3, PH3 = 450, 580
SX3, OX3 = 168.0, 155.0
DELTA = 0.26          # 繪圖用側向位移（純視覺）


def _slider_top(cv, p, half=0.13):
    """頂端『可平移、不可轉動』：與柱剛接之滑塊，下方置滾輪於水平面上"""
    x, y = p
    px, py = cv.X(x), cv.Y(y)
    s = cv.sx
    cv.rect_px(px - half * s, py - 0.030 * s, 2 * half * s, 0.060 * s, C["member"], 4)
    for t in (-0.62, 0.0, 0.62):
        cv.parts.append(f'<circle cx="{px + t * half * s:.2f}" cy="{py + 0.052 * s:.2f}" '
                        f'r="{0.021 * s:.2f}" fill="none" stroke="{C["member"]}" stroke-width="2"/>')
    gy = py + 0.073 * s
    cv.parts.append(f'<line x1="{px - 0.20 * s:.2f}" y1="{gy:.2f}" x2="{px + 0.20 * s:.2f}" '
                    f'y2="{gy:.2f}" stroke="{C["member"]}" stroke-width="2.6" stroke-linecap="round"/>')
    for k in range(7):
        gx = px - 0.185 * s + k * (0.37 * s) / 6
        cv.parts.append(f'<line x1="{gx:.2f}" y1="{gy:.2f}" x2="{gx - 8:.2f}" y2="{gy + 9:.2f}" '
                        f'stroke="{C["member"]}" stroke-width="1.8" stroke-linecap="round"/>')


def _mode_panel(title, sub, mode, y_real, y_virt, sup_bottom, sup_top,
                k_th, k_dg, note1, note2, oy):
    cv = Canvas(PW3, PH3, sx=SX3, ox=OX3, oy=oy)
    cv.panel(title, sub)
    y0v, y1v = y_virt
    y0r, y1r = y_real
    cv.line((0, min(y0v, y0r) - 0.06), (0, max(y1v, y1r) + 0.06), C["ghost"], 2.4, dash="6 5")
    # 虛擬延伸段（把柱補成等值的兩端彎矩為零之柱）
    cv.poly(member_shape((0, y0v), (0, y1v), lambda t: -DELTA * mode(y0v + (y1v - y0v) * t), 90),
            C["ghost"], 3.4, dash="7 5")
    # 實際柱段
    cv.poly(member_shape((0, y0r), (0, y1r), lambda t: -DELTA * mode(y0r + (y1r - y0r) * t), 90),
            C["deform"], 5.4)
    sup_bottom(cv)
    sup_top(cv)
    # 彎矩零點（等值柱的兩端）
    for yy in (min(y0v, y0r), max(y1v, y1r)):
        cv.dot((DELTA * mode(yy), yy), 5.6, fill="#FFFFFF", stroke=C["accent"], w=2.9)
    lo, hi = min(y0v, y0r), max(y1v, y1r)
    cv.line((0.52, lo), (0.52, hi), C["accent"], 2.4)
    for yy in (lo, hi):
        cv.line((0.495, yy), (0.545, yy), C["accent"], 2.4)
    cv.math_px(cv.X(0.52) + 11, cv.Y(0.5 * (lo + hi)), "KL = 2L", 14.5, C["accent"],
               "start", weight="700")
    cv.text_px(cv.X(0.52) + 11, cv.Y(0.5 * (lo + hi)) + 20, "（兩彎矩零點之間）",
               11.5, C["accent"], "start")
    cv.dim((-0.30, y0r), (-0.30, y1r), "L", off=0, label_off=-14)
    cv.text_px(PW3 / 2, PH3 - 82, f"理論 k = {k_th}　　設計 k = {k_dg}", 14,
               C["text"], weight="700")
    cv.text_px(PW3 / 2, PH3 - 56, note1, 12.5, C["muted"])
    cv.text_px(PW3 / 2, PH3 - 30, note2, 13, C["accent"], weight="700")
    return cv


def fig3_boundary():
    def mode_this(xi):      # 底鉸（M=0）、頂端不可轉動：sin(πξ/2)
        return math.sin(math.pi * xi / 2)

    def mode_cant(xi):      # 底固接、頂自由：1 − cos(πξ/2)
        return 1 - math.cos(math.pi * xi / 2)

    a = _mode_panel(
        "本題：固接*-鉸接", "底端鉸接（可轉、不可移）｜頂端可平移、不可轉動",
        mode_this, (0.0, 1.0), (1.0, 2.0),
        lambda cv: cv.pin_support((0, 0), size=16),
        lambda cv: _slider_top(cv, (DELTA, 1.0)),
        "2.0", "2.0",
        "曲率最大在頂端，柱底彎矩為零", 
        f"L = {SR:.1f} × {R_X:.2f} / {KK} = {L_MAX:.0f} cm",
        oy=120.4)

    b = _mode_panel(
        "懸臂柱：自由端*-固接", "底端固接（不可轉、不可移）｜頂端完全自由",
        mode_cant, (0.0, 1.0), (-1.0, 0.0),
        lambda cv: cv.fixed_support((0, 0), size=18),
        lambda cv: None,
        "2.0", "2.1",
        "曲率最大在柱底，頂端彎矩為零",
        f"若誤判為懸臂柱：L = {SR:.1f} × {R_X:.2f} / {KK_CANT} = {L_IF_CANT:.0f} cm",
        oy=288.4)

    compose([a, b],
            title="兩者理論 k 都是 2.0，但不是同一種柱",
            sub="兩柱均於柱頂承受軸壓 P。灰虛線為「把柱補成兩端彎矩為零」的虛擬延伸段；"
                "兩個空心圓即等值柱的兩個彎矩零點，其間距就是 KL",
            note=f"本題柱底是鉸、曲率最大在頂端；懸臂柱柱底是固接、曲率最大在柱底。"
                 f"設計 k 一個 2.0、一個 2.1，判錯會讓容許長度由 {L_MAX:.0f} 掉到 "
                 f"{L_IF_CANT:.0f} cm（{100 * (L_IF_CANT / L_MAX - 1):.1f}%）",
            path=f"{OUT}/{TAG}-fig-3-boundary.svg")
    return f"{OUT}/{TAG}-fig-3-boundary.svg"


# ══════════════════════════════════════════════════════════
FIGURES = [
    (fig2_section,  "§4 Part(一)",
     "把圖上的 20 cm 當成形心間距、或對 I_X 誤加平行軸 Ad²"),
    (fig3_boundary, "§5 進階·§4 Part(二)",
     "把「固接*-鉸接」說成懸臂柱 → 設計 k 取 2.1"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"d = {D_OFF:.2f} cm　I_X = {I_X:,.0f}　I_Y = {I_Y:,.0f} cm^4")
    print(f"r_X = {R_X:.3f}　r_Y = {R_Y:.3f} cm　KL/r = {SR:.1f}　C_c = {CC:.1f}")
    print(f"L = {L_MAX:.1f} cm　（若誤取設計 k = 2.1 則 {L_IF_CANT:.1f} cm）")
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<44} {section:<18} 攔：{catches}")
