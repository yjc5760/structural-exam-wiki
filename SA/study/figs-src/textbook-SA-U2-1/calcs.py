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


def ch3x():
    """第 3 章補充：U(R) 拋物線、沉陷修正、二度靜不定（2013-2）、斜桿（2005-1、2008-3）。"""
    import sympy as sp
    d = {}
    c2 = ch2()
    # (1) U(R)·EI = ½(f11 R² − 2·3600 R + ∫M0²)；∫6^12 [20(x−6)]² dx = 400·72
    d['M0sq'] = integ_poly(pmul([-120, 20], [-120, 20]), 6, 12)          # 28800
    f11, d10 = c2['f11'], c2['d10_up']                                  # 576, −3600
    d['U_EI'] = lambda R: 0.5 * (float(f11) * R * R + 2 * float(d10) * R + float(d['M0sq']))
    d['dUdR_EI'] = lambda R: float(f11) * R + float(d10)                # = EI·δ_up(C)
    d['Umin_EI'] = Fr(1, 2) * (d['M0sq'] - f11 * Fr(25, 4) ** 2)        # 3150
    d['U0_EI'] = Fr(1, 2) * d['M0sq']                                   # 14400（R = 0）
    # (2) 沉陷：D 下沉 Δ（向上為正 → δ = −Δ）：576R − 3600 = −EI·Δ
    d['settle'] = lambda Dl: (3600 - float(EX['EI']) * Dl) / 576.0
    d['Dl_ex'] = Fr(576, 1000)                                          # 0.576 m
    d['R_settle'] = (3600 - EX['EI'] * d['Dl_ex']) / 576                # 21/4 = 5.25
    d['Dl_zero'] = Fr(3600, 1000)                                       # 3.6 m → R = 0
    # (3) 2013-2：Cx（向左）、Cy（向上）兩個多餘力
    Cx, Cy = sp.symbols('Cx Cy')
    x, y = sp.symbols('x y')
    Mbc = Cy * x - 20 * sp.Piecewise((0, x < 5), (x - 5, True))
    Mab = Cx * y + 10 * Cy - 100
    def dU(var):
        return (sp.integrate(sp.diff(Mbc, var) * Mbc, (x, 0, 5)) + sp.integrate(sp.diff(Mbc, var) * Mbc, (x, 5, 10))
                + sp.integrate(sp.diff(Mab, var) * Mab, (y, 0, 10)))
    sol = sp.solve([dU(Cx), dU(Cy)], [Cx, Cy])
    d['13_Cx'], d['13_Cy'] = sol[Cx], sol[Cy]                           # 45/14、55/7
    d['13_eq1'] = sp.expand(dU(Cx)); d['13_eq2'] = sp.expand(dU(Cy))
    th = (sp.integrate(Mbc, (x, 0, 5)) + sp.integrate(Mbc, (x, 5, 10)) + sp.integrate(Mab, (y, 0, 10))).subs(sol)
    d['13_th'] = sp.nsimplify(th)                                       # 625/7
    # (4) 2005-1：BC 斜桿 s（0..4√2）、BA x（0..8）
    R, s = sp.symbols('R s', real=True)
    Mbc5 = R * s / sp.sqrt(2)
    Mba5 = (R - 10) * x - 4 * R
    eq = sp.integrate(Mbc5 * sp.diff(Mbc5, R), (s, 0, 4 * sp.sqrt(2))) + sp.integrate(Mba5 * sp.diff(Mba5, R), (x, 0, 8))
    d['05_R'] = sp.nsimplify(sp.solve(eq, R)[0])                        # 20 − 10√2
    d['05_MB'] = sp.simplify(-4 * d['05_R'])                            # BA 在 B 端（上緣受拉）
    d['05_MA'] = sp.simplify((d['05_R'] - 10) * 8 - 4 * d['05_R'])      # −40√2
    # (5) 2008-3：ds = (5/3)dx
    Mab8 = R * x - x ** 2
    Mbc8 = R * x - 12 * (x - 3)
    eq8 = sp.integrate(Mab8 * x, (x, 0, 6)) + sp.Rational(5, 3) * sp.integrate(Mbc8 * x, (x, 6, sp.Rational(21, 2)))
    d['08_R'] = sp.solve(eq8, R)[0]                                      # 3888/529
    d['08_MB'] = 6 * d['08_R'] - 36
    d['08_MC'] = d['08_R'] * sp.Rational(21, 2) - 90
    d['08_R_noratio'] = sp.solve(sp.integrate(Mab8 * x, (x, 0, 6)) + sp.integrate(Mbc8 * x, (x, 6, sp.Rational(21, 2))), R)[0]
    return d


def ch4():
    """圖乘法：表格、拋物線、SA-2016-3、2014-4 拆圖。"""
    d = {}
    simpson = lambda L, a, m_, b, ma, mm, mb: L / 6 * (a * ma + 4 * m_ * mm + b * mb)
    trap = lambda L, a, b, c, dd: L / 6 * (2 * a * c + a * dd + b * c + 2 * b * dd)
    d['simpson'], d['trap'] = simpson, trap
    # 2016-3：CD 柱，y 自 C 向下 0..20，左側受拉為正
    Mt, Mb_, Lc = Fr(-253, 10), Fr(17), Fr(20)
    d['16_Mt'], d['16_Mb'], d['16_L'] = Mt, Mb_, Lc
    d['16_Mmid'] = (Mt + Mb_) / 2                                       # −4.15
    d['16_dx'] = trap(Lc, Mt, Mb_, 0, Lc)                               # 580
    d['16_dx_simpson'] = simpson(Lc, Mt, d['16_Mmid'], Mb_, 0, 10, 20)  # 580
    d['16_th'] = -(Mt + Mb_) / 2 * Lc                                   # 83（逆時針）
    d['16_y0'] = -Mt / ((Mb_ - Mt) / Lc)                                # 11.96
    # 2014-4 拆圖（x 自 C 量）：R 三角形 0→12R、載重三角形 0→−120（x = 6..12）
    R = Fr(25, 4)
    d['14_tri_R'] = Fr(1, 2) * 12 * 12 * R                             # 450
    d['14_tri_P'] = Fr(1, 2) * 6 * (-120)                              # −360
    d['14_f11'] = Fr(12, 3) * 12 * 12                                  # 576
    d['14_d10'] = trap(Fr(6), 0, Fr(-120), Fr(6), Fr(12))               # −3600
    # 拋物線（簡支梁 UDL）：w = 2、L = 12（以 2016-3 BC 段的數字示意）
    w, L = Fr(2), Fr(12)
    d['par_w'], d['par_L'] = w, L
    d['par_h'] = w * L ** 2 / 8                                        # 36
    d['par_A'] = Fr(2, 3) * L * d['par_h']                             # 288 = wL³/12
    d['par_A_half'] = Fr(2, 3) * (L / 2) * d['par_h']                  # 144
    d['par_xbar_half'] = Fr(3, 8) * (L / 2)                             # 2.25 自頂點
    # 拋物線 × 三角形（左端 0、右端 1）：Simpson = L/6(0 + 4·h·½ + 0) = hL/3
    d['par_x_tri'] = simpson(L, 0, d['par_h'], 0, 0, Fr(1, 2), 1)      # 144
    d['par_x_tri_direct'] = integ_poly(pmul([0, w * L / 2, -w / 2], [0, 1 / L]), 0, L)
    return d


def ch5():
    """固端彎矩：兩個多餘力的最小功法 → Pab²/L²、PL/8、wL²/12；2017-2 內鉸通式。"""
    import sympy as sp
    d = {}
    P, Lb = EX['P'], EX['L']
    d['MF'] = P * Lb / 8                                                # 30 kN·m（2014-4 改 C 端固定）
    Ps, L, a, b, x, Rr, Mc, w = sp.symbols('P L a b x R M_C w', positive=True)
    # 懸臂（A 端固定、x 自 C 量），載重 P 距 A 為 a、距 C 為 b；多餘力 R（C 向上）、M_C（C 端內彎矩）
    M = Rr * x + Mc - Ps * sp.Piecewise((0, x < b), (x - b, True))
    e1 = sp.integrate(sp.diff(M, Rr) * (Rr * x + Mc), (x, 0, L)) - Ps * sp.integrate((x - b) * x, (x, b, L))
    e2 = sp.integrate(sp.diff(M, Mc) * (Rr * x + Mc), (x, 0, L)) - Ps * sp.integrate((x - b), (x, b, L))
    sol = sp.solve([e1, e2], [Rr, Mc])
    McS = sp.factor(sp.simplify(sol[Mc].subs(L, a + b)))
    RS = sp.factor(sp.simplify(sol[Rr].subs(L, a + b)))
    d['Mc_sym'], d['R_sym'] = McS, RS                                   # −P a² b/(a+b)²、P a²(a+3b)/(a+b)³
    MA = sp.factor(sp.simplify((RS * (a + b) + McS - Ps * a)))
    d['MA_sym'] = MA                                                    # −P a b²/L²
    d['flex'] = (Lb ** 3 / 3, Lb ** 2 / 2, Lb)                          # f11、f12、f22
    d['Mc_mid'] = sp.simplify(McS.subs({a: L / 2, b: L / 2}))           # −PL/8
    d['Mc_ex'] = McS.subs({Ps: 20, a: 6, b: 6})                         # −30
    # 均布：Pab²/L² 對 a 積分
    aa = sp.symbols('a', positive=True)
    d['udl'] = sp.simplify(sp.integrate(w * aa * (L - aa) ** 2 / L ** 2, (aa, 0, L)))   # wL²/12
    # 2017-2 通式
    m, n = sp.symbols('m n', positive=True)
    Ma = -w * m * (m ** 3 - m ** 2 * n + m * n ** 2 + 3 * n ** 3) / (8 * (m ** 2 - m * n + n ** 2))
    Mb = -w * n * (3 * m ** 3 + m ** 2 * n - m * n ** 2 + n ** 3) / (8 * (m ** 2 - m * n + n ** 2))
    d['17_Ma'], d['17_Mb'] = Ma, Mb
    # 以最小功法重解驗證（X = Ma）
    X, xx = sp.symbols('X xx')
    Lsum = m + n
    Ra = w * m / 2 - X / m
    Mx = Ra * xx + X - w * xx ** 2 / 2
    eq = sp.integrate(Mx * sp.diff(Mx, X), (xx, 0, Lsum))
    d['17_check'] = sp.simplify(sp.solve(eq, X)[0] - Ma)                # 0
    d['17_mid'] = sp.simplify(Ma.subs(m, n) / (w * (2 * n) ** 2))       # −1/8
    d['17_m0_b'] = sp.limit(Mb / (w * n ** 2), m, 0)                    # −1/8（支承鉸＋固定 → 支撐懸臂）
    d['17_m0_a'] = sp.limit(Ma, m, 0)                                   # 0
    fa = sp.lambdify(m, sp.simplify(-Ma.subs({w: 1, n: 1 - m})))
    fb = sp.lambdify(m, sp.simplify(-Mb.subs({w: 1, n: 1 - m})))
    d['17_fa'], d['17_fb'] = fa, fb                                     # |Ma|/wL²、|Mb|/wL²（L = 1）
    d['17_r04'] = (fa(0.4), fb(0.4))
    return d


def ch6():
    """2012-2（桁架＋彈簧）與 2006-1（梁＋桁架，α = EI/EA）。"""
    import sympy as sp
    d = {}
    X, r = sp.symbols('X r', real=True)           # r = EA/Ks（等效長度，m）
    s2 = sp.sqrt(2)
    rows = [  # 桿, L, F, ∂F/∂X
        ('ab', 4, 30 - X / 2, -sp.Rational(1, 2)),
        ('bc', 4, 30 - X / 2, -sp.Rational(1, 2)),
        ('ad', 4 * s2, -10 * s2 + s2 / 2 * X, s2 / 2),
        ('cd', 4 * s2, -30 * s2 + s2 / 2 * X, s2 / 2),
        ('bd', 4, -X, -1),
    ]
    d['12_rows'] = rows
    expr = sum(F * u * L for _, L, F, u in rows) + r * X
    d['12_expr'] = sp.expand(expr)
    Xs = sp.solve(expr, X)[0]
    d['12_Xr'] = sp.simplify(Xs)
    d['12_r'] = sp.Integer(10000) / 2500                                # 4 m
    d['12_X'] = sp.nsimplify(sp.radsimp(Xs.subs(r, 4)))                 # (−20+280√2)/17
    d['12_X_rigid'] = sp.radsimp(Xs.subs(r, 0))                         # k → ∞
    d['12_fX'] = sp.lambdify(r, Xs)
    d['12_forces'] = {nm: sp.radsimp(F.subs(X, d['12_X'])) for nm, L, F, u in rows}
    # 2006-1
    al = sp.symbols('alpha', positive=True)
    RD = (sp.Rational(8125, 10) + al * (50 + 40 * s2)) / (100 + al * (4 + 3 * s2))
    DJ = 20 * (1 + s2) * (20 - RD)                                      # ×1/EA
    d['06_RD'], d['06_DJ'] = RD, DJ
    d['06_RD0'], d['06_RDinf'] = RD.subs(al, 0), sp.limit(RD, al, sp.oo)
    d['06_DJ0'], d['06_DJinf'] = sp.N(DJ.subs(al, 0)), sp.N(sp.limit(DJ, al, sp.oo))
    d['06_fRD'] = sp.lambdify(al, RD)
    d['06_fDJ'] = sp.lambdify(al, DJ)
    d['06_RA0'] = 2 * d['06_RD0'] - 20                                  # −3.75
    return d


def ch7():
    """2018-3（纜索鬆弛）與 2019-1（逐步失效、極限機構）。"""
    import sympy as sp
    d = {}
    X1, X2, x, y = sp.symbols('X1 X2 x y', real=True)
    EI, EA, Lc = 1000, 500, 5
    Mab = -X1 * x                       # x 自 A 向右
    Mbc = -X1 * (x + 5) - X2 * x        # x 自 B 向右
    Mcg = 500 - 10 * X1 - 5 * X2        # 柱（常數）
    U = (sp.integrate(Mab ** 2, (x, 0, 5)) + sp.integrate(Mbc ** 2, (x, 0, 5)) + sp.integrate(Mcg ** 2, (y, 0, 5))) / (2 * EI) \
        + (X1 ** 2 + X2 ** 2) * Lc / (2 * EA)
    both = sp.solve([sp.diff(U, X1), sp.diff(U, X2)], [X1, X2])
    d['18_both'] = (both[X1], both[X2])                                  # X1 < 0 → AE 鬆弛
    U1 = U.subs(X1, 0)
    X2s = sp.solve(sp.diff(U1, X2), X2)[0]
    d['18_X2'] = X2s                                                    # 3750/53
    # A 點向下位移（虛設向下單位力；AE 鬆弛時）＝ −∂U/∂X1 在 X1=0 的「纜索以外」部分
    vA = (sp.integrate((-X2s * x) * (-(x + 5)), (x, 0, 5)) + sp.integrate((500 - 5 * X2s) * (-10), (y, 0, 5))) / EI
    d['18_vA'] = sp.nsimplify(vA)
    d['18_MCm'] = -5 * X2s
    d['18_MCp'] = -500
    d['18_Mcol'] = 500 - 5 * X2s
    d['18_vB'] = X2s * Lc / EA                                          # B 上移＝BF 伸長
    # 2019-1
    T, Pp = sp.symbols('T P', real=True)
    rows = [('DA', 15, T), ('BC', 15, sp.Rational(5, 4) * Pp + T), ('DB', 12, -sp.Rational(4, 5) * T),
            ('AC', 12, -sp.Rational(4, 5) * T), ('DC', 9, -sp.Rational(3, 5) * T), ('AB', 9, -sp.Rational(3, 4) * Pp - sp.Rational(3, 5) * T)]
    Ts = sp.solve(sum(F * sp.diff(F, T) * L for _, L, F in rows), T)[0]
    d['19_T'] = Ts                                                      # −95P/216
    forces = {nm: sp.simplify(F.subs(T, Ts)) for nm, L, F in rows}
    d['19_forces'] = forces
    cap = {'DA': (1250, 144), 'BC': (1250, 144), 'DB': (1250, 225), 'AC': (1250, 225), 'DC': (1250, 400), 'AB': (1250, 400)}
    lim = {}
    for nm, F in forces.items():
        c = sp.simplify(F / Pp)
        if c == 0:
            continue
        lim[nm] = (cap[nm][0] if c > 0 else cap[nm][1]) / abs(c)
    d['19_lim1'] = lim
    P1 = min(lim.values()); d['19_P1'] = P1                             # 327.41（DA 壓挫）
    U1 = sum(F ** 2 * L for _, L, F in rows).subs(T, Ts) / 2            # ×1/EA
    d['19_k1'] = sp.simplify(sp.diff(U1, Pp) / Pp)                      # 665/36
    d['19_k2'] = sp.Rational(15 * 25, 16) + sp.Rational(9 * 9, 16)      # 28.5
    d['19_P2'] = sp.Rational(400) / sp.Rational(3, 4)                   # 533.33（AB 壓挫）
    d['19_U1'] = d['19_k1'] * P1
    d['19_U1b'] = d['19_k2'] * P1
    d['19_U2'] = d['19_k2'] * d['19_P2']
    d['19_stage1'] = {nm: sp.N(F.subs(Pp, P1)) for nm, F in forces.items()}
    return d


C1, C2, C3, C3X, C4, C5, C6, C7 = ch1(), ch2(), ch3(), ch3x(), ch4(), ch5(), ch6(), ch7()

def ch8():
    """綜合重建練習：A 固定、C 滾支承梁，全跨均布 w（x 自 C 量）。"""
    import sympy as sp
    d = {}
    w, L, EI, x, R, Q, Dl, k = sp.symbols('w L EI x R Q Delta k', positive=True)
    M = R * x - w * x ** 2 / 2 + Q
    dUdR = sp.integrate(M * sp.diff(M, R), (x, 0, L)) / EI
    d['R'] = sp.solve(dUdR.subs(Q, 0), R)[0]                                   # 3wL/8
    d['MA'] = sp.simplify((M.subs({Q: 0, R: d['R']})).subs(x, L))             # −wL²/8
    d['th'] = sp.simplify((sp.integrate(M * sp.diff(M, Q), (x, 0, L)) / EI).subs({Q: 0, R: d['R']}))   # wL³/48EI
    d['R_settle'] = sp.simplify(sp.solve(dUdR.subs(Q, 0) + Dl, R)[0])         # 3wL/8 − 3EIΔ/L³
    d['R_spring'] = sp.simplify(sp.solve(dUdR.subs(Q, 0) + R / k, R)[0])      # 剛性 → 3wL/8
    d['R_spring_inf'] = sp.limit(d['R_spring'], k, sp.oo)
    d['Dl_zero'] = sp.solve(d['R_settle'], Dl)[0]                              # wL⁴/8EI
    return d


C8 = ch8()


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
    print('== 第 3 章補充')
    for k in ('M0sq', 'Umin_EI', 'U0_EI', 'Dl_ex', 'R_settle', 'Dl_zero', '13_Cx', '13_Cy', '13_eq1', '13_eq2', '13_th',
              '05_R', '05_MB', '05_MA', '08_R', '08_MB', '08_MC', '08_R_noratio'):
        v = C3X[k]
        try:
            print(f'  {k} = {v}  ({float(v):.4f})')
        except TypeError:
            print(f'  {k} = {v}')
    print('== 第 4 章')
    for k in ('16_Mmid', '16_dx', '16_dx_simpson', '16_th', '16_y0', '14_tri_R', '14_tri_P', '14_f11', '14_d10',
              'par_h', 'par_A', 'par_A_half', 'par_xbar_half', 'par_x_tri', 'par_x_tri_direct'):
        print(f'  {k} = {C4[k]}  ({float(C4[k]):.4f})')
    print('== 第 5 章')
    for k in ('MF', 'Mc_sym', 'R_sym', 'MA_sym', 'Mc_mid', 'Mc_ex', 'udl', '17_check', '17_mid', '17_m0_b', '17_m0_a', '17_r04'):
        print(f'  {k} = {C5[k]}')
    print('== 第 6 章')
    for k in ('12_expr', '12_Xr', '12_X', '12_X_rigid', '06_RD0', '06_RDinf', '06_DJ0', '06_DJinf', '06_RA0'):
        v = C6[k]
        try:
            print(f'  {k} = {v}  ({float(v):.4f})')
        except TypeError:
            print(f'  {k} = {v}')
    print('  2012-2 桿力:', {k: f'{float(v):.3f}' for k, v in C6['12_forces'].items()})
    print('== 第 7 章')
    print('  2018-3 兩索都當贅力:', [f'{float(v):.3f}' for v in C7['18_both']])
    print(f"  19_T = {C7['19_T']}")
    for k in ('18_X2', '18_vA', '18_MCm', '18_MCp', '18_Mcol', '18_vB', '19_P1', '19_k1', '19_k2', '19_P2', '19_U1', '19_U1b', '19_U2'):
        v = C7[k]
        print(f'  {k} = {v}  ({float(v):.4f})')
    print('  2019-1 一階段極限:', {k: f'{float(v):.2f}' for k, v in C7['19_lim1'].items()})
    print('  2019-1 P1 時桿力:', {k: f'{float(v):.2f}' for k, v in C7['19_stage1'].items()})
    print('== 第 8 章（綜合重建）')
    for k_, v in C8.items():
        print(f'  {k_} = {v}')
