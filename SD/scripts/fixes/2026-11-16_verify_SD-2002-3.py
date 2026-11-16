#!/usr/bin/env python3
"""SD-2002-3 勘誤驗算（2026-11-16，X-G1 階段 C）
題意：題目正本判讀 #1（2.01）、#6（㈢施加載重 2w(x)，質量不變）。
以均質簡支梁（w、EI、L 取 1，垂直向示例）驗證：規範式的 Rayleigh 方向、施加 2w 直接代原式的偏差、修正式。"""
import numpy as np
from scipy.integrate import quad
mis = []
def chk(n, got, ref, tol=1e-6):
    ok = abs(got - ref) <= tol*max(1, abs(ref)); print(f"{n:42s} {got:.6f} ref {ref:.6f} {'OK' if ok else 'MISMATCH'}")
    if not ok: mis.append(n)
g = 9.81
chk("2π/√9.81", 2*np.pi/np.sqrt(g), 2.006, 1e-3)
chk("2π/√9.80", 2*np.pi/np.sqrt(9.80), 2.007, 1e-3)
# 無因次：w=m g，取 m=1、EI=1、L=1 → 週期係數以 L²√(m/EI) 表示，g 任意（約掉）
w = g
u = lambda x, p=w: p*(x**4 - 2*x**3 + x)/24.0          # 均佈 p 下簡支梁靜撓度（EI=1）
beta = quad(lambda x: w*u(x), 0, 1)[0]; gamma = quad(lambda x: w*u(x)**2, 0, 1)[0]
T = 2*np.pi*np.sqrt(gamma/(beta*g)); Tex = 2*np.pi/np.pi**2
chk("規範式 T 係數（施加 w）", T, 0.636172, 1e-5)
chk("精確 T1 係數 2/π", Tex, 0.636620, 1e-5)
print("Rayleigh 給 T 下限（T_R ≤ T1）:", T <= Tex)
if not T <= Tex: mis.append("Rayleigh 方向")
# ㈢ 施加 2w：u' = 2u；質量仍為 w/g
u2 = lambda x: u(x, 2*w)
b_naive = quad(lambda x: w*u2(x), 0, 1)[0]; g_naive = quad(lambda x: w*u2(x)**2, 0, 1)[0]
T_naive = 2*np.pi*np.sqrt(g_naive/(b_naive*g))
chk("直接代原式（權重仍用 w）/T", T_naive/T, np.sqrt(2))
b_fix = quad(lambda x: 2*w*u2(x), 0, 1)[0]            # β 權重改用實際施加的載重 2w
T_fix = 2*np.pi*np.sqrt(g_naive/(b_fix*g))
chk("修正式 β=∫p u'dx → T", T_fix, T)
chk("或直接代原式後 ÷√2", T_naive/np.sqrt(2), T)
# 舊解做法：2w 同時代進 β、γ 的權重（β'=4β、γ'=8γ）→ √2 T（只有在質量也加倍時才是真實週期）
b_old = quad(lambda x: 2*w*u2(x), 0, 1)[0]; g_old = quad(lambda x: 2*w*u2(x)**2, 0, 1)[0]
chk("舊解 β'/β", b_old/beta, 4.0); chk("舊解 γ'/γ", g_old/gamma, 8.0)
chk("舊解 T'/T", np.sqrt(g_old/b_old)/np.sqrt(gamma/beta), np.sqrt(2))
# 質量真的加倍（m→2m）時的精確週期比：√2
chk("質量加倍時 T1'/T1", np.sqrt(2), 1.414214, 1e-6)
print("MISMATCHES:", len(mis), mis if mis else "")
