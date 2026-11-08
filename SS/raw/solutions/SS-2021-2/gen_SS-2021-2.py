#!/usr/bin/env python3
"""
SS-2021-2 填角銲疊接拉力構材之斷裂與塊狀剪力模式 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2021-2.py [輸出目錄]

重繪依據：題目正本 SS-2021-2-problem.md §4 判讀清單（2026-11-02 已確認）。
只畫考卷給的東西；不畫破壞模式（那是本題所求）。節點板外形為示意，受拉板寬與疊接長依比例。單位 mm。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2021-2"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2021-2-problem.md §4，已確認）；單位 mm
# ══════════════════════════════════════════════════════════
T_PL, T_GU = 20, 25        # #1 t = 20 mm 受拉板（右端受 P）；t = 25 mm 梯形節點板（左端承接）
W_PL = 100.0               # #2 受拉板寬 100
L_OV = 150.0               # #3 疊接長＝縱向銲道長 150 mm
RET = 8.0                  # #4 板端兩角短回銲（長度示意）；板端無橫向銲


def fig1_problem():
    W, H, sx = 760, 470, 1.15
    cv = Canvas(W, H, sx=sx, ox=300, oy=H / 2 - 30)
    cv.panel("圖二　疊接", "節點板外形示意；受拉板寬與疊接長依比例")
    gu = [(-130, -150), (-130, 150), (L_OV, 85), (L_OV, -85)]
    cv.polygon(gu, C["border"], C["member"], 1.8)
    pl = [(0, -W_PL / 2), (L_OV + 120, -W_PL / 2), (L_OV + 120, W_PL / 2), (0, W_PL / 2)]
    cv.polygon(pl, C["fill_c"], C["member"], 1.8)
    cv.line((L_OV, -W_PL / 2), (L_OV, W_PL / 2), C["member"], 1.4, dash="6 4")   # 節點板右緣（被遮）
    for y in (-W_PL / 2, W_PL / 2):
        cv.line((0, y), (L_OV, y), C["load"], 5, cap="butt")                     # 縱向填角銲
        cv.line((0, y), (0, y - RET * (1 if y > 0 else -1)), C["load"], 5, cap="butt")  # 回銲
    cv.arrow((L_OV + 125, 0), (L_OV + 185, 0), C["load"], 3.2, 12)
    cv.math((L_OV + 185, 0), "P", 16, C["load"], "start", dx=8, weight="700")
    cv.arrow((-135, 0), (-195, 0), C["load"], 3.2, 12)
    cv.text((-60, 85), f"t={T_GU} mm", 13, C["text"], weight="700")
    cv.text((75, 0), f"t={T_PL} mm", 13, C["text"], weight="700")
    cv.dim((0, -W_PL / 2), (0, W_PL / 2), f"{W_PL:.0f}", off=-28, label_off=-18)
    cv.dim((0, -W_PL / 2), (L_OV, -W_PL / 2), f"{L_OV:.0f} mm", off=34, label_off=16)
    cv.text((L_OV / 2, W_PL / 2), "縱向填角銲（兩道）", 12.5, C["load"], dy=-14, weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title="SS-2021-2 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#4；只畫考卷所給條件（破壞模式為本題所求，不畫）",
            note="銲道只沿受拉板上下兩緣（長 150 mm），板端只有兩角短回銲、無橫向銲",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2021-2.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
Q_FY, Q_FU = 2.5, 4.1                    # t/cm²（§4 數值示意）
Q_W, Q_L = W_PL / 10, L_OV / 10          # cm
Q_TP, Q_TG = T_PL / 10, T_GU / 10
Q_U = 0.87                               # l/w = 1.5 → 0.87
Q_AG = Q_W * Q_TP
Q_AE = Q_U * Q_AG
Q_PY = 0.9 * Q_FY * Q_AG
Q_PR = 0.75 * Q_FU * Q_AE
Q_AGV = 2 * Q_L * Q_TG                   # 75
Q_AGT = Q_W * Q_TG                       # 25
Q_FT = Q_FU * Q_AGT                      # 102.5
Q_FV = 0.6 * Q_FU * Q_AGV                # 184.5
Q_E1 = 0.6 * Q_FY * Q_AGV + Q_FT         # 215.0
Q_E2 = Q_FV + Q_FY * Q_AGT               # 247.0
Q_CAP = Q_FV + Q_FT                      # 287.0
Q_RN = min(Q_E2 if Q_FV > Q_FT else Q_E1, Q_CAP)
Q_PHIRN = 0.75 * Q_RN                    # 185.3


def _plan(title, sub, mode):
    W1, H1 = 520, 440
    cv = Canvas(W1, H1, sx=1.2, ox=310, oy=H1 / 2 - 30)
    cv.panel(title, sub)
    g = [(-230, -110), (0, -85), (0, 85), (-230, 110)]
    cv.polygon(g, "rgba(63,74,90,0.10)", C["member"], 1.4)
    cv.text((-215, 95), "節點板 t = 25", 12, C["muted"], "start")
    cv.polygon([(-L_OV, -W_PL / 2), (95, -W_PL / 2), (95, W_PL / 2), (-L_OV, W_PL / 2)], C["fill_c"], C["member"], 1.6)
    cv.text((48, 0), "受拉板 t = 20", 12, C["text"])
    for y in (W_PL / 2, -W_PL / 2):
        cv.line((-L_OV, y), (0, y), C["text"], 4.5, cap="butt")
    cv.arrow((97, 0), (140, 0), C["load"], 3, 10)
    cv.text((140, 0), "P", 14, C["load"], "start", dx=6, weight="700")
    if mode == "A":
        cv.line((0, -W_PL / 2 - 14), (0, W_PL / 2 + 14), C["load"], 3, dash="7 4", cap="butt")
        cv.text((0, -W_PL / 2 - 14), "整寬 100 斷開", 12.5, C["load"], dy=18, weight="700")
        cv.text_px(W1 / 2, H1 - 56, f"Ae = U·Ag = {Q_U} × {Q_AG:g} = {Q_AE:.1f} cm²（l/w = {Q_L / Q_W:g}）", 12.5, C["text"], weight="700")
        cv.text_px(W1 / 2, H1 - 30, f"φPn 斷裂 {Q_PR:.1f} t；降伏 {Q_PY:.1f} t 較小", 12.5, C["muted"])
    else:
        cv.polygon([(-L_OV, -W_PL / 2), (0, -W_PL / 2), (0, W_PL / 2), (-L_OV, W_PL / 2)], "rgba(192,57,43,0.18)", "none")
        for y in (W_PL / 2, -W_PL / 2):
            cv.line((-L_OV, y), (0, y), C["load"], 3, dash="7 4", cap="butt")
        cv.line((-L_OV, -W_PL / 2), (-L_OV, W_PL / 2), C["sfd"], 3, dash="7 4", cap="butt")
        cv.text((-L_OV / 2, W_PL / 2), "剪力面 150", 12, C["load"], dy=-14, weight="700")
        cv.text((-L_OV / 2, -W_PL / 2), "剪力面 150", 12, C["load"], dy=18, weight="700")
        cv.text((-L_OV, 0), "拉力面 100", 12, C["sfd"], "end", dx=-8, weight="700")
        cv.text_px(W1 / 2, H1 - 56, f"Agv = 2 × {Q_L:g} × {Q_TG} = {Q_AGV:g}、Agt = {Q_W:g} × {Q_TG} = {Q_AGT:g} cm²", 12.5, C["text"], weight="700")
        cv.text_px(W1 / 2, H1 - 30, "節點板上被兩道銲線圍住的塊，連同受拉板被拉出", 12.5, C["muted"])
    return cv


def fig1_modes():
    path = os.path.join(OUT, f"{TAG}-fig-1-modes.svg")
    compose([_plan("(A) 受拉板拉力斷裂", "受拉板離開節點板處、整寬橫斷", "A"),
             _plan("(B) 節點板塊狀剪力", "兩條剪力面（沿銲道）＋ 一條拉力面", "B")], cols=2,
            title="圖 1　兩種破壞模式：斷裂在受拉板（t = 20），塊狀剪力在節點板（t = 25）",
            sub="平面示意（mm）；粗黑線為兩緣縱向銲道 150",
            note="受拉板整寬都在兩道銲線之間、左端是自由邊，沒有拉力面可撕，所以它不會發生 U 形塊狀剪力",
            path=path)
    return path


def fig2_block():
    W1, H1 = 1000, 470
    cv = Canvas(W1, H1, sx=1)
    cv.panel("塊狀剪力：先比斷裂項，決定用式(1) 或式(2)", f"節點板 Fy = {Q_FY}、Fu = {Q_FU} t/cm²（數值示意）")
    x0, sc = 260, 1.9
    rows = [("拉力面斷裂 Fu·Ant", [(Q_FT, C["sfd"], f"{Q_FT:.1f}")], None),
            ("剪力面斷裂 0.6Fu·Anv", [(Q_FV, C["load"], f"{Q_FV:.1f}")], "較大 → 剪力面斷裂"),
            ("式(1) 0.6Fy·Agv + Fu·Ant", [(0.6 * Q_FY * Q_AGV, C["ghost"], f"{0.6 * Q_FY * Q_AGV:.1f}"), (Q_FT, C["ghost"], f"{Q_FT:.1f}")], f"= {Q_E1:.1f}（不採用）"),
            ("式(2) 0.6Fu·Anv + Fy·Agt", [(Q_FV, C["load"], f"{Q_FV:.1f}"), (Q_FY * Q_AGT, C["compr"], f"{Q_FY * Q_AGT:.1f}")], f"= {Q_E2:.1f} ✓"),
            ("上限 0.6Fu·Anv + Fu·Ant", [(Q_FV, C["ghost"], f"{Q_FV:.1f}"), (Q_FT, C["ghost"], f"{Q_FT:.1f}")], f"= {Q_CAP:.1f}（不控制）")]
    for i, (lab, segs, tail) in enumerate(rows):
        y = 140 + i * 56
        cv.text_px(x0 - 12, y, lab, 13, C["text"], "end", weight="700")
        xx = x0
        for v, col, s in segs:
            cv.rect_px(xx, y - 15, sc * v - 2, 30, col, 3)
            cv.text_px(xx + sc * v / 2, y, s, 12, "#FFFFFF" if col != C["ghost"] else C["text"], weight="700")
            xx += sc * v
        if tail:
            cv.text_px(xx + 10, y, tail, 13, C["bmd"] if "✓" in tail else C["muted"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 32, f"φRn = 0.75 × {Q_RN:.1f} = {round(Q_PHIRN + 1e-9, 1):.1f} t", 15, C["bmd"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-2-block.svg")
    compose([cv], cols=1,
            title=f"圖 2　0.6Fu·Anv = {Q_FV:.1f} 大於 Fu·Ant = {Q_FT:.1f}：剪力面斷裂、拉力面降伏，用式(2) = {Q_E2:.1f} t",
            sub="擇一：斷裂發生在斷裂項較大的那一面，另一面此時已降伏",
            note="兩式都算再取大或取小都不對；上限防止降伏項比同一面的斷裂項還大（本題無孔，上限不控制）",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把板端當成有橫向銲；把 t = 20、25 mm 的板對調"),
    (fig1_modes, "§4 一",
     "斷裂畫在節點板；塊狀剪力畫在受拉板；拉力面放錯位置"),
    (fig2_block, "§4 一（數值示意）、三",
     "兩式都算後取大或取小；擇一依據比成降伏項；上限誤以為會控制"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
