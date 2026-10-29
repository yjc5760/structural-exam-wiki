#!/usr/bin/env python3
"""
SS-2013-2 含靠桿（leaning column）之側移剛架 — 解題圖解產生腳本

用法：
    python3 gen_SS-2013-2.py [輸出目錄]

三條鐵則的落實：
  1. 圖上每個數字都標明來自 SS-2013-2.md 哪一節
  2. 側移模態的轉角由 §1 給定的 I_c、I_b 以傾角變位法算出（TH_B_CW），
     不是描摹；改 I_c/I_b 的比值，AB 的彎曲程度會自動跟著變
  3. 每張圖在 FIGURES 表寫明攔什麼錯
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose, column_shape, beam_shape
from recipes import bar_compare

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2013-2"

# ══════════════════════════════════════════════════════════
# 解題結果（全部來自 SS-2013-2.md，勿手動改動）
# ══════════════════════════════════════════════════════════
# §1 題目給定
E    = 2040.0           # tf/cm^2
L    = 600.0            # cm（梁跨度 ＝ 柱高）
I_C  = 30094.0          # cm^4（柱 AB、CD）
I_B  = 136108.0         # cm^4（梁 BC）
RHO  = 240.0            # tf/m^2
# §4二 G 值
G_A  = 10.0             # A 為鉸接，題目規定取 10
G_B  = I_C / I_B        # 0.221
# §4三 對位圖（側位移不束制）
K_AB = 1.71
# §4四 尤拉載重與挫屈載重
P_E    = 1683.0         # tf（K = 1）
P_EK_AB = 575.6         # tf（= P_e / K_AB^2）
SUM_PEK = P_EK_AB       # 靠桿 CD 不計入
# §4五 靜力
SUMP_OVER_PI = 2.0      # ΣP / P_I = wL / (wL/2)
# §4六～八 答案
K_PRIME = 2.42
P_CR    = 287.9         # tf
W_CR    = 96.0          # tf/m
D_ALLOW = 0.40          # m
# §5.1 兩種誤解法的量級
W_ERR1  = 192.0         # tf/m　CD 誤當一般柱（A 仍為鉸）
D_ERR1  = 0.80          # m
W_ERR2  = 287.0         # tf/m　再加上 A 誤判為固接
# §5.5 梁遠端鉸接之勁度折減（進階，非考場必要）
W_ADV   = 89.3          # tf/m
D_ADV   = 0.37          # m

# ── 側移模態的轉角：由傾角變位法解出，不是描摹 ──
# 側移 Δ 時令弦線轉角 ψ = Δ/L（順時針為正）：
#   桿 AB（A 端鉸接之修正勁度）：M_BA = (3EI_c/L)(θ_B − ψ)
#   梁 BC（C 端鉸接之修正勁度）：M_BC = (3EI_b/L)(θ_B)
#   節點 B 平衡 M_BA + M_BC = 0  ⇒  θ_B = ψ · I_c/(I_c + I_b)
TH_B_CW = I_C / (I_C + I_B)             # = 0.1811 ψ
TH_A_CW = (3 - TH_B_CW) / 2             # 由 M_AB = 0 得 θ_A = (3ψ − θ_B)/2
TH_C_CW = -TH_B_CW / 2                  # 由 M_CB = 0（C 為鉸）得 θ_C = −θ_B/2

D_DRAW = 0.22           # 繪圖用側移量（純視覺，不影響任何物理量）
MW     = 6.4            # 構材線寬


# ══════════════════════════════════════════════════════════
def _hinge(cv, p, r=4.9):
    """鉸接節點：白心圓圈"""
    cv.dot(p, r, fill="#FFFFFF", stroke=C["member"], w=2.6)


def frame_undeformed(cv, color=C["member"], w=MW, dash=None):
    for s, e in (((0, 0), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (1, 0))):
        cv.line(s, e, color, w, dash=dash, cap="butt")


def sway_shapes(cv, D=D_DRAW, col_ab=None, col_cd=None, beam=None, w=MW,
                cd_straight=True):
    """側移模態。cd_straight=True 時柱 CD 畫成直線（二力構件、零彎矩）"""
    col_ab = col_ab or C["deform"]
    col_cd = col_cd or (C["accent"] if cd_straight else C["deform"])
    beam = beam or C["deform"]
    cv.poly(column_shape((0, 0), 1.0, D, -TH_B_CW * D, 0.0, -TH_A_CW * D), col_ab, w)
    cv.poly(beam_shape((D, 1), 1.0, -TH_B_CW * D, -TH_C_CW * D), beam, w)
    if cd_straight:
        cv.line((1, 0), (1 + D, 1), col_cd, w, cap="butt")
    else:   # 誤解法：把 CD 當成與 AB 相同的一般柱（同樣彎曲）
        cv.poly(column_shape((1, 0), 1.0, D, -TH_B_CW * D, 0.0, -TH_A_CW * D), col_cd, w)


# ══════════════════════════════════════════════════════════
def fig2_leaning_column():
    """題目重繪 ＋ 側移模態：靠桿在圖上長什麼樣子"""
    PW, PH = 540, 520
    SX, OX, OY = 250, 150, 150

    # ── 左：題目重繪 ──
    a = Canvas(PW, PH, sx=SX, ox=OX, oy=OY)
    a.panel("圖 2 重繪：邊界條件", "A、D 鉸支承｜B 剛接｜C 鉸接（小圓圈）")
    frame_undeformed(a)
    a.udl((0, 1), (1, 1), 0.09, n=9, label="w")
    a.pin_support((0, 0), size=15)
    a.pin_support((1, 0), size=15)
    a.dot((0, 1), 5.4, fill=C["member"])          # B：剛接（實心）
    _hinge(a, (1, 1))                             # C：鉸接（空心圓圈）
    for p, lab, dx, dy in (((0, 0), "A", -24, -10), ((0, 1), "B", -22, -16),
                           ((1, 1), "C", 22, -16), ((1, 0), "D", 24, -10)):
        a.text(p, lab, 16, C["text"], weight="700", dx=dx, dy=dy)
    a.math_px(a.X(0) + 16, a.Y(0.11), f"G_A = {G_A:.0f}", 13, C["bmd"], "start", weight="700")
    a.math_px(a.X(0) - 30, a.Y(1) + 26, f"G_B = I_c/I_b = {G_B:.3f}", 13, C["bmd"],
              "end", weight="700")
    a.math_px(a.X(0.5), a.Y(1) + 24, f"I_b = 136,108 cm^{{4}}", 13, C["muted"])
    a.math_px(a.X(0) - 30, a.Y(0.52), f"I_c = 30,094 cm^{{4}}", 13, C["muted"], "end")
    a.text_px(a.X(1) + 30, a.Y(0.52) - 10, "靠桿", 15, C["accent"], "start", weight="700")
    a.text_px(a.X(1) + 30, a.Y(0.52) + 11, "leaning", 11.5, C["accent"], "start")
    a.dim((0, 0), (1, 0), f"L = {L:.0f} cm", off=48, label_off=15)
    a.dim((1, 0), (1, 1), f"L = {L:.0f} cm", off=-56, label_off=-15)
    a.text_px(PW / 2, PH - 58, "C 點有小圓圈 → 梁不拘束 CD 頂端轉動", 13, C["muted"])
    a.text_px(PW / 2, PH - 33, "⇒ 柱 CD 兩端皆鉸 ＝ 靠桿：能承重、零側向勁度",
              13.5, C["accent"], weight="700")

    # ── 右：側移挫屈模態 ──
    b = Canvas(PW, PH, sx=SX, ox=OX, oy=OY)
    b.panel("側移挫屈模態", "AB 彎曲抵抗｜CD 保持直線、只隨側移傾斜")
    frame_undeformed(b, C["ghost"], 2.8, dash="6 5")
    b.line((0, 0), (D_DRAW, 1), C["ghost"], 1.6, dash="3 4")      # AB 的弦線
    sway_shapes(b)
    b.pin_support((0, 0), size=15)
    b.pin_support((1, 0), size=15)
    b.dot((D_DRAW, 1), 5.4, fill=C["deform"])
    _hinge(b, (1 + D_DRAW, 1))
    b.arrow((1 + D_DRAW, 1.10), (1 + D_DRAW + 0.15, 1.10), C["deform"], 3.2, 11)
    b.math_px(b.X(1 + D_DRAW + 0.15) + 9, b.Y(1.10), "Δ", 17, C["deform"], "start", weight="700")
    b.text_px(b.X(D_DRAW * 0.62) - 12, b.Y(0.46), "彎曲", 13, C["deform"], "end", weight="700")
    b.text_px(b.X(1 + D_DRAW * 0.5) + 16, b.Y(0.46) - 10, "直線", 13, C["accent"],
              "start", weight="700")
    b.math_px(b.X(1 + D_DRAW * 0.5) + 16, b.Y(0.46) + 11, "M = 0", 12.5, C["accent"], "start")
    b.math_px(b.X(0) - 26, b.Y(0.09), "M_{A} = 0", 12.5, C["bmd"], "end", weight="700")
    b.text_px(PW / 2, PH - 58,
              "ΣP ＝ P_{AB} + P_{CD} ＝ wL　（載重：兩根都算）", 13, C["muted"])
    b.text_px(PW / 2, PH - 33,
              f"ΣP_{{eK}} ＝ P_{{eK,AB}} ＝ {SUM_PEK} tf　（容量：只有 AB）",
              13.5, C["accent"], weight="700")

    compose([a, b],
            title="靠桿（leaning column）：送重量、不送勁度",
            sub="CD 兩端皆鉸 ⇒ 二力構件 ⇒ 挫屈時全程保持直線，整層側向抵抗只剩柱 AB",
            note=f"這個不對稱正是萊梅厥公式的靈魂：對位圖的 {K_AB} 要再乘 √2 "
                 f"（AB 自己一份重量 ＋ 靠桿塞來的一份），得 K′ = {K_PRIME}",
            path=f"{OUT}/{TAG}-fig-2-leaning-column.svg")
    return f"{OUT}/{TAG}-fig-2-leaning-column.svg"


# ══════════════════════════════════════════════════════════
def fig3_magnitude():
    """量級比較：靠桿判錯會讓挫屈載重高估 2～3 倍"""
    def sketch(mini, i):
        straight = i >= 2
        mini.line((0, 0), (0, 1), C["ghost"], 1.8, dash="4 4", cap="butt")
        mini.line((0, 1), (1, 1), C["ghost"], 1.8, dash="4 4", cap="butt")
        mini.line((1, 1), (1, 0), C["ghost"], 1.8, dash="4 4", cap="butt")
        col = (C["load"], C["load"], C["accent"], C["muted"])[i]
        sway_shapes(mini, D=0.26, col_ab=col, col_cd=col, beam=col, w=3.0,
                    cd_straight=straight)

    bar_compare(
        [("誤判 ②：CD＋A 都判錯", "ΣP_{eK} 多一根、K 又低估",
          W_ERR2, f"w_{{cr}} = {W_ERR2:.0f} tf/m", C["load"]),
         ("誤判 ①：CD 視為一般柱", "ΣP_{eK} 誤含 CD",
          W_ERR1, f"w_{{cr}} = {W_ERR1:.0f} tf/m, d = {D_ERR1:.2f} m", C["load"]),
         ("正解：CD 為靠桿", "ΣP_{eK} 只計 AB",
          W_CR, f"w_{{cr}} = {W_CR:.1f} tf/m, d = {D_ALLOW:.2f} m", C["accent"]),
         ("§5.5 梁遠端鉸接折減", "梁勁度乘 0.5（進階）",
          W_ADV, f"w_{{cr}} = {W_ADV:.1f} tf/m, d = {D_ADV:.2f} m", C["muted"])],
        title="靠桿判錯的代價：挫屈載重高估 2～3 倍",
        sub=f"左側示意圖的差別只有一處——柱 CD 到底彎不彎；"
            f"誤解法讓 ΣP_{{eK}} 由 {SUM_PEK} tf 變成 {2 * SUM_PEK:.1f} tf",
        note=f"正解 w_{{cr}} = {W_CR} tf/m ⇒ d = {D_ALLOW} m；"
             f"§5.5 之梁遠端鉸接折減再降約 7%，方向偏保守",
        sketch=sketch, W=1180,
        path=f"{OUT}/{TAG}-fig-3-magnitude.svg")
    return f"{OUT}/{TAG}-fig-3-magnitude.svg"


# ══════════════════════════════════════════════════════════
FIGURES = [
    (fig2_leaning_column, "§1·§4一·§4五",
     "把 CD 讀成「底端鉸接的一般柱」→ ΣP_eK 多算一根"),
    (fig3_magnitude,      "§5.1",
     "答案量級錯（w_cr 落在 190～290 而非 96）卻沒察覺"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"側移模態轉角（傾角變位法，順時針正，以 ψ 為單位）："
          f"θ_A = {TH_A_CW:.4f}　θ_B = {TH_B_CW:.4f}　θ_C = {TH_C_CW:.4f}")
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<44} {section:<14} 攔：{catches}")
