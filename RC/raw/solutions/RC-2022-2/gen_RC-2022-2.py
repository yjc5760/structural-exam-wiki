#!/usr/bin/env python3
"""
RC-2022-2 — 解題圖解產生腳本（2026-11-13，RC-U1-1 批 2 階段 E）

用法：python3 gen_RC-2022-2.py [輸出目錄]（預設 figs/）
常數只放題目給定量（題目正本 §1／§2）與 RC-2022-2.md §4 公佈值；其餘現算，檔尾對 §4 assert。
解題圖解（2026-11-13 補，RC-U1-1 批 2 階段 E）
  fig-1-combos    四組合 As 比較      攔：以為提高 f'c 能大幅省鋼筋
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2022-2"
FIGURES = []

from recipes import bar_compare
import math
G_B, G_D, G_MU, G_AB = 30.0, 43.5, 19.5e5, 5.067
COMBOS = [("組合一", 210.0, 4200.0), ("組合二", 210.0, 5600.0), ("組合三", 280.0, 4200.0), ("組合四", 280.0, 5600.0)]


def design(fc, fy):
    k1 = 0.85 * fc * G_B
    As = k1 / fy * (G_D - math.sqrt(G_D ** 2 - 2 * G_MU / 0.9 / k1))
    n = math.ceil(As / G_AB - 1e-9)
    Ap = n * G_AB
    a = Ap * fy / k1
    return dict(As=As, n=n, pmn=0.9 * Ap * fy * (G_D - a / 2) / 1e5)


RES = [dict(name=n, fc=fc, fy=fy, **design(fc, fy)) for n, fc, fy in COMBOS]
PUB_AS = ["13.50", "10.13", "13.01", "9.754"]               # §4 比較彙整公佈的 As,req（圖上照此標示）


def fig1_compare():
    path = os.path.join(OUT, f"{TAG}-fig-1-combos.svg")
    cases = []
    for r, As_pub in zip(RES, PUB_AS):
        best = r["name"] == "組合二"
        col = C["bmd"] if best else (C["deform"] if r["fy"] == 5600 else C["member2"])
        cases.append((r["name"] + ("（最經濟）" if best else ""),
                      f"{r['fc']:g}/{r['fy']:g}, φMn {r['pmn']:.2f}",
                      r["As"], f"{As_pub} → {r['n']}-D25", col))
    bar_compare(cases, title=f"{TAG}　四種材料組合的需求 As,req（Mu = 19.5 tf·m）",
                sub="說明列：f'c/fy 與實配 φMn（tf·m）；右側：As,req（cm²）→ D25 支數。fy 4200 → 5600 少約 25%，f'c 210 → 280 只少 3–4%",
                note="組合二 2-D25 = 10.134 對需求 10.13，φMn 19.51 對 19.5：剛好夠，作答須註明",
                path=path)
    return path


FIGURES += [(fig1_compare, "§4 比較彙整", "以為提高 f'c 能大幅減少鋼筋；只比 As 不比整數支數")]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, sec, catches in FIGURES:
        print(f"{os.path.basename(fn()):<32} {sec:<18} 攔：{catches}")
    exp = [(13.50, 3, 21.57), (10.13, 2, 19.51), (13.01, 3, 22.43), (9.75, 2, 20.19)]   # §4 比較彙整（勘誤後）
    for r, (As, n, p) in zip(RES, exp):
        assert abs(r["As"] - As) < 0.01 and r["n"] == n and abs(r["pmn"] - p) < 0.006, r
    print("assert（解題圖解）OK")
