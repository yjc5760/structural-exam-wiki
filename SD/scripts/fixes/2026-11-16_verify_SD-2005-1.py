#!/usr/bin/env python3
"""SD-2005-1 驗算（2026-11-16，U3-2-G1 階段 C）：彈性—完全塑性（EPP）遲滯迴圈的每循環消能 W_D 與等效阻尼比。
路徑一：閉合式 W_D = 4 F_y (δmax-δy)、ξ = W_D/(2π K_eff δmax²)；路徑二：數值積分迴圈面積；路徑三：ξ 的另一閉合式 2(μ-1)/(πμ)。"""
import numpy as np
mis = []
def chk(name, a, b, tol=1e-4):
    ok = abs(a - b) <= tol * max(1, abs(b)); print(f"{name:42s} {a:.6g} vs {b:.6g} {'OK' if ok else 'MISMATCH'}")
    if not ok: mis.append(name)
Fy, Ke = 1.0, 1.0; dy = Fy/Ke
for mu in (2.0, 5.0, 10.0):
    dmax = mu*dy
    # 數值：EPP 迴圈（+dmax → -dmax → +dmax）
    t = np.linspace(0, 2*np.pi, 200001); u = dmax*np.cos(t)
    F = np.zeros_like(u); f = Fy; up = u[0]
    for j in range(len(u)):
        f = np.clip(f + Ke*(u[j]-up), -Fy, Fy); up = u[j]; F[j] = f
    # 第二圈穩態
    WD_num = -np.trapezoid(F, u) if hasattr(np, "trapezoid") else -np.trapz(F, u)
    WD_num = abs(WD_num)
    WD = 4*Fy*(dmax-dy)
    chk(f"μ={mu}: W_D 閉合 vs 數值", WD, WD_num, 2e-3)
    Keff = Fy/dmax
    xi = WD/(2*np.pi*Keff*dmax**2)
    chk(f"μ={mu}: ξ 閉合 vs 2(μ-1)/(πμ)", xi, 2*(mu-1)/(np.pi*mu))
    xi_old = WD/(4*np.pi*Ke*dmax**2)
    print(f"   （舊式 W_D/(4π K_e δmax²) = {xi_old:.4f}，與正確值 {xi:.4f} 不同 → 舊式勘誤）")
print("MISMATCHES:", len(mis), mis)
