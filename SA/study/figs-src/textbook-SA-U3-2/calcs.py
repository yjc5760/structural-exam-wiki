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



# ───────── 第 3 章：牆–構架互制（S6）─────────
def wall_flex(n, EI=1.0):
    """貫通全高的牆＝懸臂撓曲梁。樓層高度 1..n（以層高為單位）。
    柔度 f_ab＝a²(3b−a)/(6EI)（a≤b，b 處受單位力時 a 處的撓度；由 S1 加上 b 點以上的直線延伸推得）。"""
    z = np.arange(1, n + 1, dtype=float)
    return np.array([[min(a, b) ** 2 * (3 * max(a, b) - min(a, b)) / (6 * EI) for b in z] for a in z])


def shear_K(n, k=1.0):
    """各層勁度都是 k 的剪力建築（自由度由下往上 1..n）。"""
    return shear_building([(i, i + 1, k) for i in range(n)], n)


N18 = 8


def ex2018(EI=5 / 12, k=1.0):
    """SA-2018-1 示意數值模型（與題解 §4 相同）：牆＝8 層懸臂撓曲梁、構架＝剪力型樓層彈簧 k、
    連桿不伸縮 ⇒ 同層同位移；「牆勁度為構架 5 倍」取 12EI/h³＝5k（h＝1）。各層外力 F＝1。"""
    Kw = np.linalg.inv(wall_flex(N18, EI))
    Kf = shear_K(N18, k)
    F = np.ones(N18)
    u = np.linalg.solve(Kw + Kf, F)
    Ff, Fw = Kf @ u, Kw @ u
    u_f = np.linalg.solve(Kf, F)                 # 構架單獨
    u_w = wall_flex(N18, EI) @ F                 # 牆單獨
    Vf = np.cumsum(Ff[::-1])[::-1]               # 構架的層剪力（S3，由上往下累加）
    Vw = np.cumsum(Fw[::-1])[::-1]
    return dict(u=u, Ff=Ff, Fw=Fw, u_f=u_f, u_w=u_w, Vf=Vf, Vw=Vw,
                base_share_wall=Vw[0] / N18)


def ex2018_alt():
    """另一種「5 倍」換算（3EI/h³＝5k），題解 §4 示意數值的第二組。"""
    return ex2018(EI=5 / 3)


def ex2020_more():
    r = ex2020()
    D_wall_alone = np.linalg.solve(Kw20, P20v)
    col_sum = Kw20.sum(axis=0) / 30000          # 每一行相加（÷30000）
    colf_sum = Kf20.sum(axis=0) / 30000
    # 連桿力：牆在頂層、一樓分到的力；連桿 bc（頂層）、ef（一樓），構架推牆＝壓
    return dict(D_wall_alone=D_wall_alone, Kw_colsum=col_sum, Kf_colsum=colf_sum,
                bc=r['Fw'][0], ef=r['Fw'][1], base_wall=r['base_wall'], base_total=r['base_wall'] + r['base_frame'])


# ───────── 第 4 章：剛性樓板扭轉（SA-2021-4）─────────
EId21, EIe21, h21, Fcol21 = 9720.0, 48600.0, 3.6, 27.0
cols21 = {'C1': (-3.0, -2.0, 'd'), 'C2': (3.0, -2.0, 'e'), 'C3': (-3.0, 2.0, 'd'), 'C4': (3.0, 2.0, 'e')}


def ex2021():
    kd, ke = kc(EId21, h21), kc(EIe21, h21)
    kk = {n: (kd if t == 'd' else ke) for n, (x, y, t) in cols21.items()}
    Ky = sum(kk.values()); Kx = Ky
    xr = sum(kk[n] * cols21[n][0] for n in kk) / Ky
    yr = sum(kk[n] * cols21[n][1] for n in kk) / Kx
    Fy = 4 * Fcol21
    xF = 0.0                                          # 四個力對稱，合力在幾何中心
    Mt = Fy * (xF - xr)                               # 對剛心的扭矩（逆時針為正）
    rel = {n: (cols21[n][0] - xr, cols21[n][1] - yr) for n in kk}
    Kth_x = sum(kk[n] * rel[n][1] ** 2 for n in kk)    # x 向柱的貢獻 Σk y'²
    Kth_y = sum(kk[n] * rel[n][0] ** 2 for n in kk)    # y 向柱的貢獻 Σk x'²
    Kth = Kth_x + Kth_y
    dy, dx = Fy / Ky, 0.0
    th = Mt / Kth
    disp = {n: (dx - th * rel[n][1], dy + th * rel[n][0]) for n in kk}
    shear = {n: (kk[n] * disp[n][0], kk[n] * disp[n][1]) for n in kk}
    # 第二條路：以幾何中心為參考點的 3×3 勁度矩陣 [u, v, θ]
    K = np.zeros((3, 3))
    for n, (x, y, t) in cols21.items():
        k = kk[n]
        a = np.array([[1, 0, -y], [0, 1, x]])        # 柱位移 = a @ [u, v, θ]
        K += k * a.T @ a
    sol = np.linalg.solve(K, np.array([0.0, Fy, sum(cols21[n][0] * Fcol21 for n in cols21)]))
    disp2 = {n: (sol[0] - sol[2] * y, sol[1] + sol[2] * x) for n, (x, y, t) in cols21.items()}
    # 平衡檢查
    sVx = sum(v[0] for v in shear.values()); sVy = sum(v[1] for v in shear.values())
    sM0 = sum(cols21[n][0] * shear[n][1] - cols21[n][1] * shear[n][0] for n in kk)  # 柱力對原點（逆時針）
    # 若誤把 x'、y' 量到幾何中心
    Kth_wrong = sum(kk[n] * (cols21[n][0] ** 2 + cols21[n][1] ** 2) for n in kk)
    # 若漏掉 x 向柱的扭轉貢獻
    th_noX = Mt / Kth_y
    return dict(kd=kd, ke=ke, Ky=Ky, xr=xr, yr=yr, Fy=Fy, Mt=Mt, rel=rel, Kth_x=Kth_x, Kth_y=Kth_y, Kth=Kth,
                dy=dy, th=th, disp=disp, shear=shear, K3=K, sol3=sol, disp2=disp2,
                sVx=sVx, sVy=sVy, sM0=sM0, M_ext0=sum(cols21[n][0] * Fcol21 for n in cols21),
                Kth_wrong=Kth_wrong, th_noX=th_noX)


# ───────── 第 5 章：范倫迪爾桁架（SA-2019-2）─────────
Lp19, h19, P19, NP19 = 4.0, 6.0, 100.0, 4      # 格間寬、高、載重（B、C、D 向下）


def ex2019():
    """反曲點在每根桿中點的近似分析。下弦 A..E、上弦 F..J；格間 i＝1..4。
    正負號：軸力拉為正；弦桿剪力 V 取「與整體剪力同向」為正（左段向上）。"""
    xs = np.arange(NP19 + 1) * Lp19                 # 節點 x：0,4,8,12,16
    loads = np.array([0, P19, P19, P19, 0])        # 下弦節點向下載重
    R = loads.sum() / 2                            # 對稱：A、E 各 150
    xm = (xs[:-1] + xs[1:]) / 2                    # 格間中點
    Vg = np.array([R - loads[1:i + 1].sum() for i in range(NP19)])            # 整體剪力
    Mg = np.array([R * x - sum(loads[j] * (x - xs[j]) for j in range(NP19 + 1) if xs[j] < x) for x in xm])
    Ntop, Nbot = -Mg / h19, Mg / h19
    # 節點平衡（上弦節點 F..J，切到相鄰桿中點）
    Vv = np.zeros(NP19 + 1)                         # 腹桿剪力（上端節點受力的方向：向右為正）
    Vtop = np.zeros(NP19)
    Nlist = np.concatenate([[0.0], Ntop, [0.0]])
    for j in range(NP19 + 1):
        Vv[j] = -(Nlist[j + 1] - Nlist[j])           # ΣFx：腹桿剪力＝弦桿軸力差
    # ΣM 於上弦節點：左弦剪力×L/2 ＋ 右弦剪力×L/2 ＝ 腹桿剪力×h/2
    Vtop[0] = Vv[0] * (h19 / 2) / (Lp19 / 2)
    for j in range(1, NP19):
        Vtop[j] = Vv[j] * (h19 / 2) / (Lp19 / 2) - Vtop[j - 1]
    Vbot = Vg - Vtop
    # ΣFy 於上弦節點（無外力）：腹桿軸力＝左弦剪力 − 右弦剪力
    Vt_ext = np.concatenate([[0.0], Vtop, [0.0]])
    Nv = np.array([Vt_ext[j] - Vt_ext[j + 1] for j in range(NP19 + 1)])
    # 第二條路：下弦節點 ΣFy 檢查（腹桿拉力向上＋弦桿剪力差 − 載重 ＝ 0）
    Vb_ext = np.concatenate([[0.0], Vbot, [0.0]])
    Rv = np.array([R, 0, 0, 0, R])
    botFy = np.array([Nv[j] + Vb_ext[j] - Vb_ext[j + 1] - loads[j] + Rv[j] for j in range(NP19 + 1)])
    Mchord = Vtop * Lp19 / 2
    Mvert = np.abs(Vv) * h19 / 2
    return dict(R=R, xm=xm, Vg=Vg, Mg=Mg, Ntop=Ntop, Nbot=Nbot, Vv=Vv, Vtop=Vtop, Vbot=Vbot, Nv=Nv,
                botFy=botFy, Mchord=Mchord, Mvert=Mvert)


# ───────── 第 6 章：偏心斜撐連梁轉角（SA-2023-4）─────────
def ebf_kinematics(theta, L1=L1_23, e=e23, L2=L2_23, h=h23):
    """第二條路：真的把兩個剛性三角形繞各自的底角轉 θ（順時針，向右側移），
    求連梁兩端的新位置與端點切線，量出連梁相對兩端的轉角（不用小角度公式）。"""
    c, s = np.cos(-theta), np.sin(-theta)
    Rm = np.array([[c, -s], [s, c]])
    pL = Rm @ np.array([L1, h])                          # 左三角繞 (0,0)
    pR = np.array([L1 + e + L2, 0]) + Rm @ np.array([-L2, h])   # 右三角繞 (L,0)
    chord = np.arctan2(pR[1] - pL[1], pR[0] - pL[0])    # 弦的角度（逆時針為正）
    end_tan = -theta                                      # 兩端切線跟著三角形轉
    return dict(pL=pL, pR=pR, chord=chord, gamma=chord - end_tan)


def ex2023_more():
    r = ex2023()
    g_even = r['L'] / e23 * r['D_even'] / h23
    g_noTheta = (L1_23 + L2_23) / e23 * r['theta']
    g_exact = np.array([ebf_kinematics(t)['gamma'] for t in r['theta']])
    return dict(g_even=g_even, g_noTheta=g_noTheta, g_exact=g_exact, deg=np.degrees(r['gamma']),
                amp_chord=(L1_23 + L2_23) / e23)

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

    print('=== 第 3 章 SA-2018-1 示意模型（12EI/h³ = 5k）===')
    r = ex2018()
    print('  構架 F：', np.round(r['Ff'], 2), '\n  牆 F：', np.round(r['Fw'], 2))
    print('  構架層剪力：', np.round(r['Vf'], 2), '\n  牆層剪力：', np.round(r['Vw'], 2))
    print('  構架單獨 u（以頂層=1）：', np.round(r['u_f'] / r['u_f'][-1], 3))
    print('  牆單獨 u（以頂層=1）：', np.round(r['u_w'] / r['u_w'][-1], 3))
    print('  合體 u（以頂層=1）：', np.round(r['u'] / r['u'][-1], 3), ' 牆分擔基底剪力', round(r['base_share_wall'], 3))
    r = ex2018_alt()
    print('  (3EI/h³ = 5k) 構架 F：', np.round(r['Ff'], 2), ' 牆底剪力分擔', round(r['base_share_wall'], 3))
    print('=== 第 3 章 SA-2020-4 補充 ===')
    for kk, v in ex2020_more().items():
        print(' ', kk, v)
    print('=== 第 4 章 SA-2021-4 ===')
    r = ex2021()
    for kk in ('kd', 'ke', 'Ky', 'xr', 'yr', 'Fy', 'Mt', 'Kth_x', 'Kth_y', 'Kth', 'dy', 'th', 'sVx', 'sVy', 'sM0', 'M_ext0', 'Kth_wrong', 'th_noX'):
        print(' ', kk, r[kk])
    for n in r['disp']:
        print(f'  {n} rel={r["rel"][n]}  u,v(mm)={np.round(np.array(r["disp"][n]) * 1000, 3)}  V(kN)={np.round(r["shear"][n], 3)}  3x3 路徑 u,v(mm)={np.round(np.array(r["disp2"][n]) * 1000, 3)}')
    print('  3x3 解 [u,v,θ] =', r['sol3'])
    print('=== 第 5 章 SA-2019-2 ===')
    r = ex2019()
    for kk, v in r.items():
        print(' ', kk, np.round(v, 3))
    print('=== 第 6 章 SA-2023-4 補充 ===')
    for kk, v in ex2023_more().items():
        print(' ', kk, np.round(v, 5))
