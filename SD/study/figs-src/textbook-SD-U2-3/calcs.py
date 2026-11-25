# -*- coding: utf-8 -*-
"""SD-U2-3 橋梁耐震設計規範：教科書講義的所有數值（無因次化 L = EI = w = 1 時以數值積分驗算）。"""
import math
import numpy as np

PI = math.pi
G = 9.81
C201 = 2 * PI / math.sqrt(G)          # 2.006（g = 9.81 m/s²，u 以 m 計）
C201_cm = 2 * PI / math.sqrt(981.0)   # u 以 cm 計時的係數 0.2006

X = np.linspace(0, 1, 40001)


def integ(y):
    return float(np.trapezoid(y, X)) if hasattr(np, 'trapezoid') else float(np.trapz(y, X))


# 2024-4：簡支梁均佈 w 的靜撓度 u = w x (L³ − 2Lx² + x³)/(24EI)
u_ss = X * (1 - 2 * X ** 2 + X ** 3) / 24
Q2024 = dict(beta=integ(u_ss), zeta=integ(u_ss ** 2))
Q2024['beta_exact'] = 1 / 120
Q2024['zeta_exact'] = 31 / 362880
Q2024['coef_code'] = Q2024['zeta_exact'] / Q2024['beta_exact']     # = 31/3024，T = 2π√(coef·wL⁴/gEI)
Q2024['coef_theory'] = 1 / PI ** 4
Q2024['T_ratio'] = math.sqrt(Q2024['coef_code'] / Q2024['coef_theory'])   # T_code/T_1
Q2024['w_ratio'] = 1 / Q2024['T_ratio']
Q2024['umax'] = 5 / 384

# 2010-3：兩跨上構（每跨 L，單位長度質量 m）＋一支墩（高 L、底固頂鉸 k = 3EI/L³）
Q2010 = dict(k=3.0, span=2.0)
Q2010['coef'] = 2 * PI * math.sqrt(2 / 3)     # T = coef · L² √(m/EI) = 5.130

# 2002-3：施加 2w 時的修正
Q2002 = dict(ratio_wrong=math.sqrt(2), corr=1 / math.sqrt(2))

# 第 4 章：三軸譜示範（Sa 定值段 2.5A、Sv 定值段、Sd 定值段）
SPEC = dict(SDS=0.8, SD1=0.45)
SPEC['T0'] = SPEC['SD1'] / SPEC['SDS']

# 建築與橋梁分母
DEN = dict(building=1.4, bridge=1.2)
DEN['ratio'] = DEN['building'] / DEN['bridge']

if __name__ == '__main__':
    print('C201', C201, C201_cm)
    print('2024', Q2024)
    print('2010', Q2010)
    print('2002', Q2002); print(DEN)
