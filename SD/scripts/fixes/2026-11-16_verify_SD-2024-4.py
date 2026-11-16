#!/usr/bin/env python3
"""SD-2024-4 勘誤驗算（2026-11-16，X-G1 階段 C）：答案（β、ζ、T_code/T1）重驗，並更正 §4 Step 6 形狀比較表與 §5.2、§5.4 的說明數字。"""
import numpy as np, sympy as sp
from scipy.integrate import quad
mis = []
def chk(n, got, ref, tol=1e-4):
    ok = abs(got-ref) <= tol*max(1, abs(ref)); print(f"{n:40s} {got:.6f} ref {ref:.6f} {'OK' if ok else 'MISMATCH'}")
    if not ok: mis.append(n)
x, L, w, EI, m, g = sp.symbols("x L w EI m g", positive=True)
u = w*(x**4 - 2*L*x**3 + L**3*x)/(24*EI)
beta = sp.integrate(w*u, (x, 0, L)); zeta = sp.integrate(w*u**2, (x, 0, L))
print("β =", sp.simplify(beta), " ζ =", sp.simplify(zeta))
chk("β ×120EI/(w²L⁵)", float(sp.simplify(beta*120*EI/(w**2*L**5))), 1.0)
chk("ζ/β ×EI/(wL⁴) = 31/3024", float(sp.simplify(zeta/beta*EI/(w*L**4))), 31/3024)
Tc = 2*np.pi*np.sqrt(31/3024); T1 = 2/np.pi
chk("T_code 係數 (L²√(m/EI))", Tc, 0.636165); chk("T1 係數", T1, 0.636620)
chk("T_code/T1", Tc/T1, 0.99929); chk("3024/31", 3024/31, 97.548); chk("π⁴", np.pi**4, 97.409)
chk("分母常數相對差 %", (3024/31-np.pi**4)/np.pi**4*100, 0.143, 1e-2)
chk("週期相對差 %", (1-Tc/T1)*100, 0.071, 1e-2)
# 形狀比較：正規化靜變位 u/u(L/2) 與 sin
un = lambda s: (s**4 - 2*s**3 + s)/(5/16)
chk("u/umax @ x/L=0.25", un(0.25), 0.7125); chk("sin(π/4)", np.sin(np.pi/4), 0.7071)
chk("u/umax @0.18", un(0.18), 0.5420); chk("sin(0.18π)", np.sin(0.18*np.pi), 0.5358)
chk("差 @0.25", un(0.25)-np.sin(np.pi/4), 0.0054, 1e-2)
s = np.linspace(0, 1, 20001); d = np.abs(un(s) - np.sin(np.pi*s))
chk("全跨最大差", d.max(), 0.0062, 1e-2); print("  發生於 x/L =", round(s[d.argmax()], 3))
# 拋物線 φ=x(L−x)，Rayleigh 商（應變能法）
U = quad(lambda t: (-2.0)**2, 0, 1)[0]; Tk = quad(lambda t: (t*(1-t))**2, 0, 1)[0]
w2 = U/Tk; chk("拋物線 ω²·mL⁴/EI", w2, 120.0, 1e-9)
chk("拋物線頻率高估 %", (np.sqrt(w2)/np.pi**2 - 1)*100, 10.99, 1e-3)
chk("正弦振態 Rayleigh 商誤差", (quad(lambda t: (np.pi**2*np.sin(np.pi*t))**2, 0, 1)[0]/quad(lambda t: np.sin(np.pi*t)**2, 0, 1)[0])/np.pi**4 - 1, 0.0, 1e-9)
print("MISMATCHES:", len(mis), mis if mis else "")
