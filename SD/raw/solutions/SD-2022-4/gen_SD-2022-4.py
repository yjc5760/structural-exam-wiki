#!/usr/bin/env python3
"""SD-2022-4 解題圖解（struct-diagram；2026-11-16，組 U3-1-G2 階段 E）
fig-1 五種側推力豎向分布的 3 層算例（各層側力），數值由 §4 的算例假設重算（與 verify 腳本同式）：
m＝100 t×3、H＝3/6/9 m、V＝600 kN、T＝2.5 s、層勁度使 T1＝2.5 s、Sa ∝ 1/T。
用法：python3 gen_SD-2022-4.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
import numpy as np, scipy.linalg as sl
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2022-4"
# ── §4 算例假設 ──
M_ = 100.0; H = np.array([3, 6, 9.0]); V = 600.0; T = 2.5
def distributions():
    w = np.full(3, M_)
    d = {}
    d["均勻"] = V*w/w.sum()
    d["倒三角"] = V*w*H/(w*H).sum()
    k = 2 if T >= 2.5 else (1 if T <= 0.5 else 1 + (T - 0.5)/2)
    d[f"指數 k={k:g}"] = V*w*H**k/(w*H**k).sum()
    Ft = 0.0 if T <= 0.7 else min(0.07*T*V, 0.25*V)
    fe = (V - Ft)*w*H/(w*H).sum(); fe[-1] += Ft; d["經驗（規範式）"] = fe
    A = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 1.0]])
    kst = (2*np.pi/T)**2*M_/np.linalg.eigvalsh(A)[0]
    ev, ph = sl.eigh(kst*A, M_*np.eye(3)); Ts = 2*np.pi/np.sqrt(ev)
    G = ph.T@(M_*np.ones(3))/np.diag(ph.T@(M_*np.eye(3))@ph)
    Vn = np.array([np.cumsum((G[n]*M_*ph[:, n]/Ts[n])[::-1])[::-1] for n in range(3)])
    Vs = np.sqrt((Vn**2).sum(0)); d["SRSS"] = (Vs - np.append(Vs[1:], 0))*V/Vs[0]
    return d, Ft
COL = [C["member2"], C["deform"], C["sfd"], C["load"], C["bmd"]]

def fig1():
    d, Ft = distributions()
    W, Hc = 1100, 540
    cv = Canvas(W, Hc, bg="#FFFFFF")
    cv.text_px(W/2, 32, f"{TAG}　五種側推力豎向分布（3 層算例，V = {V:g} kN，各層側力 kN）", 17, C["text"], weight="700")
    cv.text_px(W/2, 58, "m = 100 t（每層）、H = 3／6／9 m、T = 2.5 s；SRSS 取 Sa ∝ 1/T；經驗分布採規範豎向分配式（含頂層 F_t）", 12.5, C["muted"])
    names = list(d)
    pw = (W - 80)/len(names); base_y = 495; fh = 110   # 每層高度像素
    fmax = max(max(v) for v in d.values()); scale = (pw - 60)/fmax
    for j, nm in enumerate(names):
        x0 = 40 + j*pw + 18
        cv.rect_px(40 + j*pw + 4, 76, pw - 8, 450, C["panel"], 10, C["border"], 1)
        cv.text_px(40 + j*pw + pw/2, 100, nm, 14, COL[j], weight="700")
        # 建築線：柱
        cv.parts.append(f'<line x1="{x0}" y1="{base_y}" x2="{x0}" y2="{base_y - 3*fh}" stroke="{C["member"]}" stroke-width="3"/>')
        cv.parts.append(f'<line x1="{x0 - 12}" y1="{base_y}" x2="{x0 + 12}" y2="{base_y}" stroke="{C["member"]}" stroke-width="3"/>')
        for i in range(3):
            y = base_y - (i + 1)*fh
            f = d[nm][i]; L = f*scale
            cv.parts.append(f'<line x1="{x0 - 8}" y1="{y}" x2="{x0 + 8}" y2="{y}" stroke="{C["member"]}" stroke-width="3"/>')
            # 側推力箭頭（長度與力成正比；Canvas 為 y 向上座標，故用 Hc − y）
            tmp = Canvas(W, Hc); tmp.arrow((x0 + 4, Hc - y), (x0 + 4 + L, Hc - y), COL[j], 3.0, 9)
            cv.parts += tmp.parts
            cv.text_px(x0 + 10 + L/2, y - 14, f"{f:.1f}", 13, C["text"])
            if j == 0: cv.text_px(x0 - 16, y, f"{i+1}F", 12, C["muted"], "end")
        if nm.startswith("經驗"):
            cv.text_px(40 + j*pw + pw/2, base_y + 17, f"頂層含 F_t = {Ft:g}", 12, C["load"])
    return cv.save(f"{OUT}/{TAG}-fig-1-distributions.svg")

FIGURES = [(fig1, "攔下『經驗分布＝一階振態』『SRSS 無數值／多次側推』與粗估振態，五種分布同一組假設並排比較")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
