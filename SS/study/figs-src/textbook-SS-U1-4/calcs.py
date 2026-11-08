# -*- coding: utf-8 -*-
"""SS-U1-4 接合之分析與設計：教科書講義的所有數值（圖與內文共用，先算再寫）。

單位：題目用什麼就用什麼。SS-2012-4 用 N、mm、MPa；其餘用 tf、cm、tf/cm²。
規則：
  * 講義內文、圖、範例出現的每一個數字都要能在這裡找到來源。
  * 考題數字取自 raw/solutions/SS-YYYY-N/SS-YYYY-N.md（2026-11-01 勘誤後版本）。
  * 寫完執行 `python3 calcs.py`，把印出的數字和內文逐一對照。
"""
import math

KSI = 0.07031          # 1 ksi = 0.07031 tf/cm²

# ------------------------------------------------------------------ φ 與 Ω
PHI = {                 # LRFD 強度折減係數（台灣鋼結構極限設計法規範）
    'GSY 全斷面降伏': 0.90,
    '剪力降伏（接合板）': 0.90,
    'CJP 開槽銲（同母材）': 0.90,
    'PJP 開槽銲': 0.80,
    '螺栓剪斷': 0.75,
    '孔壁承壓': 0.75,
    'NSF 淨斷面斷裂': 0.75,
    '剪力斷裂（接合板）': 0.75,
    '塊狀剪力': 0.75,
    '填角銲（銲喉剪斷）': 0.75,
    '摩阻型滑動（標準孔）': 1.00,
}


def omega(phi):
    """ASD 安全係數 Ω = 1.5/φ（1.2D+1.6L ≈ 1.5(D+L)）。"""
    return 1.5 / phi


# ------------------------------------------------------------------ 0.6 與 1/√3
def shear_ratio():
    return dict(inv_sqrt3=1 / math.sqrt(3))


# ------------------------------------------------------------------ 螺栓材料（A325）
def bolt_A325():
    d = {}
    d['Fu_ksi'] = 120.0
    d['Fu'] = 8.4                   # tf/cm²（台灣規範表值取 8.4；120 ksi = 8.44）
    d['Fnv_X'] = 0.50 * d['Fu']     # 螺紋不在剪力面：0.5Fu = 4.20
    d['Fnv_N'] = 0.40 * d['Fu']     # 螺紋在剪力面：0.4Fu = 3.36
    d['Fnt'] = 0.75 * d['Fu']       # 純拉：0.75Fu = 6.30
    d['phiFnv_X'] = 0.75 * d['Fnv_X']
    d['phiFnv_N'] = 0.75 * d['Fnv_N']
    # ASD：LRFD 推算值 φFnv/1.5 對照考卷表值（SS-2002-4 附表）
    d['asd_X_from_lrfd'] = d['phiFnv_X'] / 1.5      # 2.10
    d['asd_N_from_lrfd'] = d['phiFnv_N'] / 1.5      # 1.68
    d['asd_X_table'] = 2.10
    d['asd_N_table'] = 1.45
    d['asd_N_ratio'] = d['asd_N_table'] / d['asd_N_from_lrfd']
    # 由 0.6Fu 出發的分解：0.6 × (長接頭不均勻 ≈ 0.83) = 0.5；再 × 螺紋 0.8 = 0.4
    d['k_long'] = 0.50 / 0.60
    d['k_thread'] = 0.40 / 0.50
    # 拉剪互制（92 年附表，A325 承壓型）：Ft = 8.2 − 1.9 fv ≤ 6.3
    d['int_a'], d['int_b'], d['int_cap'] = 8.2, 1.9, 6.3
    d['int_fv_at_cap'] = (8.2 - 6.3) / 1.9      # 1.0：fv 小於此值時拉力不折減
    d['int_fv_at_zero'] = 8.2 / 1.9             # 4.32 ≈ Fnv_X
    d['SS2012_Fnv_MPa'] = 330.0                 # SS-2012-4 題給 = 48 ksi = 0.4 × 120 ksi（螺紋在剪力面）
    d['SS2012_Fnv_ratio'] = 330.0 / (120 * 6.895)
    return d


# ------------------------------------------------------------------ 承壓：1.2Lc 與 2.4d
def bearing_general():
    d = {}
    d['k_tear'] = 2 * 0.6          # 兩條剪出線 × 0.6Fu = 1.2
    d['k_cap'] = 2.4               # 孔變形上限（試驗值）
    d['Lc_cross_over_d'] = d['k_cap'] / d['k_tear']   # Lc = 2d 時兩式相等
    # ASD：Fp = 1.2Fu 作用在 d·t；LRFD φ×2.4 = 1.8，1.8/1.5 = 1.2
    d['lrfd_phi_cap'] = 0.75 * 2.4
    d['asd_from_lrfd'] = d['lrfd_phi_cap'] / 1.5
    return d


# ------------------------------------------------------------------ SS-2012-4 剪力板（貫穿範例 A）
def ss2012_4(t=None, dh_net=None):
    """SS-2012-4：剪力板 180×80 mm，3 顆 M20 A325-N 承壓型，Vu = 180 kN，A36（Fy 248、Fu 400 MPa）。
    題解：孔徑 22 mm（d+2）同時用於承壓 Lc 與淨剪面積。
    dh_net：淨面積用的孔徑（預設 22，與題解相同；傳 23 可看 d+3 的規則）。"""
    d = dict(h=180.0, w=80.0, x_bolt=40.0, Vu=180e3, db=20.0, Fnv=330.0, Fy=248.0, Fu=400.0, n_req=None)
    d['Ab'] = math.pi * d['db'] ** 2 / 4
    d['phiRn_bolt'] = 0.75 * d['Fnv'] * d['Ab']                 # N/顆
    d['n_exact'] = d['Vu'] / d['phiRn_bolt']
    d['n'] = math.ceil(d['n_exact'])
    d['Le'] = 1.5 * d['db']; d['s'] = 3 * d['db']
    d['h_check'] = 2 * d['Le'] + (d['n'] - 1) * d['s']
    d['dh'] = d['db'] + 2                                       # 22 mm 標準孔
    dhn = d['dh'] if dh_net is None else dh_net
    d['dh_net'] = dhn
    # 承壓（每 mm 板厚，N/mm）
    d['Lc_edge'] = d['Le'] - d['dh'] / 2
    d['Lc_int'] = d['s'] - d['dh']
    cap = 2.4 * d['db'] * d['Fu']
    d['Rn_edge'] = min(1.2 * d['Lc_edge'] * d['Fu'], cap)
    d['Rn_int'] = min(1.2 * d['Lc_int'] * d['Fu'], cap)
    d['cap_per_t'] = cap
    d['tear_edge'] = 1.2 * d['Lc_edge'] * d['Fu']
    d['tear_int'] = 1.2 * d['Lc_int'] * d['Fu']
    d['phiRn_bear_t'] = 0.75 * (2 * d['Rn_edge'] + (d['n'] - 2) * d['Rn_int'])
    d['t_bear'] = d['Vu'] / d['phiRn_bear_t']
    # 剪力斷裂（淨）與剪力降伏（毛）
    d['Anv_t'] = d['h'] - d['n'] * dhn
    d['phiRup_t'] = 0.75 * 0.6 * d['Fu'] * d['Anv_t']
    d['t_rup'] = d['Vu'] / d['phiRup_t']
    d['Agv_t'] = d['h']
    d['phiYld_t'] = 0.9 * 0.6 * d['Fy'] * d['Agv_t']
    d['t_yld'] = d['Vu'] / d['phiYld_t']
    # 塊狀剪力（題解未檢核，本講義補算）：剪力面沿螺栓線（上緣 → 最下一顆），拉力面由最下一顆到自由邊
    d['Leh'] = d['w'] - d['x_bolt']                             # 40 mm
    d['bs_Agv_t'] = d['Le'] + (d['n'] - 1) * d['s']            # 150
    d['bs_Anv_t'] = d['bs_Agv_t'] - (d['n'] - 0.5) * dhn       # 95
    d['bs_Ant_t'] = d['Leh'] - 0.5 * dhn                       # 29
    r1 = 0.6 * d['Fu'] * d['bs_Anv_t'] + d['Fu'] * d['bs_Ant_t']
    r2 = 0.6 * d['Fy'] * d['bs_Agv_t'] + d['Fu'] * d['bs_Ant_t']
    d['bs_rupture_t'], d['bs_yield_t'] = r1, r2
    d['phiBS_t'] = 0.75 * min(r1, r2)
    d['t_bs'] = d['Vu'] / d['phiBS_t']
    d['t_list'] = [('孔壁承壓', d['t_bear']), ('塊狀剪力', d['t_bs']), ('剪力降伏', d['t_yld']), ('剪力斷裂', d['t_rup'])]
    d['t_req'] = max(v for _, v in d['t_list'])
    d['t_use'] = 10.0 if t is None else t
    tu = d['t_use']
    d['cap'] = [  # (名稱, 容量 kN)
        ('螺栓剪斷', d['n'] * d['phiRn_bolt'] / 1e3),
        ('孔壁承壓', d['phiRn_bear_t'] * tu / 1e3),
        ('剪力降伏', d['phiYld_t'] * tu / 1e3),
        ('剪力斷裂', d['phiRup_t'] * tu / 1e3),
        ('塊狀剪力', d['phiBS_t'] * tu / 1e3),
    ]
    d['cap_min'] = min(c for _, c in d['cap'])
    d['ratio'] = d['Vu'] / 1e3 / d['cap_min']
    return d


# ------------------------------------------------------------------ SS-2017-4 偏心銲縫托架（貫穿範例 B，第 5～7 章）
def ss2017_4():
    d = dict(b=40.0, dv=80.0, te=1.0, xP=90.0)
    d['FEXX'] = 70 * KSI                                   # 4.922
    d['L'] = 2 * d['b'] + d['dv']
    d['xbar'] = d['b'] ** 2 / (2 * d['b'] + d['dv'])
    d['ybar'] = d['dv'] / 2
    xb, yb = d['xbar'], d['ybar']
    d['Jh'] = ((d['b'] - xb) ** 3 - (-xb) ** 3) / 3 + yb ** 2 * d['b']
    d['Jv'] = xb ** 2 * d['dv'] + 2 * (d['dv'] / 2) ** 3 / 3
    d['J'] = 2 * d['Jh'] + d['Jv']
    d['e'] = d['xP'] - xb
    d['q'] = 0.75 * 0.6 * d['FEXX'] * d['te']              # tf/cm
    rx, ry = d['b'] - xb, d['dv'] / 2
    ftx = d['e'] * ry / d['J']; fty = d['e'] * rx / d['J']; fv = 1 / d['L']
    d['ftx'], d['fty'], d['fv'] = ftx, fty, fv
    d['fres'] = math.hypot(ftx, fv + fty)
    d['Pu'] = d['q'] / d['fres']
    return d



# ------------------------------------------------------------------ 第 3 章：SS-2024-2 開槽圓管（tf、cm）
def ss2024_2():
    d = dict(D=27.3, t=1.0, Ag=82.6, Fy=2.3, Fu=3.1, n_slot=4, b_slot=2.2, FEXX=4.92, tg=20)
    d['L'] = d['D']
    d['GSY'] = 0.90 * d['Fy'] * d['Ag']
    d['An'] = d['Ag'] - d['n_slot'] * d['b_slot'] * d['t']
    d['xbar'] = d['D'] / math.pi
    d['U'] = 1 - d['xbar'] / d['L']
    d['Ae'] = d['U'] * d['An']
    d['NSF'] = 0.75 * d['Fu'] * d['Ae']
    d['tear'] = 0.75 * 0.6 * d['Fu'] * (8 * d['L'] * d['t'])
    d['phiTn'] = min(d['GSY'], d['NSF'], d['tear'])
    d['Lw'] = 8 * d['L']
    d['q_per_w'] = 0.75 * 0.6 * d['FEXX'] * 0.707          # tf/cm 每 cm 銲腳
    d['w_req'] = d['phiTn'] / (d['q_per_w'] * d['Lw'])        # cm
    d['w_min'] = 0.8
    return d


def semicircle_xbar(r=1.0):
    """半圓弧（線）形心到直徑的距離 = 2r/π；以 D 表示 = D/π。數值積分驗算。"""
    n = 20000
    s = sum(r * math.sin(math.pi * (i + 0.5) / n) for i in range(n)) / n
    return dict(num=s, exact=2 * r / math.pi)


def ss2022_2():
    """插銷接合（ASD，N、mm）：題解數值。"""
    d = dict(b=300.0, t=20.0, dp=100.0, a=65.0, Fy=345.0, Fu=450.0, P=450.0)
    d['be'] = min(2 * d['t'] + 16, d['a'], 135.0)
    d['Pa1'] = d['Fy'] * d['b'] * d['t'] / 1.67 / 1e3
    d['Pa2'] = d['Fu'] * 2 * d['t'] * d['be'] / 2.0 / 1e3
    d['Asf'] = 2 * d['t'] * (d['a'] + d['dp'] / 2)
    d['Pa3'] = 0.6 * d['Fu'] * d['Asf'] / 2.0 / 1e3
    d['Pa4'] = 1.8 * d['Fy'] * d['t'] * d['dp'] / 2.0 / 1e3
    return d


# ------------------------------------------------------------------ 第 4 章：摩阻型（tf、cm）
def slip_M20():
    d = dict(db=2.0, Ab=math.pi * 2.0 ** 2 / 4, At=2.45, Fu=8.4, mu=0.33)
    d['Tb'] = 0.70 * d['Fu'] * d['At']
    d['At_over_Ab'] = d['At'] / d['Ab']
    d['Tb_over_FuAb'] = d['Tb'] / (d['Fu'] * d['Ab'])
    d['Rstr'] = 1.13 * d['mu'] * d['Tb']                     # φ = 1.0，每螺栓每摩擦面
    d['asd_from_lrfd'] = d['Rstr'] / 1.5 / d['Ab']           # tf/cm²
    d['asd_table'] = 1.19
    d['bear_N'] = 0.75 * 3.36 * d['Ab']
    d['bear_X'] = 0.75 * 4.20 * d['Ab']
    d['slip_over_N'] = d['Rstr'] / d['bear_N']
    return d


def ss2004_2():
    d = dict(T=70.0, Tf=35.0, Fv=1.19, Ab=math.pi * 2.0 ** 2 / 4)
    d['per_bolt'] = 2 * d['Fv'] * d['Ab']
    d['n_exact'] = d['Tf'] / d['per_bolt']
    d['n'] = 6
    d['cap'] = d['n'] * d['per_bolt']
    return d


# ------------------------------------------------------------------ 第 5 章：銲道
def weld_general(FEXX=4.92):
    d = dict(FEXX=FEXX)
    d['te_over_w'] = 1 / math.sqrt(2)
    d['lrfd_coef'] = 0.75 * 0.6                          # 0.45
    d['asd_coef'] = d['lrfd_coef'] / 1.5                   # 0.30
    d['Fw_asd'] = 0.30 * FEXX
    d['q_lrfd_per_w'] = 0.45 * FEXX * 0.707               # tf/cm per cm 銲腳
    d['q_asd_per_w'] = 0.30 * FEXX * 0.707
    d['E70_tf'] = 70 * KSI
    return d


def directional(theta_deg):
    th = math.radians(theta_deg)
    return 1.0 + 0.5 * math.sin(th) ** 1.5


WMIN = [(6, 3), (12, 5), (19, 6), (38, 8)]     # (板厚上限 mm, 最小銲腳 mm)


def w_min(t):
    for tt, w in WMIN:
        if t <= tt:
            return w
    return 8


def ss2015_2_weld():
    d = dict(P=83.46, Lw=2 * 35.0, FEXX=4.9, t_plate=16)
    d['q_per_w'] = 0.75 * 0.6 * d['FEXX'] * 0.707 * d['Lw']  # tf per cm 銲腳
    d['w_req'] = d['P'] / d['q_per_w']
    d['w_min'] = w_min(d['t_plate']) / 10
    d['w_use'] = 0.8
    return d


# ------------------------------------------------------------------ 第 6 章：SS-2002-4 偏心螺栓群（ASD，tf、cm）
def ss2002_4():
    d = dict(P=20.0, Px=-12.0, Py=-16.0, xP=28.5, yP=15.5, Ab=3.88, Fv=2.10, Fu=4.1)
    pts = [(x, y) for x in (3.5, -3.5) for y in (10.5, 3.5, -3.5, -10.5)]
    d['pts'] = pts
    d['n'] = len(pts)
    d['Sx2'] = sum(x * x for x, _ in pts); d['Sy2'] = sum(y * y for _, y in pts)
    d['Ip'] = d['Sx2'] + d['Sy2']
    d['M'] = d['xP'] * d['Py'] - d['yP'] * d['Px']            # 逆時針為正
    d['M_y_part'] = d['xP'] * d['Py']; d['M_x_part'] = -d['yP'] * d['Px']
    d['e'] = abs(d['M']) / d['P']
    d['M_wrong'] = d['P'] * d['xP']
    res = []
    for x, y in pts:
        fx = d['Px'] / d['n'] - d['M'] * y / d['Ip']
        fy = d['Py'] / d['n'] + d['M'] * x / d['Ip']
        res.append((x, y, fx, fy, math.hypot(fx, fy)))
    d['res'] = res
    d['Rmax'] = max(r[4] for r in res)
    d['r_corner'] = math.hypot(3.5, 10.5)
    d['RM_corner'] = abs(d['M']) * d['r_corner'] / d['Ip']
    d['Rv'] = d['Fv'] * d['Ab']
    d['Rp_flange'] = 1.2 * d['Fu'] * 2.2 * 1.156
    d['ratio'] = d['Rmax'] / d['Rv']
    # 若誤把 P 當垂直力、力臂 25
    return d


# ------------------------------------------------------------------ 第 7 章：SS-2004-3（LRFD，tf、cm）
def ss2004_3():
    d = dict(FEXX=4.93, w=1.0)
    d['q'] = 0.75 * 0.6 * d['FEXX'] * 0.707 * d['w']
    segs = [((0, 12.5), (7.5, 12.5)), ((0, 7.5), (0, 12.5)), ((0, -12.5), (7.5, -12.5)), ((0, -12.5), (0, -7.5))]
    d['segs'] = segs
    L = [math.dist(a, b) for a, b in segs]
    d['L'] = sum(L)
    d['xbar'] = sum(l * (a[0] + b[0]) / 2 for l, (a, b) in zip(L, segs)) / d['L']
    xb = d['xbar']
    J = 0
    for l, (a, b) in zip(L, segs):
        # 線段對形心的 ∫r² dL
        n = 2000
        for i in range(n):
            t = (i + 0.5) / n
            x = a[0] + (b[0] - a[0]) * t - xb; y = a[1] + (b[1] - a[1]) * t
            J += (x * x + y * y) * l / n
    d['J'] = J
    c = 1 / math.sqrt(2)
    d['xP'] = 17.5 - xb; d['yP'] = 12.5
    d['M'] = d['xP'] * (-c) - d['yP'] * (-c)            # ×Pu，逆時針為正
    d['M_v'] = d['xP'] * c; d['M_h'] = d['yP'] * c
    pts = [(7.5, 12.5), (0, 12.5), (0, 7.5), (7.5, -12.5), (0, -12.5), (0, -7.5)]
    res = []
    for X, Y in pts:
        x, y = X - xb, Y
        fx = -c / d['L'] - d['M'] * y / J
        fy = -c / d['L'] + d['M'] * x / J
        res.append((X, Y, fx, fy, math.hypot(fx, fy)))
    d['res'] = res
    d['fmax'] = max(r[4] for r in res)
    d['Pu'] = d['q'] / d['fmax']
    d['P0'] = d['q'] * d['L']
    d['e_line'] = abs(d['M'])                             # 力線到形心距離（因 |P| = 1）
    d['Pu_wrong_vertical'] = None
    return d


def ss2017_4_points():
    D = ss2017_4()
    xb, yb = D['xbar'], D['ybar']
    pts = [(40, 80), (40, 0), (0, 80), (0, 0)]
    res = []
    for X, Y in pts:
        rx, ry = X - xb, Y - yb
        fx = D['e'] * ry / D['J']           # 順時針扭矩
        fy = -D['e'] * rx / D['J'] - D['fv']
        res.append((X, Y, fx, fy, math.hypot(fx, fy), math.hypot(rx, ry)))
    D['res'] = res
    D['P0'] = D['q'] * D['L']
    D['ratio_P0'] = D['Pu'] / D['P0']
    D['Jh_own'] = D['b'] ** 3 / 12 + D['b'] * (D['b'] / 2 - xb) ** 2
    D['Jh_far'] = D['b'] * yb ** 2
    D['Jv_own'] = D['dv'] ** 3 / 12
    D['Jv_far'] = D['dv'] * xb ** 2
    return D


# ------------------------------------------------------------------ 第 8 章：梁的接合
def ss2018_3():
    d = dict(d=500.0, bf=200.0, tf=16.0, tw=9.0, M=150.0, Q=100.0, Mf_given=124.5, Mw_given=25.5,
             lw=388.0, w=6.0, fa=90.5)
    hw = d['d'] - 2 * d['tf']
    d['If'] = 2 * (d['bf'] * d['tf'] ** 3 / 12 + d['bf'] * d['tf'] * ((d['d'] - d['tf']) / 2) ** 2)
    d['Iw'] = d['tw'] * hw ** 3 / 12
    d['I'] = d['If'] + d['Iw']
    d['Mf'] = d['M'] * d['If'] / d['I']; d['Mw'] = d['M'] * d['Iw'] / d['I']
    d['arm'] = d['d'] - d['tf']
    d['Ff'] = d['Mf_given'] * 1e6 / d['arm'] / 1e3              # kN
    te = d['w'] / math.sqrt(2)
    d['Sw'] = 2 * te * d['lw'] ** 2 / 6
    d['tau1'] = d['Mw_given'] * 1e6 / d['Sw']
    d['Aw'] = 2 * te * d['lw']
    d['tau2'] = d['Q'] * 1e3 / d['Aw']
    d['tau'] = math.hypot(d['tau1'], d['tau2'])
    d['w_req'] = d['w'] * d['tau'] / d['fa']
    d['tauf_400'] = d['Ff'] * 1e3 / (0.707 * d['w'] * 400)
    d['tauf_432'] = d['Ff'] * 1e3 / (0.707 * d['w'] * 432)
    d['wf_400'] = d['w'] * d['tauf_400'] / d['fa']
    d['wf_432'] = d['w'] * d['tauf_432'] / d['fa']
    return d


def ss2019_4():
    d = dict(H=50.0, bf=20.0, tf=1.6, tw=0.9, tp=2.5, bp=30.0, Vu=50.0, w=0.8, FEXX=4.9, s=15.0)
    hw = d['H'] - 2 * d['tf']
    d['AH'] = 2 * d['bf'] * d['tf'] + hw * d['tw']
    d['Ap'] = d['tp'] * d['bp']
    d['ybar'] = (d['AH'] * d['H'] / 2 + d['Ap'] * (d['H'] + d['tp'] / 2)) / (d['AH'] + d['Ap'])
    IH = (d['bf'] * d['H'] ** 3 - (d['bf'] - d['tw']) * hw ** 3) / 12
    d['I'] = IH + d['AH'] * (d['H'] / 2 - d['ybar']) ** 2 + d['bp'] * d['tp'] ** 3 / 12 + d['Ap'] * (d['H'] + d['tp'] / 2 - d['ybar']) ** 2
    d['Q'] = d['Ap'] * (d['H'] + d['tp'] / 2 - d['ybar'])
    d['Q_wrong'] = d['Ap'] * (d['H'] + d['tp'] / 2 - d['H'] / 2)
    d['q'] = d['Vu'] * d['Q'] / d['I']
    d['Fs'] = d['q'] * d['s']
    d['cap_per_cm'] = 2 * 0.75 * 0.6 * d['FEXX'] * 0.707 * d['w']
    d['L'] = d['Fs'] / d['cap_per_cm']
    d['Lmin'] = max(4 * d['w'], 4.0)
    return d


def ss2020_4():
    d = dict(V=70.0, e=5.0, Fva=2.8, ys=[4, 12, 20], n=6, tw=1.4, Fu=4.1, hpl=48.0, Fy=2.5)
    d['Sy2'] = 2 * sum(y * y for y in d['ys'])
    d['M'] = d['V'] * d['e']
    d['fv'] = d['V'] / d['n']
    d['fh'] = d['M'] * max(d['ys']) / d['Sy2']
    d['R'] = math.hypot(d['fv'], d['fh'])
    d['Ab_req'] = d['R'] / (2 * d['Fva'])
    d['Ab'] = math.pi * 2.0 ** 2 / 4
    d['cap'] = 2 * d['Ab'] * d['Fva']
    d['web_bear'] = 1.2 * d['Fu'] * 2.0 * d['tw']
    d['t_shear'] = d['V'] / (2 * d['hpl'] * 0.4 * d['Fy'])
    d['t_bend'] = d['M'] / (2 * d['hpl'] ** 2 / 6 * 0.6 * d['Fy'])
    return d


def ss2007_1():
    """平衡銲道（ASD，tf、cm）：角鋼 15×10×1.5，P 作用線距 a 側 10 cm、b 側 5 cm。"""
    d = dict(P=71.9, q=0.3 * 4.9 * 0.707 * 1.2, w_end=15.0, ya=10.0, yb=5.0)
    d['F3'] = d['q'] * d['w_end']
    d['Fb'] = (d['P'] * d['ya'] - d['F3'] * 7.5) / 15.0
    d['Fa'] = d['P'] - d['F3'] - d['Fb']
    d['a'] = d['Fa'] / d['q']; d['b'] = d['Fb'] / d['q']
    return d


def misc():
    """內文 🙈 與自我檢查用到的零星數字。"""
    D24 = ss2024_2()
    S = slip_M20()
    d = {}
    d['2024_NSF_U1'] = 0.75 * D24['Fu'] * D24['An']
    d['2024_slot_frac'] = D24['n_slot'] * D24['b_slot'] * D24['t'] / D24['Ag']
    d['U_L_eq_w'] = 3 / (3 + 1)
    d['slip_2face_asd'] = 2 * S['Rstr'] / 1.5
    d['Ab_over_At'] = S['Ab'] / S['At']
    d['2004_2_per_bolt_load'] = 35 / 6
    d['2004_2_end_bear'] = 3.0 * 4.1 / (2 * 2.0) * 2.0 * 1.0
    d['te10_w'] = 10 / 0.707
    d['2015_asd_per_w'] = 0.3 * 4.9 * 0.707 * 70
    B = ss2017_4()
    e2 = 40.0
    fx = e2 * 40 / B['J']; fy = 1 / B['L'] + e2 * 30 / B['J']
    d['2017_e40_fres'] = math.hypot(fx, fy); d['2017_e40_Pu'] = B['q'] / d['2017_e40_fres']
    A = ss2018_3()
    d['2018_w_tau1_only'] = A['w'] * A['tau1'] / A['fa']
    d['2018_Mw_frac'] = A['Mw'] / A['M']
    d['2019_Q_over'] = ss2019_4()['Q_wrong'] / ss2019_4()['Q'] - 1
    d['2004_3_r_corner'] = math.hypot(7.5 - 2.25, 12.5)
    return d


# ------------------------------------------------------------------ 第 10 章：耐震梁柱接頭（示範梁＝SS-2018-3 的 H500×200×9×16，示範假設另註）
def seismic_beam(Lclear=6000.0, Fy_tf=2.4):
    d = dict(d=500.0, bf=200.0, tf=16.0, tw=9.0, Lc=Lclear, Fy=Fy_tf)
    hw = d['d'] - 2 * d['tf']
    d['Z'] = d['bf'] * d['tf'] * (d['d'] - d['tf']) + d['tw'] * hw ** 2 / 4          # mm³
    # RBS：a = 0.625bf、b = 0.75d、每側削 c = 0.2bf（AISC 範圍 0.1～0.25bf）
    d['a'] = 0.625 * d['bf']; d['b'] = 0.75 * d['d']; d['c'] = 0.20 * d['bf']
    d['Z_rbs'] = d['Z'] - 2 * d['c'] * d['tf'] * (d['d'] - d['tf'])
    d['rbs_ratio'] = d['Z_rbs'] / d['Z']
    d['sh_rbs'] = d['a'] + d['b'] / 2
    half = d['Lc'] / 2
    d['amp_rbs'] = half / (half - d['sh_rbs'])                 # 柱面彎矩 / 塑鉸彎矩（反對稱、不計重力）
    d['face_over_Mp_rbs'] = d['amp_rbs'] * d['rbs_ratio']
    # 補強（蓋板長 a_cp）：塑鉸在蓋板末端，強度 = Mp
    d['a_cp'] = 400.0
    d['amp_cp'] = half / (half - d['a_cp'])
    d['face_over_Mp_cp'] = d['amp_cp']
    # 塑性彎矩（tf·m）與節點域剪力（單側梁、不計柱剪力）
    Zcm3 = d['Z'] / 1e3
    d['Mp_tfm'] = d['Fy'] * Zcm3 / 100
    d['Vpz'] = d['Mp_tfm'] * 100 / ((d['d'] - d['tf']) / 10)   # tf
    # 側撐
    Iy = 2 * d['tf'] * d['bf'] ** 3 / 12 + hw * d['tw'] ** 3 / 12
    A = 2 * d['bf'] * d['tf'] + hw * d['tw']
    d['ry_cm'] = math.sqrt(Iy / A) / 10
    d['Lb_max'] = 170 * d['ry_cm'] / math.sqrt(d['Fy'])
    d['Pbr'] = 0.02 * d['Fy'] * (d['bf'] / 10) * (d['tf'] / 10)
    return d


def yield_ratio():
    return dict(sn490b=(325, 445), Fu_min=490, YR_max=0.80, hardening_room=1 / 0.80 - 1,
                a572_example=0.95, a572_room=1 / 0.95 - 1)


def plate_shear_variant(h=300.0):
    """🙈 Q4：同 SS-2012-4 但板高 h、仍 3 顆、孔徑 22：比較剪力降伏與剪力斷裂。"""
    D = ss2012_4()
    Anv = h - 3 * D['dh']
    rup = 0.75 * 0.6 * D['Fu'] * Anv
    yld = 0.9 * 0.6 * D['Fy'] * h
    return dict(h=h, Anv_t=Anv, rup_t=rup, yld_t=yld, t_rup=D['Vu'] / rup, t_yld=D['Vu'] / yld,
                crit_ratio=1.2 * D['Fy'] / D['Fu'], ratio_2012=D['Anv_t'] / D['Agv_t'],
                rup_over_yld_2012=D['phiRup_t'] / D['phiYld_t'])


def _show(name, d):
    print('=' * 8, name)
    for k, v in d.items():
        if isinstance(v, float):
            print(f'  {k:16s} {v:.4f}')
        elif isinstance(v, list) and v and isinstance(v[0], tuple) and len(v[0]) == 2 and isinstance(v[0][0], str):
            print(f'  {k:16s}', ', '.join(f'{a}={b:.2f}' for a, b in v))
        elif isinstance(v, list) and v and isinstance(v[0], tuple):
            for r in v:
                print('      ', '  '.join(f'{z:.4f}' if isinstance(z, float) else str(z) for z in r))
        else:
            print(f'  {k:16s} {v}')


if __name__ == '__main__':
    print('φ / Ω')
    for k, p in PHI.items():
        print(f'  {k:14s} φ={p:.2f}  Ω=1.5/φ={omega(p):.2f}')
    _show('1/√3', shear_ratio())
    _show('A325', bolt_A325())
    _show('bearing', bearing_general())
    _show('SS-2012-4（孔徑 22，同題解）', ss2012_4())
    s23 = ss2012_4(dh_net=23)
    print('  d+3 = 23 mm 時：Anv/t =', s23['Anv_t'], ' t_rup =', round(s23['t_rup'], 2), ' t_bs =', round(s23['t_bs'], 2))
    _show('板高變化（Q4）與臨界比', plate_shear_variant())
    for nm, fn in [('SS-2024-2', ss2024_2), ('半圓 x̄', semicircle_xbar), ('SS-2022-2', ss2022_2), ('slip M20', slip_M20),
                   ('SS-2004-2', ss2004_2), ('weld', weld_general), ('SS-2015-2 weld', ss2015_2_weld), ('SS-2002-4', ss2002_4),
                   ('SS-2004-3', ss2004_3), ('SS-2017-4 points', ss2017_4_points), ('SS-2018-3', ss2018_3),
                   ('SS-2019-4', ss2019_4), ('SS-2020-4', ss2020_4), ('SS-2007-1', ss2007_1), ('misc', misc), ('seismic', seismic_beam), ('YR', yield_ratio)]:
        _show(nm, {k: v for k, v in fn().items() if k not in ('segs', 'pts')})
    print('directional 90°', directional(90), ' wmin(16)=', w_min(16), ' wmin(20)=', w_min(20))
