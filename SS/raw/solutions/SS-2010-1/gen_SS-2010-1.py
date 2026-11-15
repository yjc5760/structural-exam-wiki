#!/usr/bin/env python3
"""
SS-2010-1 階梯形斷面之 M_y 與 M_p — 題目附圖重繪腳本

用法：
    python3 gen_SS-2010-1.py [輸出目錄]

重繪依據：題目正本 SS-2010-1-problem.md §4 判讀清單（2026-11-02 已確認）。
圖上每個尺寸都對應清單一項；只畫考卷給的東西，不含任何解題結果（ENA、PNA 不畫）。
斷面依比例繪製。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "..", "skills", "struct-diagram", "scripts"))   # 五科合一後 skill 在根目錄 skills/

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2010-1"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2010-1-problem.md §4，已確認）；單位 cm
# ══════════════════════════════════════════════════════════
X_SEG = [2.0, 2.0, 2.0]          # #1 水平分段 2-2-2，總寬 6
Y_SEG = [2.0, 2.0, 2.0, 2.0]     # #2 垂直分段 2-2-2-2，總高 8
# 由下而上各層：（寬度所佔水平分段的起訖索引）
LAYERS = [(0, 3),                # #3 第 1 層：全寬 6×2
          (1, 2),                # #4 第 2 層：中央 2×2
          (0, 3),                # #5 第 3 層：全寬 6×2
          (1, 2)]                # #6 第 4 層：頂部中央凸塊 2×2
#                                  #7 左右對稱、上下不對稱

XS = [sum(X_SEG[:i]) for i in range(len(X_SEG) + 1)]   # 0, 2, 4, 6
YS = [sum(Y_SEG[:i]) for i in range(len(Y_SEG) + 1)]   # 0, 2, 4, 6, 8


def outline():
    """由各層矩形組出外框（右側由下而上、左側由上而下）"""
    right, left = [], []
    for k, (i0, i1) in enumerate(LAYERS):
        right += [(XS[i1], YS[k]), (XS[i1], YS[k + 1])]
        left += [(XS[i0], YS[k]), (XS[i0], YS[k + 1])]
    return right + left[::-1]


def fig1_problem():
    W, H, sx = 520, 470, 38
    cv = Canvas(W, H, sx=sx, ox=W / 2 - XS[-1] / 2 * sx - 30, oy=90)
    cv.panel("圖一　斷面", "依比例；單位為公分")
    cv.polygon(outline(), C["fill_c"], C["member"], 2.0)
    xr = XS[-1]
    for k in range(len(Y_SEG)):
        cv.dim((xr, YS[k]), (xr, YS[k + 1]), f"{Y_SEG[k]:g}", off=40, label_off=16)
    for i in range(len(X_SEG)):
        cv.dim((XS[i], 0), (XS[i + 1], 0), f"{X_SEG[i]:g}", off=30, label_off=16)
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title="SS-2010-1 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#7；只畫考卷所給條件",
            note="由下而上：全寬 6×2、中央 2×2、全寬 6×2、頂部凸塊 2×2（上下不對稱）",
            path=path)
    return path


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-15 補繪）——數值全部由 LAYERS 與 F_Y 即時算出，對應 SS-2010-1.md §4
# ══════════════════════════════════════════════════════════════
F_Y = 4.0                                            # tf/cm²（§4 Step 2，SS540）
RECTS = [(XS[i1] - XS[i0], YS[k + 1] - YS[k], (YS[k] + YS[k + 1]) / 2)
         for k, (i0, i1) in enumerate(LAYERS)]       # (b, h, 形心 y)
A_TOT = sum(b * h for b, h, _ in RECTS)
Y_ENA = sum(b * h * y for b, h, y in RECTS) / A_TOT
I_X = sum(b * h ** 3 / 12 + b * h * (y - Y_ENA) ** 2 for b, h, y in RECTS)
C_TOP, C_BOT = YS[-1] - Y_ENA, Y_ENA
S_X = I_X / max(C_TOP, C_BOT)
M_Y = F_Y * S_X
SIG_BOT = F_Y * C_BOT / C_TOP                        # 頂緣先降伏時的底緣應力


def _area_below(y):
    a = 0.0
    for k, (i0, i1) in enumerate(LAYERS):
        lo, hi = YS[k], YS[k + 1]
        if y > lo:
            a += (XS[i1] - XS[i0]) * (min(y, hi) - lo)
    return a


lo_, hi_ = 0.0, YS[-1]
for _ in range(100):
    mid = (lo_ + hi_) / 2
    lo_, hi_ = (mid, hi_) if _area_below(mid) < A_TOT / 2 else (lo_, mid)
Y_PNA = (lo_ + hi_) / 2


def _moment_about(y0, above):
    m = 0.0
    for k, (i0, i1) in enumerate(LAYERS):
        lo, hi = YS[k], YS[k + 1]
        a, b = (max(lo, y0), hi) if above else (lo, min(hi, y0))
        if b > a:
            m += (XS[i1] - XS[i0]) * (b - a) * abs((a + b) / 2 - y0)
    return m


Z_TOP, Z_BOT = _moment_about(Y_PNA, True), _moment_about(Y_PNA, False)
Z_X = Z_TOP + Z_BOT
M_P = F_Y * Z_X
FORCE = F_Y * A_TOT / 2
E_TOP, E_BOT = Z_TOP / (A_TOT / 2), Z_BOT / (A_TOT / 2)   # 上下半形心距 PNA


def _panel(title, sub):
    cv = Canvas(380, 520, sx=38, ox=40, oy=90)
    cv.panel(title, sub)
    return cv


def _hline(cv, y, color, label, side_dx):
    cv.line((XS[0] - 0.6, y), (XS[-1] + 0.6, y), color, 1.8, dash="6 4")
    cv.text((XS[-1] + 0.6, y), label, 12.5, color, "start", dx=side_dx, dy=4, weight="700")


def fig2_stress():
    # (a) 斷面與兩條中性軸
    a = _panel("(a) 斷面：ENA ≠ PNA", "上下不對稱，兩軸相差 0.5 cm")
    a.polygon(outline(), C["fill_c"], C["member"], 2.0)
    _hline(a, Y_ENA, C["accent"], f"ENA {Y_ENA:.1f}", 6)
    _hline(a, Y_PNA, C["bmd"], f"PNA {Y_PNA:.1f}", 6)
    a.text((XS[-1] / 2, YS[-1]), f"頂緣距 ENA {C_TOP:.1f} cm（大於底緣 {C_BOT:.1f}，控制 S）", 12, C["muted"], dy=-14)
    a.text((XS[-1] / 2, 0), f"A = {A_TOT:.0f} cm²，A/2 = {A_TOT/2:.0f}", 12, C["muted"], dy=34)
    # (b) 彈性：頂緣先達 Fy
    k = 0.6                                          # 每 1 tf/cm² 對應 0.6 cm 圖面寬
    b = _panel("(b) 降伏力矩 My：應力線性", "以 ENA 為零點，頂緣（離軸較遠）先達 Fy")
    x0 = 4.5
    b.line((x0, 0), (x0, YS[-1]), C["member"], 2.0, cap="butt")
    b.polygon([(x0, Y_ENA), (x0, YS[-1]), (x0 - k * F_Y, YS[-1])], C["fill_c"], C["compr"], 1.6)
    b.polygon([(x0, Y_ENA), (x0, 0), (x0 + k * SIG_BOT, 0)], C["fill_t"], C["tension"], 1.6)
    b.text((x0 - k * F_Y, YS[-1]), f"Fy = {F_Y:.1f}（壓）", 12.5, C["compr"], "start", dy=-12, weight="700")
    b.text((x0 + k * SIG_BOT, 0), f"{SIG_BOT:.2f}（拉）", 12.5, C["tension"], "end", dy=22, weight="700")
    b.line((x0 - 1.2, Y_ENA), (x0 + 1.2, Y_ENA), C["accent"], 1.6, dash="6 4")
    b.text((x0 + 1.2, Y_ENA), f"ENA {Y_ENA:.1f}", 12, C["accent"], "start", dx=4, dy=4)
    b.text((x0, 0), f"My = Fy × S = {M_Y:.1f} tf·cm", 13, C["text"], dy=56, weight="700")
    # (c) 塑性：上下各 A/2 達 ±Fy
    c = _panel("(c) 塑性力矩 Mp：應力塊", "以 PNA 平分面積，上壓下拉各 A/2")
    c.line((x0, 0), (x0, YS[-1]), C["member"], 2.0, cap="butt")
    c.polygon([(x0, Y_PNA), (x0, YS[-1]), (x0 - k * F_Y, YS[-1]), (x0 - k * F_Y, Y_PNA)], C["fill_c"], C["compr"], 1.6)
    c.polygon([(x0, Y_PNA), (x0, 0), (x0 + k * F_Y, 0), (x0 + k * F_Y, Y_PNA)], C["fill_t"], C["tension"], 1.6)
    yc, yt = Y_PNA + E_TOP, Y_PNA - E_BOT
    c.arrow((x0 + 0.2, yc), (x0 - k * F_Y - 0.2, yc), C["compr"], 2.6, head=9)
    c.arrow((x0 - 0.2, yt), (x0 + k * F_Y + 0.2, yt), C["tension"], 2.6, head=9)
    c.text((x0 + 0.2, yc), f"C = {FORCE:.0f} tf", 12.5, C["compr"], "start", dx=6, dy=4, weight="700")
    c.text((x0 + k * F_Y, yt), f"T = {FORCE:.0f} tf", 12.5, C["tension"], "start", dx=8, dy=4, weight="700")
    c.line((x0 - 1.2, Y_PNA), (x0 + 1.2, Y_PNA), C["bmd"], 1.6, dash="6 4")
    c.text((x0 + k * F_Y + 0.2, Y_PNA), f"PNA {Y_PNA:.1f}", 12, C["bmd"], "start", dx=4, dy=4)
    c.dim((x0 - k * F_Y - 0.9, yt), (x0 - k * F_Y - 0.9, yc), f"{E_TOP + E_BOT:.1f}", off=0, label_off=-16)
    c.text((x0, 0), f"Mp = {FORCE:.0f} × {E_TOP + E_BOT:.1f} = {M_P:.0f} tf·cm", 13, C["text"], dy=56, weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-2-stress.svg")
    compose([a, b, c], cols=3,
            title=f"圖 2　My = {M_Y:.1f}、Mp = {M_P:.0f} tf·cm，形狀因子 {Z_X / S_X:.2f}",
            sub=f"彈性看形心（ENA {Y_ENA:.1f} cm），塑性看面積平分（PNA {Y_PNA:.1f} cm）",
            note=f"I = {I_X:.2f} cm⁴、S = I / {C_TOP:.1f} = {S_X:.2f} cm³；Z = {Z_BOT:.0f} + {Z_TOP:.0f} = {Z_X:.0f} cm³",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把斷面讀成上下對稱的十字形（漏看底部全寬段與頂部凸塊的差異）"),
    (fig2_stress, "§4 一、二",
     "ENA 與 PNA 視為同一軸；S 取 c_bot（底緣）；以為底緣先降伏；塑性力臂取形心距"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    assert XS[-1] == 6 and YS[-1] == 8
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
