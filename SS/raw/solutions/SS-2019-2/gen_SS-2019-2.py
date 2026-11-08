#!/usr/bin/env python3
"""
SS-2019-2 合成梁（實心 RC 版＋H500×200×10×16）正彎矩塑性強度 Mn — 題目附圖重繪腳本

用法：
    python3 gen_SS-2019-2.py [輸出目錄]

重繪依據：題目正本 SS-2019-2-problem.md §4 判讀清單（待確認）。
只畫考卷給的東西（版厚 150 mm、版直接擱在上翼板、H 型鋼直立），不含任何解題結果（不畫中性軸、應力塊）。
H 型鋼依 H500×200×10×16 按比例，版厚 150 mm 與鋼梁同比例。
示意部分：樓版左右截斷（有效寬度 2.5 m 遠大於圖幅，以斷裂線表示並以文字標註）、骨材點。
不重繪：無。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2019-2"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2019-2-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
T_SLAB = 150.0              # #1 實心版厚 150 mm，直接擱在上翼板頂面（無鋼承板、無托肩）
D, BF, TW, TF = 500.0, 200.0, 10.0, 16.0   # #3 H500×200×10×16 = d×bf×tw×tf（mm）
B_EFF = "2.5 m"             # 題文 有效寬度 2.5 m（圖上截斷示意）
HALF_SHOWN = 330.0          # 圖上顯示的半版寬（示意，mm）

PW, PH = 680, 680


def _rect(cv, x0, x1, y0, y1, fill, stroke, w=1.6, op=1.0):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, stroke, w, op)


def _break(cv, x, y0, y1):
    """斷裂線（Z 字）"""
    ym = (y0 + y1) / 2
    a = 14.0
    cv.poly([(x, y0 + 12), (x, ym + a), (x - a, ym), (x + a, ym), (x, ym - a), (x, y1 - 12)],
            C["member"], 1.6)


def section_panel():
    sx = 0.62
    cv = Canvas(PW, PH, sx=sx, ox=PW / 2 - 40, oy=80)
    cv.panel("合成梁斷面", "H 型鋼與版厚依比例；樓版左右截斷示意")
    yb = D                       # 版底＝上翼板頂
    yt = D + T_SLAB
    _rect(cv, -HALF_SHOWN, HALF_SHOWN, yb, yt, C["ghost"], "none", 0, 0.45)
    cv.line((-HALF_SHOWN, yb), (HALF_SHOWN, yb), C["member"], 2.0)
    cv.line((-HALF_SHOWN, yt), (HALF_SHOWN, yt), C["member"], 2.0)
    _break(cv, -HALF_SHOWN, yt, yb)
    _break(cv, HALF_SHOWN, yt, yb)
    for (x, y) in ((-280, 560), (-190, 600), (-90, 545), (30, 610), (120, 560), (220, 600), (290, 548)):
        cv.circle((x, y), 6, "none", C["member2"], 1.0)
    st = C["member"]
    _rect(cv, -BF / 2, BF / 2, D - TF, D, C["fill_c"], st)
    _rect(cv, -BF / 2, BF / 2, 0, TF, C["fill_c"], st)
    _rect(cv, -TW / 2, TW / 2, TF, D - TF, C["fill_c"], st)
    cv.dim((HALF_SHOWN, yb), (HALF_SHOWN, yt), f"{T_SLAB:.0f} mm", off=46, label_off=36,
           color=C["accent"])
    cv.text((0, yt), "混凝土樓版", 15, C["text"], dy=-22, weight="700")
    cv.text((0, yt), f"有效寬度 {B_EFF}（題文；圖幅截斷）", 12.5, C["muted"], dy=-44)
    cv.line((BF / 2 - 20, D / 2 + 60), (BF / 2 + 120, D / 2 + 60), C["muted"], 1.2)
    cv.line((TW / 2, D / 2 + 30), (BF / 2 - 20, D / 2 + 60), C["muted"], 1.2)
    cv.text((BF / 2 + 120, D / 2 + 60), "H500×200×10×16", 13, C["text"], "start", dx=4)
    cv.text((BF / 2 + 120, D / 2 + 60), "d×bf×tw×tf（mm）", 12, C["muted"], "start", dx=4, dy=18)
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([section_panel()], cols=1,
            title="SS-2019-2 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1、#3；只畫考卷所給條件",
            note="實心版直接擱在上翼板頂，無鋼承板、無托肩；版厚 150 mm",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2019-2.md §4，由下式即時算出（tf、cm）
# ══════════════════════════════════════════════════════════════
Q_TS = T_SLAB / 10                                   # 15
Q_D, Q_BF, Q_TW, Q_TF = D / 10, BF / 10, TW / 10, TF / 10
Q_BE, Q_FC, Q_FY = 250.0, 0.21, 2.5
Q_HW = Q_D - 2 * Q_TF                                # 46.8
Q_AS = 2 * Q_BF * Q_TF + Q_HW * Q_TW                 # 110.8
Q_T = Q_AS * Q_FY                                    # 277
Q_CMAX = 0.85 * Q_FC * Q_BE * Q_TS                   # 669.4
Q_A = round(Q_T / (0.85 * Q_FC * Q_BE), 2)           # 6.21（解析取兩位再往下算）
Q_YC = Q_A / 2                                       # 3.105
Q_YT = Q_TS + Q_D / 2                                # 40
Q_ARM = Q_YT - Q_YC                                  # 36.895
Q_MN = Q_T * Q_ARM                                   # 10,220 tf·cm


def fig1_pna():
    W1, H1 = 1120, 620
    cv = Canvas(W1, H1)
    cv.panel("T = 277 tf 小於版可提供 669.4 tf：PNA 在混凝土版內，鋼梁全斷面受拉",
             "混凝土應力塊深 a = 6.21 cm（版厚 15 cm 內）；版有效寬 250 cm，圖中截斷示意")
    TOP, S = 120.0, 6.0
    py = lambda d: TOP + d * S
    cx = 290.0
    half = 30.0
    # 版（截斷）
    _pR(cv, cx - half * S, py(0), cx + half * S, py(Q_TS), "#E8EBEF", C["member"], 1.4)
    _pR(cv, cx - half * S, py(0), cx + half * S, py(Q_A), "rgba(29,78,216,0.16)")
    for sx in (-1, 1):
        xe = cx + sx * half * S
        _pPL(cv, [(xe, py(0) - 6), (xe - 6 * sx, py(4)), (xe + 6 * sx, py(9)), (xe, py(Q_TS) + 6)], C["panel"], 7)
        _pPL(cv, [(xe, py(0) - 6), (xe - 6 * sx, py(4)), (xe + 6 * sx, py(9)), (xe, py(Q_TS) + 6)], C["member"], 1.3)
    _pL(cv, cx - half * S, py(Q_A), cx + half * S + 8, py(Q_A), C["accent"], 1.6, dash="8 3 2 3")
    _pT(cv, cx + half * S + 12, py(Q_A), "PNA", 12, C["accent"], "start", weight="700")
    _pT(cv, cx, py(Q_A / 2), f"a = {Q_A:.2f}", 12, C["compr"], weight="700")
    _pT(cv, cx, py(Q_TS) - 14, "be = 250 cm（截斷）", 11.5, C["muted"])
    # 鋼梁
    y0 = Q_TS
    _pR(cv, cx - Q_BF / 2 * S, py(y0), cx + Q_BF / 2 * S, py(y0 + Q_TF), C["fill_t"], C["member"], 1.4)
    _pR(cv, cx - Q_BF / 2 * S, py(y0 + Q_D - Q_TF), cx + Q_BF / 2 * S, py(y0 + Q_D), C["fill_t"], C["member"], 1.4)
    _pR(cv, cx - Q_TW / 2 * S, py(y0 + Q_TF), cx + Q_TW / 2 * S, py(y0 + Q_D - Q_TF), C["fill_t"], C["member"], 1.4)
    _pT(cv, cx + 60, py(y0 + Q_D / 2), "H500×200×10×16", 12, C["text"], "start", weight="700")
    _pT(cv, cx + 60, py(y0 + Q_D / 2) + 20, f"As = {Q_AS:.1f} cm²", 12, C["muted"], "start")
    # 刻度
    xl = cx - half * S - 40
    for d, lab in ((0, "0"), (Q_A, f"{Q_A:.2f}"), (Q_TS, "15"), (Q_YT, "40"), (Q_TS + Q_D, "65")):
        _pL(cv, xl, py(d), xl + 6, py(d), C["dim"], 1.2)
        _pT(cv, xl - 4, py(d), lab, 10.5, C["muted"], "end")
    _pL(cv, xl + 6, py(0), xl + 6, py(Q_TS + Q_D), C["dim"], 1.0)
    # 應力欄
    z = 560.0
    _pL(cv, z, py(0) - 10, z, py(Q_TS + Q_D) + 6, C["member2"], 1.2)
    _pR(cv, z - 40, py(0), z, py(Q_A), C["fill_c"], C["compr"], 1.4)
    _pR(cv, z, py(y0), z + 40, py(y0 + Q_D), C["fill_t"], C["tension"], 1.4)
    _pT(cv, z - 20, py(0) - 16, "0.85f'c", 12, C["compr"], weight="700")
    _pT(cv, z + 44, py(Q_YT), "Fy", 12, C["tension"], "start", weight="700")
    # 力偶
    xa = 660.0
    _pA(cv, xa + 50, py(Q_YC), xa, py(Q_YC), C["compr"], 3.0, 10)
    _pA(cv, xa, py(Q_YT), xa + 50, py(Q_YT), C["tension"], 3.0, 10)
    _pT(cv, xa + 58, py(Q_YC), f"C = {_fmt(Q_T, 0)} tf（距版頂 a/2 = {Q_YC:.3f}）", 12.5, C["compr"], "start", weight="700")
    _pT(cv, xa + 58, py(Q_YT), f"T = As·Fy = {_fmt(Q_T, 0)} tf（距版頂 ts + d/2 = {Q_YT:.0f}）", 12.5, C["tension"], "start", weight="700")
    _pL(cv, xa + 25, py(Q_YC) + 8, xa + 25, py(Q_YT) - 8, C["dim"], 1.3)
    _pT(cv, xa + 32, py((Q_YC + Q_YT) / 2), f"力臂 = 40 − {Q_YC:.3f} = {Q_ARM:.3f} cm", 13, C["text"], "start", weight="700")
    _pT(cv, xa, py(Q_TS + Q_D) - 30, f"Mn = 277 × {Q_ARM:.3f} = {_fmt(Q_MN, 0)} tf·cm = {_fmt(Q_MN / 100, 1)} tf·m", 14, C["bmd"], "start", weight="700")
    _pT(cv, xa, py(Q_TS + Q_D) - 4, f"（φbMn = 0.9 × {_fmt(Q_MN / 100, 1)} = {_fmt(0.9 * Q_MN / 100, 1)} tf·m）", 12, C["muted"], "start")
    path = os.path.join(OUT, f"{TAG}-fig-2-pna.svg")
    compose([cv], cols=1,
            title=f"圖 2　a = {Q_A:.2f} cm 小於 ts = 15 cm；Mn = T × 力臂 = {_fmt(Q_MN / 100, 1)} tf·m",
            sub="鋼梁形心距版頂 15 + 50/2 = 40 cm；混凝土合力在應力塊中點 a/2",
            note="力臂常見錯：用鋼梁深 d 或 d/2 + ts/2（把 PNA 當成在版中央）；或 a 用全版厚 15 cm",
            path=path)
    return path


def fig3_case():
    W1, H1 = 1100, 420
    cv = Canvas(W1, H1)
    cv.panel("先比鋼梁全拉 As·Fy 與版全壓 0.85f'c·be·ts，決定 PNA 在哪裡", "長條長度依力的比例（tf）")
    X0, sc = 260.0, 0.85
    rows = [("鋼梁全斷面降伏 T", Q_T, C["tension"], f"{_fmt(Q_T, 0)} = {Q_AS:.1f} × 2.5"),
            ("版全厚受壓 Cmax", Q_CMAX, C["compr"], f"{_fmt(Q_CMAX, 1)} = 0.85 × 0.21 × 250 × 15")]
    for i, (nm, v, col, s) in enumerate(rows):
        y = 140 + i * 60
        _pT(cv, X0 - 14, y, nm, 13, C["text"], "end", weight="700")
        cv.rect_px(X0, y - 16, sc * v, 32, col, 3)
        _pT(cv, X0 + sc * v + 12, y, s, 12.5, col, "start", weight="700")
    _pL(cv, X0 + sc * Q_T, 110, X0 + sc * Q_T, 236, C["tension"], 1.2, dash="4 3")
    _pT(cv, X0 + sc * Q_T + 6, 250, f"版只需用到 {Q_T / Q_CMAX * 100:.0f}% 厚度 → a = {Q_A:.2f} cm", 12.5, C["accent"], "start", weight="700")
    cases = [("T ≤ Cmax", "PNA 在版內（本題）", "鋼梁全拉，a = T / (0.85f'c·be)", C["bmd"]),
             ("T > Cmax", "PNA 在鋼梁內", "版全壓，鋼梁上部也受壓，再分翼板／腹板", C["muted"])]
    for i, (c1, c2, c3, col) in enumerate(cases):
        x = 120 + i * 470
        cv.rect_px(x, 290, 420, 84, "#FFFFFF", 8, col, 1.4)
        _pT(cv, x + 16, 312, c1, 13.5, col, "start", weight="700")
        _pT(cv, x + 120, 312, c2, 13, C["text"], "start", weight="700")
        _pT(cv, x + 16, 346, c3, 12, C["muted"], "start")
    path = os.path.join(OUT, f"{TAG}-fig-1-case.svg")
    compose([cv], cols=1,
            title=f"圖 1　T = {_fmt(Q_T, 0)} tf 小於 Cmax = {_fmt(Q_CMAX, 1)} tf：PNA 落在混凝土版內",
            sub="完全合成作用；剪力釘足夠，C = T 由版與鋼梁之間的水平剪力傳遞",
            note="答案卷要先寫出這個比較，「a 小於 ts、PNA 在版內」的假設才有根據",
            path=path)
    return path



FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "誤加鋼承板肋高或托肩；把 H500×200×10×16 的 10、16 對調（tw、tf 讀反）"),
    (fig1_pna, "§4 Step 3–5",
     "力臂用 d 或 d/2 + ts/2；a 取全版厚；漏乘 0.85"),
    (fig3_case, "§4 Step 2",
     "未比較 As·Fy 與 0.85f'c·be·ts 就假設 PNA 位置"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
