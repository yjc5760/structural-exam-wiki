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
    print('== SA-2017-3（kN、m；θ、ψ 以 EI·θ 表示）==')
    for k, v in ex2017().items():
        print(f'  {k:12s}', fmt(v))
