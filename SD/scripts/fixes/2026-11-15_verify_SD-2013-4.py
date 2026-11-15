#!/usr/bin/env python3
"""SD-2013-4 勘誤驗算（2026-11-15，FIX-SD-U1-3-B2）：只取前兩振態的穩態底彎矩。
路徑一：逐振態等效靜力 f_n = ω_n² M φ_n q_n，對地面取矩；路徑二：閉合式 Σ_n ω_n² q_n (hᵀ M φ_n)；
對照：舊法（總加速度慣性力）與替代質量分配。輸出 MISMATCHES。單位 tf、m、s（質量以 tf/g）。"""
import numpy as np
g = 9.81; W = np.array([50., 125., 150.]); M = np.diag(W/g); h = np.array([40., 30., 15.])
P = np.array([[1, 1], [0.5, -0.8], [0.25, -0.6]]); w = np.array([5., 12.]); A = 1.5; wb = 8.
one = np.ones(3)
G = np.array([P[:, n] @ M @ one / (P[:, n] @ M @ P[:, n]) for n in range(2)])
q = np.array([-G[n]*A/(w[n]**2 - wb**2) for n in range(2)])
fn = np.array([w[n]**2 * q[n] * (M @ P[:, n]) for n in range(2)])   # tf
Mb_n = fn @ h; Mb1 = Mb_n.sum()
Mb2 = sum(w[n]**2*q[n]*(h @ M @ P[:, n]) for n in range(2))
X = P @ q; old = -(M @ (-wb**2*X + A)) @ h                            # 舊法：-m(ü+üg) 取矩
print("Γ =", G.round(4), "q =", q.round(5), "m")
print("f_n (tf) 振態1 =", fn[0].round(3), "振態2 =", fn[1].round(3), "合計 =", fn.sum(0).round(3))
print("M_b,n =", Mb_n.round(1), "→ M_b =", round(Mb1, 1), "tf·m（閉合式", round(Mb2, 1), "）；基底剪力 =", round(fn.sum(), 2), "tf")
print("舊法（總加速度慣性力）=", round(abs(old), 1), "tf·m；φ1ᵀMφ2·g =", round(P[:, 0] @ M @ P[:, 1]*g, 2), "；ΦΓ =", (P @ G).round(3))
W2 = np.array([100., 150., 150.]); M2 = np.diag(W2/g)
alt = 0
for n in range(2):
    Gn = P[:, n] @ M2 @ one/(P[:, n] @ M2 @ P[:, n]); qn = -Gn*A/(w[n]**2 - wb**2); alt += w[n]**2*qn*(h @ M2 @ P[:, n])
print("替代質量分配 100/150/150 tf：M_b =", round(alt, 1), "tf·m")
exp = dict(Mb=227.8, old=401.0, f_top=18.583, f_mid=-10.801, f_bot=-12.763)
got = dict(Mb=Mb1, old=abs(old), f_top=fn.sum(0)[0], f_mid=fn.sum(0)[1], f_bot=fn.sum(0)[2])
mm = sum(abs(got[k]-exp[k]) > 2e-3*abs(exp[k]) for k in exp) + int(abs(Mb1-Mb2) > 1e-9)
print("MISMATCHES:", mm)
