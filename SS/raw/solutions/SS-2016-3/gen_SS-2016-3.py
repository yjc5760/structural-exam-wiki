#!/usr/bin/env python3
"""
SS-2016-3 矩形板殘餘應力分布 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2016-3.py [輸出目錄]

重繪依據：題目正本 SS-2016-3-problem.md §4 判讀清單（2026-11-02 已確認）。
只重繪圖 1（斷面與殘餘應力分布）；圖 2 為材料應力–應變曲線，屬曲線圖，不重繪。
b、t 為符號，比例示意；三段寬度與應力大小依圖面數值。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2016-3"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2016-3-problem.md §4，已確認）
# ══════════════════════════════════════════════════════════
B_DRAW, T_DRAW = 3.0, 0.45    # #1 單一實心矩形板，寬 b、厚 t（繪圖比例）
SEG = [("壓", 0.25), ("拉", 0.25), ("壓", 0.25)]   # #2 三段各 b/3；#3 左右 F_y/4 壓、中段 F_y/4 拉，塊狀
SIG_DRAW = 1.6                # F_y/4 對應的繪圖高度


def fig1_problem():
    W, H, sx = 640, 520, 140
    cv = Canvas(W, H, sx=sx, ox=(W - B_DRAW * sx) / 2, oy=185)
    cv.panel("圖 1　斷面與殘餘應力", "b、t 比例示意；基線上方為壓、下方為拉")
    y0 = 1.25
    cv.polygon([(0, y0), (B_DRAW, y0), (B_DRAW, y0 + T_DRAW), (0, y0 + T_DRAW)],
               C["border"], C["member"], 1.8)
    cv.dim((B_DRAW, y0), (B_DRAW, y0 + T_DRAW), "t", off=24, label_off=14)
    cv.dim((0, y0), (B_DRAW, y0), "b", off=18, label_off=14)
    seg = B_DRAW / len(SEG)
    cv.line((-0.15, 0), (B_DRAW + 0.15, 0), C["muted"], 1.4)
    for k, (kind, frac) in enumerate(SEG):
        x0, x1 = k * seg, (k + 1) * seg
        h = SIG_DRAW * frac / 0.25 * 0.38
        y1 = h if kind == "壓" else -h
        col, fill = (C["compr"], C["fill_c"]) if kind == "壓" else (C["tension"], C["fill_t"])
        cv.polygon([(x0, 0), (x1, 0), (x1, y1), (x0, y1)], fill, col, 1.8)
        cv.text(((x0 + x1) / 2, y1 / 2), f"（{kind}）", 12.5, col, dx=18, weight="700")
        cv.math(((x0 + x1) / 2, y1 / 2), "F_{y}/4", 14, col, "end", dx=-4)
        cv.dim((x0, y1 if kind == "拉" else 0), (x1, y1 if kind == "拉" else 0), "b/3",
               off=34 if kind == "拉" else -0, label_off=16)
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title="SS-2016-3 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#3；圖 2 應力–應變曲線不重繪",
            note="圖面數值不自平衡：壓力合力為拉力合力的 2 倍（判讀清單 #4）",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2016-3.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
import math
Q_FY, Q_E = 2.5, 2040.0                     # tf/cm²（§4 (四) 已知）
Q_FR = Q_FY / 4                             # 殘留應力 ±Fy/4（照圖，不自平衡）
Q_FPL = Q_FY - Q_FR                         # 1.875：兩側整塊降伏
Q_IR = (1 / 3) ** 3                         # 兩側降伏後 Ie/I = 1/27
Q_LR1 = math.pi * math.sqrt(Q_E / Q_FPL)    # 103.6
Q_LR2 = Q_LR1 * math.sqrt(Q_IR)             # 19.9
Q_FMAX = Q_FPL + (Q_FY + Q_FR - Q_FPL) / 3          # 中間塊（原拉 Fy/4）再加 1.25 才降伏 → 平均 +0.417 = 2.29
Q_LR3 = math.pi * math.sqrt(Q_E * Q_IR / Q_FMAX)  # 18.0
Q_LR_FY = math.pi * math.sqrt(Q_E * Q_IR / Q_FY)  # 17.3（上限直接取 Fy 的算法）


def q_fcr(lr):
    fe = math.pi ** 2 * Q_E / lr ** 2
    if fe <= Q_FPL:
        return fe
    if fe * Q_IR >= Q_FMAX:
        return Q_FMAX
    return max(Q_FPL, fe * Q_IR)


def _stage(title, sub, f_avg):
    """三塊（各 b/3）在平均外加應力 f_avg 時的應力；壓為正"""
    W1, H1 = 340, 430
    cv = Canvas(W1, H1, sx=1)
    cv.panel(title, sub)
    x0, w, yb, sc = 30, 90, 300, 62
    res = [Q_FR, -Q_FR, Q_FR]
    if f_avg <= Q_FPL:
        s = [r + f_avg for r in res]
    else:
        s = [Q_FY, -Q_FR + Q_FPL + 3 * (f_avg - Q_FPL), Q_FY]
    _hl(cv, H1, x0, yb, x0 + 3 * w, yb, C["muted"], 1.4)
    _hl(cv, H1, x0, yb - sc * Q_FY, x0 + 3 * w, yb - sc * Q_FY, C["load"], 1.2, dash="5 4")
    cv.text_px(x0 + 3 * w + 4, yb - sc * Q_FY, "Fy", 12, C["load"], "start", weight="700")
    for k, v in enumerate(s):
        yld = abs(v - Q_FY) < 1e-9
        col = C["load"] if yld else (C["compr"] if v >= 0 else C["sfd"])
        top = yb - sc * v
        cv.rect_px(x0 + k * w + 3, min(top, yb), w - 6, abs(sc * v), col, 2)
        cv.text_px(x0 + k * w + w / 2, min(top, yb) - 12 if v >= 0 else yb + abs(sc * v) + 14, f"{v:+.3f}".replace("+", ""), 12, col, weight="700")
        cv.text_px(x0 + k * w + w / 2, H1 - 36, "降伏" if yld else "彈性", 12, C["load"] if yld else C["bmd"], weight="700")
    return cv


def fig1_stage():
    ps = [_stage("① 只有殘留應力", "兩側 Fy/4 壓、中間 Fy/4 拉", 0.0),
          _stage(f"② F = {Q_FPL:.3f}", "兩側同時整塊降伏", Q_FPL),
          _stage(f"③ F = {Q_FMAX:.2f}", "中間塊也降伏（全斷面）", Q_FMAX)]
    path = os.path.join(OUT, f"{TAG}-fig-1-stage.svg")
    compose(ps, cols=3,
            title=f"圖 1　比例限 F_PL = Fy − Fy/4 = {Q_FPL:.3f}；兩側降伏後只剩中間 b/3 彈性，Ie/I = (1/3)³ = 1/27",
            sub="F 為外力造成的平均應力 P/A；壓應力向上為正（tf/cm²）",
            note=f"兩側降伏後，平均應力每增加 1，中間塊增加 3：再加 {Q_FY + Q_FR - Q_FPL:.2f} 才降伏，對應平均應力 +{(Q_FY + Q_FR - Q_FPL) / 3:.3f}",
            path=path)
    return path


def fig2_curve():
    W1, H1 = 1000, 560
    cv = Canvas(W1, H1, sx=1)
    cv.panel("Fcr 對 L/r（強軸，K = 1，切線模數理論）", f"Fy = {Q_FY}、E = {Q_E:g} tf/cm²；殘留應力 ±Fy/4")
    X0, X1, YB, YT = 100, 680, 460, 110
    lmax, fmax = 200.0, 3.0
    PX = lambda l: X0 + (X1 - X0) * l / lmax
    PY = lambda f: YB - (YB - YT) * f / fmax
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for v in range(0, 201, 50):
        cv.text_px(PX(v), YB + 18, f"{v}", 11.5, C["muted"])
    for v in (0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
        cv.text_px(X0 - 8, PY(v), f"{v:.1f}", 11.5, C["muted"], "end")
        _hl(cv, H1, X0, PY(v), X1, PY(v), C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 42, "L/r", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, "Fcr（tf/cm²）", 13, C["text"], "start", weight="700")
    ls = [lmax * i / 600 for i in range(1, 601)]
    cv.poly([(PX(l), H1 - PY(min(math.pi ** 2 * Q_E / l ** 2, fmax))) for l in ls if math.pi ** 2 * Q_E / l ** 2 < 2.95], C["ghost"], 1.8, dash="6 4")
    pts = [(PX(0), H1 - PY(Q_FMAX))] + [(PX(l), H1 - PY(q_fcr(l))) for l in ls]
    cv.poly(pts, C["bmd"], 3)
    _hl(cv, H1, X0, PY(Q_FY), X1, PY(Q_FY), C["load"], 1.2, dash="5 4")
    cv.text_px(X1, PY(Q_FY) - 10, "Fy = 2.5", 12, C["load"], "end")
    for l, f, lab, dx, dy, anc in ((Q_LR3, Q_FMAX, f"({Q_LR3:.1f}, {Q_FMAX:.2f})", 10, -14, "start"),
                                   (Q_LR2, Q_FPL, f"({Q_LR2:.1f}, {Q_FPL:.3f})", 6, 22, "start"),
                                   (Q_LR1, Q_FPL, f"({Q_LR1:.1f}, {Q_FPL:.3f})", 8, -14, "start")):
        cv.dot((PX(l), H1 - PY(f)), 5.5, fill=C["accent"])
        cv.text_px(PX(l) + dx, PY(f) + dy, lab, 12, C["accent"], anc, weight="700")
    cv.text_px(PX(60), PY(Q_FPL) - 16, "平台：Fcr = 0.75Fy", 12.5, C["bmd"], weight="700")
    cv.text_px(PX(150), PY(1.1), "Euler π²E/(L/r)²", 12.5, C["muted"], "start")
    xt = 720
    rows = [("三段：", C["text"], "700"),
            (f"L/r ≤ {Q_LR3:.1f}：全斷面降伏 {Q_FMAX:.2f}", C["text"], "400"),
            (f"{Q_LR3:.1f}–{Q_LR2:.1f}：π²E/[27(L/r)²]", C["text"], "400"),
            (f"{Q_LR2:.1f}–{Q_LR1:.1f}：平台 {Q_FPL:.3f}", C["bmd"], "700"),
            (f"L/r ≥ {Q_LR1:.1f}：Euler", C["text"], "400"),
            ("", C["text"], "400"),
            (f"上限若寫 Fy = 2.5 → 對應 {Q_LR_FY:.1f}", C["muted"], "400"),
            ("差 Fy/12 = 0.21：題圖殘留應力不自平衡", C["muted"], "400")]
    for i, (s, col, wt) in enumerate(rows):
        if s:
            cv.text_px(xt, 140 + i * 32, s, 12.5, col, "start", weight=wt)
    path = os.path.join(OUT, f"{TAG}-fig-2-curve.svg")
    compose([cv], cols=1,
            title=f"圖 2　Fcr–L/r：比例限 {Q_FPL:.3f} 以下為 Euler，L/r {Q_LR2:.1f}–{Q_LR1:.1f} 整段被壓在平台",
            sub="兩側整塊同時降伏，強軸勁度一次掉到 1/27，所以中間細長比直接在比例限挫屈",
            note="殘留應力對中等細長比影響最大；極長柱仍是 Euler，極短柱接近全斷面降伏",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把斷面讀成 H 型鋼；把壓、拉段位置對調；忽略圖面數值不自平衡"),
    (fig1_stage, "§4 (四) 步驟 1、3、4",
     "比例限取 Fy 而忘了扣殘留應力；強軸 Ie/I 寫成 1/3（漏三次方）；中間塊降伏所需增量不乘 3"),
    (fig2_curve, "§4 (四) 步驟 2–5",
     "曲線畫成平滑過渡、漏掉 1.875 平台；三個轉折點算錯；以為長柱也受殘留應力影響"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
