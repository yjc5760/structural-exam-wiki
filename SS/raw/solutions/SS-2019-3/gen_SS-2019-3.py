#!/usr/bin/env python3
"""
SS-2019-3 托架偏心載重之 H 型鋼柱（ASD 檢核）— 題目附圖重繪腳本

用法：
    python3 gen_SS-2019-3.py [輸出目錄]

重繪依據：題目正本 SS-2019-3-problem.md §4 判讀清單（待確認）。
只畫考卷給的東西（A、B、C 支承、托架與 P、3 m／6 m／1 m、剖面方位），不含任何解題結果
（Pe 彎矩、各段軸力、K、F_a、F_b 都不畫）。
柱立面依 m 比例繪製；剖面 H400×200×8×13 依比例。
清單 #5（A 端是否分擔垂直力）為不確定項，圖上只照考卷畫 A 為鉸接於牆，不畫任何反力。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2019-3"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2019-3-problem.md §4，待確認）＋題文
# ══════════════════════════════════════════════════════════
L_AB = 3.0          # 圖 A–B 3 m
L_BC = 6.0          # 圖 B–C 6 m
ECC = 1.0           # #1 托架偏心 1 m（柱軸線至 P 作用線）
#                     #3 B：滾支承抵左側牆（彎曲平面內側向束制）
#                     #4 A：鉸接於右側牆；C：鉸支於地面
#                     #2 剖面：翼板垂直、腹板水平；x 軸垂直腹板、y 軸沿腹板
D, BF, TW, TF = 40.0, 20.0, 0.8, 1.3     # 題文 H400×200×8×13（cm）
P_LABEL = "P"       # 題文 P = 12 tf（工作載重）；圖上只標 P

PW, PH = 460, 600
H_TOT = L_AB + L_BC


def _hinge(cv, p):
    cv.dot(p, 6, fill="#FFFFFF", stroke=C["member"], w=2.4)


def elevation_panel():
    sx = 400 / H_TOT
    cv = Canvas(PW, PH, sx=sx, ox=230, oy=95)
    cv.panel("柱立面", "依比例")
    Cc, B, A = (0, 0), (0, L_BC), (0, H_TOT)
    cv.line(Cc, A, C["member"], 4, cap="butt")
    cv.support(A, "pin", 90, size=14)            # A：鉸接於右側牆
    cv.support(B, "roller", -90, size=12)        # B：滾支承抵左側牆
    cv.support(Cc, "pin", 0, size=14)            # C：鉸支於地面
    for p in (A, B, Cc):
        _hinge(cv, p)
    cv.text(A, "A", 16, C["text"], "end", dx=-14, dy=-8, weight="700")
    cv.text(B, "B", 16, C["text"], "end", dx=-60, dy=0, weight="700")
    cv.text(Cc, "C", 16, C["text"], "end", dx=-14, dy=-6, weight="700")
    # 托架與 P
    tip = (ECC, L_BC)
    cv.line(B, tip, C["member"], 3.6, cap="butt")
    cv.arrow((ECC, L_BC + 54 / sx), tip, C["load"], 3.0, 11)
    cv.math((ECC, L_BC + 54 / sx), P_LABEL, 18, C["load"], "start", dx=10, dy=4, weight="700")
    cv.dim((0, L_BC - 1.2), (ECC, L_BC - 1.2), f"{ECC:.0f} m", off=0, label_off=-14, size=15)
    # 3 m／6 m
    cv.dim((-2.2, L_BC), (-2.2, H_TOT), f"{L_AB:.0f} m", off=0, label_off=-26, size=15)
    cv.dim((-2.2, 0), (-2.2, L_BC), f"{L_BC:.0f} m", off=0, label_off=-26, size=15)
    for y in (0, L_BC, H_TOT):
        cv.line((-2.45, y), (-1.95, y), C["dim"], 1)
    # 剖面記號（下段）
    yc = 2.6
    for sgn in (-1, 1):
        x0, x1 = sgn * 0.45, sgn * 1.05
        cv.line((x0, yc), (x1, yc), C["member"], 1.6)
        cv.arrow((x1, yc), (x1, yc - 0.55), C["member"], 1.6, 8)
    return cv


def section_panel():
    s = 6.0
    cv = Canvas(PW, PH, sx=s, ox=PW / 2 + 20, oy=PH / 2 - 10)
    cv.panel("剖面", "H400×200×8×13（依比例）")
    def R(x0, x1, y0, y1):
        cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], C["fill_c"], C["member"], 1.6)
    R(-D / 2, -D / 2 + TF, -BF / 2, BF / 2)       # 左翼板（垂直）
    R(D / 2 - TF, D / 2, -BF / 2, BF / 2)         # 右翼板（垂直）
    R(-D / 2 + TF, D / 2 - TF, -TW / 2, TW / 2)   # 腹板（水平）
    # x 軸：垂直腹板（圖上鉛直），y 軸：沿腹板（圖上水平）
    cv.line((0, 0), (0, BF / 2 + 8), C["text"], 1.4)
    cv.math((0, BF / 2 + 8), "x", 18, C["text"], dy=-12)
    cv.line((-D / 2 - 14, 0), (-D / 2 + TF, 0), C["text"], 1.4)
    cv.math((-D / 2 - 14, 0), "y", 18, C["text"], "end", dx=-6)
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([elevation_panel(), section_panel()], cols=2,
            title="SS-2019-3 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#4；立面與剖面皆依比例；P = 12 tf（工作載重）",
            note="B 點是抵牆滾支承（立面內側向束制），P 經 1 m 托架偏心作用於 B",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2019-3.md §1／§4，由下式即時算出
# ══════════════════════════════════════════════════════════════
import math
P_TF, ECC = 12.0, 1.0                         # tf、m                        §1
L_AB, L_BC = 3.0, 6.0                         # m                            §1
A_G, S_X, R_X, R_Y, R_T = 83.4, 1170.0, 16.8, 4.56, 5.23                  # §1
BF_C, TF_C, D_C = 20.0, 1.3, 40.0             # cm                           §4 Step 5
F_Y, E_T = 2.5, 2040.0                        # §1
OLD_RATIO = 0.552                             # 舊解（漏看 B 點支承）之比值，引自 §5

M_B  = P_TF * ECC                             # 節點力矩 12 tf·m              Step 1
K_AB, K_BC = 3 / L_AB, 3 / L_BC               # 遠端鉸：k = 3EI/L（EI 約去）
M_BA = M_B * K_AB / (K_AB + K_BC)             # 8
M_BC = M_B * K_BC / (K_AB + K_BC)             # 4
R_A, R_C = M_BA / L_AB, M_BC / L_BC
R_B  = R_A + R_C
# 誤讀：A–C 單跨簡支、B 點無支承
L_AC = L_AB + L_BC
R_W  = M_B / L_AC
MW_ABOVE, MW_BELOW = R_W * L_AB, R_W * L_BC   # 4、8

fa   = P_TF / A_G                                              # Step 2（B-C 段）
CC   = math.sqrt(2 * math.pi**2 * E_T / F_Y)
EUL  = lambda klr: 12 * math.pi**2 * E_T / (23 * klr**2)
KLRY = L_BC * 100 / R_Y
FA   = EUL(KLRY) if KLRY > CC else None                        # 彈性（KL/ry > Cc）Step 3
CB   = 1.75
LRT  = L_BC * 100 / R_T
FB1  = (2/3 - F_Y * LRT**2 / (107600 * CB)) * F_Y
FB2  = 840 * CB / (L_BC * 100 * D_C / (BF_C * TF_C))
FBX  = min(max(FB1, FB2), 0.6 * F_Y)                           # Step 5
FEX  = EUL(L_BC * 100 / R_X)                                   # Step 6
CMX  = 0.6
fbx_bc, fbx_ab = M_BC * 100 / S_X, M_BA * 100 / S_X
EQ1  = [fa / FA, CMX * fbx_bc / ((1 - fa / FEX) * FBX)]        # Step 7
EQ2  = [fa / (0.6 * F_Y), fbx_bc / FBX]
R_AB = fbx_ab / (0.6 * F_Y)                                    # Step 8：L/rT 小於 √(7160Cb/Fy) → 0.6Fy


def _model_panel(title, sub, braced, m_above, m_below, reacts):
    W1, H1 = 520, 600
    cv = Canvas(W1, H1, sx=1)
    cv.panel(title, sub)
    cx, ya, yc = 180, 150, 480
    yb = ya + (yc - ya) * L_AB / L_AC
    Y = lambda y: H1 - y
    _hl(cv, H1, cx, ya, cx, yc, C["member"], 5.0)
    cv.support((cx, Y(ya)), "pin", -90, size=14)
    cv.support((cx, Y(yc)), "pin", -90, size=14)
    if braced:
        cv.support((cx, Y(yb)), "roller", -90, size=14)
    # 托架與 P
    _hl(cv, H1, cx, yb, cx + 40, yb, C["member"], 3.0)
    cv.arrow((cx + 40, Y(yb - 54)), (cx + 40, Y(yb - 4)), C["load"], 2.8, 10)
    cv.text_px(cx + 48, yb - 48, f"P = {P_TF:g} tf", 12.5, C["load"], "start", weight="700")
    cv.text_px(cx + 48, yb + 18, f"e = {ECC:g} m", 12, C["muted"], "start")
    for y, nm in ((ya, "A"), (yb, "B"), (yc, "C")):
        cv.text_px(cx + 12, y - 16 if nm == "B" else y, nm, 15, C["text"], "start", weight="700")
    for y, s in reacts:
        cv.text_px(cx - 50, y, s, 12, C["sfd"], "end", weight="700")
    # 彎矩圖：另畫一條基線（受拉側示意，B 點跳躍 = M_B）
    bx, sc = 390, 9.0
    _hl(cv, H1, bx, ya, bx, yc, C["muted"], 1.4)
    cv.polygon([(bx, Y(ya)), (bx + sc * m_above, Y(yb)), (bx, Y(yb))], C["fill_m"], C["bmd"], 2.2)
    cv.polygon([(bx, Y(yb)), (bx - sc * m_below, Y(yb)), (bx, Y(yc))], C["fill_m"], C["bmd"], 2.2)
    cv.text_px(bx + sc * m_above + 6, yb - 10, f"{m_above:g}", 14, C["bmd"], "start", weight="700")
    cv.text_px(bx - sc * m_below - 6, yb + 18, f"{m_below:g}", 14, C["bmd"], "end", weight="700")
    cv.text_px(bx, ya - 18, "M（tf·m）", 12.5, C["bmd"], weight="700")
    return cv


def fig1_models():
    p1 = _model_panel("① 正解：B 點靠牆滾支 ⇒ 兩跨連續", "節點力矩依勁度 3EI/L 分配：短跨分多",
                      True, M_BA, M_BC,
                      ((150, f"RA = {R_A:.2f}"), (150 + 330 * L_AB / L_AC, f"RB = {R_B:.2f}"),
                       (480, f"RC = {R_C:.2f}")))
    p1.text_px(260, 600 - 40, f"A-B {M_BA:g}、B-C {M_BC:g} tf·m（2 : 1）", 13.5, C["bmd"], weight="700")
    p2 = _model_panel("② 誤讀：漏看 B 點支承 ⇒ 9 m 單跨", "反力 = M/L，B 點兩側彎矩與距離成正比",
                      False, MW_ABOVE, MW_BELOW,
                      ((150, f"RA = {R_W:.2f}"), (480, f"RC = {R_W:.2f}")))
    p2.text_px(260, 600 - 40, f"A-B {MW_ABOVE:g}、B-C {MW_BELOW:g} tf·m——分配剛好相反", 13.5, C["load"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-models.svg")
    compose([p1, p2], cols=2,
            title=f"圖 1　偏心載重的節點力矩 MB = P·e = {M_B:g} tf·m 怎麼分配",
            sub="兩種支承判讀，B 點兩側彎矩之和都等於 12，但哪一段分多完全相反",
            note=f"反力單位 tf（水平）；正解的 RB = {R_B:.2f} 由 B 點靠牆滾支提供，單跨模型沒有這一項",
            path=path)
    return path


def fig2_check():
    W1, H1 = 520, 520
    cv = Canvas(W1, H1, sx=1)
    cv.panel("① 軸力路徑", "托架把 P 送進 B，再往下傳到 C")
    cx, ya, yc = 170, 130, 430
    yb = ya + (yc - ya) * L_AB / L_AC
    _hl(cv, H1, cx, ya, cx, yc, C["member"], 5.0)
    bx, sc = 300, 7.0
    _hl(cv, H1, bx, ya, bx, yc, C["muted"], 1.4)
    cv.polygon([(bx, H1 - yb), (bx + sc * P_TF, H1 - yb), (bx + sc * P_TF, H1 - yc), (bx, H1 - yc)],
               C["fill_c"], C["compr"], 2.2)
    cv.text_px(bx + sc * P_TF + 8, (yb + yc) / 2, f"N = {P_TF:g} tf（壓）", 13, C["compr"], "start", weight="700")
    cv.text_px(bx + 8, (ya + yb) / 2, "N = 0", 13, C["muted"], "start", weight="700")
    for y, nm in ((ya, "A"), (yb, "B"), (yc, "C")):
        cv.text_px(cx - 16, y, nm, 15, C["text"], "end", weight="700")
    cv.text_px(W1 / 2, H1 - 58, "A-B 段：純彎（MBA = 8）", 13, C["bmd"], weight="700")
    cv.text_px(W1 / 2, H1 - 32, "B-C 段：軸壓 12 tf ＋ 彎矩 4（梁柱）", 13, C["compr"], weight="700")
    p1 = cv

    cv = Canvas(W1, H1, sx=1)
    cv.panel("② 兩段分別檢核", f"B-C：fa/Fa = {EQ1[0]:.3f} > 0.15 ⇒ 兩式")
    x0, SC = 150, 280.0
    _hl(cv, H1, x0 + SC, 130, x0 + SC, 380, C["load"], 2.0, dash="6 4")
    cv.text_px(x0 + SC, 120, "上限 1.0", 12.5, C["load"], weight="700")
    _stack_row(cv, x0, 180, SC, [R_AB], [C["bmd"]], "A-B 純彎", C["bmd"])
    _stack_row(cv, x0, 250, SC, EQ1, [C["compr"], C["bmd"]], "B-C 互制一", C["text"])
    _stack_row(cv, x0, 320, SC, EQ2, [C["compr"], C["bmd"]], "B-C 互制二", C["text"])
    cv.text_px(x0 + SC * R_AB + 80, 180, "← 控制", 12.5, C["bmd"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 58, f"舊解（單跨模型）只算 B-C 段：{OLD_RATIO:.3f}", 12.5, C["muted"])
    cv.text_px(W1 / 2, H1 - 32, "結論同為 OK，但控制段與比值都不同", 12.5, C["muted"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-2-check.svg")
    compose([p1, p2], cols=2,
            title=f"圖 2　A-B 段撓曲控制 {R_AB:.3f}；B-C 段互制 {rsum(EQ1):.3f}",
            sub=f"Fa = {FA:.3f}（KL/ry = {KLRY:.1f} > Cc = {CC:.1f}）　Fbx = {FBX:.1f}　F'ex = {FEX:.2f}（tf/cm²）",
            note="A-B 段沒有軸力卻比 B-C 段危險：它分到兩倍的彎矩",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "漏看 B 點抵牆滾支承而把柱當成 9 m 單跨；剖面 x／y 方位讀反（誤判為弱軸彎曲）；偏心量錯取"),
    (fig1_models, "§4 Step 1",
     "漏看 B 點靠牆滾支而用 9 m 單跨，A-B／B-C 彎矩 8／4 被讀成 4／8"),
    (fig2_check, "§4 Step 2–8",
     "把軸力算到整根柱；只驗 B-C 段而漏掉控制的 A-B 段純彎"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
