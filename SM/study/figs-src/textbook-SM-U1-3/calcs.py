# -*- coding: utf-8 -*-
"""SM-U1-3 土壤夯實及壓密｜教科書講義的所有數值（圖與內文共用）。單位：kN、m、kPa（除另註）。

考題數字取自 raw/solutions/SM-YYYY-N/SM-YYYY-N.md（勘誤後版本）：
  2019-3（Dr＋R.C.＋高度）、2017-2（CBR 內插）、2008-1（土方守恆）、
  2021-2（貫穿範例：p0′→Sc→時間）、2024-3（降水＋NC/OC）、2003-2、2011-3（2:1）、
  2018-1（比例法）、2025-1（試體換現場）、2015-1（預壓）
執行 `python3 calcs.py` 印出全部數值，與內文逐一對照。
"""
import math

GW = 9.81   # γw (kN/m³)
lg = math.log10


# ---------- 第 1 章 三相 ----------
def ex2019_3():
    d = dict(emax=0.95, emin=0.55, Dr0=0.50, Gs=2.65, RC=0.95, H0=2.0)
    d['e0'] = d['emax'] - d['Dr0'] * (d['emax'] - d['emin'])
    d['gd0'] = d['Gs'] * GW / (1 + d['e0'])
    d['gdmax'] = d['Gs'] * GW / (1 + d['emin'])
    d['gdf'] = d['RC'] * d['gdmax']
    d['ef'] = d['Gs'] * GW / d['gdf'] - 1
    d['dH'] = d['H0'] * (d['e0'] - d['ef']) / (1 + d['e0'])
    d['dH_wrong'] = d['H0'] * (d['e0'] - d['ef']) / (1 + d['ef'])   # 分母誤用 1+ef
    return d


def ex2008_1():
    d = dict(gd=20.0, wc=0.12, gtA=19.6, wA=0.09, gtB=20.6, wB=0.11)
    d['Ws'] = d['gd'] * 1.0
    d['Ww'] = d['Ws'] * d['wc']
    d['gdA'] = d['gtA'] / (1 + d['wA'])
    d['gdB'] = d['gtB'] / (1 + d['wB'])
    d['VB'] = d['Ws'] / (4 * d['gdA'] + d['gdB'])
    d['VA'] = 4 * d['VB']
    d['WwA'] = d['gdA'] * d['VA'] * d['wA']
    d['WwB'] = d['gdB'] * d['VB'] * d['wB']
    d['dWw'] = d['Ww'] - d['WwA'] - d['WwB']
    return d


# ---------- 第 2 章 夯實 ----------
CMP17 = [(8.0, 17.2), (10.0, 18.2), (12.0, 18.6), (16.0, 18.3), (18.0, 17.3)]   # 2017-2 (w%, γd)
CBR17 = [9.0 - 3.0, 9.0, 12.0, 11.0, 7.0]   # 只用 2、3、4、5 點（第一點示意不用）


def ex2017_2():
    (x1, y1), (x2, y2), (x3, y3) = CMP17[1], CMP17[2], CMP17[3]
    # 過三點的拋物線
    den = (x1 - x2) * (x1 - x3) * (x2 - x3)
    a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / den
    b = (x3 ** 2 * (y1 - y2) + x2 ** 2 * (y3 - y1) + x1 ** 2 * (y2 - y3)) / den
    c = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / den
    wopt = -b / (2 * a)
    gmax = c - b * b / (4 * a)
    gdry = 18.2 + 0.4 * (10 - 9) / (12 - 9)
    gwet = 17.3 + 1.0 * (10 - 7) / (11 - 7)
    req = max(gdry, gwet)
    return dict(a=a, b=b, c=c, wopt=wopt, gmax=gmax, gdry=gdry, gwet=gwet, req=req, RC=req / 18.66 * 100)


def gzav(w, Gs=2.70):
    """零空氣孔隙曲線 γzav（kN/m³），w 為小數"""
    return Gs * GW / (1 + w * Gs)


def gS(w, S, Gs=2.70):
    return Gs * GW / (1 + w * Gs / S)


def energy():
    # 標準夯實：2.5 kg 錘、30.5 cm 落距、25 下、3 層、944 cm³
    std = 2.5 * 9.81 * 0.305 * 25 * 3 / 944e-6 / 1000   # kN·m/m³
    mod = 4.54 * 9.81 * 0.457 * 25 * 5 / 944e-6 / 1000
    return dict(std=std, mod=mod, ratio=mod / std)


# ---------- 第 3 章 有效應力與應力增量 ----------
def ex2021_2():
    """貫穿範例：5 m NC 黏土、上下砂層雙面排水、Δσ=100 kPa、cv=0.001 cm²/s"""
    d = dict(gd_s=16.5, gsat_s=18.5, gsat_c=20.0, H=5.0, Cc=0.5, e0=0.9, dp=100.0, cv=0.001, zw=1.0)
    d['zmid'] = 1 + 1 + d['H'] / 2
    d['sig'] = d['gd_s'] * 1 + d['gsat_s'] * 1 + d['gsat_c'] * 2.5
    d['u'] = GW * (d['zmid'] - d['zw'])
    d['p0'] = d['sig'] - d['u']
    d['p0_wrong'] = d['sig']   # 忘了扣 u
    d['Sc'] = d['Cc'] * d['H'] * 100 / (1 + d['e0']) * lg((d['p0'] + d['dp']) / d['p0'])   # cm
    d['Sc_wrong'] = d['Cc'] * d['H'] * 100 / (1 + d['e0']) * lg((d['p0_wrong'] + d['dp']) / d['p0_wrong'])
    d['Hdr'] = d['H'] * 100 / 2   # cm
    out = []
    for days in (30, 60, 90):
        Tv = d['cv'] * days * 86400 / d['Hdr'] ** 2
        U = math.sqrt(4 * Tv / math.pi)
        out.append((days, Tv, U, U * d['Sc']))
    d['steps'] = out
    U50 = 50 / d['Sc']
    Tv = 1.781 - 0.933 * lg(100 - U50 * 100)
    d['U50cm'] = U50
    d['Tv50cm'] = Tv
    d['t50cm'] = Tv * d['Hdr'] ** 2 / d['cv'] / 86400
    d['t50cm_wrongHdr'] = Tv * (d['H'] * 100) ** 2 / d['cv'] / 86400
    return d


def ex2024_3():
    d = dict(g_cov_d=16.00, g_cov_sat=19.68, g_sand_sat=18.29, w_sand=0.18, g_clay=21.78,
             H=10.0, e0=0.9, Cc=0.15, Cs=0.02, pc=300.0)
    d['g_sand_d'] = d['g_sand_sat'] / (1 + d['w_sand'])
    s0 = d['g_cov_d'] * 2 + d['g_cov_sat'] * 6 + d['g_sand_sat'] * 12
    u0 = (20 - 2) * GW
    d['sC0'], d['uC0'] = s0, u0
    d['pC0'] = s0 - u0
    s1 = d['g_cov_d'] * 8 + d['g_sand_d'] * 10 + d['g_sand_sat'] * 2
    u1 = (20 - 18) * GW
    d['sC1'], d['uC1'] = s1, u1
    d['pC1'] = s1 - u1
    d['dp'] = d['pC1'] - d['pC0']
    # 錯法：水位以上仍用 γsat
    s1w = d['g_cov_d'] * 2 + d['g_cov_sat'] * 6 + d['g_sand_sat'] * 12   # 總應力沒變
    d['dp_wrong'] = (s1w - u1) - d['pC0']
    d['p0'] = d['pC0'] + (d['g_clay'] - GW) * 5
    d['pf'] = d['p0'] + d['dp']
    k = d['H'] * 100 / (1 + d['e0'])
    d['S_NC'] = d['Cc'] * k * lg(d['pf'] / d['p0'])
    d['S_OC1'] = d['Cs'] * k * lg(d['pc'] / d['p0'])
    d['S_OC2'] = d['Cc'] * k * lg(d['pf'] / d['pc'])
    d['S_OC'] = d['S_OC1'] + d['S_OC2']
    d['S_allCs'] = d['Cs'] * k * lg(d['pf'] / d['p0'])
    d['OCR'] = d['pc'] / d['p0']
    return d


def ex2003_2():
    d = dict(Q=1200.0, B=2.0, zp=6.5, p0=82.735, pc=90.0)
    d['dp'] = d['Q'] / (d['B'] + d['zp']) ** 2
    d['dp_wrong'] = d['Q'] / (d['B'] + 8.0) ** 2   # z 由地表量
    d['Sc'] = 4.31
    return d


def ex2011_3():
    d = dict(Q=1000.0, B=1.5, zt=1.5, zb=4.5, H=3.0, p0=53.20, pc=100.0, Cs=0.06, Cc=0.25, e0=0.68)
    f = lambda z: d['Q'] / (d['B'] + z) ** 2
    d['dt'], d['dm'], d['db'] = f(d['zt']), f((d['zt'] + d['zb']) / 2), f(d['zb'])
    d['davg'] = d['Q'] / d['H'] * (1 / (d['B'] + d['zt']) - 1 / (d['B'] + d['zb']))
    d['simp'] = (d['dt'] + 4 * d['dm'] + d['db']) / 6
    d['pf'] = d['p0'] + d['davg']
    k = d['H'] * 1000 / (1 + d['e0'])   # mm
    d['S1'] = d['Cs'] * k * lg(d['pc'] / d['p0'])
    d['S2'] = d['Cc'] * k * lg(d['pf'] / d['pc'])
    d['S'] = d['S1'] + d['S2']
    d['S_mid'] = d['Cs'] * k * lg(d['pc'] / d['p0']) + d['Cc'] * k * lg((d['p0'] + d['dm']) / d['pc'])
    return d


# ---------- 第 4 章 e–log σ′ ----------
ELOG = dict(e0=0.90, pc=100.0, Cc=0.30, Cs=0.05, p_start=20.0)


def elog_curve(p, d=ELOG):
    """理想化現地曲線：pc 以前走 Cs，之後走 Cc（起點 p_start 時 e=e0）"""
    epc = d['e0'] - d['Cs'] * lg(d['pc'] / d['p_start'])
    if p <= d['pc']:
        return d['e0'] - d['Cs'] * lg(p / d['p_start'])
    return epc - d['Cc'] * lg(p / d['pc'])


def cc_skempton(LL):
    return 0.009 * (LL - 10)


def mv_from_cc(Cc, e0, p1, p2):
    de = Cc * lg(p2 / p1)
    return de / ((1 + e0) * (p2 - p1))


# ---------- 第 6 章 壓密時間 ----------
def U_exact(Tv, n=200):
    if Tv <= 0:
        return 0.0
    s = 0.0
    for m in range(n):
        M = math.pi * (2 * m + 1) / 2
        s += 2 / M ** 2 * math.exp(-M * M * Tv)
    return 1 - s


def Tv_from_U(U):
    """百分比版兩段式（U 為小數）"""
    if U <= 0.6:
        return math.pi / 4 * U * U
    return 1.781 - 0.933 * lg(100 - U * 100)


def U_from_Tv(Tv):
    U = math.sqrt(4 * Tv / math.pi)
    if U <= 0.6:
        return U
    return (100 - 10 ** ((1.781 - Tv) / 0.933)) / 100


def u_iso(z_over_H, Tv, n=200):
    """等時線：u/u0，z 由排水面量、H=Hdr"""
    s = 0.0
    for m in range(n):
        M = math.pi * (2 * m + 1) / 2
        s += 2 / M * math.sin(M * z_over_H) * math.exp(-M * M * Tv)
    return s


def tv_consts():
    return dict(k1=4 * math.log(10) / math.pi ** 2, c1=-4 / math.pi ** 2 * math.log(8 / math.pi ** 2) * 1 / math.log(10) * math.log(10),
                c_log=(4 / math.pi ** 2) * math.log(math.pi ** 2 / 8),
                T50=Tv_from_U(0.5), T90=Tv_from_U(0.9), T60=Tv_from_U(0.6),
                T60b=1.781 - 0.933 * lg(40), Uex50=U_exact(Tv_from_U(0.5)), Uex90=U_exact(Tv_from_U(0.9)),
                const100=1.781 - 0.933 * 2)


def ex2018_1():
    d = dict(S200=234.0, U200=0.30)
    d['Smax'] = d['S200'] / d['U200']
    d['T200'] = math.pi / 4 * d['U200'] ** 2
    d['k'] = d['T200'] / 200
    out = []
    for yr in (1, 2, 3, 4):
        t = 365 * yr
        Tv = d['k'] * t
        U = U_from_Tv(Tv)
        out.append((yr, t, Tv, U, U * d['Smax']))
    d['rows'] = out
    # 錯法：一路用 √t 外推
    d['wrong'] = [(yr, d['S200'] * math.sqrt(365 * yr / 200)) for yr in (1, 2, 3, 4)]
    return d


def ex2025_1():
    d = dict(Hlab=2.54, tlab=3.0, Hf=1000.0)   # cm、min
    d['Hdr_lab'] = d['Hlab'] / 2
    d['T50'] = Tv_from_U(0.5)
    d['cv'] = d['T50'] * d['Hdr_lab'] ** 2 / d['tlab']
    d['T90'] = Tv_from_U(0.9)
    d['t90'] = d['T90'] * d['Hf'] ** 2 / d['cv']
    d['t90_yr'] = d['t90'] / 60 / 24 / 365
    d['t90_days'] = d['t90'] / 60 / 24
    d['U45'] = 9 / 20
    d['T45'] = Tv_from_U(d['U45'])
    d['t45'] = d['T45'] * d['Hf'] ** 2 / d['cv']
    d['t45_yr'] = d['t45'] / 60 / 24 / 365
    d['t90_wrong_yr'] = d['T90'] * (d['Hf'] / 2) ** 2 / d['cv'] / 60 / 24 / 365
    d['ratio'] = (d['Hf'] / d['Hdr_lab']) ** 2
    return d


def ex2015_1():
    d = dict(p0=48.38, dp=84.0, H=8.0, Cc=None, Sc=52.46, T80=0.567, cv=0.003, Hdr=400.0)
    d['S80'] = 0.8 * d['Sc']
    d['t80'] = d['T80'] * d['Hdr'] ** 2 / d['cv'] / 86400
    return d


if __name__ == '__main__':
    def show(name, d):
        print('==', name)
        for k, v in d.items():
            if isinstance(v, float):
                print(f'  {k} = {v:.4f}')
            elif isinstance(v, list):
                for r in v:
                    print('   ', tuple(round(x, 4) if isinstance(x, float) else x for x in r))
            else:
                print(f'  {k} = {v}')
    show('2019-3', ex2019_3())
    show('2008-1', ex2008_1())
    show('2017-2', ex2017_2())
    show('energy', energy())
    print('γzav(w=0.15, Gs=2.70)=', round(gzav(0.15), 3))
    show('2021-2', ex2021_2())
    show('2024-3', ex2024_3())
    show('2003-2', ex2003_2())
    show('2011-3', ex2011_3())
    print('Cc(LL=45)=', cc_skempton(45), ' Cc(LL=50)=', cc_skempton(50))
    print('mv(Cc=0.3,e0=0.9,100→200)=', mv_from_cc(0.3, 0.9, 100, 200))
    show('Tv consts', tv_consts())
    show('2018-1', ex2018_1())
    show('2025-1', ex2025_1())
    show('2015-1', ex2015_1())
    for U in (0.2, 0.5, 0.6, 0.7, 0.9):
        print(f'U={U}: Tv(公式)={Tv_from_U(U):.4f}  U_exact(Tv)={U_exact(Tv_from_U(U)):.4f}')


# ---------- Casagrande（在固定比例的圖上作圖） ----------
CAS = dict(pc=100.0, epc=0.80, Cs=0.06, Cc=0.32, w=0.12,
           px=dict(x0=100, w=520, lmin=1.0, lmax=3.0, y0=50, h=320, emin=0.40, emax=0.95))


def e_lab(p, d=CAS):
    """平滑試驗曲線：兩條直線以 softplus 銜接（x=log10(p/pc)）"""
    x = math.log10(p / d['pc'])
    sw = d['w'] * math.log(1 + math.exp(x / d['w']))
    return d['epc'] - d['Cs'] * x - (d['Cc'] - d['Cs']) * sw


def _to_px(p, e, d=CAS):
    q = d['px']
    X = q['x0'] + (math.log10(p) - q['lmin']) / (q['lmax'] - q['lmin']) * q['w']
    Y = q['y0'] + (q['emax'] - e) / (q['emax'] - q['emin']) * q['h']
    return X, Y


def casagrande(d=CAS):
    # 曲率最大點（在像素座標）
    best = None
    ps = [10 ** (1.4 + i * 0.001) for i in range(1200)]
    for i in range(1, len(ps) - 1):
        (x0, y0), (x1, y1), (x2, y2) = _to_px(ps[i - 1], e_lab(ps[i - 1])), _to_px(ps[i], e_lab(ps[i])), _to_px(ps[i + 1], e_lab(ps[i + 1]))
        dx, dy = (x2 - x0) / 2, (y2 - y0) / 2
        ddx, ddy = x2 - 2 * x1 + x0, y2 - 2 * y1 + y0
        k = abs(dx * ddy - dy * ddx) / (dx * dx + dy * dy) ** 1.5
        if best is None or k > best[0]:
            best = (k, ps[i], (x1, y1), (dx, dy))
    _, pA, (xA, yA), (dx, dy) = best
    ang_t = math.atan2(dy, dx)            # 切線方向（往右下，像素座標 y 向下）
    ang_b = ang_t / 2                     # 水平(0) 與切線夾角的平分線
    # 原始壓縮線（漸近線）e = epc - Cc x  → 兩個像素點
    P1 = _to_px(d['pc'] * 10, d['epc'] - d['Cc'])
    P2 = _to_px(d['pc'] / 10, d['epc'] + d['Cc'])
    # 交點：A + t(cos b, sin b) 與 P1→P2 直線
    ux, uy = math.cos(ang_b), math.sin(ang_b)
    vx, vy = P2[0] - P1[0], P2[1] - P1[1]
    den = ux * (-vy) - uy * (-vx)
    t = ((P1[0] - xA) * (-vy) - (P1[1] - yA) * (-vx)) / den
    xi, yi = xA + t * ux, yA + t * uy
    q = d['px']
    p_est = 10 ** (q['lmin'] + (xi - q['x0']) / q['w'] * (q['lmax'] - q['lmin']))
    return dict(pA=pA, A=(xA, yA), ang_t=ang_t, ang_b=ang_b, I=(xi, yi), pc_est=p_est, P1=P1, P2=P2)


def schmertmann():
    e0 = 0.95
    p0 = 80.0
    Cc_field = 0.42
    e_end = 0.42 * e0
    # 現地線：(p0, e0) → e_end；擾動試驗曲線：較平、較圓（softplus），端點同在 e_end
    p_end = p0 * 10 ** ((e0 - e_end) / Cc_field)
    return dict(e0=e0, p0=p0, Cc_field=Cc_field, e_end=e_end, p_end=p_end)


def practice():
    """第 7 章綜合重建練習（自編數字）"""
    d = dict(gd=17.0, gs=19.0, gc=18.5, Hc=6.0, Cc=0.40, e0=1.10, cv=0.002, dp=60.0, Cs=0.06, pc=110.0)
    zmid = 4 + d['Hc'] / 2
    d['zmid'] = zmid
    d['sig'] = d['gd'] * 2 + d['gs'] * 2 + d['gc'] * 3
    d['u'] = GW * (zmid - 2)
    d['p0'] = d['sig'] - d['u']
    k = d['Hc'] * 100 / (1 + d['e0'])
    d['Sc_NC'] = d['Cc'] * k * lg((d['p0'] + d['dp']) / d['p0'])
    d['Sc_OC'] = d['Cs'] * k * lg(d['pc'] / d['p0']) + d['Cc'] * k * lg((d['p0'] + d['dp']) / d['pc'])
    d['Hdr'] = d['Hc'] * 100   # 單面
    d['t50'] = Tv_from_U(0.5) * d['Hdr'] ** 2 / d['cv'] / 86400
    d['t90'] = Tv_from_U(0.9) * d['Hdr'] ** 2 / d['cv'] / 86400
    Tv1 = d['cv'] * 365 * 86400 / d['Hdr'] ** 2
    d['Tv1yr'] = Tv1
    d['U1yr'] = U_from_Tv(Tv1)
    d['S1yr'] = d['U1yr'] * d['Sc_NC']
    return d
