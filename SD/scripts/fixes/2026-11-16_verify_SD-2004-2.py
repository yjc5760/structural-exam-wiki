#!/usr/bin/env python3
"""SD-2004-2 驗算（2026-11-16，U3-2-G1 階段 C）：m_b=0 化簡、等效勁度、周期、隔震層／上部結構變形分配。
路徑一：符號推導（sympy）；路徑二：2DOF 特徵值（m_b→0）數值；路徑三：極限檢查。輸出 MISMATCHES。"""
import sympy as sp, numpy as np
mis = []
def chk(name, a, b, tol=1e-6):
    ok = abs(a - b) <= tol * max(1, abs(b)); print(f"{name:40s} {a:.6g} vs {b:.6g} {'OK' if ok else 'MISMATCH'}")
    if not ok: mis.append(name)
m, k, kb, x1, x2, ug = sp.symbols("m k k_b x1 x2 u_g", positive=True)
# m_b = 0：隔震層方程式 → 靜力平衡
x1s = sp.solve(sp.Eq(kb*(x1-ug), k*(x2-x1)), x1)[0]
F = sp.simplify(k*(x2-x1s))
keq = sp.simplify(F/(x2-ug))
assert sp.simplify(keq - k*kb/(k+kb)) == 0
iso = sp.simplify((x1s-ug)/(x2-ug)); sup = sp.simplify((x2-x1s)/(x2-ug))
assert sp.simplify(iso - k/(k+kb)) == 0 and sp.simplify(sup - kb/(k+kb)) == 0 and sp.simplify(iso+sup-1) == 0
print("符號：k_eq = k k_b/(k+k_b)；x1-ug = k/(k+kb) v2（隔震層）；x2-x1 = kb/(k+kb) v2（上部結構）")
# 數值例（舊解無數值，取 m=1, k=100, kb=4）
mv, kv, kbv = 1.0, 100.0, 4.0
T_closed = 2*np.pi*np.sqrt(mv*(kv+kbv)/(kv*kbv))
mb = 1e-7*mv
M = np.diag([mb, mv]); K = np.array([[kbv + kv, -kv], [-kv, kv]])
w2, V = np.linalg.eig(np.linalg.solve(M, K)); i = np.argmin(w2.real)
T_num = 2*np.pi/np.sqrt(w2.real[i]); phi = V[:, i].real/V[1, i].real
chk("T（閉合式 vs 2DOF m_b→0）", T_closed, T_num, 1e-5)
chk("隔震層變形比 x1-ug / v2 = k/(k+kb)", phi[0], kv/(kv+kbv), 1e-5)
chk("上部結構變形比 x2-x1 / v2 = kb/(k+kb)", 1-phi[0], kbv/(kv+kbv), 1e-4)
chk("報告值 0.9615", kv/(kv+kbv), 0.9615, 1e-4)
chk("報告值 0.0385", kbv/(kv+kbv), 0.0385, 1e-3)
# 極限：kb>>k → T→2π√(m/k)；kb=k → √2 T_str
chk("kb=k 時 T/T_str = √2", 2*np.pi*np.sqrt(mv*2*kv/(kv*kv))/(2*np.pi*np.sqrt(mv/kv)), np.sqrt(2))
chk("kb=1e9 時 T→2π√(m/k)", 2*np.pi*np.sqrt(mv*(kv+1e9)/(kv*1e9)), 2*np.pi*np.sqrt(mv/kv), 1e-6)
print("MISMATCHES:", len(mis), mis)
