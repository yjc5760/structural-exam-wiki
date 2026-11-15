#!/usr/bin/env python3
"""SD-2016-3 勘誤驗算（2026-11-15，FIX-SD-U1-3-B2）：三個正交條件是否相容；各組合的 α、β；最小平方解。
輸出 MISMATCHES。"""
import numpy as np, itertools
P = {1: np.array([1, 2, 3.]), 2: np.array([-1, -1, 2.]), 3: np.array([1, -1, 1.])}; m3 = 1000.
def row(i, j):   # φiᵀ diag(α,β,m3) φj = a α + b β + c = 0
    a, b, c = P[i]*P[j]; return np.array([a, b]), -c*m3
eqs = {(i, j): row(i, j) for i, j in itertools.combinations((1, 2, 3), 2)}
sol = {}
for pair in itertools.combinations(eqs, 2):
    A = np.array([eqs[p][0] for p in pair]); b = np.array([eqs[p][1] for p in pair]); sol[pair] = np.linalg.solve(A, b)
    rest = [e for e in eqs if e not in pair][0]; res = eqs[rest][0] @ sol[pair] - eqs[rest][1]
    print(f"用 {pair}：α = {sol[pair][0]:.1f}，β = {sol[pair][1]:.1f} kg；剩下的 {rest} 殘差 = {res:.1f}")
A = np.array([e[0] for e in eqs.values()]); b = np.array([e[1] for e in eqs.values()])
ls = np.linalg.lstsq(A, b, rcond=None)[0]; print("三式最小平方：α = %.1f，β = %.1f kg" % tuple(ls))
main = sol[((1, 2), (1, 3))]
mm = int(not np.allclose(main, [1500, 2250])) + int(not np.allclose(sol[((1, 2), (2, 3))], [10000/3, 4000/3])) + int(not np.allclose(sol[((1, 3), (2, 3))], [7000, 5000]))
print("MISMATCHES:", mm)
