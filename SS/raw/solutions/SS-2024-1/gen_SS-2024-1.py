#!/usr/bin/env python3
"""
SS-2024-1 具塊狀殘餘應力之柱強度曲線 — 解題圖解產生腳本

用法：
    python3 gen_SS-2024-1.py [輸出目錄]

三條鐵則的落實：
  1. 圖上每個數字都標明來自 SS-2024-1.md 哪一節
  2. 三個轉折點由 I_e/I_x 現算（LAM1/LAM2/LAM3），且 I_e 由斷面尺寸算出，
     改 b_out 或 t_f，斷面圖與曲線會一起變
  3. 每張圖在 FIGURES 表寫明攔什麼錯
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2024-1"

# ══════════════════════════════════════════════════════════
# 解題結果（全部來自 SS-2024-1.md，勿手動改動）
# ══════════════════════════════════════════════════════════
# §1 斷面 RH400×400×13×21（cm）
H_SEC, BF, TW, TF = 40.0, 40.0, 1.3, 2.1
B_OUT = 11.35           # 翼板外側降伏段寬（每邊，共 4 塊）
B_MID = 17.3            # 翼板中央段寬
SR_C, SR_T = -0.5, +0.4  # 殘餘應力（以 F_y 為單位）：外側壓、中央與腹板拉
IX = 66600.0            # cm^4（題目給定）
IY = 22400.0            # cm^4
# §4 步驟二：有效慣性矩
YBAR = (H_SEC - TF) / 2                      # 18.95 cm
A_OUT = B_OUT * TF                           # 23.84 cm^2
DI_ONE = B_OUT * TF ** 3 / 12 + A_OUT * YBAR ** 2   # 8,568 cm^4
IE = IX - 4 * DI_ONE                         # 32,330 cm^4
RATIO = IE / IX                              # 0.485
# §4 步驟一、三、四：比例限與三個轉折點
FP = 0.5                                     # F_p / F_y（＝ 外側殘餘壓應力大小）
LAM1 = math.sqrt(RATIO)                      # 0.697　壓潰 → 非彈性
LAM2 = math.sqrt(RATIO / FP)                 # 0.985　非彈性 → 平台
LAM3 = math.sqrt(1 / FP)                     # 1.414　平台 → 彈性 Euler
# §5.1 常見誤畫法：把非彈性分支硬拉到 λ = √2
WRONG_AT_LAM3 = RATIO / LAM3 ** 2            # 0.243
# §5.4 弱軸對照
IEY = 2 * TF * B_MID ** 3 / 12 + (H_SEC - 2 * TF) * TW ** 3 / 12
RATIO_Y = IEY / IY                           # 0.081


def curve(lam):
    """本題四段曲線（§4 步驟五）"""
    if lam <= LAM1:  return 1.0
    if lam <= LAM2:  return RATIO / lam ** 2
    if lam <= LAM3:  return FP
    return 1.0 / lam ** 2


def ideal(lam):
    """圖(a) 無殘餘應力之理想曲線"""
    return 1.0 if lam <= 1.0 else 1.0 / lam ** 2


def crc(lam):
    """考卷所列之 CRC 拋物線（線性殘餘應力分布，§5.3）"""
    return 1 - lam ** 2 / 4 if lam <= math.sqrt(2) else 1.0 / lam ** 2


# ══════════════════════════════════════════════════════════
# 圖 2：斷面殘餘應力分布與有效斷面
# ══════════════════════════════════════════════════════════
PW2, PH2 = 500, 490
SX2, OX2, OY2 = 6.82, 220, 242

FL_SEGS = [(-BF / 2, -BF / 2 + B_OUT, SR_C),
           (-B_MID / 2, B_MID / 2, SR_T),
           (BF / 2 - B_OUT, BF / 2, SR_C)]


def _rect(cv, x0, x1, y0, y1, fill, stroke="none", w=1):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, stroke, w)


def _section(cv, effective_only=False):
    """RH400×400×13×21 斷面。effective_only=True 時外側 4 塊畫成已挖除"""
    yft0, yft1 = H_SEC / 2 - TF, H_SEC / 2          # 上翼板
    for sgn in (+1, -1):
        for x0, x1, sr in FL_SEGS:
            y0, y1 = (yft0, yft1) if sgn > 0 else (-yft1, -yft0)
            yielded = (sr < 0)
            if effective_only and yielded:
                _rect(cv, x0, x1, y0, y1, "#FFFFFF", C["ghost"], 1.4)
                for k in range(6):                   # 挖除區以斜線表示
                    xx = x0 + (x1 - x0) * (k + 0.5) / 6
                    cv.line((xx - 0.8, y0), (xx + 0.8, y1), C["ghost"], 1.2)
            else:
                fill = C["fill_c"] if yielded else C["fill_t"]
                _rect(cv, x0, x1, y0, y1, fill, C["member"], 1.6)
    _rect(cv, -TW / 2, TW / 2, -(H_SEC / 2 - TF), H_SEC / 2 - TF,
          C["fill_t"], C["member"], 1.6)
    cv.line((-BF / 2, H_SEC / 2), (BF / 2, H_SEC / 2), C["member"], 2.0, cap="butt")
    cv.line((-BF / 2, -H_SEC / 2), (BF / 2, -H_SEC / 2), C["member"], 2.0, cap="butt")


def _axes_xy(cv):
    cv.line((-BF / 2 - 2.6, 0), (BF / 2 + 2.6, 0), C["muted"], 1.4, dash="7 4")
    cv.line((0, -H_SEC / 2 - 1.5), (0, H_SEC / 2 + 1.5), C["muted"], 1.4, dash="7 4")
    cv.math_px(cv.X(BF / 2 + 2.6) + 8, cv.Y(0), "x", 14, C["muted"], "start")
    cv.math_px(cv.X(0) - 12, cv.Y(H_SEC / 2 + 1.5) - 8, "y", 14, C["muted"], "end")


def fig2_section():
    a = Canvas(PW2, PH2, sx=SX2, ox=OX2, oy=OY2)
    a.panel("圖(b) 殘餘應力分布（自平衡）",
            "翼板外側 4 塊受壓 −0.5F_y｜中央段與腹板受拉 +0.4F_y（尺寸單位 mm）")
    _section(a)
    _axes_xy(a)
    for sgn in (+1, -1):
        yy = sgn * (H_SEC / 2 - TF / 2)
        for x0, x1, sr in FL_SEGS:
            a.math_px(a.X(0.5 * (x0 + x1)), a.Y(yy),
                      f"{sr:+.1f}", 12, C["compr"] if sr < 0 else C["tension"], weight="700")
    a.math_px(a.X(0) + 14, a.Y(0) - 60, "+0.4", 12, C["tension"], "start", weight="700")
    a.dim((-BF / 2, H_SEC / 2), (-BF / 2 + B_OUT, H_SEC / 2), f"{B_OUT * 10:.1f}",
          off=-30, label_off=-12)
    a.dim((-B_MID / 2, H_SEC / 2), (B_MID / 2, H_SEC / 2), f"{B_MID * 10:.0f}",
          off=-30, label_off=-12)
    a.dim((BF / 2 - B_OUT, H_SEC / 2), (BF / 2, H_SEC / 2), f"{B_OUT * 10:.1f}",
          off=-30, label_off=-12)
    a.text_px(PW2 / 2, PH2 - 58,
              "外側 4 塊在平均應力達 0.5F_y 時「整塊同時降伏」", 12.5, C["muted"])
    a.text_px(PW2 / 2, PH2 - 33,
              "中央段與腹板為拉應力 → 需 1.4F_y 才降伏 ⇒ 全程彈性",
              13, C["tension"], weight="700")

    b = Canvas(PW2, PH2, sx=SX2, ox=OX2, oy=OY2)
    b.panel("有效斷面（外側已降伏，E_t = 0）",
            "降伏區等於「從斷面上挖掉」，再對 x 軸算 Euler")
    _section(b, effective_only=True)
    _axes_xy(b)
    yy = H_SEC / 2 - TF / 2
    b.line((0, yy), (BF / 2 + 3.4, yy), C["accent"], 1.4, dash="4 3")     # 翼板形心引線
    b.dim((BF / 2 + 2.6, 0), (BF / 2 + 2.6, yy),
          f"y_f = {YBAR:.2f} cm", off=0, label_off=16)
    b.text_px(b.X(-BF / 2 + B_OUT / 2), b.Y(yy) - 26, "挖除", 12, C["ghost"], weight="700")
    b.math_px(PW2 / 2, PH2 - 84,
              f"ΔI_{{one}} = b t_f^{{3}}/12 + b t_f y_f^{{2}} = {DI_ONE:,.0f} cm^{{4}}（× 4 塊）",
              12.5, C["muted"])
    b.math_px(PW2 / 2, PH2 - 59,
              f"I_e = {IX:,.0f} − {4 * DI_ONE:,.0f} = {IE:,.0f} cm^{{4}}", 13, C["muted"])
    b.math_px(PW2 / 2, PH2 - 34, f"I_e / I_x = {RATIO:.3f}", 16, C["accent"], weight="700")

    compose([a, b],
            title="強軸挫屈：被挖掉的是力臂最長的 4 塊，剛度直接掉一半",
            sub=f"被挖掉的慣性矩以「面積 × 力臂平方」為主項，故強軸只剩 {RATIO:.3f} 倍剛度；"
                f"若改問弱軸，扣除量正比於翼板寬度的三次方，只剩 {RATIO_Y:.3f} 倍",
            note="翼板中央段與腹板為殘餘拉應力，軸壓下永不降伏——有效斷面就是這兩者（含填角）",
            path=f"{OUT}/{TAG}-fig-2-section.svg")
    return f"{OUT}/{TAG}-fig-2-section.svg"


# ══════════════════════════════════════════════════════════
# 圖 3：四段柱強度曲線
# ══════════════════════════════════════════════════════════
def fig3_curve():
    W, Hc = 980, 610
    OX, OY = 100, 92
    LMAX, RMAX = 2.60, 1.10
    KX, KY = 300.0, 400.0          # 每 1 單位 λ／(F_cr/F_y) 對應的像素數

    cv = Canvas(W, Hc, sx=1.0, ox=OX, oy=OY, bg="#FFFFFF")

    def P(lam, r): return (lam * KX, r * KY)

    def path(f, lo, hi, n=240):
        return [P(lo + (hi - lo) * i / n, f(lo + (hi - lo) * i / n)) for i in range(n + 1)]

    cv.text_px(W / 2, 34, "塊狀殘餘應力 ⇒ 強度平台段，不是不連續跳躍",
               17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               "每個分支只在「與自身假設相容」的區間內成立；兩個分支都不成立的區間，"
               "強度被鎖在比例限 0.5F_y", 13, C["muted"])

    # 平台區間網底
    cv.polygon([P(LAM2, 0), P(LAM3, 0), P(LAM3, FP), P(LAM2, FP)], "rgba(180,83,9,0.10)")

    # 座標軸與刻度
    for r in (0.25, 0.50, 0.75, 1.00):
        cv.line(P(0, r), P(LMAX, r), C["border"], 1.0)
        cv.math_px(cv.X(0) - 12, cv.Y(r * KY), f"{r:.2f}", 12, C["muted"], "end")
    for lam in (0.5, 1.0, 1.5, 2.0, 2.5):
        cv.line(P(lam, 0), P(lam, RMAX), C["border"], 1.0)
        cv.math_px(cv.X(lam * KX), cv.Y(0) + 20, f"{lam:.1f}", 12, C["muted"])
    cv.arrow(P(0, 0), P(LMAX, 0), C["muted"], 1.8, 9)
    cv.arrow(P(0, 0), P(0, RMAX), C["muted"], 1.8, 9)
    cv.math_px(cv.X(LMAX * KX) + 6, cv.Y(0) + 22, "λ", 16, C["muted"], "start")
    cv.math_px(cv.X(0) - 10, cv.Y(RMAX * KY) - 6, "F_{cr}/F_y", 15, C["muted"], "end")
    cv.math_px(cv.X(0) - 12, cv.Y(0), "0", 12, C["muted"], "end")

    # 對照曲線
    cv.poly(path(ideal, 0.02, LMAX), C["ghost"], 2.4, dash="7 5")
    cv.poly(path(crc, 0.02, LMAX), C["bmd"], 1.8, dash="3 4")

    # 常見誤畫法：非彈性分支硬拉到 λ = √2，再跳回 0.5
    cv.poly(path(lambda l: RATIO / l ** 2, LAM2, LAM3), C["load"], 2.2, dash="2 4")
    cv.line(P(LAM3, WRONG_AT_LAM3), P(LAM3, FP), C["load"], 2.2, dash="2 4")
    cv.dot(P(LAM3, WRONG_AT_LAM3), 4.6, fill="#FFFFFF", stroke=C["load"], w=2.4)
    cv.text_px(cv.X(LAM3 * KX) + 12, cv.Y(WRONG_AT_LAM3 * KY) + 4,
               "誤畫：不連續跳躍", 13, C["load"], "start", weight="700")
    cv.text_px(cv.X(LAM3 * KX) + 12, cv.Y(WRONG_AT_LAM3 * KY) + 25,
               "λ 變大強度反而變大，違反單調性", 11.5, C["load"], "start")

    # 本題四段曲線
    cv.poly(path(curve, 0.0, LMAX, 600), C["deform"], 4.6)

    # 三個轉折點
    for lam, r, name, dx, dy, anc in ((LAM1, 1.0, "A", 0, -42, "middle"),
                                      (LAM2, FP, "B", -12, 20, "end"),
                                      (LAM3, FP, "C", 13, -34, "start")):
        cv.dot(P(lam, r), 6.0, fill="#FFFFFF", stroke=C["accent"], w=3.0)
        cv.text_px(cv.X(lam * KX) + dx, cv.Y(r * KY) + dy, name, 15, C["accent"],
                   anc, weight="700")
        cv.text_px(cv.X(lam * KX) + dx, cv.Y(r * KY) + dy + 19,
                   f"({lam:.3f}, {r:.3f})", 12.5, C["accent"], anc, weight="700",
                   italic=True, font=None)

    # 分段函數標註
    cv.math_px(cv.X(0.20 * KX), cv.Y(1.0 * KY) - 16, "F_{cr}/F_y = 1.0", 13,
               C["deform"], weight="700")
    cv.math_px(cv.X(0.845 * KX) + 26, cv.Y(0.70 * KY), f"{RATIO:.3f}/λ^{{2}}", 13,
               C["deform"], "start", weight="700")
    cv.math_px(cv.X(0.5 * (LAM2 + LAM3) * KX), cv.Y(FP * KY) + 22, "0.5（平台）", 13,
               C["accent"], weight="700")
    cv.math_px(cv.X(1.95 * KX), cv.Y(1 / 1.95 ** 2 * KY) - 16, "1/λ^{2}", 13,
               C["deform"], "start", weight="700")

    # 圖例
    cv.rect_px(cv.X(1.60 * KX), cv.Y(1.08 * KY), 330, 96, "#FFFFFF", 10, C["border"], 1.2)
    cv.legend(cv.X(1.60 * KX) + 16, cv.Y(1.08 * KY) + 22,
              [(C["deform"], "本題（塊狀殘餘應力，強軸）"),
               (C["ghost"], "圖(a) 理想：無殘餘應力"),
               (C["bmd"], "CRC 拋物線 1 − λ²/4（線性分布）"),
               (C["load"], "常見誤畫：不連續跳躍")], size=12, gap=21)

    cv.text_px(W / 2, Hc - 40,
               f"四段：1.0（λ ≤ {LAM1:.3f}）｜{RATIO:.3f}/λ²（{LAM1:.3f}–{LAM2:.3f}）｜"
               f"0.5（{LAM2:.3f}–{LAM3:.3f}）｜1/λ²（λ ≥ {LAM3:.3f}）",
               13.5, C["text"], weight="700")
    cv.text_px(W / 2, Hc - 18,
               "平台段的存在正是「外側整塊同時降伏」的指紋；線性分布（CRC）則逐步降伏、曲線平滑",
               12, C["muted"])
    cv.save(f"{OUT}/{TAG}-fig-3-column-curve.svg")
    return f"{OUT}/{TAG}-fig-3-column-curve.svg"


# ══════════════════════════════════════════════════════════
FIGURES = [
    (fig2_section, "§1·§4 步驟二",
     "沒看出被挖掉的是力臂最長的 4 塊 → I_e/I_x 算錯、或誤以為中央段也降伏"),
    (fig3_curve,   "§4 步驟三～五·§5.1",
     "把非彈性分支硬拉到 λ=√2 而畫出不連續跳躍（違反強度隨 λ 單調不遞增）"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"ΔI_one = {DI_ONE:,.0f} cm^4　I_e = {IE:,.0f} cm^4　I_e/I_x = {RATIO:.4f}")
    print(f"轉折點 A({LAM1:.3f}, 1.000)　B({LAM2:.3f}, {FP:.3f})　C({LAM3:.3f}, {FP:.3f})")
    print(f"誤畫法在 λ=√2 的值 = {WRONG_AT_LAM3:.3f}（低於同點正解 {FP}）")
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<44} {section:<16} 攔：{catches}")
