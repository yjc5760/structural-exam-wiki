#!/usr/bin/env python3
"""SD-2023-3 ㈢ 驗算（2026-11-16，U3-2-G4 階段 C；㈡㈣為條文題，數值答案不變）。
路徑一：T = 2π√(W/(gK))、ξ = E_D/(2πK D²)；路徑二：ω = √(K g/W) 換算、ξ = E_D/(4π E_S0)。"""
import math
mis = []
def chk(n, a, b, tol=5e-3):
    ok = abs(a-b) <= tol*max(1, abs(b)); print(f"{n:34s} {a:.5g} vs {b:.5g} {'OK' if ok else 'MISMATCH'}")
    if not ok: mis.append(n)
W, D, K, ED, g = 5000.0, 0.4, 1000.0, 50.0, 9.81
m = W/g; T1 = 2*math.pi*math.sqrt(W/(g*K)); T2 = 2*math.pi/math.sqrt(K/m)
xi1 = ED/(2*math.pi*K*D**2); ES0 = 0.5*K*D**2; xi2 = ED/(4*math.pi*ES0)
chk("m (kN·s²/m) 正本 509.68", m, 509.68, 1e-4)
chk("T 路徑一 vs 正本 4.49 s", T1, 4.49, 2e-3); chk("T 路徑二 vs 路徑一", T2, T1, 1e-9)
chk("E_S0 = 80 kN·m", ES0, 80.0, 1e-9)
chk("ξ 路徑一 vs 正本 0.0497", xi1, 0.0497, 2e-3); chk("ξ 路徑二 vs 路徑一", xi2, xi1, 1e-9)
chk("g=9.8 時 T 差異 <0.1%", 2*math.pi*math.sqrt(W/(9.8*K)), T1, 1e-3)
print(f"T_eff = {T1:.3f} s > 2.5 s（9.2.1 靜力法上限）:", T1 > 2.5)
print("MISMATCHES:", len(mis), mis)
