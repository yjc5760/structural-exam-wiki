#!/usr/bin/env python3
"""
SS-2008-2 靠桿效應與萊梅厥公式 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2008-2.py [輸出目錄]

重繪依據：題目正本 SS-2008-2-problem.md §4 判讀清單（2026-11-02 已確認）。
只畫考卷給的東西（支承、節點、EI、載重、L、L_b）；不含任何解題結果。
L、L_b 為符號，圖形比例示意。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2008-2"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2008-2-problem.md §4，已確認）
# ══════════════════════════════════════════════════════════
SINGLE_BASE = "pin"        # #1 單根柱底部鉸支
SINGLE_TOP = "guided"      # #2 頂部導槽滾支：可水平移動、不可轉動
K_SINGLE = 2.0             # 題文 K = 2.0（圖面文字 K=2）
A_KIND = D_KIND = "pin"    # #4 A 鉸支、#7 D 鉸支
B_RIGID = True             # #5 B 剛接（無鉸圓）
C_HINGE = True             # #6 C 鉸接（鉸圓）；#8 CD 為靠桿
#                            #9 梁 BC EI = ∞；#10 B、C 各受垂直 P
L_DRAW, LB_DRAW = 1.0, 1.25   # 繪圖比例（L、L_b 為符號）

PW, PH = 520, 470


def _guided_top(cv, p):
    """導槽滾支：柱頂板＋兩個滾輪＋上方固定面（可平移、不可轉動）"""
    x, y = cv.P(p)
    cv.parts.append(f'<line x1="{x-20:.1f}" y1="{y:.1f}" x2="{x+20:.1f}" y2="{y:.1f}" '
                    f'stroke="{C["member"]}" stroke-width="4" stroke-linecap="butt"/>')
    for dx in (-9, 9):
        cv.parts.append(f'<circle cx="{x+dx:.1f}" cy="{y-7:.1f}" r="5" fill="#FFFFFF" '
                        f'stroke="{C["member"]}" stroke-width="2"/>')
    cv.parts.append(f'<line x1="{x-24:.1f}" y1="{y-14:.1f}" x2="{x+24:.1f}" y2="{y-14:.1f}" '
                    f'stroke="{C["member"]}" stroke-width="2.6" stroke-linecap="round"/>')
    for k in range(6):
        bx = x - 22 + k * 9
        cv.parts.append(f'<line x1="{bx:.1f}" y1="{y-14:.1f}" x2="{bx+7:.1f}" y2="{y-23:.1f}" '
                        f'stroke="{C["member"]}" stroke-width="1.8" stroke-linecap="round"/>')


def single_panel():
    sx = 250
    cv = Canvas(PW, PH, sx=sx, ox=PW / 2, oy=110)
    cv.panel("單根柱", "底部鉸支、頂部導槽滾支")
    cv.line((0, 0), (0, L_DRAW), C["member"], 4, cap="butt")
    cv.support((0, 0), SINGLE_BASE, 0, size=14)
    _guided_top(cv, (0, L_DRAW))
    cv.dim((0, 0), (0, L_DRAW), "L", off=-70, label_off=-16)
    cv.math((0, L_DRAW / 2), "EI", 15, C["text"], "end", dx=-14)
    cv.math((0, L_DRAW / 2), f"K = {K_SINGLE:g}", 15, C["text"], "start", dx=14)
    return cv


def frame_panel():
    sx = 220
    cv = Canvas(PW, PH, sx=sx, ox=120, oy=110)
    cv.panel("鋼架", "CD 柱為靠桿")
    A, D = (0, 0), (LB_DRAW, 0)
    B, Cn = (0, L_DRAW), (LB_DRAW, L_DRAW)
    cv.line(A, B, C["member"], 4, cap="butt")
    cv.line(D, Cn, C["member"], 4, cap="butt")
    cv.line(B, Cn, C["member"], 9, cap="butt")                    # EI = ∞ 梁
    cv.support(A, A_KIND, 0, size=14)
    cv.support(D, D_KIND, 0, size=14)
    cv.dot(Cn, 7, fill="#FFFFFF", stroke=C["member"], w=2.6)       # C 鉸圓
    for p in (B, Cn):
        cv.arrow((p[0], p[1] + 0.32), (p[0], p[1] + 0.03), C["load"], 3.0, 11)
        cv.math((p[0], p[1] + 0.32), "P", 16, C["load"], "start", dx=10, weight="700")
    cv.math(((B[0] + Cn[0]) / 2, L_DRAW), "EI = ∞", 15, C["text"], dy=-20)
    for p, n, dx in ((A, "A", -16), (B, "B", -16), (Cn, "C", 18), (D, "D", 18)):
        cv.text(p, n, 15, C["text"], "middle", dx=dx, dy=-14 if p[1] else -8, weight="700")
    cv.math((0, L_DRAW / 2), "EI", 15, C["text"], "end", dx=-12)
    cv.math((0, L_DRAW / 2), "K = ?", 15, C["text"], "start", dx=12)
    cv.math((LB_DRAW, L_DRAW / 2), "EI", 15, C["text"], "start", dx=12)
    cv.dim(A, B, "L", off=-62, label_off=-16)
    cv.dim(A, D, "L_{b}", off=58, label_off=16)
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([single_panel(), frame_panel()], cols=2,
            title="SS-2008-2 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1、#2、#4–#10；只畫考卷所給條件",
            note="A、D 為鉸支；B 剛接、C 鉸接（CD 為靠桿）；梁 EI = ∞",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2008-2.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
import math
Q_K0 = K_SINGLE                      # AB 不計靠桿：鉸底＋頂不轉可移      §4 Step 1
Q_SUMP, Q_PI = 2.0, 1.0              # ΣP = 2P、P_I = P（以 P 為單位）    §4 Step 2
Q_KP = Q_K0 * math.sqrt(Q_SUMP / Q_PI)          # 2√2 = 2.83            §4 Step 3
Q_K_INV = Q_K0 * math.sqrt(Q_PI / Q_SUMP)       # 比值倒置的錯誤 1.41
Q_DL = 0.22                          # 繪圖用側移量


def _sway_ab(cv, base, top_load=True):
    pts = [(base[0] + Q_DL * math.sin(math.pi * t / 2), base[1] + L_DRAW * t) for t in [i / 40 for i in range(41)]]
    cv.poly(pts, C["member"], 4)
    cv.line(base, (base[0], base[1] + L_DRAW), C["ghost"], 2, dash="6 5")
    return (base[0] + Q_DL, base[1] + L_DRAW)


def fig2_sway():
    W1 = 520
    cv = Canvas(W1, PH, sx=225, ox=200, oy=105)
    cv.panel("① AB 單獨：K0 = 2.0", "鉸底、頂部隨剛梁平移但不轉")
    B1 = _sway_ab(cv, (0, 0))
    cv.support((0, 0), "pin", 0, size=14)
    _guided_top(cv, B1)
    cv.arrow((B1[0], B1[1] + 0.30), (B1[0], B1[1] + 0.04), C["load"], 3.0, 11)
    cv.text((B1[0], B1[1] + 0.30), "P", 15, C["load"], "start", dx=10, weight="700")
    cv.arrow((B1[0] + 0.02, B1[1] - 0.30), (B1[0] + 0.30, B1[1] - 0.30), C["sfd"], 2.6, 10)
    cv.text((B1[0] + 0.30, B1[1] - 0.30), "P·δ/L", 13.5, C["sfd"], "start", dx=8, weight="700")
    cv.dim((0, L_DRAW - 0.08), (Q_DL, L_DRAW - 0.08), "δ", off=0, label_off=-14)
    cv.text_px(W1 / 2, PH - 50, "抗側：AB 自身彎曲（柱身反曲）", 13, C["text"], weight="700")
    cv.text_px(W1 / 2, PH - 26, f"Pcr = π²EI/({Q_K0:g}L)²", 13, C["muted"])
    p1 = cv
    cv = Canvas(W1, PH, sx=210, ox=110, oy=110)
    cv.panel("② 加上靠桿 CD：兩柱同時側移 δ", "剛梁只平移；CD 兩端鉸，自身零抗側")
    A, D = (0, 0), (LB_DRAW, 0)
    B = _sway_ab(cv, A)
    Cn = (LB_DRAW + Q_DL, L_DRAW)
    cv.line(D, (LB_DRAW, L_DRAW), C["ghost"], 2, dash="6 5")
    cv.line(D, Cn, C["member"], 4, cap="butt")
    cv.line(B, Cn, C["member"], 9, cap="butt")
    cv.support(A, "pin", 0, size=14)
    cv.support(D, "pin", 0, size=14)
    cv.dot(Cn, 7, fill="#FFFFFF", stroke=C["member"], w=2.6)
    for p in (B, Cn):
        cv.arrow((p[0], p[1] + 0.32), (p[0], p[1] + 0.03), C["load"], 3.0, 11)
        cv.text((p[0], p[1] + 0.32), "P", 15, C["load"], "start", dx=10, weight="700")
    cv.arrow((Cn[0] + 0.03, Cn[1] - 0.14), (Cn[0] + 0.30, Cn[1] - 0.14), C["sfd"], 2.6, 10)
    cv.text((Cn[0] + 0.16, Cn[1] - 0.14), "P·δ/L", 13, C["sfd"], dy=18, weight="700")
    cv.arrow((B[0] + 0.03, B[1] - 0.14), (B[0] + 0.30, B[1] - 0.14), C["sfd"], 2.6, 10)
    cv.text((B[0] + 0.16, B[1] - 0.14), "P·δ/L", 13, C["sfd"], dy=18, weight="700")
    cv.text((0, L_DRAW / 2), "AB", 14, C["text"], "end", dx=-10, weight="700")
    cv.text((LB_DRAW + Q_DL / 2, L_DRAW / 2), "CD", 14, C["text"], "start", dx=12, weight="700")
    cv.text_px(W1 / 2, PH - 50, "AB 仍是唯一抗側者，卻要抵抗 2·P·δ/L", 13, C["text"], weight="700")
    cv.text_px(W1 / 2, PH - 26, "⇒ 每柱 P 只能到單獨時的一半", 13, C["muted"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-1-sway.svg")
    compose([p1, p2], cols=2,
            title="圖 1　側移挫屈：靠桿把自己的 P·δ/L 推給 AB",
            sub="B 端與不轉動的剛梁剛接，AB 才有抗側勁度；CD 的 P–Δ 全部轉由 AB 承擔",
            note="把 A 讀成固定、B 當自由端，K 也是 2.0，但抗側來源說錯；CD 不能計入 ΣPeK",
            path=path)
    return path


def fig3_kprime():
    W1, H1 = 1000, 540
    cv = Canvas(W1, H1, sx=1)
    cv.panel("LeMessurier：K' = K0 · √(ΣP / P_I)（AB 與 CD 同斷面、同長度）", "ΣP_eK 只計有抗側能力的柱；P_e 以 K = 1 計")
    X0, X1, YB, YT = 110, 620, 440, 110
    n0, n1, k0, k1 = 0.0, 4.0, 0.0, 4.5
    PX = lambda n: X0 + (X1 - X0) * (n - n0) / (n1 - n0)
    PY = lambda k: YB - (YB - YT) * (k - k0) / (k1 - k0)
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for n in range(0, 5):
        cv.text_px(PX(n), YB + 18, f"{n}", 11.5, C["muted"])
    for k in range(0, 5):
        cv.text_px(X0 - 8, PY(k), f"{k}", 11.5, C["muted"], "end")
        _hl(cv, H1, X0, PY(k), X1, PY(k), C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 42, "ΣP / P_I", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, "K'", 13, C["text"], "start", weight="700")
    ns = [n1 * i / 200 for i in range(1, 201)]
    cv.poly([(PX(n), H1 - PY(Q_K0 * math.sqrt(n))) for n in ns], C["bmd"], 2.8)
    pts = [(1.0, Q_K0, "忽略靠桿：2.0", C["muted"], -1, -14),
           (Q_SUMP / Q_PI, Q_KP, f"本題 K' = {Q_KP:.2f}", C["bmd"], 1, 24),
           (Q_PI / Q_SUMP, Q_K_INV, f"比值倒置：{Q_K_INV:.2f}", C["load"], 1, 24)]
    for n, k, lab, col, side, dy in pts:
        _hl(cv, H1, PX(n), YB, PX(n), PY(k), col, 1.2, dash="4 3")
        cv.dot((PX(n), H1 - PY(k)), 6, fill=col)
        cv.text_px(PX(n) + 10 * side, PY(k) + dy, lab, 12.5, col, "start" if side > 0 else "end", weight="700")
    xt = 660
    pe1 = math.pi ** 2 / Q_K0 ** 2
    rows = [(f"P_e = π²EI/L²；ΣP_eK = π²EI/({Q_K0:g}L)²", C["text"]),
            (f"K'² = (P_e/P)·(2P/ΣP_eK) = {Q_K0 ** 2:g} × 2 = {Q_KP ** 2:.0f}", C["text"]),
            (f"K' = √{Q_KP ** 2:.0f} = {Q_KP:.2f}", C["bmd"]),
            ("", C["text"]),
            ("每柱臨界 P：", C["text"]),
            (f"單獨 π²EI/4L² = {pe1:.3f} EI/L²", C["muted"]),
            (f"有靠桿 π²EI/8L² = {pe1 / 2:.3f} EI/L²（減半）", C["bmd"])]
    for i, (s, col) in enumerate(rows):
        if s:
            cv.text_px(xt, 150 + i * 32, s, 13, col, "start", weight="700" if col == C["bmd"] else "400")
    path = os.path.join(OUT, f"{TAG}-fig-2-kprime.svg")
    compose([cv], cols=1,
            title=f"圖 2　K' = 2.0 × √2 = {Q_KP:.2f}：同樣勁度扛兩倍 P–Δ，有效長度放大 √2 倍",
            sub="ΣP / P(AB) = 2P / P = 2",
            note="分子分母寫反得 1.41（K 反而變小，與物理相反）；把 CD 也放進 ΣPeK 則根號內出現 0 或 ∞",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "A 或單根柱底讀成固定端；B、C 的剛接／鉸接對調"),
    (fig2_sway, "§4 Step 1、Step 4",
     "誤以為靠桿 CD 自身能抗側；AB 抗側來源說成柱腳固定；忘了 CD 的 P–Δ 轉給 AB"),
    (fig3_kprime, "§4 Step 2–3",
     "ΣP/P_I 寫反得 1.41；漏掉靠桿只答 2.0；CD 算入 ΣP_eK"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
