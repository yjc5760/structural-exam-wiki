#!/usr/bin/env python3
"""
SS-2019-4 組合斷面蓋板之斷續填角銲（LRFD，剪力流）— 題目附圖重繪腳本

用法：
    python3 gen_SS-2019-4.py [輸出目錄]

重繪依據：題目正本 SS-2019-4-problem.md §4 判讀清單（待確認）。
只畫考卷附圖所示：H500×200×9×16 上翼板頂面疊 PL25×300，鋼板底面與翼板兩側邊緣交角各一道填角銲，
銲接符號 8 ▷ L-150（基線上下對稱）。
斷面依比例（題文尺寸）；銲道三角形放大示意（實際銲腳 8 mm）。L 為所求，符號照考卷寫「L」。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2019-4"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2019-4-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
D, BF, TW, TF = 500.0, 200.0, 9.0, 16.0   # 題文 H500×200×9×16
TP, BP = 25.0, 300.0                      # 題文 PL25×300（圖上標 300 mm）
WS = "8"                                  # #2 填角銲腳長 8 mm
PITCH = "L-150"                           # #2 每段長 L（所求）－中心距 150 mm，上下對稱（鏈式）
#                                           #1 銲道：鋼板底面與翼板左右兩側邊緣交角各一道
W_DRAW = 16.0                             # 銲道三角形繪製尺寸（放大示意，實際 8 mm）

PW, PHT = 820, 730


def _rect(cv, x0, x1, y0, y1, fill=C["fill_c"], w=1.8):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, C["member"], w)


def panel():
    sx = 0.95
    cv = Canvas(PW, PHT, sx=sx, ox=300, oy=60)
    cv.panel("組合斷面", "H500×200×9×16 ＋ PL25×300（上翼板頂面）")
    _rect(cv, -BF / 2, BF / 2, 0, TF)
    _rect(cv, -TW / 2, TW / 2, TF, D - TF)
    _rect(cv, -BF / 2, BF / 2, D - TF, D)
    _rect(cv, -BP / 2, BP / 2, D, D + TP, "rgba(180,83,9,0.16)")
    for sg in (-1, 1):                        # 填角銲：鋼板底面 × 翼板側緣
        x = sg * BF / 2
        cv.polygon([(x, D), (x + sg * W_DRAW, D), (x, D - W_DRAW)], C["member"], C["member"], 1)
    cv.dim((-BP / 2, D + TP), (BP / 2, D + TP), "300 mm", off=-30, label_off=-16, size=16)
    # 銲接符號：箭頭指右側銲道
    m = C["text"]
    tx, ty = cv.P((BF / 2 + W_DRAW * 0.45, D - W_DRAW * 0.45))
    kx, ky = tx + 70, ty + 75
    cv.parts.append(f'<line x1="{kx:.1f}" y1="{ky:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{m}" stroke-width="1.5"/>')
    ang = math.atan2(ty - ky, tx - kx)
    hl, hw = 11, 4
    pts = [(tx, ty), (tx - hl * math.cos(ang) + hw * math.sin(ang), ty - hl * math.sin(ang) - hw * math.cos(ang)),
           (tx - hl * math.cos(ang) - hw * math.sin(ang), ty - hl * math.sin(ang) + hw * math.cos(ang))]
    cv.parts.append(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{m}"/>')
    cv.parts.append(f'<line x1="{kx:.1f}" y1="{ky:.1f}" x2="{kx + 210:.1f}" y2="{ky:.1f}" stroke="{m}" stroke-width="1.5"/>')
    x0 = kx + 62
    for sg in (-1, 1):
        cv.parts.append(f'<polygon points="{x0:.1f},{ky:.1f} {x0:.1f},{ky + sg * 15:.1f} {x0 + 15:.1f},{ky:.1f}" '
                        f'fill="#FFFFFF" stroke="{m}" stroke-width="1.5"/>')
        cv.text_px(x0 - 8, ky + sg * 13, WS, 17, m, "end")
        cv.text_px(x0 + 22, ky + sg * 13, PITCH, 17, m, "start")
    cv.text_px(PW - 24, PHT - 34, "黑色三角＝填角銲（放大示意）", 12.5, C["muted"], "end")
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([panel()], cols=1,
            title="SS-2019-4 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1、#2；斷面依比例，銲道三角形放大示意；L 為所求",
            note="兩道銲在鋼板底面與翼板側緣交角；L-150 為每段長 L、中心距 150 mm，基線上下對稱＝兩側並列",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2019-4.md §4，由下式即時算出
# 座標：y 自 H 型鋼底面向上（cm），x 自斷面中線
# ══════════════════════════════════════════════════════════════
import math
Q_HD, Q_BF, Q_TW, Q_TF = 50.0, 20.0, 0.9, 1.6        # H500×200×9×16           §1
Q_BP, Q_TP = 30.0, 2.5                               # 蓋板 PL25×300           §1
Q_VU, Q_S, Q_W = 50.0, 15.0, 0.8                     # tf、cm、cm              §1
Q_AH = 2 * Q_BF * Q_TF + (Q_HD - 2 * Q_TF) * Q_TW    # 106.12                  Step 1
Q_AP = Q_BP * Q_TP
Q_YH, Q_YPL = Q_HD / 2, Q_HD + Q_TP / 2
Q_YB = (Q_AH * Q_YH + Q_AP * Q_YPL) / (Q_AH + Q_AP)  # 35.87                   Step 2
Q_IH = (Q_BF * Q_HD ** 3 - (Q_BF - Q_TW) * (Q_HD - 2 * Q_TF) ** 3) / 12
Q_I  = Q_IH + Q_AH * (Q_YH - Q_YB) ** 2 + Q_BP * Q_TP ** 3 / 12 + Q_AP * (Q_YPL - Q_YB) ** 2   # Step 3
Q_DP = Q_YPL - Q_YB
Q_Q  = Q_AP * Q_DP                                   # 1153.5                  Step 4
Q_QF = Q_VU * Q_Q / Q_I                              # 0.7638 tf/cm            Step 5
Q_FS = Q_QF * Q_S                                    # 11.46                   Step 6
Q_TE = 0.707 * Q_W
Q_RW = 2 * 0.75 * 0.6 * 4.9 * Q_TE                   # 2.494 tf/cm（兩道）     Step 7
Q_LREQ = Q_FS / Q_RW                                 # 4.59                    Step 8
Q_LUSE = math.ceil(Q_LREQ)
Q_Q_WRONG = Q_AP * (Q_YPL - Q_YH)                    # 誤：以 H 形心算 Q


def fig1_section():
    W1, H1 = 1000, 600
    sx = 8.0
    cv = Canvas(W1, H1, sx=sx, ox=300, oy=95)
    cv.panel("組合斷面（依比例，cm）", "蓋板以兩道 8 mm 填角銲斷續銲於上翼板")
    def rect(x0, x1, y0, y1, fill, st=C["member"], w=1.4):
        cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, st, w)
    rect(-Q_BF / 2, Q_BF / 2, 0, Q_TF, "rgba(63,74,90,0.18)")
    rect(-Q_BF / 2, Q_BF / 2, Q_HD - Q_TF, Q_HD, "rgba(63,74,90,0.18)")
    rect(-Q_TW / 2, Q_TW / 2, Q_TF, Q_HD - Q_TF, "rgba(63,74,90,0.18)")
    rect(-Q_BP / 2, Q_BP / 2, Q_HD, Q_HD + Q_TP, C["fill_m"], C["bmd"], 2.0)
    for sg in (-1, 1):
        x = sg * Q_BF / 2
        cv.polygon([(x, Q_HD), (x + sg * 1.4, Q_HD), (x, Q_HD - 1.4)], C["load"], C["load"], 1.0)
    cv.line((-Q_BP / 2 - 6, Q_YB), (Q_BP / 2 + 6, Q_YB), C["accent"], 2.2, dash="7 4")
    cv.text_px(cv.X(-Q_BP / 2 - 6) - 6, cv.Y(Q_YB), f"組合中性軸 {Q_YB:.2f}", 12.5, C["accent"], "end", weight="700")
    cv.line((-Q_BP / 2 - 6, Q_YH), (Q_BP / 2 + 6, Q_YH), C["ghost"], 1.2, dash="10 4 2 4")
    cv.text_px(cv.X(-Q_BP / 2 - 6) - 6, cv.Y(Q_YH), f"H 型鋼形心 {Q_YH:g}", 12, C["muted"], "end")
    cv.dim((Q_BP / 2 + 2, Q_YB), (Q_BP / 2 + 2, Q_YPL), f"{Q_DP:.2f}", off=-26, label_off=-30, size=13)
    cv.text_px(cv.X(0), cv.Y(Q_HD + Q_TP) - 14, f"蓋板 A = {Q_AP:g} cm²（Q 只算這一塊）", 12.5, C["bmd"], weight="700")
    xr = 620
    lines = [(f"A = {Q_AH:.2f} + {Q_AP:g} = {Q_AH + Q_AP:.2f} cm²", C["text"]),
             (f"中性軸距 H 底面 {Q_YB:.2f} cm", C["text"]),
             (f"I ≈ {Q_I / 1e4:.2f} × 10⁴ cm⁴", C["text"]),
             (f"Q = {Q_AP:g} × {Q_DP:.2f} = {Q_Q:,.1f} cm³", C["bmd"]),
             (f"q = VQ/I = {Q_VU:g} × {Q_Q:,.1f} / I", C["text"]),
             (f"  = {Q_QF:.3f} tf/cm", C["bmd"]),
             ("", C["text"]),
             (f"誤以 H 形心算：Q = {Q_Q_WRONG:,.1f}", C["load"]),
             (f"（高估 {Q_Q_WRONG / Q_Q - 1:.0%}）", C["load"])]
    for i, (s, col) in enumerate(lines):
        if s:
            cv.text_px(xr, 150 + i * 34, s, 13.5, col, "start", weight="700" if col != C["text"] else "400")
    path = os.path.join(OUT, f"{TAG}-fig-1-section.svg")
    compose([cv], cols=1,
            title=f"圖 1　加蓋板後中性軸上移到 {Q_YB:.2f} cm，Q = {Q_Q:,.1f} cm³",
            sub="剪力流要用組合斷面的 I 與中性軸；Q 只取銲道以外（蓋板）那一塊",
            note="加了蓋板，中性軸就不在 H 型鋼中點——用 25 cm 會把蓋板的力臂與 Q 都算錯",
            path=path)
    return path


def fig2_inter():
    W1, H1 = 1000, 560
    cv = Canvas(W1, H1, sx=1)
    cv.panel("斷續銲：每段 L、中心距 s = 15 cm（沿梁長，上下兩道對稱）", "每一個 s 範圍內的剪力流合力，由該段銲道承擔")
    x0, sc = 130, 12.0
    nseg = 4
    yb, yt = 150, 220
    _hl(cv, H1, x0, yb + 35, x0 + sc * Q_S * nseg, yb + 35, C["ghost"], 1.4, dash="8 4")
    cv.rect_px(x0, yb, sc * Q_S * nseg, 70, "rgba(63,74,90,0.08)", 0, C["member"], 1.4)
    for k in range(nseg):
        xc = x0 + sc * (Q_S * k + Q_S / 2)
        for yy in (yb, yb + 70):
            cv.rect_px(xc - sc * Q_LUSE / 2, yy - 5, sc * Q_LUSE, 10, C["load"], 2)
        if k < nseg - 1:
            cv.dim((xc, H1 - yb + 26), (xc + sc * Q_S, H1 - yb + 26), f"s = {Q_S:g}", off=0, label_off=-14, size=12.5)
    xc0 = x0 + sc * Q_S / 2
    cv.dim((xc0 - sc * Q_LUSE / 2, H1 - yb - 96), (xc0 + sc * Q_LUSE / 2, H1 - yb - 96), f"L = {Q_LUSE}", off=0, label_off=-14, size=12.5)
    # 剪力流示意箭頭
    for k in range(10):
        xa = x0 + 20 + k * (sc * Q_S * nseg - 40) / 10
        cv.arrow((xa, H1 - yb - 130), (xa + 26, H1 - yb - 130), C["sfd"], 1.8, 7)
    cv.text_px(x0 + sc * Q_S * nseg / 2, yb + 150, f"q = {Q_QF:.3f} tf/cm（沿全長連續）", 13, C["sfd"], weight="700")
    # 長條比較
    bx, bs = 260, 30.0
    rows = ((f"每間距需求 q·s", Q_FS, C["sfd"]), (f"L = {Q_LUSE} cm 容量 φRn·L", Q_RW * Q_LUSE, C["bmd"]))
    for i, (nm, v, col) in enumerate(rows):
        y = 400 + i * 52
        cv.text_px(bx - 12, y, nm, 13, C["text"], "end", weight="700")
        cv.rect_px(bx, y - 14, bs * v, 28, col, 4)
        cv.text_px(bx + bs * v + 8, y, f"{v:.2f} tf", 13, col, "start", weight="700")
    cv.text_px(W1 - 40, 400, f"L ≥ {Q_FS:.2f} / {Q_RW:.3f}", 13, C["text"], "end")
    cv.text_px(W1 - 40, 428, f"  = {Q_LREQ:.2f} → {Q_LUSE} cm", 14, C["bmd"], "end", weight="700")
    cv.text_px(W1 - 40, 456, f"填充率 {Q_LUSE / Q_S:.0%}", 12.5, C["muted"], "end")
    path = os.path.join(OUT, f"{TAG}-fig-2-inter.svg")
    compose([cv], cols=1,
            title=f"圖 2　每 {Q_S:g} cm 剪力 {Q_FS:.2f} tf ⇒ 每段銲長 {Q_LUSE} cm",
            sub=f"φRn = 2 道 × 0.75 × 0.6 × 4.9 × {Q_TE:.3f} = {Q_RW:.3f} tf/cm（每 cm 段長，兩道合計）",
            note="q 是「每 cm 梁長」的剪力；斷續銲要先乘間距 s 換成每段的力，再除以每 cm 銲道容量",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "只算一道銲（漏另一側）；把 150 當成段長或淨距；上下對稱誤讀成交錯"),
    (fig1_section, "§4 Step 1–5",
     "中性軸取 H 型鋼中點（25 cm）；Q 取錯面積；I 未含蓋板"),
    (fig2_inter, "§4 Step 6–8",
     "把每 cm 的 q 直接當每段力；只算一道銲；間距與段長混淆"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
