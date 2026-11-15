#!/usr/bin/env python3
"""SD-2015-2 勘誤驗算（2026-11-15，FIX-SD-U1-3-B2）：k1=k2=50 kN/cm、m1=m2=50 t（考卷），三路計算。
路徑一：閉合解 λ=(3∓√5)/2；路徑二：scipy.linalg.eigh；路徑三：kgf–cm 重力單位制。輸出 MISMATCHES 數。"""
import numpy as np, scipy.linalg as sl
m = 50e3; k = 50e3/1e-2            # kg、N/m（50 kN/cm = 5×10⁶ N/m）
lam = np.array([(3-5**0.5)/2, (3+5**0.5)/2]); w_a = np.sqrt(lam*k/m)
phi_a = np.array([1/(1-l) for l in lam])           # 屋頂/二樓
K = k*np.array([[2,-1],[-1,1.]]); M = m*np.eye(2)
w2, V = sl.eigh(K, M); w_b = np.sqrt(w2); phi_b = V[1]/V[0]
g = 981.0                                          # cm/s²
kc = 50e3/9.81; mc = 50e3/g                        # kgf/cm、kgf·s²/cm
w_c = np.sqrt(np.linalg.eigvalsh(kc*np.array([[2,-1],[-1,1.]]))/mc)
exp = dict(w1=6.1803, w2=16.1803, phi1=1.6180, phi2=-0.6180)
got = dict(w1=w_a[0], w2=w_a[1], phi1=phi_a[0], phi2=phi_a[1])
mm = sum(abs(got[x]-exp[x]) > 1e-3*max(1, abs(exp[x])) for x in exp)
mm += int(not np.allclose(w_a, w_b, rtol=1e-9)) + int(not np.allclose(phi_a, phi_b, rtol=1e-9)) + int(not np.allclose(w_a, w_c, rtol=1e-3))
orth = np.array([1, phi_a[0]]) @ M @ np.array([1, phi_a[1]])
print("ω =", w_a.round(4), "rad/s；f =", (w_a/2/np.pi).round(4), "Hz；T =", (2*np.pi/w_a).round(4), "s")
print("φ1 = {1,", round(phi_a[0], 4), "}；φ2 = {1,", round(phi_a[1], 4), "}；φ1ᵀMφ2 =", round(orth, 6))
print("舊解（300／200 tf/cm）：ω = 44.29、108.50 rad/s → 與本解比", round(44.29/w_a[0], 2), "倍")
print("MISMATCHES:", mm)
