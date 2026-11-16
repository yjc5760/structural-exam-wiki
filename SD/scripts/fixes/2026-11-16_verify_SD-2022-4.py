#!/usr/bin/env python3
"""SD-2022-4 勘誤驗證（2026-11-16）：五種側力分布算例獨立重算（SRSS 以兩條路徑），並檢查正本數值與舊值殘留。"""
import os, numpy as np, scipy.linalg as sl
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "raw", "solutions", "SD-2022-4", "SD-2022-4.md")
s = open(P, encoding="utf-8").read().replace("\r\n", "\n")
mm = []
def chk(name, got, exp, tol):
    ok = abs(got - exp) <= tol; print(f"{'OK ' if ok else 'BAD'} {name}: {got:.4f} vs {exp}"); ok or mm.append(name)
def has(t):
    ok = t in s; print(("OK " if ok else "BAD"), "正本含", t); ok or mm.append("缺 " + t)
m = 100.0; H = np.array([3, 6, 9.0]); V = 600.0; T = 2.5; w = np.full(3, m)
for i, e in enumerate([100, 200, 300]): chk(f"倒三角 F{i+1}", (V*w*H/(w*H).sum())[i], e, 0.05)
k = 2 if T >= 2.5 else (1 if T <= 0.5 else 1 + (T-0.5)/2)
for i, e in enumerate([42.9, 171.4, 385.7]): chk(f"指數 F{i+1}", (V*w*H**k/(w*H**k).sum())[i], e, 0.05)
Ft = 0.0 if T <= 0.7 else min(0.07*T*V, 0.25*V); chk("Ft", Ft, 105, 0.01)
Fe = (V-Ft)*w*H/(w*H).sum(); Fe[-1] += Ft
for i, e in enumerate([82.5, 165.0, 352.5]): chk(f"經驗 F{i+1}", Fe[i], e, 0.01)
A = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 1.0]])
kst = (2*np.pi/T)**2*m/np.linalg.eigvalsh(A)[0]; chk("層勁度", kst, 3189, 0.5)
ev, ph = sl.eigh(kst*A, m*np.eye(3)); Ts = 2*np.pi/np.sqrt(ev)
for n in range(3): ph[:, n] /= ph[np.argmax(abs(ph[:, n])), n]
for n, e in enumerate([2.500, 0.892, 0.617]): chk(f"T{n+1}", Ts[n], e, 0.0005)
for i, e in enumerate([0.445, 0.802, 1.0]): chk(f"phi1[{i}]", ph[i, 0], e, 0.0005)
for i, e in enumerate([1.0, 0.445, -0.802]): chk(f"phi2[{i}]", ph[i, 1], e, 0.0005)
M = m*np.eye(3); G = ph.T@M@np.ones(3)/np.diag(ph.T@M@ph)
for n, e in enumerate([1.220, 0.349, -0.134]): chk(f"Gamma{n+1}", G[n], e, 0.0005)
Me = G**2*np.diag(ph.T@M@ph)/300
for n, e in enumerate([0.914, 0.075, 0.011]): chk(f"有效質量比{n+1}", Me[n], e, 0.0005)
Sa = 1/Ts
# 路徑一：振態層剪力 cumsum
Vn = np.array([np.cumsum((G[n]*m*ph[:, n]*Sa[n])[::-1])[::-1] for n in range(3)])
Vs = np.sqrt((Vn**2).sum(0))
for i, e in enumerate([112.7, 89.9, 58.8]): chk(f"SRSS 層剪力比 V{i+1}", Vs[i], e, 0.05)
F = (Vs - np.append(Vs[1:], 0))*V/Vs[0]
# 路徑二：以上三角矩陣乘振態力
U = np.triu(np.ones((3, 3))); Vn2 = np.array([U@(G[n]*m*ph[:, n]*Sa[n]) for n in range(3)])
Vs2 = np.sqrt((Vn2**2).sum(0)); F2 = (Vs2 - np.append(Vs2[1:], 0))*V/Vs2[0]
for i, e in enumerate([121.4, 165.3, 313.3]):
    chk(f"SRSS F{i+1}", F[i], e, 0.05); chk(f"SRSS F{i+1}（路徑二）", F2[i], e, 0.05)
F1 = V*m*ph[:, 0]/(m*ph[:, 0]).sum()
for i, e in enumerate([118.8, 214.1, 267.0]): chk(f"一階振態分布 F{i+1}", F1[i], e, 0.05)
chk("舊振態正交性 φ1ᵀMφ2", np.array([0.3, 0.7, 1])@M@np.array([1, 0.3, -0.7]), -19, 1e-9)
for t in ["82.5", "165.0", "352.5", "121.4", "165.3", "313.3", "42.9", "171.4", "385.7", "118.8／214.1／267.0", "{0.445, 0.802, 1.000}", "1.220", "0.349", "−0.134", "3189"]: has(t)
# 殘留：舊定義與舊值只准在 §1 常見誤讀與 §5.7
body = s[s.index("\n## 2."):]; main = body[:body.index("### 5.7")]
for t in ["{0.3, 0.7, 1.0}", "0.3, 0.7", "多模態各自", "不對：", "\\text{kN}\\cdot\\text{s}^2", "First-Mode", "Pushover 1", "| 90 |", "210 |"]:
    n = main.count(t); print(("OK " if n == 0 else "BAD"), "殘留", t, n); n and mm.append("殘留 " + t)
print("MISMATCHES:", len(mm), mm if mm else "")
