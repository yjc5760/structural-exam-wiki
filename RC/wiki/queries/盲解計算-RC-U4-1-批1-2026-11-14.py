# RC-U4-1 批1 盲解計算  單位 kgf, cm（tension +）
from math import sqrt
from scipy.optimize import brentq
R={}
def b1(fc): return max(0.65,min(0.85,0.85-0.05*(fc-280)/70))
print("===== RC-2003-1")
fc=350;b=35;h=70;Ab=1.387;Aps=4*Ab;As=2*Ab;dp=63;d=58;Ep=2e6
fse=14000-2000;Pe=fse*Aps;Ec=15000*sqrt(fc)
A=b*h;I=b*h**3/12;e=dp-h/2;r2=I/A
e1=fse/Ep;e2=Pe/(A*Ec)*(1+e*e/r2)
def fp(eps):
    return Ep*eps if eps<= 16400/(2e6-65000) else min(65000*eps+16400,19000)
B=b1(fc)
def res(c):
    eps_p=e1+e2+0.003*(dp-c)/c; eps_s=0.003*(d-c)/c
    return 0.85*fc*b*B*c-(Aps*fp(eps_p)+As*fp(eps_s))
c=brentq(res,1,60);a=B*c
eps_p=e1+e2+0.003*(dp-c)/c;eps_s=0.003*(d-c)/c
Tp=Aps*fp(eps_p);Ts=As*fp(eps_s)
Mn=Tp*(dp-a/2)+Ts*(d-a/2)
print(f"e1={e1:.5f} e2={e2:.6f} c={c:.3f} a={a:.3f} eps_p={eps_p:.5f} fps={fp(eps_p):.0f} eps_s={eps_s:.5f} fs={fp(eps_s):.0f} Mn={Mn/1e5:.2f} tf-m")
# 若忽略 e2
def res2(c):
    return 0.85*fc*b*B*c-(Aps*fp(e1+0.003*(dp-c)/c)+As*fp(0.003*(d-c)/c))
c2=brentq(res2,1,60);a2=B*c2;print(f" 不計e2: Mn={(Aps*fp(e1+0.003*(dp-c2)/c2)*(dp-a2/2)+As*fp(0.003*(d-c2)/c2)*(d-a2/2))/1e5:.2f}")

print("===== RC-2004-5")
fc=350;b=40;h=90;dp=80;Aps=6.16;fpu=16500;B=b1(fc);gp=0.4
rho=Aps/(b*dp);fps=fpu*(1-gp/B*rho*fpu/fc);a=Aps*fps/(0.85*fc*b);c=a/B
et=0.003*(dp-c)/c;Mn=Aps*fps*(dp-a/2)
fr=2.0*sqrt(fc);Pe=0.6*fpu*Aps;A=b*h;S=b*h*h/6;e=dp-h/2
Mcr=(fr+Pe/A+Pe*e/S)*S
print(f"rho={rho:.6f} fps={fps:.0f} a={a:.3f} c={c:.3f} et={et:.4f} Mn={Mn/1e5:.2f} phiMn={0.9*Mn/1e5:.2f}; fr={fr:.2f} Pe={Pe:.0f} Mcr={Mcr/1e5:.2f}; 1.2Mcr={1.2*Mcr/1e5:.2f} omega={Aps*fps/(b*dp*fc):.4f}")

def comp(parts):
    # parts: list of (A, ybar from bottom, Iself)
    At=sum(p[0] for p in parts);yb=sum(p[0]*p[1] for p in parts)/At
    It=sum(p[2]+p[0]*(p[1]-yb)**2 for p in parts);return At,yb,It

print("===== RC-2006-4")
fc=350;fcs=280;n=sqrt(fcs/fc);gam=2.4e-3 # kgf/cm3
b=30;h=80;A=b*h;I=b*h**3/12;yb=40;e=yb-15;P=210000;L=2000
wg=A*gam;Mg=wg*L**2/8
ws=100*15*gam;Ms=ws*L**2/8
wl=1.0e3/1e4*100; ML=wl*L**2/8
beff=min(30+2*8*15,100,L/4)  # 跨度/4 也檢
At,ybc,Ic=comp([(A,40,I),(beff*n*15,87.5,beff*n*15**3/12)])
ftop_c=80-ybc
sb=-P/A-P*e*I**-1*yb+(Mg+Ms)/I*yb+ML/Ic*ybc
st=-P/A+P*e/I*40-(Mg+Ms)/I*40-ML/Ic*(80-ybc)
print(f"n={n:.4f} beff={beff} Mg={Mg/1e5:.2f} Ms={Ms/1e5:.2f} ML={ML/1e5:.2f}; comp A={At:.1f} yb={ybc:.2f} I={Ic:.0f}")
print(f"  梁頂={st:.2f}  梁底={sb:.2f} kgf/cm2 (+拉)")
slabtop=-ML/Ic*(95-ybc)*n
print(f"  (版頂 {slabtop:.2f})")
# 若梁距誤為200
At2,yb2,I2=comp([(A,40,I),(200*n*15,87.5,200*n*15**3/12)]);
ws2=200*15*gam;Ms2=ws2*L**2/8;ML2=2*ML
print(f"  [對照 梁距200] 梁頂={-P/A+P*e/I*40-(Mg+Ms2)/I*40-ML2/I2*(80-yb2):.2f} 梁底={-P/A-P*e/I*40+(Mg+Ms2)/I*40+ML2/I2*yb2:.2f}")
# 若翼寬不換算 n=1
At3,yb3,I3=comp([(A,40,I),(100*15,87.5,100*15**3/12)])
print(f"  [對照 n=1] 梁頂={-P/A+P*e/I*40-(Mg+Ms)/I*40-ML/I3*(80-yb3):.2f} 梁底={-P/A-P*e/I*40+(Mg+Ms)/I*40+ML/I3*yb3:.2f}")

print("===== RC-2007-4")
fc=350;fcs=280;n=sqrt(fcs/fc)
A=3613;I=5.2e6;ct=62.8;cb=51.5;St=83082;Sb=101370;e=cb-20
Pi=13200*21.7;Pe=0.8*Pi;L=2000
wg=A*gam;ws=220*20*gam;wsd=7.5
Mg=wg*L**2/8;Ms=ws*L**2/8;Msd=wsd*L**2/8
beff=min(220,17.5+16*20,L/4)
htot=ct+cb
At,ybc,Ic=comp([(A,cb,I),(beff*n*20,htot+10,beff*n*20**3/12)])
print(f"Pi={Pi:.0f} Pe={Pe:.0f} wg={wg:.1f} Mg={Mg/1e5:.3f} Ms={Ms/1e5:.3f} Msd={Msd/1e5:.3f} beff={beff}; comp A={At:.1f} yb={ybc:.2f} I={Ic:.4g}")
Sbc=Ic/ybc;Stc=Ic/(htot-ybc);Sslab=Ic/(htot+20-ybc)/n
fb0=-Pe/A-Pe*e/Sb+(Mg+Ms)/Sb+Msd/Sbc
ft0=-Pe/A+Pe*e/St-(Mg+Ms)/St-Msd/Stc
fs0=-Msd/Sslab
print(f" 未加活載：梁底={fb0:.2f} 梁頂={ft0:.2f} 版頂={fs0:.2f}")
def Pmax(ft_allow,fcg,fcs_):
    M1=(ft_allow-fb0)*Sbc      # 梁底拉
    M2=(fcg+ft0)*Stc            # 梁頂壓 (ft0負)
    M3=(fcs_+fs0)*Sslab
    Ms_=[M1,M2,M3];return [m/(L/4) for m in Ms_]
for lab,ft,fcg,fcsl in [("現行規範 U類2.0√fc、壓0.60fc",2.0*sqrt(fc),0.6*fc,0.6*fcs),("考卷 3√fc、0.4fc",3*sqrt(fc),0.4*fc,0.4*fcs)]:
    P=Pmax(ft,fcg,fcsl);print(f" {lab}: P(梁底拉)={P[0]/1e3:.2f} tf, P(梁頂壓)={P[1]/1e3:.2f}, P(版頂壓)={P[2]/1e3:.2f}")
# sustained check 0.45fc under Pe+DL
print(f" 持續載重梁頂壓 {ft0:.1f} vs 0.45fc={0.45*fc}")
# 若用自算斷面性質
print("===== RC-2008-4")
fc=350;fcs=280;n=sqrt(fcs/fc);b=30;h=70;A=b*h;I=b*h**3/12;e=35-20;P=200000;L=1500
wg=A*gam;ws=90*15*gam;Mg=wg*L**2/8;Ms=ws*L**2/8
At,ybc,Ic=comp([(A,35,I),(90*n*15,77.5,90*n*15**3/12)])
fb0=-P/A-P*e/I*35+(Mg+Ms)/I*35
ft0=-P/A+P*e/I*35-(Mg+Ms)/I*35
print(f"Mg={Mg/1e5:.3f} Ms={Ms/1e5:.3f} comp A={At:.1f} yb={ybc:.2f} I={Ic:.0f}; 梁底0={fb0:.2f} 梁頂0={ft0:.2f}")
def wmax(ftb,fcg,fcsl):
    M1=(ftb-fb0)*Ic/ybc; M2=(fcg+ft0)*Ic/(70-ybc); M3=fcsl*Ic/(85-ybc)/n
    return [8*m/L**2*100/1e3 for m in (M1,M2,M3)]  # tf/m
for lab,ftb,fcg,fcsl in [("題設 無拉、0.45fc",0,0.45*fc,0.45*fcs),("現行 U類2.0√fc、0.60fc",2*sqrt(fc),0.6*fc,0.6*fcs)]:
    w=wmax(ftb,fcg,fcsl);print(f" {lab}: w(梁底)={w[0]:.3f} w(梁頂)={w[1]:.3f} w(版頂)={w[2]:.3f} tf/m → /0.9m = {min(w)/0.9:.3f} tf/m2")
# 對照：版重由合成斷面承受
fb0s=-P/A-P*e/I*35+Mg/I*35+Ms/Ic*ybc
print(f" [對照 有支撐] w(梁底,無拉)={8*(-fb0s)*Ic/ybc/L**2*100/1e3:.3f} tf/m")

print("===== RC-2009-4")
fc=350;Es=2.04e6;Ec=15000*sqrt(fc);fr=2.0*sqrt(fc)
As=4*6.47;Ap=4*1.77;Ac=900-As-Ap;fse=13200;fpy=16330
Pe=fse*Ap;ec0=-Pe/(Ac*Ec+As*Es)
for lab,Aeff in [("A=900/8(8支鋼材)",900/8),("A=900/4(僅D29)",900/4)]:
    fs=0.03/(1.08e-6*1.0*(3*Aeff)**(1/3));es=fs/Es
    fct=fr/(1+sqrt(500*es));fp=min(fse+Es*(es-ec0),fpy);fp_el=fse+Es*(es-ec0)
    N=As*fs+Ap*fp+Ac*fct
    print(f" {lab}: fs={fs:.0f} es={es:.6f} fct={fct:.2f} fp(彈性)={fp_el:.0f}→{fp:.0f} N={N/1e3:.1f} tf (鋼筋{As*fs/1e3:.1f}+鋼棒{Ap*fp/1e3:.1f}+混凝土{Ac*fct/1e3:.1f}); ec0={ec0:.6f}")

print("===== RC-2011-5")
Fi=250e3;F0=220e3;MG=30e5;MS=15e5;ML=70e5;n=6;Asp=24
A1,Zt1,Zb1,I1,e1=2500,40000,39000,1.8e6,25
A2,Zt2,Zb2,I2,e2=2800,41000,43000,1.9e6,24
A3,Zt3,Zb3,I3,e3=3900,137000,74000,4.3e6,39
ti=-Fi/A1+Fi*e1/Zt1-MG/Zt1;bi=-Fi/A1-Fi*e1/Zb1+MG/Zb1
tf=-F0/A1+F0*e1/Zt1-MG/Zt1-MS/Zt2-ML/Zt3
bf=-F0/A1-F0*e1/Zb1+MG/Zb1+MS/Zb2+ML/Zb3
fpi=Fi/Asp;fpf=F0/Asp+n*(MS*e2/I2+ML*e3/I3)
print(f" 施預力: 上={ti:.2f} 下={bi:.2f} 鋼腱={fpi:.0f}")
print(f" 全載重(F0在淨斷面): 上={tf:.2f} 下={bf:.2f} 鋼腱={fpf:.0f} (F0/Asp={F0/Asp:.0f})")
# 替代: 損失 30tf 作用於變換斷面
dF=F0-Fi
tf2=-Fi/A1+Fi*e1/Zt1-dF/A2+dF*e2/Zt2-MG/Zt1-MS/Zt2-ML/Zt3
bf2=-Fi/A1-Fi*e1/Zb1-dF/A2-dF*e2/Zb2+MG/Zb1+MS/Zb2+ML/Zb3
print(f" [替代 損失在變換斷面] 上={tf2:.2f} 下={bf2:.2f}")
# 替代: MG 也算 (鋼腱在施預力時含 MG 增量—後拉未灌漿不計)
print("===== RC-2012-1")
fc=350;fci=0.7*fc;b=30;h=90;A=b*h;S=b*h*h/6;Aps=3*0.9871;fpi=0.75*19000;Pi=fpi*Aps;e=30
w=A*2.3e-3;L=610;Mfix=w*L*L/2
lim_c=0.6*fci;lim_t=0.8*sqrt(fci)
for lab,sgn in [("鋼腱上偏",1),("鋼腱下偏",-1)]:
    for pos,M in [("自由端",0),("固定端",Mfix)]:
        top=-Pi/A-sgn*Pi*e/S+M/S; bot=-Pi/A+sgn*Pi*e/S-M/S
        print(f" {lab} {pos}: 上={top:.2f} 下={bot:.2f}")
print(f" Pi={Pi:.0f} w={w*100:.4f}kgf/m Mfix={Mfix/1e5:.3f}tf-m 容許壓={lim_c:.1f} 拉={lim_t:.2f}")
Mneed=(Pi*e/S-Pi/A-lim_t)*S;x=sqrt(2*Mneed/w);print(f" 下緣拉超限範圍 距自由端 x<{x/100:.2f} m")
fb=-Pi/A+Pi*e/S;ft=-Pi/A-Pi*e/S;yt=h*fb/(fb-ft);T=0.5*fb*yt*b;print(f" 自由端拉力區深 {yt:.2f} cm, T={T:.0f} kgf, As(0.5fy=2100)={T/2100:.2f} cm2 / (0.6fy)={T/2520:.2f}")

print("===== RC-2013-4")
fc=350;b=30;h=60;e=20;dp=h/2+e;Fe=65000;Aps=6.5;fpu=17100;Es=2.04e6;Ec=15000*sqrt(fc)
A=b*h;S=b*h*h/6;I=b*h**3/12;r2=I/A;fr=2.0*sqrt(fc)
Mcr=(fr+Fe/A+Fe*e/S)*S
rho=Aps/(b*dp);fps=fpu*(1-0.5*rho*fpu/fc);B=b1(fc);a=Aps*fps/(0.85*fc*b);c=a/B
E1=Fe/Aps/Es;E2=Fe/(A*Ec)*(1+e*e/r2);E3=0.003*(dp-c)/c
print(f" Mcr={Mcr/1e5:.3f} tf-m; fse={Fe/Aps:.0f} ({Fe/Aps/fpu:.3f}fpu); rho={rho:.6f} fps={fps:.0f} a={a:.3f} c={c:.3f} e1={E1:.5f} e2={E2:.5f} e3={E3:.5f} 合計={E1+E2+E3:.5f}; Mn={Aps*fps*(dp-a/2)/1e5:.2f}")
print(f"  不計e2 合計={E1+E3:.5f}")

print("===== RC-2014-4")
I=4.69e5;A=1100;S=I/30;e=19.8;Pi=70e3;Pe=60e3;L=1200
Mg=2.64*L**2/8;Mt=(2.64+11)*L**2/8;Mt2=11*L**2/8
for lab,P,M in [("施預力",Pi,Mg),("使用(1.364)",Pe,Mt),("使用(1.1含自重)",Pe,Mt2)]:
    print(f" {lab}: 上={-P/A+P*e/S-M/S:.2f} 下={-P/A-P*e/S+M/S:.2f}")
print(f" 容許: 傳遞壓0.60fci={0.6*300} 拉0.8√fci={0.8*sqrt(300):.2f} (端1.6√={1.6*sqrt(300):.2f}); 使用 U類拉2.0√fc={2*sqrt(420):.2f} 壓0.45fc={0.45*420} 0.60fc={0.6*420}")
print(f" 持續(Pe+自重) 上={-Pe/A+Pe*e/S-Mg/S:.2f}")
S2=15.63e4
print(f" [對照 S照印1.563e5] 使用 上={-Pe/A+Pe*e/S2-Mt/S2:.2f} 下={-Pe/A-Pe*e/S2+Mt/S2:.2f}")

print("===== RC-2018-4")
fc=420;b=35;h=70;dp=55;Aps=14;Fe=100e3;fpu=19000;Es=2e6;Ec=3.07e5;fr=2.0*sqrt(fc)
A=b*h;I=b*h**3/12;S=I/35;e=dp-35;r2=I/A;fse=Fe/Aps
Mcr=(fr+Fe/A+Fe*e/S)*S
print(f" fse={fse:.0f} = {fse/fpu:.3f} fpu (<0.5fpu → 近似式不適用); fr={fr:.2f}; Mcr(全斷面)={Mcr/1e5:.2f} tf-m")
# 變換斷面（套管灌漿視為混凝土、鋼腱 n）
n=Es/Ec;At,yb,It=comp([(A,35,I),((n-1)*Aps,h-dp,0)])
# 預力作用時（灌漿前）用淨斷面: 扣套管
Ad=3.14159*7.5**2/4;An,ybn,In=comp([(A,35,I),(-Ad,15,-3.14159*7.5**4/64)])
fbP=-Fe/An-Fe*(ybn-15)/In*ybn
Mcr2=(fr-fbP)*It/yb
print(f" [對照 預力用淨斷面、開裂用變換斷面] Mcr={Mcr2/1e5:.2f} (An={An:.1f} ybn={ybn:.2f}; At={At:.1f} yb={yb:.2f})")
B=b1(fc);E1=fse/Es;E2=Fe/(A*Ec)*(1+e*e/r2)
def fps_pci(eps):  # 270ksi 低鬆弛（PCI），按 fpu=19000 縮放
    return Es*eps if eps<=0.0086 else fpu*(1-0.04/(270*(eps-0.007)))*1.0 if False else min(Es*eps, fpu-0.04/(eps-0.007)*fpu/270)
def r(c):
    eps=E1+E2+0.003*(dp-c)/c;return 0.85*fc*b*B*c-Aps*fps_pci(eps)
c=brentq(r,1,50);a=B*c;eps=E1+E2+0.003*(dp-c)/c;fs=fps_pci(eps);Mn=Aps*fs*(dp-a/2)
print(f" 應變相容(PCI 曲線): c={c:.3f} a={a:.3f} eps_ps={eps:.5f} (E1={E1:.5f},E2={E2:.6f}) fps={fs:.0f} Mn={Mn/1e5:.2f} tf-m; Mn/Mcr={Mn/Mcr:.2f}")
for lab,k in [("考卷式0.5",0.5),("γp=0.28/β1",0.28/B),("γp=0.40/β1",0.40/B)]:
    rho=Aps/(b*dp);f=fpu*(1-k*rho*fpu/fc);a=Aps*f/(0.85*fc*b);print(f"  [{lab}] fps={f:.0f} a={a:.2f} Mn={Aps*f*(dp-a/2)/1e5:.2f}  εps={E1+E2+0.003*(dp-a/B)/(a/B):.5f}")
print("===== RC-2021-4")
fc=350;L=1200;Fi=300e3;Fe=0.7*Fi;gam=2.4e-3
beff=min(L/4,30+2*8*12,250);print(" beff",beff)
At,yb,It=comp([(30*50,25,30*50**3/12),(beff*12,56,beff*12**3/12)])
yt=62-yb;e=yb-10;MD=16*L**2/8
print(f" comp A={At:.0f} yb={yb:.3f} I={It:.0f} e={e:.3f} MD={MD/1e5:.2f}")
def wl(P,ftb,fct,M0):
    fb0=-P/At-P*e*yb/It+M0*yb/It; ft0=-P/At+P*e*yt/It-M0*yt/It
    M1=(ftb-fb0)*It/yb; M2=(fct+ft0)*It/yt
    return [8*m/L**2*100/1e3 for m in (M1,M2)],fb0,ft0
for lab,ftb,fcm in [("現行 U類2.0√fc / 0.60fc",2*sqrt(fc),0.6*fc),("考卷 1.6√fc / 0.6fc",1.6*sqrt(fc),0.6*fc)]:
    w,fb0,ft0=wl(Fe,ftb,fcm,MD);print(f" 讀法① {lab}: w(底拉)={w[0]:.3f} w(頂壓)={w[1]:.3f} tf/m; DL 下 底={fb0:.2f} 頂={ft0:.2f}")
print(f" 持續(Pe+D) 板頂/梁頂壓 vs 0.45fc={0.45*fc}")
# 傳遞階段（讀法①，Fi + D）
print(f" 傳遞 Fi+D: 底={-Fi/At-Fi*e*yb/It+MD*yb/It:.2f} 頂={-Fi/At+Fi*e*yt/It-MD*yt/It:.2f}")
# 讀法②: 預力+梁自重 on 預鑄梁, 其餘 on composite
Ab=1500;Ib=30*50**3/12;eb=15;wg=Ab*gam;Mg=wg*L**2/8;Mrest=MD-Mg
fb0=-Fe/Ab-Fe*eb*25/Ib+Mg*25/Ib+Mrest*yb/It
w2=(2*sqrt(fc)-fb0)*It/yb*8/L**2*100/1e3;w2e=(1.6*sqrt(fc)-fb0)*It/yb*8/L**2*100/1e3
print(f" [讀法② 預力+梁重於預鑄梁、其餘靜載於合成] w(底拉,2.0√)={w2:.3f} w(1.6√)={w2e:.3f}")
print("===== RC-2023-4")
fc=420;fy=4200;b=100;d=22;h=25;Aps=1.47*5;fse=11000;fpu=19000;fpy=0.85*fpu
rho=Aps/(b*d);fps=min(fse+700+fc/(300*rho),fpy,fse+2100)
for lab,As in [("As=0.004Act",0.004*b*h/2),("不計普通鋼筋",0)]:
    T=Aps*fps+As*fy;a=T/(0.85*fc*b);B=b1(fc);c=a/B;Mn=T*(d-a/2)
    print(f" {lab}: As={As:.2f} rho_p={rho:.6f} fps={fps:.0f} a={a:.3f} c={c:.3f} et={0.003*(d-c)/c:.4f} Mn={Mn/1e5:.3f} tf-m/m")
