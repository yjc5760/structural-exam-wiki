#!/usr/bin/env python3
"""SD-2018-2 解題圖解（struct-diagram；2026-11-16，X-G1 階段 E）
fig-5-tripartite：在 log Spv–log T 上畫規範四段設計譜（示意參數），疊常數 Spa（斜率 +1）與常數 Sd（斜率 −1）線族，
標出斜軸增大方向（Spa ↖、Sd ↗）與各段對應的 Newmark 段；虛線為規範省略的常數 Sd 段（e→f）。
攔下的錯誤：舊解把 Spa 軸寫成右上、Sd 軸寫成右下，並把 a–f 各段對應錯開一段。
示意參數 SDS、SD1、Te 只決定圖形位置，不是考卷數據（考卷沒有給數值）。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2018-2"

SDS, SD1, g = 1.0, 0.6, 9.81          # 示意參數（g 為單位）
T0 = SD1/SDS; Te = 4.0                # Te：示意的常數位移段起點（Newmark e 點）
def Sa(T):
    if T <= 0.2*T0: return SDS*(0.4 + 3*T/T0)
    return SDS if T <= T0 else SD1/T
Spv = lambda T, sa=None: (Sa(T) if sa is None else sa)*g*T/(2*math.pi)
LT = (-2.0, 1.3); LV = (-2.4, 0.6)    # log10 範圍
W, H = 760, 560
cv = Canvas(W, H, sx=1, bg="#FFFFFF")
bx0, bx1, by0, by1 = 80, 700, 70, 500
X = lambda T: bx0 + (bx1-bx0)*(math.log10(T)-LT[0])/(LT[1]-LT[0])
Y = lambda v: by0 + (by1-by0)*(math.log10(v)-LV[0])/(LV[1]-LV[0])
def clipline(f, col, w, dash):
    pts = []
    for i in range(301):
        lt = LT[0] + (LT[1]-LT[0])*i/300; T = 10**lt; v = f(T)
        if 10**LV[0] <= v <= 10**LV[1]: pts.append((X(T), Y(v)))
    if len(pts) > 1: cv.poly(pts, col, w, dash=dash)

def fig5():
    cv.text_px(W/2, 26, "三軸座標：斜率 +1 為常數 Spa、斜率 −1 為常數 Sd；規範四段對應 a→b、b→c、c→d、d→e", 14, C["text"], weight="700")
    for k in range(-3, 3):                                   # 常數 Spa 線族（g）
        clipline(lambda T, k=k: (10**k)*g*T/(2*math.pi), C["border"], 1.0, "4 4")
    for k in range(-4, 1):                                   # 常數 Sd 線族（m）
        clipline(lambda T, k=k: 2*math.pi*(10**k)/T, "#E8D9C6", 1.0, "4 4")
    cv.line((bx0, by0), (bx1, by0), C["muted"], 1.6); cv.line((bx0, by0), (bx0, by1), C["muted"], 1.6)
    cv.text_px(bx1, H - by0 + 22, "log T", 13, C["muted"], "end"); cv.text_px(bx0 - 8, H - by1 - 8, "log Spv", 13, C["muted"], "start")
    # 斜軸方向
    ox, oy = 600, 190
    cv.arrow((ox, oy), (ox - 60, oy + 60), C["deform"], 2.4, 9); cv.text_px(ox - 66, H - oy - 70, "Spa 增大 ↖", 13, C["deform"], "end")
    cv.arrow((ox, oy), (ox + 60, oy + 60), C["accent"], 2.4, 9); cv.text_px(ox + 66, H - oy - 70, "Sd 增大 ↗", 13, C["accent"], "start")
    # 規範譜各段
    OFF = {"②": (14, 20, "start"), "③": (14, 22, "start"), "④": (0, -16, "middle")}
    segs = [(0.01, 0.2*T0, "② 較短週期 ↔ b→c", C["sfd"]), (0.2*T0, T0, "③ SDS ↔ c→d（斜率 +1）", C["deform"]),
            (T0, 10.0, "④ SD1/T ↔ d→e（水平）", C["bmd"])]
    for a, b, lab, col in segs:
        pts = [(X(a*(b/a)**(i/60)), Y(Spv(a*(b/a)**(i/60)))) for i in range(61)]
        cv.poly(pts, col, 3.4)
        m = math.sqrt(a*b); dx, dy, anc = OFF[lab[0]]
        cv.text_px(X(m) + dx, H - Y(Spv(m)) + dy, lab, 12.5, col, anc, weight="700")
    # ① 零週期：T→0 時 Sa→0.4SDS，在三軸圖上是一條常數 Spa 線（a→b）
    pts = [(X(T), Y(0.4*SDS*g*T/(2*math.pi))) for T in [0.01*(3**(i/20)) for i in range(21)]]
    cv.poly(pts, C["load"], 2.0, dash="8 5")
    Tl = 0.014; cv.text_px(X(Tl) + 10, H - Y(0.4*SDS*g*Tl/(2*math.pi)) + 26, "① 0.4SDS（常數 Spa）↔ a→b", 12.5, C["load"], "start", weight="700")
    # 規範省略的 e→f：常數 Sd（斜率 −1）
    Sde = Spv(Te)*Te/(2*math.pi)
    pts = [(X(T), Y(2*math.pi*Sde/T)) for T in [Te*(10/Te)**(i/30) for i in range(31)]]
    cv.poly(pts, C["accent"], 2.6, dash="8 5")
    cv.text_px(X(9.0), H - Y(2*math.pi*Sde/9.0) + 26, "e→f 常數 Sd（規範表沒有）", 12.5, C["accent"], "middle", weight="700")
    cv.text_px(W/2, H - 20, "示意參數 SDS＝1、SD1＝0.6（T0＝0.6 s）；規範長週期段 Sa∝1/T 高於 e→f 的 Sa∝1/T²，偏保守", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-5-tripartite.svg")

FIGURES = [(fig5, "斜軸方向 Spa ↖、Sd ↗；規範四段對應 a→b～d→e，缺 e→f")]
if __name__ == "__main__":
    for fn, c in FIGURES: print(fn(), "—", c)
