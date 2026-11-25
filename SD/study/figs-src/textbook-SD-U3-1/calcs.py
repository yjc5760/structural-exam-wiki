# -*- coding: utf-8 -*-
"""SD-U3-1 結構耐震設計（含 RC 結構與鋼結構）：教科書講義的所有數值。
單位：tf、cm、kgf/cm²（依考題）。考題數字取自 raw/solutions（勘誤後版本）。
"""
import math

PI = math.pi
DB = {'D13': (1.27, 1.267), 'D25': (2.54, 5.067)}   # 直徑 cm、面積 cm²

# ---------- 第 1 章：短柱（2017-3） ----------
H17 = {1: 0.5, 2: 0.5, 3: 0.75, 4: 1.0}      # 有效柱高 / ℓ
K17 = {i: 1 / h ** 3 for i, h in H17.items()}
S17 = sum(K17.values())
V17 = {i: k / S17 for i, k in K17.items()}

# 懸臂梁法（2015-4）：柱 x = 0、7、17 m，A = 1 m²，柱高 4 m，P = 20 tf
CM = dict(x=[0.0, 7.0, 17.0], h=4.0, P=20.0, L=[7.0, 10.0])
CM['xbar'] = sum(CM['x']) / 3
CM['d'] = [x - CM['xbar'] for x in CM['x']]
CM['sum_d2'] = sum(d * d for d in CM['d'])
CM['M'] = CM['P'] * CM['h'] / 2                    # 反曲點（柱中點）以上的傾覆力矩
CM['N'] = [CM['M'] * d / CM['sum_d2'] for d in CM['d']]   # 柱軸力（負為拉）
CM['Vb'] = [abs(CM['N'][0]), abs(CM['N'][0] + CM['N'][1])]  # 梁剪力
CM['Mb'] = [CM['Vb'][0] * CM['L'][0] / 2, CM['Vb'][1] * CM['L'][1] / 2]
# 柱剪力：由節點彎矩平衡（柱頂彎矩 = 相接梁端彎矩和），V = 2M/h
CM['Mc'] = [CM['Mb'][0], CM['Mb'][0] + CM['Mb'][1], CM['Mb'][1]]
CM['Vc'] = [2 * m / CM['h'] for m in CM['Mc']]

# ---------- 第 2 章：崩塌機構（2010-4） ----------
Q2010 = dict(Ka=12 + 3, Kb=12 + 12)
Q2010['w_ratio'] = math.sqrt(Q2010['Ka'] / Q2010['Kb'])
Q2010['Va'] = 3.0     # ×Mp/L
Q2010['Vb'] = 4.0
Q2010['Zsq'] = 1 / 4  # 方形 Z = b³/4
# 彈塑性側力–位移曲線（單位 Mp/L、Mp L²/(EI)）：(a) 固-固柱 12、固-鉸柱 3
def pushover_a():
    # 固-固柱：Mp 於 V = 2Mp/L（兩端同時降伏）；固-鉸柱：V = Mp/L（底端降伏）
    k1, k2 = 12.0, 3.0              # EI/L³ 單位 → 位移以 Mp L²/EI 計：Δy1 = (2/L·Mp)/(12EI/L³) = Mp L²/(6EI)
    dy1 = 2 / k1; dy2 = 1 / k2
    pts = [(0, 0)]
    d1 = min(dy1, dy2)
    pts.append((d1, (k1 + k2) * d1))
    d2 = max(dy1, dy2)
    pts.append((d2, (k1 + k2) * d1 + (k2 if dy1 < dy2 else k1) * (d2 - d1)))
    pts.append((d2 * 1.8, pts[-1][1]))
    return pts


def pushover_b():
    k = 24.0; dy = 2 / 12.0
    return [(0, 0), (dy, k * dy), (dy * 3, k * dy)]


PA, PB = pushover_a(), pushover_b()

# ---------- 第 3、4 章：RC 特殊抗彎構架梁（2013-2） ----------
B = dict(b=40.0, h=60.0, d=53.0, fc=280.0, fy=4200.0, L=700.0, col=60.0, WD=2.7, WL=1.4)
B['ln'] = B['L'] - B['col']                    # 640 cm


def As_req(Mu_tfm, b=B['b'], d=B['d'], fc=B['fc'], fy=B['fy'], phi=0.9):
    Mu = Mu_tfm * 1e5
    Rn = Mu / (phi * b * d * d)
    rho = 0.85 * fc / fy * (1 - math.sqrt(1 - 2 * Rn / (0.85 * fc)))
    return rho * b * d, rho, Rn


def phiMn(As, b=B['b'], d=B['d'], fc=B['fc'], fy=B['fy']):
    a = As * fy / (0.85 * fc * b)
    return 0.9 * As * fy * (d - a / 2) / 1e5, a


def Mpr(As, b=B['b'], d=B['d'], fc=B['fc'], fy=B['fy']):
    a = 1.25 * As * fy / (0.85 * fc * b)
    return As * 1.25 * fy * (d - a / 2) / 1e5, a


MU = {'A−': 40, 'A+': 20, '中+': 19, 'B−': 48, 'B+': 17}
REQ = {k: As_req(v) for k, v in MU.items()}
SEL = {'A−': 5, 'B−': 6, 'A+': 3, 'B+': 3, '中+': 3}       # D25 根數（題解選配）
AS = {k: n * DB['D25'][1] for k, n in SEL.items()}
PHIMN = {k: phiMn(a)[0] for k, a in AS.items()}
RHO_MAX = {k: a / (B['b'] * B['d']) for k, a in AS.items()}
MPR = {k: Mpr(AS[k])[0] for k in ('A−', 'B−', 'A+', 'B+')}
WU = 1.2 * B['WD'] + 1.0 * B['WL']
VG = WU * B['ln'] / 100 / 2
VEQ1 = (MPR['A−'] + MPR['B+']) / (B['ln'] / 100)
VEQ2 = (MPR['A+'] + MPR['B−']) / (B['ln'] / 100)
VEQ = max(VEQ1, VEQ2)
VE = VEQ + VG
S_MAX = min(B['d'] / 4, 15.0, 6 * DB['D25'][0])
AV = 2 * DB['D13'][1]
PHIVS12 = 0.75 * AV * B['fy'] * B['d'] / 12 / 1000
VU_2H = VE - WU * 2 * B['h'] / 100

# ---------- 第 5 章：螺箍筋（2009-4） ----------
SP = dict(D=55.0, cover=4.0, fc=350.0, fyt=4200.0, s=7.5)
SP['Dc'] = SP['D'] - 2 * SP['cover']                  # 47 cm（至螺箍外緣）
SP['Ag'] = PI * SP['D'] ** 2 / 4
SP['Ac'] = PI * SP['Dc'] ** 2 / 4
SP['req1'] = 0.45 * (SP['Ag'] / SP['Ac'] - 1) * SP['fc'] / SP['fyt']
SP['req2'] = 0.12 * SP['fc'] / SP['fyt']
SP['ds'] = SP['Dc'] - DB['D13'][0]                    # 螺箍中心線直徑
SP['act'] = PI * SP['ds'] * DB['D13'][1] / (SP['Ac'] * SP['s'])
SP['clear'] = SP['s'] - DB['D13'][0]                  # 淨距

# ---------- 第 6 章：側推分布（2022-4 自設例：3 層、每層 W、層高 3 m、V = 600 kN） ----------
PO = dict(V=600.0, h=[3.0, 6.0, 9.0], w=[1.0, 1.0, 1.0])
def dist(k):
    wh = [w * h ** k for w, h in zip(PO['w'], PO['h'])]
    s = sum(wh)
    return [PO['V'] * x / s for x in wh]
PO['uniform'] = dist(0); PO['tri'] = dist(1); PO['k2'] = dist(2)
def k_exp(T):
    if T <= 0.5:
        return 1.0
    if T >= 2.5:
        return 2.0
    return 1 + (T - 0.5) / 2


if __name__ == '__main__':
    print('2017-3', V17, S17)
    print('懸臂梁法', CM)
    print('2010-4', Q2010, PA, PB)
    print('REQ', {k: (round(v[0], 2), round(v[1], 5)) for k, v in REQ.items()})
    print('AS', AS, 'phiMn', {k: round(v, 2) for k, v in PHIMN.items()}, 'rho', RHO_MAX)
    print('MPR', {k: round(v, 2) for k, v in MPR.items()}, 'wu', WU, 'Vg', VG, 'Veq', VEQ1, VEQ2, 'Ve', VE)
    print('smax', S_MAX, 'phiVs@12', PHIVS12, 'Vu2h', VU_2H)
    print('SP', SP)
    print('PO', PO, k_exp(1.0))
