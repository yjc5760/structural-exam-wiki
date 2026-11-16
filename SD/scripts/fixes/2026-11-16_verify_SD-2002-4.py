#!/usr/bin/env python3
"""SD-2002-4 獨立重算（2026-11-16）。路徑 1：閉合解 ω²=(k/m)(3∓√5)/2；路徑 2：scipy eigh；路徑 3：振態等值靜力 Ku=f。
Sa = 0.2·C(T)·g（題目正本判讀 #1）；比對正本中的數值與主答（絕對值和）、替代答（SRSS）。"""
import os, math, re
import numpy as np
from scipy.linalg import eigh
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "raw", "solutions", "SD-2002-4", "SD-2002-4.md")
md = open(P, encoding="utf-8").read()
g = 9.81; m = 800.0; L = 3.0; EI = 4.5e4
def C(T):
    if T <= 0.03: return 1.0
    if T <= 0.2: return 8.824*T + 0.7352
    if T <= 1.32: return 2.5
    if T <= 3.3: return 3.3/T
    return 1.0
kc = 12*EI/L**3; ks = 2*kc
wA2 = ks/m; TA = 2*math.pi/math.sqrt(wA2); dA = C(TA)*0.2*g/wA2
M = np.diag([m, m]); K = np.array([[2*ks, -ks], [-ks, ks]])
w2, Ph = eigh(K, M)
w2c = np.array([(3-math.sqrt(5))/2, (3+math.sqrt(5))/2])*ks/m
assert np.allclose(w2, w2c)
T = 2*math.pi/np.sqrt(w2); r = np.ones(2)
X = []; Sd = []
for n in range(2):
    phi = Ph[:, n]/Ph[0, n]; G = phi@M@r/(phi@M@phi); sd = C(T[n])*0.2*g/w2[n]
    Sd.append(sd); X.append(G*phi*sd)
    u = np.linalg.solve(K, M@(G*phi)*C(T[n])*0.2*g)      # 路徑 3
    assert np.allclose(u, G*phi*sd)
X = np.array(X); dB = math.sqrt((X[:, 0]**2).sum())
D_abs = (dA + dB)*1000; D_srss = math.hypot(dA, dB)*1000
vals = {"k_col": (kc, "20{,}000"), "TA": (TA, f"{TA:.3f}"), "dA mm": (dA*1000, f"{dA*1000:.1f}"),
        "T1": (T[0], f"{T[0]:.3f}"), "T2": (T[1], f"{T[1]:.3f}"), "C1": (C(T[0]), f"{C(T[0]):.3f}"),
        "Sd1": (Sd[0], f"{Sd[0]:.4f}"), "Sd2": (Sd[1], f"{Sd[1]:.5f}"), "X1": (X[0,0], f"{X[0,0]:.4f}"),
        "X2": (X[1,0], f"{X[1,0]:.5f}"), "dB mm": (dB*1000, f"{dB*1000:.1f}"),
        "Δ abs": (D_abs, f"{D_abs:.1f}"), "Δ srss": (D_srss, f"{D_srss:.1f}")}
mis = [(k, s) for k, (v, s) in vals.items() if s not in md]
for k, (v, s) in vals.items(): print(f"{k:7s} {v:.6g}  （正本字串 {s}）")
# 主答必須是絕對值和
if not re.search(r"\\boxed\{\\Delta_\{\\min\} \\approx 269", md): mis.append(("主答", "269 boxed"))
for bad in ("而非絕對值和", "B棟一樓", "text{1F}", "_{B,1F}"):
    if bad in "\n".join(l for l in md.split("## 2.", 1)[1].splitlines() if not l.startswith("*修正日期")): mis.append(("殘留", bad))
for x in mis: print("MISMATCH", x)
print("MISMATCHES:", len(mis))
