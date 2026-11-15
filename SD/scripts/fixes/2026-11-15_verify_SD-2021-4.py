#!/usr/bin/env python3
"""SD-2021-4 勘誤驗算（2026-11-15）：地表加速度振幅 0.50 g（題目正本判讀 #3），1g=980 cm/s²。
路徑 A：穩態放大係數閉合式；路徑 B：Newmark 平均加速度法線彈性時間歷時（9 s＋自由振動）；
路徑 C：彈性–完全塑性（EPP）時間歷時（只作對照，說明近似法則偏保守）。印 MISMATCHES: 0。"""
import numpy as np
m = 2e6; xi = 0.075; Ry = 2.5e7; g = 9.80; ag = 0.5 * g
Tg = 0.3; W = 2 * np.pi / Tg
bad = 0
def chk(name, a, b, tol=2e-3):
    global bad
    ok = abs(a - b) <= tol * max(1e-9, abs(b)); bad += (not ok)
    print(f"{'OK ' if ok else 'BAD'} {name}: {a:.5g} vs {b:.5g}")
def u0(T):
    w = 2 * np.pi / T
    return ag / np.sqrt((w**2 - W**2)**2 + (2 * xi * w * W)**2)
chk("u0(T=0.1) cm", u0(0.1) * 100, 0.1394); chk("u0(T=0.2) cm", u0(0.2) * 100, 0.8801)
chk("u_el(T=0.3) cm", u0(0.3) * 100, 7.447)
Ts = np.linspace(0.1, 0.3, 2001); chk("worst T in [0.1,0.3]", Ts[np.argmax(u0(Ts))], 0.3, 1e-9)
k = m * W**2; uy = Ry / k; R = k * u0(0.3) / Ry
chk("k N/m", k, 8.773e8); chk("Fe kN", k * u0(0.3) / 1e3, 65333); chk("uy cm", uy * 100, 2.850)
chk("R=mu (equal displacement)", R, 2.613); chk("mu equal energy", (R**2 + 1) / 2, 3.914)
# T=0.1 s 補驗算
k1 = m * (2 * np.pi / 0.1)**2; chk("T=0.1 uy cm", Ry / k1 * 100, 0.3166); print("T=0.1 elastic:", u0(0.1) < Ry / k1)
def newmark(T, epp=False, dt=2e-4, tend=12.0):
    w = 2 * np.pi / T; kk = m * w**2; c = 2 * xi * m * w; uyy = Ry / kk
    n = int(tend / dt); u = v = 0.0; fs = 0.0; up = 0.0
    p = lambda t: -m * ag * np.sin(W * t) if t <= 9.0 else 0.0
    a = (p(0) - c * v - fs) / m; umax = 0.0
    for i in range(n):
        t1 = (i + 1) * dt; u1 = u
        for _ in range(30):   # Newton（EPP）
            a1 = 4 / dt**2 * (u1 - u) - 4 / dt * v - a; v1 = v + dt / 2 * (a + a1)
            f = kk * (u1 - up)
            if epp and abs(f) > Ry: f = np.sign(f) * Ry; kt = 0.0
            else: kt = kk
            r = p(t1) - m * a1 - c * v1 - f
            du = r / (4 * m / dt**2 + 2 * c / dt + kt); u1 += du
            if abs(du) < 1e-12: break
        a1 = 4 / dt**2 * (u1 - u) - 4 / dt * v - a; v1 = v + dt / 2 * (a + a1)
        f = kk * (u1 - up)
        if epp and abs(f) > Ry: up = u1 - np.sign(f) * uyy
        u, v, a = u1, v1, a1; umax = max(umax, abs(u))
    return umax, uyy
ue, _ = newmark(0.3); chk("Newmark elastic T=0.3 cm", ue * 100, 7.447)
up_, uyy = newmark(0.3, epp=True); print(f"EPP T=0.3: umax={up_*100:.3f} cm, mu={up_/uyy:.3f}（對照，不列入核對）")
print("MISMATCHES:", bad)
