#!/usr/bin/env python3
"""
SD-2016-5 摩擦單擺隔震系統（FPS）週期推導 — 解題圖解產生腳本

用法：python3 gen_SD-2016-5.py [輸出目錄]

圖 1  FPS 滑塊受力圖：球面半徑 r、偏轉角 θ、水平位移 x = r sinθ、重量 W、法向力 N（指向球心），
      N 的水平分量即回復力 W tanθ ≈ (W/r)x。
      攔「回復力來自摩擦」與「週期與質量有關」：回復力是重力經球面幾何轉成的水平分量，k = W/r 與 m = W/g 同比例。
本題為全符號題；THETA 只決定示意圖的比例（改 THETA 重跑，幾何與分量跟著變）。式子取自 SD-2016-5.md §4、§5。
"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.environ.get("STRUCT_DIAGRAM_SCRIPTS",
    os.path.join(HERE, "..", "..", "..", "..", "skills", "struct-diagram", "scripts"))
sys.path.insert(0, SKILL)
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
TAG = "SD-2016-5"
THETA = math.radians(24)        # 示意偏轉角
R = 1.0                          # 球面半徑（正規化）
WLEN = 0.42                      # W 箭頭長（示意）


def fig1(path):
    W_, H_ = 1240, 600
    sx = 330
    cv = Canvas(W_, H_, sx=sx, ox=330, oy=H_ - 110)   # 球心 O 在 (0,0)
    O = (0.0, 0.0)
    # 球面（下半部弧）
    arc = [(R * math.sin(a), -R * math.cos(a)) for a in [math.radians(-50 + i) for i in range(101)]]
    cv.poly(arc, C["member"], 4)
    for a in [math.radians(-48 + 6 * i) for i in range(17)]:     # 球面外側剖線
        p = (R * math.sin(a), -R * math.cos(a)); q = (1.08 * R * math.sin(a) - 0.03, -1.08 * R * math.cos(a))
        cv.line(p, q, C["member2"], 1.4)
    # 鉛直參考線、半徑
    cv.line(O, (0, -R - 0.05), C["ghost"], 1.8, dash="6 5")
    S = (R * math.sin(THETA), -R * math.cos(THETA))               # 滑塊位置
    cv.line(O, S, C["member2"], 2, dash="7 5")
    cv.dot(O, 5, C["text"]); cv.text(O, "O（球心）", 14, C["text"], anchor="start", dx=10, dy=-4)
    mid = (S[0] / 2, S[1] / 2)
    cv.math((S[0] * 0.44, S[1] * 0.44), "r", 17, C["text"], dx=14, dy=-4)
    # θ 角
    th_arc = [(0.22 * math.sin(a), -0.22 * math.cos(a)) for a in [THETA * i / 30 for i in range(31)]]
    cv.poly(th_arc, C["accent"], 2)
    cv.math((0.25 * math.sin(THETA / 2), -0.25 * math.cos(THETA / 2)), "θ", 16, C["accent"], dx=6, dy=10)
    # 滑塊（小方塊，沿切線方向）
    tx, ty = math.cos(THETA), math.sin(THETA); nx, ny = -math.sin(THETA), math.cos(THETA)   # 切線、指向球心的法線
    hw, hh = 0.07, 0.05
    blk = [(S[0] + a * tx * hw + b * nx * hh * 2, S[1] + a * ty * hw + b * ny * hh * 2) for a, b in ((-1, 0), (1, 0), (1, 1), (-1, 1))]
    cv.polygon(blk, C["panel"], C["member"], 2)
    G = (S[0] + nx * hh, S[1] + ny * hh)
    # W（向下）
    cv.arrow(G, (G[0], G[1] - WLEN), C["load"], 3.2)
    cv.math((G[0], G[1] - WLEN), "W = mg", 15, C["load"], anchor="start", dx=10, dy=6)
    # N（指向球心，大小 W/cosθ）
    Nlen = WLEN / math.cos(THETA)
    Nend = (G[0] + nx * Nlen, G[1] + ny * Nlen)
    cv.arrow(G, Nend, C["deform"], 3.2)
    cv.math(((G[0] + Nend[0]) / 2, (G[1] + Nend[1]) / 2), "N = W/cosθ", 15, C["deform"], anchor="end", dx=-12, dy=8)
    # N 的水平分量（回復力，指向中心線）
    Hlen = Nlen * math.sin(THETA)
    cv.arrow((G[0], G[1] + Nlen * math.cos(THETA)), (G[0] - Hlen, G[1] + Nlen * math.cos(THETA)), C["accent"], 2.8, dash=None)
    cv.line(G, (G[0], G[1] + Nlen * math.cos(THETA)), C["deform"], 1.4, dash="4 4")
    cv.line((G[0] - Hlen, G[1] + Nlen * math.cos(THETA)), Nend, C["deform"], 1.4, dash="4 4")
    cv.text((G[0] - Hlen, G[1] + Nlen * math.cos(THETA)), "回復力 N sinθ = W tanθ", 13.5, C["accent"], anchor="end", dx=-8, dy=-2)
    # 水平位移 x
    yb = -R - 0.13
    cv.dim((0, yb), (S[0], yb), "x = r sinθ", off=0, size=14)
    # 右側推導摘要
    bx = 1.12
    lines = [("忽略摩擦、小角度（sinθ ≈ tanθ ≈ x/r）：", C["text"], True),
             ("水平：m·x'' = −N sinθ = −W tanθ ≈ −(W/r)x", C["text"], False),
             ("側向勁度 k = W/r", C["accent"], True),
             ("ω^{2} = k/m = (W/r)/(W/g) = g/r", C["text"], False),
             ("T = 2π(r/g)^{1/2}，與 W（質量）無關", C["bmd"], True)]
    for i, (s, col, b) in enumerate(lines):
        cv.text((bx, -0.08 - 0.12 * i), s, 13.5, col, anchor="start", weight="700" if b else "400")
    return compose([cv], title="圖 1　摩擦單擺隔震系統（FPS）滑塊受力：回復力來自重力經球面轉成的水平分量",
                   note="θ 為示意角度；推導用小角度近似，週期只由球面半徑 r 決定",
                   path=path)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1(os.path.join(OUT, f"{TAG}-fig-1-fps-fbd.svg"))
    print("ok")
