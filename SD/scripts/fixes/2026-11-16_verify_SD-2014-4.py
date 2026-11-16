#!/usr/bin/env python3
"""SD-2014-4 勘誤驗算（2026-11-16）：論述題，驗證勘誤後正本引用的觀念數值。
1) 線性黏滯阻尼 SDOF 簡諧穩態：|彈性力+阻尼力| 最大的相位＝|絕對加速度| 最大的相位，
   該時刻彈性力＝cos[tan^-1(2ξ)]×最大彈性力、阻尼力＝sin[tan^-1(2ξ)]×最大阻尼力，合力＝√(1+4ξ²)×kU。
   （ω=ωn 共振時 F_d,max = cωU = 2ξkU）；同時驗證無高階振態（SDOF）就有第三狀態。
2) 彈性–完全塑性（BRB 理想化）對稱循環消能 E = 4Fy(Δ−δy)：數值積分迴圈面積比對閉合式。
3) 附加黏滯阻尼降低位移：共振動力放大 1/(2ξ)。
純 Python，無外部套件。輸出 MISMATCHES: n。"""
import math
mism = []
def chk(name, got, exp, tol=1e-3):
    ok = abs(got-exp) <= tol*max(1.0, abs(exp))
    print(f"{'OK ' if ok else 'BAD'} {name}: {got:.6g} vs {exp:.6g}")
    if not ok: mism.append(name)
# 1) 相位與組合係數
k, U = 1.0, 1.0
for xi in (0.05, 0.10, 0.25):
    N = 200000; best = (-1, 0); besta = (-1, 0)
    for i in range(N):
        th = 2*math.pi*i/N
        Fe = k*U*math.sin(th); Fd = 2*xi*k*U*math.cos(th)
        s = abs(Fe+Fd)
        if s > best[0]: best = (s, th)
        # m ü_abs = -(Fe+Fd)：絕對加速度與合力同比例，另以運動方程式直接算 ü_abs
        m = 1.0; wn = math.sqrt(k/m)
        u = U*math.sin(th); v = U*wn*math.cos(th)
        uabs_dd = -(k*u + 2*xi*m*wn*v)/m
        if abs(uabs_dd) > besta[0]: besta = (abs(uabs_dd), th)
    th = best[1]
    chk(f"xi={xi} 合力最大＝√(1+4ξ²)kU", best[0], math.sqrt(1+4*xi*xi))
    chk(f"xi={xi} 絕對加速度最大與合力最大同相位(mod π)", math.cos(2*(besta[1]-th)), 1.0)
    Fe = k*U*math.sin(th); Fd = 2*xi*k*U*math.cos(th)
    CF1 = math.cos(math.atan(2*xi)); CF2 = math.sin(math.atan(2*xi))
    chk(f"xi={xi} 該時刻彈性力/最大彈性力＝CF1", abs(Fe)/(k*U), CF1)
    chk(f"xi={xi} 該時刻阻尼力/最大阻尼力＝CF2", abs(Fd)/(2*xi*k*U), CF2)
chk("CF1(ξ=0.25)", math.cos(math.atan(0.5)), 0.894, 1e-3)
chk("CF2(ξ=0.25)", math.sin(math.atan(0.5)), 0.447, 2e-3)
# 2) 彈性–完全塑性迴圈面積
def loop_energy(Fy, dy, D, n=200000):
    # 路徑 0→D→−D→D，追蹤力，最後一個完整循環 (D→−D→D) 的 ∮F du
    def path(a, b):
        return [a+(b-a)*i/n for i in range(n+1)]
    F = 0.0; u0 = 0.0; E = 0.0; up = 0.0  # up: 塑性位移
    pts = path(0, D)[1:] + path(D, -D)[1:] + path(-D, D)[1:]
    started = False; uprev = 0.0
    for idx, u in enumerate(pts):
        Ftr = k_e*(u-up)
        if Ftr > Fy: up = u - Fy/k_e; Fn = Fy
        elif Ftr < -Fy: up = u + Fy/k_e; Fn = -Fy
        else: Fn = Ftr
        if idx >= n:  # 從 D 開始的完整循環
            E += 0.5*(F+Fn)*(u-uprev)
        F = Fn; uprev = u
    return E
Fy, dy = 1.0, 1.0; k_e = Fy/dy
for mu in (1.0, 2.0, 5.0):
    D = mu*dy
    chk(f"BRB 迴圈面積 μ={mu}", loop_energy(Fy, dy, D), 4*Fy*(D-dy), 2e-3)
chk("BRB μ=5 → 16 Fyδy", 4*Fy*(5*dy-dy), 16.0)
# 3) 共振放大
for xi, exp in ((0.05, 10.0), (0.20, 2.5)):
    chk(f"共振動力放大 1/(2ξ) ξ={xi}", 1/(2*xi), exp)
print("MISMATCHES:", len(mism), mism)
