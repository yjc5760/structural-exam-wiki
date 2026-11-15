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


if __name__ == '__main__':
    show()
