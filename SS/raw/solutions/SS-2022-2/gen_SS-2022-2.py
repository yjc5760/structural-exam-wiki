#!/usr/bin/env python3
"""
SS-2022-2 插銷鉸接拉力構件 ASD 可用強度與 D5.2 尺寸 — 解題圖解腳本

用法：
    python3 gen_SS-2022-2.py [輸出目錄]

本題考卷無附圖（題目正本 SS-2022-2-problem.md §3）；本腳本只產生解題圖解。
數值全部取自 SS-2022-2.md §4，由下式即時算出（單位 mm、MPa、kN）。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2022-2"


# ── 解題圖解共用小工具（像素座標；y 由上往下）──
def _hl(cv, PH, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line((x0, PH - y0), (x1, PH - y1), color, w, dash=dash, cap="butt")


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2022-2.md §4
# ══════════════════════════════════════════════════════════════
Q_PD, Q_PL = 135.0, 315.0          # kN
Q_B, Q_T, Q_D, Q_A0 = 300.0, 20.0, 100.0, 65.0   # 板寬、厚、孔徑、端距／邊距（孔緣起算）
Q_FY, Q_FU = 345.0, 450.0          # MPa
Q_P = Q_PD + Q_PL                  # 450 kN
Q_BEMAX = 2 * Q_T + 16             # 56


def q_states(a_end, side_near, side_far):
    be = min(Q_BEMAX, side_near, side_far)
    pa1 = Q_FY * Q_B * Q_T / 1000 / 1.67
    pa2 = Q_FU * 2 * Q_T * be / 1000 / 2.00
    pa3 = 0.6 * Q_FU * 2 * Q_T * (a_end + Q_D / 2) / 1000 / 2.00
    pa4 = 1.8 * Q_FY * Q_T * Q_D / 1000 / 2.00
    return be, [("① 全斷面降伏", pa1), ("② 受拉有效面積斷裂", pa2), ("③ 受剪有效面積斷裂", pa3), ("④ 插銷承壓", pa4)]


Q_C0 = Q_A0 + Q_D / 2                                  # 孔心距板端／近側邊 115
Q_BE0, Q_ST0 = q_states(Q_A0, Q_A0, Q_B - Q_C0 - Q_D / 2)
Q_A1 = 75.0                                            # 修正後端距
Q_BE1, Q_ST1 = q_states(Q_A1, (Q_B - Q_D) / 2, (Q_B - Q_D) / 2)
Q_A_REQ = 1.33 * Q_BEMAX                               # 74.5
Q_W_REQ = 2 * Q_BEMAX + Q_D                            # 212


def _plate(title, sub, a_end, cy):
    W1, H1 = 520, 500
    cv = Canvas(W1, H1, sx=1.0, ox=60, oy=85)
    cv.panel(title, sub)
    L = 360
    cv.polygon([(0, 0), (L, 0), (L, Q_B), (0, Q_B)], C["fill_c"], C["member"], 1.6)
    cx = a_end + Q_D / 2
    cv.circle((cx, cy), Q_D / 2, fill="#FFFFFF", stroke=C["member"], w=1.8)
    be = min(Q_BEMAX, cy - Q_D / 2, Q_B - cy - Q_D / 2)
    for y0 in (cy - Q_D / 2 - be, cy + Q_D / 2):
        cv.polygon([(cx - 6, y0), (cx + 6, y0), (cx + 6, y0 + be), (cx - 6, y0 + be)], C["load"], "none")
    for y in (cy - Q_D / 2, cy + Q_D / 2):
        cv.line((0, y), (cx, y), C["sfd"], 2.6, dash="6 4", cap="butt")
    cv.arrow((L, Q_B / 2), (L + 55, Q_B / 2), C["load"], 3, 10)
    cv.text((L + 55, Q_B / 2), "P", 14, C["load"], "start", dx=6, weight="700")
    cv.dim((0, cy), (a_end, cy), f"a={a_end:g}", off=0, label_off=-12)
    cv.dim((0, -10), (cx, -10), f"{cx:g}", off=-14, label_off=14)
    cv.dim((L, 0), (L, cy), f"{cy:g}", off=-30, label_off=-22)
    cv.text((cx, cy), f"d={Q_D:g}", 12, C["text"])
    cv.text((cx + 10, cy + Q_D / 2 + be / 2), f"be={be:g}", 12, C["load"], "start", weight="700")
    cv.text((cx / 2, cy + Q_D / 2), "剪出面", 11.5, C["sfd"], dy=-10)
    return cv


def fig1_layout():
    p1 = _plate("題給配置（孔在角隅）", f"孔緣距板端與近側邊 {Q_A0:g}", Q_A0, Q_C0)
    p2 = _plate("修正配置（D5.2）", f"孔置中、端距 {Q_A1:g} ≥ 1.33be = {Q_A_REQ:.1f}", Q_A1, Q_B / 2)
    path = os.path.join(OUT, f"{TAG}-fig-1-layout.svg")
    compose([p1, p2], cols=2,
            title=f"圖 1　be = min(2t + 16, 孔緣至側邊) = {Q_BE0:g} mm；題給配置孔不置中、端距 {Q_A0:g} 小於 {Q_A_REQ:.1f}，不符 D5.2",
            sub="紅塊：受拉有效寬 be（孔兩側各一）；紫虛線：受剪剪出面，長 a + d/2",
            note=f"a 量到孔緣（不是孔心）；孔心距板端 a + d/2 = {Q_C0:g}；板寬需 ≥ 2be + d = {Q_W_REQ:g}（300 ✓）",
            path=path)
    return path


def fig2_states():
    W1, H1 = 1000, 500
    cv = Canvas(W1, H1, sx=1)
    cv.panel("四種極限狀態的可用強度 Pa = Pn / Ω（kN）", "Ω：降伏 1.67、斷裂與承壓 2.00；服務載重 P = PD + PL")
    x0, sc = 230, 0.42
    for i, ((lab, v0), (_, v1)) in enumerate(zip(Q_ST0, Q_ST1)):
        y = 140 + i * 72
        ctrl = v0 == min(v for _, v in Q_ST0)
        cv.text_px(x0 - 12, y, lab, 13, C["text"], "end", weight="700")
        cv.rect_px(x0, y - 18, sc * v0, 16, C["load"] if ctrl else C["compr"], 3)
        cv.text_px(x0 + sc * v0 + 8, y - 10, f"{v0:.0f}" + ("（控制）" if ctrl else ""), 12.5, C["load"] if ctrl else C["compr"], "start", weight="700")
        cv.rect_px(x0, y + 2, sc * v1, 16, C["ghost"], 3)
        cv.text_px(x0 + sc * v1 + 8, y + 10, f"{v1:.0f}（修正後）" if abs(v1 - v0) > 0.5 else f"{v1:.0f}", 12, C["muted"], "start")
    xp = x0 + sc * Q_P
    _hl(cv, H1, xp, 110, xp, 420, C["accent"], 1.6, dash="5 4")
    cv.text_px(xp, 438, f"P = {Q_PD:g} + {Q_PL:g} = {Q_P:g}", 12.5, C["accent"], weight="700")
    pa = min(v for _, v in Q_ST0)
    cv.text_px(W1 - 40, 300, f"Pa = {pa:.0f} kN ≥ {Q_P:g}", 14, C["bmd"], "end", weight="700")
    cv.text_px(W1 - 40, 328, f"利用率 {Q_P / pa * 100:.1f}%", 13, C["bmd"], "end")
    cv.text_px(W1 - 40, 356, "強度足夠，但配置要改", 12.5, C["muted"], "end")
    path = os.path.join(OUT, f"{TAG}-fig-2-states.svg")
    compose([cv], cols=1,
            title=f"圖 2　受拉有效面積斷裂控制：Pa = {pa:.0f} kN ＞ P = {Q_P:g} kN（利用率 {Q_P / pa * 100:.1f}%）",
            sub="上條：題給配置；下條（灰）：修正配置後，只有剪出面積變大（③ 621 → 675）",
            note="只算全斷面降伏（1,240）會嚴重高估；ASD 要比服務載重 450，不是係數化載重",
            path=path)
    return path


FIGURES = [
    (fig1_layout, "§4 二、四、五、八",
     "a 量到孔心；be 取實際邊距而漏 2t + 16 上限；剪出面長只取 a；忽略 D5.2 孔位規定"),
    (fig2_states, "§4 三–七",
     "只算全斷面降伏；Ω 用錯；與係數化載重比較"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
