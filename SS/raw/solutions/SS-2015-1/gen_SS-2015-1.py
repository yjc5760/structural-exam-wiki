#!/usr/bin/env python3
"""
SS-2015-1 簡支鋼梁三分點載重之 BH 斷面選擇、剪力與撓度檢核（LRFD）— 題目附圖重繪腳本

用法：
    python3 gen_SS-2015-1.py [輸出目錄]

重繪依據：題目正本 SS-2015-1-problem.md §4 判讀清單（待確認）。
只重繪圖 1(a)（簡支梁和斷面）；只畫考卷給的東西，不含任何解題結果（不標所選 BH 斷面）。
梁跨度依比例（3@2.8 m）；載重箭頭長度、梁高為示意；右側 BH 斷面為符號示意（H、B、tw、tf 為所求斷面之代號）。
不重繪：圖 1(b) 梁設計彎矩強度曲線（設計圖表，曲線讀值已照錄於 problem.md §2）、第 3 頁參考公式。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2015-1"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2015-1-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
NSEG, SEG = 3, 2.8          # 圖 1(a) 3@2.8 = 8.4 m
SPAN = NSEG * SEG
LOAD_AT = (1, 2)            # 題文 三分點各受 P_D、P_L
BRACE_AT = (0, 1, 2, 3)     # #1 側撐在兩支承與兩載重點（⊗）
#                             題文 P_D = 22 tf、P_L = 35 tf（圖上只標符號，數值照題文另列）
PD, PL = 22, 35

PW, PH = 640, 420


def _otimes(cv, p, r=7):
    x, y = cv.P(p)
    m = C["accent"]
    cv.parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#FFFFFF" stroke="{m}" stroke-width="1.8"/>')
    d = r * 0.7
    for sx_, sy_ in ((1, 1), (1, -1)):
        cv.parts.append(f'<line x1="{x-d*sx_:.1f}" y1="{y-d*sy_:.1f}" x2="{x+d*sx_:.1f}" y2="{y+d*sy_:.1f}" '
                        f'stroke="{m}" stroke-width="1.6"/>')


def beam_panel():
    sx = (PW - 140) / SPAN
    cv = Canvas(PW, PH, sx=sx, ox=70, oy=170)
    cv.panel("簡支梁", "左端鉸支、右端滾支；三分點受集中載重")
    h = 0.32                    # 梁高（示意）
    cv.polygon([(0, 0), (SPAN, 0), (SPAN, h), (0, h)], C["fill_c"], C["member"], 1.8)
    cv.support((0, 0), "pin", 0, size=14)
    cv.support((SPAN, 0), "roller", 0, size=14)
    for k in LOAD_AT:
        x = k * SEG
        cv.arrow((x, h + 2.0), (x, h + 0.05), C["load"], 2.6, 10)
        cv.math((x, h + 2.0), "P_{D}", 15, C["load"], "end", dx=-8, dy=6, weight="700")
        cv.math((x, h + 1.2), "P_{L}", 15, C["load"], "end", dx=-8, dy=6, weight="700")
    for k in BRACE_AT:
        _otimes(cv, (k * SEG, h / 2))
    _otimes(cv, (SPAN - 1.6, h + 1.7))
    cv.text((SPAN - 1.6, h + 1.7), "：側撐", 13, C["accent"], "start", dx=10)
    cv.text_px(PW / 2, 88, f"題文：P_D = {PD} tf、P_L = {PL} tf（各三分點）", 12.5, C["muted"])
    cv.dim((0, 0), (SPAN, 0), f"3@{SEG} = {SPAN:.1f} m", off=56, label_off=16)
    return cv


def section_panel():
    cv = Canvas(PW, PH, sx=1.0, ox=0, oy=0)
    cv.panel("斷面（符號示意）", "BH H×B×tw×tf，單位：mm")
    cx, top, bot = PW / 2 - 20, PH - 110, 110      # 像素座標排版（y 向上）
    B, TF, TW = 150, 18, 12
    for xa, xb, ya, yb in ((cx - B / 2, cx + B / 2, top - TF, top), (cx - B / 2, cx + B / 2, bot, bot + TF),
                           (cx - TW / 2, cx + TW / 2, bot + TF, top - TF)):
        cv.polygon([(xa, ya), (xb, ya), (xb, yb), (xa, yb)], C["fill_c"], C["member"], 1.6)
    cv.dim((cx + B / 2, bot), (cx + B / 2, top), "H", off=36, label_off=16)
    cv.dim((cx - B / 2, bot), (cx + B / 2, bot), "B", off=30, label_off=16)
    cv.dim((cx - B / 2, top - TF), (cx - B / 2, top), "t_{f}", off=-26, label_off=-16)
    cv.arrow((cx - 50, (top + bot) / 2), (cx - TW / 2 - 1, (top + bot) / 2), C["dim"], 1.2, 8)
    cv.arrow((cx + 50, (top + bot) / 2), (cx + TW / 2 + 1, (top + bot) / 2), C["dim"], 1.2, 8)
    cv.math((cx - 54, (top + bot) / 2), "t_{w}", 15, C["dim"], "end")
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([beam_panel(), section_panel()], cols=2,
            title="SS-2015-1 題目附圖 1(a)（重繪）",
            sub="依題目正本判讀清單 #1；只畫考卷所給條件；圖 1(b) 設計彎矩強度曲線不重繪",
            note="⊗ 側撐在兩支承與兩載重點：每段無側撐長度都是一個三分段",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2015-1.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
import math
Q_FY, Q_E = 2.52, 2040.0                 # tf/cm²
Q_PU = 1.2 * PD + 1.6 * PL               # 82.4 tf
Q_MU = Q_PU * SEG                        # 230.72 tf·m
Q_LB = SEG                               # 2.8 m
Q_SECS = [(870, 350, 16, 25, 240), (920, 300, 19, 25, 247), (826, 350, 16, 28, 251), (820, 400, 16, 25, 254),
          (610, 350, 19, 45, 325), (600, 400, 19, 40, 329), (500, 500, 25, 40, 396)]   # H、bf、tw、tf（mm）、kg/m（圖 1(b)）


def q_sec(h, b, tw, tf):
    H, B, TW, TF = h / 10, b / 10, tw / 10, tf / 10
    hw = H - 2 * TF
    A = 2 * B * TF + hw * TW
    zx = B * TF * (H - TF) + TW * hw * hw / 4
    iy = TF * B ** 3 / 6 + hw * TW ** 3 / 12
    ry = math.sqrt(iy / A)
    lp = 80 * ry / math.sqrt(Q_FY) / 100
    ix = 2 * (B * TF ** 3 / 12 + B * TF * (hw / 2 + TF / 2) ** 2) + TW * hw ** 3 / 12
    return dict(A=A, zx=zx, phimp=0.9 * Q_FY * zx / 100, lp=lp, ix=ix, hw=hw, tw=TW)


Q_TAB = [(s, q_sec(*s[:4])) for s in Q_SECS]
Q_PICK = next(s for s, p in Q_TAB if p["phimp"] >= Q_MU and p["lp"] >= Q_LB)
Q_PP = q_sec(*Q_PICK[:4])
Q_VN = 0.9 * 0.6 * Q_FY * Q_PP["hw"] * Q_PP["tw"]        # 224.9
Q_DL = 23 * PL * (SPAN * 100) ** 3 / (648 * Q_E * Q_PP["ix"])   # 0.892 cm
Q_DA = SPAN * 100 / 360


def fig1_select():
    W1, H1 = 1000, 540
    cv = Canvas(W1, H1, sx=1)
    cv.panel("七個候選斷面依單位重排序：φbMp 與 Lp", f"需求 Mu = {Q_MU:.2f} tf·m、Lb = {Q_LB} m（Lb ≤ Lp 才能用 φbMp）")
    x0, sc, m0 = 330, 22.0, 220.0
    for i, (s, p) in enumerate(Q_TAB):
        y = 130 + i * 50
        ok = p["phimp"] >= Q_MU and p["lp"] >= Q_LB
        pick = s == Q_PICK
        lab = f"{s[4]} kg/m　BH {s[0]}×{s[1]}×{s[2]}×{s[3]}"
        cv.text_px(x0 - 12, y, lab, 12.5, C["load"] if pick else C["text"], "end", weight="700" if pick else "400")
        w = sc * (p["phimp"] - m0)
        cv.rect_px(x0, y - 13, w, 26, C["load"] if pick else (C["bmd"] if ok else C["ghost"]), 3)
        tag = "✓ 最輕合格" if pick else ("✓（較重）" if ok else "不足")
        cv.text_px(max(x0 + w, x0 + sc * (Q_MU - m0)) + 10, y, f"{p['phimp']:.2f}　Lp {p['lp']:.2f} m　{tag}", 12, C["load"] if pick else (C["muted"] if ok else C["load"]), "start", weight="700" if pick or not ok else "400")
    xm = x0 + sc * (Q_MU - m0)
    _hl(cv, H1, xm, 105, xm, 130 + 6 * 50 + 22, C["accent"], 1.6, dash="5 4")
    cv.text_px(xm, 130 + 6 * 50 + 40, f"Mu = {Q_MU:.2f}", 12.5, C["accent"], weight="700")
    for v in (220, 225, 230, 235):
        cv.text_px(x0 + sc * (v - m0), 112, f"{v}", 11, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-1-select.svg")
    compose([cv], cols=1,
            title=f"圖 1　依重量逐一檢核：240 kg/m 差 {Q_MU - Q_TAB[0][1]['phimp']:.2f}，247 kg/m（BH 920×300×19×25）是最輕合格斷面",
            sub="長條長度 = φbMp − 220（tf·m）；七條曲線在 Lb = 2.8 m 都還在塑性平台",
            note="從圖面高低挑、或 240 不合格後直接跳 251，都會漏掉 247；247 的 Lp = 3.02 m 只比 Lb 多 0.22 m",
            path=path)
    return path


def fig2_checks():
    W1, H1 = 1000, 470
    cv = Canvas(W1, H1, sx=1)
    cv.panel(f"BH {Q_PICK[0]}×{Q_PICK[1]}×{Q_PICK[2]}×{Q_PICK[3]} 的三項檢核（使用率）", "彎矩、剪力、活載撓度 L/360")
    x0, sc = 300, 480.0
    rows = [("彎矩 Mu / φbMn", Q_MU / Q_PP["phimp"], f"{Q_MU:.2f} / {Q_PP['phimp']:.2f}"),
            ("剪力 Vu / φvVn", Q_PU / Q_VN, f"{Q_PU:.1f} / {Q_VN:.1f}"),
            ("撓度 δL / (L/360)", Q_DL / Q_DA, f"{Q_DL:.3f} / {Q_DA:.2f} cm")]
    for i, (lab, r, s) in enumerate(rows):
        y = 150 + i * 80
        cv.text_px(x0 - 12, y, lab, 13, C["text"], "end", weight="700")
        cv.rect_px(x0, y - 15, sc, 30, "rgba(46,125,50,0.10)", 3, stroke=C["ghost"], sw=1)
        cv.rect_px(x0, y - 15, sc * r, 30, C["load"] if r > 0.9 else C["bmd"], 3)
        cv.text_px(x0 + sc + 10, y, f"{r * 100:.1f}%（{s}）", 12.5, C["text"], "start", weight="700")
    _hl(cv, H1, x0 + sc, 120, x0 + sc, 390, C["accent"], 1.4, dash="5 4")
    cv.text_px(x0 + sc, 410, "1.0", 12, C["accent"])
    cv.text_px(W1 / 2, H1 - 28, f"δ = 23PL³/648EI，P = PL = {PL} tf、Ix ≈ {round(Q_PP['ix'], -2):,.0f} cm⁴；剪力腹板 h/tw = {Q_PP['hw'] / Q_PP['tw']:.1f} 小於 70.4 → 無剪力挫屈", 12.5, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-2-checks.svg")
    compose([cv], cols=1,
            title=f"圖 2　彎矩使用率 {Q_MU / Q_PP['phimp'] * 100:.1f}% 控制；剪力 {Q_PU / Q_VN * 100:.1f}%、撓度 {Q_DL / Q_DA * 100:.1f}% 都很寬裕",
            sub=f"Pu = 1.2 × {PD} + 1.6 × {PL} = {Q_PU:.1f} tf；兩載重點間為等彎矩段 Mu = Pu × L/3",
            note="撓度只用活載 PL（不乘係數）；三分點兩集中力的係數是 23/648，不是單一集中力的 1/48",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "漏看載重點的 ⊗ 側撐而以全跨 8.4 m 查圖 1(b)；P_D、P_L 誤當只作用一點"),
    (fig1_select, "§4 Step 2",
     "依圖面高低挑斷面；240 不合格後跳過 247；忘了確認 Lb ≤ Lp"),
    (fig2_checks, "§4 Step 1、3、4",
     "撓度用係數化載重或 PL³/48EI；剪力 Aw 定義混淆"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
