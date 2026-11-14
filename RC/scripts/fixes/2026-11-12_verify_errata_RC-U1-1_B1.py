import math
mis=[]
def chk(tag,name,calc,pub,tol):
    ok=abs(calc-pub)<=tol
    print(f"{tag:10s} {name:12s} calc={calc:.6g} pub={pub} {'OK' if ok else 'MISMATCH'}")
    if not ok: mis.append((tag,name))
Es,ecu=2.04e6,0.003
def phi_t(et,ey=0.002): return 0.9 if et>=0.005 else 0.65+(et-0.002)*250/3
# RC-2002-4
b,d,dp,fc,fy,As,Asp=30,60,7,350,4200,50.70,10.14; B=0.80
a=(As*fy-Asp*(fy-0.85*fc))/(0.85*fc*b); c=a/B
chk('2002-4','a',a,19.43,0.005); chk('2002-4','c',c,24.29,0.01)
chk('2002-4',"e's",ecu*(c-dp)/c,0.002135,5e-7)
et=ecu*(d-c)/c; chk('2002-4','et',et,0.00441,5e-6)
Mn=(0.85*fc*b*a*(d-a/2)+Asp*(fy-0.85*fc)*(d-dp))/1e5; chk('2002-4','Mn',Mn,108.2,0.05)
rb=0.85*B*fc/fy*6120/(6120+fy); chk('2002-4','0.75rb',0.75*rb,0.02521,1e-5)
ph=phi_t(et); chk('2002-4','phi',ph,0.851,5e-4); chk('2002-4','phiMn',ph*Mn,92.1,0.05)
chk('2002-4','phi(0.483+83.3et)',0.483+83.3*et,0.851,1e-3)
# cross path: moment about NA
Mn2=(0.85*fc*b*a*(c-a/2)+Asp*(fy-0.85*fc)*(c-dp)+As*fy*(d-c))/1e5; chk('2002-4','Mn(about NA)',Mn2,108.2,0.05)
# RC-2011-2
fc=350;bf,hf,bw,d=80,10,40,100;ey=fy/Es;n=Es/(15000*math.sqrt(fc))
cb=6120/(6120+fy)*d; ab=B*cb; Cb=0.85*fc*(bf*hf+bw*(ab-hf)); Asb=Cb/fy; As=0.9*Asb
chk('2011-2','cb',cb,59.30,0.005); chk('2011-2','ab',ab,47.44,0.005); chk('2011-2','Cb',Cb,683558,1); chk('2011-2','Asb',Asb,162.75,0.005); chk('2011-2','As',As,146.48,0.005)
a=hf+(As*fy/(0.85*fc)-bf*hf)/bw; chk('2011-2','a',a,41.70,0.005)
ar=round(a,2); cu=ar/B; chk('2011-2','cu',cu,52.13,0.006)
et=ecu*(d-cu)/cu; chk('2011-2','et',et,0.002755,5e-7)
ph=0.65+0.25*(et-ey)/(0.005-ey); chk('2011-2','phi',ph,0.7092,5e-5)
Mn=(0.85*fc*bw*ar*(d-ar/2)+0.85*fc*(bf-bw)*hf*(d-hf/2))/1e5; chk('2011-2','Mn',Mn,505.8,0.05); chk('2011-2','phiMn',ph*Mn,358.7,0.05)
# cross: Mn about centroid of compression? use exact a -> same within 0.1
Mn_ex=(0.85*fc*bw*a*(d-a/2)+0.85*fc*(bf-bw)*hf*(d-hf/2))/1e5; chk('2011-2','Mn(exact a)',Mn_ex,505.8,0.1)
qa=bw/2; qb=(bf-bw)*hf+n*As; qc=-((bf-bw)*hf*hf/2+n*As*d); x=(-qb+math.sqrt(qb*qb-4*qa*qc))/(2*qa)
chk('2011-2','kyd',x,45.63,0.005)
# cross: direct first moment check
fm=bf*hf*(x-hf/2)+bw*(x-hf)**2/2-n*As*(d-x); chk('2011-2','1st moment',fm,0,1e-6)
py=round(ey,6)/(d-round(x,2)); pu=ecu/cu; chk('2011-2','phiy e5',py*1e5,3.787,5e-4); chk('2011-2','phiu e5',pu*1e5,5.755,5e-4); chk('2011-2','mu',pu/py,1.52,0.005)
rb=0.85*B*fc/fy*6120/(6120+fy); chk('2011-2','Asb rect+Asf',rb*bw*d+0.85*fc*(bf-bw)*hf/fy,162.75,0.03)
# RC-2005-2
fc=280;b,bw,hf,d=120,25,12,50;B=0.85
c=3/7*d; am=B*c; Cm=0.85*fc*(b-bw)*hf+0.85*fc*bw*am; Asm=Cm/fy; As=Asm/2
chk('2005-2','cmax',c,21.43,0.005); chk('2005-2','amax',am,18.21,0.005); chk('2005-2','Cmax',Cm,379695,1); chk('2005-2','Asmax',Asm,90.40,0.005); chk('2005-2','As',As,45.20,0.005)
a=As*fy/(0.85*fc*b); chk('2005-2','a',a,6.65,0.005); cc=a/B; chk('2005-2','c',cc,7.82,0.005)
et=ecu*(d-cc)/cc; chk('2005-2','et',et,0.0162,5e-5)
Mn=As*fy*(d-a/2)/1e5; chk('2005-2','Mn',Mn,88.61,0.005); pM=0.9*Mn; chk('2005-2','phiMn',pM,79.75,0.005)
Wu=8*pM/81; chk('2005-2','Wu',Wu,7.88,0.005); wL=(Wu-1.2*0.75)/1.6; chk('2005-2','wL',wL,4.36,0.005)
# cross: T-beam general formula with exact strain compat at et=0.004 -> check strain
cchk=ecu*(d-c)/c; chk('2005-2','et@cmax',cchk,0.004,1e-9)
# old reading values in table
cb=6120/10320*d; ab=B*cb; Asb=(0.85*fc*(b-bw)*hf+0.85*fc*bw*ab)/fy; chk('2005-2','old Asb',Asb,100.3,0.05)
As0=0.75*Asb/2; a0=As0*fy/(0.85*fc*b); pM0=0.9*As0*fy*(d-a0/2)/1e5; chk('2005-2','old phiMn',pM0,67.16,0.01)
chk('2005-2','old wL',(8*pM0/81-1.4*0.75)/1.7,3.28,0.005); chk('2005-2','mixed wL',(Wu-1.4*0.75)/1.7,4.02,0.005)
chk('2005-2','web-only cap',0.85*fc*bw*am/fy,25.8,0.05)
print('MISMATCHES:',len(mis),mis)
