# -*- coding: utf-8 -*-
"""教科書講義 SA-U1-2 的所有數值（圖與內文共用，先算再寫）。
單位：kN、m（SA-2002-2、SA-2004-1 依考卷用 T／t）。
執行 python3 calcs.py 會印出全部數值供內文對帳。
"""
from fractions import Fraction as Fr
import numpy as np

# ─────────────────────────────────────────────
# 第 1 章：靜不定度計數（全部由種子 S1「數未知 − 數方程」）
# ─────────────────────────────────────────────

def deg_truss(m, r, j):
    """桁架：未知 = m 根桿力 + r 個反力；方程 = 每節點 2 條。"""
    return m + r - 2 * j


def deg_frame(m, r, j, c):
    """剛架：未知 = 每桿 3 個（一端 N、V、M）+ r；方程 = 每節點 3 條 + 每個釋放 1 條。"""
    return 3 * m + r - 3 * j - c


def deg_tree(r, c):
    """無閉合環的樹狀梁／剛架：整個結構當一個自由體（3 條）+ 每個釋放 1 條。"""
    return r - 3 - c


# 考題計數表：(題號, 型式, 參數, 說明)
TRUSS_CASES = [
    ('SA-2002-2', dict(m=14, r=4, j=9), 'A、B 皆鉸支承；A–B 虛線不是桿件'),
    ('SA-2010-1', dict(m=13, r=3, j=8), 'B 滾支承貼垂直牆（反力水平）、G 鉸支承'),
    ('SA-2013-1', dict(m=20, r=4, j=12), 'a、i 皆鉸支承；a–b 為一根連續桿'),
]
FRAME_CASES = [
    # 題號, m, r, j, c, 樹狀?, 說明
    ('SA-2012-1', 4, 4, 5, 1, True, 'a 固定(3)＋d 滾(1)；c 內鉸'),
    ('SA-2004-1', 3, 4, 4, 1, True, 'A 固定(3)＋C 滾(1)；B 內鉸'),
    ('SA-2002-1', 7, 4, 8, 1, True, 'A、H 鉸支承(2+2)；F 內鉸'),
    ('SA-2016-1', 4, 5, 5, 1, True, 'A 鉸(2)＋E 固定(3)；C 內鉸 → 一度靜不定'),
    ('SA-2016-1 誤讀', 4, 4, 5, 1, True, '若把 E 讀成鉸支承(2)：算出 0，誤判靜定'),
    ('SA-2022-1', 3, 5, 4, 1, True, 'a 固定(3)＋c 彈簧(1)＋d 滾(1)；b 內鉸 → 一度靜不定'),
    ('SA-2004-3', None, 4, None, 1, True, 'A 固定(3)＋C 彈簧(1)；B 內鉸 → 靜定'),
]

# SA-2024-2 反用：要靜定需要幾根桿
J_2024_2, R_2024_2 = 14, 3
M_NEED_2024_2 = 2 * J_2024_2 - R_2024_2           # 25
M_COUNT_2024_2 = 6 + 6 + 7 + 6                    # 下弦6 上弦6 豎7 斜6

# ─────────────────────────────────────────────
# 通用：平面剛體平衡求解（未知力線性方程組）
# ─────────────────────────────────────────────

def solve_bodies(bodies, unknowns):
    """bodies: list of list of terms；每個 term = (fx, fy, x, y, couple, coef_dict)
    其中 coef_dict 給未知量的係數（作用力 = 已知 + Σ coef*未知）。
    為簡單起見，term 寫成 ('F', x, y, fx_known, fy_known, {'U': (cx, cy)}) 或 ('M', m_known, {'U': cm})。
    回傳 dict 未知量 → 值。每個 body 3 條方程：ΣFx、ΣFy、ΣM(原點, 逆時針為正)。
    """
    n = len(unknowns)
    idx = {u: i for i, u in enumerate(unknowns)}
    A, b = [], []
    for body in bodies:
        rows = [np.zeros(n) for _ in range(3)]
        rhs = [0.0, 0.0, 0.0]
        for t in body:
            if t[0] == 'F':
                _, x, y, fx, fy, co = t
                rhs[0] -= fx; rhs[1] -= fy; rhs[2] -= (x * fy - y * fx)
                for u, (cx, cy) in co.items():
                    rows[0][idx[u]] += cx; rows[1][idx[u]] += cy; rows[2][idx[u]] += x * cy - y * cx
            else:
                _, mk, co = t
                rhs[2] -= mk
                for u, cm in co.items():
                    rows[2][idx[u]] += cm
        A += rows; b += rhs
    sol = np.linalg.lstsq(np.array(A), np.array(b), rcond=None)
    x = sol[0]
    resid = np.array(A) @ x - np.array(b)
    assert np.allclose(resid, 0, atol=1e-9), resid
    return {u: float(x[idx[u]]) for u in unknowns}


# ─────────────────────────────────────────────
# 第 2 章：內鉸
# ─────────────────────────────────────────────
# SA-2012-1：a 固定(x=0)、b 40↓(x=4)、c 內鉸(x=8)、d 滾(x=12)、e 40↓(x=16)；ac 段 2EI、ce 段 EI
X12 = dict(a=0, b=4, c=8, d=12, e=16)
P12 = 40.0
# 附屬 c–e：未知 Vc（鉸對 c–e 的向上力）、Rd
s12_sub = solve_bodies(
    [[('F', 8, 0, 0, 0, {'Vc': (0, 1)}), ('F', 12, 0, 0, 0, {'Rd': (0, 1)}), ('F', 16, 0, 0, -P12, {}),
      ('F', 8, 0, 0, 0, {'Hc': (1, 0)})]],
    ['Vc', 'Rd', 'Hc'])
# 主 a–c：c 點受 −Vc（作用反作用）
s12_main = solve_bodies(
    [[('F', 0, 0, 0, 0, {'Ra': (0, 1), 'Ha': (1, 0)}), ('M', 0, {'Ma': 1}),
      ('F', 4, 0, 0, -P12, {}), ('F', 8, 0, 0, -s12_sub['Vc'], {})]],
    ['Ra', 'Ha', 'Ma'])
R12 = dict(Vc=s12_sub['Vc'], Rd=s12_sub['Rd'], Ra=s12_main['Ra'], Ma=s12_main['Ma'])


def M12(x):
    """SA-2012-1 彎矩（正＝下緣受拉），由右端往左累加（右側自由體）。"""
    M = 0.0
    for xp, F in ((16, -P12), (12, R12['Rd']), (4, -P12)):
        if xp > x:
            M += F * (xp - x)
    return M


def EI12(x):
    return 2.0 if x < 8 else 1.0   # 以 EI 為單位


# 數值積分：雙重積分求變形曲線（a 固定：y=θ=0；c 鉸處斜率不連續；d：y=0）
def deflection12(n=16000):
    xs = np.linspace(0, 16, n + 1)
    dx = xs[1] - xs[0]
    k = np.array([M12(x) / EI12(x) for x in xs])   # 曲率（以 1/EI 為單位），正＝下凹向上
    # a–c：θ(0)=0, y(0)=0
    th = np.zeros_like(xs); y = np.zeros_like(xs)
    ic = int(round(8 / dx)); id_ = int(round(12 / dx))
    for i in range(1, ic + 1):
        th[i] = th[i - 1] + 0.5 * (k[i] + k[i - 1]) * dx
        y[i] = y[i - 1] + 0.5 * (th[i] + th[i - 1]) * dx
    yc = y[ic]
    # c–e：y(c)=yc，θ(c+) 未知 = t0；要求 y(d)=0（線性於 t0）
    def run(t0):
        th2 = np.zeros_like(xs); y2 = np.zeros_like(xs)
        th2[ic] = t0; y2[ic] = yc
        for i in range(ic + 1, len(xs)):
            th2[i] = th2[i - 1] + 0.5 * (k[i] + k[i - 1]) * dx
            y2[i] = y2[i - 1] + 0.5 * (th2[i] + th2[i - 1]) * dx
        return th2, y2
    _, ya = run(0.0); _, yb = run(1.0)
    t0 = -ya[id_] / (yb[id_] - ya[id_])
    th2, y2 = run(t0)
    th[ic + 1:] = th2[ic + 1:]; y[ic + 1:] = y2[ic + 1:]
    return xs, y, th, dict(yc=yc, thc_left=th[ic], thc_right=t0, ye=y[-1], the=th[-1])


XS12, Y12, TH12, D12 = deflection12()
# 題解答案（以 1/EI 為單位）：y_c = +7040/3（向上）、y_e = −12160/3（向下）、θ_e = 1120（順時針）
ANS12 = dict(yc=Fr(7040, 3), ye=Fr(-12160, 3), the=-1120)

# SA-2004-1：A 固定(0,0)、柱高 4（中點 4t →）、B 內鉸(0,4)、梁 B→C 4 m 滾支承、C→D 2 m 懸臂、w=2 t/m 全長 6 m
s04_sub = solve_bodies(
    [[('F', 0, 4, 0, 0, {'By': (0, 1), 'Bx': (1, 0)}), ('F', 4, 4, 0, 0, {'Cy': (0, 1)}),
      ('F', 3, 4, 0, -12.0, {})]],
    ['By', 'Bx', 'Cy'])
s04_main = solve_bodies(
    [[('F', 0, 0, 0, 0, {'Ax': (1, 0), 'Ay': (0, 1)}), ('M', 0, {'MA': 1}),
      ('F', 0, 2, 4.0, 0, {}), ('F', 0, 4, -s04_sub['Bx'], -s04_sub['By'], {})]],
    ['Ax', 'Ay', 'MA'])
R04 = {**s04_sub, **s04_main}
X04_VZERO = R04['By'] / 2.0          # 梁上 V = By − 2x = 0
M04_MAX = R04['By'] * X04_VZERO - X04_VZERO ** 2

# SA-2002-2：三鉸型桁架（座標 A 原點；單位 T）
# 載重：D(0,12)、F(8,12)、C(16,12)、H(24,12)、I(32,12) 各 20 T 向下；D 點 16 T 向右
LOADS_0202 = [(0, 12, 16, -20), (8, 12, 0, -20), (16, 12, 0, -20), (24, 12, 0, -20), (32, 12, 0, -20)]
left_0202 = [(0, 12, 16, -20), (8, 12, 0, -20)]   # 左半（不含 C 節點的載重：C 的 20T 歸哪半不影響對 C 取矩）
# 手寫：ΣM_A=0 → By；ΣM_C(左半)=0 → Ax
# 注意：16T 向右作用在 y=12，對 A 的力矩 = −y·fx = −192（順時針）；By·32 − 20(0+8+16+24+32) − 192 = 0
By0202 = Fr(20 * 80 + 192, 32)                                    # 56
Ay0202 = 100 - By0202                                             # 44
# 左半對 C(16,12) 取矩：Ax·(0−12)·(−1)... 寫成：ΣM_C = Ay·(0−16) − Ax·(0−12) + 外力
# 外力（左半，C 本身載重通過 C 不計）：D(0,12)：fx=16 → −(12−12)·16 = 0；fy=−20 → (0−16)(−20)=320；F(8,12)：(8−16)(−20)=160
# Ay 在 A(0,0)：(0−16)·Ay；Ax 在 A：−(0−12)·Ax = 12Ax
Ax0202 = Fr(-(320 + 160) - (-16) * Ay0202, 12)                    # 12Ax − 16Ay + 480 = 0
Bx0202 = -(Ax0202 + 16)
R0202 = dict(Ax=Ax0202, Ay=Ay0202, Bx=Bx0202, By=By0202)

# 三鉸結構推力（只有垂直載重時）：H = M_C^0 / h，M_C^0＝同跨簡支梁在 C 的彎矩
Ay0_v = Fr(20 * (32 + 24 + 16 + 8 + 0), 32)                      # 50
MC0_v = Ay0_v * 16 - 20 * 16 - 20 * 8                             # 320
H_v_0202 = MC0_v / 12                                             # 80/3

# SA-2002-1：剛架，F 內鉸；A(0,0)、H(6,0) 鉸支承；未知 Ax Ay Hx Hy Fx Fy（Fx,Fy＝鉸對右分離體的力）
left0201 = [('F', 0, 0, 0, 0, {'Ax': (1, 0), 'Ay': (0, 1)}),
            ('F', 0, 4, 10.0, 0, {}),            # C 點 10 kN →
            ('M', 6.0, {}),                       # B 點 6 kN-m 逆時針
            ('M', -2.0 * 2, {}),                  # C–D 均布力矩 2 kN-m/m 順時針 × 2 m
            ('F', 3, 4, 0, -8.0, {}),             # E 點 8 kN ↓
            ('M', 4.0, {}),                       # F 左（梁端）4 kN-m 逆時針
            ('F', 6, 4, 0, 0, {'Fx': (-1, 0), 'Fy': (0, -1)})]
right0201 = [('F', 6, 0, 0, 0, {'Hx': (1, 0), 'Hy': (0, 1)}),
             ('M', -4.0, {}),                     # F 下（柱頂）4 kN-m 順時針
             ('F', 6, 1, -4.0, 0, {}),            # G–H 2 kN/m 向左 × 2 m，合力在 y=1
             ('F', 6, 4, 0, 0, {'Fx': (1, 0), 'Fy': (0, 1)})]
R0201 = solve_bodies([left0201, right0201], ['Ax', 'Ay', 'Hx', 'Hy', 'Fx', 'Fy'])
# 錯法：把 F 兩側力偶相加抵銷（兩個都拿掉）
left_bad = [t for t in left0201 if not (t[0] == 'M' and t[1] == 4.0)]
right_bad = [t for t in right0201 if not (t[0] == 'M' and t[1] == -4.0)]
R0201_bad = solve_bodies([left_bad, right_bad], ['Ax', 'Ay', 'Hx', 'Hy', 'Fx', 'Fy'])


def show():
    print('== 第 1 章 計數')
    for q, p, note in TRUSS_CASES:
        print(f'{q:14s} 桁架 m={p["m"]} r={p["r"]} j={p["j"]} → i={deg_truss(**p)}   {note}')
    for q, m, r, j, c, tree, note in FRAME_CASES:
        full = deg_frame(m, r, j, c) if m is not None else '—'
        print(f'{q:14s} 剛架 m={m} r={r} j={j} c={c} → 完整式 {full}、樹狀式 {deg_tree(r, c)}   {note}')
    print(f'SA-2024-2 需要 m = 2j − r = {M_NEED_2024_2}；實數 {M_COUNT_2024_2}')
    print('== 第 2 章 SA-2012-1')
    print('  反力', {k: round(v, 6) for k, v in R12.items()}, '(Vc=鉸對 c–e 的向上力；Ma 逆時針正)')
    print('  M(a,b,c,d,e) =', [round(M12(x + 1e-9), 3) for x in (0, 4, 8, 12)], round(M12(16), 3))
    print('  數值積分(1/EI)：yc=%.3f (題解 %.3f)  ye=%.3f (題解 %.3f)  θe=%.3f (題解 %d)' % (
        D12['yc'], float(ANS12['yc']), D12['ye'], float(ANS12['ye']), D12['the'], ANS12['the']))
    print('  c 鉸兩側斜率：左 %.3f 右 %.3f （1/EI）' % (D12['thc_left'], D12['thc_right']))
    print('== SA-2004-1', {k: round(v, 4) for k, v in R04.items()}, 'V=0 於 x=', X04_VZERO, 'Mmax=', M04_MAX)
    print('== SA-2002-2', {k: str(v) for k, v in R0202.items()}, ' 檢查 ΣFx=', R0202['Ax'] + 16 + R0202['Bx'])
    print('   只有垂直載重時 Ay0=',Ay0_v,' M_C^0=',MC0_v,' H=',H_v_0202)
    print('== SA-2002-1', {k: round(v, 4) for k, v in R0201.items()})
    print('   錯法（F 兩側力偶抵銷）', {k: round(v, 4) for k, v in R0201_bad.items()})


# ─────────────────────────────────────────────
# 第 3、4 章：桁架（通用節點法：每節點 ΣFx、ΣFy，全部聯立；拉力為正）
# ─────────────────────────────────────────────

def solve_truss(nodes, bars, supports, loads):
    """nodes: {名: (x,y)}；bars: ['AB', ...] 或 [('A','B'), ...]；
    supports: {名: [(ux,uy), ...]} 每個方向一個反力（正向＝該單位向量方向）；
    loads: {名: (fx, fy)}。回傳 (桿力 dict, 反力 dict)；桿力拉為正。
    同時檢查方程數 = 未知數（靜定）且每節點殘差為 0。"""
    bars = [tuple(b) for b in bars]
    names = list(nodes)
    unk = [('bar', b) for b in bars] + [('R', n, k) for n, ds in supports.items() for k in range(len(ds))]
    nrow, ncol = 2 * len(names), len(unk)
    assert nrow == ncol, f'非靜定：方程 {nrow}、未知 {ncol}'
    A = np.zeros((nrow, ncol)); b = np.zeros(nrow)
    row = {n: 2 * i for i, n in enumerate(names)}
    for j, u in enumerate(unk):
        if u[0] == 'bar':
            p, q = u[1]
            (x1, y1), (x2, y2) = nodes[p], nodes[q]
            Lb = math.hypot(x2 - x1, y2 - y1)
            ex, ey = (x2 - x1) / Lb, (y2 - y1) / Lb
            # 拉力：對 p 節點的作用力指向 q
            A[row[p], j] += ex; A[row[p] + 1, j] += ey
            A[row[q], j] -= ex; A[row[q] + 1, j] -= ey
        else:
            _, n, k = u
            ux, uy = supports[n][k]
            A[row[n], j] += ux; A[row[n] + 1, j] += uy
    for n, (fx, fy) in loads.items():
        b[row[n]] -= fx; b[row[n] + 1] -= fy
    x = np.linalg.solve(A, b)
    assert np.allclose(A @ x, b, atol=1e-9)
    F = {}; R = {}
    for j, u in enumerate(unk):
        v = 0.0 if abs(x[j]) < 1e-10 else float(x[j])
        if u[0] == 'bar':
            F[''.join(u[1])] = v
        else:
            R[(u[1], u[2])] = v
    return F, R


def blen(nodes, bar):
    (x1, y1), (x2, y2) = nodes[bar[0]], nodes[bar[1]]
    return math.hypot(x2 - x1, y2 - y1)


import math
S2 = math.sqrt(2)
HX, HY = (1, 0), (0, 1)

# SA-2017-1：A(0,0) B(0,4) C(0,8) D(3,4) E(6,0)；A、E 鉸支承；C 12 kN →、B 9 kN →（kN）
N17 = dict(A=(0, 0), B=(0, 4), C=(0, 8), D=(3, 4), E=(6, 0))
B17 = ['AB', 'BC', 'BD', 'AD', 'CD', 'DE']
F17, R17 = solve_truss(N17, B17, {'A': [HX, HY], 'E': [HX, HY]}, {'C': (12, 0), 'B': (9, 0)})
# 節點法順序（每一步的未知數）
ORDER17 = [('C', ['BC', 'CD']), ('E', ['DE', 'Ex']), ('D', ['AD', 'BD']), ('B', ['AB']), ('A', ['Ax（驗算）'])]

# SA-2010-1：G 原點；G 鉸、B 貼牆滾支承（水平反力）；H 30 kN ↓
N10 = dict(G=(0, 0), H=(4, 0), C=(0, 2), D=(2, 2), E=(4, 2), F=(6, 2), A=(2, 4), B=(6, 4))
B10 = ['AB', 'AC', 'AE', 'EB', 'BF', 'CD', 'DE', 'EF', 'CG', 'GD', 'DH', 'GH', 'HF']
F10, R10 = solve_truss(N10, B10, {'G': [HX, HY], 'B': [HX]}, {'H': (0, -30)})

# SA-2013-1：a 原點；a、i 鉸支承；c5 d10 e10 f10 g5 kN ↓；a–b 連續豎桿（l 高度無節點）
N13 = dict(a=(0, 0), l=(5, 10), b=(0, 20), k=(10, 20), c=(0, 30), d=(10, 30), e=(20, 30),
           f=(30, 30), j=(30, 20), g=(40, 30), h=(40, 20), i=(40, 10))
B13 = ['cd', 'de', 'ef', 'fg', 'cb', 'ba', 'ck', 'dk', 'bk', 'ke', 'bl', 'lk', 'al',
       'ej', 'fj', 'jg', 'jh', 'gh', 'hi', 'ji']
F13, R13 = solve_truss(N13, B13, {'a': [HX, HY], 'i': [HX, HY]},
                       {'c': (0, -5), 'd': (0, -10), 'e': (0, -10), 'f': (0, -10), 'g': (0, -5)})

# SA-2002-2（第 1、2 章已用幾何；這裡求全部桿力）
N0202 = dict(A=(0, 0), B=(32, 0), D=(0, 12), F=(8, 12), C=(16, 12), H=(24, 12), I=(32, 12), E=(8, 6), G=(24, 6))
B0202 = ['DA', 'IB', 'DF', 'FC', 'CH', 'HI', 'DE', 'FE', 'EC', 'AE', 'CG', 'HG', 'GI', 'GB']
F0202, R0202t = solve_truss(N0202, B0202, {'A': [HX, HY], 'B': [HX, HY]},
                            {'D': (16, -20), 'F': (0, -20), 'C': (0, -20), 'H': (0, -20), 'I': (0, -20)})
ABCDE_0202 = dict(a='DF', b='DE', c='AE', d='CH', e='CG')

# SA-2003-3：K 型細分桁架（t）；左鉸右滾；L1、L2 各 2 t ↓
N03 = dict(L0=(0, 0), L1=(8, 0), L2=(16, 0), L3=(24, 0), L4=(32, 0),
           M1=(4, 4), M2=(12, 4), M3=(20, 4), M4=(28, 4), U1=(8, 8), U2=(16, 8), U3=(24, 8))
B03 = [('L0', 'M1'), ('M1', 'U1'), ('U1', 'M2'), ('M2', 'L2'), ('M1', 'M2'), ('M1', 'L1'), ('L1', 'M2'),
       ('L4', 'M4'), ('M4', 'U3'), ('U3', 'M3'), ('M3', 'L2'), ('M3', 'M4'), ('M4', 'L3'), ('L3', 'M3'),
       ('U1', 'U2'), ('U2', 'U3'), ('U2', 'L2'), ('L0', 'L1'), ('L1', 'L2'), ('L2', 'L3'), ('L3', 'L4')]
F03, R03 = solve_truss(N03, B03, {'L0': [HX, HY], 'L4': [HY]}, {'L1': (0, -2), 'L2': (0, -2)})
A03, B03b = 'M1M2', 'U1M2'          # 桿 a、b


def bars_crossing(nodes, bars, x):
    """垂直切線 x 會切到哪些桿。"""
    out = []
    for b in bars:
        b = tuple(b)
        x1, x2 = nodes[b[0]][0], nodes[b[1]][0]
        if min(x1, x2) < x < max(x1, x2):
            out.append(''.join(b))
    return out


CUT03_BAD = bars_crossing(N03, B03, 6)       # 4 根
CUT03_OK = bars_crossing(N03, B03, 14)       # 3 根

# SA-2014-1：A 鉸、G 滾；P 在 C（以 P = 1）
N14 = dict(A=(0, 0), B=(12, 0), C=(24, 0), D=(36, 0), E=(48, 0), F=(60, 0), G=(72, 0),
           H=(12, 12), I=(24, 17), J=(36, 22), K=(48, 17), L=(60, 12))
B14 = ['AH', 'HI', 'IJ', 'JK', 'KL', 'LG', 'AB', 'BC', 'CD', 'DE', 'EF', 'FG',
       'BH', 'CI', 'DJ', 'EK', 'FL', 'HC', 'ID', 'KD', 'LE']
F14, R14 = solve_truss(N14, B14, {'A': [HX, HY], 'G': [HY]}, {'C': (0, -1)})
ID_EXACT_14 = -37 * math.sqrt(433) / 1122
# 截面法對 D 取矩：F_IJ 的力臂（點到直線距離）
ARM_IJ_D = abs(5 * 36 - 12 * 0 + 84) / 13            # 264/13
# 移動載重：P 分別在 B～F 時 CD 桿力
IL_CD_14 = {}
for nm in 'BCDEF':
    Fm, _ = solve_truss(N14, B14, {'A': [HX, HY], 'G': [HY]}, {nm: (0, -1)})
    IL_CD_14[nm] = Fm['CD']


def il_cd_formula(x):
    """CD 桿力影響線（P=1 在下弦 x 處）：右側用左自由體、左側用右自由體。"""
    return (72 - x) / 51 if x >= 24 else 2 * x / 51


# 桁架＝挖空的梁：P=1 在 C 時，下弦桿力 = 簡支梁 M(取矩點 x) / 取矩點高度
def M_beam14(x, xp=24.0, Lsp=72.0):
    Ra = (Lsp - xp) / Lsp
    return Ra * x - (x - xp if x > xp else 0)


CHORD14 = [('BC', 'H'), ('CD', 'I'), ('DE', 'K'), ('EF', 'L')]   # 下弦桿與其取矩點（被切另兩桿交點）

# SA-2016-4：判讀格線座標（考卷無尺寸）；以直接勁度法、隨機 EA 與 k 驗證「只有 AE 受力」
N164 = {"D": (0, 2), "E": (1, 2), "F": (2, 2), "G": (3, 2), "H": (4, 2),
        "A": (1, 3), "B": (2, 3), "C": (3, 3), "I": (2, 1), "J": (3, 1), "K": (2, 0), "L": (3, 0),
        "P": (5, 0), "M": (4, 1.3), "N": (5, 1.3), "O": (6, 1.3)}
B164 = ['AB', 'BC', 'AD', 'AE', 'AF', 'BF', 'CF', 'CG', 'CH', 'DE', 'EF', 'FG', 'GH',
        'FI', 'GJ', 'IJ', 'FJ', 'GI', 'IK', 'JL', 'KL', 'IL', 'JK', 'LP', 'NP']
RULE_ZERO_164 = ['LP', 'NP', 'BF']


def stiffness_check_164(seed):
    rng = np.random.default_rng(seed)
    free = [n for n in N164 if n not in ('A', 'C', 'D', 'M', 'O')]
    idx = {}
    for n in free:
        idx[(n, 0)] = len(idx); idx[(n, 1)] = len(idx)
    K = np.zeros((len(idx), len(idx))); f = np.zeros(len(idx))
    def add_bar(p, q, k):
        (x1, y1), (x2, y2) = N164[p], N164[q]
        Lb = math.hypot(x2 - x1, y2 - y1); c, s = (x2 - x1) / Lb, (y2 - y1) / Lb
        kk = k / Lb * np.outer([c, s, -c, -s], [c, s, -c, -s])
        dofs = [(p, 0), (p, 1), (q, 0), (q, 1)]
        for a, da in enumerate(dofs):
            for bb, db in enumerate(dofs):
                if da in idx and db in idx:
                    K[idx[da], idx[db]] += kk[a, bb]
        return (c, s, Lb, k)
    EA = {b: rng.uniform(0.5, 3.0) for b in B164}
    info = {b: add_bar(b[0], b[1], EA[b]) for b in B164}
    ks = rng.uniform(0.2, 5.0)
    info['HM'] = add_bar('H', 'M', ks * math.hypot(N164['M'][0] - 4, N164['M'][1] - 2))  # 彈簧 k（k/L·L）
    # 梁 MNO：N 點以垂直彈簧（梁的撓曲勁度）＋水平束制（M 鉸）模擬
    kb = rng.uniform(0.5, 5.0)
    K[idx[('N', 1)], idx[('N', 1)]] += kb
    K[idx[('N', 0)], idx[('N', 0)]] += 1e3
    for n, (fx, fy) in {'E': (0, -100), 'N': (0, -100)}.items():
        if (n, 0) in idx:
            f[idx[(n, 0)]] += fx; f[idx[(n, 1)]] += fy
    u = np.linalg.solve(K, f)
    def disp(n):
        return (u[idx[(n, 0)]], u[idx[(n, 1)]]) if (n, 0) in idx else (0.0, 0.0)
    out = {}
    for b, (c, s, Lb, k) in info.items():
        p, q = b[0], b[1]
        (u1, v1), (u2, v2) = disp(p), disp(q)
        out[b] = k / Lb * ((u2 - u1) * c + (v2 - v1) * s)
    return out


CHK164 = [stiffness_check_164(s) for s in range(5)]
for _r in CHK164:
    assert abs(_r['AE'] - 100) < 1e-6, _r['AE']
    assert all(abs(v) < 1e-6 for kk, v in _r.items() if kk != 'AE'), _r
M164_PART = 23; J164_PART = 12   # 只看 A～L 部分：桿 23、節點 12、A/C/D 鉸 r=6


def show_truss():
    def p(tag, F, R):
        print(tag)
        print('   桿力', {k: round(v, 4) for k, v in F.items()})
        print('   反力', {f'{k[0]}{k[1]}': round(v, 4) for k, v in R.items()})
    print('== 第 3 章')
    p('SA-2017-1', F17, R17)
    p('SA-2010-1', F10, R10)
    print('   AC/√2 =', round(F10['AC'] / S2, 4), ' EB/√2 =', round(F10['EB'] / S2, 4), ' HF/√2=', round(F10['HF'] / S2, 4))
    p('SA-2013-1', F13, R13)
    print('   ke/√2=', round(F13['ke'] / S2, 4), ' kc/√2=', round(F13['ck'] / S2, 4), ' lk/√5=', round(F13['lk'] / math.sqrt(5), 4))
    print('SA-2016-4 直接勁度法 5 組隨機 EA/k：AE =', [round(r['AE'], 6) for r in CHK164], '其餘最大 |F| =',
          max(abs(v) for r in CHK164 for kk, v in r.items() if kk != 'AE'))
    print('   A～L 部分 m + r − 2j =', M164_PART, '+ 6 −', 2 * J164_PART, '=', M164_PART + 6 - 2 * J164_PART)
    print('== 第 4 章')
    p('SA-2002-2', F0202, R0202t)
    print('   a～e =', {k: str(Fr(F0202[v]).limit_denominator(100)) for k, v in ABCDE_0202.items()})
    p('SA-2003-3', F03, R03)
    print('   a =', round(F03[A03], 4), ' b/√2 =', round(F03[B03b] / S2, 4), ' 切 x=6:', CUT03_BAD, ' 切 x=14:', CUT03_OK)
    p('SA-2014-1 (P=1 在 C)', F14, R14)
    print('   CD =', Fr(F14['CD']).limit_denominator(1000), ' IJ =', Fr(F14['IJ']).limit_denominator(1000),
          ' ID =', round(F14['ID'], 6), '（精確 −37√433/1122 =', round(ID_EXACT_14, 6), '）  IJ 對 D 力臂 =', ARM_IJ_D, '= 264/13')
    print('   移動載重 CD：', {k: str(Fr(v).limit_denominator(100)) for k, v in IL_CD_14.items()},
          ' 公式', {k: str(Fr(il_cd_formula(x)).limit_denominator(100)) for k, x in zip('BCDEF', (12, 24, 36, 48, 60))})
    for bar, c in CHORD14:
        x, h = N14[c]
        print(f'   下弦 {bar}：節點法 {F14[bar]:.4f}  M({x})/h({h}) = {M_beam14(x) / h:.4f}')


# ─────────────────────────────────────────────
# 第 5～9 章：內力圖、彎曲、共軛梁、虛功、非外力成因
# ─────────────────────────────────────────────

def integ(fn, a, b, n=20000):
    """梯形法數值積分（分段函數用，跨不連續點請分段呼叫）。"""
    e = (b - a) * 1e-10
    xs = np.linspace(a + e, b - e, n + 1)
    ys = np.array([fn(x) for x in xs])
    return float(np.trapezoid(ys, xs)) if hasattr(np, 'trapezoid') else float(np.trapz(ys, xs))


# ---------- 第 5 章 ----------
def V12(x):
    """SA-2012-1 剪力（左面向上為正），x 由 a 起算。"""
    V = R12['Ra']
    for xp, Fv in ((4, -P12), (8, 0.0), (12, R12['Rd'])):
        if x > xp:
            V += Fv
    return V


# SA-2004-1 梁 B(0)–C(4)–D(6)：w = 2 t/m，B 端鉸力 3 t 向上，C 滾支承 9 t
def M04(x):
    return 3 * x - x * x if x <= 4 else -(6 - x) ** 2


def V04(x):
    return 3 - 2 * x if x < 4 else 2 * (6 - x)


X04_INFL = 3.0          # M04 = 0 的位置（反曲點）
M04_C = M04(4)          # −4

# SA-2002-1 梁 C(0)–F(6)：F 鉸力對梁向上 29/3、梁端力偶 4（逆時針）、E(3) 8 kN↓、C–D(0~2) 分布力偶 2 kN-m/m 順時針
FY0201 = -R0201['Fy']    # 鉸對右柱向下 → 對梁向上 29/3


def M0201(x):
    m = FY0201 * (6 - x) + 4.0
    if x < 3:
        m -= 8 * (3 - x)
    if x < 2:
        m -= 2 * (2 - x)
    return m


def V0201(x):
    """梁剪力（左面向上為正）＝ −（右段向上力合計）。"""
    up = FY0201 - (8 if x < 3 else 0)
    return -up


# ---------- 第 6、7 章：SA-2012-1 面積法／共軛梁 ----------
A12 = dict(F1=320.0, x1=2.0, F2=160.0, x2=16 / 3, F3=-320.0, x3=32 / 3, F4=-320.0, x4=40 / 3)   # M/EI 合力（以 1/EI），向上為正
TH_C_LEFT = (A12['F1'] + A12['F2'])                                   # a 到 c 左側的轉角（a 端水平）
Y_C_AREA = A12['F1'] * (8 - 2) + A12['F2'] * (8 - 16 / 3)              # 面積矩法 = 7040/3
# 共軛梁：a' 自由、c' 內支承、d' 內鉸、e' 固定
Rc_conj = -(A12['F1'] * 10 + A12['F2'] * (12 - 16 / 3) + A12['F3'] * (12 - 32 / 3)) / 4      # −960
Vd_up_on_left = -(A12['F1'] + A12['F2'] + A12['F3'] + Rc_conj)                           # 800（右段給左段向上）
# 右段 d'–e'：d' 受左段給的力 = 800 向下；F4 = 320 向下在 40/3
TH_E_CONJ = -Vd_up_on_left + A12['F4']          # e' 剪力（向上為正）＝ −800 − 320 = −1120 → 順時針 1120
Y_E_CONJ = -Vd_up_on_left * 4 + A12['F4'] * (16 - 40 / 3)     # −3200 − 853.3 = −12160/3


# 標準撓度（以數值積分驗算：懸臂、簡支）
def std_check():
    L_, P_, w_, EI_ = 3.0, 2.0, 1.5, 7.0
    # 懸臂 P：δ = ∫ m M/EI，m = −(L−x)、M = −P(L−x)
    d1 = integ(lambda x: (L_ - x) * P_ * (L_ - x) / EI_, 0, L_)
    t1 = integ(lambda x: P_ * (L_ - x) / EI_, 0, L_)
    d2 = integ(lambda x: (L_ - x) * w_ * (L_ - x) ** 2 / 2 / EI_, 0, L_)
    # 簡支 P 中點、w 中點、w 端轉角
    mm = lambda x: x / 2 if x <= L_ / 2 else (L_ - x) / 2
    d3 = integ(lambda x: mm(x) * P_ * mm(x) / EI_, 0, L_)
    Mw = lambda x: w_ * x * (L_ - x) / 2
    d4 = integ(lambda x: mm(x) * Mw(x) / EI_, 0, L_)
    t4 = integ(lambda x: (1 - x / L_) * Mw(x) / EI_, 0, L_)
    return dict(c3=d1 / (P_ * L_ ** 3 / EI_), c2=t1 / (P_ * L_ ** 2 / EI_), c8=d2 / (w_ * L_ ** 4 / EI_),
                s48=d3 / (P_ * L_ ** 3 / EI_), s384=d4 / (w_ * L_ ** 4 / EI_), s24=t4 / (w_ * L_ ** 3 / EI_))


STD = std_check()


def area_n(n, b=1.0, h=1.0):
    """y = h (x/b)^n 下的面積與形心距 x=b 端的距離。"""
    A = integ(lambda x: h * (x / b) ** n, 0, b)
    xb = integ(lambda x: x * h * (x / b) ** n, 0, b) / A
    return A / (b * h), (b - xb) / b


AREA_N = {n: area_n(n) for n in (1, 2, 3)}

# ---------- 第 7 章：SA-2022-1（EI = 250000、k = 6000，單位 kN、m） ----------
EI22, K22 = 250000.0, 6000.0
Rb22 = 480 / 5                       # 96
Vb22 = Rb22 - 72                     # 24（左梁在 b 被向上撐 24）
Fs22 = (72 * 5 - 24 * 10) / 5        # 24（彈簧受壓）
Rd22 = 72 - Fs22 - 24                # 24
Mc22 = Rd22 * 5                      # 120
Db22 = Rb22 * 5 ** 3 / (3 * EI22)    # 0.016
Dc22_rigid = Db22 / 2                # 0.008
Vst22 = 0.5 * 10 * Mc22 / 2           # 共軛簡支梁端反力 300/EI
Mcst22 = Vst22 * 5 - (0.5 * 5 * Mc22) * 5 / 3      # 1000/EI
Dc22_el = Mcst22 / EI22                            # 0.004
Dc22 = Dc22_rigid + Dc22_el          # 0.012
ds22 = Fs22 / K22                    # 0.004
De22 = Dc22 - ds22                   # 0.008

# ---------- 第 7 章：SA-2024-1（EI 常數；A 滾、C 內鉸、D 固定；A 端 200 逆時針、B 100↓） ----------
RA24 = (200 + 100 * 4) / 8           # 75
VC24 = 100 - RA24                    # 25（C 鉸對 AC 向上；CD 懸臂端受 25↓）


def M24(x):
    if x <= 4:
        return RA24 * x - 200
    if x <= 8:
        return RA24 * x - 200 - 100 * (x - 4)
    return -VC24 * (x - 8)


def deflect24(n=24000):
    """數值積分：D(12) 固定 y=θ=0，往左積分到 C；AC 段：y(C) 已知、y(A)=0 → 找 θ(C+)。向上為正。"""
    xs = np.linspace(0, 12, n + 1)
    dx = xs[1] - xs[0]
    k = np.array([M24(x) for x in xs])        # 以 1/EI
    y = np.zeros_like(xs); th = np.zeros_like(xs)
    ic = int(round(8 / dx))
    for i in range(n - 1, ic - 1, -1):         # 由 D 往左
        th[i] = th[i + 1] - 0.5 * (k[i] + k[i + 1]) * dx
        y[i] = y[i + 1] - 0.5 * (th[i] + th[i + 1]) * dx
    yc = y[ic]

    def run(t0):
        th2 = np.zeros(ic + 1); y2 = np.zeros(ic + 1)
        th2[ic] = t0; y2[ic] = yc
        for i in range(ic - 1, -1, -1):
            th2[i] = th2[i + 1] - 0.5 * (k[i] + k[i + 1]) * dx
            y2[i] = y2[i + 1] - 0.5 * (th2[i] + th2[i + 1]) * dx
        return th2, y2
    _, ya = run(0.0); _, yb = run(1.0)
    t0 = -ya[0] / (yb[0] - ya[0])
    th2, y2 = run(t0)
    y[:ic + 1] = y2; th[:ic + 1] = th2
    return xs, y, th, yc


XS24, Y24, TH24, YC24 = deflect24()
IMIN24 = int(np.argmin(Y24[:int(len(XS24) * 8 / 12)]))
X24_MAX, Y24_MAX = float(XS24[IMIN24]), float(Y24[IMIN24])        # ≈ 5.691、−635.98
Y24_UP = float(Y24[:int(len(XS24) * 4 / 12)].max())                # AB 段最大向上
X24_EXACT = 8 - 4 / math.sqrt(3)
Y24_EXACT = 1600 / 3 + 1600 / (9 * math.sqrt(3))
EIMIN24 = Y24_EXACT / 0.04

# ---------- 第 8 章：單位力法 ----------
# SA-2017-1：C 點 1 kN →
F17u, R17u = solve_truss(N17, B17, {'A': [HX, HY], 'E': [HX, HY]}, {'C': (1, 0)})
ROWS17 = [(b, F17[b], F17u[b], blen(N17, b), F17[b] * F17u[b] * blen(N17, b)) for b in B17]
DC17 = sum(r[4] for r in ROWS17)                                   # 566.5（/EA）

# SA-2012-1：單位力法（數值積分）求 y_e、θ_e（向下、順時針為正）
def m12_ye(x):        # e 點向下單位力的虛彎矩（同 M12 的符號規則）
    # c–e：d 為支點；左段 a–c 受鉸力。e 1↓ → Rd = 2↑、鉸對 c–e 1↓ → 對 a–c 1↑
    if x >= 8:
        return -1 * (16 - x) + (2 * (12 - x) if x < 12 else 0)
    return 1 * (8 - x)                     # a–c：c 端 1↑ 的懸臂


def m12_te(x):        # e 點順時針單位力偶
    # c–e 對 d 取矩：鉸力 Vc·4 = 1 → 對 c–e 向下 1/4？以靜力：Σ M_d：Vc(−4)... 用數值平衡
    if x >= 12:
        return -1.0
    if x >= 8:
        return -(x - 8) / 4
    return 0.25 * (8 - x)


YE12_UL = integ(lambda x: M12(x) * m12_ye(x) / EI12(x), 0, 8) + integ(lambda x: M12(x) * m12_ye(x) / EI12(x), 8, 16)
TE12_UL = integ(lambda x: M12(x) * m12_te(x) / EI12(x), 0, 8) + integ(lambda x: M12(x) * m12_te(x) / EI12(x), 8, 16)

# SA-2003-2：剛梁＋三連桿（λ = 1、F = 1、EA = 1）
N03_2 = dict(AD=1.0, AE=0.0, BE=-2.0)          # 拉為正
L03_2 = dict(AD=3.0, AE=5.0, BE=3.0)
DC03_2 = sum(N03_2[b] * N03_2[b] * L03_2[b] for b in N03_2)     # n = N/F → 15

# SA-2004-3：A 固定、AB 30 m（2EI）、B 內鉸、BC 18 m、C 彈簧、CD 12 m（EI）；B、D 各 36 t↓；EI = 1e6、k = 1e4
EI43, K43 = 1e6, 1e4
RC43 = 36 * 30 / 18                     # 60（彈簧受壓）
PB43 = 36 + 36 - RC43                   # 12：AB 懸臂端淨受力（向下）
DB43 = PB43 * 30 ** 3 / (3 * 2 * EI43)  # 0.054
DC43 = RC43 / K43                       # 0.006


def M43(s):           # s 由 A 起算 0~60；彎矩（下緣受拉為正）
    if s <= 30:
        return -PB43 * (30 - s)
    x = s - 30
    if x <= 18:
        return -24 * x
    return -36 * (30 - x)


def m43_D(s):         # D 點 1↓：彈簧 5/3↑、B 鉸對 BCD 2/3↓（對 AB 2/3↑）
    if s <= 30:
        return (2 / 3) * (30 - s)
    x = s - 30
    if x <= 18:
        return -(2 / 3) * x
    return -(30 - x)


EI43f = lambda s: 2 * EI43 if s <= 30 else EI43
DD43_AB = integ(lambda s: M43(s) * m43_D(s) / EI43f(s), 0, 30)
DD43_BD = integ(lambda s: M43(s) * m43_D(s) / EI43f(s), 30, 48) + integ(lambda s: M43(s) * m43_D(s) / EI43f(s), 48, 60)
DD43_SP = (5 / 3) * RC43 / K43          # 彈簧項：虛彈簧力 × 實彈簧力 / k（同為受壓）
DD43 = DD43_AB + DD43_BD + DD43_SP      # 0.02584

# ---------- 第 9 章 ----------
ALPHA = 1.5e-5


def compat_disp(nodes, bars, fixed, elong, settle=None):
    """幾何相容：已知各桿伸長量與支承位移，解節點位移（靜定桁架唯一解）。
    fixed: {節點: [(ux,uy) 被束制的方向]}；settle: {(節點, k): 該束制方向的位移}。"""
    names = list(nodes); idx = {n: i for i, n in enumerate(names)}
    rows, rhs = [], []
    for b in bars:
        p, q = b[0], b[1]
        (x1, y1), (x2, y2) = nodes[p], nodes[q]
        Lb = math.hypot(x2 - x1, y2 - y1); ex, ey = (x2 - x1) / Lb, (y2 - y1) / Lb
        r = np.zeros(2 * len(names))
        r[2 * idx[q]] += ex; r[2 * idx[q] + 1] += ey; r[2 * idx[p]] -= ex; r[2 * idx[p] + 1] -= ey
        rows.append(r); rhs.append(elong.get(b, 0.0))
    for n, ds in fixed.items():
        for k, (ux, uy) in enumerate(ds):
            r = np.zeros(2 * len(names)); r[2 * idx[n]] = ux; r[2 * idx[n] + 1] = uy
            rows.append(r); rhs.append((settle or {}).get((n, k), 0.0))
    A = np.array(rows); bvec = np.array(rhs)
    u = np.linalg.solve(A, bvec)
    return {n: (u[2 * idx[n]], u[2 * idx[n] + 1]) for n in names}


# SA-2024-2：B 滾、F 鉸；下弦 A..G (0..24, 0)，上弦 H..N (0..24, 3)
N242 = {**{c: (4 * i, 0) for i, c in enumerate('ABCDEFG')}, **{c: (4 * i, 3) for i, c in enumerate('HIJKLMN')}}
B242 = ['AB', 'BC', 'CD', 'DE', 'EF', 'FG', 'HI', 'IJ', 'JK', 'KL', 'LM', 'MN',
        'HA', 'IB', 'JC', 'KD', 'LE', 'MF', 'NG', 'HB', 'BJ', 'JD', 'DL', 'LF', 'FN']
SUP242 = {'B': [HY], 'F': [HX, HY]}
U242C, R242C = solve_truss(N242, B242, SUP242, {'C': (0, -1)})
U242E, R242E = solve_truss(N242, B242, SUP242, {'E': (0, -1)})
vF242 = 12.0                                         # mm 向下
# 1·Δ + R̄·δ_support = Σ n ΔL ；R̄ 向上為正、支承位移向下 → δ = −12
rhsC = 4.8 + R242C[('F', 1)] * (-vF242)
rhsE = 6.4 + R242E[('F', 1)] * (-vF242)
A2 = np.array([[U242C['CD'], U242C['DE']], [U242E['CD'], U242E['DE']]])
dCD242, dDE242 = np.linalg.solve(A2, np.array([rhsC, rhsE]))
dT242 = dDE242 / (ALPHA * 4000)                      # ℃
# 反向檢查：用幾何相容直接算 C、E 位移
_u = compat_disp(N242, [tuple(b) for b in B242], {'B': [(0, 1)], 'F': [(1, 0), (0, 1)]},
                 {('C', 'D'): dCD242, ('D', 'E'): dDE242}, {('F', 1): -vF242})
CHK242 = (-_u['C'][1], -_u['E'][1])                  # 向下為正 → 應為 4.8、6.4
# 給了 E、A 的誘餌：EA = 100e3 MPa × 150 mm² = 15000 kN；內力全 0 → ΣnNL/EA = 0
EA242 = 100e3 * 150 / 1000                            # kN

# SA-2015-1：A(0,0) 鉸、C(4,0) 滾、D(8,0)、B(4,3)；D 50↓、B 水平力 T（向左）；BD 縮短 0.5 cm；C 下陷 0.4 cm；EA = 2e5
N15 = dict(A=(0, 0), C=(4, 0), D=(8, 0), B=(4, 3))
B15 = ['AB', 'BC', 'BD', 'AC', 'CD']
SUP15 = {'A': [HX, HY], 'C': [HY]}
F15_P, R15_P = solve_truss(N15, B15, SUP15, {'D': (0, -50)})
F15_T, R15_T = solve_truss(N15, B15, SUP15, {'B': (-1, 0)})   # 單位 T（向左）
U15, R15u = solve_truss(N15, B15, SUP15, {'D': (0, -1)})
EA15 = 2e5
c0 = sum(U15[b] * F15_P[b] * blen(N15, b) for b in B15) / EA15
c1 = sum(U15[b] * F15_T[b] * blen(N15, b) for b in B15) / EA15
err15 = U15['BD'] * (-0.005)
sup15 = R15u[('C', 0)] * (-0.004)
# 0 + sup15 = c0 + c1·T + err15
T15 = (sup15 - c0 - err15) / c1
# 反向檢查：相容法（各桿伸長 = NL/EA + 誤差）
_F = {b: F15_P[b] + T15 * F15_T[b] for b in B15}
_e = {(b[0], b[1]): _F[b] * blen(N15, b) / EA15 + (-0.005 if b == 'BD' else 0) for b in B15}
_u15 = compat_disp(N15, [tuple(b) for b in B15], {'A': [(1, 0), (0, 1)], 'C': [(0, 1)]}, _e, {('C', 0): -0.004})
CHK15 = _u15['D'][1]                                   # 應為 0

# SA-2023-1：梁 A(0)–B(2)–C(6)–D(10)–E(12)，B 滾、D 鉸；柱 CF 高 4，F 受 P→；D 下陷 3 mm；EI = 20000
EI23 = 20000.0
ROT23 = 0.003 / 8                                      # 剛體轉角
DE23_RIGID = ROT23 * 10                                # E 向下 0.00375
# P 的彈性：C 點順時針力偶 4P；E 單位向下的虛彎矩 m = −0.25(x−2)（x 由 A 起，B..D 段）、D..E 段 −(12−x)
def M23(x):            # 每單位 P；B(2)…D(10)；C(6) 處順時針 4 → 彎矩跳 +4（下緣受拉為正）
    if x < 2 or x > 10:
        return 0.0
    return -0.5 * (x - 2) + (4 if x > 6 else 0)


def m23(x):
    if 2 <= x <= 10:
        return -0.25 * (x - 2)
    if x > 10:
        return -(12 - x)
    return 0.0


DE23_P = (integ(lambda x: M23(x) * m23(x), 2, 6) + integ(lambda x: M23(x) * m23(x), 6, 10)) / EI23   # 每單位 P，向下為正
P23 = DE23_RIGID / (-DE23_P)                          # 28.125


def show_late():
    print('== 第 5 章')
    print('  2012-1 V(a..e)=', [V12(x) for x in (1, 5, 9, 13)], ' M(b,c,d)=', [M12(x + 1e-9) for x in (4, 8, 12)])
    print('  2004-1 梁 M(1.5)=', M04(1.5), ' M(C)=', M04_C, ' 反曲點 x=', X04_INFL, ' V(4−,4+)=', V04(3.999), V04(4.001))
    print('  2002-1 梁 M(C,D,E,F−)=', [round(M0201(x), 3) for x in (0, 2, 3, 6)], ' V(1,2.5,4)=', [round(V0201(x), 3) for x in (1, 2.5, 4)],
          ' dM/dx 於 C–D =', round((M0201(1.01) - M0201(0.99)) / 0.02, 4))
    print('== 第 6、7 章 SA-2012-1')
    print('  θc左 =', TH_C_LEFT, ' yc(面積矩) =', Y_C_AREA, '= 7040/3', ' 數值積分 yc =', round(D12['yc'], 2))
    print('  共軛梁 Rc\' =', Rc_conj, ' 左段給右段 =', Vd_up_on_left, ' θe =', TH_E_CONJ, ' ye =', round(Y_E_CONJ, 3), '（−12160/3 =', round(-12160 / 3, 3), '）')
    print('  標準撓度係數（應為 1/3,1/2,1/8,1/48,5/384,1/24）:', {k: round(v, 5) for k, v in STD.items()},
          [round(x, 5) for x in (1 / 3, 1 / 2, 1 / 8, 1 / 48, 5 / 384, 1 / 24)])
    print('  n 次曲線面積/形心:', {n: (round(a, 4), round(c, 4)) for n, (a, c) in AREA_N.items()})
    print('== SA-2022-1  Rb', Rb22, 'Fs', Fs22, 'Rd', Rd22, 'Mc', Mc22, 'Δb', Db22, 'Δc剛', Dc22_rigid, 'Δc彈', Dc22_el, 'Δc', Dc22, 'δs', ds22, 'Δe', De22)
    print('== SA-2024-1  RA', RA24, 'VC', VC24, 'yC(數值)', round(YC24, 3), '(−1600/3 =', round(-1600 / 3, 3), ')',
          ' 最大向下 x=', round(X24_MAX, 3), 'y=', round(Y24_MAX, 3), ' 精確', round(X24_EXACT, 3), round(Y24_EXACT, 3), ' AB 最大向上', round(Y24_UP, 2), ' EImin', round(EIMIN24, 1))
    print('== 第 8 章 SA-2017-1')
    for r in ROWS17:
        print('   ', r[0], 'N', round(r[1], 3), 'n', round(r[2], 4), 'L', r[3], 'nNL', round(r[4], 3))
    print('   δC =', round(DC17, 3), '/EA')
    print('  2012-1 單位力法 ye =', round(YE12_UL, 3), ' θe =', round(TE12_UL, 3))
    print('  2003-2 ΔC =', DC03_2, 'Fλ/EA')
    print('  2004-3 ΔB', DB43, 'ΔC', DC43, ' ΔD 三項: AB', round(DD43_AB, 5), 'BCD', round(DD43_BD, 5), '彈簧', round(DD43_SP, 5), '合計', round(DD43, 5))
    print('== 第 9 章')
    print('  2024-2 n(CD,DE) for C:', round(U242C['CD'], 4), round(U242C['DE'], 4), ' for E:', round(U242E['CD'], 4), round(U242E['DE'], 4),
          ' R̄F:', round(R242C[('F', 1)], 4), round(R242E[('F', 1)], 4))
    print('     δCD =', round(dCD242, 4), 'mm  ΔL_DE =', round(dDE242, 4), 'mm  ΔT =', round(dT242, 2), '℃  反向檢查 C,E =', [round(v, 4) for v in CHK242], ' EA =', EA242)
    print('  2015-1 R̄C =', R15u[('C', 0)], ' c0 =', c0, ' c1 =', c1, ' 誤差項', err15, ' 支承項', sup15, ' T =', round(T15, 3), '(31600/179 =', round(31600 / 179, 3), ')  反向 D 位移 =', CHK15)
    print('     n:', {b: round(U15[b], 4) for b in B15})
    print('  2023-1 剛體 ΔE =', DE23_RIGID, ' 每單位 P 的 ΔE =', round(DE23_P, 9), '(−8/3EI =', -8 / 3 / EI23, ')  P =', round(P23, 4))


if __name__ == '__main__':
    show()
    show_truss()
    show_late()
