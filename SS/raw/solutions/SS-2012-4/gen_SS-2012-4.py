#!/usr/bin/env python3
"""
SS-2012-4 梁柱接頭剪力板栓接設計（LRFD）— 題目附圖重繪腳本

用法：
    python3 gen_SS-2012-4.py [輸出目錄]

重繪依據：題目正本 SS-2012-4-problem.md §4 判讀清單（待確認）。
只畫考卷附圖所示：柱、梁（翼板延伸至柱面）、剪力板 180 mm（沿梁深）× 80 mm（自柱面向外）。
剪力板依比例；梁深、柱深、翼板厚與構材長度為示意（考卷未給）。
螺栓數目與配置為所求，考卷附圖未畫，本圖亦不畫（題文另指定螺栓線距柱面 40 mm）。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2012-4"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2012-4-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
HP = 180.0          # #1 剪力板沿梁深方向 180 mm（「長」）
WP = 80.0           # #1 剪力板自柱面向外 80 mm（「寬」）
#                     #2 螺栓單行、距柱面 40 mm（題文；為考生配置，不畫）
# 示意（考卷未給）：
DB, TFB = 280.0, 12.0   # 梁深、梁翼板厚
DC, TFC = 175.0, 12.0   # 柱深、柱翼板厚
LB = 260.0              # 梁畫出長度
HC = 40.0               # 柱伸出梁翼外的長度

PW, PHT = 900, 700


def _rect(cv, x0, x1, y0, y1, fill="#FFFFFF", w=1.8):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, C["member"], w)


def panel():
    sx = 1.25
    cv = Canvas(PW, PHT, sx=sx, ox=360, oy=170)
    cv.panel("梁柱接頭立面", "單位：mm")
    top, bot = DB + HC, -HC
    # 柱兩翼板（雙線）
    for x0 in (-DC, -TFC):
        _rect(cv, x0, x0 + TFC, bot, top)
    for yy in (top, bot):
        xm = -DC / 2
        cv.poly([(-DC - 15, yy), (xm - 10, yy), (xm - 3, yy + 18), (xm + 3, yy - 18), (xm + 10, yy),
                 (15, yy)], C["member"], 1.8)
    # 梁翼板：延伸穿過柱（柱內為連續板）至梁端
    for y0 in (0.0, DB - TFB):
        _rect(cv, -DC + TFC, -TFC, y0, y0 + TFB)
        _rect(cv, 0, LB, y0, y0 + TFB)
    # 梁端斷裂線
    ym = DB / 2
    cv.poly([(LB, -6), (LB, ym - 18), (LB + 12, ym - 6), (LB - 12, ym + 6), (LB, ym + 18), (LB, DB + 6)],
            C["member"], 1.8)
    # 剪力板
    y0 = (DB - HP) / 2
    _rect(cv, 0, WP, y0, y0 + HP, C["fill_c"], 2.2)
    # 尺寸
    xd = WP + 40
    for yy in (y0, y0 + HP):
        cv.line((WP, yy), (xd + 8, yy), C["dim"], 1, dash="3 3")
    cv.dim((xd, y0 + HP), (xd, y0), f"{HP:.0f}", label_off=-24, size=16)
    yd = bot - 10
    cv.line((0, bot), (0, yd - 6), C["dim"], 1, dash="3 3")
    cv.line((WP, y0), (WP, yd - 6), C["dim"], 1, dash="3 3")
    cv.dim((0, yd), (WP, yd), f"{WP:.0f}", label_off=18, size=16)
    # 標註
    cv.line((WP * 0.55, y0 + HP), (WP * 0.9, DB + HC + 10), C["muted"], 1.1)
    cv.text((WP * 0.9, DB + HC + 10), "剪力板", 16, C["text"], "start", dx=4)
    cv.line((-DC + TFC / 2, DB * 0.35), (-DC - 45, DB * 0.2), C["muted"], 1.1)
    cv.text((-DC - 45, DB * 0.2), "柱", 16, C["text"], "end", dx=-4)
    cv.line((LB * 0.7, 0), (LB * 0.7 + 20, -40), C["muted"], 1.1)
    cv.text((LB * 0.7 + 20, -40), "梁", 16, C["text"], "start", dx=4)
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([panel()], cols=1,
            title="SS-2012-4 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1；剪力板依比例，梁深、柱深與構材長度為示意；螺栓配置為所求（不畫）",
            note="180 mm 是沿梁深的板長、80 mm 是自柱面向外的板寬；螺栓線距柱面 40 mm（題文）",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2012-4.md §4，由下式即時算出
# 座標：x 自柱面向外（mm）、y 自板底向上（mm）
# ══════════════════════════════════════════════════════════════
import math
Q_VU, Q_D, Q_FNV = 180.0, 20.0, 330.0            # kN、mm、MPa                  §1
Q_FU, Q_FY, Q_PHI = 400.0, 248.0, 0.75           # MPa                           §1
Q_XB = 40.0                                      # 螺栓距柱面                    §1
Q_AB = math.pi * Q_D ** 2 / 4
Q_RB = Q_PHI * Q_FNV * Q_AB / 1e3                # 77.75 kN/顆                   Step 1
Q_N  = math.ceil(Q_VU / Q_RB)                    # 3                             Step 2
Q_LE, Q_S = 1.5 * Q_D, 3 * Q_D                   # 30、60                        Step 3
Q_YS = [Q_LE + k * Q_S for k in range(Q_N)]      # 30、90、150
Q_DH = Q_D + 2                                   # 22                            Step 4
Q_LC_E, Q_LC_I = Q_LE - Q_DH / 2, Q_S - Q_DH     # 19、38
Q_RN_E = min(1.2 * Q_LC_E * Q_FU, 2.4 * Q_D * Q_FU)   # ×t（N/mm）
Q_RN_I = min(1.2 * Q_LC_I * Q_FU, 2.4 * Q_D * Q_FU)
Q_BRG = Q_PHI * (2 * Q_RN_E + (Q_N - 2) * Q_RN_I)     # 27,360 t
Q_RUP = Q_PHI * 0.6 * Q_FU * (HP - Q_N * Q_DH)        # 20,520 t              Step 5
Q_YLD = 0.9 * 0.6 * Q_FY * HP                         # 24,106 t              Step 6
Q_TREQ = {"承壓": Q_VU * 1e3 / Q_BRG, "剪力降伏": Q_VU * 1e3 / Q_YLD, "淨斷面剪力破壞": Q_VU * 1e3 / Q_RUP}
Q_TUSE = 10.0
Q_CAPS = {"螺栓剪力": Q_N * Q_RB, "承壓": Q_BRG * Q_TUSE / 1e3, "剪力降伏": Q_YLD * Q_TUSE / 1e3,
          "淨斷面剪力破壞": Q_RUP * Q_TUSE / 1e3}


def fig1_plate():
    W1, H1 = 560, 600
    sx = 1.9
    cv = Canvas(W1, H1, sx=sx, ox=170, oy=150)
    cv.panel("① 剪力板配置與淨剪斷面", "180 × 80 mm；螺栓單排、距柱面 40 mm")
    cv.polygon([(-14, -10), (0, -10), (0, HP + 10), (-14, HP + 10)], "rgba(63,74,90,0.18)", C["member"], 1.4)
    cv.text_px(cv.X(-14) - 8, cv.Y(HP / 2), "柱面", 12, C["muted"], "end")
    cv.polygon([(0, 0), (WP, 0), (WP, HP), (0, HP)], C["fill_c"], C["member"], 1.8)
    cv.line((Q_XB, -12), (Q_XB, HP + 12), C["load"], 2.4, dash="8 4")
    for y in Q_YS:
        cv.circle((Q_XB, y), Q_DH / 2, fill="#FFFFFF", stroke=C["member"], w=2.0)
        cv.circle((Q_XB, y), Q_D / 2, fill="rgba(63,74,90,0.25)", stroke="none")
    ticks = [0] + Q_YS + [HP]
    for a, b in zip(ticks[:-1], ticks[1:]):
        cv.dim((WP, a), (WP, b), f"{b - a:.0f}", off=30, label_off=18, size=12.5)
    cv.dim((0, HP), (Q_XB, HP), f"{Q_XB:.0f}", off=-22, label_off=-13, size=12.5)
    cv.dim((Q_XB, HP), (WP, HP), f"{WP - Q_XB:.0f}", off=-22, label_off=-13, size=12.5)
    cv.text_px(cv.X(Q_XB) - 10, cv.Y(-12) + 18, "淨剪斷面（紅虛線）", 12, C["load"], "middle", weight="700")
    cv.text_px(W1 / 2, H1 - 56, f"Anv = (180 − {Q_N} × {Q_DH:.0f}) t = {HP - Q_N * Q_DH:.0f} t", 14, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, f"孔徑 {Q_DH:.0f} mm（標準孔 d + 2）；Agv = 180 t", 12.5, C["muted"])
    p1 = cv

    cv = Canvas(W1, H1, sx=sx, ox=190, oy=150)
    cv.panel("② 承壓的淨距 Lc：邊緣孔只有一半", "Rn = 1.2 Lc t Fu ≤ 2.4 d t Fu")
    cv.polygon([(0, 0), (WP, 0), (WP, HP), (0, HP)], "rgba(63,74,90,0.06)", C["member"], 1.2)
    for y in Q_YS:
        cv.circle((Q_XB, y), Q_DH / 2, fill="#FFFFFF", stroke=C["member"], w=2.0)
    # 剪力向下 → 螺栓壓向孔下緣；Lc 自孔緣量到下一孔緣或板緣
    segs = [(0, Q_YS[0] - Q_DH / 2, Q_LC_E, C["load"])] + \
           [(Q_YS[k] + Q_DH / 2, Q_YS[k + 1] - Q_DH / 2, Q_LC_I, C["bmd"]) for k in range(Q_N - 1)]
    for a, b, lc, col in segs:
        cv.line((Q_XB + 18, a), (Q_XB + 18, b), col, 4.0, cap="butt")
        cv.text_px(cv.X(WP) + 10, cv.Y((a + b) / 2), f"Lc = {lc:.0f}", 12.5, col, "start", weight="700")
    cv.text_px(W1 / 2, H1 - 82, f"邊緣孔：1.2 × {Q_LC_E:.0f} × 400 = {Q_RN_E:,.0f} t（N）", 12.5, C["load"], weight="700")
    cv.text_px(W1 / 2, H1 - 56, f"內部孔：1.2 × {Q_LC_I:.0f} × 400 = {Q_RN_I:,.0f} t ≤ 2.4dtFu = {2.4 * Q_D * Q_FU:,.0f} t", 12.5, C["bmd"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, f"φ ΣRn = 0.75 × (2 × {Q_RN_E:,.0f} + {Q_RN_I:,.0f}) = {Q_BRG:,.0f} t", 12.5, C["text"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-1-plate.svg")
    compose([p1, p2], cols=2,
            title=f"圖 1　3 顆 M20：1.5d + 2 × 3d + 1.5d = 180 mm 恰好排滿",
            sub=f"φRn（單剪）= 0.75 × 330 × {Q_AB:.1f} = {Q_RB:.2f} kN/顆；{Q_VU:g}/{Q_RB:.2f} = {Q_VU / Q_RB:.2f} → {Q_N} 顆",
            note="下方邊緣孔（剪力方向）的淨距只有 19 mm，承壓容量約為內部孔的一半",
            path=path)
    return path


def fig2_thick():
    W1, H1 = 560, 470
    cv = Canvas(W1, H1, sx=1)
    cv.panel("① 各極限狀態所需板厚（mm）", "取最大者，再進位到標準板厚")
    x0, sc = 200, 30.0
    tmax = max(Q_TREQ.values())
    for i, (nm, v) in enumerate(Q_TREQ.items()):
        y = 150 + i * 72
        col = C["load"] if v == tmax else C["ghost"]
        cv.text_px(x0 - 12, y, nm, 13, C["text"], "end", weight="700" if v == tmax else "400")
        cv.rect_px(x0, y - 15, sc * v, 30, col, 4)
        if v == tmax:
            cv.text_px(x0 + sc * v - 10, y, f"{v:.2f}（控制）", 13, "#FFFFFF", "end", weight="700")
        else:
            cv.text_px(x0 + sc * v + 8, y, f"{v:.2f}", 13, C["muted"], "start", weight="700")
    _hl(cv, H1, x0 + sc * Q_TUSE, 110, x0 + sc * Q_TUSE, 360, C["bmd"], 1.8, dash="5 4")
    cv.text_px(x0 + sc * Q_TUSE, 378, f"採用 t = {Q_TUSE:g}", 12.5, C["bmd"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, "淨斷面剪力破壞控制——不是全斷面降伏", 12.5, C["muted"])
    p1 = cv
    cv = Canvas(W1, H1, sx=1)
    cv.panel(f"② t = {Q_TUSE:g} mm 的各項容量（kN）", f"需求 Vu = {Q_VU:g} kN")
    x0, sc = 200, 1.1
    for i, (nm, v) in enumerate(Q_CAPS.items()):
        y = 140 + i * 64
        cv.text_px(x0 - 12, y, nm, 13, C["text"], "end")
        cv.rect_px(x0, y - 14, sc * v, 28, C["bmd"], 4)
        cv.text_px(x0 + sc * v + 8, y, f"{v:.1f}", 13, C["bmd"], "start", weight="700")
    _hl(cv, H1, x0 + sc * Q_VU, 110, x0 + sc * Q_VU, 380, C["load"], 2.0, dash="6 4")
    cv.text_px(x0 + sc * Q_VU, 398, f"Vu = {Q_VU:g}", 12.5, C["load"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, f"最小餘裕：淨斷面剪力破壞 {Q_CAPS['淨斷面剪力破壞'] / Q_VU:.2f} 倍", 12.5, C["muted"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-2-thick.svg")
    compose([p1, p2], cols=2,
            title=f"圖 2　t ≥ {tmax:.2f} mm（淨斷面剪力破壞）→ 採 {Q_TUSE:g} mm",
            sub=f"承壓 φΣRn = {Q_BRG:,.0f}t、降伏 0.9 × 0.6Fy × 180t = {Q_YLD:,.0f}t、破壞 0.75 × 0.6Fu × {HP - Q_N * Q_DH:.0f}t = {Q_RUP:,.0f}t（N）",
            note="三個極限狀態都與 t 成正比，所以「所需板厚」可以直接並排比較",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "180／80 對調（把 80 當板長而排不下螺栓）；把螺栓配成兩行"),
    (fig1_plate, "§4 Step 1–4",
     "邊距、間距配錯；淨剪面積未扣孔或扣錯孔徑；邊緣孔承壓誤用內部孔的 Lc"),
    (fig2_thick, "§4 Step 5–7",
     "以剪力降伏（7.47 mm）為控制，忽略淨斷面剪力破壞"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
