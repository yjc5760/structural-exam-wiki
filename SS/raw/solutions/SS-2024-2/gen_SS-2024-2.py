#!/usr/bin/env python3
"""
SS-2024-2 圓管與十字形連接板之縱向填角銲接頭 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2024-2.py [輸出目錄]

重繪依據：題目正本 SS-2024-2-problem.md §4 判讀清單（2026-11-02 已確認）。
只畫考卷給的東西；銲腳尺寸為㈡所求，不標數值。附圖內的填角銲最小尺寸表已照錄於題目正本 §2，不重繪。
斷面依比例；側視圖連接板外形與管長為示意。單位 mm。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2024-2"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2024-2-problem.md §4，已確認）；單位 mm
# ══════════════════════════════════════════════════════════
D = 273.0                 # 題文 D = 273
T_PIPE = 10.0             # #4 管壁厚 10（STK273×10）
T_G = 20.0                # 題文 t_g = 20
N_WELD = 8                # #1 十字板四支 × 管外兩側 = 8 道
L_W = D                   # #2 每道 L = D
SLOT = 22.0               # #3 槽端半圓孔徑 22，槽端在銲道區之外
ARM = 165.0               # 十字板伸出長度（示意）
LEG = 18.0                # 銲道三角形大小（示意；銲腳為㈡所求）


def section_panel():
    W, H, sx = 460, 480, 0.9
    cv = Canvas(W, H, sx=sx, ox=W / 2, oy=H / 2 - 30)
    cv.panel("斷面", "依比例；黑色三角形為填角銲（8 道）")
    R = D / 2
    cv.circle((0, 0), R, fill=C["fill_c"], stroke=C["member"], w=1.8)
    cv.circle((0, 0), R - T_PIPE, fill=C["panel"], stroke=C["member"], w=1.8)
    for ang in (0, 90):
        a = math.radians(ang)
        ux, uy = math.cos(a), math.sin(a)
        nx, ny = -uy, ux
        p = [(-ARM * ux + T_G / 2 * nx, -ARM * uy + T_G / 2 * ny), (ARM * ux + T_G / 2 * nx, ARM * uy + T_G / 2 * ny),
             (ARM * ux - T_G / 2 * nx, ARM * uy - T_G / 2 * ny), (-ARM * ux - T_G / 2 * nx, -ARM * uy - T_G / 2 * ny)]
        cv.polygon(p, C["border"], C["member"], 1.6)
    k = 0
    for ang in (0, 90, 180, 270):
        a = math.radians(ang)
        ux, uy = math.cos(a), math.sin(a)
        nx, ny = -uy, ux
        for s in (1, -1):
            bx, by = R * ux + s * T_G / 2 * nx, R * uy + s * T_G / 2 * ny
            tri = [(bx, by), (bx + LEG * ux, by + LEG * uy), (bx + s * LEG * nx, by + s * LEG * ny)]
            cv.polygon(tri, C["text"], C["text"], 1)
            k += 1
    assert k == N_WELD
    cv.dim((-R, R), (R, R), "D", off=-60, label_off=-14)
    cv.arrow((-40, -60), (-T_G / 2, -60), C["dim"], 1.2, 7)
    cv.arrow((40, -60), (T_G / 2, -60), C["dim"], 1.2, 7)
    cv.math((40, -60), "t_{g}", 14, C["dim"], "start", dx=6)
    cv.text_px(W / 2, H - 30, "STK273×10", 13, C["muted"])
    return cv


def side_panel():
    W, H, sx = 460, 480, 0.72
    cv = Canvas(W, H, sx=sx, ox=100, oy=H / 2 - 20)
    cv.panel("側視", "連接板插入管端開槽；粗黑線為銲道")
    R = D / 2
    cv.polygon([(-90, -R - 30), (L_W + SLOT, -R - 30), (L_W + SLOT, R + 30), (-90, R + 30)],
               C["border"], C["member"], 1.4)
    for y in (-R, R):
        cv.line((0, y), (L_W + 130, y), C["member"], 1.8)
    for y in (-R, R):
        cv.line((L_W + SLOT / 2, y), (L_W + 130, y), C["muted"], 1.0, dash="5 4")
    for y in (-R + 6, -T_G / 2 - 6, T_G / 2 + 6, R - 6):
        cv.line((0, y), (L_W, y), C["text"], 8, cap="butt")
    cv.circle((L_W + SLOT / 2, 0), SLOT / 2, stroke=C["member"], w=1.4)
    cv.dim((0, R + 30), (L_W, R + 30), "L = D", off=-22, label_off=-14)
    cv.text((L_W + SLOT / 2, 0), "半圓孔徑 = 22mm", 12.5, C["accent"], "middle", dy=-28, weight="700")
    cv.text((-45, 0), "十字形連接板", 12.5, C["text"], dy=-60, weight="700")
    cv.text((L_W + 80, -R), "圓管", 13, C["text"], dy=-16, weight="700")
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([section_panel(), side_panel()], cols=2,
            title="SS-2024-2 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#4；填角銲最小尺寸表已照錄於題目正本 §2",
            note="十字板四支、每支管外兩側各一道，共 8 道；每道長 L = D = 273 mm；槽端在銲道區之外",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2024-2.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
Q_FY, Q_FU = 2.3, 3.1                    # t/cm²（STK400）          §4 Step 1–2
Q_AG = 82.6                              # cm²（題給）
Q_DC, Q_TC = D / 10, T_PIPE / 10         # cm
Q_N_SLOT, Q_W_SLOT = 4, SLOT / 10
Q_AN = Q_AG - Q_N_SLOT * Q_W_SLOT * Q_TC                 # 73.8
Q_XB = Q_DC / math.pi                                    # 8.69
Q_U = 1 - Q_XB / Q_DC                                    # 0.682
Q_AE = round(Q_U, 3) * Q_AN                              # 50.3
Q_T1 = 0.90 * Q_FY * Q_AG                                # 171.0
Q_T2 = 0.75 * Q_FU * Q_U * Q_AN                          # 117.0（Ae 不先捨位）
Q_SW = N_WELD * Q_DC                                     # 218.4
Q_T3 = 0.75 * 0.6 * Q_FU * Q_SW * Q_TC                   # 304.7
Q_TU = min(Q_T1, Q_T2, Q_T3)
Q_FEXX = 4.92
Q_KW = 0.75 * 0.6 * Q_FEXX * 0.707                       # 1.566 t/cm per cm leg
Q_WREQ = Q_TU / (round(Q_KW, 3) * Q_SW) * 10             # 3.4 mm
Q_WMIN = 8.0
Q_WMAX = 0.75 * 0.6 * Q_FU * Q_TC / round(Q_KW, 3) * 10  # 8.9 mm


def fig1_shearlag():
    W1, H1 = 520, 480
    cv = Canvas(W1, H1, sx=0.95, ox=W1 / 2, oy=H1 / 2 - 12)
    cv.panel("剪力遲滯：半圓管形心到板面 x̄ = D/π", "以一支板為界，半圓管的力要經板傳遞")
    R = D / 2
    pts = [(R * math.cos(math.pi * i / 60), R * math.sin(math.pi * i / 60)) for i in range(61)]
    pin = [((R - T_PIPE) * math.cos(math.pi * i / 60), (R - T_PIPE) * math.sin(math.pi * i / 60)) for i in range(61)]
    cv.polygon(pts + pin[::-1], "rgba(192,57,43,0.25)", "none")
    cv.circle((0, 0), R, stroke=C["member"], w=1.8)
    cv.circle((0, 0), R - T_PIPE, stroke=C["member"], w=1.4)
    cv.polygon([(-ARM, -T_G / 2), (ARM, -T_G / 2), (ARM, T_G / 2), (-ARM, T_G / 2)], C["border"], C["member"], 1.4)
    cv.polygon([(-T_G / 2, -ARM), (T_G / 2, -ARM), (T_G / 2, ARM), (-T_G / 2, ARM)], C["border"], C["member"], 1.4)
    xb = D / math.pi
    cv.dot((0, xb), 6, fill=C["load"])
    cv.dim((0, T_G / 2), (0, xb), f"{Q_XB:.2f}", off=-55, label_off=-24)
    cv.text((0, xb), "半圓管形心", 12, C["load"], "start", dx=16, dy=-2, weight="700")
    cv.text_px(W1 / 2, H1 - 48, f"U = 1 − x̄/L = 1 − {Q_XB:.2f}/{Q_DC:g} = {Q_U:.3f}（L = D）", 13, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 24, f"An = {Q_AG} − 4 × {Q_W_SLOT} × {Q_TC:g} = {Q_AN:.1f}；Ae = {Q_AE:.1f} cm²", 12.5, C["muted"])
    p1 = cv
    W2 = 520
    cv = Canvas(W2, H1, sx=1)
    cv.panel("拉力設計強度 φTn（t）", "三種極限狀態取小")
    x0, sc = 40, 1.25
    rows = [("全斷面降伏 0.90FyAg", Q_T1), ("淨斷面斷裂 0.75FuAe", Q_T2), ("管壁沿銲道剪撕 0.75(0.6Fu)Anv", Q_T3)]
    for i, (lab, v) in enumerate(rows):
        y = 140 + i * 90
        ctrl = v == Q_TU
        cv.text_px(x0, y - 24, lab, 12.5, C["text"], "start")
        cv.rect_px(x0, y - 12, sc * v, 24, C["load"] if ctrl else C["ghost"], 3)
        cv.text_px(x0 + sc * v + 8 if sc * v < 400 else x0 + sc * v - 8, y, f"{v:.1f}" + ("（控制）" if ctrl else ""),
                   13, C["load"] if ctrl else C["muted"], "start" if sc * v < 400 else "end", weight="700")
    cv.text_px(W2 / 2, H1 - 36, f"φTn = {Q_TU:.1f} t，作為（二）銲道設計力", 13.5, C["bmd"], weight="700")
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-1-shearlag.svg")
    compose([p1, p2], cols=2,
            title=f"圖 1　U = {Q_U:.3f}、Ae = {Q_AE:.1f} cm²：淨斷面斷裂控制，φTn = {Q_TU:.1f} t",
            sub="開槽扣 4 道 × 22 mm；x̄ 用半圓管形心（題目給定），不是整管形心",
            note="U 取 1.0（忘了剪力遲滯）會得 171.6 t，高估約 47%；x̄ 若量到管中心（= 0）也是同樣錯誤",
            path=path)
    return path


def fig2_weld():
    W1, H1 = 1000, 420
    cv = Canvas(W1, H1, sx=1)
    cv.panel("（二）填角銲腳 w（mm）的上下限", f"8 道 × {Q_DC:g} cm = {Q_SW:.1f} cm；φRw = 0.75 × 0.6FEXX × 0.707w = {Q_KW:.3f}w t/cm")
    X0, X1, Y = 120, 880, 240
    wmax = 12.0
    PX = lambda w: X0 + (X1 - X0) * w / wmax
    _hl(cv, H1, X0, Y, X1, Y, C["muted"], 2)
    for w in range(0, 13, 2):
        _hl(cv, H1, PX(w), Y - 6, PX(w), Y + 6, C["muted"], 1.2)
        cv.text_px(PX(w), Y + 24, f"{w}", 11.5, C["muted"])
    cv.rect_px(PX(Q_WMIN), Y - 16, PX(Q_WMAX) - PX(Q_WMIN), 32, "rgba(46,125,50,0.25)", 2)
    marks = [(Q_WREQ, f"強度需求 {Q_WREQ:.1f}", C["compr"], -46), (Q_WMIN, f"最小銲腳 {Q_WMIN:g}（tg = 20 查表）", C["bmd"], -76),
             (Q_WMAX, f"上限 {Q_WMAX:.1f}（不強於管壁）", C["load"], 52)]
    for w, lab, col, dy in marks:
        _hl(cv, H1, PX(w), Y - 20, PX(w), Y + 20, col, 2.4)
        cv.text_px(PX(w), Y + dy, lab, 12.5, col, weight="700")
    cv.text_px(W1 / 2, H1 - 40, f"取 w = max({Q_WREQ:.1f}, {Q_WMIN:g}) = 8 mm ≤ {Q_WMAX:.1f} ✓；8 mm 銲道強度 {round(Q_KW, 3) * 0.8 * Q_SW:.1f} t ≫ {Q_TU:.1f} t", 13.5, C["bmd"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-2-weld.svg")
    compose([cv], cols=1,
            title="圖 2　銲腳由最小銲腳 8 mm 控制，落在強度需求 3.4 與母材上限 8.9 之間",
            sub=f"w_req = {Q_TU:.1f} / ({Q_KW:.3f} × {Q_SW:.1f})；上限：{Q_KW:.3f}w ≤ 0.75 × 0.6 × {Q_FU} × {Q_TC:g}",
            note="最小銲腳依較厚板（連接板 20 mm）查表，且不超過較薄板（管壁 10 mm）；只算強度會得 3.4 mm，不符最小銲腳",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "銲道數算成 4 道；銲長不等於 D；把開槽當成在銲道區內"),
    (fig1_shearlag, "§4（一）Step 1–4",
     "U 取 1.0；x̄ 量到管中心；開槽未扣；只算全斷面降伏"),
    (fig2_weld, "§4（二）Step 5–10",
     "只算強度需求 3.4 mm；最小銲腳查較薄板；忘了不強於母材的上限"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
