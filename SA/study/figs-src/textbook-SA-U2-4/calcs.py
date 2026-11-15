# -*- coding: utf-8 -*-
"""SA-U2-4 靜不定結構之矩陣分析法｜教科書講義的所有數值（圖與內文共用，先算再寫）。

正負號約定（全書統一）：
  * 轉角 θ、彎矩 M：逆時針為正。
  * 平移：整體座標 X 向右、Y 向上為正；梁元素局部 v 為「局部 y」方向（局部 x 逆轉 90°）。
  * 梁元素局部自由度順序 (v1, θ1, v2, θ2)。
規則：
  * 講義內文、圖、範例出現的每一個數字都要能在這裡找到來源。
  * 考題數字取自 raw/solutions/XX-YYYY-N/XX-YYYY-N.md（勘誤後版本）。
  * 執行 `python3 calcs.py`，把印出的數字和內文逐一對照。
"""
import math
import numpy as np
import sympy as sp

E_, I_, L_ = sp.symbols('E I L', positive=True)
EI = E_ * I_


# ───────── 第 1 章：彈簧元素由 S1 量出 ─────────
def spring_element():
    """左端推 1（右端鎖）→ 左需 +k、右需 −k；反之亦然。"""
    k = sp.symbols('k', positive=True)
    K = sp.zeros(2, 2)
    for j in range(2):
        d = [0, 0]; d[j] = 1
        N = k * (d[1] - d[0])     # 彈簧拉力（伸長為正）
        K[0, j] = -N              # 左節點需要的外力
        K[1, j] = +N              # 右節點需要的外力
    return K


# ───────── 第 2 章：懸臂柔度 → 梁元素勁度 ─────────
def cantilever_flex():
    """S3：懸臂（左端 x=0 固定）自由端受 V（向上）與 M（逆時針）時的 (v, θ)，由 v''=M/EI 積分。"""
    x, V, M = sp.symbols('x V M')
    Mx = V * (L_ - x) + M                 # 斷面彎矩（使下緣受拉為正）
    th = sp.integrate(Mx / EI, (x, 0, x))
    v = sp.integrate(th, (x, 0, x))
    vL, thL = sp.simplify(v.subs(x, L_)), sp.simplify(th.subs(x, L_))
    return sp.Matrix([[sp.diff(vL, V), sp.diff(vL, M)],
                      [sp.diff(thL, V), sp.diff(thL, M)]])


def end_stiffness():
    F = cantilever_flex()
    return F, sp.simplify(F.inv()), sp.simplify(F.det())


def beam_element():
    """右端兩行：S3 求逆＋整根梁平衡；左端兩行：Maxwell 對稱＋平衡。"""
    _, K22, _ = end_stiffness()
    k = sp.zeros(4, 4)
    for j, d in enumerate([(1, 0), (0, 1)]):
        V2, M2 = K22 * sp.Matrix(d)
        V1 = -V2                          # ΣFy = 0
        M1 = -M2 - V2 * L_                # 對左端 ΣM = 0
        k[:, 2 + j] = sp.Matrix([V1, M1, V2, M2])
    for i in (2, 3):                      # 對稱：k_ij = k_ji
        for j in (0, 1):
            k[i, j] = k[j, i]
    for j in (0, 1):                      # 左端推動時的平衡
        k[0, j] = -k[2, j]
        k[1, j] = -k[3, j] - k[2, j] * L_
    return sp.simplify(k)


def beam_element_reference():
    c = EI / L_**3
    return c * sp.Matrix([[12, 6 * L_, -12, 6 * L_],
                          [6 * L_, 4 * L_**2, -6 * L_, 2 * L_**2],
                          [-12, -6 * L_, 12, -6 * L_],
                          [6 * L_, 2 * L_**2, -6 * L_, 4 * L_**2]])


def hermite(xi):
    """單位端位移的變形形狀（ξ=x/L）：v1=1、θ1·L=1、v2=1、θ2·L=1。"""
    return (1 - 3 * xi**2 + 2 * xi**3, xi - 2 * xi**2 + xi**3,
            3 * xi**2 - 2 * xi**3, -xi**2 + xi**3)


def condense(k, keep, drop):
    Kaa = k.extract(keep, keep); Kab = k.extract(keep, drop); Kbb = k.extract(drop, drop)
    return sp.simplify(Kaa - Kab * Kbb.inv() * Kab.T)


def modified_and_sway():
    k = beam_element_reference()
    return dict(
        k_mod=condense(k, [1], [3])[0],                       # 遠端鉸：3EI/L
        sway_fixed_fixed=k[2, 2],                             # 頂轉角鎖住：12EI/L³
        sway_fixed_free_rot=condense(k, [2], [3])[0],         # 頂可自由轉：3EI/L³
        sway_pin_fixed=condense(k.extract([1, 2, 3], [1, 2, 3]), [1], [0])[0],  # 底鉸、頂鎖轉：3EI/L³
    )


# ───────── 貫穿範例：SA-2025-1 門型剛架 ─────────
def frame_elem_global(x1, y1, x2, y2, EIv=1.0, EAv=1e9):
    Lx, Ly = x2 - x1, y2 - y1
    Ln = math.hypot(Lx, Ly); c, s = Lx / Ln, Ly / Ln
    a = EAv / Ln; b = EIv / Ln**3
    kl = np.array([[a, 0, 0, -a, 0, 0],
                   [0, 12 * b, 6 * Ln * b, 0, -12 * b, 6 * Ln * b],
                   [0, 6 * Ln * b, 4 * Ln**2 * b, 0, -6 * Ln * b, 2 * Ln**2 * b],
                   [-a, 0, 0, a, 0, 0],
                   [0, -12 * b, -6 * Ln * b, 0, 12 * b, -6 * Ln * b],
                   [0, 6 * Ln * b, 2 * Ln**2 * b, 0, -6 * Ln * b, 4 * Ln**2 * b]])
    T = np.zeros((6, 6))
    for i in (0, 3):
        T[i:i + 2, i:i + 2] = [[c, s], [-s, c]]
        T[i + 2, i + 2] = 1
    return T.T @ kl @ T


def portal_numeric(beam_EI=1.0, L=1.0, col_EI=1.0, EA=1e9):
    """獨立驗算：完整 6 自由度（含軸向，EA 取極大近似忽略軸向變形）。"""
    nodes = {'A': (0, 0), 'B': (0, L), 'C': (L, L), 'D': (L, 0)}
    idx = {n: i for i, n in enumerate('ABCD')}
    K = np.zeros((12, 12))
    for (n1, n2, eiv) in [('A', 'B', col_EI), ('B', 'C', beam_EI), ('D', 'C', col_EI)]:
        ke = frame_elem_global(*nodes[n1], *nodes[n2], eiv, EA)
        dofs = [3 * idx[n1] + k for k in range(3)] + [3 * idx[n2] + k for k in range(3)]
        K[np.ix_(dofs, dofs)] += ke
    free = [3, 4, 5, 6, 7, 8]
    Fv = np.zeros(6); Fv[3] = 1.0           # P=1 作用在右上角 C（考卷）
    d = np.linalg.solve(K[np.ix_(free, free)], Fv)
    return dict(k_lat=1 / d[3], thB=d[2], thC=d[5], uB=d[0], uC=d[3])


def portal_symbolic():
    """手算版：3 自由度 (θB, θC, Δ)；柱局部 x 向上、局部 y 向左 → Δ（向右）= −v2。"""
    kb = beam_element_reference()
    T = sp.diag(-1, 1)
    kcol = sp.simplify(T.T * kb.extract([2, 3], [2, 3]) * T)     # (Δ, θ_top)
    K = sp.zeros(3, 3)
    for th_idx in (0, 1):                     # 左柱→θB、右柱→θC
        m = {0: 2, 1: th_idx}
        for i in range(2):
            for j in range(2):
                K[m[i], m[j]] += kcol[i, j]
    kbeam = kb.extract([1, 3], [1, 3])
    for i in range(2):
        for j in range(2):
            K[i, j] += kbeam[i, j]
    K = sp.simplify(K)
    kstar = condense(K, [2], [0, 1])[0]
    Kab = K.extract([2], [0, 1]); Kbb = K.extract([0, 1], [0, 1])
    th = sp.simplify((-Kbb.inv() * Kab.T)[0])
    return dict(kcol=kcol, K=K, kstar=kstar, th_per_delta=th)


def chain_example():
    """第 1 章範例：牆—k1—節點1—k2—節點2，P 作用在節點 2。"""
    k1, k2, P = sp.symbols('k1 k2 P', positive=True)
    K = sp.Matrix([[k1 + k2, -k2], [-k2, k2]])
    # 組裝版：元素 1（牆—1）只碰到 d1；元素 2（1—2）是完整 2×2
    Ka = sp.zeros(2, 2); Ka[0, 0] += k1
    Ka += k2 * sp.Matrix([[1, -1], [-1, 1]])
    d = sp.simplify(K.inv() * sp.Matrix([0, P]))
    return dict(K=K, same_as_assembly=(K == Ka), d1=d[0], d2=sp.simplify(d[1]),
                N1=sp.simplify(k1 * d[0]), N2=sp.simplify(k2 * (d[1] - d[0])), detK=sp.factor(K.det()))


def J_solid():
    r, R = sp.symbols('r R', positive=True)
    J = sp.integrate(r**2 * 2 * sp.pi * r, (r, 0, R))
    d = sp.symbols('d', positive=True)
    return J, sp.simplify(J.subs(R, d / 2))


PORTAL = dict(kstar_num=84, kstar_den=5, ratio_to_rigid=84 / 5 / 24, th_coef='-3/5')


if __name__ == '__main__':
    print('== 第 1 章 彈簧元素（由 S1 量出）'); sp.pprint(spring_element())
    ce = chain_example()
    print('串接範例', {k: v for k, v in ce.items() if k != 'K'})
    print('J =', J_solid())
    F, K22, det = end_stiffness()
    print('== 第 2 章 懸臂柔度 F'); sp.pprint(F)
    print('det F =', det)
    print('端勁度 F^-1'); sp.pprint(K22)
    kb = beam_element()
    print('梁元素 4×4（推導版）與教科書版相同？', sp.simplify(kb - beam_element_reference()) == sp.zeros(4, 4))
    sp.pprint(kb)
    print('== 修正勁度與柱側移勁度')
    for k, v in modified_and_sway().items():
        print('  ', k, '=', sp.simplify(v))
    ps = portal_symbolic()
    print('== SA-2025-1 門型剛架（手算版，逆時針為正）')
    print('柱頂 2×2 (Δ, θ):'); sp.pprint(ps['kcol'])
    print('[K] (θB, θC, Δ):'); sp.pprint(ps['K'])
    print('凝縮側向勁度 k* =', ps['kstar'])
    print('θB / Δ =', ps['th_per_delta'])
    pn = portal_numeric()
    print('數值獨立驗算 k·L³/EI =', round(pn['k_lat'], 6), '（84/5 =', 84 / 5, '）')
    print('數值 θB·L/Δ =', round(pn['thB'] * pn['k_lat'], 6), ' θC·L/Δ =', round(pn['thC'] * pn['k_lat'], 6))
    print('梁 EI→0：', round(portal_numeric(beam_EI=1e-6)['k_lat'], 4), '（2 × 3 = 6）')
    print('梁 EI→∞：', round(portal_numeric(beam_EI=1e6)['k_lat'], 4), '（2 × 12 = 24）')
    print('84/5 ÷ 24 =', round(84 / 5 / 24, 4))
