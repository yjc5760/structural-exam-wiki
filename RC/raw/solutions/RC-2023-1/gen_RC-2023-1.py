#!/usr/bin/env python3
"""
RC-2023-1 — 解題圖解產生腳本（2026-11-13，RC-U1-1 批 2 階段 E）

用法：python3 gen_RC-2023-1.py [輸出目錄]（預設 figs/）
常數只放題目給定量（題目正本 §1／§2）與 RC-2023-1.md §4 公佈值；其餘現算，檔尾對 §4 assert。
解題圖解（2026-11-13 補，RC-U1-1 批 2 階段 E）
  fig-1-curvature 降伏／極限應變剖面  攔：降伏時用等值應力塊
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2023-1"
FIGURES = []

import math
U_B, U_D, U_AS, U_FY, U_ES, U_ECU = 40.0, 53.0, 4 * 5.07, 4200.0, 2.04e6, 0.003   # fy 為題目正本確認之假設
U_EY = U_FY / U_ES


def ductility(fc):
    n = U_ES / (15000 * math.sqrt(fc))
    rho = U_AS / (U_B * U_D)
    k = math.sqrt((n * rho) ** 2 + 2 * n * rho) - n * rho
    phy = U_EY / (U_D * (1 - k))
    c = U_AS * U_FY / (0.85 * fc * 0.85 * U_B)
    phu = U_ECU / c
    return dict(fc=fc, n=n, k=k, kd=k * U_D, phy=phy, c=c, phu=phu, mu=phu / phy)


RU = [ductility(210.0), ductility(280.0)]


def sci(v, name):
    m, e = f"{v:.3e}".split("e")
    return f"{name} = {m}×10^{{{int(e)}}} 1/cm"


def fig1_curvature():
    path = os.path.join(OUT, f"{TAG}-fig-1-curvature.svg")
    W, H = 470, 560
    top, kz = 128, 280 / U_D
    emax = max(U_ECU * (U_D - r["c"]) / r["c"] for r in RU)
    ks = 200 / emax
    x0 = 250
    panels = []
    for r in RU:
        cv = Canvas(W, H)
        cv.panel(f"f'c = {r['fc']:g}", f"n = {r['n']:.2f}；kd = {r['kd']:.2f}；c = {r['c']:.2f} cm")
        Y = lambda z: H - (top + z * kz)              # Canvas 會再翻轉
        P = lambda e, z: (x0 - e * ks, Y(z))          # 拉應變（正）畫在左、壓應變畫在右
        cv.line(P(0, -3), P(0, U_D + 4), C["ghost"], 2, dash="5 4")
        cv.line(P(-0.0062, 0), P(emax * 1.02, 0), C["member2"], 1.2)
        cv.line(P(-0.0062, U_D), P(emax * 1.02, U_D), C["member2"], 1.2, dash="3 3")
        ecy = U_EY * r["kd"] / (U_D - r["kd"])
        cv.poly([P(-ecy, 0), P(U_EY, U_D)], C["accent"], 2.6)
        etu = U_ECU * (U_D - r["c"]) / r["c"]
        cv.poly([P(-U_ECU, 0), P(etu, U_D)], C["deform"], 2.6)
        cv.dot(P(0, r["kd"]), 4.5, fill=C["accent"])
        cv.dot(P(0, r["c"]), 4.5, fill=C["deform"])
        cv.text_px(x0 + 10, H - Y(r["kd"]) + 2, f"kd = {r['kd']:.2f}", 12, C["accent"], "start", weight="700")
        cv.text_px(x0 + 10, H - Y(r["c"]) - 4, f"c = {r['c']:.2f}", 12, C["deform"], "start", weight="700")
        cv.text_px(x0 - U_EY * ks, H - Y(U_D) + 18, f"εy = {U_EY:.6f}", 11.5, C["accent"])
        cv.text_px(x0 - etu * ks, H - Y(U_D) + 36, f"εs = {etu:.5f}", 11.5, C["deform"])
        cv.text_px(x0 + U_ECU * ks, H - Y(0) - 16, "εcu = 0.003", 11.5, C["deform"])
        cv.text_px(24, H - Y(0) - 2, "頂面", 11.5, C["muted"], "start")
        cv.text_px(24, H - Y(U_D) - 2, "鋼筋 d", 11.5, C["muted"], "start")
        cv.text_px(W / 2, H - 64, sci(r["phy"], "φ_{y}") + "；" + sci(r['phu'], "φ_{u}"), 13, C["text"], weight="700")
        cv.text_px(W / 2, H - 34, f"μφ = φu / φy = {r['mu']:.2f}", 14, C["bmd"], weight="700")
        panels.append(cv)
    compose(panels, title=f"{TAG}　降伏（橘，轉換斷面）與極限（藍，等值應力塊）的應變剖面",
            sub="斜率即曲率；兩欄水平比例相同。f'c 提高時 kd 幾乎不變（φy 只差 3%），c 卻明顯變淺（φu 增 33%）",
            note=f"μ280 / μ210 = {RU[1]['mu']:.2f} / {RU[0]['mu']:.2f} = {RU[1]['mu']/RU[0]['mu']:.2f}；降伏狀態不可用等值應力塊求中性軸",
            path=path)
    return path


FIGURES += [(fig1_curvature, "§4 Case 1–2", "降伏時也用等值應力塊；以為 f'c 提高主要改變 φy")]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, sec, catches in FIGURES:
        print(f"{os.path.basename(fn()):<32} {sec:<18} 攔：{catches}")
    exp = [(0.3433, 5.916e-5, 14.03, 2.138e-4, 3.61), (0.3242, 5.748e-5, 10.53, 2.850e-4, 4.96)]   # §4
    for r, (k, py, c, pu, mu) in zip(RU, exp):
        assert abs(r["k"] - k) < 2e-4 and abs(r["phy"] / py - 1) < 2e-3 and abs(r["c"] - c) < 0.01
        assert abs(r["phu"] / pu - 1) < 2e-3 and abs(r["mu"] - mu) < 0.006
    assert abs(RU[1]["mu"] / RU[0]["mu"] - 1.37) < 0.005
    print("assert（解題圖解）OK")
