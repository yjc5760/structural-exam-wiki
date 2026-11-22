"""Numbers for lecture-SM-U3-3; asserts tie to 題解正本."""
import math
d = math.radians; t = lambda a: math.tan(d(a))
def close(a, b, tol): assert abs(a - b) <= tol, (a, b)
N = {}
GW = 9.81
# ---- SM-2024-2
N['24'] = dict(FS=t(35)/t(42), i=math.sin(d(30)), i_tan=t(30))
close(N['24']['FS'], 0.7777, 1e-3)

# ---- SM-2014-1 infinite slope c'-phi' with parallel seepage
e = 0.35*2.64; gt = 2.64*1.24/(1+e)*GW; gs = 2.64*1.35/(1+e)*GW
def fs14(dw, H=6.0, beta=15, c=15, phi=20):
    H1 = min(dw, H); H2 = H - H1
    sv = gt*H1 + gs*H2; u = GW*H2*math.cos(d(beta))**2
    sn = sv*math.cos(d(beta))**2 - u; tau = sv*math.sin(d(beta))*math.cos(d(beta))
    return (c + sn*t(phi))/tau, sv, u, sn, tau
FS14, sv, u, sn, tau = fs14(1.5)
close(e, 0.924, 1e-3); close(gt, 16.69, 0.01); close(gs, 18.17, 0.01)
close(u, 41.19, 0.02); close(sn, 58.45, 0.05); close(FS14, 1.36, 0.005)
N['14'] = dict(e=e, gt=gt, gs=gs, sv=sv, u=u, sn=sn, tau=tau, FS=FS14, FS_dry=fs14(6.0)[0], FS_full=fs14(0.0)[0],
               u_wrong=GW*4.5, FS_uwrong=(15 + (sv*math.cos(d(15))**2 - GW*4.5)*t(20))/tau)

# ---- SM-2023-2 planar wedge
L = 8/math.sin(d(45)); b = 8/t(45) - 8/t(60); W = 0.5*b*8*20
Td = W*math.sin(d(45)); Nn = W*math.cos(d(45))
fs23 = lambda c: (c*L + Nn*t(36))/Td
close(W, 270.50, 0.02); close(fs23(50), 3.684, 0.002); close(fs23(5), 1.022, 0.002)
N['23'] = dict(L=L, W=W, Td=Td, N=Nn, cL50=50*L, Ntan=Nn*t(36), FS1=fs23(50), FS2=fs23(5), FS0=fs23(0),
               c_for_1=(Td - Nn*t(36))/L)

# ---- SM-2008-4 wedge + seismic + anchor
LAB = 7.5/math.sin(d(70)); LAC = LAB*math.sin(d(115))/math.sin(d(35)); A = 0.5*LAB*LAC*math.sin(d(30)); W8 = 20*A
def fs08(kh, P=0.0):
    Td = W8*math.sin(d(40)) + kh*W8*math.cos(d(40)); Nn = W8*math.cos(d(40)) - kh*W8*math.sin(d(40))
    return (10*LAC + (Nn + P)*t(28))/Td, Td, Nn
FS8, Td8, N8 = fs08(0.2)
close(W8, 503.24, 0.05); close(FS8, 0.7406, 1e-3)
P = (1.2*Td8 - 10*LAC - N8*t(28))/t(28)
close(P, 346.09, 0.2); close(2*P, 692.18, 0.4)
N['08'] = dict(LAC=LAC, W=W8, Td=Td8, N=N8, FS=FS8, FS_static=fs08(0)[0], P=P, T=2*P)
# anchor inclined: optimal angle reduces driving too (for comparison only)
# anchor inclined at angle psi from normal toward up-slope: N += P cos psi, Td -= P sin psi
def P_needed(psi):
    lo, hi = 0, 2000
    for _ in range(80):
        m = (lo+hi)/2
        fs = (10*LAC + (N8 + m*math.cos(d(psi)))*t(28))/(Td8 - m*math.sin(d(psi)))
        if fs < 1.2: lo = m
        else: hi = m
    return (lo+hi)/2
N['08']['P_opt'] = min((P_needed(p), p) for p in range(0, 61))

# ---- SM-2006-3 three-block
KA, KP = 1/3, 3.0
def blk(g, water):
    a = KA*g; zc = 2*10*math.sqrt(KA)/a; sa = a*12 - 2*10*math.sqrt(KA); PA = 0.5*sa*(12 - zc)
    PP = 0.5*((2*10*math.sqrt(KP)) + (KP*g*2 + 2*10*math.sqrt(KP)))*2
    PwA = 0.5*GW*144 if water else 0; PwP = 0.5*GW*4 if water else 0
    T = 12*20
    return dict(zc=zc, PA=PA, PP=PP, PwA=PwA, PwP=PwP, T=T, FS=(T + PP + PwP)/(PA + PwA))
n6, r6 = blk(20, False), blk(20 - GW, True)
close(n6['FS'], 1.22, 0.005); close(r6['FS'], 0.47, 0.005); close(r6['PA'], 125.63, 0.1)
N['06'] = dict(n=n6, r=r6)

# ---- SM-2021-4 slices (題解 Step 2-4 表；量測值)
S = [  # W, alpha, b, u
    (555.9, 60, 5.45, 0.0), (846.4, 42, 5.01, 17.5), (765.6, 30, 4.96, 40.7), (578.6, 13, 5.13, 50.8), (227.7, 0, 5.25, 21.8)]
tp = t(36); rows = []
for W, a, b, u in S:
    dL = b/math.cos(d(a)); Np = W*math.cos(d(a)) - u*dL
    rows.append(dict(W=W, a=a, dL=dL, res=10*dL + Np*tp, drv=W*math.sin(d(a)), Np=Np))
FSf = sum(r['res'] for r in rows)/sum(r['drv'] for r in rows)
close(FSf, 0.975, 0.002)
# Bishop simplified using same W, u, b, alpha (lecture-only comparison)
fs = FSf
for _ in range(100):
    num = sum((10*b + (W - u*b)*tp)/(math.cos(d(a)) + math.sin(d(a))*tp/fs) for W, a, b, u in S)
    fs = num/sum(W*math.sin(d(a)) for W, a, b, u in S)
N['21'] = dict(rows=rows, FS=FSf, FS_bishop=fs, sum_drv=sum(r['drv'] for r in rows),
               sum_res=sum(r['res'] for r in rows))

if __name__ == '__main__':
    import json
    print(json.dumps(N, indent=1, ensure_ascii=False, default=float))
