#!/usr/bin/env python3
"""
SS-2003-2 混凝土包覆型鋼合成柱 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2003-2.py [輸出目錄]

重繪依據：題目正本 SS-2003-2-problem.md §4 判讀清單（2026-11-02 已確認）與 §1 題文
（H312×303×13×21）。混凝土外廓與型鋼依比例；鋼筋位置考卷未標，僅示意四角。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2003-2"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2003-2-problem.md §4，已確認）；單位 mm
# ══════════════════════════════════════════════════════════
B, H = 500.0, 600.0                     # #1 混凝土寬 500（水平）× 高 600（垂直）
D, BF, TW, TF = 312.0, 303.0, 13.0, 21.0   # §1 題文 H312×303×13×21；#2 翼板水平、腹板垂直、置中
N_BAR = 4                               # #4 4 根 D32，四角各 1 根
COVER_SKETCH = 55.0                     # 鋼筋位置示意用（考卷未標，非題給）


def _rect(cv, x0, x1, y0, y1, fill, stroke=C["member"], w=1.6):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, stroke, w)


def fig1_problem():
    W, Hc, sx = 520, 540, 0.56
    cv = Canvas(W, Hc, sx=sx, ox=W / 2 + 20, oy=Hc / 2 - 30)
    cv.panel("合成柱斷面", "混凝土與型鋼依比例；鋼筋位置示意")
    _rect(cv, -B / 2, B / 2, -H / 2, H / 2, C["border"], C["member"], 2.0)
    _rect(cv, -BF / 2, BF / 2, D / 2 - TF, D / 2, C["member"], C["member"])
    _rect(cv, -BF / 2, BF / 2, -D / 2, -D / 2 + TF, C["member"], C["member"])
    _rect(cv, -TW / 2, TW / 2, -D / 2 + TF, D / 2 - TF, C["member"], C["member"])
    c = COVER_SKETCH
    for sxg in (-1, 1):
        for syg in (-1, 1):
            cv.dot((sxg * (B / 2 - c), syg * (H / 2 - c)), 6.5, fill=C["text"], stroke=C["text"], w=1)
    cv.dim((-B / 2, H / 2), (B / 2, H / 2), f"{B:.0f} mm", off=-24, label_off=-14)
    cv.dim((-B / 2, -H / 2), (-B / 2, H / 2), f"{H:.0f} mm", off=-28, label_off=-34)
    cv.text_px(W / 2, Hc - 26, "H312×303×13×21 置中；4 根 D32 於四角", 12.5, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title="SS-2003-2 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1、#2、#4；只畫考卷所給條件",
            note="強軸（水平軸）挫屈沿 600 mm 方向、弱軸挫屈沿 500 mm 方向",
            path=path)
    return path


# ── 解題圖解共用小工具（像素座標；y 由上往下）──
def _hl(cv, PH, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line((x0, PH - y0), (x1, PH - y1), color, w, dash=dash, cap="butt")


def rsum(terms, nd=3):
    """與解析相同的加法：各項先四捨五入到 nd 位再相加"""
    return round(sum(terms), nd)   # 本題採精確加總（Fmy = 6.934）


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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2003-2.md §1／§4，由下式即時算出
# ══════════════════════════════════════════════════════════════
import math
Q_B, Q_H = B / 10, H / 10                     # 50、60 cm
Q_AS, Q_AR = 165.0, 4 * 8.14                  # cm²                          §4 步驟 1
Q_AC = Q_B * Q_H - Q_AS - Q_AR
Q_FY, Q_FYR, Q_FC, Q_EC = 3.5, 4.2, 0.280, 250.0   # t/cm²                   §1
Q_C1, Q_C2, Q_C3 = 0.7, 0.6, 0.2              # 考卷式之係數
Q_FMY_T = [Q_FY, Q_C1 * Q_FYR * Q_AR / Q_AS, Q_C2 * Q_FC * Q_AC / Q_AS]
Q_FMY = sum(Q_FMY_T)                          # 6.934                        步驟 2
Q_EM_T = [2100.0, Q_C3 * Q_EC * Q_AC / Q_AS]
Q_EM = sum(Q_EM_T)                            # 2949                         步驟 3
Q_RY, Q_RX = 7.7, 13.4                        # 型鋼 r                        §1
Q_RMY, Q_RMX = max(Q_RY, 0.3 * Q_B), max(Q_RX, 0.3 * Q_H)   # 15.0、18.0     步驟 4
Q_KL = 0.8 * 1500
def q_phipn(r):
    lam = Q_KL / (math.pi * r) * math.sqrt(Q_FMY / Q_EM)
    fcr = math.exp(-0.419 * lam ** 2) * Q_FMY if lam <= 1.5 else 0.877 / lam ** 2 * Q_FMY
    return lam, fcr, 0.85 * Q_AS * fcr
Q_OK = q_phipn(Q_RMY)                         # 513 t                        步驟 5–6
Q_WRONG = q_phipn(Q_RY)                       # 誤用型鋼 ry


def fig1_rm():
    W1, H1 = 520, 560
    sx = 6.0
    cv = Canvas(W1, H1, sx=sx, ox=W1 / 2, oy=300)
    cv.panel("① SRC 斷面（依比例）", "型鋼 H312×303×13×21 置中，四角 D32")
    def rect(x0, x1, y0, y1, fill, st=C["member"], w=1.4):
        cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, st, w)
    rect(-Q_B / 2, Q_B / 2, -Q_H / 2, Q_H / 2, "rgba(148,163,184,0.25)", C["member"], 1.8)
    d, bf, tw, tf = D / 10, BF / 10, TW / 10, TF / 10
    rect(-bf / 2, bf / 2, d / 2 - tf, d / 2, C["fill_c"], C["compr"])
    rect(-bf / 2, bf / 2, -d / 2, -d / 2 + tf, C["fill_c"], C["compr"])
    rect(-tw / 2, tw / 2, -d / 2 + tf, d / 2 - tf, C["fill_c"], C["compr"])
    c = COVER_SKETCH / 10
    for sxg in (-1, 1):
        for syg in (-1, 1):
            cv.circle((sxg * (Q_B / 2 - c), syg * (Q_H / 2 - c)), 1.6, fill=C["text"], stroke=C["text"], w=1)
    cv.dim((-Q_B / 2, -Q_H / 2), (Q_B / 2, -Q_H / 2), f"{Q_B:g} cm", off=26, label_off=16, size=12)
    cv.dim((Q_B / 2, -Q_H / 2), (Q_B / 2, Q_H / 2), f"{Q_H:g}", off=26, label_off=18, size=12)
    cv.text_px(W1 / 2, H1 - 30, f"強軸挫屈沿 {Q_H:g} cm 方向、弱軸挫屈沿 {Q_B:g} cm 方向", 12.5, C["muted"])
    p1 = cv
    cv = Canvas(W1, H1, sx=1)
    cv.panel("② rm 取型鋼 r 與 0.3 × 全厚的較大者（cm）", "兩個方向都由 0.3 × 全厚控制")
    x0, sc = 170, 14.0
    rows = (("繞弱軸：型鋼 ry", Q_RY, C["ghost"]), ("0.3 × 50", 0.3 * Q_B, C["bmd"]),
            ("繞強軸：型鋼 rx", Q_RX, C["ghost"]), ("0.3 × 60", 0.3 * Q_H, C["bmd"]))
    for i, (nm, v, col) in enumerate(rows):
        y = 140 + i * 62 + (24 if i >= 2 else 0)
        cv.text_px(x0 - 12, y, nm, 13, C["text"], "end")
        cv.rect_px(x0, y - 14, sc * v, 28, col, 4)
        cv.text_px(x0 + sc * v + 8, y, f"{v:.1f}" + (" ← rm" if col == C["bmd"] else ""), 13, col if col == C["bmd"] else C["muted"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 56, f"KL = 0.8 × 1500 = {Q_KL:.0f} cm；KL/rmy = {Q_KL / Q_RMY:.1f}（控制）", 13, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, f"誤用型鋼 ry = {Q_RY}：KL/r = {Q_KL / Q_RY:.1f}", 12.5, C["load"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-1-rm.svg")
    compose([p1, p2], cols=2,
            title=f"圖 1　修正迴轉半徑：rmy = {Q_RMY:.1f}、rmx = {Q_RMX:.1f} cm",
            sub="考卷第 1 項：型鋼的迴轉半徑不得小於合成斷面沿挫屈平面全厚度的 30%",
            note="包覆混凝土把型鋼「撐」在較大的斷面裡——這條規定讓 r 由 7.7 提到 15.0，細長比幾乎減半",
            path=path)
    return path


def fig2_strength():
    W1, H1 = 520, 520
    cv = Canvas(W1, H1, sx=1)
    cv.panel("① 修正強度與修正模數的組成", "混凝土與鋼筋折算到型鋼斷面上")
    x0, sc = 150, 44.0
    _stack_row(cv, x0, 160, sc, Q_FMY_T, [C["compr"], C["load"], C["ghost"]], "Fmy（t/cm²）", C["text"])
    cv.legend(x0 - 120, 210, [(C["compr"], f"型鋼 Fy = {Q_FY}"), (C["load"], f"鋼筋 0.7Fyr·Ar/As = {Q_FMY_T[1]:.3f}"),
                              (C["ghost"], f"混凝土 0.6fc'·Ac/As = {Q_FMY_T[2]:.3f}")], size=12, gap=20)
    sc2 = 0.1
    cv.rect_px(x0, 330, sc2 * Q_EM_T[0], 30, C["compr"], 0)
    cv.rect_px(x0 + sc2 * Q_EM_T[0], 330, sc2 * Q_EM_T[1], 30, C["ghost"], 0)
    cv.text_px(x0 - 12, 345, "Em（t/cm²）", 14, C["text"], "end", weight="700")
    cv.text_px(x0 + sc2 * Q_EM + 10, 345, f"= {Q_EM:,.0f}", 14, C["text"], "start", weight="700")
    cv.text_px(W1 / 2, 400, f"2100 + 0.2 × {Q_EC:g} × {Q_AC:.2f}/{Q_AS:g} = {Q_EM:,.0f}", 12.5, C["muted"])
    cv.text_px(W1 / 2, H1 - 30, f"Ac = {Q_AC:.2f} cm²、Ar = {Q_AR:.2f} cm²、As = {Q_AS:g} cm²", 12, C["muted"])
    p1 = cv
    cv = Canvas(W1, H1, sx=1)
    cv.panel("② φcPn = 0.85 As Fcr（t）", "rm 的取法決定答案")
    x0, sc = 170, 0.55
    rows = ((f"用 rm = {Q_RMY:.1f}", Q_OK, C["bmd"]), (f"誤用 ry = {Q_RY}", Q_WRONG, C["ghost"]))
    for i, (nm, (lam, fcr, p), col) in enumerate(rows):
        y = 160 + i * 110
        cv.text_px(x0 - 12, y, nm, 13.5, C["text"], "end", weight="700")
        cv.rect_px(x0, y - 17, sc * p, 34, col, 4)
        cv.text_px(x0 + sc * p + 8, y, f"{p:.0f}", 14, col if i == 0 else C["muted"], "start", weight="700")
        cv.text_px(x0, y + 32, f"λc = {lam:.3f}，Fcr = {fcr:.3f}" + ("（非彈性）" if lam <= 1.5 else "（彈性）"), 12,
                   C["muted"], "start")
    cv.text_px(W1 / 2, H1 - 56, f"差 {Q_OK[2] / Q_WRONG[2]:.1f} 倍", 14, C["load"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, f"強軸 rmx = {Q_RMX:.1f}：φcPn = {q_phipn(Q_RMX)[2]:.0f} t，不控制", 12.5, C["muted"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-2-strength.svg")
    compose([p1, p2], cols=2,
            title=f"圖 2　Fmy = {Q_FMY:.3f}、Em = {Q_EM:,.0f} ⇒ φcPn = {Q_OK[2]:.0f} t",
            sub="公式代換：Ag → As、r → rm、Fy → Fmy、E → Em；Pn 只乘型鋼面積 As",
            note="漏掉 0.3 × 全厚的規定，細長比會從 80 變成 156、落入彈性挫屈段，強度只剩三成",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "500／600 mm 方向對調（r_m 下限取錯邊）；鋼筋根數讀錯"),
    (fig1_rm, "§4 步驟 4–5",
     "直接用型鋼 ry = 7.7（漏用 0.3 × 全厚）；全厚度方向（50／60）對調"),
    (fig2_strength, "§4 步驟 2–3、6",
     "Pn 乘總面積；Fmy、Em 漏項；誤用 ry 使強度只剩約三成"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
