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
