#!/usr/bin/env python3
"""
SS-2004-3 托架偏心載重之填角銲（LRFD 彈性法）— 題目附圖重繪腳本

用法：
    python3 gen_SS-2004-3.py [輸出目錄]

重繪依據：題目正本 SS-2004-3-problem.md §4 判讀清單（待確認）。
只畫考卷附圖所示：托架板搭於柱翼板、上下兩組 L 形填角銲（斜線區）、7.5／10／5／15／5 cm 尺寸、Pu 1:1 斜向。
托架板與銲道依比例（銲道寬以 10 mm 銲腳示意）；柱翼板寬、托架右緣位置與斜切轉折為示意（考卷未標）。
附表（表 10.2.5 銲接設計強度）已照錄於題目正本 §2，不重繪。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2004-3"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2004-3-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
LAP = 7.5           # #2 托架左緣至柱翼板右緣 7.5 cm（＝水平銲道長）
EP = 10.0           # #3 柱翼板右緣至 Pu 作用點 10 cm
HV = 5.0            # #1 垂直銲道各 5 cm（沿托架左緣，上下各一）
HM = 15.0           # #1 中段 15 cm 不銲
H = 2 * HV + HM     # 托架總高 25 cm
#                     #4 Pu 作用於托架上緣，1:1 向左下
#                     #5 只畫一面（單面填角銲，待確認）
W = 1.0             # 題文 銲腳 10 mm（斜線區寬度）
# 示意（考卷未標）：
BF = 14.0           # 柱翼板寬
X_RE = EP + 2.5     # 托架右緣
Y_K = H - 6.5       # 右緣垂直段下端（斜切起點）
COL_EXT = 5.0

PW, PHT = 760, 680


def _hatched(cv, x0, x1, y0, y1, step=0.55):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], C["fill_t"], C["load"], 1.2)
    xa, xb = min(x0, x1), max(x0, x1)
    ya, yb = min(y0, y1), max(y0, y1)
    h = yb - ya
    k = xa - h
    while k < xb:
        p0 = (max(k, xa), ya + max(0, xa - k))
        p1 = (min(k + h, xb), ya + min(h, xb - k))
        if p1[0] > p0[0]:
            cv.line(p0, p1, C["load"], 1.0)
        k += step


def _zig(cv, x0, x1, y):
    xm = (x0 + x1) / 2
    cv.poly([(x0, y), (xm - 0.6, y), (xm - 0.2, y + 1.0), (xm + 0.2, y - 1.0), (xm + 0.6, y), (x1, y)],
            C["member"], 1.8)


def panel():
    sx = 14.0
    cv = Canvas(PW, PHT, sx=sx, ox=380, oy=105)
    cv.panel("托架立面", "托架板搭接於柱翼板（翼板面向讀者）")
    # 柱翼板（托架以外可見部分）
    top, bot = H + COL_EXT, -COL_EXT
    cv.line((-BF, bot), (-BF, top), C["member"], 2.0)
    cv.line((0, H), (0, top), C["member"], 2.0)
    cv.line((0, 0), (0, bot), C["member"], 2.0)
    _zig(cv, -BF - 1, 1, top)
    _zig(cv, -BF - 1, 1, bot)
    # 托架板
    cv.polygon([(-LAP, 0), (0, 0), (X_RE, Y_K), (X_RE, H), (-LAP, H)], C["fill_c"], C["member"], 2.2)
    # 銲道（斜線區）：上組＝上緣水平 7.5＋左緣垂直 5；下組對稱
    _hatched(cv, -LAP, 0, H, H + W)
    _hatched(cv, -LAP - W, -LAP, H - HV, H + W)
    _hatched(cv, -LAP, 0, -W, 0)
    _hatched(cv, -LAP - W, -LAP, -W, HV)
    # 尺寸：上方 7.5、10
    yd = H + COL_EXT + 3.0
    cv.line((-LAP, H + W), (-LAP, yd + 0.5), C["dim"], 1, dash="3 3")
    cv.line((0, top), (0, yd + 0.5), C["dim"], 1, dash="3 3")
    cv.line((EP, H), (EP, yd + 0.5), C["muted"], 1.2, dash="5 4")
    cv.dim((-LAP, yd), (0, yd), f"{LAP} cm", label_off=-15)
    cv.dim((0, yd), (EP, yd), f"{EP:.0f} cm", label_off=-15)
    # 尺寸：左側 5／15／5
    xd = -BF - 3.0
    for ya, yb, lab in ((H, H - HV, f"{HV:.0f} cm"), (H - HV, HV, f"{HM:.0f} cm"), (HV, 0, f"{HV:.0f} cm")):
        cv.dim((xd, ya), (xd, yb), lab, label_off=30)
    for yy in (H, H - HV, HV, 0):
        cv.line((xd - 0.6, yy), (-LAP - W - 0.3, yy), C["dim"], 1, dash="3 3")
    # Pu：托架上緣、距翼板右緣 10 cm，1:1 向左下
    L = 7.5
    tail = (EP + L, H + L)
    cv.arrow(tail, (EP, H), C["load"], 3.2, 12)
    cv.math(tail, "P_{u}", 17, C["load"], "start", dx=6, dy=-8, weight="700")
    s = 1.6
    t0 = (EP + 2.6, H + 2.6 - 0.0)
    t0 = (t0[0] + 0.5, t0[1] - 0.5)
    t1 = (t0[0] + s, t0[1] + s)
    cn = (t1[0], t0[1])
    cv.poly([t0, cn, t1], C["load"], 1.4)
    cv.text(((t0[0] + cn[0]) / 2, t0[1]), "1", 13, C["load"], dy=11)
    cv.text((cn[0], (cn[1] + t1[1]) / 2), "1", 13, C["load"], "start", dx=6)
    # 銲道說明
    cv.text_px(PW - 24, PHT - 40, "斜線區＝填角銲（銲腳 10 mm）", 12.5, C["load"], "end")
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([panel()], cols=1,
            title="SS-2004-3 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#5；托架與銲道依比例，柱翼板寬與托架右緣外形為示意",
            note="每組銲道是水平 7.5 cm＋垂直 5 cm 的 L 形，中段 15 cm 不銲；10 cm 由翼板右緣量到 Pu",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2004-3.md §4，由下式即時算出
# 座標：原點在托架左緣、上下中點；x 向右、y 向上（cm）
# ══════════════════════════════════════════════════════════════
import math
Q_FEXX, Q_PHI = 4.93, 0.75                       # t/cm²                 §1
Q_TE  = 0.707 * W                                # 喉厚                  §4.1
Q_CAP = Q_PHI * 0.6 * Q_FEXX * Q_TE              # 1.568 t/cm
Q_HH  = H / 2                                    # 12.5
Q_SEGS = [((0, Q_HH), (LAP, Q_HH)), ((0, Q_HH - HV), (0, Q_HH)),
          ((0, -Q_HH), (LAP, -Q_HH)), ((0, -Q_HH), (0, -Q_HH + HV))]
Q_LW  = sum(math.dist(a, b) for a, b in Q_SEGS)
Q_XB  = sum(math.dist(a, b) * (a[0] + b[0]) / 2 for a, b in Q_SEGS) / Q_LW   # 2.25
def _ilin(a, b, xc, yc):
    L = math.dist(a, b); mx, my = (a[0] + b[0]) / 2 - xc, (a[1] + b[1]) / 2 - yc
    ix = L * my * my + (L ** 3 / 12 if a[0] == b[0] else 0)
    iy = L * mx * mx + (L ** 3 / 12 if a[1] == b[1] else 0)
    return ix, iy
Q_IX = sum(_ilin(a, b, Q_XB, 0)[0] for a, b in Q_SEGS)
Q_IY = sum(_ilin(a, b, Q_XB, 0)[1] for a, b in Q_SEGS)
Q_J  = Q_IX + Q_IY                                # 3519.3
Q_UX = Q_UY = -1 / math.sqrt(2)                   # 1:1 向左下
Q_XP, Q_YP = LAP + EP - Q_XB, Q_HH                # (15.25, 12.5) 相對形心
Q_MV = Q_XP * Q_UY                                # 垂直分量 → 順時針（負）
Q_MH = -Q_YP * Q_UX                               # 水平分量 → 逆時針（正）
Q_M  = Q_MV + Q_MH                                # −1.944（×Pu）
Q_PTS = {"上水平右端": (LAP, Q_HH), "上垂直上端": (0, Q_HH), "上垂直下端": (0, Q_HH - HV),
         "下水平右端": (LAP, -Q_HH), "下垂直下端": (0, -Q_HH), "下垂直上端": (0, -Q_HH + HV)}
def q_stress(x, y):
    xr = x - Q_XB
    return Q_UX / Q_LW - Q_M * y / Q_J, Q_UY / Q_LW + Q_M * xr / Q_J
Q_FR = {k: math.hypot(*q_stress(*p)) for k, p in Q_PTS.items()}
Q_CTRL = max(Q_FR, key=Q_FR.get)
Q_PU = Q_CAP / Q_FR[Q_CTRL]                      # 33.4
Q_PU0 = Q_CAP * Q_LW                             # 無扭矩上限 39.2


def _wgroup(cv):
    for a, b in Q_SEGS:
        cv.line(a, b, C["load"], 5.0, cap="butt")
    cv.poly([(0, -Q_HH), (LAP + EP + 2.5, -Q_HH)], C["ghost"], 1.0, dash="4 4")


def fig1_line():
    W1, H1 = 560, 560
    sx = 13.0
    cv = Canvas(W1, H1, sx=sx, ox=110, oy=250)
    cv.panel("① 載重線幾乎通過銲道形心", "托架上緣作用 Pu（1:1 向左下）；紅粗線＝銲道")
    cv.poly([(0, Q_HH), (LAP + EP + 2.5, Q_HH), (LAP + EP + 2.5, Q_HH - 6.5), (LAP, -Q_HH), (0, -Q_HH), (0, Q_HH)],
            C["ghost"], 1.4)
    _wgroup(cv)
    cv.line((Q_XB - 0.8, 0), (Q_XB + 0.8, 0), C["text"], 1.4); cv.line((Q_XB, -0.8), (Q_XB, 0.8), C["text"], 1.4)
    cv.text_px(cv.X(Q_XB) - 4, cv.Y(0) + 34, f"形心（距托架左緣 {Q_XB:.2f}）", 12, C["text"], "start", weight="700")
    p0 = (LAP + EP, Q_HH)
    cv.line((p0[0] - 4 * Q_UX, p0[1] - 4 * Q_UY), (p0[0] + 21 * Q_UX, p0[1] + 21 * Q_UY), C["ghost"], 1.4, dash="6 5")
    cv.arrow((p0[0] - 4 * Q_UX, p0[1] - 4 * Q_UY), p0, C["load"], 3.2, 11)
    cv.text_px(cv.X(p0[0] - 4 * Q_UX) + 8, cv.Y(p0[1] - 4 * Q_UY), "Pu", 14, C["load"], "start", weight="700")
    # 形心到力線垂足
    t = -((p0[0] - Q_XB) * Q_UX + p0[1] * Q_UY)
    foot = (p0[0] + t * Q_UX, p0[1] + t * Q_UY)
    cv.line((Q_XB, 0), foot, C["accent"], 2.6)
    cv.text_px(cv.X(Q_XB) + 34, cv.Y(0) - 12, f"e = {abs(Q_M):.2f} cm", 13, C["accent"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 56, f"淨扭矩 M = {abs(Q_M):.2f}·Pu（順時針）", 14, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, f"Lw = {Q_LW:g} cm，J = {Q_J:.1f} cm³", 12.5, C["muted"])
    p1 = cv

    cv = Canvas(W1, H1, sx=1)
    cv.panel("② 兩個分量的力矩互相抵銷", "以 Pu = 1 計，對銲道形心取矩")
    x0, sc = 200, 18.0
    rows = ((f"垂直分量 × {Q_XP:.2f}", abs(Q_MV), C["load"], "順時針"),
            (f"水平分量 × {Q_YP:.1f}", abs(Q_MH), C["compr"], "逆時針"),
            ("淨扭矩", abs(Q_M), C["accent"], "順時針"))
    for i, (nm, v, col, d) in enumerate(rows):
        y = 150 + i * 80
        cv.text_px(x0 - 12, y, nm, 13, C["text"], "end", weight="700" if i == 2 else "400")
        cv.rect_px(x0, y - 15, sc * v, 30, col, 4)
        cv.text_px(x0 + sc * v + 8, y, f"{v:.2f}·Pu（{d}）", 12.5, col, "start", weight="700")
    cv.text_px(W1 / 2, H1 - 82, f"只算垂直分量：M = {abs(Q_MV):.2f}·Pu，是淨值的 {abs(Q_MV) / abs(Q_M):.1f} 倍", 13, C["load"], weight="700")
    cv.text_px(W1 / 2, H1 - 56, "Pu 會被低估許多", 12.5, C["muted"])
    cv.text_px(W1 / 2, H1 - 30, "水平分量作用在上緣、對形心是反向力矩", 12.5, C["muted"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-1-line.svg")
    compose([p1, p2], cols=2,
            title=f"圖 1　載重線離形心只有 {abs(Q_M):.2f} cm：扭矩小",
            sub=f"作用點相對形心 ({Q_XP:.2f}, {Q_YP:.1f}) cm；Pu 分量各 0.7071·Pu",
            note=f"銲道群形心不在托架左緣，而在其右方 {Q_XB:.2f} cm；斜向載重要兩個分量一起取矩",
            path=path)
    return path


def fig2_stress():
    W1, H1 = 560, 560
    sx = 13.0
    cv = Canvas(W1, H1, sx=sx, ox=170, oy=300)
    cv.panel("① 銲道端點應力（直接＋扭矩，×Pu）", "箭頭長度與應力成比例")
    _wgroup(cv)
    vs = 3.6 / max(Q_FR.values())
    for k, (x, y) in Q_PTS.items():
        fx, fy = q_stress(x, y)
        crit = k == Q_CTRL
        tip = (x + vs * fx, y + vs * fy)
        cv.arrow((x, y), tip, C["load"] if crit else C["bmd"], 3.0 if crit else 2.0, 9)
        cv.dot((x, y), 3.5, fill=C["text"])
        cv.text_px(cv.X(tip[0]) - 6, cv.Y(tip[1]) + 16, f"{Q_FR[k]:.5f}" if crit else f"{Q_FR[k]:.4f}", 11.5, C["load"] if crit else C["bmd"],
                   "end", weight="700")
    cv.text_px(W1 / 2, H1 - 56, f"控制點：{Q_CTRL}　fr = {Q_FR[Q_CTRL]:.5f}·Pu", 13.5, C["load"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, "順時針扭矩使下緣右端的扭矩剪力朝左下，與直接剪力同向", 12, C["muted"])
    p1 = cv

    cv = Canvas(W1, H1, sx=1)
    cv.panel("② 最大 Pu（tf）", f"φRnw = 0.75 × 0.6 × {Q_FEXX} × {Q_TE:.3f} = {Q_CAP:.3f} t/cm")
    x0, sc = 170, 8.0
    rows = (("本解（含扭矩）", Q_PU, C["bmd"]), ("上限：無扭矩", Q_PU0, C["ghost"]))
    for i, (nm, v, col) in enumerate(rows):
        y = 170 + i * 90
        cv.text_px(x0 - 12, y, nm, 13, C["text"], "end", weight="700")
        cv.rect_px(x0, y - 16, sc * v, 32, col, 4)
        cv.text_px(x0 + sc * v + 8, y, f"{v:.1f}", 14, col if i == 0 else C["muted"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 82, f"Pu = {Q_CAP:.3f} / {Q_FR[Q_CTRL]:.5f} = {Q_PU:.1f} tf", 14, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 56, f"為無扭矩上限的 {Q_PU / Q_PU0:.0%}——符合「載重線接近形心」", 12.5, C["muted"])
    cv.text_px(W1 / 2, H1 - 30, "答案若遠低於此上限，多半是扭矩算大了", 12.5, C["muted"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-2-stress.svg")
    compose([p1, p2], cols=2,
            title=f"圖 2　控制點在下水平銲右端，Pu = {Q_PU:.1f} tf",
            sub=f"f = Pu/Lw ＋ M·r/J（Lw = {Q_LW:g} cm、J = {Q_J:.1f} cm³、M = {abs(Q_M):.2f}·Pu）",
            note="六個端點都要比：扭矩剪力最大處不一定是合力最大處，要看它與直接剪力的夾角",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "漏掉垂直 5 cm 段或把中段 15 cm 也當銲道；10 cm 誤由托架左緣量起"),
    (fig1_line, "§4.2–4.3",
     "形心取在托架左緣；只用垂直分量取矩（M 放大 5.5 倍、Pu 嚴重低估）"),
    (fig2_stress, "§4.4–4.6",
     "選錯控制點；答案遠低於無扭矩上限仍不察覺"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
