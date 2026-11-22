# -*- coding: utf-8 -*-
"""RC-U1-2 教科書講義（柱強度）：全部數值（圖與內文共用）。單位 kgf、cm；力另列 tf、彎矩 tf·m。
執行 python3 calcs.py 印出全部數值，內文的數字一律抄這裡的輸出。

規範：建築物混凝土結構設計規範（112 年版，土木 401-112／ACI 318-19 世代）。
  Es = 2.04e6 kgf/cm²；判斷鋼筋降伏用 εy = fy/Es = 0.002059；
  φ 分區依表 21.2.2，SD420 依 §21.2.2.1 取 εty = 0.002，拉力控制界限 0.005。
符號：應變、力以「壓為正」；彎矩對斷面幾何形心取矩，使壓力側受壓者為正。
"""
import math

ES = 2.04e6
ECU = 0.003


def beta1(fc):
    if fc <= 280:
        return 0.85
    if fc >= 560:
        return 0.65
    return 0.85 - 0.05 * (fc - 280) / 70


def phi_col(et, spiral=False, ety=0.002):
    lo = 0.75 if spiral else 0.65
    if et <= ety:
        return lo
    if et >= ety + 0.003:
        return 0.90
    return lo + (0.90 - lo) * (et - ety) / 0.003


def tf(x):
    return x / 1000.0


def tfm(m):
    return m / 1e5


class Col:
    """矩形斷面，多層鋼筋。layers = [(距壓力面 cm, 面積 cm²)]。"""

    def __init__(self, b, h, layers, fc, fy, name=''):
        self.b, self.h, self.layers, self.fc, self.fy, self.name = b, h, layers, fc, fy, name
        self.b1 = beta1(fc)
        self.ey = fy / ES
        self.Ast = sum(A for _, A in layers)
        self.Ag = b * h
        self.dt = max(d for d, _ in layers)

    def at(self, c, deduct=True):
        """給中性軸 c，回傳完整狀態。c 可大於 h（a 以 h 為上限）。"""
        b1, fc, fy = self.b1, self.fc, self.fy
        a = min(b1 * c, self.h)
        Cc = 0.85 * fc * a * self.b
        rows = []
        P = Cc
        M = Cc * (self.h / 2 - a / 2)
        for d, A in self.layers:
            e = ECU * (c - d) / c
            fs = max(-fy, min(fy, ES * e))
            inblock = (d < a) and fs > 0
            fnet = fs - 0.85 * fc if (inblock and deduct) else fs
            F = A * fnet
            P += F
            M += F * (self.h / 2 - d)
            rows.append(dict(d=d, A=A, eps=e, fs=fs, inblock=inblock, fnet=fnet, F=F, arm=self.h / 2 - d,
                             yld=abs(e) >= self.ey))
        et = -ECU * (c - self.dt) / c   # 最外拉力筋拉應變（拉為正）
        ph = phi_col(et)
        return dict(c=c, a=a, Cc=Cc, rows=rows, P=P, M=M, et=et, phi=ph, e=(M / P if abs(P) > 1e-9 else float('inf')))

    def P0(self):
        return 0.85 * self.fc * (self.Ag - self.Ast) + self.fy * self.Ast

    def cb(self):
        return ECU / (ECU + self.ey) * self.dt

    def c_tc(self):  # εt = 0.005
        return ECU / (ECU + 0.005) * self.dt

    def solve(self, fn, target, lo=0.5, hi=None, n=200):
        """以二分法求 c 使 fn(state) = target（fn 對 c 單調）。"""
        hi = hi or 3 * self.h
        f_lo = fn(self.at(lo)) - target
        for _ in range(n):
            mid = (lo + hi) / 2
            fm = fn(self.at(mid)) - target
            if (fm > 0) == (f_lo > 0):
                lo, f_lo = mid, fm
            else:
                hi = mid
        return (lo + hi) / 2

    def c_for_P(self, P):
        return self.solve(lambda s: s['P'], P)

    def c_pure_bending(self):
        return self.solve(lambda s: s['P'], 0.0)

    def c_for_e(self, e):
        # e = M/P；在壓力區 P>0 時 e 隨 c 增加而減小
        return self.solve(lambda s: -s['M'] / s['P'] if s['P'] > 0 else -1e9, -e, lo=self.c_pure_bending() + 1e-3)

    def curve(self, n=160, cmax_factor=4.0):
        """互制圖：c 從純彎點到很大；回傳 [(M, P, φ, c)]，P 不截頂。"""
        c0 = self.c_pure_bending()
        pts = []
        for i in range(n + 1):
            c = c0 * (cmax_factor * self.h / c0) ** (i / n)
            s = self.at(c)
            pts.append((s['M'], s['P'], s['phi'], c))
        pts.append((0.0, self.P0(), 0.65, float('inf')))
        return pts


# ---------------------------------------------------------------- 示範柱 = RC-2024-3
AB8 = 5.07
DEMO = Col(40, 40, [(8, 3 * AB8), (20, 2 * AB8), (32, 3 * AB8)], 280, 4200, '示範柱 RC-2024-3')


def demo():
    D = DEMO
    s32 = D.at(32.0)                  # εt = 0（RC-2024-3）
    cb = D.cb(); sb = D.at(cb)
    ct = D.c_tc(); st = D.at(ct)
    c0 = D.c_pure_bending(); s0 = D.at(c0)
    P0 = D.P0()
    Pmax = 0.80 * P0
    # Mn 峰值掃描
    best = max((D.at(c / 100.0)['M'], c / 100.0) for c in range(500, 6000))
    bestphi = max((D.at(c / 100.0)['M'] * D.at(c / 100.0)['phi'], c / 100.0) for c in range(500, 6000))
    # 0.80P0 截頂時的 c（φ=0.65）
    c_cap = D.c_for_P(Pmax)
    return dict(D=D, s32=s32, cb=cb, sb=sb, ct=ct, st=st, c0=c0, s0=s0, P0=P0, Pmax=Pmax,
                phiPmax=0.65 * Pmax, Mpk=best[0], c_Mpk=best[1], phiMpk=bestphi[0], c_phiMpk=bestphi[1],
                c_cap=c_cap, s_cap=D.at(c_cap), rhog=D.Ast / D.Ag)


# ---------------------------------------------------------------- 考古題
def rc2021_2():
    C = Col(50, 50, [(6.5, 3 * 5.067), (25, 2 * 5.067), (43.5, 3 * 5.067)], 280, 4200, 'RC-2021-2')
    return C, C.at(14.5)


def rc2008_2():
    C = Col(40, 56, [(8, 4 * 5.07), (28, 2 * 5.07), (48, 2 * 5.07)], 350, 4200, 'RC-2008-2')
    return C, C.at(48.0)


def rc2019_2():
    C = Col(50, 70, [(7, 5 * 5.07), (63, 5 * 5.07)], 280, 4200, 'RC-2019-2')
    Pn = 291000 / 0.65
    c = C.c_for_P(Pn)
    return C, C.at(c), Pn


def rc2002_2():
    C = Col(30, 40, [(7, 3 * 6.47), (33, 3 * 6.47)], 280, 4200, 'RC-2002-2')
    c = C.c_for_e(10.0)
    return C, C.at(c), C.at(C.cb())


def rc2015_1():
    C = Col(60, 60, [(8, 4 * 8.143), (52, 4 * 8.143)], 350, 4200, 'RC-2015-1')
    sb = C.at(C.cb()); st = C.at(C.c_tc()); s0 = C.at(C.c_pure_bending())
    scan = [(c, C.at(c)) for c in (15.0, 17.0, C.c_tc(), 21.0, 23.0, 26.0, 28.0, C.cb())]
    return C, sb, st, s0, scan


def rc2011_3():
    C = Col(40, 60, [(6, 3 * 8.143), (54, 3 * 8.143)], 350, 4200, 'RC-2011-3')
    sb = C.at(C.cb())
    Pn = 0.9 * sb['P']
    c = C.c_for_P(Pn)
    s = C.at(c)
    # 曲率韌性：使用軸力 N = Pn/1.3
    N = Pn / 1.3
    Ec = 15000 * math.sqrt(C.fc)
    ey = C.ey
    As, Asp, d, dp, b = 3 * 8.143, 3 * 8.143, 54.0, 6.0, 40.0

    def resid(k):
        return 0.5 * Ec * ey / (d - k) * k * b * k + Asp * (ES - Ec) * ey * (k - dp) / (d - k) - (N + As * C.fy)

    lo, hi = 1.0, 53.0
    for _ in range(200):
        m = (lo + hi) / 2
        if resid(m) > 0:
            hi = m
        else:
            lo = m
    k = (lo + hi) / 2
    phy = ey / (d - k)
    cu = C.c_for_P(N)
    phu = ECU / cu
    return dict(C=C, sb=sb, Pn=Pn, s=s, N=N, Ec=Ec, k=k, phy=phy, cu=cu, phu=phu, mu=phu / phy,
                ec_y=phy * k)


def mu_phi_2011(N):
    """RC-2011-3 斷面在軸力 N（kgf）下的 φy、φu、μφ（同題解方法）。"""
    C = Col(40, 60, [(6, 3 * 8.143), (54, 3 * 8.143)], 350, 4200)
    Ec = 15000 * math.sqrt(350); ey = C.ey
    As = Asp = 3 * 8.143; d, dp, b = 54.0, 6.0, 40.0
    def resid(k):
        return 0.5 * Ec * ey / (d - k) * k * b * k + Asp * (ES - Ec) * ey * (k - dp) / (d - k) - (N + As * C.fy)
    lo, hi = 1.0, 53.0
    for _ in range(200):
        m = (lo + hi) / 2
        if resid(m) > 0:
            hi = m
        else:
            lo = m
    k = (lo + hi) / 2
    phy = ey / (d - k)
    cu = C.c_for_P(N)
    return dict(k=k, phy=phy, cu=cu, phu=ECU / cu, mu=(ECU / cu) / phy)


def mu_delta(mu_phi, Lp_L):
    return 1 + 3 * (mu_phi - 1) * Lp_L * (1 - 0.5 * Lp_L)


def rc2010_1():
    D, Dc, fc, fy = 75.0, 68.0, 350.0, 4200.0
    Ag = math.pi * D ** 2 / 4
    Ach = math.pi * Dc ** 2 / 4
    Ast = 12 * 8.17
    Asp, db, s = 1.27, 1.27, 8.0
    Py = 0.85 * fc * (Ag - Ast) + fy * Ast
    rho_min = 0.45 * (Ag / Ach - 1) * fc / fy
    rho_th = 0.85 / 2.05 * (Ag / Ach - 1) * fc / fy
    s_rho = 4 * Asp / (rho_min * Dc)
    s_clear = 7.5 + db
    rho = 4 * Asp / (Dc * s)
    fL = rho * fy / 2
    fcc = fc + 4.1 * fL
    loss = 0.85 * fc * (Ag - Ach)
    gain = 4.1 * fL * Ach
    Pu = 0.85 * fc * (Ach - Ast) + 4.1 * fL * Ach + fy * Ast
    return dict(Ag=Ag, Ach=Ach, Ast=Ast, Py=Py, rho_min=rho_min, rho_th=rho_th, s_rho=s_rho, s_clear=s_clear,
                rho=rho, fL=fL, fcc=fcc, loss=loss, gain=gain, Pu=Pu, phiPmax=0.85 * 0.75 * Py, s=s, Dc=Dc, D=D)


def fc_2017(e, fc=210.0):
    """RC-2017-1 考卷圖 2 的雙折線：0→0.002 直線升到 f'c，之後每 0.001 降 0.2f'c。"""
    if e <= 0.002:
        return fc * e / 0.002
    return fc * (1 - 0.2 * (e - 0.002) / 0.001)


def rc2017_1():
    Ac, Ast = 2800 - 16 * 5.067, 16 * 5.067
    def P(e):
        return fc_2017(e) * Ac + min(ES * e, 4200) * Ast
    best = max((P(i / 1e6), i / 1e6) for i in range(500, 3001))
    Po = 0.85 * 210 * Ac + 4200 * Ast
    return dict(Ac=Ac, Ast=Ast, Ppk=best[0], e_pk=best[1], P003=P(0.003), Po=Po, phiPmax=0.80 * 0.65 * Po, P=P,
                Mnb=98.04, Pnb=211.7)


def rc2017_2():
    Vu = 195742.0
    Avf = Vu / (0.75 * 1.0 * 4200)
    return dict(Vu=Vu, Avf=Avf, n=math.ceil(Avf / 3.871))


def rc2006_2():
    Ig_Ec = 130727e6      # Ec·Ig（題解值，kgf·cm²）
    EI = 0.4 * Ig_Ec / 1.3
    klu = 540.0
    Pc = math.pi ** 2 * EI / klu ** 2
    Cm = 0.6 + 0.4 * 15 / 27
    Pu = 400e3
    dns = Cm / (1 - Pu / (0.75 * Pc))
    return dict(EI=EI, Pc=Pc, Cm=Cm, Pu=Pu, x=Pu / (0.75 * Pc), dns=dns, Mc=dns * 27, M2min=Pu * (1.5 + 0.03 * 50) / 1e5, r=0.3 * 50, klr=540 / 15)


def rc2016_3():
    h = 40.0
    r = 0.3 * h
    klr = 0.9 * 800 / r
    lim = min(34 + 12 * 0.875, 40)
    Ec = 15000 * math.sqrt(280)
    Ig = h ** 4 / 12
    EI = 0.25 * Ec * Ig
    Pc = math.pi ** 2 * EI / (0.9 * 800) ** 2
    Cm = 0.6 - 0.4 * 0.875
    Pu = 130e3
    x = Pu / (0.75 * Pc)
    return dict(r=r, klr=klr, lim=lim, Ec=Ec, Ig=Ig, EI=EI, Pc=Pc, Cm=Cm, Pu=Pu, x=x, dns_raw=Cm / (1 - x), dns=max(1.0, Cm / (1 - x)))


def amp_curve(x):
    """放大係數 1/(1-x)，x = Pu/(0.75Pc)。"""
    return 1 / (1 - x)


def rc2013_2():
    b, cc, fc, fyt, s = 50.0, 4.0, 280.0, 2800.0, 12.0
    hc = b - 2 * cc
    Ag, Ach = b * b, hc * hc
    a1 = 0.3 * hc * (Ag / Ach - 1) * fc / fyt
    a2 = 0.09 * hc * fc / fyt
    hx = (hc - 2 * 1.27 - 3.22) / 4
    return dict(hc=hc, Ag=Ag, Ach=Ach, a1=a1, a2=a2, per_s=max(a1, a2), req=max(a1, a2) * s, s=s, hx=hx,
                so_raw=10 + (35 - hx) / 3, so=so(hx), b4=b / 4, six_db=6 * 3.22, legs=math.ceil(max(a1, a2) * s / 1.27))


def so(hx):
    return max(10.0, min(15.0, 10 + (35 - hx) / 3))


if __name__ == '__main__':
    R = demo(); D = R['D']
    print('== 示範柱 RC-2024-3：40×40，3-2-3 #8，fc 280 fy 4200')
    print(f"Ast={D.Ast:.2f} ρg={R['rhog']:.4f} β1={D.b1} εy={D.ey:.6f}")
    for lab, s in (('εt=0 c=32', R['s32']), (f"平衡 c={R['cb']:.2f}", R['sb']), (f"拉控 c={R['ct']:.2f}", R['st']),
                   (f"純彎 c={R['c0']:.2f}", R['s0']), (f"截頂 c={R['c_cap']:.2f}", R['s_cap'])):
        print(f"[{lab}] a={s['a']:.2f} Cc={tf(s['Cc']):.2f}tf P={tf(s['P']):.2f}tf M={tfm(s['M']):.2f}tf·m e={s['e']:.2f} εt={s['et']:.5f} φ={s['phi']:.3f} φP={tf(s['phi']*s['P']):.1f} φM={tfm(s['phi']*s['M']):.2f}")
        for r in s['rows']:
            print(f"    d={r['d']} A={r['A']:.2f} ε={r['eps']:.6f} fs={r['fs']:.0f} 塊內={r['inblock']} fnet={r['fnet']:.0f} F={tf(r['F']):.2f} arm={r['arm']}")
    print(f"P0={tf(R['P0']):.2f} 0.80P0={tf(R['Pmax']):.2f} φPmax={tf(R['phiPmax']):.2f}")
    print(f"Mn 峰值 {tfm(R['Mpk']):.2f} @c={R['c_Mpk']:.2f}；φMn 峰值 {tfm(R['phiMpk']):.2f} @c={R['c_phiMpk']:.2f}")
    print(f"cb by 6120: {6120/(6120+4200)*32:.2f}")
    C, s = rc2021_2(); print(f"== RC-2021-2 P={tf(s['P']):.2f} M={tfm(s['M']):.2f} e={s['e']:.2f}")
    for r in s['rows']:
        print(f"    d={r['d']} ε={r['eps']:.6f} fs={r['fs']:.0f} fnet={r['fnet']:.0f} F={tf(r['F']):.2f}")
    C, s = rc2008_2(); print(f"== RC-2008-2 a={s['a']:.2f} P={tf(s['P']):.2f} M={tfm(s['M']):.2f}")
    C, s, Pn = rc2019_2(); print(f"== RC-2019-2 Pn={tf(Pn):.2f} c={s['c']:.2f} M={tfm(s['M']):.2f} φM={0.65*tfm(s['M']):.2f} εt={s['et']:.5f} cb={C.cb():.2f}")
    C, s, sb = rc2002_2(); print(f"== RC-2002-2 c={s['c']:.2f} P={tf(s['P']):.2f} M={tfm(s['M']):.2f} eb={sb['e']:.2f} cb={C.cb():.2f}")
    C, sb, st, s0, scan = rc2015_1()
    print(f"== RC-2015-1 平衡 P={tf(sb['P']):.2f} M={tfm(sb['M']):.2f} φ={sb['phi']:.3f} φM={tfm(sb['phi']*sb['M']):.2f}; 拉控 c={st['c']:.2f} P={tf(st['P']):.2f} M={tfm(st['M']):.2f} φM={tfm(0.9*st['M']):.2f}; 純彎 M={tfm(s0['M']):.2f}")
    for c, x in scan:
        print(f"    c={c:.2f} εt={x['et']:.5f} φ={x['phi']:.3f} M={tfm(x['M']):.2f} φM={tfm(x['phi']*x['M']):.2f}")
    R3 = rc2011_3()
    print(f"== RC-2011-3 Pb={tf(R3['sb']['P']):.2f} Mb={tfm(R3['sb']['M']):.2f} Pn={tf(R3['Pn']):.2f} c={R3['s']['c']:.2f} εt={R3['s']['et']:.6f} φ={R3['s']['phi']:.4f} Mn={tfm(R3['s']['M']):.2f} φMn={tfm(R3['s']['phi']*R3['s']['M']):.2f}")
    print(f"    N={tf(R3['N']):.2f} Ec={R3['Ec']:.0f} k={R3['k']:.2f} φy={R3['phy']:.4e} εc,y={R3['ec_y']:.5f} c*={R3['cu']:.2f} φu={R3['phu']:.4e} μφ={R3['mu']:.2f}")
    R4 = rc2010_1()
    print("== RC-2010-1", {k: (round(v, 5) if isinstance(v, float) else v) for k, v in R4.items()})
    r=rc2017_1(); print("== RC-2017-1", {k:v for k,v in r.items() if k!="P"})
    print("== RC-2017-2", rc2017_2())
    print("== RC-2006-2", rc2006_2())
    print("== RC-2016-3", rc2016_3())
    print("== RC-2013-2", rc2013_2(), 'so(hx=21)=', so(21.0))
