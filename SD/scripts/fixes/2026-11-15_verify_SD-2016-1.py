#!/usr/bin/env python3
"""SD-2016-1 勘誤驗算（2026-11-15，FIX-SD-U1-3-B2）：㈣ 三角形脈衝下的最大位移。
路徑一：衝量近似時間歷時取 max|v|；路徑二：無阻尼精確解（solve_ivp）；路徑三：振態座標 Duhamel 閉合積分。
另驗算單自由度三角形脈衝 DLF：衝量近似 = π t_d/T。輸出 MISMATCHES。"""
import numpy as np
from scipy.integrate import solve_ivp, quad
m, k = 2e3, 1e5; M = np.diag([2*m, m]); K = np.array([[3*k, -k], [-k, k]])
P0, td = 2.4e5, 0.2
p = lambda t: P0*t/0.1 if t <= 0.1 else (P0*(td - t)/0.1 if t <= td else 0.0)
w = np.array([5., 10.]); Phi = np.array([[1, 1], [2, -1.]]); Mn = np.diag(Phi.T @ M @ Phi)
t = np.linspace(0, 4, 40001)
# 路徑一：衝量放在脈衝形心 0.1 s
I = P0*td/2; eta_dot = Phi[1]*I/Mn
tau = np.clip(t - 0.1, 0, None)
v_imp = Phi @ np.array([eta_dot[n]/w[n]*np.sin(w[n]*tau) for n in range(2)])
# 路徑二：精確數值積分
f = lambda tt, y: np.r_[y[2:], np.linalg.solve(M, np.array([0, p(tt)]) - K @ y[:2])]
s = solve_ivp(f, [0, 4], [0, 0, 0, 0], t_eval=t, max_step=1e-3, rtol=1e-10, atol=1e-13)
# 路徑三：Duhamel 閉合（t > td 後自由振動，取 t 網格上最大）
def eta(n, tt):
    return quad(lambda s_: Phi[1, n]*p(s_)*np.sin(w[n]*(tt - s_)), 0, min(tt, td), points=[0.1], limit=200)[0]/(Mn[n]*w[n])
tg = np.linspace(0, 4, 4001); v_d = np.array([[Phi[i] @ np.array([eta(n, tt) for n in range(2)]) for tt in tg] for i in range(2)])
r = dict(imp1=abs(v_imp[0]).max(), imp2=abs(v_imp[1]).max(), ex1=abs(s.y[0]).max(), ex2=abs(s.y[1]).max(),
         du1=abs(v_d[0]).max(), du2=abs(v_d[1]).max(), srss1=np.hypot(0.8, 0.4), srss2=np.hypot(1.6, 0.4))
for kk, vv in r.items(): print(f"{kk:6s} = {vv:.4f} m")
def dlf(tdT):
    W = 2*np.pi; d = tdT; pp = lambda tt: 2*tt/d if tt <= d/2 else (2*(d - tt)/d if tt <= d else 0.0)
    ss = solve_ivp(lambda tt, y: [y[1], pp(tt) - W**2*y[0]], [0, 3], [0, 0], max_step=1e-4, rtol=1e-10)
    return abs(ss.y[0]).max()*W**2
for n in range(2):
    T = 2*np.pi/w[n]; print(f"振態{n+1}: td/T = {td/T:.3f}，DLF 精確 = {dlf(td/T):.3f}，衝量近似 πtd/T = {np.pi*td/T:.3f}（舊解寫 2πtd/T = {2*np.pi*td/T:.2f}）")
exp = dict(imp1=1.039, imp2=1.761, ex1=0.997, ex2=1.709)
mm = sum(abs(r[x] - exp[x]) > 2e-3 for x in exp) + int(abs(r["ex1"] - r["du1"]) > 3e-3) + int(abs(r["ex2"] - r["du2"]) > 3e-3)
print("MISMATCHES:", mm)
