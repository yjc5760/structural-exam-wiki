# -*- coding: utf-8 -*-
"""教科書講義 SA-U1-3（靜定及靜不定結構影響線）的所有數值。
圖檔 import 本檔；內文的數字抄自 `python3 calcs.py` 的輸出。

符號慣例（全書一致）：
  ・單位載重 1 向下，位置 x（m）從左端量起
  ・反力向上為正；剪力 V＝斷面左側所有向上力的和（左上右下為正）
  ・彎矩 M 使梁下側受拉（正彎矩）為正；固定端彎矩 M_A 依題解慣例「上側受拉為正」
  ・影響線正值畫在軸上方
"""
import numpy as np

# ─────────────────────────────────────────────
# 通用：靜定梁影響線求解器（平衡方程，不用 Müller-Breslau，拿來交叉驗算）
# ─────────────────────────────────────────────


class Beam:
    """一根直梁：supports = [(名稱, x, 種類)]，種類 'roller'／'pin'／'fixed'；hinges = [x, ...]。
    未知量：每個支承的垂直反力；固定端另加一個反力矩（逆時針為正）。
    方程：ΣFy＝0、對 x＝0 取矩、每個內鉸「鉸右側所有力對鉸取矩＝0」。"""

    def __init__(self, supports, hinges=(), length=None):
        self.sup = supports
        self.hinges = list(hinges)
        self.Lt = length if length is not None else max(s[1] for s in supports)
        self.unk = []
        for n, x, k in supports:
            self.unk.append(('R', n, x))
            if k == 'fixed':
                self.unk.append(('M', n, x))
        assert len(self.unk) == 2 + len(self.hinges), '不是靜定梁'

    def solve(self, xP, P=1.0):
        n = len(self.unk)
        A = np.zeros((n, n)); b = np.zeros(n)
        # ΣFy = 0 ：ΣR − P = 0
        for j, (t, _, x) in enumerate(self.unk):
            if t == 'R':
                A[0, j] = 1
        b[0] = P
        # ΣM（對 x=0，逆時針為正）：R·x + Mcouple − P·xP = 0
        for j, (t, _, x) in enumerate(self.unk):
            A[1, j] = x if t == 'R' else 1
        b[1] = P * xP
        # 內鉸：右側自由體對鉸取矩＝0
        for i, h in enumerate(self.hinges):
            r = 2 + i
            for j, (t, _, x) in enumerate(self.unk):
                if x > h:
                    A[r, j] = (x - h) if t == 'R' else 1
            b[r] = P * (xP - h) if xP > h else 0.0
        sol = np.linalg.solve(A, b)
        return {(t, nm): v for (t, nm, _), v in zip(self.unk, sol)}

    def R(self, name, xP):
        return self.solve(xP)[('R', name)]

    def Mfix(self, name, xP):
        """固定端反力矩（逆時針為正）＝左端固定時『上側受拉』為正的彎矩。"""
        return self.solve(xP)[('M', name)]

    def V(self, s, xP, side=+1):
        """斷面 s 的剪力（左側向上力之和）。載重恰在 s 時 side=+1 取右側極限（載重算在左邊）。"""
        sol = self.solve(xP)
        v = sum(val for (t, nm), val in sol.items() if t == 'R' and self._x(nm) < s)
        if xP < s or (xP == s and side > 0):
            v -= 1.0
        return v

    def M(self, s, xP):
        """斷面 s 的彎矩（正彎矩＝下側受拉），由左側自由體求。"""
        sol = self.solve(xP)
        m = 0.0
        for (t, nm), val in sol.items():
            x = self._x(nm)
            if x < s or (x == s and t == 'R' and s == 0):
                m += val * (s - x) if t == 'R' else -val   # 逆時針反力矩對斷面造成負彎矩
        if xP < s:
            m -= 1.0 * (s - xP)
        return m

    def _x(self, name):
        for n, x, k in self.sup:
            if n == name:
                return x


# ─────────────────────────────────────────────
# 第 1 章：貫穿全書的 10 m 簡支梁（斷面 C 距 A 6 m）
# ─────────────────────────────────────────────
L = 10.0
a, b = 6.0, 4.0          # 斷面 C 的位置
SS = Beam([('A', 0.0, 'pin'), ('B', L, 'roller')])


def RA_ss(x):  # 由 ΣM_B＝0
    return (L - x) / L


def RB_ss(x):
    return x / L


def VC_ss(x):
    return -x / L if x < a else 1 - x / L


def MC_ss(x):
    return x * b / L if x <= a else (L - x) * a / L


MC_PEAK = a * b / L                 # 2.4 m
VC_LEFT, VC_RIGHT = -a / L, 1 - a / L   # −0.6、+0.4
# 例 1-1：50 kN 停在 x = 3 m
P1, X1 = 50.0, 3.0
EX1 = dict(RA=P1 * RA_ss(X1), RB=P1 * RB_ss(X1), VC=P1 * VC_ss(X1), MC=P1 * MC_ss(X1),
           etaRA=RA_ss(X1), etaVC=VC_ss(X1), etaMC=MC_ss(X1))
# 對照：同一個 50 kN 若停在 C 正上方
EX1_atC = dict(MC=P1 * MC_PEAK)
# 彎矩圖（載重固定在 x=3）的 C 點值，與影響線讀值相同（互易的伏筆）
BMD_at_C = RB_ss(X1) * (L - a)   # 載重固定在 x=3 時，彎矩圖在斷面 s=6 的值（右側自由體 R_B·4）＝1.2

# 第 2 章：同一根梁加 3 m 懸臂段（A 鉸、B 滾、自由端 D 在 13 m）
LD = 13.0
OH = Beam([('A', 0.0, 'pin'), ('B', L, 'roller')], length=LD)
OH_RA_D = OH.R('A', LD)            # −0.3
OH_RB_D = OH.R('B', LD)            # 1.3
OH_MC_D = OH.M(a, LD)              # −1.8
OH_VC_D = OH.V(a, LD)              # −0.3

# Müller-Breslau 的幾何：彎矩 → 鉸兩側相對轉角 1
thA = b / L                        # 左段轉角 0.4 rad
thB = a / L                        # 右段轉角 0.6 rad
# ─────────────────────────────────────────────
# 第 2 章範例：SA-2025-2 Gerber 梁（A 固定、C／E 滾、B／D 內鉸，4@4 m，F 在 6 m）
# ─────────────────────────────────────────────
G = Beam([('A', 0.0, 'fixed'), ('C', 8.0, 'roller'), ('E', 16.0, 'roller')], hinges=[4.0, 12.0])
G_PTS = [('A', 0.0), ('B', 4.0), ('F', 6.0), ('C', 8.0), ('D', 12.0), ('E', 16.0)]
XF = 6.0


def g_RA(x): return G.R('A', x)
def g_RC(x): return G.R('C', x)
def g_RE(x): return G.R('E', x)
def g_MA(x): return G.Mfix('A', x)
def g_VF(x, side=+1): return G.V(XF, x, side)


G_TABLE = {
    'RA': [g_RA(x) for _, x in G_PTS],
    'RC': [g_RC(x) for _, x in G_PTS],
    'RE': [g_RE(x) for _, x in G_PTS],
    'MA': [g_MA(x) for _, x in G_PTS],
}
G_VF = {'B': g_VF(4.0), 'F-': g_VF(6.0 - 1e-9), 'F+': g_VF(6.0 + 1e-9), 'C': g_VF(8.0),
        'D': g_VF(12.0), 'E': g_VF(16.0)}
# 例 2-2：一部 100 kN 單軸載重可停在梁上任一處 → R_C 最大、最小
G_RC_MAX = max(g_RC(x) for x in np.linspace(0, 16, 1601))   # 2（在 D）
G_RA_MIN = min(g_RA(x) for x in np.linspace(0, 16, 1601))   # −1（在 D）

# 第 2 章預告：一端固定一端滾支承（靜不定）R_C 影響線，x 從固定端量
def RC_prop(x, Lp=L):
    return x ** 2 * (3 * Lp - x) / (2 * Lp ** 3)


RC_PROP_4 = RC_prop(4.0)           # 0.208


def check_linear(fn, x1, x2, n=9):
    """檢查 fn 在 [x1,x2] 內為直線（靜定 IL 的性質）。回傳最大偏差。"""
    xs = np.linspace(x1, x2, n)
    ys = np.array([fn(x) for x in xs])
    lin = ys[0] + (ys[-1] - ys[0]) * (xs - xs[0]) / (xs[-1] - xs[0])
    return float(np.max(np.abs(ys - lin)))


if __name__ == '__main__':
    print('== 第 1 章 簡支梁 L=10, C 在 a=6 ==')
    for x in (0, 3, 6, 10):
        print(f'x={x:>4}: RA={RA_ss(x):.3f} (solver {SS.R("A", x):.3f})  RB={RB_ss(x):.3f}  '
              f'MC={MC_ss(x):.3f} (solver {SS.M(a, x):.3f})')
    print('VC 跳躍 ', VC_LEFT, '→', VC_RIGHT, '  solver', SS.V(a, a - 1e-9), SS.V(a, a + 1e-9))
    print('MC 峰值 ab/L =', MC_PEAK, '  延長線：左線在 x=L 高', b, '、右線在 x=0 高', a)
    print('例 1-1 50kN@3m:', {k: round(v, 3) for k, v in EX1.items()}, ' 停在 C:', EX1_atC)
    print('BMD(載重在3)在 C 的值 =', BMD_at_C, '  IL_MC(3) =', MC_ss(3))
    print('\n== 第 2 章 懸臂段 D=13 ==')
    print('RA(D)=', round(OH_RA_D, 3), ' RB(D)=', round(OH_RB_D, 3), ' MC(D)=', round(OH_MC_D, 3),
          ' VC(D)=', round(OH_VC_D, 3))
    print('Müller-Breslau 彎矩：左段轉角', thA, ' 右段轉角', thB, ' 和 =', thA + thB, ' 峰值 =', thA * a)
    print('\n== SA-2025-2 ==')
    print('位置   ', [p for p, _ in G_PTS])
    for k, v in G_TABLE.items():
        print(f'{k:3s}    ', [float(round(t, 3)) + 0.0 for t in v])
    print('VF     ', {k: float(round(v, 3)) + 0.0 for k, v in G_VF.items()})
    print('RC 最大', round(G_RC_MAX, 3), '  RA 最小', round(G_RA_MIN, 3))
    print('直線檢查（偏差）：RC 在 B–D', check_linear(g_RC, 4, 12), ' D–E', check_linear(g_RC, 12, 16))
    print('\n== 靜不定預告 ==  RC_prop(4) =', round(RC_PROP_4, 4))
