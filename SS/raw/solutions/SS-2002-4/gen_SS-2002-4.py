#!/usr/bin/env python3
"""
SS-2002-4 托架板偏心螺栓接合（ASD 彈性法）— 題目附圖重繪腳本

用法：
    python3 gen_SS-2002-4.py [輸出目錄]

重繪依據：題目正本 SS-2002-4-problem.md §4 判讀清單（待確認）。
圖上只畫考卷給的東西：螺栓配置、5／7／21／25 cm 尺寸、P 的作用點與 3:4 斜率，不含任何解題結果。
螺栓群與 25 cm 依比例；鋼板左緣（與翼板左緣齊）、右下斜切的轉折位置、柱的上下延伸長度為示意（考卷未標）。
附表（容許應力、承壓公式）已照錄於題目正本 §2，不重繪。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2002-4"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2002-4-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
G = 7.0             # #2 行距 7 cm（兩行分居腹板兩側）
S = 7.0             # #2 列距 7 cm（3@7 cm = 21 cm）
NROW = 4            # #2 2 行 × 4 列 = 8 顆
EDGE = 5.0          # #4 鋼板上、下緣至最外列螺栓 5 cm
A25 = 25.0          # #3 右側螺栓行至鋼板右緣 25 cm（P 作用點水平位置）
PV, PH = 4.0, 3.0   # #5 P 向左下，垂直 4：水平 3，作用於鋼板右上角
DB = 2.2            # 題文 螺栓標稱直徑 22 mm
BF, TW = 15.44, 0.813   # §2 W6×25：bf、tw（#1 翼板面向讀者，虛線為腹板）
# 示意（考卷未標）：鋼板左緣取翼板左緣；右緣垂直段約占板高 40%
CHAMF = 0.40
COL_EXT = 12.0      # 柱在鋼板上下各延伸（示意）

X_R = G / 2 + A25                      # 鋼板右緣
Y_T = (NROW - 1) * S + EDGE            # 鋼板上緣（原點：最下列螺栓、腹板中心）
Y_B = -EDGE
H_PL = Y_T - Y_B

PW, PHT = 860, 700


def _wave(cv, x0, x1, y, amp=0.9, n=40):
    pts = [(x0 + (x1 - x0) * i / n, y + amp * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
    cv.poly(pts, C["member"], 1.8)


def panel():
    sx = 9.0
    cv = Canvas(PW, PHT, sx=sx, ox=330, oy=210)
    cv.panel("托架板螺栓接合立面", "W6×25 翼板面向讀者；鋼板厚 15 mm")
    xl, xr = -BF / 2, BF / 2
    # 柱（翼板外框）：鋼板以外的可見部分
    top, bot = Y_T + COL_EXT, Y_B - COL_EXT
    cv.line((xl, Y_T), (xl, top), C["member"], 2.2)
    cv.line((xr, Y_T), (xr, top), C["member"], 2.2)
    cv.line((xl, Y_B), (xl, bot), C["member"], 2.2)
    cv.line((xr, Y_B), (xr, bot), C["member"], 2.2)
    _wave(cv, xl, xr, top)
    _wave(cv, xl, xr, bot)
    for sg in (-1, 1):                                   # 腹板（虛線）
        cv.line((sg * TW / 2, Y_T), (sg * TW / 2, top - 1.5), C["member"], 1.4, dash="5 4")
        cv.line((sg * TW / 2, Y_B), (sg * TW / 2, bot + 1.5), C["member"], 1.4, dash="5 4")
    # 鋼板
    y_k = Y_T - CHAMF * H_PL
    plate = [(xl, Y_B), (xr, Y_B), (X_R, y_k), (X_R, Y_T), (xl, Y_T)]
    cv.polygon(plate, C["fill_c"], C["member"], 2.2)
    # 螺栓
    for j in range(NROW):
        for sg in (-1, 1):
            cv.circle((sg * G / 2, j * S), DB / 2, "#FFFFFF", C["member"], 1.8)
    # 尺寸：左側 5／3@7=21／5
    xd = xl
    for ya, yb_, lab, lo in ((Y_T, (NROW - 1) * S, f"{EDGE:.0f} cm", 30),
                             ((NROW - 1) * S, 0, f"3@{S:.0f} cm = {(NROW - 1) * S:.0f} cm", 66),
                             (0, Y_B, f"{EDGE:.0f} cm", 30)):
        cv.dim((xd, ya), (xd, yb_), lab, off=48, label_off=lo)
    for yy in ((NROW - 1) * S, 0):                       # 延伸線拉到螺栓中心
        cv.line((xd, yy), (-G / 2, yy), C["dim"], 1, dash="3 3")
    # 尺寸：下方 7 cm、25 cm
    yb = Y_B - 5.0
    cv.line((-G / 2, 0), (-G / 2, yb - 0.6), C["dim"], 1, dash="3 3")
    cv.line((G / 2, 0), (G / 2, yb - 0.6), C["dim"], 1, dash="3 3")
    cv.line((X_R, y_k), (X_R, yb - 0.6), C["dim"], 1, dash="3 3")
    cv.dim((-G / 2, yb), (G / 2, yb), f"{G:.0f} cm", label_off=17)
    cv.dim((G / 2, yb), (X_R, yb), f"{A25:.0f} cm", label_off=17)
    lx, ly = cv.P((0, yb))
    cv.rect_px(lx - 17, ly + 8, 34, 18, C["panel"], rx=3)   # 讓腹板虛線不穿過標字
    cv.math_px(lx, ly + 17, f"{G:.0f} cm", 14, C["dim"])
    # P：鋼板右上角，向左下 3:4
    k = 2.6
    tail = (X_R + PH * k, Y_T + PV * k)
    cv.arrow(tail, (X_R, Y_T), C["load"], 3.2, 12)
    cv.text(tail, "P = 20 tonf", 15, C["load"], "start", dx=6, dy=-10, weight="700")
    s = 0.75                                              # 斜率三角形（貼在箭線右側）
    t0 = (X_R + PH * 1.0 + 1.2, Y_T + PV * 1.0)
    t1 = (t0[0] + PH * s * 2, t0[1] + PV * s * 2)
    cn = (t1[0], t0[1])
    cv.poly([t0, cn, t1], C["load"], 1.4)
    cv.text(((t0[0] + cn[0]) / 2, t0[1]), "3", 13, C["load"], dy=11)
    cv.text((cn[0], (cn[1] + t1[1]) / 2), "4", 13, C["load"], "start", dx=6)
    # 文字標註
    lp = (X_R - 3, y_k + 2)
    cv.line(lp, (X_R + 6, y_k - 3), C["muted"], 1.1)
    cv.text((X_R + 6, y_k - 3), "厚度 15 mm 之鋼板", 13.5, C["text"], "start", dx=4)
    lc = (xr - 2, bot + 4)
    cv.line(lc, (xr + 10, bot + 2), C["muted"], 1.1)
    cv.text((xr + 10, bot + 2), "W6×25 型鋼", 13.5, C["text"], "start", dx=4)
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([panel()], cols=1,
            title="SS-2002-4 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#5；螺栓群與 25 cm 依比例，鋼板外形與柱長為示意",
            note="25 cm 由右側螺栓行量到鋼板右緣（P 作用點），不是由腹板中心或左行量起",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2002-4.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
Q_P = 20.0                                         # tf                      §1
Q_UX, Q_UY = -PH / 5.0, -PV / 5.0                   # 方向（向左下 3:4）       判讀 #5
Q_BOLTS = [(x, y) for x in (-G / 2, G / 2) for y in (-1.5 * S, -0.5 * S, 0.5 * S, 1.5 * S)]
Q_XP, Q_YP = G / 2 + A25, 1.5 * S + EDGE           # 作用點相對形心（28.5, 15.5）  §4 步驟 2
Q_PX, Q_PY = Q_P * Q_UX, Q_P * Q_UY
Q_IP = sum(x * x + y * y for x, y in Q_BOLTS)      # 588                     步驟 1
Q_M  = Q_XP * Q_PY - Q_YP * Q_PX                   # −270（順時針）            步驟 3
Q_E  = abs(Q_M) / Q_P                              # 13.5
Q_N  = len(Q_BOLTS)
def q_force(x, y):
    fx = Q_PX / Q_N - Q_M * y / Q_IP
    fy = Q_PY / Q_N + Q_M * x / Q_IP
    return fx, fy
Q_R = [(x, y, *q_force(x, y)) for x, y in Q_BOLTS]
Q_RMAX = max(math.hypot(fx, fy) for *_, fx, fy in Q_R)
Q_FV, Q_AB = 2.10, 3.88                            # t/cm²、cm²               步驟 5
Q_RV = Q_FV * Q_AB
Q_FPB = 1.2 * 4.1                                  # 1.2Fu                    步驟 5
Q_RP_COL, Q_RP_PL = Q_FPB * DB * 1.156, Q_FPB * DB * 1.5


def fig1_ecc():
    W1, H1 = 560, 560
    sx = 9.0
    cv = Canvas(W1, H1, sx=sx, ox=150, oy=250)
    cv.panel("① 扭矩 = P × 形心到力線的垂直距離", "力線方向 3:4，作用於鋼板右上角")
    for x, y in Q_BOLTS:
        cv.circle((x, y), DB / 2, fill="#FFFFFF", stroke=C["member"], w=1.8)
    cv.line((-1.2, 0), (1.2, 0), C["text"], 1.4); cv.line((0, -1.2), (0, 1.2), C["text"], 1.4)
    cv.text_px(cv.X(0) + 7, cv.Y(0) - 12, "O", 13, C["text"], "start", weight="700")
    p0 = (Q_XP, Q_YP)
    a, b = (p0[0] - 11 * Q_UX, p0[1] - 11 * Q_UY), (p0[0] + 40 * Q_UX, p0[1] + 40 * Q_UY)
    cv.line(a, b, C["ghost"], 1.4, dash="6 5")
    cv.arrow((p0[0] - 9 * Q_UX, p0[1] - 9 * Q_UY), p0, C["load"], 3.2, 11)
    cv.text_px(cv.X(p0[0] - 9 * Q_UX) + 8, cv.Y(p0[1] - 9 * Q_UY), f"P = {Q_P:g} tf", 13.5, C["load"], "start", weight="700")
    cv.dot(p0, 4.5, fill=C["load"])
    cv.text_px(cv.X(p0[0]) + 10, cv.Y(p0[1]) + 16, f"({Q_XP:g}, {Q_YP:g})", 12, C["muted"], "start")
    t = -(p0[0] * Q_UX + p0[1] * Q_UY)
    foot = (p0[0] + t * Q_UX, p0[1] + t * Q_UY)
    cv.line((0, 0), foot, C["accent"], 2.6)
    # 直角記號
    k = 1.4
    nx, ny = -foot[0] / Q_E, -foot[1] / Q_E
    c1 = (foot[0] + k * nx, foot[1] + k * ny); c2 = (c1[0] - k * Q_UX, c1[1] - k * Q_UY); c3 = (foot[0] - k * Q_UX, foot[1] - k * Q_UY)
    cv.poly([c1, c2, c3], C["accent"], 1.4)
    mid = (foot[0] / 2, foot[1] / 2)
    cv.text_px(cv.X(mid[0]) + 12, cv.Y(mid[1]) + 4, f"e = {Q_E:.1f} cm", 14, C["accent"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 56, f"M = P·e = {Q_P:g} × {Q_E:.1f} = {abs(Q_M):.0f} tf·cm（順時針）", 14, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, f"Ip = Σx² + Σy² = {Q_IP:.0f} cm²（8 顆）", 12.5, C["muted"])
    p1 = cv

    cv = Canvas(W1, H1, sx=1)
    cv.panel("② 分量取矩：兩個分量的力矩方向相反", "第二條路徑，結果必須與 ① 相同")
    x0, sc = 210, 0.38
    rows = ((f"Py × xP = {abs(Q_PY):g} × {Q_XP:g}", abs(Q_PY) * Q_XP, C["load"], "順時針"),
            (f"Px × yP = {abs(Q_PX):g} × {Q_YP:g}", abs(Q_PX) * Q_YP, C["compr"], "逆時針"),
            ("淨扭矩 M", abs(Q_M), C["accent"], "順時針"),
            (f"誤：P × xP = {Q_P:g} × {Q_XP:g}", Q_P * Q_XP, C["ghost"], "誤"))
    for i, (nm, v, col, dirn) in enumerate(rows):
        y = 140 + i * 74
        cv.text_px(x0 - 12, y, nm, 12.5, C["text"] if i < 3 else C["muted"], "end", weight="700" if i == 2 else "400")
        cv.rect_px(x0, y - 14, sc * v, 28, col, 4)
        cv.text_px(x0 + sc * v + 8, y, f"{v:.0f}（{dirn}）", 12.5, col if i < 3 else C["muted"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 56, f"{abs(Q_PY) * Q_XP:.0f} − {abs(Q_PX) * Q_YP:.0f} = {abs(Q_M):.0f} tf·cm ✓ 與 P·e 相同", 13.5, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, "水平分量把扭矩抵掉四成——只看垂直分量會高估 69%", 12.5, C["muted"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-1-ecc.svg")
    compose([p1, p2], cols=2,
            title=f"圖 1　偏心距 e = {Q_E:.1f} cm，扭矩 M = {abs(Q_M):.0f} tf·cm",
            sub=f"O＝螺栓群形心；P = {Q_P:g} tf：Px = {abs(Q_PX):g} tf（←）、Py = {abs(Q_PY):g} tf（↓）；作用點相對形心 ({Q_XP:g}, {Q_YP:g}) cm",
            note="斜向載重的偏心距是形心到力線的垂直距離，不是作用點的水平或垂直座標",
            path=path)
    return path


def fig2_forces():
    W1, H1 = 560, 600
    sx = 13.0
    cv = Canvas(W1, H1, sx=sx, ox=230, oy=310)
    cv.panel("① 各螺栓合力（直接剪力＋扭矩剪力）", "箭頭長度與合力大小成比例")
    vs = 7.0 / Q_RMAX * 1.0
    for x, y, fx, fy in Q_R:
        r = math.hypot(fx, fy)
        crit = abs(r - Q_RMAX) < 1e-9
        cv.circle((x, y), DB / 2, fill="#FFFFFF", stroke=C["member"], w=1.8)
        tip = (x + vs * fx, y + vs * fy)
        cv.arrow((x, y), tip, C["load"] if crit else C["bmd"], 3.0 if crit else 2.2, 9)
        dx = 8 if fx >= 0 else -8
        cv.text_px(cv.X(tip[0]) + dx, cv.Y(tip[1]) + (14 if fy < 0 else -10), f"{r:.2f}", 12,
                   C["load"] if crit else C["bmd"], "start" if fx >= 0 else "end", weight="700")
    # 臨界螺栓的分量
    xc, yc, fxc, fyc = max(Q_R, key=lambda q: math.hypot(q[2], q[3]))
    dd = (Q_PX / Q_N * vs, Q_PY / Q_N * vs)
    cv.arrow((xc, yc), (xc + dd[0], yc + dd[1]), C["muted"], 1.6, 7, dash="4 3")
    cv.arrow((xc + dd[0], yc + dd[1]), (xc + vs * fxc, yc + vs * fyc), C["sfd"], 1.6, 7, dash="4 3")
    cv.line((-1, 0), (1, 0), C["text"], 1.2); cv.line((0, -1), (0, 1), C["text"], 1.2)
    cv.legend(40, H1 - 96, [(C["muted"], f"直接剪力 P/n = {Q_P / Q_N:.1f} tf"), (C["sfd"], "扭矩剪力 ⊥ 半徑")], size=12, gap=19)
    cv.text_px(W1 / 2, H1 - 30, "右下角：扭矩剪力與直接剪力方向最接近 ⇒ 合力最大", 12.5, C["muted"])
    p1 = cv

    cv = Canvas(W1, H1, sx=1)
    cv.panel("② 最大螺栓力與容許值（tf）", "取剪力與承壓的較小者")
    x0, sc = 190, 18.0
    rows = (("最大螺栓力", Q_RMAX, C["load"]), ("單剪 Fv·Ab", Q_RV, C["bmd"]),
            ("承壓（柱翼板）", Q_RP_COL, C["compr"]), ("承壓（鋼板）", Q_RP_PL, C["ghost"]))
    for i, (nm, v, col) in enumerate(rows):
        y = 150 + i * 80
        cv.text_px(x0 - 12, y, nm, 13, C["text"], "end", weight="700")
        cv.rect_px(x0, y - 15, sc * v, 30, col, 4)
        cv.text_px(x0 + sc * v - 10, y, f"{v:.3f}" if i == 1 else f"{v:.2f}", 13, "#FFFFFF" if i < 3 else C["text"], "end", weight="700")
    _hl(cv, H1, x0 + sc * Q_RV, 120, x0 + sc * Q_RV, 430, C["bmd"], 1.6, dash="5 4")
    cv.text_px(W1 / 2, H1 - 56, f"{Q_RMAX:.2f} ≤ {Q_RV:.3f}（剪力控制），比值 {Q_RMAX / Q_RV:.2f} ⇒ O.K.", 14, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, "承壓容量遠大於剪力——控制的是螺栓本身", 12.5, C["muted"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-2-forces.svg")
    compose([p1, p2], cols=2,
            title=f"圖 2　最不利螺栓在右下角：R = {Q_RMAX:.2f} tf ≤ {Q_RV:.3f} tf",
            sub=f"f = P/n ＋ M·r/Ip（M = {abs(Q_M):.0f} tf·cm、Ip = {Q_IP:.0f} cm²）",
            note="扭矩剪力最大的是四個角點，但只有右下角的扭矩剪力與直接剪力同向相加",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "25 cm 起點讀成腹板中心或左行（偏心差 3.5 或 7 cm）；P 斜率 3:4 讀反成水平 4、垂直 3"),
    (fig1_ecc, "§4 步驟 2–3",
     "以作用點座標當力臂（P × 28.5 = 570）或只取一個分量的力矩，扭矩高估"),
    (fig2_forces, "§4 步驟 4–6",
     "選錯臨界螺栓（取右上角）；以承壓而非剪力為控制"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
