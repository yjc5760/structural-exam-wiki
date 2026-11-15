#!/usr/bin/env python3
"""SD-2021-2 勘誤驗算（2026-11-15，SD-U1-3 批 3 階段 C）
㈡ 半正弦脈衝最大位移改計入㈠求得的阻尼比 ξ=0.06（考卷「其阻尼比可由㈠計算得知」）。
三路：閉合分段解、solve_ivp 數值積分、Duhamel 卷積。最後印 MISMATCHES。"""
import math, numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
W, M, P0, TD = 10.0, 1e4, 1e5, 0.1
X1, X2 = 2.4, 20.0
bad = []
def chk(name, got, ref, tol):
    ok = abs(got - ref) <= tol; print(f"{name:28s} {got:.6g}  正本 {ref}  {'OK' if ok else 'MISMATCH'}")
    if not ok: bad.append(name)
Rd = lambda r, z: 1/math.sqrt((1-r*r)**2 + (2*z*r)**2)
XI = X1/(2*X2); chk("ξ（近似）", XI, 0.06, 1e-9)
chk("ξ（精確 brentq）", brentq(lambda z: Rd(1, z)/Rd(0.01, z) - X2/X1, .01, .3), 0.05999, 5e-5)
K = M*W**2; XST = P0/K; OM = math.pi/TD; r = OM/W; WD = W*math.sqrt(1-XI**2)
chk("k (N/m)", K, 1e6, 1); chk("x_st (m)", XST, 0.1, 1e-12); chk("ω_D (rad/s)", WD, 9.982, 5e-4)
den = (1-r*r)**2 + (2*XI*r)**2
C = XST*(1-r*r)/den; D = -XST*2*XI*r/den
chk("R_d(r=π, ξ)", math.hypot(C, D)/XST, 0.1126, 5e-5)
chk("φ (deg)", math.degrees(math.atan2(2*XI*r, 1-r*r)), 177.57, 5e-3)
A = -D; B = (XI*W*A - C*OM)/WD
def xf(t): return math.exp(-XI*W*t)*(A*math.cos(WD*t)+B*math.sin(WD*t)) + C*math.sin(OM*t) + D*math.cos(OM*t)
def vf(t, h=1e-7): return (xf(t+h)-xf(t-h))/(2*h)
u0, v0 = xf(TD), vf(TD)
chk("x(t_d) (cm)", 100*u0, 2.878, 5e-4); chk("ẋ(t_d) (m/s)", v0, 0.5134, 5e-5)
Af, Bf = u0, (v0 + XI*W*u0)/WD
tp = math.atan2(Bf*WD - XI*W*Af, Af*WD + XI*W*Bf)/WD
xmax = math.exp(-XI*W*tp)*(Af*math.cos(WD*tp)+Bf*math.sin(WD*tp))
chk("自由相峰值時刻 t (s)", TD+tp, 0.2016, 5e-4); chk("x_max 閉合 (cm)", 100*xmax, 5.677, 5e-4)
chk("R_d 計阻尼", xmax/XST, 0.568, 5e-4)
# 路徑二：數值積分
c = 2*XI*M*W
f = lambda t, y: [y[1], ((P0*math.sin(OM*t) if t <= TD else 0) - c*y[1] - K*y[0])/M]
s1 = solve_ivp(f, [0, TD], [0, 0], max_step=1e-5, rtol=1e-10, atol=1e-13)
s2 = solve_ivp(f, [TD, 1.0], s1.y[:, -1], max_step=1e-5, rtol=1e-10, atol=1e-13)
u = np.r_[s1.y[0], s2.y[0]]; chk("x_max solve_ivp (cm)", 100*abs(u).max(), 5.677, 5e-4)
chk("強迫相最大 (cm)", 100*abs(s1.y[0]).max(), 2.878, 5e-4)
# 路徑三：Duhamel（t=tp 處）
t = TD+tp
dh = quad(lambda s: P0*math.sin(OM*s)*math.exp(-XI*W*(t-s))*math.sin(WD*(t-s)), 0, TD, epsabs=1e-12)[0]/(M*WD)
chk("x_max Duhamel (cm)", 100*dh, 5.677, 5e-4)
# 對照：無阻尼
x0 = XST/(1-r*r)*(-r*math.sin(W*TD)); vx = XST/(1-r*r)*(OM*math.cos(OM*TD)-r*W*math.cos(W*TD))
chk("無阻尼 x(t_d) (cm)", 100*x0, 2.98, 5e-3); chk("無阻尼 x_max (cm)", 100*math.hypot(x0, vx/W), 6.22, 5e-3)
chk("差異 %", 100*(1-xmax/math.hypot(x0, vx/W)), 8.7, 0.05)
chk("衝量近似 (cm)", 100*(2*P0*TD/math.pi)/(M*W), 6.37, 5e-3)
print("MISMATCHES:", len(bad), bad)
