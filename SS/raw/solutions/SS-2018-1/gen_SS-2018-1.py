#!/usr/bin/env python3
"""
SS-2018-1 中央細縫鋼板受拉之伸長量 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2018-1.py [輸出目錄]

重繪依據：題目正本 SS-2018-1-problem.md §4 判讀清單（待確認）。
只重繪上方鋼板示意（細縫、標點、尺寸）；下方應力–應變圖屬曲線圖，不重繪（數值見題目正本 §2、§4）。
板長與 w 的比例為示意；細縫長 0.2w 依比例。不含任何解題結果。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "..", "skills", "struct-diagram", "scripts"))   # 五科合一後 skill 在根目錄 skills/

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2018-1"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2018-1-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
L0 = 1000.0          # #5 標點間距 l0 = 1000 mm，兩標點在細縫兩側
W_DRAW = 1.0         # 板寬 w（符號；繪圖單位）
SLIT = 0.2           # #4 細縫寬方向長 0.2w，位於板寬中央、垂直拉力方向；淨寬 0.8w（推得值）
SLIT_T = 0.035       # 細縫沿拉力方向極窄（未標，示意）
LEN_DRAW, GAP = 6.0, 0.6   # 繪圖用：板長（示意）、標點距板端


def fig1_problem():
    W, H, sx = 820, 380, 105
    cv = Canvas(W, H, sx=sx, ox=(W - LEN_DRAW * sx) / 2, oy=170)
    cv.panel("鋼板（示意）", "應力–應變圖為曲線圖，不重繪；兩鋼材數值見題目正本")
    cv.polygon([(0, 0), (LEN_DRAW, 0), (LEN_DRAW, W_DRAW), (0, W_DRAW)], C["fill_c"], C["member"], 1.8)
    xm = LEN_DRAW / 2
    y0 = (W_DRAW - SLIT) / 2
    cv.polygon([(xm - SLIT_T, y0), (xm + SLIT_T, y0), (xm + SLIT_T, y0 + SLIT), (xm - SLIT_T, y0 + SLIT)],
               C["text"], C["text"], 1)
    xa, xb = GAP, LEN_DRAW - GAP
    for x in (xa, xb):
        cv.dot((x, W_DRAW / 2), 6, fill=C["text"], stroke=C["text"], w=1)
    cv.arrow((0, W_DRAW / 2), (-0.55, W_DRAW / 2), C["load"], 3, 10)
    cv.arrow((LEN_DRAW, W_DRAW / 2), (LEN_DRAW + 0.55, W_DRAW / 2), C["load"], 3, 10)
    cv.dim((xm + SLIT_T, y0), (xm + SLIT_T, y0 + SLIT), "0.2w", off=34, label_off=26)
    cv.dim((xa + 1.0, 0), (xa + 1.0, W_DRAW), "w", off=0, label_off=14)
    cv.dim((xa, 0), (xb, 0), f"l_{{0}} = {L0:.0f} mm", off=46, label_off=16)
    cv.text((xm, W_DRAW), "細縫", 13, C["text"], dy=-16, weight="700")
    cv.text((xb, W_DRAW), "標點", 13, C["text"], dy=-16, weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title="SS-2018-1 題目附圖（重繪）",
            sub="依題目正本判讀清單 #4、#5（待確認）；只畫考卷所給條件",
            note="細縫垂直拉力方向、長 0.2w，細縫處淨寬 0.8w；兩標點跨過細縫、間距 1000 mm",
            path=path)
    return path


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-15 補繪）——數值取自 SS-2018-1.md §4 與題目正本 §4
# ══════════════════════════════════════════════════════════════
FU = 500.0; AN_AG = 1 - SLIT                     # 淨／全斷面比 0.8
E_S = 2.05e5                                       # N/mm²（§4 Step 3，題未給）
MAT = {"A": {"fy": 450.0, "plat_end": 0.06},       # 題目正本 #1、#3
       "B": {"fy": 300.0, "pt": (0.06, 400.0)}}    # 題目正本 #2
EPS_U = 0.2
SIG_G = FU * AN_AG                                 # 400：淨斷面達 Fu 時的全斷面應力
EPS_A = SIG_G / E_S                                # A 仍彈性
EPS_B = MAT["B"]["pt"][0]                          # B 由圖讀 0.06
DA, DB = EPS_A * L0, EPS_B * L0


def fig2_curve():
    W1, H1p = 1000, 560
    cv = Canvas(W1, H1p, sx=1)
    cv.panel("最大拉力時（細縫淨斷面達 Fu），全斷面應力 = 0.8 Fu = 400", "曲線依題目刻度；B 的平台終點與兩曲線硬化段形狀為示意")
    X0, X1, YB, YT = 110, 640, 470, 120
    em, s0, s1 = 0.22, 0.0, 550.0
    PX = lambda e: X0 + (X1 - X0) * e / em
    PY = lambda s: YB - (YB - YT) * (s - s0) / (s1 - s0)
    L = lambda x0, y0, x1, y1, col, w=2.0, dash=None: cv.line((x0, H1p - y0), (x1, H1p - y1), col, w, dash=dash, cap="butt")
    L(X0, YB, X1, YB, C["muted"], 1.5); L(X0, YB, X0, YT, C["muted"], 1.5)
    for e in (0.06, 0.2):
        cv.text_px(PX(e), YB + 18, f"{e:g}", 11.5, C["muted"])
    for s in (300, 400, 450, 500):
        cv.text_px(X0 - 8, PY(s), f"{s}", 11.5, C["muted"], "end")
        L(X0, PY(s), X1, PY(s), C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 40, "應變 ε", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, "σ（N/mm²）", 13, C["text"], "start", weight="700")
    ea = MAT["A"]["fy"] / E_S; eb = MAT["B"]["fy"] / E_S
    pa = [(0, 0), (ea, 450), (0.06, 450), (0.13, 485), (EPS_U, FU)]
    pb = [(0, 0), (eb, 300), (0.02, 300), (0.06, 400), (0.13, 470), (EPS_U, FU)]
    cv.poly([(PX(e), H1p - PY(s)) for e, s in pa], C["compr"], 2.6)
    cv.poly([(PX(e), H1p - PY(s)) for e, s in pb], C["tension"], 2.6)
    cv.text_px(PX(0.15) , PY(492) - 12, "鋼材 A（Fy 450，YR 0.90）", 12.5, C["compr"], "end", weight="700")
    cv.text_px(PX(0.12), PY(360), "鋼材 B（Fy 300，YR 0.60）", 12.5, C["tension"], "start", weight="700")
    L(X0, PY(SIG_G), X1, PY(SIG_G), C["accent"], 1.8, dash="7 4")
    cv.text_px(X1 - 4, PY(SIG_G) - 10, f"全斷面 σ = {SIG_G:.0f}", 12.5, C["accent"], "end", weight="700")
    cv.dot((PX(EPS_A), H1p - PY(SIG_G)), 6.5, fill=C["compr"])
    cv.text_px(PX(EPS_A) + 12, PY(SIG_G) - 14, f"A：仍彈性 ε = {EPS_A:.5f}", 12.5, C["compr"], "start", weight="700")
    cv.dot((PX(EPS_B), H1p - PY(SIG_G)), 6.5, fill=C["tension"])
    cv.text_px(PX(EPS_B) + 12, PY(SIG_G) + 22, f"B：ε = {EPS_B:g}", 12.5, C["tension"], "start", weight="700")
    xt = 680
    rows = [("標距 1000 mm 的伸長量：", C["text"]),
            (f"A：{DA:.1f} mm ≈ 2 mm", C["compr"]),
            (f"B：{DB:.0f} mm", C["tension"]),
            ("", C["text"]),
            ("判斷式：", C["text"]),
            (f"YR = Fy/Fu 與 An/Ag = {AN_AG:.1f} 比", C["text"]),
            ("A：0.90 高於 0.8，全斷面來不及降伏", C["compr"]),
            ("B：0.60 低於 0.8，全長降伏、變形擴散", C["tension"])]
    for i, (s, col) in enumerate(rows):
        if s:
            cv.text_px(xt, 150 + i * 32, s, 13, col, "start", weight="700" if col != C["text"] else "400")
    path = os.path.join(OUT, f"{TAG}-fig-2-curve.svg")
    compose([cv], cols=1,
            title=f"圖 2　ΔA ≈ {DA:.0f} mm、ΔB ≈ {DB:.0f} mm：降伏比是否低於 An/Ag = {AN_AG:.1f}",
            sub="鋼材 A 是 450 平台、B 是 300 平台，兩者 Fu 都是 500",
            note="淨斷面在 P = 0.8 Fu·Ag 時就斷，全斷面應力最高只到 400；A 的 Fy 450 碰不到，只剩細縫處局部變形",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把細縫讀成平行拉力方向；標點間距沒有跨過細縫"),
    (fig2_curve, "§4 (一)(二)",
     "A、B 兩曲線對調；以為全長都達 εu；忽略淨斷面先達 Fu 時全斷面只有 0.8Fu"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
