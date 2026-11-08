#!/usr/bin/env python3
"""
SS-2025-2 三面圍銲疊接受拉桿件之寬度 L — 題目附圖重繪腳本

用法：
    python3 gen_SS-2025-2.py [輸出目錄]

重繪依據：題目正本 SS-2025-2-problem.md §4 判讀清單（2026-11-02 已確認）。
只畫考卷給的東西；L 為待求符號，連接板外形與桿件長度為示意。單位 cm。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2025-2"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2025-2-problem.md §4，已確認）
# ══════════════════════════════════════════════════════════
L_OV = 3.0          # #2 疊接長＝縱向銲道長 3 cm
L_SYM = 8.0         # #3 桿件寬 L（符號；繪圖用寬度）
#                     #1 三面圍銲：上、下緣各 3 cm，端面一道長 L；#4 桿件厚 2 cm、連接板厚 1 cm


def fig1_problem():
    W, H, sx = 760, 460, 14
    cv = Canvas(W, H, sx=sx, ox=360, oy=H / 2 - 20)
    cv.panel("銲接結合", "連接板外形與桿件長度示意")
    gu = [(0, -6.5), (0, 6.5), (16, 11), (16, -11)]
    cv.polygon(gu, C["border"], C["member"], 1.8)
    h = L_SYM / 2
    cv.polygon([(-14, -h), (L_OV, -h), (L_OV, h), (-14, h)], C["fill_c"], C["member"], 1.8)
    for y in (-h, h):
        cv.line((0, y), (L_OV, y), C["load"], 5, cap="butt")
    cv.line((L_OV, -h), (L_OV, h), C["load"], 5, cap="butt")
    cv.arrow((-14.5, 0), (-19, 0), C["load"], 3.2, 12)
    cv.math((-19, 0), "P", 16, C["load"], "end", dx=-8, weight="700")
    cv.arrow((16.5, 0), (21, 0), C["load"], 3.2, 12)
    cv.math((21, 0), "P", 16, C["load"], "start", dx=8, weight="700")
    cv.text((-7, 0), "受拉桿件（厚 2 cm）", 13, C["text"], weight="700")
    cv.text((10, 5.5), "連接板（厚 1 cm）", 13, C["text"], weight="700")
    cv.dim((0, h), (L_OV, h), f"{L_OV:g} cm", off=-44, label_off=-14)
    cv.dim((L_OV, -h), (L_OV, h), "L", off=34, label_off=14)
    cv.text((L_OV / 2, -h), "三面圍銲（紅）", 12.5, C["load"], dy=22, weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title="SS-2025-2 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#4；L 為待求",
            note="銲道沿上緣 3 cm、端面 L、下緣 3 cm 三面圍銲；3 cm 為疊接長",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2025-2.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
Q_FY, Q_FU = 2.5, 4.1                    # tf/cm²
Q_T = 2.0                                # 桿件厚 cm（#4）
Q_LW = L_OV                              # 縱向銲道長 l = 3 cm


def q_u(w):
    """容許應力規範 §4.3：板類僅兩側縱向銲道；超出範圍回傳 None"""
    if Q_LW >= 2 * w:
        return 1.00
    if Q_LW >= 1.5 * w:
        return 0.87
    if Q_LW >= w:
        return 0.75
    return None


def q_p(w):
    u = q_u(w)
    gy = 0.6 * Q_FY * Q_T * w
    nsf = 0.5 * Q_FU * u * Q_T * w if u else None
    return u, gy, nsf


Q_LMAX = Q_LW
f2 = lambda v: f"{v + 1e-9:.2f}"           # 四捨五入顯示（9.225 → 9.23，與解析同）
Q_U3, Q_GY3, Q_NSF3 = q_p(Q_LMAX)
Q_PV = 0.4 * Q_FY * 2 * Q_LW * Q_T                     # 12.0
Q_PMAX = min(Q_GY3, Q_NSF3, Q_PV)


def fig1_pl():
    W1, H1 = 1000, 540
    cv = Canvas(W1, H1, sx=1)
    cv.panel("容許拉力 P 隨桿寬 L 變化（l = 3 cm 固定）", "U 隨 l/w 分段：l ≥ 2w → 1.00；≥ 1.5w → 0.87；≥ w → 0.75；l 小於 w 不允許")
    X0, X1, YB, YT = 100, 640, 450, 110
    lmax, pmax = 4.0, 12.0
    PX = lambda l: X0 + (X1 - X0) * l / lmax
    PY = lambda p: YB - (YB - YT) * p / pmax
    for a, b, u, col in ((0, 1.5, "U = 1.00", "rgba(46,125,50,0.10)"), (1.5, 2.0, "0.87", "rgba(46,125,50,0.18)"),
                         (2.0, 3.0, "U = 0.75", "rgba(46,125,50,0.26)"), (3.0, 4.0, "不允許", "rgba(192,57,43,0.12)")):
        cv.rect_px(PX(a), YT, PX(b) - PX(a), YB - YT, col, 0)
        cv.text_px((PX(a) + PX(b)) / 2, YT + 16, u, 12, C["load"] if u == "不允許" else C["bmd"], weight="700")
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for v in (0, 1.0, 1.5, 2.0, 3.0, 4.0):
        cv.text_px(PX(v), YB + 18, f"{v:g}", 11.5, C["muted"])
    for v in range(0, 13, 3):
        cv.text_px(X0 - 8, PY(v), f"{v}", 11.5, C["muted"], "end")
    cv.text_px((X0 + X1) / 2, YB + 42, "桿寬 L（cm）", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, "P（tf）", 13, C["text"], "start", weight="700")
    ls = [Q_LMAX * i / 300 for i in range(1, 301)]
    cv.poly([(PX(l), H1 - PY(q_p(l)[1])) for l in ls], C["compr"], 2.8)
    for a, b in ((0.0001, 1.5), (1.5001, 2.0), (2.0001, 3.0)):
        seg = [a + (b - a) * i / 40 for i in range(41)]
        cv.poly([(PX(l), H1 - PY(q_p(l)[2])) for l in seg], C["load"], 2.4, dash="7 4")
    cv.dot((PX(Q_LMAX), H1 - PY(Q_GY3)), 6.5, fill=C["bmd"])
    cv.text_px(PX(Q_LMAX) - 10, PY(Q_GY3) - 14, f"L = {Q_LMAX:g}：P = {Q_GY3:.2f} tf", 12.5, C["bmd"], "end", weight="700")
    cv.legend(X0 + 14, YT + 40, [(C["compr"], "全斷面降伏 0.6Fy·2L = 3.0L"), (C["load"], "淨斷面斷裂 0.5Fu·U·2L = 4.1UL")], size=12, gap=19)
    xt = 680
    rows = [("L", "U", "P(GY)", "P(NSF)")]
    for l in (1.0, 1.5, 2.0, 3.0):
        u, gy, nsf = q_p(l)
        rows.append((f"{l:g}", f"{u:.2f}", f2(gy), f2(nsf)))
    for i, r in enumerate(rows):
        for c, v in enumerate(r):
            cv.text_px(xt + c * 72, 150 + i * 30, v, 12.5, C["text"], weight="700" if i == 0 else "400")
    cv.text_px(xt - 10, 150 + 6 * 30, "每段 P(NSF) 都大於 P(GY)", 12.5, C["muted"], "start")
    cv.text_px(xt - 10, 150 + 7 * 30, "⇒ 全程降伏控制，P 隨 L 遞增", 12.5, C["muted"], "start")
    cv.text_px(xt - 10, 150 + 8 * 30, f"⇒ L 取上限 {Q_LMAX:g} cm（L ≤ l）", 13, C["bmd"], "start", weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-pl.svg")
    compose([cv], cols=1,
            title=f"圖 1　L 有「最大值」：L ≤ l = {Q_LW:g} cm；P = 3.0L 單調遞增，L = {Q_LMAX:g} 時 P = {Q_GY3:.2f} tf",
            sub="U 是階梯函數，不能對 L 微分求極值",
            note="以為 L 愈小愈好（求最小值）、或把 L 超過 3 cm 也代 U = 0.75，都是錯的",
            path=path)
    return path


def fig2_check():
    W1, H1 = 1000, 420
    cv = Canvas(W1, H1, sx=1)
    cv.panel(f"L = {Q_LMAX:g} cm 的三項檢核（tf）", f"Ag = 2 × {Q_LMAX:g} = {Q_T * Q_LMAX:g} cm²，U = {Q_U3}（l/w = 1.0），Ae = {Q_U3 * Q_T * Q_LMAX:.1f} cm²")
    x0, sc = 330, 40
    rows = [("全斷面降伏 0.6Fy·Ag", Q_GY3), ("淨斷面斷裂 0.5Fu·Ae", Q_NSF3), ("銲道旁母材剪斷 0.4Fy·Av", Q_PV)]
    for i, (lab, v) in enumerate(rows):
        y = 150 + i * 70
        ctrl = v == Q_PMAX
        cv.text_px(x0 - 12, y, lab, 13, C["text"], "end", weight="700")
        cv.rect_px(x0, y - 15, sc * v, 30, C["load"] if ctrl else C["ghost"], 3)
        cv.text_px(x0 + sc * v + 8, y, f2(v) + ("（控制）" if ctrl else ""), 13, C["load"] if ctrl else C["muted"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 40, f"Pmax = min({f2(Q_GY3)}, {f2(Q_NSF3)}, {Q_PV:.1f}) = {Q_PMAX:.2f} tf（全斷面降伏控制）", 14, C["bmd"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-2-check.svg")
    compose([cv], cols=1,
            title=f"圖 2　Lmax = {Q_LMAX:g} cm：Pmax = {Q_PMAX:.2f} tf，全斷面降伏控制",
            sub="ASD：Ft = 0.6Fy（毛面積）、0.5Fu（有效淨面積）、Fv = 0.4Fy",
            note="淨斷面斷裂 9.23 只比降伏大 3%；U 若誤取 1.0 會以為斷裂更不控制",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "漏看端面橫向銲道；把 3 cm 當成桿件寬或端距"),
    (fig1_pl, "§4 Step 2–4",
     "把 L 當成有最小值；對階梯 U 微分；L 超過 l 仍取 U = 0.75"),
    (fig2_check, "§4 Step 5–6",
     "U 取 1.0；淨斷面用 0.6Fy；漏檢核銲道旁母材"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
