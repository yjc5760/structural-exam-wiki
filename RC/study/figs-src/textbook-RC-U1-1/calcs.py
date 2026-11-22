# -*- coding: utf-8 -*-
"""RC-U1-1 教科書講義：全部數值（圖與內文共用）。單位 kgf、cm；彎矩另列 tf·m。
執行 python3 calcs.py 印出全部數值，內文的數字一律抄這裡的輸出。

規範：建築物混凝土結構設計規範（112 年版，土木 401-112）。
  Es = 2.04e6 kgf/cm²；SD420 依 §21.2.2.1 取 εty = 0.002（φ 分區用）；判斷鋼筋降伏仍用 fy/Es。
"""
import math

ES = 2.04e6
ECU = 0.003
AB = {'D10': 0.7133, 'D13': 1.267, 'D16': 1.986, 'D19': 2.865, 'D22': 3.871, 'D25': 5.067, 'D29': 6.469, 'D32': 8.143}
DB = {'D10': 0.953, 'D13': 1.27, 'D16': 1.59, 'D19': 1.91, 'D22': 2.22, 'D25': 2.54, 'D29': 2.87, 'D32': 3.22}


def beta1(fc):
    if fc <= 280:
        return 0.85
    if fc >= 560:
        return 0.65
    return 0.85 - 0.05 * (fc - 280) / 70


def eps_ty(fy):
    """φ 分區用的 εty：SD420 規範允許取 0.002，其他 fy/Es。"""
    return 0.002 if abs(fy - 4200) < 1 else fy / ES


def phi_of(et, fy=4200):
    ety = eps_ty(fy)
    if et >= ety + 0.003:
        return 0.90
    if et <= ety:
        return 0.65
    return 0.65 + 0.25 * (et - ety) / 0.003


def tfm(m):  # kgf·cm → tf·m
    return m / 1e5


def ec(fc, k=15000):
    return k * math.sqrt(fc)


def fr(fc):
    return 2.0 * math.sqrt(fc)


def hognestad(e, fc, e0=0.002):
    """Hognestad 拋物線＋線性下降（0.003 時降到 0.925 峰值左右）。"""
    if e <= e0:
        return fc * (2 * e / e0 - (e / e0) ** 2)
    return fc * (1 - 0.15 * (e - e0) / (0.0038 - e0))


def stress_block_equiv(fc, ecu=0.003, n=4000):
    """以 Hognestad 曲線數值積分求 k1k3、k2，再反推等值矩形 α、β。"""
    # 以 c = 1 計：深度 y（0 在頂），應變 ecu*(1-y)
    s = 0.0; m = 0.0
    for i in range(n):
        y = (i + 0.5) / n
        e = ecu * (1 - y)
        sg = hognestad(e, fc)
        s += sg / n
        m += sg * y / n
    k1k3 = s / fc        # 平均應力 / f'c
    k2 = m / s           # 合力位置 / c
    beta = 2 * k2
    alpha = k1k3 / beta
    return dict(k1k3=k1k3, k2=k2, beta=beta, alpha=alpha)


def block_compare():
    """示範梁：用曲線模型（Hognestad，峰值 f'c）與規範應力塊各算一次 c 與力臂，看 Mn 差多少。"""
    D = demo_beam()
    E = stress_block_equiv(D['fc'])
    c_m = D['T'] / (E['k1k3'] * D['fc'] * D['b'])
    z_m = D['d'] - E['k2'] * c_m
    z_c = D['d'] - D['a'] / 2
    return dict(c_model=c_m, k2c=E['k2'] * c_m, z_model=z_m, c_code=D['c'], a2=D['a'] / 2, z_code=z_c,
                Mn_model=D['T'] * z_m, Mn_code=D['T'] * z_c, diff=(z_m - z_c) / z_c)


# ------------------------------------------------------------ 貫穿範例：示範梁
def demo_beam():
    b, h, d = 40.0, 60.0, 53.0
    n_bar = 4
    As = n_bar * AB['D25']
    fc, fy = 280.0, 4200.0
    b1 = beta1(fc)
    T = As * fy
    a = T / (0.85 * fc * b)
    c = a / b1
    et = ECU * (d - c) / c
    Mn = T * (d - a / 2)
    ph = phi_of(et, fy)
    # 最大鋼筋量（拉力控制 εt = 0.005）
    cmax = 3 / 8 * d
    amax = b1 * cmax
    Asmax = 0.85 * fc * amax * b / fy
    # 平衡
    cb = 6120 / (6120 + fy) * d
    Asb = 0.85 * fc * b1 * cb * b / fy
    rho_b = Asb / (b * d)
    # 最小鋼筋量
    asmin1 = 14 / fy * b * d
    asmin2 = 0.8 * math.sqrt(fc) / fy * b * d
    Asmin = max(asmin1, asmin2)
    # 開裂
    frr = fr(fc)
    Ig = b * h ** 3 / 12
    Mcr = frr * Ig / (h / 2)
    a_min = Asmin * fy / (0.85 * fc * b)
    Mn_min = Asmin * fy * (d - a_min / 2)
    # 素混凝土 vs As,min 的 φMn
    return dict(b=b, h=h, d=d, As=As, fc=fc, fy=fy, b1=b1, T=T, a=a, c=c, et=et, Mn=Mn, phi=ph,
                phiMn=ph * Mn, cmax=cmax, amax=amax, Asmax=Asmax, cb=cb, Asb=Asb, rho_b=rho_b,
                rho=As / (b * d), rho_max=Asmax / (b * d),
                asmin1=asmin1, asmin2=asmin2, Asmin=Asmin, fr=frr, Ig=Ig, Mcr=Mcr,
                a_min=a_min, Mn_min=Mn_min, ratio_min=0.9 * Mn_min / Mcr,
                Mn_max=Asmax * fy * (d - amax / 2))


def mn_rect(As, fc=280.0, fy=4200.0, b=40.0, d=53.0):
    a = As * fy / (0.85 * fc * b)
    return As * fy * (d - a / 2)


def sens():
    """示範梁各參數 +x% 時 Mn 的變化（拉力控制範圍內）。"""
    D = demo_beam()
    base = D['Mn']
    r = {}
    r['As+25%'] = mn_rect(D['As'] * 1.25) / base - 1
    r['fy 4200→5600'] = mn_rect(D['As'], fy=5600) / base - 1
    r['fc 280→350'] = mn_rect(D['As'], fc=350) / base - 1
    r['b 40→50'] = mn_rect(D['As'], b=50) / base - 1
    r['d 53→63'] = mn_rect(D['As'], d=63) / base - 1
    return r


def sweep_As(D=None, n=300):
    """固定示範梁斷面，As 由小到大掃描：回傳 (As, εt, φ, Mn, φMn) 列表；含過筋（鋼筋未降伏）的應變相容段。"""
    D = D or demo_beam()
    b, d, fc, fy, b1 = D['b'], D['d'], D['fc'], D['fy'], D['b1']
    out = []
    for i in range(1, n + 1):
        As = 80.0 * i / n
        a = As * fy / (0.85 * fc * b)
        c = a / b1
        es = ECU * (d - c) / c
        if es >= fy / ES:
            fs = fy
        else:
            # 鋼筋未降伏：0.85fc b β1 c = As Es 0.003 (d-c)/c
            A_ = 0.85 * fc * b * b1; B_ = As * ES * ECU; C_ = -As * ES * ECU * d
            c = (-B_ + math.sqrt(B_ * B_ - 4 * A_ * C_)) / (2 * A_)
            a = b1 * c
            es = ECU * (d - c) / c
            fs = ES * es
        Mn = As * fs * (d - a / 2)
        ph = phi_of(es, fy)
        out.append((As, es, ph, Mn, ph * Mn))
    return out


def phi_peak():
    """鋼筋降伏範圍內（εt ≥ εy）的 φMn 局部極大：應落在 εt = 0.005（拉力控制界限）。"""
    s = [r for r in sweep_As(n=4000) if r[1] >= 4200 / ES]
    best = max(s, key=lambda r: r[4])
    D = demo_beam()
    at_ey = s[-1]
    return dict(As=best[0], et=best[1], phiMn=best[4], As_ey=at_ey[0], phiMn_ey=at_ey[4], Mn_ey=at_ey[3],
                phiMn_max=0.9 * D['Mn_max'])


# ------------------------------------------------------------ 第 5 章：雙筋（示範梁加壓力筋）
def doubly_demo():
    D = demo_beam()
    b, d, fc, fy, b1 = D['b'], D['d'], D['fc'], D['fy'], D['b1']
    As = 6 * AB['D25']
    Asp = 2 * AB['D25']
    dp = 6.0
    # 每層 6 根排得下嗎：淨距
    clear = (b - 2 * 4.0 - 2 * DB['D10'] - 6 * DB['D25']) / 5
    # 先假設壓力筋降伏
    a0 = (As * fy - Asp * (fy - 0.85 * fc)) / (0.85 * fc * b)
    c0 = a0 / b1
    eps0 = ECU * (c0 - dp) / c0
    # 未降伏：0.85fc b β1 c + A's(6120(c-d')/c - 0.85fc) = As fy  → ×c
    A_ = 0.85 * fc * b * b1
    B_ = Asp * 6120 - Asp * 0.85 * fc - As * fy
    C_ = -Asp * 6120 * dp
    c = (-B_ + math.sqrt(B_ * B_ - 4 * A_ * C_)) / (2 * A_)
    c_neg = (-B_ - math.sqrt(B_ * B_ - 4 * A_ * C_)) / (2 * A_)
    a = b1 * c
    eps_p = ECU * (c - dp) / c
    fsp = ES * eps_p
    Cc = 0.85 * fc * a * b
    Cs = Asp * (fsp - 0.85 * fc)
    T = As * fy
    et = ECU * (d - c) / c
    Mn = Cc * (d - a / 2) + Cs * (d - dp)
    ph = phi_of(et, fy)
    # 若拿掉壓力筋（同 As 單筋）
    a1 = T / (0.85 * fc * b); c1 = a1 / b1; et1 = ECU * (d - c1) / c1
    Mn1 = T * (d - a1 / 2); ph1 = phi_of(et1, fy)
    # 錯法：直接當降伏
    Mn_wrong = 0.85 * fc * a0 * b * (d - a0 / 2) + Asp * (fy - 0.85 * fc) * (d - dp)
    # 門檻 c ≥ d'/(1-εy/0.003)
    ey = fy / ES
    cth = dp / (1 - ey / ECU)
    return dict(As=As, Asp=Asp, dp=dp, clear=clear, a0=a0, c0=c0, eps0=eps0, A=A_, B=B_, C=C_, c=c, c_neg=c_neg,
                a=a, eps_p=eps_p, fsp=fsp, Cc=Cc, Cs=Cs, T=T, et=et, Mn=Mn, phi=ph, phiMn=ph * Mn,
                a1=a1, c1=c1, et1=et1, Mn1=Mn1, ph1=ph1, phiMn1=ph1 * Mn1, Mn_wrong=Mn_wrong, ey=ey, cth=cth,
                ratio_cth=1 / (1 - ey / ECU))


def rc2024_2():
    """RC-2024-2：懸臂、底部受壓。b=30、d=52、d'=8、As 3-#10、A's 2-#10，fc=210、fy=4200。"""
    b, d, dp, fc, fy = 30.0, 52.0, 8.0, 210.0, 4200.0
    As, Asp = 3 * 8.14, 2 * 8.14
    b1 = beta1(fc)
    a0 = (As - Asp) * fy / (0.85 * fc * b)
    c0 = a0 / b1
    A_ = 0.85 * fc * b * b1; B_ = Asp * 6120 - As * fy; C_ = -Asp * 6120 * dp
    c = (-B_ + math.sqrt(B_ * B_ - 4 * A_ * C_)) / (2 * A_)
    a = b1 * c
    fsp = 6120 * (c - dp) / c
    Cc = 0.85 * fc * a * b; Cs = Asp * fsp
    et = ECU * (d - c) / c
    Mn = Cc * (d - a / 2) + Cs * (d - dp)
    wu = 2 * 0.9 * Mn / 300 ** 2 * 100 / 1000  # tf/m
    # 扣除壓力筋排開的混凝土（a > d′ 時）
    B2 = Asp * 6120 - Asp * 0.85 * fc - As * fy
    c2 = (-B2 + math.sqrt(B2 * B2 - 4 * A_ * C_)) / (2 * A_)
    a2 = b1 * c2
    fsp2 = 6120 * (c2 - dp) / c2
    Cc2 = 0.85 * fc * a2 * b; Cs2 = Asp * (fsp2 - 0.85 * fc)
    Mn2 = Cc2 * (d - a2 / 2) + Cs2 * (d - dp)
    wu2 = 2 * 0.9 * Mn2 / 300 ** 2 * 100 / 1000
    return dict(a0=a0, c0=c0, c=c, a=a, fsp=fsp, et=et, Mn=Mn, phiMn=0.9 * Mn, wu=wu,
                c_ded=c2, a_ded=a2, fsp_ded=fsp2, et_ded=ECU * (d - c2) / c2, Mn_ded=Mn2, phiMn_ded=0.9 * Mn2, wu_ded=wu2)


# ------------------------------------------------------------ 第 6 章：T 形梁
def tbeam_demo():
    """示範梁變成樓版系統中的內梁：bw=40、h=60、d=53、hf=12、跨度 L=800、梁中心距 400。As = 6-D25。"""
    bw, d, hf, L, s = 40.0, 53.0, 12.0, 800.0, 400.0
    fc, fy = 280.0, 4200.0
    be1, be2, be3 = L / 4, bw + 16 * hf, s
    be = min(be1, be2, be3)
    As = 6 * AB['D25']
    a = As * fy / (0.85 * fc * be)
    c = a / 0.85
    et = ECU * (d - c) / c
    Mn = As * fy * (d - a / 2)
    # 負彎矩：同一支梁在支承處 → 寬 bw 的矩形
    a_neg = As * fy / (0.85 * fc * bw)
    Mn_neg = As * fy * (d - a_neg / 2)
    a_wrong = a
    # 要多少鋼筋才會讓 a = hf
    As_hf = 0.85 * fc * be * hf / fy
    return dict(bw=bw, d=d, hf=hf, L=L, s=s, be1=be1, be2=be2, be3=be3, be=be, As=As, a=a, c=c, et=et,
                Mn=Mn, phiMn=0.9 * Mn, a_neg=a_neg, c_neg=a_neg / 0.85, et_neg=ECU * (d - a_neg / 0.85) / (a_neg / 0.85),
                Mn_neg=Mn_neg, As_hf=As_hf)


def rc2020_1():
    """RC-2020-1：be 三條件、Mu=130 tf·m 求 As（a > hf）。"""
    bw, d, hf, L, s = 50.0, 64.0, 10.0, 500.0, 400.0
    fc, fy, Mu = 210.0, 4200.0, 130e5
    be = min(L / 4, bw + 16 * hf, bw + (s - bw))
    # 矩形試算
    k = fy / (0.85 * fc * be)
    A2 = 0.9 * fy * k / 2; B2 = -0.9 * fy * d; C2 = Mu
    As_r = (-B2 - math.sqrt(B2 * B2 - 4 * A2 * C2)) / (2 * A2)
    a_r = k * As_r
    Cf = 0.85 * fc * (be - bw) * hf
    Asf = Cf / fy
    Mnf = Cf * (d - hf / 2)
    Mnw = Mu / 0.9 - Mnf
    kw = fy / (0.85 * fc * bw)
    A3 = fy * kw / 2; B3 = -fy * d; C3 = Mnw
    Asw = (-B3 - math.sqrt(B3 * B3 - 4 * A3 * C3)) / (2 * A3)
    aw = kw * Asw
    c = aw / 0.85
    et = ECU * (d - c) / c
    return dict(be=be, As_r=As_r, a_r=a_r, Cf=Cf, Asf=Asf, Mnf=Mnf, Asw=Asw, aw=aw, c=c, et=et, As=Asf + Asw)


def rc2024_1():
    d, bw, b, hf = 80.0, 40.0, 80.0, 20.0
    out = {}
    # Case 1
    fc, fy, eu = 280.0, 4200.0, 0.003
    c = eu / (eu + 0.005) * d; a = 0.85 * c
    C = 0.85 * fc * ((b - bw) * hf + bw * a)
    out['c1'] = c; out['a1'] = a; out['Asmax1'] = C / fy
    out['Asmin1'] = max(14 / fy, 0.8 * math.sqrt(fc) / fy) * bw * d
    # Case 2
    fc, fy, eu = 210.0, 6900.0, 0.004
    ey = fy / ES
    cb = eu / (eu + ey) * d; ab = 0.85 * cb
    out['ey2'] = ey; out['cb2'] = cb; out['Asb2'] = 0.85 * fc * ((b - bw) * hf + bw * ab) / fy
    lim = ey + 0.003
    c = eu / (eu + lim) * d; a = 0.85 * c
    out['lim2'] = lim; out['c2'] = c; out['a2'] = a
    out['Asmax2'] = 0.85 * fc * ((b - bw) * hf + bw * a) / fy
    return out


# ------------------------------------------------------------ 第 7 章：彎矩–曲率
def mphi(fc, b=40.0, h=60.0, d=53.0, As=None, fy=4200.0, k_ec=15000):
    As = As if As is not None else 4 * AB['D25']
    Ecc = ec(fc, k_ec)
    n = ES / Ecc
    rho = As / (b * d)
    k = -n * rho + math.sqrt((n * rho) ** 2 + 2 * n * rho)
    kd = k * d
    ey = fy / ES
    phy = ey / (d - kd)
    # 降伏時頂緣混凝土應變
    ec_top = phy * kd
    Icr = b * kd ** 3 / 3 + n * As * (d - kd) ** 2
    My = As * fy * (d - kd / 3)
    a = As * fy / (0.85 * fc * b)
    c = a / beta1(fc)
    phu = ECU / c
    Mn = As * fy * (d - a / 2)
    # 開裂（未開裂轉換斷面）
    frr = fr(fc)
    ybar = (b * h * h / 2 + (n - 1) * As * d) / (b * h + (n - 1) * As)
    It = b * h ** 3 / 12 + b * h * (h / 2 - ybar) ** 2 + (n - 1) * As * (d - ybar) ** 2
    yb = h - ybar
    Mcr = frr * It / yb
    phcr = frr / (Ecc * yb)
    return dict(fc=fc, Ec=Ecc, n=n, rho=rho, k=k, kd=kd, ey=ey, phy=phy, ec_top=ec_top, Icr=Icr, My=My,
                a=a, c=c, phu=phu, Mn=Mn, mu=phu / phy, Mcr=Mcr, phcr=phcr, ybar=ybar, It=It)


def mphi_doubly():
    """雙筋示範梁（第 5 章那支）的 kd：(n-1)A's。"""
    D = doubly_demo()
    b, d, fc, fy = 40.0, 53.0, 280.0, 4200.0
    n = ES / ec(fc)
    As, Asp, dp = D['As'], D['Asp'], D['dp']
    # b x²/2 + (n-1)A's (x-d') = n As (d-x)
    A_ = b / 2; B_ = (n - 1) * Asp + n * As; C_ = -((n - 1) * Asp * dp + n * As * d)
    x = (-B_ + math.sqrt(B_ * B_ - 4 * A_ * C_)) / (2 * A_)
    phy = (fy / ES) / (d - x)
    phu = ECU / D['c']
    # 同 As 單筋
    rho = As / (b * d)
    k = -n * rho + math.sqrt((n * rho) ** 2 + 2 * n * rho)
    x1 = k * d
    phy1 = (fy / ES) / (d - x1)
    phu1 = ECU / D['c1']
    return dict(n=n, x=x, phy=phy, phu=phu, mu=phu / phy, x1=x1, phy1=phy1, phu1=phu1, mu1=phu1 / phy1)


# ------------------------------------------------------------ 第 8 章：設計
def design_demo():
    """簡支梁 L=7 m，wD=2.5（含自重）、wL=1.8 tf/m → Mu → 反推 As → 選 4-D25 → 就是第 2 章那支梁。"""
    L, wD, wL = 7.0, 2.5, 1.8
    w14 = 1.4 * wD
    w = 1.2 * wD + 1.6 * wL
    Mu_tfm = w * L ** 2 / 8
    Mu = Mu_tfm * 1e5
    b, d, fc, fy = 40.0, 53.0, 280.0, 4200.0
    # 精確解 a
    a = d - math.sqrt(d * d - 2 * Mu / (0.85 * 0.9 * fc * b))
    As_req = 0.85 * fc * a * b / fy
    # 迭代 jd
    it = []
    jd = 0.9 * d
    for _ in range(3):
        As_i = Mu / (0.9 * fy * jd)
        a_i = As_i * fy / (0.85 * fc * b)
        it.append((jd, As_i, a_i))
        jd = d - a_i / 2
    n = math.ceil(As_req / AB['D25'])
    # 排筋：每排可放幾根 D25（b=40、保護層 4、箍筋 D10、淨距 max(2.5, db)）
    s_min = max(2.5, DB['D25'])
    avail = b - 2 * 4.0 - 2 * DB['D10']
    nmax = int((avail + s_min) // (DB['D25'] + s_min))
    clear4 = (avail - 4 * DB['D25']) / 3
    h_chk = 4.0 + DB['D10'] + DB['D25'] / 2
    return dict(L=L, wD=wD, wL=wL, w14=w14, w=w, Mu14=w14 * L ** 2 / 8, Mu_tfm=Mu_tfm, a=a, As_req=As_req,
                it=it, n=n, nmax=nmax, clear4=clear4, s_min=s_min, h_chk=h_chk)


def rc2019_1():
    """RC-2019-1：b=50、d=63、fc=210、fy=4200，φ 在過渡區，Mu 由題解 → 二次式 As。此處只驗算題解答案 44.9 cm²。"""
    b, d, fc, fy = 50.0, 63.0, 210.0, 4200.0
    As = 44.9
    a = As * fy / (0.85 * fc * b); c = a / 0.85
    et = ECU * (d - c) / c
    ph = phi_of(et, fy)
    Mn = As * fy * (d - a / 2)
    return dict(As=As, a=a, c=c, et=et, phi=ph, phiMn=ph * Mn)


def rc2016_1():
    L, wD, wL, ME = 7.5, 2.0, 1.0, 16.5
    MDe = wD * L ** 2 / 12; MLe = wL * L ** 2 / 12
    MDm = wD * L ** 2 / 24; MLm = wL * L ** 2 / 24
    return dict(end_g=1.2 * MDe + 1.6 * MLe, end_e=1.2 * MDe + 1.0 * MLe + ME, end_rev=-0.9 * MDe + ME,
                mid_g=1.2 * MDm + 1.6 * MLm)


def phi_line():
    return [(e, phi_of(e)) for e in [0.002, 0.003, 0.004, 0.005]]


if __name__ == '__main__':
    def show(name, dct):
        print(f'== {name}')
        for k, v in dct.items():
            if isinstance(v, float):
                print(f'  {k:10s} = {v:.6g}')
            else:
                print(f'  {k:10s} = {v}')

    print('β1(350)=', beta1(350), ' β1(420)=', beta1(420))
    show('Hognestad 等值', stress_block_equiv(280))
    show('示範梁', demo_beam())
    show('應力塊敏感度', block_compare())
    show('參數敏感度', sens())
    show('φMn 峰值', phi_peak())
    show('雙筋示範', doubly_demo())
    show('RC-2024-2', rc2024_2())
    show('T 形示範', tbeam_demo())
    show('RC-2020-1', rc2020_1())
    show('RC-2024-1', rc2024_1())
    show('Mφ fc=280', mphi(280))
    show('Mφ fc=210', mphi(210))
    show('Mφ 雙筋', mphi_doubly())
    show('設計', design_demo())
    show('RC-2019-1', rc2019_1())
    show('RC-2016-1', rc2016_1())
    print('φ line', phi_line())
    for fy in (2800, 4200, 5600, 6900):
        ety = eps_ty(fy); lim = ety + 0.003
        print(f'fy={fy}: εy={fy/ES:.5f} εty={ety:.5f} 界限={lim:.5f} cmax/d={0.003/(0.003+lim):.4f} cb/d={6120/(6120+fy):.4f} c/d′門檻={1/(1-fy/ES/0.003) if fy/ES<0.003 else float("inf"):.3f}')
