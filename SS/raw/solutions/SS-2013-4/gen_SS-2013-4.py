#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2013-4 圖解產生腳本（無側撐剛架之二階設計彎矩）

所有幾何與數值皆由下方常數區與其推導式決定，改一個輸入重跑即改變圖形。
執行：python3 gen_SS-2013-4.py   →   figs/*.svg
"""
import sys, os, math
# struct-diagram 的 primitives 取自本知識庫自帶的 skill 副本（repo 相對路徑，故可原地重跑）；
# 若把本檔搬到別處，設環境變數 SD_SKILL 指向 struct-diagram 目錄即可。
_HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.environ.get("SD_SKILL",
                       os.path.normpath(os.path.join(_HERE, "..", "..", "..",
                                                     "skills", "struct-diagram")))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
from structdraw import Canvas, C, compose, column_shape, beam_shape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")

# ══════════════════════════════════════════════════════════════
# 由 SS-2013-4 §1 / §4 解得（每個數字都標明出處章節）
# ══════════════════════════════════════════════════════════════
LC       = 1.0            # 柱 BC 長度 L（繪圖單位）            §1 幾何
LB       = 1.5 * LC       # AB = BD = 1.5L                      §1 幾何
G_B      = (1/LC) / (2/LB)          # = 0.75  柱頂 G（分母含兩段梁）§4 二
G_C      = 10.0                     # 鉸接，原卷約定               §4 二
K_APPROX = math.sqrt((1.6*G_B*G_C + 4*(G_B+G_C) + 7.5) / (G_B+G_C+7.5))  # 1.851  §4 三
SUM_PEK  = math.pi**2 / K_APPROX**2     # = 2.88（單位 EI/L^2）    §4 四
PE1      = math.pi**2                   # = 9.87（無側移 K=1）      §4 七
SUM_PEK_AISC = 0.85 * 12/7              # = 1.457（R_M × 12EI/7L^2） §6.2

# 一階側移狀態的變形（由斜率-偏移法推得，見 §6.2）：
#   梁遠端為滾支承 ⇒ 每段梁在 B 之轉動勁度 3EI/(1.5L)=2EI/L，兩段共 4EI/L
#   柱遠端鉸接     ⇒ M_BC = (3EI/L)(θ_B − ψ)
#   節點平衡       ⇒ 7θ_B = 3ψ
PSI     = 0.30            # 繪圖用層間傾角 Δ/L（示意放大，不影響比例關係）
DELTA   = PSI * LC        # 柱頂側移
TH_B_CW = (3/7) * PSI                  # 柱頂轉角（順時針正）
TH_C_CW = (3*PSI - TH_B_CW) / 2        # 柱底鉸接：M_CB=0 ⇒ θ_C=(3ψ−θ_B)/2 = (9/7)ψ
TH_A_CW = -TH_B_CW / 2                 # 梁遠端鉸接：M_AB=0 ⇒ θ_A = −θ_B/2
# structdraw 的 column_shape/beam_shape 一律吃「整體逆時針正」，故取負號
TH_B, TH_C, TH_A = -TH_B_CW, -TH_C_CW, -TH_A_CW

MLT     = 1.0             # M_lt / (H·L) —— 層剪力全部由 BC 承擔  §4 五
MNT     = 0.0             # §4 五（P 與柱同軸 + 跨度對稱 ⇒ θ_B=0）


# ══════════════════════════════════════════════════════════════
def fig1_frame():
    """圖 1：題目重繪（向量版）"""
    W, H = 800, 470
    L, R, T, B = 60, 60, 116, 92
    XL, XR = -0.78, 2*LB + 0.28          # 需涵蓋 H 箭頭尾端與右側標註
    sx = min((W-L-R) / (XR-XL), (H-T-B) / (LC*1.0))
    cv = Canvas(W, H, sx=sx, ox=L - XL*sx, oy=B, bg="#FFFFFF")

    A, Bp, D, Cp = (0, LC), (LB, LC), (2*LB, LC), (LB, 0)

    # 梁 A—B—D 與柱 B—C
    cv.line(A, D, C["member"], 6.5, cap="butt")
    cv.line(Bp, Cp, C["member"], 6.5, cap="butt")

    # 支承：A、D 滾支承（水平自由）；C 鉸支承（水平束制）
    cv.roller_support(A, 0, 15)
    cv.roller_support(D, 0, 15)
    cv.pin_support(Cp, 0, 15)

    # 剛性節點 B
    cv.dot(Bp, 6.2, fill=C["member"])
    s = 0.10
    cv.polygon([(LB-s, LC), (LB, LC-s), (LB+s, LC)], C["fill_m"], C["bmd"], 1.6)

    # 外力：H 於 A（向右）、P 於 B（向下）
    cv.arrow((-0.62, LC), (-0.10, LC), C["load"], 3.6, 12)
    cv.math_px(cv.X(-0.36), cv.Y(LC) - 16, "H", 18, C["load"], weight="700")
    cv.arrow((LB, LC + 0.60), (LB, LC + 0.06), C["load"], 3.6, 12)
    cv.math_px(cv.X(LB) + 15, cv.Y(LC + 0.42), "P", 18, C["load"], "start", weight="700")

    # 節點名稱
    for p, nm, dx, dy in ((A, "A", -6, -20), (Bp, "B", 20, -18),
                          (D, "D", 8, -20), (Cp, "C", 20, 6)):
        cv.text_px(cv.X(p[0]) + dx, cv.Y(p[1]) + dy, nm, 17, C["text"], weight="700")

    # 尺寸
    cv.dim(A, Bp, "1.5L", off=-38, label_off=-14)
    cv.dim(Bp, D, "1.5L", off=-38, label_off=-14)
    cv.dim(Cp, Bp, "L", off=-40, label_off=-13)
    cv.math_px(cv.X(LB*0.5), cv.Y(LC) + 22, "EI", 15, C["muted"], weight="700")
    cv.math_px(cv.X(LB*1.5), cv.Y(LC) + 22, "EI", 15, C["muted"], weight="700")
    cv.math_px(cv.X(LB) + 26, cv.Y(LC*0.5), "EI", 15, C["muted"], "start", weight="700")

    # 標註：本題最易誤讀處
    cv.text_px(cv.X(0) - 4, cv.Y(LC) + 66, "滾支承：水平自由", 13, C["accent"], "middle", weight="700")
    cv.text_px(cv.X(2*LB) + 4, cv.Y(LC) + 66, "滾支承：水平自由", 13, C["accent"], "middle", weight="700")
    cv.text_px(cv.X(LB), cv.Y(0) + 62, "鉸支承：唯一水平束制", 13, C["accent"], weight="700")

    cv.text_px(W/2, 34, "圖 1　題目幾何重繪（原卷圖 4）", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58, "全結構只有一根柱：BC。A、D 是梁兩端的滾支承，不是柱頂節點",
               13, C["muted"])
    cv.text_px(W/2, 84, f"抗側力構材僅 BC ⇒ 側移未受束制（無側撐剛架），K > 1",
               13, C["bmd"])
    cv.save(os.path.join(OUT, "SS-2013-4-fig-1-frame.svg"))


# ══════════════════════════════════════════════════════════════
def _frame_ghost(cv):
    cv.line((0, LC), (2*LB, LC), C["ghost"], 3.0, dash="7 5")
    cv.line((LB, LC), (LB, 0), C["ghost"], 3.0, dash="7 5")


def fig2_nt_lt():
    """圖 2：M_nt / M_lt 分解 + 柱 BC 之 M_lt 彎矩圖（三聯）"""
    PW, PH = 470, 430
    Lm, Rm, Tm, Bm = 62, 62, 108, 74
    sx = min((PW-Lm-Rm) / (2*LB), (PH-Tm-Bm) / (LC*1.28))

    # ── 格 1：無側移狀態（M_nt） ──
    p1 = Canvas(PW, PH, sx=sx, ox=Lm, oy=Bm)
    p1.panel("① 無側移狀態 → M_{nt}", "加虛擬水平支撐，只施重力 P")
    _frame_ghost(p1)
    p1.line((0, LC), (2*LB, LC), C["member"], 5.2, cap="butt")
    p1.line((LB, LC), (LB, 0), C["member"], 5.2, cap="butt")
    p1.roller_support((0, LC), 0, 12); p1.roller_support((2*LB, LC), 0, 12)
    p1.pin_support((LB, 0), 0, 12)
    p1.arrow((LB, LC+0.52), (LB, LC+0.05), C["load"], 3.2, 11)
    p1.math_px(p1.X(LB) + 14, p1.Y(LC+0.36), "P", 16, C["load"], "start", weight="700")
    # 虛擬水平支撐
    p1.line((LB, LC), (2*LB + 0.34, LC), C["deform"], 2.6, dash="6 4")
    p1.polygon([(2*LB+0.34, LC-0.09), (2*LB+0.34, LC+0.09),
                (2*LB+0.46, LC+0.09), (2*LB+0.46, LC-0.09)], C["fill_c"], C["deform"], 1.6)
    p1.text_px(p1.X(2*LB) + 6, p1.Y(LC) - 26, "虛擬支撐", 12, C["deform"], weight="700")
    # 對稱標記
    p1.dim((0, LC), (LB, LC), "1.5L", off=-30, label_off=-12)
    p1.dim((LB, LC), (2*LB, LC), "1.5L", off=-30, label_off=-12)
    p1.dot((LB, LC), 5.6, fill=C["bmd"])
    p1.math_px(p1.X(LB) - 22, p1.Y(LC) + 30, "θ_{B} = 0", 15, C["bmd"], "end", weight="700")
    p1.math_px(PW/2, PH - 40, f"M_{{nt}} = {MNT:g}", 18, C["bmd"], weight="700")

    # ── 格 2：側移狀態（M_lt） ──
    p2 = Canvas(PW, PH, sx=sx, ox=Lm, oy=Bm)
    p2.panel("② 側移狀態 → M_{lt}", "移除支撐，只施水平力 H")
    _frame_ghost(p2)
    # 柱：底鉸接 θ_C、頂 θ_B（由節點平衡解出）
    p2.poly(column_shape((LB, 0), LC, DELTA, TH_B, 0.0, TH_C), C["deform"], 5.2)
    # 梁：兩端隨側移平移 Δ，端點轉角 θ_A（遠端鉸接）與 θ_B
    p2.poly(beam_shape((0+DELTA, LC), LB, TH_A, TH_B), C["deform"], 5.2)
    # 右段 BD 的遠端 D 亦為滾支承（M=0）⇒ θ_D = −θ_B/2，與 θ_A 同值
    p2.poly(beam_shape((LB+DELTA, LC), LB, TH_B, TH_A), C["deform"], 5.2)
    p2.roller_support((0, LC), 0, 12); p2.roller_support((2*LB, LC), 0, 12)
    p2.pin_support((LB, 0), 0, 12)
    p2.arrow((0+DELTA-0.55, LC), (0+DELTA-0.06, LC), C["load"], 3.4, 11)
    p2.math_px(p2.X(DELTA-0.30), p2.Y(LC) - 16, "H", 16, C["load"], weight="700")
    p2.dim((LB, LC), (LB+DELTA, LC), "Δ", off=-26, label_off=-12, color=C["deform"])
    p2.math_px(p2.X(LB) + 30, p2.Y(LC*0.60), "V_{BC} = H", 14.5, C["load"], "start", weight="700")
    p2.math_px(PW/2, PH - 40, "M_{lt} = H·L", 18, C["bmd"], weight="700")

    # ── 格 3：柱 BC 之 M_lt 彎矩圖 ──
    p3 = Canvas(PW, PH, sx=sx, ox=Lm + (PW-Lm-Rm)*0.42, oy=Bm)
    p3.panel("③ 柱 BC 之 M_{lt} 彎矩圖", "繪於受拉側；由 B 端 HL 線性降至 C 端 0")
    p3.line((0, 0), (0, LC), C["member"], 5.2, cap="butt")
    p3.pin_support((0, 0), 0, 12)
    wmax = 0.62 * MLT
    p3.polygon([(0, 0), (0, LC), (-wmax, LC)], C["fill_m"], C["bmd"], 2.4)
    p3.math_px(p3.X(-wmax) + 4, p3.Y(LC) - 22, "M_{lt} = HL", 15, C["bmd"], "middle", weight="700")
    p3.math_px(p3.X(0) - 14, p3.Y(0) - 4, "0", 15, C["bmd"], "end", weight="700")
    p3.text_px(p3.X(0) + 16, p3.Y(LC) + 8, "B", 15, C["text"], "start", weight="700")
    p3.text_px(p3.X(0) + 16, p3.Y(0) - 20, "C", 15, C["text"], "start", weight="700")
    p3.text_px(PW/2, PH - 40, "柱底鉸接 ⇒ 彎矩必為 0，無反曲點", 13, C["muted"])

    compose([p1, p2, p3], cols=3,
            title="圖 2　Mnt 與 Mlt 之分離（B1-B2 放大法的前置一階分析）",
            sub="Mu = B1·Mnt + B2·Mlt；本題 Mnt = 0，故答案完全由 B2 控制",
            note="A、D 為滾支承，水平反力為零 ⇒ 層剪力全部由 BC 承擔，Mlt = H·L（不是 HL/3）；側移量為示意放大",
            path=os.path.join(OUT, "SS-2013-4-fig-2-nt-lt.svg"))


# ══════════════════════════════════════════════════════════════
def fig3_b2():
    """圖 3：B_2 隨軸壓力之放大曲線（含 AISC 側移法對照）"""
    W, H = 900, 520
    Lm, Rm, Tm, Bm = 88, 268, 104, 76
    XMAX, YMAX = 3.4, 4.6
    sx = min((W-Lm-Rm) / XMAX, (H-Tm-Bm) / YMAX)
    cv = Canvas(W, H, sx=sx, ox=Lm, oy=Bm, bg="#FFFFFF")

    def curve(pek, color, n=400, cap=YMAX):
        pts = []
        for i in range(n+1):
            p = XMAX * i / n
            if p >= pek * (1 - 1/cap):
                break
            pts.append((p, 1.0 / (1 - p/pek)))
        return pts

    # 座標軸
    cv.arrow((0, 0), (XMAX, 0), C["muted"], 1.8, 9)
    cv.arrow((0, 0), (0, YMAX), C["muted"], 1.8, 9)
    cv.math((XMAX, 0), "P L^{2}/EI", 14.5, C["muted"], "start", dx=6, dy=16)
    cv.math((0, YMAX), "B_{2}", 15, C["muted"], "end", dx=-10)
    for v in (1, 2, 3, 4):
        cv.line((0, v), (XMAX, v), C["border"], 1.0)
        cv.text_px(cv.X(0) - 10, cv.Y(v), f"{v}", 12, C["muted"], "end")
    for v in (1, 2, 3):
        cv.text_px(cv.X(v), cv.Y(0) + 18, f"{v}", 12, C["muted"])
    cv.line((0, 1), (XMAX, 1), C["muted"], 1.6, dash="5 4")

    # 兩條曲線 + 漸近線
    for pek, color in ((SUM_PEK, C["bmd"]), (SUM_PEK_AISC, C["accent"])):
        cv.poly(curve(pek, color), color, 3.2)
        cv.line((pek, 0), (pek, YMAX), color, 1.6, dash="6 4")
        cv.math_px(cv.X(pek) + 6, cv.Y(YMAX) + 12, f"{pek:.2f}", 13, color, "start", weight="700")

    # 實務放大上限 B2 ≤ 1.5
    p_at = SUM_PEK * (1 - 1/1.5)
    cv.dot((p_at, 1.5), 5.4, fill=C["deform"])
    cv.math_px(cv.X(p_at) - 12, cv.Y(1.5) - 16, "B_{2} = 1.5", 13, C["deform"], "end", weight="700")

    cv.legend(W - Rm + 6, 152,
              [(C["bmd"], "台灣 2010（K = 1.85）"), (C["accent"], "AISC 360-16 側移法"),
               (C["muted"], "一階值（無放大）")], size=12)
    cv.math_px(W - Rm + 6, 220, f"ΣP_{{eK}} = {SUM_PEK:.2f} EI/L^{{2}}", 12.5, C["bmd"], "start", weight="700")
    cv.math_px(W - Rm + 6, 244, f"ΣP_{{e,story}} = {SUM_PEK_AISC:.2f} EI/L^{{2}}", 12.5, C["accent"], "start", weight="700")

    cv.text_px(W/2, 34, "圖 3　側移放大係數 B_2 的漸近行為", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58, "B_2 = 1/(1 − ΣP_u/ΣP_eK)；橫軸為無因次軸壓 PL²/EI", 13, C["muted"])
    cv.text_px(W/2, 82,
               "曲線的垂直漸近線就是該層的側移挫屈載重；ΣP_eK 若誤加三根柱（7.72）會把漸近線右推 2.7 倍",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               f"P 趨近 {SUM_PEK:.2f} EI/L² 時 B_2 發散（層間側移挫屈）；適用範圍要求 ΣP_u 小於 ΣP_eK",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2013-4-fig-3-b2-curve.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1_frame(); fig2_nt_lt(); fig3_b2()
    print(f"G_B={G_B:.3f}  K={K_APPROX:.3f}  SumPeK={SUM_PEK:.3f}  Pe1={PE1:.2f}")
    print(f"theta_B(cw)={TH_B_CW:.4f}  theta_C(cw)={TH_C_CW:.4f}  theta_A(cw)={TH_A_CW:.4f}")
    print("done ->", OUT)
