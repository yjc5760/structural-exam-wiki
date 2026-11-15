# -*- coding: utf-8 -*-
"""SA-U2-1 靜不定結構最小功法 教科書講義：全部數值（圖與內文共用，先算再寫）。

單位：kN、m。
貫穿全書的範例：SA-2014-4（L 形剛架；A 固定、D 滾支承；AC 梁 12 m、EI = 1000 kN·m²；
B 為 AC 中點，20 kN 向下）。因 D 為滾支承，CD 柱彎矩恆為 0，整題等於一支
「A 固定、C 端被往上頂住」的梁——第 2 章先拿掉頂住的力（懸臂梁）算位移，
第 3 章以最小功法求 R，第 4 章用圖乘法再算一次，第 5 章把 C 端也固定，得到 PL/8。

考題數字取自 raw/solutions/SA-2014-4/SA-2014-4.md（盲解比對 AUDIT-SA-U2-1-B1 一致、無勘誤）。
座標：x 由 C（自由端）向左量，0 ≤ x ≤ 12；彎矩以「下緣受拉為正」。
執行 `python3 calcs.py` 印出所有數值，與內文逐一對照。
"""
from fractions import Fraction as Fr

# ------------------------------------------------------------------ 共用積分工具（精確分數）
def integ_poly(coefs, a, b):
    """∫_a^b Σ c_k x^k dx，coefs = [c0, c1, c2, ...]，皆 Fraction。"""
    a, b = Fr(a), Fr(b)
    return sum(Fr(c) * (b ** (k + 1) - a ** (k + 1)) / (k + 1) for k, c in enumerate(coefs))


def pmul(p, q):
    out = [Fr(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += Fr(a) * Fr(b)
    return out


# ------------------------------------------------------------------ 貫穿範例 SA-2014-4
EX = dict(P=Fr(20), L=Fr(12), a=Fr(6), EI=Fr(1000))


def M_real(x, R=0.0, P=20.0, a=6.0):
    """AC 梁彎矩（下緣受拉為正），x 由 C 向左；R 為 C 端向上力（第 2 章 R = 0）。"""
    return R * x - P * max(0.0, x - a)


def ch1():
    d = {}
    # 1.1 功：線彈性慢慢加載 = 三角形；突加 = 矩形（兩倍）
    k, Pmax = 50.0, 20.0                       # 示意彈簧 50 kN/m、終值 20 kN
    d['k'], d['P'] = k, Pmax
    d['delta'] = Pmax / k                       # 0.4 m
    d['W_slow'] = 0.5 * Pmax * d['delta']       # 4 kN·m
    d['W_rect'] = Pmax * d['delta']             # 8 kN·m（常犯：忘了 ½）
    # 1.6 剪力 vs 彎曲應變能：懸臂梁端點集中載重、矩形斷面
    #     U_M = P²L³/(6EI)，I = bh³/12 → 2P²L³/(E b h³)
    #     U_V = κP²L/(2GA) = κP²L/(2G b h)
    #     U_V/U_M = (κ/4)(E/G)(h/L)²；κ = 6/5、ν = 0.3 → E/G = 2.6
    kap, nu = 1.2, 0.3
    EG = 2 * (1 + nu)
    d['kappa'], d['EG'] = kap, EG
    d['coef'] = kap / 4 * EG                    # 0.78
    d['ratio'] = lambda Lh: d['coef'] / Lh ** 2
    d['ratio_LH'] = {Lh: d['coef'] / Lh ** 2 for Lh in (2, 3, 5, 10, 20)}
    # 1.7 SA-2014-4 的 CD 柱：滾支承 → D_x = 0 → M_CD ≡ 0、U_CD = 0
    d['MCD'] = 0
    return d


def ch2():
    """懸臂梁（拿掉 C 端支承）：卡氏定理＋虛設力求 C 點位移與轉角。"""
    d = {}
    P, a, Lb = EX['P'], EX['a'], EX['L']
    # 實際彎矩：0 ≤ x < 6：M = 0；6 ≤ x ≤ 12：M = −P(x − a)
    M2 = [P * a, -P]                            # −P(x−a) = −Px + Pa（6 ≤ x ≤ 12 段）
    # (1) C 點垂直位移：虛設向下力 Q → ∂M/∂Q = m = −x（向下為正）
    m_down = [0, -1]
    d['dC'] = integ_poly(pmul(M2, m_down), a, Lb)        # = 3600（÷EI，向下）
    # (2) C 點轉角：虛設順時針力偶 Q → m = −1（順時針使下緣…見內文；此處取逆時針 +1）
    m_ccw = [1]                                          # 逆時針力偶：M 增加 +Q
    d['thC_ccw'] = integ_poly(pmul(M2, m_ccw), a, Lb)    # = −360 → 順時針 360/EI
    # (3) 柔度：C 端向上單位力的 m = +x，f11 = ∫x² = 576
    d['f11'] = integ_poly([0, 0, 1], 0, Lb)              # 576
    d['d10_up'] = integ_poly(pmul(M2, [0, 1]), a, Lb)    # −3600（向上為正 → 向下 3600）
    d['I6_12_x_xm6'] = integ_poly([0, -6, 1], 6, 12)     # ∫6^12 x(x−6) dx = 180
    d['I6_12_xm6'] = integ_poly([-6, 1], 6, 12)          # ∫6^12 (x−6) dx = 18
    # 數值（EI = 1000）
    d['dC_m'] = d['dC'] / EX['EI']                       # 3.6 m（示意：EI 很小）
    d['thC_rad'] = -d['thC_ccw'] / EX['EI']              # 0.36 rad 順時針
    # 公式檢查：懸臂、載重距固定端 b = 6、距自由端 a = 6
    b = Lb - a
    d['dC_formula'] = P * b ** 2 / 6 * (3 * Lb - b)      # Pb²(3L−b)/6 = 3600 ✔
    d['thC_formula'] = P * b ** 2 / 2                    # Pb²/2 = 360 ✔
    return d


def ch3():
    """最小功法：C 端向上力 R，∂U/∂R = 0；再以卡氏求 θC。"""
    d = {}
    c2 = ch2()
    P, a, Lb, EI = EX['P'], EX['a'], EX['L'], EX['EI']
    # ∂U/∂R = (1/EI)[R∫0^12 x² dx − P∫6^12 x(x−6) dx] = 0
    d['R'] = P * c2['I6_12_x_xm6'] / c2['f11']           # 3600/576 = 6.25
    d['R_frac'] = d['R']                                 # = 5P/16
    d['R_over_P'] = d['R'] / P                           # 5/16
    # θC（逆時針虛設力偶，m = +1）：R∫0^12 x dx − P∫6^12 (x−6) dx
    Ix = integ_poly([0, 1], 0, Lb)                       # 72
    d['Ix'] = Ix
    d['thC_EI'] = d['R'] * Ix - P * c2['I6_12_xm6']      # 450 − 360 = 90
    d['thC_rad'] = d['thC_EI'] / EI                      # 0.09 rad 逆時針
    d['MA'] = d['R'] * Lb - P * (Lb - a)                 # 75 − 120 = −45
    d['MB'] = d['R'] * a                                 # 37.5
    d['x0'] = P * a / (P - d['R'])                       # 反曲點：Rx = P(x−6) → x = 120/13.75
    return d


def ch5():
    """兩端固定、跨中集中載重：最小功法 → PL/8（自我驗算基準）。"""
    d = {}
    P, Lb = EX['P'], EX['L']
    d['MF'] = P * Lb / 8                                 # 30 kN·m
    return d


C1, C2, C3, C5 = ch1(), ch2(), ch3(), ch5()

if __name__ == '__main__':
    print('== 第 1 章')
    print(f"  彈簧 k={C1['k']} kN/m, P={C1['P']} kN → δ={C1['delta']} m；W(慢)={C1['W_slow']}、W(矩形)={C1['W_rect']} kN·m")
    print(f"  U_V/U_M = {C1['coef']:.3f}(h/L)²；", {k: f'{v*100:.2f}%' for k, v in C1['ratio_LH'].items()})
    print('== 第 2 章（懸臂，÷EI）')
    for k in ('dC', 'thC_ccw', 'f11', 'd10_up', 'I6_12_x_xm6', 'I6_12_xm6', 'dC_formula', 'thC_formula'):
        print(f'  {k} = {C2[k]}')
    print(f"  EI=1000 → δC={float(C2['dC_m'])} m、θC={float(C2['thC_rad'])} rad（順時針）")
    print('== 第 3 章（最小功法）')
    for k in ('R', 'R_over_P', 'Ix', 'thC_EI', 'thC_rad', 'MA', 'MB', 'x0'):
        v = C3[k]
        print(f'  {k} = {v}  ({float(v):.4f})')
    print('== 第 5 章')
    print(f"  PL/8 = {C5['MF']}")
