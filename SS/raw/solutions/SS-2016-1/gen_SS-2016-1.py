#!/usr/bin/env python3
"""
SS-2016-1 梁柱翼板、腹板寬厚比 λp、λr 的差異與制定因素 — 解題圖解腳本

用法：
    python3 gen_SS-2016-1.py [輸出目錄]

本題考卷無附圖（題目正本 SS-2016-1-problem.md §3）；本腳本只產生解題圖解。
係數全部取自題表（SS-2016-1.md §1）；k 值取自 §4（一）。觀念題，圖中不代入任何 Fy。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2016-1"

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
# 解題圖解（2026-11-03 補繪）——係數取自題表（SS-2016-1.md §1）與 §4
# ══════════════════════════════════════════════════════════════
Q_ROWS = [  # 名稱、λp 係數（None = 不適用）、λr 係數、顏色
    ("梁翼板（彎曲）", 17, 25, C["compr"]),
    ("柱翼板（純壓）", 16, 25, C["compr"]),
    ("梁腹板（彎曲）", 170, 260, C["bmd"]),
    ("柱腹板（均勻壓）", None, 68, C["load"]),
]


def _q_plate(cv, x0, y0, w, h, sup_top, sup_bot, stress, label, sub, color):
    """受壓平板：上下長邊的支撐狀態、左右載重邊的應力分布（stress: 'uniform' 或 'bend'）"""
    _pR(cv, x0, y0, x0 + w, y0 + h, "#E6EAF0", C["member"], 1.4)
    for sup, yy, sgn in ((sup_top, y0, -1), (sup_bot, y0 + h, 1)):
        if sup:
            _pL(cv, x0, yy, x0 + w, yy, C["member"], 4.0)
            for i in range(10):
                xx = x0 + 8 + i * (w - 16) / 9
                _pL(cv, xx, yy, xx - 7, yy + sgn * 8, C["member"], 1.2)
        else:
            _pL(cv, x0, yy, x0 + w, yy, C["load"], 1.6, dash="6 4")
            _pT(cv, x0 + w / 2, yy + sgn * 12, "自由邊", 11.5, C["load"], weight="700")
    n = 7
    for side in (-1, 1):
        xe = x0 if side < 0 else x0 + w
        for i in range(n):
            t = i / (n - 1)
            yy = y0 + 6 + t * (h - 12)
            if stress == "uniform":
                L = 26.0
            else:
                L = 30.0 * (1 - 2 * t)
            if abs(L) < 3:
                continue
            if L > 0:   # 壓：箭頭指向板
                _pA(cv, xe + side * (L + 4), yy, xe + side * 3, yy, C["compr"], 1.8, 6)
            else:       # 拉：箭頭離開板
                _pA(cv, xe + side * 3, yy, xe + side * (-L + 4), yy, C["tension"], 1.8, 6)
    _pT(cv, x0 + w / 2, y0 - 46, label, 13.5, color, weight="700")
    _pT(cv, x0 + w / 2, y0 - 28, sub, 11.5, C["muted"])


def fig1_plates():
    W1, H1 = 1140, 540
    cv = Canvas(W1, H1)
    cv.panel("λr 由「邊界條件 × 壓應力分布」決定：同類受力的肢材，λr 相同",
             "粗線＋斜線 = 有支撐的長邊；虛線 = 自由邊；藍箭頭 = 壓、紅箭頭 = 拉")
    w, h = 230.0, 120.0
    xs = (80.0, 450.0, 820.0)
    y0 = 170.0
    _q_plate(cv, xs[0], y0, w, h, False, True, "uniform", "(a) 翼板突出肢：梁、柱相同", "一邊接腹板、一邊自由；均勻受壓", C["compr"])
    _q_plate(cv, xs[1], y0, w, h, True, True, "bend", "(b) 梁腹板", "兩邊接翼板；上壓下拉（應力梯度）", C["bmd"])
    _q_plate(cv, xs[2], y0, w, h, True, True, "uniform", "(c) 柱腹板", "兩邊接翼板；全高均勻受壓", C["load"])
    rows = [
        (xs[0], ["未加勁肢材", "梁翼板外緣應力沿寬度近乎均勻", "→ 與柱翼板同一挫屈模式", "λr = 25/√Fy（梁柱相同）"], C["compr"]),
        (xs[1], ["加勁肢材，只有上半受壓", "k 由均勻壓約 4 提高到約 23.9", "受拉側再提供拘束", "λr = 260/√Fy"], C["bmd"]),
        (xs[2], ["加勁肢材，全寬受壓", "k 約 4（均勻壓）", "挫屈臨界應力低得多", "λr = 68/√Fy"], C["load"]),
    ]
    for x, ls, col in rows:
        for i, s in enumerate(ls):
            last = i == len(ls) - 1
            _pT(cv, x + w / 2, y0 + h + 50 + i * 30 + (10 if last else 0), s,
                15 if last else 12.5, col if last else C["text"], weight="700" if last else "400")
    _pT(cv, W1 / 2, H1 - 40, "λr ∝ √(k) × √(E/Fy)：k 越大、容許寬厚比越大；梁腹板 260 約為柱腹板 68 的 3.8 倍", 13, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-1-plates.svg")
    compose([cv], cols=1,
            title="圖 1　翼板 λr 梁柱相同、腹板 λr 梁大於柱：差在壓應力分布，不在構材名稱",
            sub="(a) 梁翼板與柱翼板受力模式相同；(b)(c) 同為兩邊支撐，梁腹板一半受拉，挫屈係數 k 大幅提高",
            note="常見錯：以為梁翼板也有應力梯度而 λr 不同；或把梁腹板 λr 大歸因於腹板較厚",
            path=path)
    return path


def fig2_limits():
    PW1, PH1 = 570, 520
    a = Canvas(PW1, PH1)
    a.panel("(a) 題表係數：λp 一律小於 λr", "長條長度 = 係數（÷√Fy 前）；淺色段 = λp 到 λr 的非結實區")
    X0, sc = 190.0, 1.25
    for i, (nm, lp, lr, col) in enumerate(Q_ROWS):
        y = 140 + i * 82
        _pT(a, X0 - 12, y, nm, 12.5, C["text"], "end", weight="700")
        if lp:
            a.rect_px(X0, y - 13, sc * lp, 26, col, 3)
            a.rect_px(X0 + sc * lp, y - 13, sc * (lr - lp), 26, C["ghost"], 3)
            _pT(a, X0 + sc * lp, y + 26, f"λp {lp}", 11.5, col)
        else:
            a.rect_px(X0, y - 13, sc * lr, 26, C["ghost"], 3)
            _pT(a, X0 + 8, y + 26, "λp 不適用（受壓構材只看 λr）", 11.5, C["muted"], "start")
        _pT(a, X0 + sc * lr + 8, y, f"λr {lr}", 12.5, col, "start", weight="700")
    _pT(a, PW1 / 2, PH1 - 40, "翼板 17 對 25、腹板 170 對 260：λp 約為 λr 的 0.64～0.68", 12, C["muted"])
    b = Canvas(PW1, PH1)
    b.panel("(b) λp 與 λr 劃出的三段", "Mn 對寬厚比 λ 的示意（不代數值）")
    X0, X1, Y0, Y1 = 90.0, 530.0, 420.0, 130.0
    lp, lr = 0.32, 0.62
    gx = lambda t: X0 + t * (X1 - X0)
    _pL(b, X0, Y0, X1, Y0, C["member"], 1.4)
    _pL(b, X0, Y0, X0, Y1 - 10, C["member"], 1.4)
    yMp, yMr = Y1 + 20, Y1 + 120
    _pPL(b, [(X0, yMp), (gx(lp), yMp), (gx(lr), yMr)], C["bmd"], 2.8)
    ts = [lr + i * (1 - lr) / 30 for i in range(31)]
    _pPL(b, [(gx(t), yMr + (Y0 - 30 - yMr) * (1 - (lr / t) ** 2) / (1 - (lr / 1.0) ** 2)) for t in ts], C["load"], 2.4, dash="7 4")
    for t, s in ((lp, "λp"), (lr, "λr")):
        _pL(b, gx(t), Y0, gx(t), Y1 - 4, C["muted"], 1.0, dash="3 3")
        _pT(b, gx(t), Y0 + 18, s, 13, C["text"], weight="700")
    _pT(b, X0 - 8, yMp, "Mp", 12.5, C["bmd"], "end", weight="700")
    _pT(b, X0 - 8, yMr, "Mr", 12.5, C["compr"], "end", weight="700")
    _pL(b, X0, yMr, gx(lr), yMr, C["compr"], 1.0, dash="3 3")
    zones = [((X0 + gx(lp)) / 2, "結實", "達 Mp 且有", "轉動能力（約 3～4 倍）"),
             ((gx(lp) + gx(lr)) / 2, "非結實", "降伏前不局部挫屈", "但塑性轉動不足"),
             ((gx(lr) + X1) / 2, "細長", "彈性局部挫屈", "先於降伏")]
    for x, t1, t2, t3 in zones:
        yz = Y1 + 70 if t1 == "細長" else Y0 - 90
        _pT(b, x, yz, t1, 13, C["text"], weight="700")
        _pT(b, x, yz + 20, t2, 11, C["muted"])
        _pT(b, x, yz + 36, t3, 11, C["muted"])
    _pT(b, (X0 + X1) / 2, Y0 + 44, "寬厚比 λ", 12.5, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-2-limits.svg")
    compose([a, b], cols=2,
            title="圖 2　λr：降伏前不得局部挫屈；λp：還要撐到塑性鉸轉動完成，所以更嚴",
            sub="λr 考慮肢材種類、應力分布、邊界條件、殘留應力、Fy；λp 另加塑性轉動能力、應變硬化與試驗校正",
            note="兩者都正比於 1/√Fy（彈性挫屈應力 ∝ E(t/b)²）；高強度鋼的寬厚比限制較嚴",
            path=path)
    return path


FIGURES = [
    (fig1_plates, "§4（一）",
     "以為梁翼板有應力梯度；把梁腹板 λr 大歸因於厚度或構材名稱"),
    (fig2_limits, "§4（二）",
     "λp、λr 物理意義混淆；漏列殘留應力、轉動能力、Fy 等因素"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
