"""Numbers for lecture-SM-U3-2. Every value printed in the lecture comes from here; asserts tie to 題解正本."""
import math
d = math.radians
def close(a, b, tol): assert abs(a - b) <= tol, (a, b)

def ka_rankine(phi): return math.tan(d(45 - phi / 2)) ** 2
def ka_incl(a, phi):
    ca, cp = math.cos(d(a)), math.cos(d(phi)); r = math.sqrt(ca*ca - cp*cp)
    return ca * (ca - r) / (ca + r)
def ka_coulomb(beta, phi, delta, alpha):
    s = math.sin; B, P, D, A = d(beta), d(phi), d(delta), d(alpha)
    return s(B+P)**2 / (s(B)**2 * s(B-D) * (1 + math.sqrt(s(P+D)*s(P-A)/(s(B-D)*s(A+B))))**2)
def kae_mo(beta, phi, delta, alpha, th):
    s = math.sin; B, P, D, A, T = d(beta), d(phi), d(delta), d(alpha), d(th)
    return s(P+B-T)**2 / (math.cos(T)*s(B)**2*s(B-D-T)*(1+math.sqrt(s(P+D)*s(P-A-T)/(s(B-D-T)*s(A+B))))**2)

N = {}
# ---------- SM-2009-4 gravity wall, inclined backfill, solve B
def w09(B):
    Ka = ka_incl(20, 30); Pa = 0.5*Ka*18*36; Pah, Pav = Pa*math.cos(d(20)), Pa*math.sin(d(20))
    W1 = 0.6*6*24; W2 = 0.5*(B-0.6)*6*24
    V = W1 + W2 + Pav
    MR = W1*(B-0.3) + W2*(2/3)*(B-0.6) + Pav*B
    MO = Pah*2
    return dict(Ka=Ka, Pa=Pa, Pah=Pah, Pav=Pav, W1=W1, W2=W2, V=V, MR=MR, MO=MO,
                xbar=(MR-MO)/V, FSOT=MR/MO, FSSL=V*math.tan(d(33))/Pah)
lo, hi = 1.0, 5.0
for _ in range(80):
    m = (lo+hi)/2
    r = w09(m)
    if r['xbar'] - m/3 > 0: hi = m
    else: lo = m
B09 = (lo+hi)/2; r09 = w09(B09)
close(r09['Ka'], 0.4142, 2e-4); close(r09['Pa'], 134.20, 0.05); close(B09, 2.49, 0.005)
r09b = w09(2.49)   # 題解以 B=2.49 代入
close(r09b['FSOT'], 1.88, 0.006); close(r09b['FSSL'], 1.38, 0.006)
N['09'] = dict(B=B09, **{k: r09b[k] for k in r09b})
N['09']['qtoe'] = 2*r09b['V']/2.49
# B needed for FSOT=2, FSSL=1.5
def solve(f, target, lo, hi):
    for _ in range(80):
        m = (lo+hi)/2
        if f(m) < target: lo = m
        else: hi = m
    return (lo+hi)/2
N['09']['B_OT2'] = solve(lambda b: w09(b)['FSOT'], 2.0, 1, 6)
N['09']['B_SL15'] = solve(lambda b: w09(b)['FSSL'], 1.5, 1, 6)

# ---------- SM-2025-3 phi=0 base
PA25 = 0.5*(1/3)*17*49; R25 = 30*6; W25 = 27*23.5
close(PA25, 138.83, 0.01); close(R25/PA25, 1.2965, 1e-4); close(W25, 634.5, 1e-6)
N['25'] = dict(PA=PA25, R=R25, FS=R25/PA25, W=W25, FS_sand=W25*math.tan(d(20))/PA25,
               W_needed_sand=1.5*PA25/math.tan(d(20)))
close(N['25']['FS_sand'], 1.66, 0.006)

# ---------- SM-2018-4 cantilever, virtual back
Hp = 7.5 + 0.96 + 3.5*math.tan(d(12)); Ka18 = ka_incl(12, 32); Pa18 = 0.5*17.8*Hp**2*Ka18
close(Hp, 9.204, 1e-3); close(Ka18, 0.3275, 2e-4); close(Pa18, 246.92, 0.1)
Pax, Pay = Pa18*math.cos(d(12)), Pa18*math.sin(d(12))
Ws = [0.4*7.5*23.55, 0.5*0.2*7.5*23.55, 5.6*0.96*23.55, 3.5*7.5*17.8, 0.5*3.5*(3.5*math.tan(d(12)))*17.8, 1.5*0.79*17.8]
xs = [1.9, 1.5+0.2*2/3, 2.8, 3.85, 2.1+3.5*2/3, 0.75]
V18 = sum(Ws) + Pay; MR18 = sum(w*x for w, x in zip(Ws, xs)) + Pay*5.6; MO18 = Pax*Hp/3
FSOT18 = MR18/MO18; FSSL18 = (20*5.6 + V18*math.tan(d(2/3*28)))/Pax
close(FSOT18, 3.67, 0.006); close(FSSL18, 1.55, 0.006)
N['18'] = dict(Hp=Hp, Ka=Ka18, Pa=Pa18, Pax=Pax, Pay=Pay, V=V18, MR=MR18, MO=MO18, FSOT=FSOT18, FSSL=FSSL18,
               Wsoil=Ws[3]+Ws[4], Pa_realback=0.5*17.8*7.5**2*Ka18)

# ---------- SM-2016-4 Coulomb + bearing + M-O
beta = math.degrees(math.atan(8/2)); Ka16 = ka_coulomb(beta, 30, 15, 0); Pa16 = 0.5*18*64*Ka16
close(Ka16, 0.4148, 3e-4); close(Pa16, 238.92, 0.2)
ang = 90 - beta + 15
Pah16, Pav16 = Pa16*math.cos(d(ang)), Pa16*math.sin(d(ang))
xpa = 5 - (8/3/8)*2
V16 = 564 + 188 + Pav16; MR16 = 564*1.5 + 188*(3+2/3) + Pav16*xpa; MO16 = Pah16*8/3
FSOT16 = MR16/MO16; FSSL16 = (15*5 + V16*math.tan(d(18)))/Pah16
close(FSOT16, 3.66, 0.006); close(FSSL16, 1.71, 0.006)
xb16 = (MR16-MO16)/V16; e16 = 2.5 - xb16; qmax16 = V16/5*(1+6*e16/5); qmin16 = V16/5*(1-6*e16/5)
close(e16, 0.794, 0.002); close(qmax16, 339.0, 0.5)
Bp16 = 5 - 2*e16; th16 = math.degrees(math.atan(Pah16/V16))
Fci16, Fgi16 = (1-th16/90)**2, (1-th16/30)**2
qu16 = 20*30.14*Fci16 + 0.5*18*Bp16*22.4*Fgi16
close(qu16, 642.2, 1.0); close(qu16/qmax16, 1.89, 0.01)
qu16_noincl = 20*30.14 + 0.5*18*Bp16*22.4
th_ = math.degrees(math.atan(0.15/0.95)); Kae = kae_mo(beta, 30, 15, 0, th_)
Pae = 0.5*18*64*0.95*Kae; dP = Pae - Pa16; zbar = (Pa16*8/3 + dP*0.6*8)/Pae
close(Kae, 0.5414, 3e-4); close(Pae, 296.26, 0.3); close(zbar, 3.08, 0.01)
N['16_4'] = dict(beta=beta, Ka=Ka16, Pa=Pa16, ang=ang, Pah=Pah16, Pav=Pav16, V=V16, MR=MR16, MO=MO16,
                 FSOT=FSOT16, FSSL=FSSL16, xbar=xb16, e=e16, qmax=qmax16, qmin=qmin16, Bp=Bp16, th=th16,
                 Fci=Fci16, Fgi=Fgi16, qu=qu16, FS_qmax=qu16/qmax16, qeff=V16/Bp16, FS_eff=qu16/(V16/Bp16),
                 qu_noincl=qu16_noincl, thp=th_, Kae=Kae, Pae=Pae, dP=dP, zbar=zbar)

# ---------- SM-2016-3 MSE wall
Ka3 = ka_rankine(32); Pa1 = 0.5*Ka3*18*36; Pa2 = Ka3*60*6; Ph3 = Pa1 + Pa2; V3 = 20*6*4.5 + 60*4.5
MO3 = Pa1*2 + Pa2*3; MR3 = V3*2.25
xb3 = (MR3-MO3)/V3; e3 = 2.25 - xb3; Lp = 4.5 - 2*e3; th3 = math.degrees(math.atan(Ph3/V3))
ic, ig = (1-th3/90)**2, (1-th3/32)**2
qu3 = 20*35.49*ic + 0.5*18*Lp*30.22*ig
FSSL3 = (12*4.5 + V3*math.tan(d(15)))/Ph3
close(MR3/MO3, 3.43, 0.006); close(FSSL3, 1.29, 0.006); close(qu3/(V3/Lp), 2.98, 0.006); close(th3, 14.55, 0.01)
qu3_noincl = 20*35.49 + 0.5*18*Lp*30.22
close(qu3_noincl/(V3/Lp), 6.21, 0.01)
N['16_3'] = dict(Ka=Ka3, Pa1=Pa1, Pa2=Pa2, Ph=Ph3, V=V3, FSOT=MR3/MO3, FSSL=FSSL3, e=e3, Lp=Lp, th=th3,
                 ic=ic, ig=ig, qu=qu3, qeff=V3/Lp, FSBC=qu3/(V3/Lp), FSBC_noincl=qu3_noincl/(V3/Lp),
                 plane=45+32/2)

# ---------- SM-2004-3 water level
Ka4 = ka_rankine(35)
def Ph4(x): return 0.5*Ka4*19.2*36 - 0.5*Ka4*9.81*x*x + 0.5*9.81*x*x
x4 = math.sqrt((146 - 0.5*Ka4*19.2*36)/(0.5*9.81*(1-Ka4)))
close(x4, 3.826, 0.002)
N['04'] = dict(Ka=Ka4, x=x4, Ph0=Ph4(0), Ph6=Ph4(6), ratio=1/Ka4)

# ---------- SM-2015-2 (只引用題解數值)
N['15'] = dict(zc=2*20/(17.5*math.sqrt(ka_rankine(20))), Ptot=197.30, FS=0.68, W=391.0, U=73.58)
close(N['15']['zc'], 3.264, 0.002)

if __name__ == '__main__':
    import json
    print(json.dumps(N, indent=1, ensure_ascii=False, default=lambda v: round(v, 4)))
