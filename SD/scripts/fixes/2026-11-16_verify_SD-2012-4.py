#!/usr/bin/env python3
"""SD-2012-4 ㈡ 勘誤驗算（2026-11-16）：D'_D = D_D/sqrt(1+(T/T_eD)^2) 的物理關係。
路徑 1：單質量串聯彈簧（隔震層 k_i、上部 k_s）閉合解；等速度段譜位移 Sd ∝ T。
路徑 2：兩質量 2DOF（基礎層質量很小）振態疊加（SRSS），同一譜位移律，數值逼近路徑 1。
檢核正本寫出的每個數值與關係；最後印 MISMATCHES。"""
import numpy as np, math
mis = []
def chk(name, got, exp, tol=1e-3):
    ok = abs(got - exp) <= tol * max(1, abs(exp))
    print(f"{'OK ' if ok else 'BAD'} {name}: {got:.6g} (正本 {exp:.6g})")
    if not ok: mis.append(name)

m = 1.0; DDc = 1.0                     # 無因次：D_D 取 1
def series(TeD, T):
    ki = 4*math.pi**2*m/TeD**2; ks = 4*math.pi**2*m/T**2
    Ttot = math.sqrt(TeD**2 + T**2)     # 串聯：1/k = 1/ki + 1/ks
    chk_T = 2*math.pi*math.sqrt(m*(1/ki + 1/ks))
    assert abs(chk_T - Ttot) < 1e-12
    Dtot = DDc * Ttot/TeD               # Sd ∝ T（D_D 以 T_eD、剛體算）
    iso = Dtot * ks/(ki+ks); sup = Dtot * ki/(ki+ks)
    return Ttot, Dtot, iso, sup
# 正本例：T_eD = 3.0 s、T = 1.0 s
Ttot, Dtot, iso, sup = series(3.0, 1.0)
r = 1/3
chk("例 系統週期 sqrt(TeD^2+T^2) [s]", Ttot, 3.1623)
chk("例 總位移 / D_D = sqrt(1+r^2)", Dtot, 1.0541)
chk("例 隔震層位移 / D_D = 公式 D'_D", iso, 1/math.sqrt(1+r*r))
chk("例 隔震層位移 / D_D", iso, 0.9487)
chk("例 上部變形 / D_D = D'_D r^2", sup, (1/math.sqrt(1+r*r))*r*r)
chk("例 上部變形 / D_D", sup, 0.1054)
old_sup = (1/math.sqrt(1+r*r))*r     # 舊解寫法 D'_D·T/T_eD
print(f"   舊解上部變形 D'_D·r = {old_sup:.4f}（與串聯解 {sup:.4f} 不符，僅 r=1 時相同）")
# 掃描 r：公式恆等
for TeD, T in [(2.5,0.3),(3,0.5),(4,1.0),(2,2)]:
    _, Dt, i_, s_ = series(TeD, T); rr = T/TeD
    chk(f"掃描 r={rr:.3f} 隔震層=公式", i_, 1/math.sqrt(1+rr*rr), 1e-9)
    chk(f"掃描 r={rr:.3f} 總位移=D_D sqrt(1+r^2)", Dt, math.sqrt(1+rr*rr), 1e-9)
# 極端情況
chk("T=TeD 時 D'_D/D_D = 1/sqrt2", 1/math.sqrt(2), 0.7071)
chk("r=0.1 修正量 1-1/sqrt(1.01) [%]", 100*(1-1/math.sqrt(1.01)), 0.4963)
chk("r=0.4 修正量 1-1/sqrt(1.16) [%]", 100*(1-1/math.sqrt(1.16)), 7.152)
# 路徑 2：2DOF，基礎質量 mb = 0.001 m，Sd_n = D_D * T_n / T_eD
mb, ms = 1e-3, 1.0
TeD, T = 3.0, 1.0
ki = 4*math.pi**2*(ms+mb)/TeD**2; ks = 4*math.pi**2*ms/T**2
K = np.array([[ki+ks, -ks], [-ks, ks]]); M = np.diag([mb, ms])
w2, ph = np.linalg.eig(np.linalg.solve(M, K)); idx = np.argsort(w2); w2 = w2[idx]; ph = ph[:, idx]
iso2 = 0; sup2 = 0; tot2 = 0
for n in range(2):
    p = ph[:, n]; G = p @ M @ np.ones(2) / (p @ M @ p); Tn = 2*math.pi/math.sqrt(w2[n]); Sd = DDc*Tn/TeD
    iso2 += (G*p[0]*Sd)**2; sup2 += (G*(p[1]-p[0])*Sd)**2; tot2 += (G*p[1]*Sd)**2
chk("2DOF 隔震層位移 ≈ D'_D", math.sqrt(iso2), 0.9487, 3e-3)
chk("2DOF 上部變形 ≈ D'_D r^2", math.sqrt(sup2), 0.1054, 3e-3)
chk("2DOF 屋頂總位移 ≈ D_D sqrt(1+r^2)", math.sqrt(tot2), 1.0541, 3e-3)
print("MISMATCHES:", len(mis), mis)
