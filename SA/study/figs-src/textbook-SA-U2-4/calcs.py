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



# ═════════ 第 3～8 章（2026-11-18 補齊）═════════

def dof_count():
    """第 3 章：自由度盤點。回傳 (節點自由度總數, 支承束制, 軸向／剛性約束, 剩下)。"""
    return {
        'SA-2025-1 門型': (12, 6, 3, 3),     # 4 節點×3；A、D 固定各 3；兩柱＋梁不伸縮 3
        'SA-2018-2 Z 形': (12, 6, 3, 3),
        'SA-2012-4 剛桿': (12, 5, 5, 2),     # a 固定 3、d 鉸 2；三桿不伸縮 3＋cd 剛體 2（θc＝θd、vc＝θd·L/2）
    }


def portal_partition():
    """第 3 章：門型剛架單位 Δ＝1 時，用 [K_sf] 回代柱底反力（含節點轉角回應）。"""
    ps = portal_symbolic()
    th = ps['th_per_delta']                    # θB＝θC＝−3/(5L)
    # 左柱底 A：局部推導（柱底固定、頂 (Δ, θ)）。底端剪力＝−(12Δ/L³+6θ/L²)EI，底彎矩＝(6Δ/L²+2θ/L)EI
    V_top = EI * (12 / L_**3 + 6 * th / L_**2)          # 柱頂需要的水平力（每單位 Δ）
    M_base = EI * (6 / L_**2 + 2 * th / L_)             # 柱底彎矩（逆時針，每單位 Δ）
    M_top = EI * (6 / L_**2 + 4 * th / L_)
    return dict(V_col=sp.simplify(V_top), M_base=sp.simplify(M_base), M_top=sp.simplify(M_top),
                base_shear_sum=sp.simplify(2 * V_top))


def rigid_bar_2012():
    """SA-2012-4：ab 柱 L、bc 梁 L/2（EI）、cd 剛桿 L/2，d 鉸。r1＝θb、r2＝cd 轉角（兩者順時針為正）。
    用 [K]＝Tᵀ[k]T（T＝自由度 → 元素端位移，逆時針／向上為正）。"""
    a = L_ / 2
    k = beam_element_reference().subs(L_, a)
    T = sp.Matrix([[0, 0], [-1, 0], [0, a], [0, -1]])   # (v_b, θ_b, v_c, θ_c) = T (r1, r2)
    K = sp.Matrix(sp.simplify(T.T * k * T))
    K[0, 0] += 4 * EI / L_                              # 柱 ab：b 端轉動勁度
    return sp.simplify(K)


def truss_2013():
    """第 4 章：SA-2013-4（kN、mm）。"""
    EA = 200 * 10000.0
    nodes = {'A': (0, 0), 'B': (14000, 0), 'C': (0, 6000), 'D': (6000, 6000)}
    dof = {('B', 'x'): 0, ('D', 'x'): 1, ('D', 'y'): 2}
    bars = [('A', 'B'), ('A', 'D'), ('C', 'D'), ('B', 'D')]
    K = np.zeros((3, 3)); info = {}
    for i, j in bars:
        (x1, y1), (x2, y2) = nodes[i], nodes[j]
        Ln = math.hypot(x2 - x1, y2 - y1); c, s = (x2 - x1) / Ln, (y2 - y1) / Ln
        kk = EA / Ln
        g = np.array([-c, -s, c, s])
        ids = [dof.get((i, 'x')), dof.get((i, 'y')), dof.get((j, 'x')), dof.get((j, 'y'))]
        for a_, ia in enumerate(ids):
            for b_, ib in enumerate(ids):
                if ia is not None and ib is not None:
                    K[ia, ib] += kk * g[a_] * g[b_]
        info[i + j] = dict(L=Ln, c=c, s=s, k=kk, ids=ids, g=g)
    d = np.array([0.1277, 0.1743, 0.7055])
    Pv = K @ d
    N = {}
    for name, v in info.items():
        u = np.array([0.0 if t is None else d[t] for t in v['ids']])
        N[name] = v['k'] * (v['g'] @ u)
    d_exact = np.linalg.solve(K, [80, 100, 150])
    return dict(K=K, P=Pv, N=N, info=info, d_exact=d_exact)


def fem_by_area():
    """第 5 章：兩端固定 → M/EI 圖總面積＝0（S3）。簡支彎矩圖面積 − 端彎矩 × L ＝ 0。"""
    w, P = sp.symbols('w P', positive=True)
    x = sp.symbols('x')
    A_udl = sp.integrate(w * x * (L_ - x) / 2, (x, 0, L_))
    A_pt = sp.Rational(1, 2) * L_ * P * L_ / 4
    return dict(udl=sp.simplify(A_udl / L_), point=sp.simplify(A_pt / L_),
                A_udl=sp.simplify(A_udl), A_pt=A_pt)


def fem_half_cantilever():
    """第 5 章：中央集中力的另一條路——半跨＝S3 懸臂（尖端鎖轉）。"""
    P = sp.symbols('P', positive=True)
    a = L_ / 2; V = P / 2
    M_tip = sp.solve(sp.Eq(V * a**2 / (2 * EI) + sp.Symbol('M') * a / EI, 0), sp.Symbol('M'))[0]
    return dict(M_mid=sp.simplify(M_tip), M_end=sp.simplify(V * a + M_tip))


def zframe_2018():
    """SA-2018-2：Z 形剛架。自由度 (u, θB, θC)，向右、逆時針為正。"""
    P = sp.symbols('P', positive=True)
    c = EI / L_**3
    K = c * sp.Matrix([[24, -6 * L_, 6 * L_], [-6 * L_, 8 * L_**2, 2 * L_**2], [6 * L_, 2 * L_**2, 8 * L_**2]])
    Pv = sp.Matrix([0, -P * L_ / 8, P * L_ / 8])
    D = sp.simplify(K.inv() * Pv)
    u, tB, tC = D
    M = dict(
        AB=sp.simplify(2 * EI / L_ * tB - 6 * EI / L_**2 * u),
        BA=sp.simplify(4 * EI / L_ * tB - 6 * EI / L_**2 * u),
        BC=sp.simplify(2 * EI / L_ * (2 * tB + tC) + P * L_ / 8),
        CB=sp.simplify(2 * EI / L_ * (2 * tC + tB) - P * L_ / 8),
        CD=sp.simplify(4 * EI / L_ * tC + 6 * EI / L_**2 * u),
        DC=sp.simplify(2 * EI / L_ * tC + 6 * EI / L_**2 * u))
    mid = sp.simplify(P * L_ / 4 - P * L_ / 24)
    return dict(K=K, P=Pv, D=D, M=M, Mmid=mid)


def zframe_numeric():
    """SA-2018-2 獨立驗算：6 自由度 numpy（EA 極大），BC 中點加節點。"""
    Lv, EIv, Pv = 1.0, 1.0, 1.0
    nodes = [(0, 1), (0, 0), (0.5, 0), (1, 0), (1, -1)]   # A, B, M, C, D（B 在原點）
    elems = [(0, 1), (1, 2), (2, 3), (3, 4)]
    K = np.zeros((15, 15))
    for i, j in elems:
        ke = frame_elem_global(*nodes[i], *nodes[j], EIv, 1e9)
        ds = [3 * i + k for k in range(3)] + [3 * j + k for k in range(3)]
        K[np.ix_(ds, ds)] += ke
    free = list(range(3, 12))
    F = np.zeros(15); F[3 * 2 + 1] = -Pv
    d = np.zeros(15); d[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
    return dict(u=d[3], thB=d[5], thC=d[11])


def fabrication_2011():
    """SA-2011-4：AC 短 0.02 m，EA＝1e4 kN；A(3,4)、B(0,4)、C(0,0)、D(6,0)。"""
    EA = 1e4
    A_ = np.array([3.0, 4.0])
    others = {'AB': np.array([0.0, 4.0]), 'AC': np.array([0.0, 0.0]), 'AD': np.array([6.0, 0.0])}
    K = np.zeros((2, 2)); info = {}
    for n, p in others.items():
        v = p - A_; Ln = np.linalg.norm(v); e = v / Ln
        k = EA / Ln
        K += k * np.outer(e, e)
        info[n] = dict(L=Ln, e=e, k=k)
    T0 = info['AC']['k'] * 0.02
    Peq = T0 * info['AC']['e']
    D = np.linalg.solve(K, Peq)
    N = {}
    for n, v in info.items():
        elong = -(v['e'] @ D)               # A 往遠端方向動 → 桿縮短
        N[n] = v['k'] * elong + (T0 if n == 'AC' else 0.0)
    eq = sum(N[n] * info[n]['e'] for n in N)  # 節點 A 合力（拉力把 A 拉向遠端）
    return dict(K=K, T0=T0, Peq=Peq, D=D, N=N, resid=eq)


def settlement_demo():
    """第 5 章：懸臂—滾支梁，右端 B 下陷 δ。自由度 θB；支承位移 v_B＝−δ。"""
    d = sp.symbols('delta', positive=True)
    kb = beam_element_reference()                 # (v1, θ1, v2, θ2)
    Kff = kb[3, 3]; Kfs = kb[3, 2]
    Pf = -Kfs * (-d)
    thB = sp.simplify(Pf / Kff)
    MA = sp.simplify(kb[1, 2] * (-d) + kb[1, 3] * thB)
    MB = sp.simplify(kb[3, 2] * (-d) + kb[3, 3] * thB)
    return dict(Kff=Kff, Kfs=Kfs, Pf=sp.simplify(Pf), thB=thB, MA=MA, MB=MB)


def condensation_general():
    """第 6 章：2×2 靜態凝縮的符號式（與 Kaa − Kab Kbb⁻¹ Kba 對照）。"""
    a, b, c = sp.symbols('a b c')
    K = sp.Matrix([[a, b], [b, c]])
    return sp.simplify(condense(K, [0], [1]))


def portal_limits():
    """第 6 章：梁柱勁度比 ρ＝(EI_b/L_b)/(EI_c/L_c) 對側向勁度的影響（柱 EI、L 固定）。"""
    rho = sp.symbols('rho', nonnegative=True)
    # 反對稱：θ 方程 (4 + 6ρ)θ + 6Δ/L = 0 → k = 24 − 2·6·6/(4+6ρ)
    k = sp.simplify(24 - 72 / (4 + 6 * rho))
    return dict(k=k, k0=k.subs(rho, 0), k1=k.subs(rho, 1), kinf=sp.limit(k, rho, sp.oo))


def pushover_2024():
    """SA-2024-4：柱 2EI、高 2L；梁 EI、長 L；EI＝425000 kN·m²、L＝7 m。"""
    EIv, Lv = 425000.0, 7.0
    u = EIv / Lv**3
    # 柱元素 (Δ, θ頂)：12(2EI)/(2L)³＝3EI/L³、6(2EI)/(2L)²＝3EI/L²、4(2EI)/(2L)＝4EI/L
    def K_of(beam_on):
        kb = 1.0 if beam_on else 0.0
        return np.array([[6, 3, 3], [3, 4 + 4 * kb, 2 * kb], [3, 2 * kb, 4 + 4 * kb]], float)  # ×EI/L³，θ 已乘 L
    out = {}
    K1 = K_of(True)
    k1 = 1 / np.linalg.inv(K1)[0, 0]
    K2 = K_of(False)
    k2 = 1 / np.linalg.inv(K2)[0, 0]
    # 彈性階段單位 P 的彎矩
    d = np.linalg.solve(K1 * u, [1, 0, 0])
    Dl, th = d[0], d[1] / Lv
    M_base = 2 * EIv / Lv * th + 3 * EIv / Lv**2 * Dl
    M_top = 4 * EIv / Lv * th + 3 * EIv / Lv**2 * Dl
    M_beam = 6 * EIv / Lv * th
    P1 = 300 / abs(M_beam)
    D1 = P1 / (k1 * u)
    Mb1 = M_base * P1
    d2 = np.linalg.solve(K2 * u, [1, 0, 0])
    Mb_inc = 2 * EIv / Lv * d2[1] / Lv + 3 * EIv / Lv**2 * d2[0]
    Mt_inc = 4 * EIv / Lv * d2[1] / Lv + 3 * EIv / Lv**2 * d2[0]
    dP2 = (580 - Mb1) / Mb_inc
    D2 = D1 + dP2 / (k2 * u)
    Pu_mech = (2 * 580 + 2 * 300) / 14
    return dict(u=u, k1=k1, k2=k2, kt1=k1 * u, kt2=k2 * u, th_ratio1=th * Lv / Dl,
                M_base=M_base, M_top=M_top, M_beam=M_beam, P1=P1, D1=D1, Mb1=Mb1, Mt1=M_top * P1,
                Mb_inc=Mb_inc, Mt_inc=Mt_inc, dP2=dP2, P2=P1 + dP2, D2=D2, Pu_mech=Pu_mech)


def semirigid_2019():
    """SA-2019-4：(d1, d2, d3, d4)＝(Δ, θB柱, θB梁, θD)；kr＝10EI/L。"""
    P, Q, w, R, kr = sp.symbols('P Q w R k_r', positive=True)
    c = EI / L_**3
    K = c * sp.Matrix([[15, 6 * L_, 0, 3 * L_], [6 * L_, 14 * L_**2, -10 * L_**2, 0],
                       [0, -10 * L_**2, 14 * L_**2, 2 * L_**2], [3 * L_, 0, 2 * L_**2, 10 * L_**2]])
    # 逐元素組裝（獨立驗算）
    Ka = sp.zeros(4, 4)
    def add(m, ids):
        for i, a in enumerate(ids):
            for j, b in enumerate(ids):
                Ka[a, b] += m[i, j]
    add(sp.Matrix([[12 * c, 6 * EI / L_**2], [6 * EI / L_**2, 4 * EI / L_]]), [0, 1])        # 柱 AB
    add(sp.Matrix([[3 * c, 3 * EI / L_**2], [3 * EI / L_**2, 3 * EI / L_]]), [0, 3])         # 柱 CD（C 鉸）
    add(10 * EI / L_ * sp.Matrix([[1, -1], [-1, 1]]), [1, 2])                                 # 旋轉彈簧
    add(EI / L_ * sp.Matrix([[4, 2], [2, 4]]), [2, 3])                                        # 梁 BD
    add(sp.Matrix([[3 * EI / L_]]), [3])                                                      # 梁 DE（E 滾）
    Pv = sp.Matrix([R + P / 2 + sp.Rational(11, 16) * Q, P * L_ / 8, 0, sp.Rational(3, 16) * Q * L_ - w * L_**2 / 8])
    # 柱 CD 中點 Q（C 鉸、D 固定）的固端力：由 propped cantilever 公式驗算
    # 柱 CD 凝縮自 4×4：底端轉角放掉
    kb = beam_element_reference()
    kc = condense(kb.extract([1, 2, 3], [1, 2, 3]), [1, 2], [0])   # (v頂, θ頂) 底鉸
    # 彈簧極限
    Kg = K.subs(EI, EI)
    return dict(K=K, same=sp.simplify(K - Ka) == sp.zeros(4, 4), P=Pv, kc_pinned=sp.simplify(kc))


def torsion_spring_2015():
    """SA-2015-4：(r1, r2, r3)＝(θB1, vB2 向下, θB2)，順時針為正。"""
    kt = sp.symbols('k_theta', positive=True)
    w, P = sp.symbols('w P', positive=True)
    K = sp.Matrix([[8 * EI / L_ + kt, 0, -kt], [0, 12 * EI / L_**3, 6 * EI / L_**2], [-kt, 6 * EI / L_**2, 4 * EI / L_ + kt]])
    R = sp.Matrix([-w * L_**2 / 12, P / 2, P * L_ / 8])
    lim0 = sp.simplify(K.subs(kt, 0))
    return dict(K=K, R=R, K_kt0=lim0)


def grid_2025():
    """SA-2025-4：格床（實心圓桿 J＝2I），以 6 自由度完整矩陣數值驗算對稱解。"""
    E_v, G_v, I_v, L_v, w_v = 1.0, 0.4, 1.0, 1.0, 1.0
    J_v = 2 * I_v
    # 格床元素：局部 (w, θx', θy') 兩端；x' 沿桿軸。扭轉繞 x'、彎曲繞 y'（撓度 w 向下為正→這裡改向上為正）
    def grid_elem(x1, y1, x2, y2):
        Ln = math.hypot(x2 - x1, y2 - y1); c, s = (x2 - x1) / Ln, (y2 - y1) / Ln
        a = G_v * J_v / Ln; b = E_v * I_v / Ln**3
        # 自由度順序 (w, θ_t, θ_b)：θ_t 繞桿軸、θ_b 繞桿軸的垂直水平軸（右手）
        kl = np.zeros((6, 6))
        kl[np.ix_([1, 4], [1, 4])] = a * np.array([[1, -1], [-1, 1]])
        # 撓度 w（+z）與繞 y' 的轉角 θ_b：dw/dx' = −θ_b
        bb = np.array([[12, -6 * Ln, -12, -6 * Ln], [-6 * Ln, 4 * Ln**2, 6 * Ln, 2 * Ln**2],
                       [-12, 6 * Ln, 12, 6 * Ln], [-6 * Ln, 2 * Ln**2, 6 * Ln, 4 * Ln**2]]) * b
        idx = [0, 2, 3, 5]
        kl[np.ix_(idx, idx)] = bb
        T = np.zeros((6, 6))
        for i in (0, 3):
            T[i, i] = 1
            T[i + 1:i + 3, i + 1:i + 3] = [[c, s], [-s, c]]
        return T.T @ kl @ T
    nodes = {'d': (0, 0), 'a': (L_v, 0), 'b': (L_v, L_v), 'c': (0, L_v)}
    order = ['a', 'b', 'c', 'd']
    K = np.zeros((12, 12))
    for i, j in [('a', 'b'), ('b', 'c'), ('c', 'd')]:
        ke = grid_elem(*nodes[i], *nodes[j])
        ds = [3 * order.index(i) + k for k in range(3)] + [3 * order.index(j) + k for k in range(3)]
        K[np.ix_(ds, ds)] += ke
    # bc 均布 w 向下（−z）：鎖住時兩端剪力各 wL/2 向上、彎矩 wL²/12；等效節點載重＝反號
    # bc 沿 −x 方向（b→c），彎曲轉角繞 y 軸。以「固端力向量」在局部組再轉換
    Ln = L_v
    f_local = np.array([w_v * Ln / 2, 0, -w_v * Ln**2 / 12, w_v * Ln / 2, 0, w_v * Ln**2 / 12])  # 固端力（局部，支承對桿）
    # 檢查符號：用 w 向下時固端剪力向上 (+z)。彎矩符號依 bb 的約定：θ_b 正 → dw/dx' 負
    c, s = -1.0, 0.0
    T = np.zeros((6, 6))
    for i in (0, 3):
        T[i, i] = 1; T[i + 1:i + 3, i + 1:i + 3] = [[c, s], [-s, c]]
    f_g = T.T @ f_local
    F = np.zeros(12)
    for k_, n in enumerate(['b', 'c']):
        F[3 * order.index(n):3 * order.index(n) + 3] -= f_g[3 * k_:3 * k_ + 3]
    free = [3, 4, 5, 6, 7, 8]
    d = np.linalg.solve(K[np.ix_(free, free)], F[free])
    wb, txb, tyb, wc, txc, tyc = d
    ref = dict(wb=-w_v * L_v**4 / (6 * E_v * I_v), txb=w_v * L_v**3 / (24 * I_v * (E_v + G_v)),
               tyb=w_v * L_v**3 / (4 * E_v * I_v))
    return dict(d=d, ref=ref)


def grid_symbolic():
    """SA-2025-4：手算三條方程（對稱降為 3 個未知數）。w_b 向下為正。"""
    E, G, I, w = sp.symbols('E G I omega', positive=True)
    J = 2 * I
    thx, thy, wb = sp.symbols('theta_x theta_y w_b')
    e1 = sp.Eq((G * J / L_ + 2 * E * I / L_) * thx, w * L_**2 / 12)
    e2 = sp.Eq(4 * E * I / L_ * thy - 6 * E * I / L_**2 * wb, 0)
    e3 = sp.Eq(12 * E * I / L_**3 * wb - 6 * E * I / L_**2 * thy, w * L_ / 2)
    s = sp.solve([e1, e2, e3], [thx, thy, wb])
    Mxa = sp.simplify(G * J / L_ * s[thx])
    Mya = sp.simplify(6 * E * I / L_**2 * s[wb] - 2 * E * I / L_ * s[thy])
    return dict(sol={k: sp.simplify(v) for k, v in s.items()}, Mxa=Mxa, Mya=Mya, Rza=w * L_ / 2)

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

    print('\n══════ 第 3～8 章 ══════')
    print('自由度盤點', dof_count())
    pp = portal_partition()
    print('門型 每單位Δ：柱頂水平力', pp['V_col'], ' 柱底彎矩', pp['M_base'], ' 柱頂彎矩', pp['M_top'], ' 兩柱合計', pp['base_shear_sum'])
    print('SA-2012-4 剛桿 [K]（順時針為正）='); sp.pprint(rigid_bar_2012())
    t = truss_2013()
    print('SA-2013-4 [K] kN/mm =\n', np.round(t['K'], 3))
    print('  P =', np.round(t['P'], 2), '  反解 d(80,100,150) =', np.round(t['d_exact'], 4))
    for n, v in t['info'].items():
        print('  ', n, 'L=%.1f c=%.4f s=%.4f k=%.3f N=%.2f' % (v['L'], v['c'], v['s'], v['k'], t['N'][n]))
    print('固端彎矩（面積法）', fem_by_area())
    print('固端彎矩（半跨懸臂）', fem_half_cantilever())
    z = zframe_2018()
    print('SA-2018-2 D =', list(z['D']), ' M =', z['M'], ' 跨中', z['Mmid'])
    zn = zframe_numeric()
    print('  numpy 驗算 u·EI/PL³=%.6f(−1/48=%.6f) θB=%.6f(−1/24=%.6f) θC=%.6f' % (zn['u'], -1/48, zn['thB'], -1/24, zn['thC']))
    print('支承沉陷示範', settlement_demo())
    fb = fabrication_2011()
    print('SA-2011-4 K =', np.round(fb['K'], 2), ' T0 =', fb['T0'], ' Peq =', fb['Peq'], ' D =', np.round(fb['D'], 6))
    print('  N =', {k: round(v, 2) for k, v in fb['N'].items()}, ' 節點合力殘差', np.round(fb['resid'], 9))
    print('凝縮 2×2 一般式', condensation_general())
    print('門型 勁度比', portal_limits())
    po = pushover_2024()
    print('SA-2024-4', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in po.items()})
    sr = semirigid_2019()
    print('SA-2019-4 [K] 逐元素組裝相同？', sr['same']); sp.pprint(sr['K']); print('  {P} =', list(sr['P']))
    print('  底鉸柱凝縮 (v頂, θ頂)：'); sp.pprint(sr['kc_pinned'])
    ts = torsion_spring_2015()
    print('SA-2015-4 [K]：'); sp.pprint(ts['K']); print('  {R} =', list(ts['R']))
    g = grid_symbolic()
    print('SA-2025-4 手算', g)
    gn = grid_2025()
    print('  numpy 6 自由度：', np.round(gn['d'], 6), ' 參考', gn['ref'])
