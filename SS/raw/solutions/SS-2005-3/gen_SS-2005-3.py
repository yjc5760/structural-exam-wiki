#!/usr/bin/env python3
"""
SS-2005-3 箱型懸臂梁銲接於柱（ASD 彈性法，彎矩＋扭矩）— 題目附圖重繪腳本

用法：
    python3 gen_SS-2005-3.py [輸出目錄]

重繪依據：題目正本 SS-2005-3-problem.md §4 判讀清單（待確認）。
只畫考卷附圖所示：立面（柱、箱型梁、兩個銲接符號、50 cm、A-A 剖切記號）與 A-A 斷面（P 偏心 14 cm）。
箱型梁 300×300×18 與 50 cm、14 cm 依比例；柱深、柱翼板厚、柱內加勁板厚與柱長為示意（考卷未標）。
銲接符號照考卷：現場銲旗＋雙面填角（10／10；12–200／12–200，尾註「對稱於梁中心線」）。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2005-3"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2005-3-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
B, T = 30.0, 1.8        # 題文 箱型梁 300×300×18×18 mm
E_M = 50.0              # #5 P 距柱面 50 cm（立面）
E_T = 14.0              # #5 P 距梁垂直中心線 14 cm（A-A 斷面），位於中心線左側
W1 = "10"               # #1 上翼板與柱面：10 mm 填角銲，雙面（符號 10/10），未標長度
W2, L2 = "12", "200"    # #2 腹板與柱面：12 mm 填角銲，雙面，每道 200 mm，對稱於梁中心線
#                         #3 下翼板無銲接符號（照考卷不畫符號）
# 示意（考卷未標）：
DC, TFC = 30.0, 1.6     # 柱深、柱翼板厚
TST = 1.6               # 柱內加勁板厚
HC = 46.0               # 柱自梁中心線上下各畫出長度
X_SEC = 100.0           # A-A 斷面在同一畫布上的水平位置（排版用）

PW, PHT = 1120, 720


def _zig(cv, x0, x1, y):
    xm = (x0 + x1) / 2
    cv.poly([(x0, y), (xm - 1.2, y), (xm - 0.4, y + 2.0), (xm + 0.4, y - 2.0), (xm + 1.2, y), (x1, y)],
            C["member"], 1.8)


def _weld_symbol(cv, tip, knee, ref_px, tri_px, top_l, bot_l, top_r=None, bot_r=None, tail=None):
    """銲接符號（像素排版）：箭頭→折點→基線；折點處現場銲旗；tri_px 處畫雙面填角三角形。"""
    m = C["text"]
    kx, ky = cv.P(knee)
    tx, ty = cv.P(tip)
    cv.parts.append(f'<line x1="{kx:.1f}" y1="{ky:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" '
                    f'stroke="{m}" stroke-width="1.5"/>')
    import math
    ang = math.atan2(ty - ky, tx - kx)
    hl, hw = 11, 4
    pts = [(tx, ty), (tx - hl * math.cos(ang) + hw * math.sin(ang), ty - hl * math.sin(ang) - hw * math.cos(ang)),
           (tx - hl * math.cos(ang) - hw * math.sin(ang), ty - hl * math.sin(ang) + hw * math.cos(ang))]
    cv.parts.append(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{m}"/>')
    cv.parts.append(f'<line x1="{kx:.1f}" y1="{ky:.1f}" x2="{kx + ref_px:.1f}" y2="{ky:.1f}" '
                    f'stroke="{m}" stroke-width="1.5"/>')
    # 現場銲旗
    cv.parts.append(f'<line x1="{kx:.1f}" y1="{ky:.1f}" x2="{kx:.1f}" y2="{ky - 34:.1f}" '
                    f'stroke="{m}" stroke-width="1.5"/>')
    cv.parts.append(f'<polygon points="{kx:.1f},{ky - 34:.1f} {kx + 12:.1f},{ky - 29:.1f} '
                    f'{kx:.1f},{ky - 24:.1f}" fill="{m}"/>')
    # 雙面填角：基線上下各一個直角三角形（垂直邊在左）
    x0 = kx + tri_px
    for sg in (-1, 1):
        cv.parts.append(f'<polygon points="{x0:.1f},{ky:.1f} {x0:.1f},{ky + sg * 13:.1f} '
                        f'{x0 + 13:.1f},{ky:.1f}" fill="#FFFFFF" stroke="{m}" stroke-width="1.5"/>')
    cv.text_px(x0 - 6, ky - 11, top_l, 14, m, "end")
    cv.text_px(x0 - 6, ky + 12, bot_l, 14, m, "end")
    if top_r:
        cv.text_px(x0 + 18, ky - 11, top_r, 14, m, "start")
        cv.text_px(x0 + 18, ky + 12, bot_r, 14, m, "start")
    if tail:
        ex = kx + ref_px
        cv.parts.append(f'<polyline points="{ex + 12:.1f},{ky - 10:.1f} {ex:.1f},{ky:.1f} '
                        f'{ex + 12:.1f},{ky + 10:.1f}" fill="none" stroke="{m}" stroke-width="1.5"/>')
        for i, line in enumerate(tail):
            cv.text_px(ex + 18, ky - 10 + 21 * i, line, 14, m, "start")


def _cut_mark(cv, p, up=True):
    x, y = cv.P(p)
    s = -1 if up else 1
    m = C["text"]
    cv.parts.append(f'<polyline points="{x:.1f},{y:.1f} {x:.1f},{y + s * 16:.1f} {x - 26:.1f},{y + s * 16:.1f}" '
                    f'fill="none" stroke="{m}" stroke-width="1.5"/>')
    cv.parts.append(f'<polygon points="{x - 34:.1f},{y + s * 16:.1f} {x - 24:.1f},{y + s * 16 - 4:.1f} '
                    f'{x - 24:.1f},{y + s * 16 + 4:.1f}" fill="{m}"/>')
    cv.text_px(x - 16, y + s * 16 + 14, "A", 15, m)


def _rect(cv, x0, x1, y0, y1, fill="none", w=2.0):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, C["member"], w)


def panel():
    sx = 6.4
    cv = Canvas(PW, PHT, sx=sx, ox=250, oy=PHT / 2 - 10)
    cv.panel("立面與 A-A 斷面", "註：銲接符號單位為 mm")
    h = B / 2
    # ── 柱（兩翼板＋梁翼高度之加勁板）──
    for x0 in (-DC, -TFC):
        _rect(cv, x0, x0 + TFC, -HC, HC, "#FFFFFF", 1.8)
    for yy in (h, -h):
        _rect(cv, -DC + TFC, -TFC, yy - TST, yy, "#FFFFFF", 1.6)
    _zig(cv, -DC - 1.5, 1.5, HC)
    _zig(cv, -DC - 1.5, 1.5, -HC)
    cv.line((-DC + TFC / 2, -HC + 4), (-DC - 4, -HC - 3), C["muted"], 1.1)
    cv.text((-DC - 4, -HC - 3), "鋼柱", 14, C["text"], "end", dx=-4)
    # ── 箱型梁立面 ──
    _rect(cv, 0, E_M, -h, h, C["fill_c"], 2.0)
    for yy in (h - T, -h + T):
        cv.line((0, yy), (E_M, yy), C["member"], 1.3, dash="6 4")
    cv.line((-6, 0), (E_M + 8, 0), C["muted"], 1.1, dash="12 3 2 3")
    # P（立面）
    cv.arrow((E_M, h + 11), (E_M, h + 0.4), C["load"], 5, 14)
    cv.math((E_M, h + 11), "P", 17, C["load"], dy=-12, weight="700")
    # A-A 剖切記號
    _cut_mark(cv, (E_M + 9, h + 2), up=True)
    _cut_mark(cv, (E_M + 9, -h - 2), up=False)
    # 50 cm
    yd = -h - 15
    cv.line((E_M, -h), (E_M, yd - 1.5), C["dim"], 1, dash="3 3")
    cv.dim((0, yd), (E_M, yd), f"{E_M:.0f} cm", label_off=-15)
    # ── 銲接符號 ──
    _weld_symbol(cv, (0, h), (9, h + 18), 120, 74, W1, W1)
    _weld_symbol(cv, (0, 0), (8, -h - 7), 110, 58, W2, W2, L2, L2,
                 tail=("對稱於梁", "中心線"))
    # ── A-A 斷面 ──
    xc = X_SEC + B / 2
    _rect(cv, X_SEC, X_SEC + B, -h, h, C["fill_c"], 2.0)
    _rect(cv, X_SEC + T, X_SEC + B - T, -h + T, h - T, "#FFFFFF", 1.6)
    cv.line((xc, h + 12), (xc, -h - 5), C["muted"], 1.1, dash="12 3 2 3")
    xp = xc - E_T
    cv.arrow((xp, h + 11), (xp, h + 0.4), C["load"], 5, 14)
    cv.math((xp, h + 11), "P", 17, C["load"], dy=-12, weight="700")
    cv.dim((xp, h + 7), (xc, h + 7), f"{E_T:.0f} cm", label_off=-14)
    cv.text((xc, -h - 9), "A-A 斷面", 15, C["text"], weight="700")
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([panel()], cols=1,
            title="SS-2005-3 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#5；箱型梁與 50、14 cm 依比例，柱深與柱內加勁板為示意",
            note="只有兩個銲接符號（上翼板 10/10、腹板 12–200 對稱中心線），下翼板沒有符號；P 另有 14 cm 側向偏心",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2005-3.md §4，由下式即時算出
# 座標（A-A 斷面）：y 向上、z 水平，原點在梁斷面中心（cm）
# ══════════════════════════════════════════════════════════════
import math
Q_TE1, Q_TE2 = 0.707 * 1.0, 0.707 * 1.2           # 喉厚：10 mm、12 mm 填角銲    §4.1
Q_H = B / 2                                        # 15
Q_LW2 = 20.0                                       # 腹板銲每道 20 cm（y = −10～10）
# (喉厚, 長度, 方向, 中心 y, 中心 z)；方向 'z' 為水平銲、'y' 為垂直銲
Q_WELDS = [(Q_TE1, B, "z", Q_H, 0.0), (Q_TE1, B, "z", Q_H - T, 0.0)] + \
          [(Q_TE2, Q_LW2, "y", 0.0, z) for z in (Q_H, -Q_H, Q_H - T, -(Q_H - T))]
Q_A  = sum(t * L for t, L, *_ in Q_WELDS)
Q_YB = sum(t * L * y for t, L, d, y, z in Q_WELDS) / Q_A
Q_IZ = sum(t * L * (y - Q_YB) ** 2 + (t * L ** 3 / 12 if d == "y" else 0) for t, L, d, y, z in Q_WELDS)
Q_IY = sum(t * L * z ** 2 + (t * L ** 3 / 12 if d == "z" else 0) for t, L, d, y, z in Q_WELDS)
Q_J  = Q_IZ + Q_IY
Q_M, Q_T = E_M, E_T                                # M = 50P、T = 14P               §4.3
Q_YC, Q_ZC = -Q_LW2 / 2, Q_H                       # 控制點（腹板銲下端、外側）     §4.4
Q_DC = Q_YB - Q_YC                                 # 15.42
Q_FN = Q_M * Q_DC / Q_IZ
Q_FV = 1 / Q_A + Q_T * Q_ZC / Q_J
Q_FH = Q_T * Q_DC / Q_J
Q_FR = math.sqrt(Q_FN ** 2 + Q_FV ** 2 + Q_FH ** 2)
Q_FW = 0.3 * 4.9                                   # 容許 1.47 t/cm²               §4.5
Q_P  = Q_FW / Q_FR                                 # 14.0
Q_P_ALT = 35.7                                     # 替代解讀（下翼板亦銲），引自 §4.6
Q_FR_TOP = math.sqrt((Q_M * (Q_H - Q_YB) / Q_IZ) ** 2 + (1 / Q_A) ** 2)   # 上翼板（約值，僅比較）
Q_INNER = B - 2 * T                                # 箱內淨寬 26.4


def fig1_section():
    W1, H1 = 1000, 620
    sx = 12.5
    cv = Canvas(W1, H1, sx=sx, ox=330, oy=300)
    cv.panel("A-A 斷面：柱面銲道群（紅＝銲道，線寬示意喉厚）", "下翼板沒有銲 → 銲道群形心上移")
    def rect(z0, z1, y0, y1, fill, st=C["member"], w=1.4):
        cv.polygon([(z0, y0), (z1, y0), (z1, y1), (z0, y1)], fill, st, w)
    rect(-Q_H, Q_H, -Q_H, Q_H, "rgba(63,74,90,0.08)")
    rect(-Q_H + T, Q_H - T, -Q_H + T, Q_H - T, "#FFFFFF", C["member"], 1.0)
    for t, L, d, y, z in Q_WELDS:
        if d == "z":
            cv.line((z - L / 2, y), (z + L / 2, y), C["load"], 4.5 if t == Q_TE1 else 5.5, cap="butt")
        else:
            cv.line((z, y - L / 2), (z, y + L / 2), C["load"], 5.5, cap="butt")
    cv.line((-Q_H - 4, 0), (Q_H + 4, 0), C["ghost"], 1.2, dash="10 4 2 4")
    cv.text_px(cv.X(-Q_H + T) + 8, cv.Y(0) - 12, "梁中線", 12, C["muted"], "start")
    cv.line((-Q_H - 4, Q_YB), (Q_H + 4, Q_YB), C["accent"], 2.2, dash="7 4")
    cv.text_px(cv.X(-Q_H + T) + 8, cv.Y(Q_YB) - 12, f"銲道群中性軸（中線上方 {Q_YB:.2f}）", 12.5, C["accent"], "start", weight="700")
    cv.dim((Q_H + 2, Q_YC), (Q_H + 2, Q_YB), f"{Q_DC:.2f}", off=34, label_off=26, size=13)
    cv.dot((Q_ZC, Q_YC), 7, fill=C["load"])
    cv.text_px(cv.X(Q_ZC) + 14, cv.Y(Q_YC) + 26, "控制點 (y, z) = (−10, 15)", 12.5, C["load"], "start", weight="700")
    zp = -Q_T
    cv.arrow((zp, Q_H + 6), (zp, Q_H + 0.4), C["load"], 3.2, 11)
    cv.text_px(cv.X(zp) - 8, cv.Y(Q_H + 5), "P", 15, C["load"], "end", weight="700")
    cv.dim((zp, Q_H + 2.6), (0, Q_H + 2.6), f"{Q_T:g}", off=-16, label_off=-12, size=12)
    # 右側說明
    xr = 650
    lines = [(f"銲道喉部總面積 A = {Q_A:.1f} cm²", C["text"]),
             (f"上翼板兩道（10 mm）＋ 腹板四道（12 mm × 20 cm）", C["muted"]),
             (f"M = {Q_M:g}P（立面偏心 {Q_M:g} cm）", C["text"]),
             (f"T = {Q_T:g}P（斷面側偏 {Q_T:g} cm）", C["text"]),
             (f"距中性軸最遠的是腹板銲下端：{Q_DC:.2f} cm", C["load"]),
             (f"若誤取梁中線：只有 10 cm，fn 低估 {1 - 10 / Q_DC:.0%}", C["load"]),
             ("", C["text"]),
             (f"註：箱內上翼板下面那道，箱內淨寬僅 {Q_INNER:.1f} cm；", C["muted"]),
             ("解析依判讀清單 #1 計 30 cm（#4 待確認）；", C["muted"]),
             (f"改用 {Q_INNER:.1f} cm 時 P 約 13.9 tf。", C["muted"])]
    for i, (s, col) in enumerate(lines):
        if s:
            cv.text_px(xr, 150 + i * 30, s, 13, col, "start", weight="700" if col == C["load"] else "400")
    path = os.path.join(OUT, f"{TAG}-fig-1-section.svg")
    compose([cv], cols=1,
            title=f"圖 1　銲道群中性軸在梁中線上方 {Q_YB:.2f} cm，控制點在腹板銲下端",
            sub="立面彎矩 M 使下方受壓；只有腹板銲道下段承擔受壓區",
            note="不對稱的銲道群要先求形心，不能直接拿梁斷面中線當中性軸",
            path=path)
    return path


def fig2_comp():
    W1, H1 = 560, 520
    cv = Canvas(W1, H1, sx=1)
    cv.panel("① 控制點三個應力分量（×P，tf/cm²）", "彎曲正應力為主")
    x0, sc = 180, 2700.0
    rows = (("fn（彎曲，垂直柱面）", Q_FN, C["bmd"]), ("fv（直接＋扭矩，垂直）", Q_FV, C["sfd"]),
            ("fh（扭矩，水平）", Q_FH, C["accent"]), ("合成 fr", Q_FR, C["load"]))
    for i, (nm, v, col) in enumerate(rows):
        y = 140 + i * 66
        cv.text_px(x0 - 12, y, nm, 12.5, C["text"], "end", weight="700" if i == 3 else "400")
        cv.rect_px(x0, y - 14, max(sc * v, 3), 28, col, 4)
        cv.text_px(x0 + sc * v + 8, y, f"{v:.5f}" if i in (1, 2) else f"{v:.4f}", 12.5, col, "start", weight="700")
    cv.text_px(W1 / 2, H1 - 56, f"fr = √(fn² + fv² + fh²) = {Q_FR:.4f}P", 13.5, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, f"只算剪力（忽略 fn）會得 fr ≈ {math.hypot(Q_FV, Q_FH):.4f}P，低估 5 倍以上", 12.5, C["load"])
    p1 = cv

    cv = Canvas(W1, H1, sx=1)
    cv.panel("② 工作載重 P（tf）", f"容許 0.3 × 4.9 = {Q_FW:.2f} t/cm²（喉部）")
    x0, sc = 210, 7.0
    rows2 = (("本解（照符號）", Q_P, C["bmd"]), (f"箱內銲改 {Q_INNER:.1f} cm", 13.9, C["ghost"]),
             ("替代：下翼板亦銲", Q_P_ALT, C["ghost"]))
    for i, (nm, v, col) in enumerate(rows2):
        y = 150 + i * 80
        cv.text_px(x0 - 12, y, nm, 12.5, C["text"], "end", weight="700" if i == 0 else "400")
        cv.rect_px(x0, y - 15, sc * v, 30, col, 4)
        cv.text_px(x0 + sc * v + 8, y, f"{v:.1f}", 13.5, col if i == 0 else C["muted"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 56, f"P = {Q_FW:.2f} / {Q_FR:.4f} = {Q_P:.1f} tf", 14, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, "下翼板無銲接符號，不採替代解讀（§4.6）", 12.5, C["muted"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-2-comp.svg")
    compose([p1, p2], cols=2,
            title=f"圖 2　控制點 fr = {Q_FR:.4f}P ⇒ P = {Q_P:.1f} tf",
            sub=f"fn = M·d/Iz、fv = P/A + T·z/J、fh = T·d/J（d = {Q_DC:.2f}、z = {Q_ZC:g} cm）",
            note="懸臂端偏心 50 cm 的彎矩才是主角；扭矩 14P 與直接剪力只佔合成應力的一小部分",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "漏看 A-A 斷面的 14 cm 扭矩偏心；把 200 讀成銲腳或把下翼板也當有銲"),
    (fig1_section, "§4.1–4.2、§4.4",
     "中性軸取梁中線（d = 10 而非 15.42 cm）；控制點選在上翼板"),
    (fig2_comp, "§4.4–4.6",
     "忽略彎曲正應力、只算剪力；把下翼板也當有銲（P 高估為 35.7）"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
