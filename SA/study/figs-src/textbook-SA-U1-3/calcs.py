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



# ═════════════════════════════════════════════
# 第 3～7 章（2026-11-18 補齊）
# 每個閉合解都另以 fe.py（直接勁度法）逐點驗算；不一致就 assert 失敗。
# ═════════════════════════════════════════════
from fe import Frame, Truss
from fractions import Fraction as Fr

TOL = 1e-6


def lerp_nodes(xn, yn, x):
    """節點值 → 節間直線（桁架影響線的本質）。"""
    return float(np.interp(x, xn, yn))


def truss_il(tr, load_nodes, qty):
    """把單位載重逐一放在 load_nodes（名稱），回傳 qty(u, R, N) 的節點值。"""
    out = []
    for nm in load_nodes:
        u, R, N = tr.solve({nm: (0.0, -1.0)})
        out.append(qty(u, R, N))
    return out


# ─────────────────────────────────────────────
# 第 3 章：桁架影響線
# ─────────────────────────────────────────────
# 3.1 縱梁（簡支）把節間內的載重分給兩節點
def panel_share(x, xi, xj):
    t = (x - xi) / (xj - xi)
    return 1 - t, t


DECK_X, DECK_XI, DECK_XJ = 13.0, 10.0, 20.0          # 例：載重在 b–c 節間、距 b 3 m
DECK_SHARE = panel_share(DECK_X, DECK_XI, DECK_XJ)   # (0.7, 0.3)

# 3.2 SA-2004-2 桁架：下弦 a–e 4@10 m、高 10 m
T4 = dict(a=(0, 0), b=(10, 0), c=(20, 0), d=(30, 0), e=(40, 0), B=(10, 10), C=(20, 10), D=(30, 10))
T4_MEM = [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('B', 'C'), ('C', 'D'), ('a', 'B'), ('B', 'b'),
          ('B', 'c'), ('C', 'c'), ('c', 'D'), ('D', 'd'), ('D', 'e')]
TR4 = Truss(T4, T4_MEM, {'a': (True, True), 'e': (False, True)})
T4_X = [0, 10, 20, 30, 40]
T4_LN = ['a', 'b', 'c', 'd', 'e']
L4, H4 = 40.0, 10.0


def t4_Ra(x): return 1 - x / L4
def t4_Mbeam(s, x): return x * (L4 - s) / L4 if x <= s else s * (L4 - x) / L4
def t4_Nbc(x): return t4_Mbeam(10, x) / H4                     # 對 B 取矩：下弦拉
def t4_NBC(x): return -t4_Mbeam(20, x) / H4                    # 對 c 取矩：上弦壓
def t4_Vpanel(x, xi=10, xj=20):                                # 節間 b–c 的剪力（節點值再直線）
    vi, vj = -xi / L4, 1 - xj / L4
    if x <= xi: return -x / L4
    if x >= xj: return 1 - x / L4
    return vi + (vj - vi) * (x - xi) / (xj - xi)
def t4_NBc(x): return np.sqrt(2) * t4_Vpanel(x)                # 斜桿 Bc：N sin45° = V


_fe4 = truss_il(TR4, T4_LN, lambda u, R, N: (R['a'][1], TR4.force(N, 'b', 'c'), TR4.force(N, 'B', 'c'),
                                              TR4.force(N, 'B', 'C')))
for k, x in enumerate(T4_X):
    assert abs(_fe4[k][0] - t4_Ra(x)) < TOL and abs(_fe4[k][1] - t4_Nbc(x)) < TOL
    assert abs(_fe4[k][2] - t4_NBc(x)) < TOL and abs(_fe4[k][3] - t4_NBC(x)) < TOL
T4_NBC_PEAK = t4_Nbc(10)                     # 0.75
T4_NBc_b, T4_NBc_c = t4_NBc(10), t4_NBc(20)  # −0.354、+0.707
T4_NBc_zero = 10 + 10 * 0.25 / 0.75          # 13.33 m
T4_NBC_c = t4_NBC(20)                        # −1.0

# 3.3 SA-2014-1：上弦傾斜；CD 桿對 I(24,17) 取矩
T14 = dict(A=(0, 0), B=(12, 0), C=(24, 0), D=(36, 0), E=(48, 0), F=(60, 0), G=(72, 0),
           H=(12, 12), I=(24, 17), J=(36, 22), K=(48, 17), L=(60, 12))
T14_MEM = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'), ('F', 'G'),
           ('A', 'H'), ('H', 'I'), ('I', 'J'), ('J', 'K'), ('K', 'L'), ('L', 'G'),
           ('B', 'H'), ('C', 'I'), ('D', 'J'), ('E', 'K'), ('F', 'L'),
           ('H', 'C'), ('I', 'D'), ('K', 'D'), ('L', 'E')]
TR14 = Truss(T14, T14_MEM, {'A': (True, True), 'G': (False, True)})
T14_LN = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
T14_X = [0, 12, 24, 36, 48, 60, 72]
_fe14 = truss_il(TR14, T14_LN, lambda u, R, N: TR14.force(N, 'C', 'D'))


def t14_NCD(x):            # = 梁在 C（x=24）的彎矩 ÷ 17
    M = x * 48 / 72 if x <= 24 else 24 * (72 - x) / 72
    return M / 17


for k, x in enumerate(T14_X):
    assert abs(_fe14[k] - t14_NCD(x)) < TOL
T14_NODES = {nm: Fr(round(t14_NCD(x) * 17 * 3), 3 * 17) for nm, x in zip(T14_LN[1:6], T14_X[1:6])}
T14_MAX = ('C', t14_NCD(24))                 # 16/17

# 3.4 SA-2022-3：嵌板無斜桿＝剪力滑塊；d 處等效內鉸
T22 = {}
for i in range(11):
    T22[f'B{i}'] = (3 * i, 0)
for i in range(1, 10):
    T22[f'T{i}'] = (3 * i, 4)
T22_MEM = [(f'B{i}', f'B{i + 1}') for i in range(10)]
T22_MEM += [(f'T{i}', f'T{i + 1}') for i in range(1, 7)] + [('T8', 'T9')]
T22_MEM += [(f'T{i}', f'B{i}') for i in range(1, 10)]
T22_MEM += [('B0', 'T1'), ('T2', 'B3'), ('T6', 'B7'), ('B7', 'T8'), ('T9', 'B10')]
for p in (1, 3, 5, 8):
    T22_MEM += [(f'T{p}', f'B{p + 1}'), (f'B{p}', f'T{p + 1}')]
assert len(T22_MEM) == 39
TR22 = Truss(T22, T22_MEM, {'B0': (False, True), 'B4': (False, True), 'B6': (False, True), 'B10': (True, True)})
T22_X = [3 * i for i in range(11)]
_fe22 = truss_il(TR22, [f'B{i}' for i in range(11)],
                 lambda u, R, N: (R['B0'][1], R['B4'][1], R['B6'][1], R['B10'][1],
                                  TR22.force(N, 'B2', 'B3'), TR22.force(N, 'T2', 'B3')))
T22_TAB = {k: [r[j] for r in _fe22] for j, k in enumerate(['Ra', 'Rb', 'Rc', 'Re', 'Nmn', 'Nnk'])}


def eqbeam22(x):
    """等效 Gerber 梁（Müller-Breslau 形狀）：節點值。回傳 Ra、Rb、Rc、Re。"""
    if x <= 12: return (12 - x) / 12, x / 12, 0.0, 0.0
    if x <= 15: return (x - 12) / 12, 1 - 5 * (x - 12) / 12, 1 - (15 - x) / 3, 0.0
    if x <= 21: return (18 - x) / 12, (x - 18) / 12, 1.0, 0.0
    return (x - 30) / 36, (30 - x) / 36, 1 - (x - 21) / 9, (x - 21) / 9


for k, x in enumerate(T22_X):
    ra, rb, rc, re = eqbeam22(x)
    assert abs(T22_TAB['Ra'][k] - ra) < TOL and abs(T22_TAB['Rb'][k] - rb) < TOL
    assert abs(T22_TAB['Rc'][k] - rc) < TOL and abs(T22_TAB['Re'][k] - re) < TOL
    assert abs(T22_TAB['Nmn'][k] - (
        (6 * ra - max(6 - x, 0)) / 4)) < TOL                       # N_mn = M_k / 4（k 在 x=6）
    V = ra - (1.0 if x <= 6 else 0.0)                               # 6–9 嵌板剪力（節點上）
    assert abs(T22_TAB['Nnk'][k] - 1.25 * V) < TOL                  # N_nk = 5/4·V

T22_NNK_ZERO = 8.0       # 6–9 節間內變號：V=(x−8)/4
assert abs(lerp_nodes(T22_X, T22_TAB['Nnk'], 8.0)) < TOL

# ─────────────────────────────────────────────
# 第 4 章：求最大效應
# ─────────────────────────────────────────────
W_UDL = 10.0   # kN/m（例 4-1 自訂）


def area(fn, x1, x2, n=6000, sign=0):
    xs = np.linspace(x1, x2, n + 1)
    ys = np.array([fn(x) for x in xs])
    if sign > 0: ys = np.clip(ys, 0, None)
    if sign < 0: ys = np.clip(ys, None, 0)
    return float(np.sum((ys[1:] + ys[:-1]) * np.diff(xs)) / 2)


def oh_MC(x): return OH.M(a, x)
def oh_VC(x): return OH.V(a, x)
def oh_RA(x): return OH.R('A', x)


UDL = {
    'MC+': area(oh_MC, 0, LD, sign=1), 'MC-': area(oh_MC, 0, LD, sign=-1),
    'VC+': area(oh_VC, 0, LD, sign=1), 'VC-': area(oh_VC, 0, LD, sign=-1),
    'RA+': area(oh_RA, 0, LD, sign=1), 'RA-': area(oh_RA, 0, LD, sign=-1),
}
assert abs(UDL['MC+'] - 12) < 1e-3 and abs(UDL['MC-'] + 2.7) < 1e-3
assert abs(UDL['VC+'] - 0.8) < 1e-3 and abs(UDL['VC-'] + 2.25) < 1e-3
UDL_KN = {k: W_UDL * v for k, v in UDL.items()}
UDL_FULL_MC = W_UDL * (UDL['MC+'] + UDL['MC-'])          # 93（全鋪）

# 輪壓列（2004-2、2007-3 同一部卡車，車頭 ① 在最左、往左開）
AXLE_P = [20.0, 40.0, 40.0, 40.0]
AXLE_DX = [0.0, 2.4, 3.9, 5.4]
W_TRUCK = sum(AXLE_P)


def truck_effect(fn, x_front, span, P=AXLE_P, DX=AXLE_DX):
    s = 0.0
    for p, d in zip(P, DX):
        x = x_front + d
        if 0 <= x <= span:
            s += p * fn(x)
    return s


def truck_scan(fn, span, step=0.005, P=AXLE_P, DX=AXLE_DX):
    n = int(round((span + DX[-1]) / step))
    xs = np.round(np.linspace(-DX[-1], span, n + 1), 9)
    xs = np.unique(np.concatenate([xs, np.round([k - d for k in np.arange(0, span + 1e-9, 0.1) for d in DX], 9)]))
    vals = np.array([truck_effect(fn, x, span, P, DX) for x in xs])
    return xs, vals


# 2004-2 R_a：車頭 ① 放在 a
T4_RA_MAX = truck_effect(t4_Ra, 0.0, L4)                   # 128.3
_xs, _v = truck_scan(t4_Ra, L4)
assert abs(_v.max() - T4_RA_MAX) < 1e-6
# 2004-2 N_bc：判定法 W_L/a ≤ W/L ≤ (W_L+P)/a
CRIT_4 = []
for k in range(4):
    WL = sum(AXLE_P[:k])
    CRIT_4.append((k + 1, WL / 10, W_TRUCK / L4, (WL + AXLE_P[k]) / 10,
                   WL / 10 <= W_TRUCK / L4 <= (WL + AXLE_P[k]) / 10))
T4_NBC_CR = [c[0] for c in CRIT_4 if c[4]][0]            # ② 號軸
T4_NBC_MAX = truck_effect(t4_Nbc, 10 - AXLE_DX[T4_NBC_CR - 1], L4)    # 96.9
_xs4, _v4 = truck_scan(t4_Nbc, L4)
assert abs(_v4.max() - T4_NBC_MAX) < 1e-6
T4_SCAN = (_xs4, _v4)
T4_NBC_TRY = {k + 1: truck_effect(t4_Nbc, 10 - AXLE_DX[k], L4) for k in range(4)}
# 反向（車掉頭：40,40,40,20 在前）— 只是對照
_P_rev, _D_rev = AXLE_P[::-1], [0.0, 1.5, 3.0, 5.4]
T4_NBC_REV = truck_scan(t4_Nbc, L4, P=_P_rev, DX=_D_rev)[1].max()

# 2007-3 三鉸拱桁架
T7 = dict(A=(0, 0), B=(48, 0), E=(0, 17), F=(12, 17), G=(24, 17), H=(36, 17), I=(48, 17), C=(12, 12), D=(36, 12))
T7_MEM = [('A', 'E'), ('A', 'C'), ('E', 'C'), ('F', 'C'), ('C', 'G'), ('G', 'D'), ('H', 'D'), ('D', 'I'),
          ('D', 'B'), ('I', 'B'), ('E', 'F'), ('F', 'G'), ('G', 'H'), ('H', 'I')]
TR7 = Truss(T7, T7_MEM, {'A': (True, True), 'B': (True, True)})
T7_X = [0, 12, 24, 36, 48]
_fe7 = truss_il(TR7, ['E', 'F', 'G', 'H', 'I'], lambda u, R, N: (R['A'][1], R['A'][0], TR7.force(N, 'F', 'G')))
T7_AY = [r[0] for r in _fe7]
T7_AX = [r[1] for r in _fe7]
T7_FG = [r[2] for r in _fe7]
assert np.allclose(T7_AY, [1, .75, .5, .25, 0], atol=TOL)
assert np.allclose(T7_AX, [0, 12 / 34, 24 / 34, 12 / 34, 0], atol=TOL)
assert np.allclose(T7_FG, [0, -81 / 85, 42 / 85, 21 / 85, 0], atol=TOL)


def t7_AY(x): return lerp_nodes(T7_X, T7_AY, x)
def t7_FG(x): return lerp_nodes(T7_X, T7_FG, x)


T7_AY_MAX = truck_effect(t7_AY, 0.0, 48)                 # 130.25
T7_FG_COMP = truck_effect(t7_FG, 12 - AXLE_DX[2], 48)    # ③ 在 F：−115.22
T7_FG_TENS = truck_effect(t7_FG, 24 - AXLE_DX[1], 48)    # ② 在 G：+59.68
_x7, _v7 = truck_scan(t7_FG, 48)
assert abs(_v7.min() - T7_FG_COMP) < 1e-6 and abs(_v7.max() - T7_FG_TENS) < 1e-6
assert abs(truck_scan(t7_AY, 48)[1].max() - T7_AY_MAX) < 1e-6

# 2011-3 的均布（曲線影響線；數字在第 7 章推）——第 4 章只引用
# ─────────────────────────────────────────────
# 第 5 章：靜不定影響線 ＝ v(x) / f_ii
# ─────────────────────────────────────────────
LP = 10.0          # SA-2003-4：A 固定、C 滾支承、B 在中點


def pc_v(x, Lp=LP):        # 懸臂（A 固定）自由端向上單位力時，x 處向上位移 × EI
    return x ** 2 * (3 * Lp - x) / 6


PC_F = LP ** 3 / 3         # f_CC × EI = 333.3
def pc_RC(x): return pc_v(x) / PC_F          # = RC_prop
def pc_VB(x): return (-pc_RC(x)) if x < 5 else (1 - pc_RC(x))
def pc_MB(x): return 5 * pc_RC(x) - max(x - 5, 0)


assert abs(pc_RC(4) - RC_PROP_4) < 1e-12


def beam_frame(L_, supports, h=0.25, EI=None, hinges=()):
    """直梁：supports=[(x, 'pin'|'roller'|'fixed')]；EI=[(x1,x2,EI)]；hinges＝內鉸位置（鉸左側元素釋放）。"""
    fr = Frame()
    cuts = sorted(set([0.0, L_] + [s[0] for s in supports] + list(hinges) + [e[0] for e in (EI or [])] +
                      [e[1] for e in (EI or [])]))
    for x1, x2 in zip(cuts[:-1], cuts[1:]):
        ei = 1.0
        for e in (EI or []):
            if e[0] <= x1 + 1e-9 and x2 <= e[1] + 1e-9:
                ei = e[2]
        n = max(1, int(round((x2 - x1) / h)))
        fr.member((x1, 0), (x2, 0), EI=ei, n=n, rel_j=any(abs(x2 - hh) < 1e-9 for hh in hinges))
    for x, k in supports:
        if k == 'fixed':
            fr.support(x, ux=True, uy=True, rz=True)
        elif k == 'pin':
            fr.support(x, ux=True, uy=True)
        else:
            fr.support(x, uy=True)
    return fr


def beam_il(fr, xs, qty):
    """把單位載重放在 xs 的每個節點，qty(R 依 x 的字典) 回傳量值。"""
    out = []
    for x in xs:
        nd = fr.node(x)
        u, R = fr.unit_down(nd)
        rx = {round(fr.xy[k][0], 6): R[k] for k in fr.fix}
        out.append(qty(rx, x, u))
    return np.array(out)


def M_left(rx, s, xP):
    m = 0.0
    for xk, r in rx.items():
        if xk < s - 1e-9:
            m += r[1] * (s - xk) - r[2]
    if xP < s - 1e-9:
        m -= (s - xP)
    return m


def V_left(rx, s, xP, side=+1):
    v = sum(r[1] for xk, r in rx.items() if xk < s - 1e-9)
    if xP < s - 1e-9 or (abs(xP - s) < 1e-9 and side > 0):
        v -= 1.0
    return v


_fpc = beam_frame(LP, [(0, 'fixed'), (LP, 'roller')])
_xs = np.arange(0, LP + 1e-9, 0.5)
_rc = beam_il(_fpc, _xs, lambda rx, x, u: rx[LP][1])
assert np.allclose(_rc, [pc_RC(x) for x in _xs], atol=1e-9)
_mb = beam_il(_fpc, _xs, lambda rx, x, u: M_left(rx, 5, x))
assert np.allclose(_mb, [pc_MB(x) for x in _xs], atol=1e-9)
PC_TAB = {x: pc_RC(x) for x in (2.5, 4, 5, 7.5)}
PC_VB = (pc_VB(5 - 1e-12), pc_VB(5 + 1e-12))           # −5/16、+11/16
PC_MB_PEAK = pc_MB(5)                                    # 25/16
assert abs(PC_VB[0] + 5 / 16) < 1e-9 and abs(PC_VB[1] - 11 / 16) < 1e-9 and abs(PC_MB_PEAK - 25 / 16) < 1e-12

# 5.4 SA-2016-2 剛架（L=1、EI=1）：柱 AB 高 L、梁 BC 長 L，A 固定、C 滾支承
def fr16_v(x, L_=1.0): return L_ ** 2 * x + L_ * x ** 2 / 2 - x ** 3 / 6
FR16_F = 4 / 3                                  # f_CC·EI/L³
FR16_COL, FR16_BEAM = 1.0, 1 / 3                # 柱段 L³/EI、梁段 L³/3EI
def fr16_IL(x, L_=1.0): return (6 * L_ ** 2 * x + 3 * L_ * x ** 2 - x ** 3) / (8 * L_ ** 3)


_f16 = Frame()
_f16.member((0, 0), (0, 1), n=8)
_f16.member((0, 1), (1, 1), n=40)
_f16.support(0, 0, ux=True, uy=True, rz=True)
_f16.support(1, 1, uy=True)
for x in np.linspace(0, 1, 9):
    u, R = _f16.unit_down(_f16.node(x, 1))
    assert abs(R[_f16.node(1, 1)][1] - fr16_IL(x)) < 1e-6    # 軸向 EA=1e9（近似不計軸變）
_f16b = Frame()                                  # 基本結構：拿掉 C 的滾支承（懸臂剛架）
_f16b.member((0, 0), (0, 1), n=8)
_f16b.member((0, 1), (1, 1), n=40)
_f16b.support(0, 0, ux=True, uy=True, rz=True)
_u, _R = _f16b.solve({_f16b.node(1, 1): (0, 1.0, 0)})
assert abs(_u[_f16b.node(1, 1)][1] - FR16_F) < 1e-5
for x in (0.25, 0.5, 0.75):
    assert abs(_u[_f16b.node(x, 1)][1] - fr16_v(x)) < 1e-5
FR16_SWAY = _u[_f16b.node(0, 1)][0]               # C 向上推 1 時 B 的水平位移（≠0：有側移）
FR16_TAB = {r: fr16_IL(r) for r in (0.25, 0.5, 0.75)}   # 107/512、29/64、369/512

# 5.5 SA-2020-3：a 鉸、b 滾、c 內鉸、d 固定；ab=bc=2、cd=3；cd 為 1.5EI
F20_RIGID, F20_BEND = 1.5, 4 / 3                 # f_bb·EI 的兩部分：c 上升 3 的一半＋ac 簡支彎曲 L³/48
F20 = F20_RIGID + F20_BEND                       # 17/6
assert abs(F20 - 17 / 6) < 1e-12
F20_VC = 0.5 * 27 / (3 * 1.5)                    # 懸臂 cd 端點受 0.5 上升 3/EI


def v20(x):
    if x <= 2: return (21 * x - x ** 3) / 12
    if x <= 4: return (x ** 3 - 12 * x ** 2 + 45 * x - 16) / 12
    x2 = x - 4
    return (x2 ** 3 / 18 - 1.5 * x2 + 3)


def il20(x): return v20(x) / F20


_f20 = beam_frame(7, [(0, 'pin'), (2, 'roller'), (7, 'fixed')], EI=[(4, 7, 1.5)], hinges=[4])
_x20 = np.arange(0, 7 + 1e-9, 0.25)
_rb20 = beam_il(_f20, _x20, lambda rx, x, u: rx[2.0][1])
assert np.allclose(_rb20, [il20(x) for x in _x20], atol=1e-9)
IL20_MAX = il20(3.0)                              # 19/17
IL20_C = il20(4.0)                                # 18/17
assert abs(IL20_MAX - 19 / 17) < 1e-12 and abs(IL20_C - 18 / 17) < 1e-12
assert max(_rb20) <= IL20_MAX + 1e-9

# ─────────────────────────────────────────────
# 第 6 章：互易定理
# ─────────────────────────────────────────────
# 6.1 互易的數字示範：10 m 簡支梁，EI=1
_fs = beam_frame(10, [(0, 'pin'), (10, 'roller')], h=0.5)
_u3, _ = _fs.unit_down(_fs.node(3))
_u6, _ = _fs.unit_down(_fs.node(6))
BETTI_63 = -_u3[_fs.node(6)][1]      # 載重在 3、量 6
BETTI_36 = -_u6[_fs.node(3)][1]      # 載重在 6、量 3
assert abs(BETTI_63 - BETTI_36) < 1e-9


def ss_defl(P_at, x, L_=10.0):        # 簡支梁 P=1 在 P_at，x 處下垂 × EI（閉合解）
    a_, b_ = (P_at, L_ - P_at)
    if x <= a_:
        return b_ * x * (L_ ** 2 - b_ ** 2 - x ** 2) / (6 * L_)
    return a_ * (L_ - x) * (L_ ** 2 - a_ ** 2 - (L_ - x) ** 2) / (6 * L_)


assert abs(ss_defl(3, 6) - BETTI_63) < 1e-9 and abs(ss_defl(6, 3) - BETTI_36) < 1e-9

# 6.2 SA-2018-4：C 點向下位移影響線（EI=800 kN·m²）
EI18 = 800.0
_f18 = Frame()
_f18.member((0, 0), (5, 0), EI=EI18, n=40)
_f18.member((5, 0), (15, 0), EI=EI18, n=80)
_f18.member((15, 0), (20, 0), EI=EI18, n=40)
_f18.member((2, -4), (5, 0), EI=EI18, n=10)
_f18.member((18, -4), (15, 0), EI=EI18, n=10)
_f18.support(0, 0, uy=True)
_f18.support(20, 0, uy=True)
_f18.support(2, -4, ux=True, uy=True, rz=True)
_f18.support(18, -4, ux=True, uy=True, rz=True)
_uC, _ = _f18.unit_down(_f18.node(10))
V18_C = -_uC[_f18.node(10)][1]
assert abs(V18_C - 55 / 6144) < 1e-6
TH18_B = -_uC[_f18.node(5)][2]   # 順時針為正
assert abs(abs(_uC[_f18.node(5)][2]) - 1 / 1024) < 1e-6
assert abs(_uC[_f18.node(5)][1]) < 1e-7 and abs(_uC[_f18.node(5)][0]) < 1e-7    # B 不平移


def v18(x):
    """C 受向下 1 時梁的下垂（＝C 點位移影響線），m/kN。"""
    if x > 10: x = 20 - x
    if x <= 5:
        return x * (x ** 2 - 25) / 51200
    s = x - 5             # BD 段：簡支 + 兩端負彎矩 −35/32
    L_ = 10.0
    simp = s * (3 * L_ ** 2 - 4 * s ** 2) / (48 * EI18) if s <= 5 else 0
    endm = (-35 / 32) * s * (L_ - s) / (2 * EI18)
    return simp + endm


_x18 = np.arange(0, 20 + 1e-9, 0.25)
_v18_fe = [-_uC[_f18.node(x)][1] for x in _x18]
assert np.allclose(_v18_fe, [v18(x) for x in _x18], atol=1e-8)
# 互易檢查：載重放在 x、量 C 的下垂 ＝ 上面那條曲線
for x in (2.5, 7.5, 12.5):
    _ux, _ = _f18.unit_down(_f18.node(x))
    assert abs(-_ux[_f18.node(10)][1] - v18(x)) < 1e-7, (x, -_ux[_f18.node(10)][1], v18(x))
V18_MIN_X = 5 / np.sqrt(3)
V18_MIN = v18(V18_MIN_X)
assert abs(V18_MIN + 5 * np.sqrt(3) / 9216) < 1e-9
K18 = dict(AB=3 * EI18 / 5, BF=4 * EI18 / 5, BD=2 * EI18 / 10)   # 480、640、160
FEM18 = 1 * 10 / 8                                                # 1.25

# 6.3 SA-2021-3：兩端鉸支桁架，H_a ＝ v_i / f_ee
T21 = dict(a=(0, 0), b=(3, 0), c=(6, 0), d=(9, 0), e=(12, 0), f=(3, 4), g=(6, 4), h=(9, 4))
T21_MEM = [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('f', 'g'), ('g', 'h'), ('a', 'f'), ('h', 'e'),
           ('f', 'b'), ('g', 'c'), ('h', 'd'), ('b', 'g'), ('g', 'd')]
TR21 = Truss(T21, T21_MEM, {'a': (True, True), 'e': (True, True)})
TR21_0 = Truss(T21, T21_MEM, {'a': (True, True), 'e': (False, True)})      # 基本結構：e 改滾支承
T21_LN = ['a', 'b', 'c', 'd', 'e']
T21_X = [0, 3, 6, 9, 12]
_t21 = truss_il(TR21, T21_LN, lambda u, R, N: (R['a'][0], TR21.force(N, 'a', 'b'), TR21.force(N, 'b', 'g')))
_t21_0 = truss_il(TR21_0, T21_LN, lambda u, R, N: (TR21_0.force(N, 'a', 'b'), TR21_0.force(N, 'b', 'g'),
                                                     u[TR21_0.ix['e']][0]))
T21_HA = [r[0] for r in _t21]
T21_SAB = [r[1] for r in _t21]
T21_SBG = [r[2] for r in _t21]
T21_SAB0 = [r[0] for r in _t21_0]
T21_SBG0 = [r[1] for r in _t21_0]
T21_VE = [r[2] for r in _t21_0]                       # e 向右滑（×EA），＝ v_i
F21_EE = 12.0                                          # ×1/EA
assert np.allclose(T21_HA, [0, 3 / 8, 9 / 16, 3 / 8, 0], atol=TOL)
assert np.allclose(T21_SAB, [0, 3 / 16, -3 / 16, -3 / 16, 0], atol=TOL)
assert np.allclose(T21_SBG, [0, 5 / 16, -10 / 16, -5 / 16, 0], atol=TOL)
assert np.allclose(T21_SBG, T21_SBG0, atol=TOL)
assert np.allclose(T21_SAB0, [0, 9 / 16, 6 / 16, 3 / 16, 0], atol=TOL)
assert np.allclose(T21_VE, [0, 4.5, 6.75, 4.5, 0], atol=TOL)
_u, _R, _N = TR21_0.solve({'e': (1.0, 0.0)})
assert abs(_u[TR21_0.ix['e']][0] - F21_EE) < 1e-9

# ─────────────────────────────────────────────
# 第 7 章：連續梁（三彎矩方程、共軛梁）
# ─────────────────────────────────────────────
def MB_equal(u, L_):
    """等跨兩跨連續梁（兩端簡支）中間支承彎矩影響線；u＝載重到『所在跨外側支承』的距離。"""
    return -u * (L_ ** 2 - u ** 2) / (4 * L_ ** 2)


# 7.2 SA-2005-3：A 滾、B 鉸、C 滾，10+10 m；D 在 BC 中點
def md05(x):
    if x <= 10:
        return MB_equal(x, 10) / 2
    xp = x - 10
    simp = xp / 2 if xp <= 5 else (10 - xp) / 2
    return simp + MB_equal(10 - xp, 10) / 2


_f05 = beam_frame(20, [(0, 'roller'), (10, 'pin'), (20, 'roller')])
_x05 = np.arange(0, 20 + 1e-9, 2.5)
_md = beam_il(_f05, _x05, lambda rx, x, u: M_left(rx, 15, x))
assert np.allclose(_md, [md05(x) for x in _x05], atol=1e-9)
MD05_TAB = [(x, md05(x)) for x in _x05]
MD05_PEAK = md05(15)                 # 65/32
assert abs(MD05_PEAK - 65 / 32) < 1e-12

# 7.3 SA-2011-3：A 滾(0)、B 滾(30)、D 鉸(60)，C 在 45
L11 = 30.0


def mb11(x): return MB_equal(x, L11) if x <= L11 else MB_equal(60 - x, L11)


def mc11(x):
    simp = 0.0
    if x >= L11:
        xp = x - L11
        simp = xp / 2 if xp <= 15 else (L11 - xp) / 2
    return simp + mb11(x) / 2


def ra11(x): return ((L11 - x) / L11 if x <= L11 else 0.0) + mb11(x) / L11
def rd11(x): return ra11(60 - x)
def rb11(x): return 1 - ra11(x) - rd11(x)
def vc11(x, side=+1): return ra11(x) + rb11(x) - (1.0 if (x < 45 or (x == 45 and side > 0)) else 0.0)


_f11 = beam_frame(60, [(0, 'roller'), (30, 'roller'), (60, 'pin')], h=0.5)
_x11 = np.arange(0, 60 + 1e-9, 1.0)
_chk = beam_il(_f11, _x11, lambda rx, x, u: (rx[0.0][1], rx[30.0][1], M_left(rx, 30, x), M_left(rx, 45, x)))
assert np.allclose(_chk[:, 0], [ra11(x) for x in _x11], atol=1e-9)
assert np.allclose(_chk[:, 1], [rb11(x) for x in _x11], atol=1e-9)
assert np.allclose(_chk[:, 2], [mb11(x) for x in _x11], atol=1e-9)
assert np.allclose(_chk[:, 3], [mc11(x) for x in _x11], atol=1e-9)
MC11_PEAK = mc11(45)                                    # 195/32
VC11 = (vc11(45 - 1e-12), vc11(45 + 1e-12))             # −13/32、+19/32
XMIN11 = L11 / np.sqrt(3)                               # 17.32
MB11_MIN = mb11(XMIN11)                                 # −2.887
RA11_MIN = ra11(60 - XMIN11)                            # −0.0962
VC11_AB = vc11(XMIN11)                                  # +0.0962
MC11_AB = mc11(XMIN11)                                  # −1.443
assert abs(MC11_PEAK - 195 / 32) < 1e-12 and abs(VC11[0] + 13 / 32) < 1e-12 and abs(VC11[1] - 19 / 32) < 1e-12
A11_POS = area(mc11, 30, 60)                            # 84.375
A11_NEG = area(mc11, 0, 30)                             # −28.125
A11_SIMP, A11_MB = L11 ** 2 / 8, -L11 ** 2 / 16         # 112.5、−56.25
assert abs(area(mb11, 0, 30) - A11_MB) < 1e-3
W11 = 2.0
M11_MAX = W11 * A11_POS                                 # 168.75
M11_FULL = W11 * (A11_POS + A11_NEG)                    # 112.5
M11_MIN = W11 * A11_NEG                                 # −56.25
assert abs(M11_MAX - 168.75) < 1e-2 and abs(M11_FULL - 112.5) < 1e-2

# 7.4 SA-2015-2：A 鉸(0)、B 滾(30)、C 內鉸(40)、D 滾(50)、E 滾(80)；F 在 15
_f15 = beam_frame(80, [(0, 'pin'), (30, 'roller'), (50, 'roller'), (80, 'roller')], h=0.5, hinges=[40])
_x15 = np.arange(0, 80 + 1e-9, 0.5)
_vf = beam_il(_f15, _x15, lambda rx, x, u: V_left(rx, 15, x, side=+1))


def vf15(x):
    if x <= 15: return x * (x ** 2 - 5700) / 144000
    if x <= 30: return (x - 30) * (x ** 2 + 30 * x - 4800) / 144000
    if x <= 40: return -(x - 30) * (x ** 2 - 90 * x + 2800) / 48000
    if x <= 50: return -(x - 50) * (x ** 2 - 70 * x + 400) / 48000
    return (x - 110) * (x - 80) * (x - 50) / 144000


for x, v in zip(_x15, _vf):
    if abs(x - 15) > 1e-9:
        assert abs(v - vf15(x)) < 1e-9, (x, v, vf15(x))
VF15_L = vf15(15)                         # −73/128（F 左）
VF15_R = VF15_L + 1                       # +55/128
VF15_C = vf15(40)                         # −1/6
assert abs(VF15_L + 73 / 128) < 1e-12 and abs(VF15_C + 1 / 6) < 1e-12
_xx = np.linspace(50, 80, 30001)
_yy = [vf15(x) for x in _xx]
VF15_DE_MAX = (float(_xx[int(np.argmax(_yy))]), max(_yy))   # (62.7, 0.0722)
# 基本結構（F 剪力釋放、施剪力對）反力與彎矩（×EI 的共軛載重）
REL15 = dict(A=1, B=-4, D=4, E=-1)
def m15(x):
    if x <= 30: return x
    if x <= 50: return 120 - 3 * x
    return x - 80
assert m15(40) == 0
CONJ15 = dict(thA=-950.0, dF=24000.0, yFm=-13687.5, yC=-4000.0)
assert abs(CONJ15['yFm'] / CONJ15['dF'] - VF15_L) < 1e-12
assert abs((CONJ15['yFm'] + CONJ15['dF']) / CONJ15['dF'] - VF15_R) < 1e-12
assert abs(CONJ15['yC'] / CONJ15['dF'] - VF15_C) < 1e-12

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
    # ───────── 第 3～7 章 ─────────
    r = lambda v, n=4: float(round(v, n)) + 0.0
    print('\n== 第 3 章 桁架 ==')
    print('縱梁分配 x=13 在 10–20：', DECK_SHARE)
    print('2004-2 節點 x', T4_X)
    print('  Ra ', [r(t4_Ra(x)) for x in T4_X])
    print('  Nbc', [r(t4_Nbc(x)) for x in T4_X], ' 峰值', T4_NBC_PEAK)
    print('  NBc', [r(t4_NBc(x)) for x in T4_X], ' 零點', r(T4_NBc_zero))
    print('  NBC', [r(t4_NBC(x)) for x in T4_X])
    print('2014-1 N_CD（×P）', {k: str(v) for k, v in T14_NODES.items()}, ' 最大', T14_MAX[0], r(T14_MAX[1]))
    print('2022-3 節點 x', T22_X)
    for k, v in T22_TAB.items():
        print(f'  {k:4s}', [str(Fr(x).limit_denominator(64)) for x in v])
    print('\n== 第 4 章 最大效應 ==')
    print('懸臂梁面積（m² 或 m）', {k: r(v, 3) for k, v in UDL.items()})
    print(f'w = {W_UDL} kN/m →', {k: r(v, 2) for k, v in UDL_KN.items()}, ' M_C 全鋪', r(UDL_FULL_MC, 2))
    print('2004-2 Ra,max', r(T4_RA_MAX, 2))
    print('  判定法 (軸, W_L/a, W/L, (W_L+P)/a, 成立)', CRIT_4)
    print('  各軸放在 b 的 N_bc', {k: r(v, 2) for k, v in T4_NBC_TRY.items()}, ' 最大', r(T4_NBC_MAX, 2), ' 掉頭對照', r(T4_NBC_REV, 2))
    print('2007-3 Ay', [r(v) for v in T7_AY], ' Ax', [r(v) for v in T7_AX], ' FG', [str(Fr(v).limit_denominator(100)) for v in T7_FG])
    print('  Ay,max', r(T7_AY_MAX, 2), ' FG 壓', r(T7_FG_COMP, 2), ' FG 拉', r(T7_FG_TENS, 2))
    print('\n== 第 5 章 靜不定 ==')
    print('撐竿懸臂 L=10：f·EI =', r(PC_F, 3), ' R_C', {k: r(v) for k, v in PC_TAB.items()})
    print('  V_B', PC_VB, ' M_B 峰', PC_MB_PEAK, '（簡支對照 2.5、∓0.5）')
    print('2016-2 f_CC: 梁', FR16_BEAM, '柱', FR16_COL, '合', FR16_F, ' 柱佔', FR16_COL / FR16_F, ' IL', {k: r(v) for k, v in FR16_TAB.items()},
          ' B 側移(C 推上 1 力)', r(FR16_SWAY))
    print('2020-3 f_bb·EI 剛體', F20_RIGID, ' 彎曲', r(F20_BEND), ' 合', r(F20), ' v_c', F20_VC)
    print('  IL', {x: r(il20(x)) for x in (1, 2, 3, 4, 5.5, 7)}, ' max', r(IL20_MAX), ' c', r(IL20_C))
    print('\n== 第 6 章 互易 ==')
    print('簡支 10 m：載重 3 量 6 =', r(BETTI_63), '；載重 6 量 3 =', r(BETTI_36), '（×1/EI）')
    print('2018-4 勁度', K18, ' FEM', FEM18, ' θB', r(abs(TH18_B), 7), ' 1/1024 =', r(1 / 1024, 7))
    print('  v_C', r(V18_C, 6), ' 55/6144=', r(55 / 6144, 6), ' 外跨最小', r(V18_MIN, 6), '@', r(V18_MIN_X, 3))
    print('2021-3 v_e(×1/EA)', [r(v) for v in T21_VE], ' f_ee', F21_EE)
    print('  H_a', [str(Fr(v).limit_denominator(64)) for v in T21_HA])
    print('  S_ab0', [str(Fr(v).limit_denominator(64)) for v in T21_SAB0], ' S_ab', [str(Fr(v).limit_denominator(64)) for v in T21_SAB])
    print('  S_bg', [str(Fr(v).limit_denominator(64)) for v in T21_SBG])
    print('\n== 第 7 章 連續梁 ==')
    print('2005-3 M_D', [(float(x), str(Fr(v).limit_denominator(512))) for x, v in MD05_TAB])
    print('2011-3 MC 峰', MC11_PEAK, ' VC', VC11, ' 極值位置', r(XMIN11, 2), ' MB', r(MB11_MIN, 3), ' RA', r(RA11_MIN), ' VC(AB)', r(VC11_AB), ' MC(AB)', r(MC11_AB, 3))
    print('  面積 + ', r(A11_POS, 3), ' − ', r(A11_NEG, 3), ' A1', A11_SIMP, ' A_MB', A11_MB, ' M_max', r(M11_MAX, 2), ' 全鋪', r(M11_FULL, 2), ' M_min', r(M11_MIN, 2))
    print('2015-2 VF', r(VF15_L), r(VF15_R), ' C', r(VF15_C), ' DE 極大', (r(VF15_DE_MAX[0], 1), r(VF15_DE_MAX[1])))
