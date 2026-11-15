# -*- coding: utf-8 -*-
"""SA-U3-2 建築結構系統分析｜教科書講義的所有數值（圖與內文共用，先算再寫）。

正負號約定（全書統一）：
  * 水平位移、水平力：向右為正。
  * 轉角、扭矩：逆時針為正（第 4、6 章才用到）。
規則：
  * 講義內文、圖、範例出現的每一個數字都要能在這裡找到來源。
  * 考題數字取自 raw/solutions/SA-YYYY-N/SA-YYYY-N.md（勘誤後版本，2026-11-07／11-08）。
  * 執行 `python3 calcs.py`，把印出的數字和內文逐一對照。
"""
import numpy as np
import sympy as sp

# ───────── 第 1 章：柱彈簧 ─────────
E_, I_, h_, V_ = sp.symbols('E I h V', positive=True)
EI_ = E_ * I_


def cantilever_tip(Vs, l):
    """種子 S1：懸臂自由端受 V 的撓度 V l^3 / 3EI（由 v''=M/EI 積分，見 U2-4 第 2 章）。"""
    x = sp.symbols('x')
    M = Vs * (l - x)
    th = sp.integrate(M / EI_, (x, 0, x))
    v = sp.integrate(th, (x, 0, x))
    return sp.simplify(v.subs(x, l))


def col_fixed_fixed():
    """兩端不轉的柱：反曲點在中點（S5）→ 上下兩支長 h/2 的懸臂串聯（S2）。"""
    half = cantilever_tip(V_, h_ / 2)
    Delta = sp.simplify(2 * half)
    k = sp.simplify(V_ / Delta)
    M_end = V_ * h_ / 2
    M_in_Delta = sp.simplify(M_end.subs(V_, k * sp.Symbol('Delta')))
    return Delta, k, M_end, M_in_Delta


def col_pinned_base():
    """柱底鉸接、柱頂不轉：整根是一支長 h 的懸臂（反曲點跑到鉸那裡）。"""
    Delta = cantilever_tip(V_, h_)
    return sp.simplify(V_ / Delta)


def ff_shape(xi):
    """兩端不轉的柱，單位側移的變形形狀 3ξ²−2ξ³（ξ＝高度／h）。"""
    return 3 * xi ** 2 - 2 * xi ** 3


def ff_moment(xi):
    """對應的彎矩分布（以 6EIΔ/h² 為 1）：1−2ξ（底端 +1、頂端 −1、中點 0）。"""
    return 1 - 2 * xi


def kc(EI, h):
    return 12 * EI / h ** 3


# ───────── SA-2020-4（第 1～3 章貫穿範例）─────────
EI20, h20, P20 = 81920.0, 3.2, 60.0
k20 = kc(EI20, h20)                       # 30000 kN/m
K20_story = 2 * k20                       # 每層兩根柱
Kf20 = np.array([[K20_story, -K20_story], [-K20_story, 2 * K20_story]])   # 自由度：頂層、一樓
Kw20 = 30000.0 * np.array([[1, -2], [-2, 6]])
P20v = np.array([P20, P20])


def ex2020():
    D_frame_alone = np.linalg.solve(Kf20, P20v)          # 只有構架
    K = Kf20 + Kw20
    D = np.linalg.solve(K, P20v)
    Fw = Kw20 @ D                                       # 牆在各層分到的力＝連桿力
    Ff = Kf20 @ D
    V_eh = k20 * D[1]
    M_eh = 6 * EI20 * D[1] / h20 ** 2
    return dict(D_frame_alone=D_frame_alone, K=K, D=D, Fw=Fw, Ff=Ff, V_eh=V_eh, M_eh=M_eh,
                M_eh_Vh2=V_eh * h20 / 2, base_wall=Fw.sum(), base_frame=2 * V_eh)


# ───────── 剪力建築的一般組裝（S1 推一下 + S2 並聯）─────────
def shear_building(cols, n):
    """cols = [(下端樓層, 上端樓層, k)]，樓層 0＝地面。以 S1「推第 j 層一單位」量出 [K]（自由度 1..n）。"""
    K = np.zeros((n, n))
    for lo, hi, k in cols:
        for a in (lo, hi):
            for b in (lo, hi):
                if a == 0 or b == 0:
                    continue
                K[a - 1, b - 1] += k if a == b else -k
    return K


# ───────── SA-2022-4（第 2 章範例）─────────
EI22, h22 = 97200.0, 3.6
k22 = kc(EI22, h22)                       # 25000
k22_tall = kc(EI22, 2 * h22)              # 3125 = k/8
F22 = np.array([100.0, 200.0, 300.0])     # b、c、d（一、二、三樓）


def ex2022():
    cols = [(0, 1, k22), (0, 1, k22),               # a、e 柱：地面→一樓
            (1, 2, k22), (1, 2, k22),               # 一樓→二樓
            (0, 2, k22_tall), (0, 2, k22_tall),     # m、n 挑高柱：地面→二樓
            (2, 3, k22), (2, 3, k22), (2, 3, k22), (2, 3, k22)]
    K = shear_building(cols, 3)
    D = np.linalg.solve(K, F22)
    V_story = np.array([F22.sum(), F22[1:].sum(), F22[2]])   # 切面以上外力
    Ha = k22 * D[0]
    Ma = Ha * h22 / 2
    Hm = k22_tall * D[1]
    Mm = Hm * 2 * h22 / 2
    # 錯解：以為 m、n 每層都有梁（四根 3.6 m 柱每層）
    cols_wrong = [(i, i + 1, k22) for i in range(3) for _ in range(4)]
    D_wrong = np.linalg.solve(shear_building(cols_wrong, 3), F22)
    return dict(K=K, D=D, V_story=V_story, Ha=Ha, Ma=Ma, Hm=Hm, Mm=Mm,
                base_sum=2 * Ha + 2 * Hm, D_wrong=D_wrong)


# ───────── SA-2023-4（第 2 章層剪力、第 6 章 γ）─────────
F23 = np.array([600.0, 900.0, 1200.0])    # 一、二、三層（樓板兩端相加）
roof23, h23, e23, L1_23, L2_23 = 0.06, 4.0, 0.6, 4.0, 4.0


def ex2023():
    V = np.array([F23.sum(), F23[1:].sum(), F23[2]])
    D = roof23 * V / V.sum()
    th = D / h23
    L = L1_23 + e23 + L2_23
    g = L / e23 * th
    return dict(V=V, ratio=V / 300, D=D, theta=th, L=L, amp=L / e23, gamma=g,
                D_even=np.full(3, roof23 / 3))


if __name__ == '__main__':
    np.set_printoptions(precision=6, suppress=True)
    D, k, M, MD = col_fixed_fixed()
    print('=== 第 1 章 柱彈簧 ===')
    print('懸臂端撓度 S1:', cantilever_tip(V_, h_))
    print('兩端不轉 Δ =', D, '  k =', k, '  M_end =', M, '=', MD)
    print('柱底鉸接 k =', col_pinned_base(), '  比值 =', sp.simplify(k / col_pinned_base()))
    print('2020-4 k =', k20, '  每層 K =', K20_story, '  誤用 3EI/h³ =', 3 * EI20 / h20 ** 3)
    print('h 加 10%：k 乘', 1.1 ** -3, '；EI 加倍：k 乘 2')
    print('懸臂 h/2 尖端撓度 =', cantilever_tip(V_, h_ / 2))
    print('2022-4 k =', k22, '  挑高 k =', k22_tall, ' 比 =', k22 / k22_tall)
    r = ex2020()
    print('=== SA-2020-4 ===')
    for kk, v in r.items():
        print(' ', kk, v)
    print('  Δ(mm) =', r['D'] * 1000, '  構架單獨 Δ(mm) =', r['D_frame_alone'] * 1000)
    r = ex2022()
    print('=== SA-2022-4 ===')
    for kk, v in r.items():
        print(' ', kk, v)
    print('  Δ(mm) =', r['D'] * 1000, ' 錯解 Δ(mm)=', r['D_wrong'] * 1000)
    r = ex2023()
    print('=== SA-2023-4 ===')
    for kk, v in r.items():
        print(' ', kk, v)
    print('  Δ(cm) =', r['D'] * 100)
