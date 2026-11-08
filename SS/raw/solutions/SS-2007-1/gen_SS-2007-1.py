#!/usr/bin/env python3
"""
SS-2007-1 角鋼平衡填角焊設計（ASD）— 題目附圖重繪腳本

用法：
    python3 gen_SS-2007-1.py [輸出目錄]

重繪依據：題目正本 SS-2007-1-problem.md §4 判讀清單（待確認）。
只畫考卷圖一所示：L150×100×15 的 150 mm 肢平貼 15 mm 連接板，三段填角焊（上緣 a、下緣 b、端部 15 cm），
P 作用線距上緣 10 cm。考卷為斜向透視圖，本圖改為正視平面圖（角鋼水平放置）。
肢寬 15 cm、肢背稜線（另一肢厚 1.5 cm）、10 cm 依比例；焊道長 a、b 為所求，長度只示意，不代表答案；
連接板外形與角鋼伸出長度為示意。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2007-1"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2007-1-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
BL = 15.0           # #1 150 mm 肢平貼連接板（端部橫向焊標 15 cm）
T = 1.5             # 題文 角鋼厚 15 mm（#3 下緣平行線＝另一肢稜線 → b 側為肢背）
EP = 10.0           # #4 由上緣（a 側、趾）量到 P 作用線 10 cm
W = 1.2             # 題文 腳長 1.2 cm（斜線區寬）
#                     #2 三段焊：上緣縱向 a、下緣縱向 b、端部橫向 15 cm
# 示意（所求或考卷未標）：
A_SK, B_SK = 20.0, 34.0     # a、b 長度示意（為所求）
L_ANG = 72.0                # 角鋼畫出長度

PW, PHT = 1000, 560


def _hatched(cv, x0, x1, y0, y1, step=0.75):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], C["fill_t"], C["load"], 1.2)
    xa, xb, ya, yb = min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)
    h = yb - ya
    k = xa - h
    while k < xb:
        p0 = (max(k, xa), ya + max(0, xa - k))
        p1 = (min(k + h, xb), ya + min(h, xb - k))
        if p1[0] > p0[0]:
            cv.line(p0, p1, C["load"], 1.0)
        k += step


def panel():
    sx = 8.0
    cv = Canvas(PW, PHT, sx=sx, ox=215, oy=230)
    cv.panel("角鋼與連接板（平面）", "L 150×100×15，Unit = mm；150 mm 肢平貼連接板")
    # 連接板（不規則外形，示意）
    plate = [(-20, 22), (42, 22), (44, -6), (40, -19), (10, -21), (-14, -19), (-21, -8), (-19, 6)]
    cv.polygon(plate, "rgba(63,74,90,0.08)", C["member"], 1.6)
    cv.text((10, -13), "15 mm-plate", 17, C["text"])
    # 角鋼（150 肢平貼；下緣為肢背，另一肢厚 1.5 cm 的稜線）
    cv.polygon([(0, 0), (L_ANG, 0), (L_ANG, BL), (0, BL)], C["fill_c"], C["member"], 2.2)
    cv.line((0, T), (L_ANG, T), C["member"], 1.4)
    # 焊道（斜線區）
    _hatched(cv, 0, A_SK, BL, BL + W)
    _hatched(cv, 0, B_SK, -W, 0)
    _hatched(cv, -W, 0, -W, BL + W)
    # a、b、15 cm
    cv.dim((0, BL + W), (A_SK, BL + W), "a", off=-26, label_off=-14, size=18)
    cv.dim((0, -W), (B_SK, -W), "b", off=26, label_off=16, size=18)
    cv.dim((-W, 0), (-W, BL), f"{BL:.0f} cm", off=-30, label_off=-36)
    # P 與 10 cm
    yp = BL - EP
    cv.line((L_ANG - 6, yp), (L_ANG, yp), C["load"], 1.0, dash="4 3")
    cv.arrow((L_ANG, yp), (L_ANG + 10, yp), C["load"], 3.2, 12)
    cv.math((L_ANG + 10, yp), "P", 18, C["load"], "start", dx=8, weight="700")
    xd = L_ANG + 4
    cv.line((L_ANG, BL), (xd + 0.6, BL), C["dim"], 1, dash="3 3")
    cv.dim((xd, BL), (xd, yp), f"{EP:.0f} cm", label_off=-30)
    # 標註
    cv.line((L_ANG * 0.55, BL), (L_ANG * 0.55 + 4, BL + 9), C["muted"], 1.1)
    cv.text((L_ANG * 0.55 + 4, BL + 9), "L 150×100×15", 16, C["text"], "start", dx=4)
    cv.line((L_ANG * 0.75, T / 2), (L_ANG * 0.75 + 3, -7), C["muted"], 1.1)
    cv.text((L_ANG * 0.75 + 3, -7), "肢背（另一肢稜線）", 13, C["muted"], "start", dx=4)
    cv.text_px(PW - 24, PHT - 34, "斜線區＝填角焊（腳長 1.2 cm）", 12.5, C["load"], "end")
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([panel()], cols=1,
            title="SS-2007-1 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#4；由斜向透視改為平面正視，a、b 長度為所求（示意）",
            note="10 cm 由趾側（a 側上緣）量到 P，P 距肢背（b 側）只有 5 cm；端部橫向焊 15 cm 也是焊道",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2007-1.md §4，由下式即時算出
# 座標：x 沿角鋼長向（由端部橫向銲起算，cm）；y 跨 150 mm 肢，b（肢背）在 y = 0、a（趾）在 y = 15
# ══════════════════════════════════════════════════════════════
import math
Q_FY, Q_FU, Q_U = 3.5, 4.8, 0.85                       # t/cm²、U              §1
Q_AG = (15 + 10 - T) * T                               # 35.25 cm²             Step 1
Q_AE = Q_U * Q_AG
Q_PY, Q_PU = 0.6 * Q_FY * Q_AG, 0.5 * Q_FU * Q_AE      # 74.0、71.9
Q_P = min(Q_PY, Q_PU)
Q_Q = 0.3 * 4.9 * 0.707 * W                            # 1.247 t/cm            Step 2
Q_F3 = Q_Q * BL                                        # 端部橫向銲 18.71       Step 3
Q_YP = BL - EP                                         # P 作用線距 b 側 5 cm
Q_FB = (Q_P * EP - Q_F3 * BL / 2) / BL                 # 對 a 線取矩            Step 4
Q_FA = Q_P - Q_F3 - Q_FB
Q_LA, Q_LB = Q_FA / Q_Q, Q_FB / Q_Q                    # 11.7、30.9
Q_LA_U, Q_LB_U = math.ceil(Q_LA), math.ceil(Q_LB)       # 12、31
Q_EQ = (Q_P - Q_F3) / 2 / Q_Q                          # 誤：兩側平分


def fig1_balance():
    W1, H1 = 1000, 520
    sx = 15.0
    cv = Canvas(W1, H1, sx=sx, ox=235, oy=170)
    cv.panel("角鋼 150 mm 肢平貼連接板（平面，依比例）", "紅＝銲道；箭頭＝銲道對角鋼的抵抗力與外力 P")
    Lx = 34.0
    cv.polygon([(0, 0), (Lx, 0), (Lx, BL), (0, BL)], "rgba(63,74,90,0.10)", C["member"], 1.6)
    cv.line((0, BL), (Q_LA_U, BL), C["load"], 6, cap="butt")
    cv.line((0, 0), (Q_LB_U, 0), C["load"], 6, cap="butt")
    cv.line((0, 0), (0, BL), C["load"], 6, cap="butt")
    cv.text_px(cv.X(Q_LA_U / 2), cv.Y(BL) - 14, f"a = {Q_LA_U} cm", 13, C["load"], weight="700")
    cv.text_px(cv.X(Q_LB_U / 2), cv.Y(0) + 22, f"b = {Q_LB_U} cm", 13, C["load"], weight="700")
    cv.text_px(cv.X(Lx) + 72, cv.Y(BL) + 4, "a 側（趾）", 12, C["muted"], "start")
    cv.text_px(cv.X(Lx) + 72, cv.Y(0) + 4, "b 側（肢背）", 12, C["muted"], "start")
    # P
    cv.line((Lx - 6, Q_YP), (Lx + 7, Q_YP), C["ghost"], 1.2, dash="6 4")
    cv.arrow((Lx - 2, Q_YP), (Lx + 7, Q_YP), C["load"], 3.4, 12)
    cv.text_px(cv.X(Lx + 7) + 6, cv.Y(Q_YP), f"P = {Q_P:.1f}", 14, C["load"], "start", weight="700")
    # 銲道合力（向左，畫在構材外側）
    for y, f, lab, dx in ((BL, Q_FA, f"Fa = {Q_FA:.2f}", 0), (BL / 2, Q_F3, f"F3 = {Q_F3:.2f}", 0), (0, Q_FB, f"Fb = {Q_FB:.2f}", 0)):
        x0 = -1.5
        cv.arrow((x0, y), (x0 - 0.13 * f, y), C["compr"], 3.0, 10)
        cv.text_px(cv.X(x0 - 0.13 * f) - 6, cv.Y(y), lab, 12.5, C["compr"], "end", weight="700")
    cv.dim((Lx + 4, Q_YP), (Lx + 4, BL), f"{EP:g}", off=-30, label_off=-14, size=12.5)
    cv.dim((Lx + 4, 0), (Lx + 4, Q_YP), f"{Q_YP:g}", off=-30, label_off=-14, size=12.5)
    cv.text_px(W1 / 2, H1 - 44,
               f"對 a 線取矩：Fb × 15 + F3 × 7.5 = P × 10 ⇒ Fb = {Q_FB:.2f}；Fa = P − F3 − Fb = {Q_FA:.2f}（tf）",
               13, C["text"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-balance.svg")
    compose([cv], cols=1,
            title=f"圖 1　平衡銲：P 偏向肢背，b 側要比 a 側長（{Q_LB_U} 對 {Q_LA_U} cm）",
            sub=f"P 作用線距 a 側 {EP:g} cm、距 b 側 {Q_YP:g} cm；端部橫向銲 {BL:g} cm 承 {Q_F3:.2f} tf（合力在 7.5 cm）",
            note=f"驗算：三力合力位置 (0 × {Q_FA:.2f} + 7.5 × {Q_F3:.2f} + 15 × {Q_FB:.2f}) / {Q_P:.1f} = {(7.5 * Q_F3 + 15 * Q_FB) / Q_P:.1f} cm（自 a 側），恰為 P 作用線位置",
            path=path)
    return path


def fig2_lengths():
    W1, H1 = 560, 460
    cv = Canvas(W1, H1, sx=1)
    cv.panel("① 設計力 P（tf）", "毛斷面降伏與有效淨斷面斷裂取小")
    x0, sc = 190, 4.2
    for i, (nm, v, col) in enumerate((("0.6 Fy Ag", Q_PY, C["ghost"]), ("0.5 Fu U An", Q_PU, C["bmd"]))):
        y = 160 + i * 90
        cv.text_px(x0 - 12, y, nm, 14, C["text"], "end", weight="700")
        cv.rect_px(x0, y - 16, sc * v, 32, col, 4)
        cv.text_px(x0 + sc * v + 8, y, f"{v:.1f}", 14, col if i else C["muted"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 56, f"P = {Q_P:.1f} tf（有效淨斷面斷裂控制，U = {Q_U}）", 13.5, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, f"Ag = (15 + 10 − 1.5) × 1.5 = {Q_AG:.2f} cm²（全銲接無孔）", 12.5, C["muted"])
    p1 = cv
    cv = Canvas(W1, H1, sx=1)
    cv.panel("② 縱向銲所需長度（cm）", f"每 cm 容許 q = {Q_Q:.3f} tf/cm")
    x0, sc = 190, 9.0
    rows = ((f"a（趾側）", Q_LA, Q_LA_U, C["bmd"]), (f"b（肢背側）", Q_LB, Q_LB_U, C["bmd"]),
            ("誤：兩側平分", Q_EQ, None, C["ghost"]))
    for i, (nm, v, u, col) in enumerate(rows):
        y = 140 + i * 74
        cv.text_px(x0 - 12, y, nm, 13, C["text"] if u else C["muted"], "end", weight="700")
        cv.rect_px(x0, y - 14, sc * v, 28, col, 4)
        cv.text_px(x0 + sc * v + 8, y, f"{v:.1f}" + (f" → {u}" if u else "（a 側過長、b 側不足）"), 12.5,
                   col if u else C["muted"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 30, f"兩側平分各 {Q_EQ:.1f} cm：b 側只剩所需的 {Q_EQ / Q_LB:.0%}", 12.5, C["load"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-2-lengths.svg")
    compose([p1, p2], cols=2,
            title=f"圖 2　P = {Q_P:.1f} tf ⇒ a = {Q_LA_U} cm、b = {Q_LB_U} cm",
            sub=f"q = 0.3 × 4.9 × 0.707 × {W} = {Q_Q:.3f} tf/cm；Fa = {Q_FA:.2f}、Fb = {Q_FB:.2f}、F3 = {Q_F3:.2f} tf",
            note="平衡銲的長度分配由力矩決定：靠近 P 作用線的那一側要承擔較大的力",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "10 cm 誤當成距肢背，a、b 分配對調；漏算端部橫向焊 15 cm"),
    (fig1_balance, "§4 Step 3–6",
     "兩側等長或取矩線錯；忽略端部橫向銲的力矩貢獻；合力未落在 P 作用線上"),
    (fig2_lengths, "§4 Step 1–5",
     "以 0.6FyAg 為設計力；兩側平分銲長（b 側不足）"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
