#!/usr/bin/env python3
"""SD-2018-4 驗算（2026-11-16，U3-2-G4 階段 C 規範表核對）：考卷提示 B 表 vs 現行規範表 3-1（B_S、B_1）；
以兩表重算 Te、B、ξe、μ、R，與正本比對。路徑二：回代 D、A、ξe 公式閉合。"""
import math, numpy as np
mis = []
def chk(n, a, b, tol=3e-3):
    ok = abs(a-b) <= tol*max(1, abs(b)); print(f"{n:40s} {a:.5g} vs {b:.5g} {'OK' if ok else 'MISMATCH'}")
    if not ok: mis.append(n)
XI = [2, 5, 10, 20, 30, 40, 50]
EXAM = [0.80, 1.00, 1.25, 1.50, 1.63, 1.70, 1.75]
BS   = [0.80, 1.00, 1.33, 1.60, 1.79, 1.87, 1.93]   # 現行表 3-1 短週期
B1   = [0.80, 1.00, 1.25, 1.50, 1.63, 1.70, 1.75]   # 現行表 3-1 長週期
chk("考卷表 = 現行 B1（逐列最大差）", max(abs(a-b) for a, b in zip(EXAM, B1)), 0.0, 1e-12)
g, D, A = 980.0, 25.0, 0.08
Te = 2*math.pi*math.sqrt(D/(A*g)); chk("Te 正本 3.548 s", Te, 3.548, 1e-3)
Sa = min(0.48/Te, 0.8); B = g/(4*math.pi**2)*Sa*Te**2/D; chk("B 正本 1.691", B, 1.691, 1e-3)
def solve(tab):
    xi = float(np.interp(B, tab, XI))/100; mu = math.pi*A*xi/2; R = D/(A-mu); return xi, mu, R
xi, mu, R = solve(B1)
chk("ξe 正本 0.387", xi, 0.387, 2e-3); chk("μ 正本 0.0487", mu, 0.0487, 2e-3); chk("R 正本 798 cm", R, 798, 3e-3)
chk("回代 D/R+μ = A", D/R+mu, A, 1e-9)
chk("回代 ξe 公式", 2/math.pi*mu/(D/R+mu), xi, 1e-9)
Te2 = 2*math.pi*math.sqrt(1/((1/R+mu/D)*g)); chk("回代 Te 公式", Te2, Te, 1e-9)
chk("回代 D", g/(4*math.pi**2)*Sa*Te2**2/float(np.interp(xi*100, XI, B1)), D, 1e-6)
xs, ms, Rs = solve(BS)
print(f"（誤用短週期 B_S：ξe={xs:.4f}, μ={ms:.4f}, R={Rs:.1f} cm）")
chk("誤用 B_S 的 ξe ≈ 0.248", xs, 0.248, 5e-3); chk("誤用 B_S 的 μ ≈ 0.031", ms, 0.031, 1e-2); chk("誤用 B_S 的 R ≈ 512 cm", Rs, 512, 5e-3)
print("MISMATCHES:", len(mis), mis)
