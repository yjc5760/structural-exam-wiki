#!/usr/bin/env python3
"""SD-2021-3 勘誤驗算（2026-11-15）：初始位移 {6,6,6} cm（題目正本判讀 #1），頂層層剪力 V3=k(v3-v2)。
路徑 A：振態展開閉合解；路徑 B：狀態空間數值積分（scipy solve_ivp）；路徑 C：最大值上確界（三振態絕對值和、長時間掃描）。
k=m=1 無因次；V3 以 cm·k 表示。印 MISMATCHES: 0 表示全部一致。"""
import numpy as np
from scipy.integrate import solve_ivp
s3 = np.sqrt(3)
M = np.diag([1, 1, 0.5]); K = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 1.]])
w2 = np.array([2 - s3, 2, 2 + s3]); w = np.sqrt(w2)
Phi = np.array([[1, 1, 1], [s3, 0, -s3], [2, -1, 2.]])
bad = 0
def chk(name, a, b, tol=1e-6):
    global bad
    ok = abs(a - b) <= tol * max(1, abs(b)); bad += (not ok)
    print(f"{'OK ' if ok else 'BAD'} {name}: {a:.6f} vs {b:.6f}")
for i in range(3):   # 題給振態滿足特徵方程
    chk(f"eig residual {i+1}", np.linalg.norm(K @ Phi[:, i] - w2[i] * M @ Phi[:, i]), 0.0)
u0 = np.array([6, 6, 6.])
Mn = np.diag(Phi.T @ M @ Phi); q0 = (Phi.T @ M @ u0) / Mn
for a, b, n in zip(q0, [2 + s3, 2, 2 - s3], ["q1(0)", "q2(0)", "q3(0)"]): chk(n, a, b)
coef = q0 * (Phi[2] - Phi[1])           # V3 各振態係數（cm·k）
for a, b, n in zip(coef, [1, -2, 1], ["c1", "c2", "c3"]): chk("V3 " + n, a, b)
V3 = lambda t: (coef[None, :] * np.cos(np.outer(t, w))).sum(1)
sol = solve_ivp(lambda t, y: np.r_[y[3:], -np.linalg.solve(M, K @ y[:3])], (0, 60), np.r_[u0, 0, 0, 0],
                rtol=1e-11, atol=1e-12, dense_output=True)
tt = np.linspace(0, 60, 6001); y = sol.sol(tt)
chk("ODE vs modal max diff", np.max(np.abs((y[2] - y[1]) - V3(tt))), 0.0, 1e-6)
chk("V3(0)", V3(np.array([0.]))[0], 0.0)
tl = np.linspace(0, 3000, 3_000_001); v = V3(tl)
chk("sup|V3| (scan, 3000)", -v.min(), 4.0, 2e-3)
chk("max positive V3", v.max(), 2.25, 2e-3)
chk("|V3| upper bound sum|c|", np.abs(coef).sum(), 4.0)
# 舊讀法 {6,0,0} 對照（不採用）
q0o = (Phi.T @ M @ np.array([6, 0, 0.])) / Mn; co = q0o * (Phi[2] - Phi[1])
for a, b, n in zip(co, [2 - s3, -4, 2 + s3], ["c1", "c2", "c3"]): chk("old V3 " + n, a, b)
chk("old SRSS", np.sqrt((co**2).sum()), np.sqrt(30))
print("MISMATCHES:", bad)
