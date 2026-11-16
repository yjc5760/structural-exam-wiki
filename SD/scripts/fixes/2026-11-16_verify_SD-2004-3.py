#!/usr/bin/env python3
"""SD-2004-3 勘誤驗算（2026-11-16，FIX-SD-U1-2-G1）
題意依題目正本 SD-2004-3-problem.md（已確認）：C 為鉸支承（在 A 正上方）、CD 剛性長 L/2、均佈 m0、D 自由；
EF 鉛直剛性鉸接連桿，F 距 C 為 L/4（E 在 x＝L/4）。φ(x)＝sin(πx/L)。
兩條路徑算 m*_CD：(1) 對 s 積分 m0 (s θ)^2；(2) I_C θ^2。另以數值積分核對。印出 MISMATCHES。"""
import sympy as sp, math
x, s, L, m, m0, EI = sp.symbols("x s L m m0 EI", positive=True)
phi = sp.sin(sp.pi*x/L)
vF = phi.subs(x, L/4)                      # √2/2（每單位 Z）
theta = vF/(L/4)                           # CD 繞 C 的轉角（每單位 Z）
mCD_1 = sp.integrate(m0*(s*theta)**2, (s, 0, L/2))
IC = m0*(L/2)**3/3
mCD_2 = IC*theta**2
mAB = sp.integrate(m*phi**2, (x, 0, L))
kst = sp.integrate(EI*sp.diff(phi, x, 2)**2, (x, 0, L))
# 數值：L=1, m0=1
n = 200000; num = sum((((i+0.5)/n*0.5)*(math.sqrt(2)/2)/0.25)**2 for i in range(n))*0.5/n
book = {"vF": sp.sqrt(2)/2, "theta": 2*sp.sqrt(2)/L, "vD": sp.sqrt(2), "mCD": m0*L/3, "mAB": m*L/2,
        "mstar": m*L/2 + m0*L/3, "kstar": sp.pi**4*EI/(2*L**3), "IC": m0*L**3/24,
        "omega2": (sp.pi**4*EI/(2*L**3))/(m*L/2 + m0*L/3)}
calc = {"vF": vF, "theta": theta, "vD": theta*L/2, "mCD": mCD_1, "mAB": mAB, "mstar": mAB + mCD_1,
        "kstar": kst, "IC": IC, "omega2": kst/(mAB + mCD_2)}
mis = 0
for kk in book:
    ok = sp.simplify(calc[kk] - book[kk]) == 0; mis += (not ok); print(f"{kk:7s} = {sp.simplify(calc[kk])}  {'OK' if ok else 'MISMATCH'}")
ok = sp.simplify(mCD_1 - mCD_2) == 0; mis += (not ok); print("積分法＝I_Cθ² :", ok)
ok = abs(num - 1/3) < 1e-6; mis += (not ok); print("數值積分 m*_CD/(m0 L) =", round(num, 8))
# 舊解（整根平移）對照值，僅列印
print("舊解 m*_CD（整根平移）=", sp.simplify(m0*(L/2)*vF**2), "；比值 新/舊 =", sp.Rational(4, 3))
# m0=0 極限：ω² = π⁴EI/(mL⁴)
ok = sp.simplify(book["omega2"].subs(m0, 0) - sp.pi**4*EI/(m*L**4)) == 0; mis += (not ok)
print("MISMATCHES:", mis)
