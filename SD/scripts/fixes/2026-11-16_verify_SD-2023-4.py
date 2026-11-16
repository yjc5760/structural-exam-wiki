#!/usr/bin/env python3
"""SD-2023-4 ㈠ 驗算（2026-11-16，U3-2-G4 階段 C；㈡ 為條文改寫，㈠ 數值不變）。
路徑一：閉合式 ξ = (ω_n/ω)E_D/(4πE_S0)；路徑二：數值積分迴圈面積、c_eq = E_D/(πωρ²)、ξ = c_eq/(2mω_n)。"""
import math, numpy as np
mis = []
def chk(n, a, b, tol=2e-3):
    ok = abs(a-b) <= tol*max(1, abs(b)); print(f"{n:30s} {a:.5g} vs {b:.5g} {'OK' if ok else 'MISMATCH'}")
    if not ok: mis.append(n)
PI = math.pi; m, k = 1.0, 16*PI**2; wn = math.sqrt(k/m)
REF = {("a",2*PI,.01):.199,("a",2*PI,.02):.199,("a",4*PI,.01):.199,("a",4*PI,.02):.199,
       ("b",2*PI,.01):.398,("b",2*PI,.02):.398,("b",4*PI,.01):.199,("b",4*PI,.02):.199,
       ("c",2*PI,.01):1.013,("c",2*PI,.02):.507,("c",4*PI,.01):.507,("c",4*PI,.02):.253}
t = np.linspace(0, 2*PI, 400001)
for (d, w, r), ref in REF.items():
    F0 = {"a": 5*r*w, "b": 20*PI*r, "c": 0.4*PI}[d]
    ED = PI*r*F0 if d != "c" else 4*r*F0
    xi1 = (wn/w)*ED/(4*PI*0.5*k*r*r)
    x = r*np.sin(t)
    F = F0*np.cos(t) if d != "c" else F0*np.sign(np.cos(t))
    EDn = abs(np.trapezoid(F*r*np.cos(t), t))
    xi2 = EDn/(PI*w*r*r)/(2*m*wn)
    chk(f"{d} ω={w/PI:.0f}π ρ={r} 閉合", xi1, ref, 3e-3); chk(f"{d} ω={w/PI:.0f}π ρ={r} 數值", xi2, xi1, 2e-3)
print("MISMATCHES:", len(mis), mis)
