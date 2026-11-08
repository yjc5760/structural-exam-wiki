#!/usr/bin/env python3
"""
SS-2005-2 混凝土包覆鋼梁（SRC 梁）塑性應力分析 Mn — 題目附圖重繪腳本

用法：
    python3 gen_SS-2005-2.py [輸出目錄]

重繪依據：題目正本 SS-2005-2-problem.md §4 判讀清單（待確認）。
只畫考卷給的東西（斷面外形、H 型鋼、四支主筋、8 cm 尺寸），不含任何解題結果（不畫中性軸、應力塊）。
斷面、H 型鋼與主筋直徑依比例繪製。
示意部分：主筋水平位置（考卷未標，取與上下相同之 8 cm 內縮）、箍筋框線、骨材點。
不重繪：無。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2005-2"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2005-2-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
B, H = 50.0, 70.0           # #1 斷面寬 50 cm、高 70 cm
COVER = 8.0                 # #2 上、下緣至主筋「中心」8 cm
N_TOP, N_BOT = 2, 2         # #3 上 2 支、下 2 支，位於四角
DB = 3.2                    # 題文 D32（直徑約 3.2 cm，僅供依比例畫圓）
D, BF, TW, TF = 48.8, 30.0, 1.1, 1.8   # 題文 H488×300×11×18（mm → cm）
#                             #4 鋼梁直立置中
X_BAR = COVER               # 主筋水平內縮：考卷未標，示意取 8 cm
STIR = COVER - DB / 2 - 0.6 # 箍筋框線（示意）

PW, PH = 640, 620


def _rect(cv, x0, x1, y0, y1, fill, stroke, w=1.6, op=1.0):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, stroke, w, op)


def section_panel():
    sx = 5.6
    cv = Canvas(PW, PH, sx=sx, ox=PW / 2 - B / 2 * sx - 40, oy=90)
    cv.panel("混凝土包覆梁斷面", "斷面、H 型鋼、主筋依比例；箍筋與骨材為示意")
    # 混凝土
    _rect(cv, 0, B, 0, H, C["ghost"], "none", 0, op=0.40)
    _rect(cv, 0, B, 0, H, "none", C["member"], 2.2)
    for (x, y) in ((6, 52), (12, 30), (38, 58), (41, 22), (9, 14), (30, 6.5), (20, 63),
                   (44, 44), (5, 40), (33, 40)):
        cv.circle((x, y), 0.45, "none", C["member2"], 1.0)
    # 箍筋（示意）
    _rect(cv, STIR, B - STIR, STIR, H - STIR, "none", C["member2"], 1.4)
    # H 型鋼（置中、直立）
    xc, yc = B / 2, H / 2
    st = C["member"]
    _rect(cv, xc - BF / 2, xc + BF / 2, yc + D / 2 - TF, yc + D / 2, C["fill_c"], st, 1.6)
    _rect(cv, xc - BF / 2, xc + BF / 2, yc - D / 2, yc - D / 2 + TF, C["fill_c"], st, 1.6)
    _rect(cv, xc - TW / 2, xc + TW / 2, yc - D / 2 + TF, yc + D / 2 - TF, C["fill_c"], st, 1.6)
    # 主筋（四角）
    bars = [(X_BAR, H - COVER), (B - X_BAR, H - COVER), (X_BAR, COVER), (B - X_BAR, COVER)]
    for p in bars:
        cv.circle(p, DB / 2, C["member"], C["member"], 1.0)
    # 尺寸
    cv.dim((0, H), (B, H), f"{B:.0f} cm", off=-34, label_off=-14)
    cv.dim((0, 0), (0, H), f"{H:.0f} cm", off=-46, label_off=-30)
    cv.dim((B, H - COVER), (B, H), f"{COVER:.0f} cm", off=46, label_off=30, color=C["accent"])
    cv.dim((B, 0), (B, COVER), f"{COVER:.0f} cm", off=46, label_off=30, color=C["accent"])
    # 標示
    cv.line((xc + TW / 2, yc + 4), (B + 14, yc + 6), C["muted"], 1.2)
    cv.text((B + 14, yc + 6), "鋼梁", 14, C["text"], "start", dx=4)
    cv.text((B + 14, yc + 6), "H488×300×11×18", 12, C["muted"], "start", dx=4, dy=20)
    for p in bars[2:]:
        cv.line(p, (B / 2, -9), C["muted"], 1.2)
    cv.text((B / 2, -9), "主筋 4-D32", 14, C["text"], dy=14)
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([section_panel()], cols=1,
            title="SS-2005-2 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#4；只畫考卷所給條件",
            note="8 cm 量到主筋中心（不是箍筋線）；H 型鋼置於斷面正中",
            path=path)
    return path


# ── 解題圖解共用小工具（像素座標；y 由上往下）──
def _pP(cv, x, y):
    return (x, cv.h - y)


def _pL(cv, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line(_pP(cv, x0, y0), _pP(cv, x1, y1), color, w, dash=dash, cap="butt")


def _pR(cv, x0, y0, x1, y1, fill, stroke="none", sw=1.2):
    cv.polygon([_pP(cv, x0, y0), _pP(cv, x1, y0), _pP(cv, x1, y1), _pP(cv, x0, y1)], fill, stroke, sw)


def _pA(cv, x0, y0, x1, y1, color, w=2.6, head=9):
    cv.arrow(_pP(cv, x0, y0), _pP(cv, x1, y1), color, w, head)


def _pT(cv, x, y, s, size=13, color=C["text"], anchor="middle", weight="400"):
    cv.text_px(x, y, s, size, color, anchor, weight=weight)


def _pPL(cv, pts, color, w=2.0, dash=None):
    cv.poly([_pP(cv, x, y) for x, y in pts], color, w, dash=dash)


def _fmt(v, nd=1):
    """與解析相同的顯示：四捨五入（加微量避免浮點 .x5 落到下方）＋千分位"""
    v = round(v + (1e-9 if v >= 0 else -1e-9), nd)
    return f"{v:,.{nd}f}"



# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2005-2.md §4，由下式即時算出（tf、cm）
# ══════════════════════════════════════════════════════════════
Q_FC = 0.85 * 0.21                      # 0.85 f'c = 0.1785 tf/cm²
Q_FY, Q_FYR = 2.5, 4.2                  # 鋼骨、鋼筋
Q_AR = 16.38                            # 2-D32
Q_TOPF = (H - D) / 2                    # 10.6
Q_Y1, Q_Y2 = Q_TOPF, Q_TOPF + TF        # 上翼板 10.6～12.4
Q_Y3, Q_Y4 = H - Q_TOPF - TF, H - Q_TOPF  # 下翼板 57.6～59.4
Q_HW = Q_Y3 - Q_Y2                      # 45.2
Q_CC = B * Q_FC                         # 8.925 tf/cm
Q_RF = Q_AR * Q_FYR                     # 68.8
Q_FF = BF * TF * Q_FY                   # 135.0
Q_WW = TW * Q_FY                        # 2.75 tf/cm
Q_ST = 2 * Q_FF + Q_WW * Q_HW           # 394.3


def q_ct(y):
    """PNA 距頂面 y（≥ 8 cm，上排筋受壓）時的總壓力 C、總拉力 T"""
    cs = 0.0
    if y > Q_Y1: cs += min(y - Q_Y1, TF) * BF * Q_FY
    if y > Q_Y2: cs += min(y - Q_Y2, Q_HW) * Q_WW
    if y > Q_Y3: cs += min(y - Q_Y3, TF) * BF * Q_FY
    return Q_CC * y + Q_RF + cs, Q_ST - cs + Q_RF


Q_YP = (Q_WW * Q_Y3 + Q_WW * Q_Y2) / (Q_CC + 2 * Q_WW)     # 13.34
Q_PARTS = [  # 名稱、壓/拉、力、作用位置
    ("混凝土", "壓", Q_CC * Q_YP, Q_YP / 2),
    ("上排鋼筋", "壓", Q_RF, COVER),
    ("上翼板", "壓", Q_FF, (Q_Y1 + Q_Y2) / 2),
    ("腹板受壓段", "壓", Q_WW * (Q_YP - Q_Y2), (Q_Y2 + Q_YP) / 2),
    ("腹板受拉段", "拉", Q_WW * (Q_Y3 - Q_YP), (Q_YP + Q_Y3) / 2),
    ("下翼板", "拉", Q_FF, (Q_Y3 + Q_Y4) / 2),
    ("下排鋼筋", "拉", Q_RF, H - COVER),
]
Q_MN = sum(f * abs(yc - Q_YP) for _, _, f, yc in Q_PARTS)   # 13,548.9 tf·cm


def fig1_pna():
    W1, H1 = 1120, 600
    cv = Canvas(W1, H1)
    cv.panel("塑性應力分布：PNA 在腹板頂端下方 0.94 cm（y = 13.34 cm）",
             "壓力側：混凝土 0.85f'c、上排筋 Fyr、上翼板與 0.94 cm 腹板 Fy；其餘鋼骨與下排筋全拉")
    TOP, S = 100.0, 6.2
    py = lambda d: TOP + d * S
    x0 = 60.0
    px = lambda x: x0 + x * S
    # 斷面
    _pR(cv, px(0), py(0), px(B), py(H), "#EEF0F3", C["member"], 1.6)
    _pR(cv, px(0), py(0), px(B), py(Q_YP), "rgba(29,78,216,0.10)")
    for ya, yb in ((Q_Y1, Q_Y2), (Q_Y3, Q_Y4)):
        _pR(cv, px((B - BF) / 2), py(ya), px((B + BF) / 2), py(yb), "#B8C0CC", C["member"], 1.3)
    _pR(cv, px((B - TW) / 2), py(Q_Y2), px((B + TW) / 2), py(Q_Y3), "#B8C0CC", C["member"], 1.3)
    for yy in (COVER, H - COVER):
        for xx in (X_BAR, B - X_BAR):
            cv.circle(_pP(cv, px(xx), py(yy)), DB / 2 * S, C["accent"], C["text"], 1.2)
    # 位置刻度（左）
    for d, lab in ((0, "0"), (COVER, "8.0"), (Q_Y1, "10.6"), (Q_Y2, "12.4"), (Q_Y3, "57.6"),
                   (Q_Y4, "59.4"), (H - COVER, "62.0"), (H, "70")):
        _pL(cv, px(0) - 6, py(d), px(0), py(d), C["dim"], 1.2)
        _pT(cv, px(0) - 9, py(d), lab, 10.5, C["muted"], "end")
    _pT(cv, px(B / 2), py(H) + 18, "距頂面深度 (cm)，左側刻度", 11.5, C["muted"])
    # 應力欄：混凝土
    zc = 430.0
    _pL(cv, zc, py(0) - 8, zc, py(H) + 4, C["member2"], 1.2)
    _pR(cv, zc - 34, py(0), zc, py(Q_YP), C["fill_c"], C["compr"], 1.4)
    _pT(cv, zc - 17, py(0) - 16, "混凝土", 12, C["compr"], weight="700")
    _pT(cv, zc + 6, py(Q_YP / 2), "0.1785", 10.5, C["compr"], "start")
    # 應力欄：鋼骨（壓左、拉右）
    zs = 540.0
    _pL(cv, zs, py(0) - 8, zs, py(H) + 4, C["member2"], 1.2)
    _pR(cv, zs - 34, py(Q_Y1), zs, py(Q_YP), C["fill_c"], C["compr"], 1.4)
    _pR(cv, zs, py(Q_YP), zs + 34, py(Q_Y4), C["fill_t"], C["tension"], 1.4)
    _pT(cv, zs, py(0) - 16, "鋼骨 Fy = 2.5", 12, C["text"], weight="700")
    _pT(cv, zs - 38, py(Q_Y1) - 2, "壓", 11.5, C["compr"], "end", weight="700")
    _pT(cv, zs + 38, py(36), "拉", 11.5, C["tension"], "start", weight="700")
    # 鋼筋力（箭頭）
    zr = 620.0
    _pL(cv, zr, py(0) - 8, zr, py(H) + 4, C["member2"], 1.2)
    _pT(cv, zr, py(0) - 16, "鋼筋 4.2", 12, C["text"], weight="700")
    _pA(cv, zr + 2, py(COVER), zr - 34, py(COVER), C["compr"], 2.6, 8)
    _pA(cv, zr - 2, py(H - COVER), zr + 34, py(H - COVER), C["tension"], 2.6, 8)
    # PNA 線
    _pL(cv, px(0) - 4, py(Q_YP), zr + 40, py(Q_YP), C["accent"], 1.8, dash="8 3 2 3")
    _pT(cv, px(B) + 6, py(Q_YP) + 13, f"PNA  y = {_fmt(Q_YP, 2)}", 12, C["accent"], "start", weight="700")
    # 力表（右），以導線接到作用深度
    tx, ty0, dy = 700.0, 150.0, 40.0
    cols = (tx + 8, tx + 150, tx + 230, tx + 320)
    _pT(cv, cols[0], ty0 - 30, "組成", 12, C["muted"], "start", weight="700")
    for c, s in zip(cols[1:], ("力 (tf)", "力臂 (cm)", "力矩 (tf·cm)")):
        _pT(cv, c, ty0 - 30, s, 12, C["muted"], weight="700")
    for i, (nm, kind, f, yc) in enumerate(Q_PARTS):
        yy = ty0 + i * dy
        col = C["compr"] if kind == "壓" else C["tension"]
        _pPL(cv, [(zr + 44, py(yc)), (tx - 10, yy), (tx, yy)], col, 1.0, dash="3 3")
        cv.circle(_pP(cv, zr + 44, py(yc)), 2.6, col, col, 1)
        _pT(cv, cols[0], yy, f"{nm}（{kind}）", 12.5, col, "start", weight="700")
        _pT(cv, cols[1], yy, _fmt(f, 2), 12.5, col)
        _pT(cv, cols[2], yy, _fmt(abs(yc - Q_YP), 2), 12.5, C["text"])
        _pT(cv, cols[3], yy, _fmt(f * abs(yc - Q_YP), 1), 12.5, C["text"])
    yy = ty0 + 7 * dy
    _pL(cv, tx, yy - 20, tx + 380, yy - 20, C["border"], 1.2)
    csum = sum(f for _, k, f, _ in Q_PARTS if k == "壓")
    _pT(cv, cols[0], yy, f"C = T = {_fmt(csum, 1)}", 12.5, C["text"], "start", weight="700")
    _pT(cv, cols[3], yy, _fmt(Q_MN, 1), 13, C["bmd"], weight="700")
    _pT(cv, tx + 190, yy + 38, f"Mn = {_fmt(Q_MN / 100, 1)} tf·m，φbMn = 0.9 × {_fmt(Q_MN / 100, 1)} = {_fmt(0.9 * Q_MN / 100, 1)} tf·m",
        13.5, C["bmd"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-2-pna.svg")
    compose([cv], cols=1,
            title=f"圖 2　PNA y = {_fmt(Q_YP, 2)} cm：C = T = {_fmt(csum, 1)} tf，對 PNA 取矩 Mn = {_fmt(Q_MN, 0)} tf·cm",
            sub="混凝土壓力取全寬 50 cm × y × 0.85f'c（解析主解，未扣鋼骨排開的混凝土）",
            note="各力臂一律量到 PNA；上排筋在 PNA 以上算壓、下排筋算拉，四支筋都要計入",
            path=path)
    return path


def fig2_trial():
    W1, H1 = 1060, 520
    cv = Canvas(W1, H1)
    cv.panel("PNA 試算：總壓力 C(y) 隨 y 增加、總拉力 T(y) 隨 y 減少，交點即 PNA",
             "橫軸 PNA 距頂面 y (cm)；縱軸力 (tf)")
    X0, X1, Y0, Y1 = 110.0, 700.0, 450.0, 100.0
    ya, yb, fa, fb = 8.0, 20.0, 100.0, 500.0
    gx = lambda y: X0 + (y - ya) / (yb - ya) * (X1 - X0)
    gy = lambda f: Y0 - (f - fa) / (fb - fa) * (Y0 - Y1)
    _pR(cv, gx(Q_Y1), Y1, gx(Q_Y2), Y0, "rgba(138,148,166,0.16)")
    _pT(cv, gx((Q_Y1 + Q_Y2) / 2), Y1 + 14, "上翼板", 11.5, C["muted"])
    _pT(cv, gx(16.5), Y1 + 14, "腹板 →", 11.5, C["muted"])
    _pL(cv, X0, Y0, X1, Y0, C["member"], 1.4)
    _pL(cv, X0, Y0, X0, Y1, C["member"], 1.4)
    for y in range(8, 21, 2):
        _pL(cv, gx(y), Y0, gx(y), Y0 + 5, C["member"], 1.2)
        _pT(cv, gx(y), Y0 + 18, str(y), 11.5, C["muted"])
    for f in range(100, 501, 100):
        _pL(cv, X0 - 5, gy(f), X0, gy(f), C["member"], 1.2)
        _pT(cv, X0 - 9, gy(f), str(f), 11.5, C["muted"], "end")
        _pL(cv, X0, gy(f), X1, gy(f), C["border"], 0.8)
    _pT(cv, (X0 + X1) / 2, Y0 + 40, "PNA 距頂面 y (cm)", 12.5, C["muted"])
    ys = [ya + i * (yb - ya) / 240 for i in range(241)]
    _pPL(cv, [(gx(y), gy(q_ct(y)[0])) for y in ys], C["compr"], 2.6)
    _pPL(cv, [(gx(y), gy(q_ct(y)[1])) for y in ys], C["tension"], 2.6)
    _pT(cv, gx(19.6), gy(q_ct(19.6)[0]) - 14, "C(y)", 13, C["compr"], weight="700")
    _pT(cv, gx(19.6), gy(q_ct(19.6)[1]) + 16, "T(y)", 13, C["tension"], weight="700")
    c1, t1 = q_ct(Q_Y1)
    c2, t2 = q_ct(Q_Y2)
    for y, c, t in ((Q_Y1, c1, t1), (Q_Y2, c2, t2)):
        _pL(cv, gx(y), gy(c), gx(y), gy(t), C["muted"], 1.2, dash="4 3")
        cv.dot(_pP(cv, gx(y), gy(c)), 4, C["compr"])
        cv.dot(_pP(cv, gx(y), gy(t)), 4, C["tension"])
    _pPL(cv, [(gx(Q_Y1) + 4, gy(c1) + 3), (gx(14.0), gy(165))], C["muted"], 1.0, dash="3 3")
    _pT(cv, gx(14.05), gy(165), f"y = 10.6：C {_fmt(c1, 1)} 小於 T {_fmt(t1, 1)}", 11.5, C["muted"], "start")
    _pT(cv, gx(Q_Y2) + 8, gy(c2) + 30, f"y = 12.4：C {_fmt(c2, 1)} 小於 T {_fmt(t2, 1)}", 11.5, C["text"], "start")
    cp, _ = q_ct(Q_YP)
    _pL(cv, gx(Q_YP), gy(cp), gx(Q_YP), Y0, C["accent"], 1.6, dash="6 3")
    cv.dot(_pP(cv, gx(Q_YP), gy(cp)), 6, C["accent"])
    _pT(cv, gx(Q_YP) + 10, gy(cp) - 34, f"交點 y = {_fmt(Q_YP, 2)} cm，C = T = {_fmt(cp, 1)} tf", 13, C["accent"], "start", weight="700")
    # 右側說明
    xt = 740.0
    rows = [("三次試算", C["text"], "700"),
            ("試 1　PNA 在上翼板以上（鋼骨全拉）", C["text"], "700"),
            ("8.925y + 68.8 = 394.3 + 68.8", C["muted"], "400"),
            ("→ y = 44.2 大於 10.6，矛盾", C["load"], "700"),
            ("試 2　PNA 在上翼板內", C["text"], "700"),
            (f"y = 12.4 時 C {_fmt(c2, 1)} 仍小於 T {_fmt(t2, 1)}", C["muted"], "400"),
            ("→ 還要往下", C["load"], "700"),
            ("試 3　PNA 在腹板內", C["text"], "700"),
            (f"14.425y = 192.5 → y = {_fmt(Q_YP, 2)}", C["muted"], "400"),
            ("→ 落在 12.4～57.6，成立", C["bmd"], "700")]
    for i, (s, col, wt) in enumerate(rows):
        _pT(cv, xt, 112 + i * 31, s, 12.5, col, "start", weight=wt)
    path = os.path.join(OUT, f"{TAG}-fig-1-trial.svg")
    compose([cv], cols=1,
            title=f"圖 1　C(y) 與 T(y) 在腹板內相交：PNA y = {_fmt(Q_YP, 2)} cm（上翼板全壓）",
            sub="C(y)、T(y) 依解析 4.2 節各組成降伏力逐段累加；上排筋假設受壓（y 大於 8 cm 成立）",
            note="試 2 檢核翼板底 y = 12.4 時 C 仍不足，才確定 PNA 進入腹板；跳過這一步容易把 PNA 放在翼板內",
            path=path)
    return path



FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把 8 cm 讀成保護層（量到鋼筋外緣或箍筋），使主筋深度差一個半徑；H 型鋼未置中"),
    (fig1_pna, "§4.3–4.4",
     "力臂沒量到 PNA；漏了上排筋或下排筋；混凝土壓力用錯深度"),
    (fig2_trial, "§4.3",
     "PNA 位置試算錯段（停在上翼板）；試 1 矛盾後未換段"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
