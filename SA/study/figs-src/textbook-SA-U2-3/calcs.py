# -*- coding: utf-8 -*-
"""SA-U2-3 傾角變位法 教科書講義：全部數值（圖與內文共用，先算再寫）。

單位：kN、m（貫穿範例 SA-2017-3）；推導用的係數一律以分數（fractions）精確計算。
符號約定（全書唯一要背的約定）：桿端彎矩 M、節點轉角 θ、弦轉角 ψ 皆「順時針為正」。

考題數字取自 raw/solutions/SA-2017-3/SA-2017-3.md（2026-08-26 FEM 符號勘誤、
2026-11-08 θA/θD 方向勘誤後版本）。
執行 `python3 calcs.py` 印出所有數值，與內文逐一對照。
"""
from fractions import Fraction as Fr


# ------------------------------------------------------------------ 共用：彈性曲線
def hermite(xi, vA, sA, vB, sB, L=1.0):
    """三次 Hermite 內插。v 向上為正；s = dv/dx（斜率）。回傳 v(xi·L)。"""
    H1 = 1 - 3 * xi**2 + 2 * xi**3
    H2 = xi - 2 * xi**2 + xi**3
    H3 = 3 * xi**2 - 2 * xi**3
    H4 = -xi**2 + xi**3
    return vA * H1 + sA * L * H2 + vB * H3 + sB * L * H4


def member_curve(thA, thB, dA=0.0, dB=0.0, L=1.0):
    """以「順時針為正」的端點轉角 θ 與端點位移（向上為正）給出 v(xi)。
    順時針轉角 θ ⇔ 斜率 dv/dx = −θ（x 向右、v 向上）。"""
    return lambda xi: hermite(xi, dA, -thA, dB, -thB, L)


# ------------------------------------------------------------------ 第 2 章：彎矩面積 → 1/3、1/6 → 4、2、½、6
def ch2():
    d = {}
    # 簡支梁 A 端施加順時針 M（L=1、EI=1 無因次）：M/EI 圖為三角形，A 端高 M、B 端 0
    area = Fr(1, 2)                         # 三角形面積 = ½·M·L/EI
    d['tBA'] = area * Fr(2, 3)              # B 點偏離 A 切線：面積 × 形心距 B（2L/3）= ML²/3EI
    d['tAB'] = area * Fr(1, 3)              # A 點偏離 B 切線：面積 × 形心距 A（L/3）= ML²/6EI
    d['near'] = d['tBA']                    # θ_A = t_BA / L = ML/3EI
    d['far'] = d['tAB']                     # |θ_B| = t_AB / L = ML/6EI（方向相反）
    # 柔度矩陣（順時針為正）：[θA, θB] = (L/EI)·[[1/3, −1/6], [−1/6, 1/3]]·[MA, MB]
    f11, f12 = d['near'], -d['far']
    det = f11 * f11 - f12 * f12
    d['k_near'] = f11 / det                 # 4
    d['k_far'] = -f12 / det                 # 2
    d['carry'] = d['k_far'] / d['k_near']   # 1/2
    # 鎖住 B、轉 θA：θB = 0 ⇒ MB/3 − MA/6 = 0 ⇒ MB = MA/2；θA = MA/3 − MB/6 = MA/4
    d['MB_over_MA'] = d['far'] / d['near']
    d['thA_per_MA'] = d['near'] - d['far'] * d['MB_over_MA']   # 1/4
    # ψ 狀態：θ 全部換成 θ−ψ，θA=θB=0 → −(4+2)ψ = −6ψ
    d['k_psi'] = d['k_near'] + d['k_far']   # 6
    d['k_psi_div2'] = d['k_psi'] / 2        # 3（主式括號內的 3ψ）
    # 剛體檢查：θA = θB = ψ 時 2(2θA+θB−3ψ) = 0
    d['rigid'] = 2 * (2 * 1 + 1 - 3 * 1)
    return d


# ------------------------------------------------------------------ 貫穿範例：SA-2017-3 門型剛架
EX = dict(Lc=4, Lb=6, w=45, P1=60, P2=60, yP2=2)   # 柱高、梁跨、kN/m、C 點節點載重(←)、右柱中點載重(←)、P2 距 D


def ex2017():
    e = dict(EX)
    Lc, Lb, w, P1, P2, yP = (Fr(e[k]) for k in ('Lc', 'Lb', 'w', 'P1', 'P2', 'yP2'))
    # 勁度係數（以 EI 為單位）
    e['kb'] = 2 / Lb                         # 梁 2EI/L = EI/3
    e['kc_full'] = 2 / Lc                    # 柱 2EI/L = EI/2（完整式）
    e['kc_pin'] = 3 / Lc                     # 柱 3EI/L = 3EI/4（鉸端修正式）
    # 固端彎矩（第 3 章）
    e['MF_BC'] = -w * Lb**2 / 12             # −135
    e['MF_CB'] = +w * Lb**2 / 12             # +135
    e['MF_DC'] = +P2 * Lc / 8                # 向左的載重攤平後朝上 → 整組反號：+30
    e['MF_CD'] = -P2 * Lc / 8                # −30
    e['MFm_CD'] = e['MF_CD'] - e['MF_DC'] / 2   # 修正固端彎矩 −45（第 4 章）
    # 層剪力：H_A=(M_AB+M_BA)/Lc；H_D=(M_DC+M_CD+P2·(Lc−yP2))/Lc；H_A+H_D=P1+P2
    #   ⇒ M_BA + M_CD = (P1+P2)·Lc − P2·(Lc−yP2) = 480 − 120 = 360
    e['story_rhs'] = (P1 + P2) * Lc - P2 * (Lc - yP)
    kc, kb = e['kc_pin'], e['kb']
    # 未知數 t=EIθB、s=EIθC、p=EIψ
    A = [[kc + 2 * kb, kb, -kc],             # 節點 B：M_BA + M_BC = 0
         [kb, 2 * kb + kc, -kc],             # 節點 C：M_CB + M_CD = 0
         [kc, kc, -2 * kc]]                  # 層剪力：M_BA + M_CD = 360
    b = [-e['MF_BC'], -(e['MF_CB'] + e['MFm_CD']), e['story_rhs'] - e['MFm_CD']]
    t, s, p = solve3(A, b)
    e['t'], e['s'], e['p'] = t, s, p
    e['M_BA'] = kc * (t - p)
    e['M_BC'] = kb * (2 * t + s) + e['MF_BC']
    e['M_CB'] = kb * (2 * s + t) + e['MF_CB']
    e['M_CD'] = kc * (s - p) + e['MFm_CD']
    # 反求柱底轉角（完整式＋M=0）
    e['thA'] = (3 * p - t) / 2                                  # (EI/2)(2θA+θB−3ψ)=0
    e['thD'] = (3 * p - s - e['MF_DC'] / e['kc_full']) / 2      # (EI/2)(2θD+θC−3ψ)+30=0
    # 第 2 章：把答案代回柱 AB 的完整式，自我檢查
    e['chk_MAB'] = e['kc_full'] * (2 * e['thA'] + t - 3 * p)
    e['chk_MBA'] = e['kc_full'] * (2 * t + e['thA'] - 3 * p)
    e['chk_MDC'] = e['kc_full'] * (2 * e['thD'] + s - 3 * p) + e['MF_DC']
    e['EIDelta'] = p * Lc                    # EIΔ（向右為正；負＝向左）
    return e


def ex2017_shape(EI=3600.0, n=60):
    """SA-2017-3 的真實彈性曲線（傾角變位解＋桿上載重的固端撓度），回傳整體座標（m）的點列。
    EI 只是放大倍率：取 3600 kN·m² 時側移 |Δ| = 1800/3600 = 0.5 m，方便作圖。"""
    e = ex2017()
    t, s, p, tA, tD = (float(e[k]) / EI for k in ('t', 's', 'p', 'thA', 'thD'))
    Lc, Lb, w, P2 = e['Lc'], e['Lb'], e['w'], e['P2']
    D = p * Lc                               # 側移（向右為正）
    out = {}
    # 柱 AB：局部 x 由 A 往上，v 指向左（局部 x 逆轉 90°）；水平位移 u = −v
    pts = []
    for i in range(n + 1):
        xi = i / n
        v = hermite(xi, 0, -tA, -D, -t, Lc)
        pts.append((0 - v, Lc * xi))
    out['AB'] = pts
    # 梁 BC：局部 x 向右、v 向上；端點無垂直位移；加均布載重的兩端固定撓度（向下）
    pts = []
    for i in range(n + 1):
        xi = i / n
        x = Lb * xi
        v = hermite(xi, 0, -t, 0, -s, Lb) - w * x**2 * (Lb - x)**2 / (24 * EI)
        pts.append((x + D, Lc + v))
    out['BC'] = pts
    # 柱 DC：局部 x 由 D 往上，v 指向左；中點載重向左＝局部 +v，加兩端固定的集中載重撓度
    pts = []
    for i in range(n + 1):
        xi = i / n
        x = Lc * xi
        xx = min(x, Lc - x)
        vp = P2 * xx**2 * (3 * Lc - 4 * xx) / (48 * EI)
        v = hermite(xi, 0, -tD, -D, -s, Lc) + vp
        pts.append((Lb - v, x))
    out['DC'] = pts
    out['D'] = D
    return out



# ------------------------------------------------------------------ 第 3 章：固端彎矩（兩端夾死）＝ 兩個條件：M/EI 總面積 = 0、對一端的一次矩 = 0
def ch3():
    d = {}
    # 對稱載重：兩端彎矩大小相同 M0（上緣受拉）。條件「總面積 = 0」⇒ M0·L = 簡支彎矩圖面積
    d['udl_Mmax'] = Fr(1, 8)                      # 簡支最大彎矩 wL²/8
    d['udl_area'] = Fr(2, 3) * d['udl_Mmax']      # 拋物線面積 = (2/3)·(wL²/8)·L = wL³/12
    d['udl_MF'] = d['udl_area']                   # M0 = 面積/L = wL²/12
    d['P_Mmax'] = Fr(1, 4)                        # 簡支最大彎矩 PL/4
    d['P_area'] = Fr(1, 2) * d['P_Mmax']          # 三角形面積 = ½·(PL/4)·L = PL²/8
    d['P_MF'] = d['P_area']                       # PL/8
    # 偏心集中載重（a、b 取 a = L/4 當數值例；通式見內文）
    a, b = Fr(1, 4), Fr(3, 4)
    area = a * b / 2                              # ½·(Pab/L)·L
    xbar = (1 + a) / 3                            # 三角形形心距 A：(L+a)/3
    # 端彎矩圖（上緣受拉）：梯形 MA→MB；面積 (MA+MB)/2；對 A 一次矩 MA/6 + MB/3
    # 條件：(MA+MB)/2 = area；MA/6 + MB/3 = area·xbar
    s1 = 2 * area                                 # MA + MB
    s2 = 6 * area * xbar                          # MA + 2MB
    d['ecc_a'], d['ecc_b'] = a, b
    d['ecc_MB'] = s2 - s1                         # = a²b
    d['ecc_MA'] = s1 - d['ecc_MB']                # = ab²
    d['ecc_chkA'] = a * b * b
    d['ecc_chkB'] = a * a * b
    # SA-2012-3：頂梁跨 4L，距兩端 L 處各一個 P（以 PL 為單位）
    Ls = Fr(4)
    d['s12_each'] = [Fr(1) * 3**2 / Ls**2, Fr(3) * 1**2 / Ls**2]   # P·a·b²/L²：a=1,b=3 → 9/16；a=3,b=1 → 3/16
    d['s12_MF'] = sum(d['s12_each'])              # 12/16 = 3/4
    d['s12_area'] = 1 * 2 + 2 * Fr(1, 2) * 1 * 1  # 簡支彎矩圖：梯形 PL 高、上底 2L、下底 4L → 3PL²
    d['s12_short'] = d['s12_area'] / Ls           # 3/4（對稱捷徑交叉驗算）
    # SA-2023-3：BC 跨 4 m 中點 50 kN 向上 → 整組反號
    d['s23_P'], d['s23_L'] = 50, 4
    d['s23_MF_BC'] = Fr(50 * 4, 8)                # +25
    d['s23_MF_CB'] = -Fr(50 * 4, 8)               # −25
    return d


# ------------------------------------------------------------------ 第 4 章：遠端鉸接 → 3EI/L 與修正固端彎矩
def ch4():
    d = {}
    d['k_pin'] = 1 / Fr(1, 3)                     # 遠端自由轉：θ = ML/3EI ⇒ M = 3EIθ/L
    d['k_fix'] = 4
    d['ratio'] = d['k_pin'] / d['k_fix']          # 3/4
    # 代換推導：M_BA = 0 ⇒ θB = (3ψ − θA)/2 − M_F,BA·L/(4EI)；代入 M_AB 得 (3EI/L)(θA−ψ) + (M_F,AB − ½M_F,BA)
    d['sub_coef'] = 2 * (2 - Fr(1, 2))            # (2EI/L)(2 − ½) = 3EI/L
    # 一端鉸接的固端彎矩（以 wL²、PL 為單位，取絕對值）
    d['pc_udl'] = Fr(1, 12) + Fr(1, 2) * Fr(1, 12)    # 1/8
    d['pc_P'] = Fr(1, 8) + Fr(1, 2) * Fr(1, 8)        # 3/16
    # 柱側移勁度預告：兩端固定 12、一端鉸 3（以 EI/L³）
    d['sway_fix'] = 2 * 6                         # 兩端各 6EIΔ/L²，剪力 = 12EIΔ/L³
    d['sway_pin'] = 3                             # 3EIΔ/L²／L
    # SA-2017-3（柱底鉸）
    e = ex2017()
    d['s17_MFm_CD'] = e['MFm_CD']
    d['s17_thA'], d['s17_thD'] = e['thA'], e['thD']
    # SA-2023-3：柱 AB 6 m，A 鉸；20 kN/m；BC、CD 各 4 m，D 固定，C 滾支（無側移）
    w, Lab, Lbc = 20, 6, 4
    MF_AB, MF_BA = Fr(w * Lab**2, 12), -Fr(w * Lab**2, 12)   # +60、−60（向左的均布 → 整組反號）
    MF_BC, MF_CB = Fr(50 * Lbc, 8), -Fr(50 * Lbc, 8)        # +25、−25（50 kN 向上）
    MFm_BA = MF_BA - MF_AB / 2                               # −90
    kAB = Fr(3, Lab)                                          # 3EI/6 = 0.5EI
    kBC = Fr(2, Lbc)                                          # 2EI/4 = 0.5EI
    kCD = Fr(2, Lbc)
    # 節點 B：kAB·t + MFm_BA + kBC(2t+s) + MF_BC = 0；節點 C：kBC(2s+t) + MF_CB + kCD·2s = 0
    A = [[kAB + 2 * kBC, kBC], [kBC, 2 * kBC + 2 * kCD]]
    b = [-(MFm_BA + MF_BC), -MF_CB]
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    t = (b[0] * A[1][1] - A[0][1] * b[1]) / det
    s_ = (A[0][0] * b[1] - b[0] * A[1][0]) / det
    d.update(s23_MF_AB=MF_AB, s23_MF_BA=MF_BA, s23_MFm_BA=MFm_BA, s23_kAB=kAB, s23_t=t, s23_s=s_,
             s23_M_BA=kAB * t + MFm_BA, s23_M_BC=kBC * (2 * t + s_) + MF_BC)
    # SA-2022-2：左柱 a–c 4 m，中點 30 kN；a 鉸
    d['s22_MF'] = Fr(30 * 4, 8)                   # 15
    d['s22_MFm_ca'] = d['s22_MF'] - Fr(1, 2) * (-d['s22_MF'])   # 15 + 7.5 = 22.5
    return d


# ------------------------------------------------------------------ 第 5 章：非均勻斷面（SA-2025-3：三段各 L/3，EI、2EI、EI）
def _pint(coefs, a, b):
    """∫_a^b Σ c_k u^k du（Fraction 精確積分）。coefs[k] = u^k 的係數。"""
    return sum(c * (Fr(b) ** (k + 1) - Fr(a) ** (k + 1)) / (k + 1) for k, c in enumerate(coefs))


def _pmul(p, q):
    out = [Fr(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


SEG25 = [(Fr(0), Fr(1, 3), Fr(1)), (Fr(1, 3), Fr(2, 3), Fr(2)), (Fr(2, 3), Fr(1), Fr(1))]   # (起, 迄, EI 倍數)


def flex(segs, fA, fB):
    """∫ fA(u)·fB(u)/EI(u) du（L=EI=1 無因次）；fA、fB 為多項式係數。"""
    return sum(_pint(_pmul(fA, fB), a, b) / r for a, b, r in segs)


def ch5(segs=SEG25):
    d = {}
    mA = [Fr(1), Fr(-1)]          # A 端加單位順時針彎矩：簡支梁彎矩圖 1−u（下緣受拉為正）
    mB = [Fr(0), Fr(-1)]          # B 端加單位順時針彎矩：−u
    d['fAA'] = flex(segs, mA, mA)                 # 47/162
    d['fBB'] = flex(segs, mB, mB)
    d['fAB'] = flex(segs, mA, mB)                 # −41/324（必為負）
    D = d['fAA'] * d['fBB'] - d['fAB'] ** 2
    d['D'] = D
    d['kAA'] = d['fBB'] / D                       # 1128/265
    d['kAB'] = -d['fAB'] / D                      # 492/265
    d['C'] = d['kAB'] / d['kAA']                  # 41/94
    d['kpsi'] = -(d['kAA'] + d['kAB'])            # −324/53
    # 跨中集中載重 P（L=P=1）：簡支彎矩 u/2（u≤½）、(1−u)/2（u≥½）；θ_A^(P) = ∫ M·m_A/EI
    def M_P_segs():
        out = []
        for a, b, r in segs:
            for lo, hi, poly in ((Fr(0), Fr(1, 2), [Fr(0), Fr(1, 2)]), (Fr(1, 2), Fr(1), [Fr(1, 2), Fr(-1, 2)])):
                x0, x1 = max(a, lo), min(b, hi)
                if x0 < x1:
                    out.append((x0, x1, r, poly))
        return out
    d['DeltaA'] = sum(_pint(_pmul(poly, mA), a, b) / r for a, b, r, poly in M_P_segs())   # 13/288
    d['DeltaB'] = sum(_pint(_pmul(poly, mB), a, b) / r for a, b, r, poly in M_P_segs())
    # 兩端夾死：fAA·MA + fAB·MB + ΔA = 0；fAB·MA + fBB·MB + ΔB = 0
    MA = (-d['DeltaA'] * d['fBB'] + d['DeltaB'] * d['fAB']) / D
    MB = (-d['fAA'] * d['DeltaB'] + d['fAB'] * d['DeltaA']) / D
    d['MF_AB'], d['MF_BA'] = MA, MB               # −13/120、+13/120
    d['fA_minus_fAB'] = d['fAA'] - d['fAB']       # 5/12
    return d


UNIFORM = [(Fr(0), Fr(1), Fr(1))]


# ------------------------------------------------------------------ 第 6 章：無側移結構
def ch6():
    d = {}
    # SA-2023-3：沿用第 4 章的解
    c4 = ch4()
    d['s23_t'], d['s23_s'] = c4['s23_t'], c4['s23_s']
    # SA-2019-3：三跨連續梁（各跨 L），B、C 等量沉陷 Δ。以 w、L、EI 為單位，係數存成 (Δ 的係數 EIΔ/L², wL² 的係數)
    # 修正式：M_BA = 3(θB − Δ/L) + (1/12 + 1/24) wL²；BC：M_BC = 2θB − wL²/12（θC = −θB、ψ=0）
    # 節點 B：5θB − 3Δ + wL²/24 = 0 → EIθB/L = (3/5)Δ − wL²/120（以 EIΔ/L²、wL² 計）
    tB = (Fr(3, 5), Fr(-1, 120))
    MBA = (3 * tB[0] - 3, 3 * tB[1] + Fr(1, 8))   # (−6/5, +1/10)
    d['s19_MBA'] = MBA
    # R_A = wL/2 − M_BA/L → 增量 = (6/5)EIΔ/L³ = 0.1 wL → Δ = wL⁴/12EI
    d['s19_dRA_coef'] = -MBA[0]                   # 6/5
    d['s19_Delta'] = Fr(1, 10) / d['s19_dRA_coef']   # 1/12（wL⁴/EI）
    # SA-2021-1：a 滾、b 彈簧 k=15000、c 內鉸、d 固定；ab=4（中點 36 kN）、b 點 36 kN、bc=4、cd=2；EI=10000
    EI, k, Lab, Lbc, Lcd, P = Fr(10000), Fr(15000), Fr(4), Fr(4), Fr(2), Fr(36)
    kc = 3 * EI / Lcd**3                          # 懸臂 cd 對 c 的等效彈簧 3750
    MF_ab, MF_ba = -P * Lab / 8, P * Lab / 8
    MFm_ba = MF_ba - MF_ab / 2                    # 27
    # 未知數 x = [θb, Δb, Δc]（Δ 向下為正）。M_ba = 3EI/4 (θb − Δb/4) + 27；M_bc = 3EI/4 (θb − (Δc−Δb)/4)
    a = 3 * EI / Lab
    def Mba(x): return a * (x[0] - x[1] / Lab) + MFm_ba
    def Mbc(x): return a * (x[0] - (x[2] - x[1]) / Lbc)
    # 方程：Mba+Mbc=0；kΔb = P + P/2 + Mba/4 − Mbc/4；kcΔc = Mbc/4（線性 → 用三個基底求係數）
    import itertools
    def F(x):
        return [Mba(x) + Mbc(x), k * x[1] - (P + P / 2 + Mba(x) / Lab - Mbc(x) / Lbc), kc * x[2] - Mbc(x) / Lbc]
    z = [Fr(0)] * 3
    f0 = F(z)
    A = [[F([Fr(int(i == j)) for j in range(3)])[r] - f0[r] for i in range(3)] for r in range(3)]
    sol = solve3(A, [-v for v in f0])
    d['s21_kc'] = kc
    d['s21_MFm_ba'] = MFm_ba
    d['s21_thb'], d['s21_Db'], d['s21_Dc'] = sol
    d['s21_Mba'], d['s21_Mbc'] = Mba(sol), Mbc(sol)
    d['s21_spring'] = k * sol[1]                  # 57 kN
    return d

def solve3(A, b):
    M = [list(map(Fr, r)) + [Fr(v)] for r, v in zip(A, b)]
    n = 3
    for i in range(n):
        piv = next(r for r in range(i, n) if M[r][i] != 0)
        M[i], M[piv] = M[piv], M[i]
        for r in range(n):
            if r != i:
                fac = M[r][i] / M[i][i]
                M[r] = [a - fac * c for a, c in zip(M[r], M[i])]
    return [M[i][n] / M[i][i] for i in range(n)]


def fmt(v, nd=2):
    if isinstance(v, Fr):
        if v.denominator == 1:
            return str(v.numerator)
        return f'{v} ≈ {float(v):.{nd}f}'
    return f'{v:.{nd}f}' if isinstance(v, float) else str(v)



# ------------------------------------------------------------------ 第 7 章：有側移剛架（層剪力方程、12EI/L³、短柱）
def story_rhs(loads):
    """層剪力方程（＝剛體虛功）右端：Σ(M_上+M_下) = −Σ P_x·y。
    loads = [(P_x 向右為正, 作用點距柱底高度 y)]；所有柱同高、柱底同高程時成立。"""
    return -sum(Fr(p) * Fr(y) for p, y in loads)


def ch7():
    d = {}
    # 柱側移勁度（以 EI/L³ 為單位）：兩端固定 θ=0 → 端彎矩各 −6EIΔ/L²，剪力 12EIΔ/L³；一端鉸 → 3
    d['k_ff'] = 2 * 6                             # 12
    d['k_fp'] = 3                                 # 3
    # 短柱：剛性梁、兩柱兩端固定、EI 相同，柱高 4 m 與 2 m，頂部水平力 90 kN
    h1, h2, P = Fr(4), Fr(2), Fr(90)
    k1, k2 = 12 / h1**3, 12 / h2**3               # 以 EI 為單位
    d['sc_k1'], d['sc_k2'] = k1, k2
    d['sc_ratio'] = k2 / k1                       # 8
    d['sc_V1'], d['sc_V2'] = P * k1 / (k1 + k2), P * k2 / (k1 + k2)   # 10、80
    d['sc_EIDelta'] = P / (k1 + k2)               # EIΔ
    # 柱頂彎矩：M = 6EIΔ/h²
    d['sc_M1'], d['sc_M2'] = 6 * d['sc_EIDelta'] / h1**2, 6 * d['sc_EIDelta'] / h2**2   # 20、80
    # SA-2017-3：層剪力方程右端由「外力 × 高度」直接得到
    d['s17_rhs'] = story_rhs([(-60, 4), (-60, 2)])            # 360
    e = ex2017()
    d['s17_HA'] = e['M_BA'] / 4                               # 70.10（柱底反力向右）
    d['s17_HD'] = (120 + e['M_CD']) / 4                       # 49.90
    VB = Fr(45 * 6, 2) - (e['M_BC'] + e['M_CB']) / 6          # 梁 B 端剪力（向上）＝柱 AB 軸力
    d['s17_VA'] = VB                                          # 195
    d['s17_VD'] = 45 * 6 - VB                                 # 75
    # 梁 BC 彎矩（下緣受拉為正）：M(x) = −M_BC·(−1)…：左端下緣受拉值 = +M_BC，右端 = −M_CB
    MB, MC = e['M_BC'], -e['M_CB']
    d['s17_beam_mid'] = (MB + MC) / 2 + Fr(45 * 36, 8)        # 102.12
    # 反曲點：M(x)=MB + (MC−MB)x/6 + 22.5x(6−x)=0
    a_, b_, c_ = -Fr(45, 2), (MC - MB) / 6 + Fr(45 * 6, 2), MB
    disc = float(b_**2 - 4 * a_ * c_)
    d['s17_x0'] = (-float(b_) + disc**0.5) / (2 * float(a_))  # 1.82 m
    # 右柱載重點彎矩：柱 DC 自 D 起，M_DC=0，柱頂 M_CD；載重點 y=2：柱 D 端剪力 × 2
    d['s17_col_load'] = d['s17_HD'] * 2                       # 99.8
    d['s17_ratio'] = e['M_BA'] / e['M_CD']                    # 3.52
    # 驗算：柱 AB 剪力 = (M_AB+M_BA)/4，方向
    # SA-2022-2：K = EI/4 = 10000；x=Kθc、y=Kθd、z=KΔ；ψ_ac = +Δ/4、ψ_de = −Δ/4（e 在上）
    MFm = Fr(45, 2)
    # M_ca = 3K(θc − Δ/4) + 22.5；M_cd = 2K(2θc+θd)；M_dc = 2K(2θd+θc)；M_de = 3K(θd + Δ/4) − 22.5
    def M22(x, y, z):
        return dict(ca=3 * x - Fr(3, 4) * z + MFm, cd=4 * x + 2 * y, dc=4 * y + 2 * x, de=3 * y + Fr(3, 4) * z - MFm)
    # 虛功：(M_ac+M_ca)(1/4) + (M_de+M_ed)(−1/4) + 30·(1/2) + 30·(1/2) = 0 → M_ca − M_de = −120
    d['s22_rhs'] = -4 * (30 * Fr(1, 2) + 30 * Fr(1, 2))       # −120
    def F22(v):
        m = M22(*v)
        return [m['ca'] + m['cd'], m['dc'] + m['de'], m['ca'] - m['de'] - d['s22_rhs']]
    z0 = [Fr(0)] * 3
    f0 = F22(z0)
    A = [[F22([Fr(int(i == j)) for j in range(3)])[r] - f0[r] for i in range(3)] for r in range(3)]
    x, y, z = solve3(A, [-v for v in f0])
    d['s22_x'], d['s22_y'], d['s22_z'] = x, y, z              # 30、−30、230
    m = M22(x, y, z)
    d.update({f's22_M{k}': v for k, v in m.items()})          # ca −60、cd 60、dc −60、de 60
    K = Fr(10000)
    d['s22_Dc_mm'] = z / K * 1000                             # 23
    # b 點：弦一半 + 彈性（簡支柱中點：P L³/48EI ＋ 端彎矩 |M| L²/16EI），EI = 40000
    EI, Lc = Fr(40000), Fr(4)
    d['s22_el_P'] = 30 * Lc**3 / 48                           # 40（/EI）
    d['s22_el_M'] = abs(m['ca']) * Lc**2 / 16                 # 60（/EI）
    d['s22_Db_mm'] = (z / K / 2 + (d['s22_el_P'] + d['s22_el_M']) / EI) * 1000   # 14
    # SA-2024-3：k = L_b/L；θ = 6k/(4k+3)·ψ；彎矩以 K_cψ 表示；側移勁度 PL/(K_cψ) = 3(8k+15)/(4k+3)
    def s24(k):
        k = Fr(k)
        th = 6 * k / (4 * k + 3)
        out = dict(th=th, MAB=2 * (th - 3), MBA=2 * (2 * th - 3), MBC=3 * th / k, MDC=Fr(-3))
        out['PL'] = -(out['MAB'] + out['MBA'] + out['MDC'])
        out['ratio'] = abs(out['MAB']) / abs(out['MBC'])
        return out
    d['s24'] = s24
    r = s24(Fr(3, 2))
    d['s24_k'] = Fr(3, 2)
    d['s24_ratio'] = r['ratio']                               # 2
    d['s24_PL'] = r['PL']                                     # 9
    d.update({f's24_{k}_PL': v / r['PL'] for k, v in r.items() if k.startswith('M')})   # 以 PL 表示
    d['s24_lim0'] = Fr(15)                                    # k→0：12 + 3
    d['s24_liminf'] = Fr(6)                                   # k→∞：3 + 3
    d['s24_sym_k'] = Fr(3)                                    # 誤當剛接對稱 → 3
    return d


# ------------------------------------------------------------------ 第 8 章：斜桿與非正交構架
def ch8():
    d = {}
    # SA-2020-1：ab 水平 4 m（a 固定）、bc 斜 4-3-5、c 靠垂直牆滾支承；68 kN 在 bc 中點
    # 位移：u_b = 0（ab 軸向）、u_c = 0（牆）；bc 軸向 → v_c = v_b = −Δ（向下 Δ）
    d['s20_Pn'] = Fr(68) * Fr(4, 5)                           # 54.4
    d['s20_Pa'] = Fr(68) * Fr(3, 5)                           # 40.8
    d['s20_MF'] = d['s20_Pn'] * 5 / 8                         # 34
    # 未知 t=EIθb、s=EIθc、D=EIΔ；ψ_ab = Δ/4、ψ_bc = 0
    def M(t, s, D):
        return dict(ab=Fr(1, 2) * (t - 3 * D / 4), ba=Fr(1, 2) * (2 * t - 3 * D / 4),
                    bc=Fr(2, 5) * (2 * t + s) - d['s20_MF'], cb=Fr(2, 5) * (2 * s + t) + d['s20_MF'])
    # 虛功：(M_ab+M_ba)·δΔ/4 + 68·δΔ = 0 → M_ab + M_ba = −272
    d['s20_vw'] = -68 * 4
    def F(v):
        m = M(*v)
        return [m['ba'] + m['bc'], m['cb'], m['ab'] + m['ba'] - d['s20_vw']]
    z0 = [Fr(0)] * 3
    f0 = F(z0)
    A = [[F([Fr(int(i == j)) for j in range(3)])[r] - f0[r] for i in range(3)] for r in range(3)]
    t, s, D = solve3(A, [-v for v in f0])
    d['s20_t'], d['s20_s'], d['s20_D'] = t, s, D              # 220、−152.5、2408/3
    m = M(t, s, D)
    d.update({f's20_M{k}': v for k, v in m.items()})          # ab −191、ba −81、bc 81、cb 0
    d['s20_Cx'] = (68 * 6 + m['ab']) / 3                      # 217/3（整體對 a 取矩，M_a 逆時針 191）
    # bc 中點彎矩（下緣受拉）：端點 +81→0 線性 + 法向載重三角形 P⊥L/4
    d['s20_bc_mid'] = m['bc'] / 2 + d['s20_Pn'] * 5 / 4      # 40.5 + 68 = 108.5
    # SA-2014-3：K = EI/L（DE 的 EI/L）；R = Δ/L；ψ：AB −R、BC +R、BD −2R、DE +2R
    s3 = 3 ** 0.5
    LDE = (s3 / 2, -1 / 2)                                    # D→E 單位向量（以 L 為長度）
    v = LDE[0] / (-LDE[1])                                    # u·ex + v·ey = 0 → v = u·(√3/2)/(1/2) = √3u
    d['s14_vD'] = s3                                          # D 上移 √3Δ
    d['s14_vD_chk'] = v
    d['s14_psi'] = dict(AB=Fr(-1), BC=Fr(1), BD=Fr(-2), DE=Fr(2))
    d['s14_psi_BD_chk'] = -s3 / (s3 / 2)                      # −2
    d['s14_psi_DE_chk'] = 2.0                                 # |D 位移| = 2Δ，桿長 L
    kAB, kBC, kBD, kDE = Fr(2), Fr(2), Fr(2), Fr(1)           # EI/L 倍數（2I/L、2I/L、√3I/(√3L/2)、I/L）
    psi = d['s14_psi']
    def M14(tB, tD, R):
        mm = {}
        mm['AB'] = 2 * kAB * (tB - 3 * psi['AB'] * R); mm['BA'] = 2 * kAB * (2 * tB - 3 * psi['AB'] * R)
        mm['BC'] = 2 * kBC * (2 * tB - 3 * psi['BC'] * R); mm['CB'] = 2 * kBC * (tB - 3 * psi['BC'] * R)
        mm['BD'] = 2 * kBD * (2 * tB + tD - 3 * psi['BD'] * R); mm['DB'] = 2 * kBD * (2 * tD + tB - 3 * psi['BD'] * R)
        mm['DE'] = 2 * kDE * (2 * tD - 3 * psi['DE'] * R); mm['ED'] = 2 * kDE * (tD - 3 * psi['DE'] * R)
        return mm
    PL = Fr(66 * 8)
    def F14(v):
        mm = M14(*v)
        vw = PL + (mm['AB'] + mm['BA']) * psi['AB'] + (mm['BC'] + mm['CB']) * psi['BC'] \
            + (mm['BD'] + mm['DB']) * psi['BD'] + (mm['DE'] + mm['ED']) * psi['DE']
        return [mm['BA'] + mm['BC'] + mm['BD'], mm['DB'] + mm['DE'], vw]
    z0 = [Fr(0)] * 3
    f0 = F14(z0)
    A = [[F14([Fr(int(i == j)) for j in range(3)])[r] - f0[r] for i in range(3)] for r in range(3)]
    tB, tD, R = solve3(A, [-v for v in f0])
    d['s14_tB'], d['s14_tD'], d['s14_R'] = tB, tD, R          # Kθ、KR（K = EI/L）
    d['s14_tB_R'], d['s14_tD_R'] = tB / R, tD / R             # −15/17、−12/17
    mm = M14(tB, tD, R)
    d.update({f's14_M{k}': v for k, v in mm.items()})
    d['s14_VAB'] = (mm['AB'] + mm['BA']) / 8
    d['s14_VBC'] = -(mm['BC'] + mm['CB']) / 8
    d['s14_rest'] = 66 - d['s14_VAB'] - d['s14_VBC']          # 由 BD–DE 傳到 E
    return d


# ------------------------------------------------------------------ 第 9 章：對稱／反對稱
def ch9():
    d = {}
    # SA-2020-2：EI=20000；未知 t=EIθb、D=EIΔ（b 下沉）；ψ_ab = Δ/4
    # 節點 b：M_ba + M_bc + M_bf = 0：(t − 3D/8) + (t/2 − 6) + 3t/2 = 0 → 3t − 3D/8 = 6
    # 節點 b 垂直：V_ba + V_bc = 0：(M_ab+M_ba)/4 + 6 = 0
    def M20(t, D):
        return dict(ab=Fr(1, 2) * (t - 3 * D / 4), ba=Fr(1, 2) * (2 * t - 3 * D / 4), bc=Fr(1, 2) * (2 * t - t) - 6,
                    bf=Fr(1, 2) * (2 * t + t))
    # 解 2×2
    a11, a12, b1 = Fr(3), Fr(-3, 8), Fr(6)
    a21, a22, b2 = Fr(3, 8), Fr(-3, 16), Fr(-6)
    det = a11 * a22 - a12 * a21
    t = (b1 * a22 - a12 * b2) / det
    D = (a11 * b2 - b1 * a21) / det
    m = M20(t, D)
    assert m['ba'] + m['bc'] + m['bf'] == 0 and (m['ab'] + m['ba']) / 4 + 6 == 0
    d['s20_t'], d['s20_D'] = t, D                             # 8、48
    d.update({f's20_M{k}': v for k, v in m.items()})          # ab −14、ba −10、bc −2、bf 12
    d['s20_theta'] = t / 20000
    d['s20_v_mm'] = D / 20000 * 1000                          # 2.40
    # SA-2021-2：反對稱 θb = θe = θ、θc = θd = φ；ψ = Δ/3；EI=20000
    def M21(t, p, s):
        return dict(ba=t, be=Fr(2, 6) * (2 * t + t), bc=Fr(2, 3) * (2 * t + p - 3 * s),
                    cb=Fr(2, 3) * (2 * p + t - 3 * s), cd=Fr(2, 6) * (2 * p + p))
    def F21(v):
        mm = M21(*v)
        return [mm['ba'] + mm['be'] + mm['bc'], mm['cb'] + mm['cd'], mm['bc'] + mm['cb'] + 36]
    z0 = [Fr(0)] * 3
    f0 = F21(z0)
    A = [[F21([Fr(int(i == j)) for j in range(3)])[r] - f0[r] for i in range(3)] for r in range(3)]
    t, p, s = solve3(A, [-v for v in f0])
    d['s21_t'], d['s21_p'], d['s21_s'] = t, p, s              # 10、16、22
    mm = M21(t, p, s)
    d.update({f's21_M{k}': v for k, v in mm.items()})         # ba 10、be 10、bc −20、cb −16、cd 16
    d['s21_D_mm'] = 3 * s / 20000 * 1000                      # 3.30
    d['s21_theta'] = t / 20000
    d['s21_story'] = story_rhs([(24, 3)]) / 2                 # 每根柱 M_bc + M_cb = −36
    # SA-2015-3：對稱於中柱 GD → θ_D = 0、無側移；C 鉸下陷 δ
    # M_BA = EIθB；M_BC = 3EI(θB − δ) − 0.5；M_DC = EIδ/3 + 4.5
    # 節點 B：4t − 3δ = 0.5；鉸 C 剪力：M_BC − M_DC/3 = −8
    a11, a12, b1 = Fr(4), Fr(-3), Fr(1, 2)
    a21, a22, b2 = Fr(3), -Fr(3) - Fr(1, 9), Fr(-8) + Fr(1, 2) + Fr(3, 2)
    det = a11 * a22 - a12 * a21
    t = (b1 * a22 - a12 * b2) / det
    dl = (a11 * b2 - b1 * a21) / det
    d['s15_t'], d['s15_d'] = t, dl                            # 176/31、459/62
    MAB, MBA = t / 2, t
    MBC = 3 * (t - dl) - Fr(1, 2)
    MDC = dl / 3 + Fr(9, 2)
    assert MBA + MBC == 0
    d.update(s15_MAB=MAB, s15_MBA=MBA, s15_MBC=MBC, s15_MDC=MDC)
    VC = 6 - MDC / 3                                          # 鉸 C 對 CD 的向上力 114/31
    d['s15_VC'] = VC
    d['s15_xmax'] = VC / 4                                    # 0.919 m
    d['s15_Mmax'] = VC**2 / 8                                 # 1.69
    VD = 6 + MDC / 3
    d['s15_Gy'] = 2 * VD                                      # 516/31
    d['s15_MFm_BC'] = -Fr(4 * 1, 8)                           # −wL²/8，L=1
    d['s15_MFm_DC'] = Fr(4 * 9, 8)                            # +wL²/8，L=3
    return d


# ------------------------------------------------------------------ 第 10 章：綜合重建（門型剛架、兩端固定、梁柱同 EI、同長 L，柱頂 P 向右）
def ch10():
    d = {}
    # 反對稱：θB = θC = θ；以 K = EI/L、ψ 為未知
    # M_AB = 2K(θ − 3ψ)、M_BA = 2K(2θ − 3ψ)、M_BC = 2K(3θ) = 6Kθ
    # 節點 B：10θ − 6ψ = 0 → θ = 3ψ/5
    th = Fr(3, 5)
    MAB, MBA, MBC = 2 * (th - 3), 2 * (2 * th - 3), 6 * th     # 以 Kψ 為單位
    PL = -2 * (MAB + MBA)                                     # 層剪力：2(M_AB+M_BA) = −PL
    d['th'] = th
    d['Kpsi'] = 1 / PL                                        # Kψ = PL·(…)
    d['MAB'], d['MBA'], d['MBC'] = MAB / PL, MBA / PL, MBC / PL   # 以 PL 為單位：−2/7、−3/14、3/14
    d['k_lat'] = PL                                           # P/Δ = (PL/Kψ)·EI/L³ → 84/5
    d['k_rigid'] = Fr(24)                                     # 梁剛性：2 × 12
    d['k_zero'] = Fr(6)                                       # 梁無勁度：2 × 3
    # 變化題 1：柱底改鉸（修正式）。M_BA = 3K(θ − ψ)、M_BC = 6Kθ → 9θ − 3ψ = 0 → θ = ψ/3
    thp = Fr(1, 3)
    MBAp = 3 * (thp - 1)
    PLp = -2 * MBAp                                           # 2·M_BA = −PL
    d['pin_th'] = thp
    d['pin_MBA'] = MBAp / PLp                                 # −1/2（以 PL）
    d['pin_k'] = PLp                                          # 4（×EI/L³）
    d['pin_k_rigid'] = Fr(6)                                  # 2 × 3
    # 變化題 2：梁受均布 w（對稱）：θC = −θB、無側移。M_BA = 4Kθ、M_BC = 2Kθ − wL²/12 → 6Kθ = wL²/12
    Kth = Fr(1, 72)                                           # 以 wL² 計
    d['g_Kth'] = Kth
    d['g_MAB'] = 2 * Kth                                      # 1/36
    d['g_MBA'] = 4 * Kth                                      # 1/18
    d['g_MBC'] = 2 * Kth - Fr(1, 12)                          # −1/18
    d['g_mid'] = Fr(1, 8) + d['g_MBC']                        # 跨中下緣受拉 1/8 − 1/18 = 5/72
    # 精選 5 題的對答案數字（沿用各章）
    c4, c5, c8 = ch4(), ch5(), ch8()
    d['p23_t'], d['p23_MBA'] = c4['s23_t'], c4['s23_M_BA']
    d['p25_kAA'], d['p25_kAB'], d['p25_C'], d['p25_MF'] = c5['kAA'], c5['kAB'], c5['C'], c5['MF_AB']
    d['p20_Mab'], d['p20_Mba'], d['p20_Cx'] = c8['s20_Mab'], c8['s20_Mba'], c8['s20_Cx']
    return d

if __name__ == '__main__':
    print('== 第 2 章（L=EI=1 無因次）==')
    for k, v in ch2().items():
        print(f'  {k:12s}', fmt(v))
    print('== 第 3 章 ==')
    for k, v in ch3().items():
        print(f'  {k:12s}', v if isinstance(v, list) else fmt(v))
    print('== 第 4 章 ==')
    for k, v in ch4().items():
        print(f'  {k:12s}', fmt(v))
    print('== 第 5 章（SA-2025-3）==')
    for k, v in ch5().items():
        print(f'  {k:12s}', fmt(v))
    print('== 第 5 章（均勻梁驗核）==')
    for k, v in ch5(UNIFORM).items():
        print(f'  {k:12s}', fmt(v))
    print('== 第 6 章 ==')
    for k, v in ch6().items():
        print(f'  {k:12s}', v if isinstance(v, tuple) else fmt(v))
    print('== SA-2017-3（kN、m；θ、ψ 以 EI·θ 表示）==')
    for k, v in ex2017().items():
        print(f'  {k:12s}', fmt(v))
    for nm, fn in (('第 7 章', ch7), ('第 8 章', ch8), ('第 9 章', ch9), ('第 10 章', ch10)):
        print(f'== {nm} ==')
        for k, v in fn().items():
            if callable(v):
                continue
            print(f'  {k:14s}', v if isinstance(v, (dict, tuple)) else fmt(v))
